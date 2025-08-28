import json
from openai import OpenAI
from cleanlab_codex.client import Client as CleanlabClient

from tools import tools, TOOL_FUNCTIONS

class SalesAgent:
    def __init__(self, openai_api_key: str, cleanlab_project=None):
        self.openai_api_key = openai_api_key
        self.cleanlab_project = cleanlab_project
        self.llm_client = OpenAI(api_key=openai_api_key)
        
        # System prompt for the agent
        self.system_prompt = {
            "role": "system",
            "content": """
You are AgentForce, a highly capable sales assistant and CRM expert. You are professional, proactive, and results-driven.

Available tools:
""" + "\n".join(f"- {t['function']['name']}: {t['function']['description']}" for t in tools) + """

Your capabilities include:
- Lead management and qualification
- Opportunity tracking and pipeline management
- Sales analytics and KPI reporting
- Email generation and follow-up scheduling
- Customer relationship management

Instructions:
1. Think step by step about what the user needs
2. Use the most appropriate tools to gather information or perform actions
3. You can use multiple tools in sequence to fully address complex requests
4. After getting tool results, analyze them and decide if you need more information
5. Provide comprehensive, helpful responses with specific details
6. Always prioritize customer satisfaction and sales results

IMPORTANT - Context Handling:
- Pay close attention to the conversation history
- When users make follow-up requests, refer back to previous messages for missing context
- For lead searches, if a user previously mentioned criteria, use that information for follow-up queries
- If you're missing required parameters, ask the user to clarify rather than making assumptions
- Always maintain context from previous tool calls and results

Example conversation flow:
User: "Search for qualified leads from TechCorp"
Assistant: [searches for qualified leads from TechCorp]
User: "Create a follow-up email for the first one"
Assistant: [uses the lead information from previous query to generate email]

Always be proactive and helpful. If a user asks about a lead, also suggest next steps. 
If they're creating a lead, remind them to schedule follow-ups. Provide actionable insights.

Use a professional but friendly tone. Be concise but thorough. Focus on driving sales results.
"""
        }
    
    def call_openai(self, messages: list, **kwargs):
        """Call OpenAI API with error handling"""
        try:
            resp = self.llm_client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=messages,
                tools=tools,
                **kwargs
            )
            return resp.choices[0].message
        except Exception as e:
            raise Exception(f"OpenAI API Error: {str(e)}")
    
    def run_cleanlab_validation(self, query: str, messages: list, response, thread_id: str, tools=None, metadata=None):
        """Run Cleanlab validation if available"""
        if not self.cleanlab_project:
            return {"should_guardrail": False, "expert_answer": None, "error": "Cleanlab not available"}
        
        try:
            # Extract the response content as a string for Cleanlab validation
            response_content = response.content
            
            validate_params = {
                "response": response_content,  # Pass the response content as a string
                "query": query,
                "context": "",
                "messages": messages,
                "metadata": metadata or {"integration": "sales-support-streamlit", "thread_id": thread_id},
                "tools": tools
            }
            
            vr = self.cleanlab_project.validate(**validate_params)
            return {
                "should_guardrail": vr.should_guardrail,
                "expert_answer": vr.expert_answer,
                "escalated_to_sme": getattr(vr, 'escalated_to_sme', False)
            }
        except Exception as e:
            return {"should_guardrail": False, "expert_answer": None, "error": str(e)}
    
    def process_message(self, user_input: str, history: list, thread_id: str):
        """Process a user message and return response"""
        
        # Add user input to history only if it's not already the last message
        if not history or not (history[-1].get("role") == "user" and history[-1].get("content") == user_input):
            history.append({"role": "user", "content": user_input})
        
        # Query the LLM
        try:
            response = self.call_openai(history, temperature=0.7)
        except Exception as e:
            raise e
        
        # Cleanlab validation
        try:
            validation_result = self.run_cleanlab_validation(
                query=user_input,
                messages=history,
                response=response, 
                tools=tools,
                thread_id=thread_id
            )
        except Exception as e:
            validation_result = {"should_guardrail": False, "expert_answer": None, "error": str(e)}
        
        final_response = response
        
        # Convert message object to dict format for history
        assistant_message = {
            "role": final_response.role,
            "content": final_response.content,
        }
        if hasattr(final_response, 'tool_calls') and final_response.tool_calls:
            assistant_message["tool_calls"] = final_response.tool_calls
        
        # Add the LLM response to history
        history.append(assistant_message)
        
        # Check if there are tool calls
        if not final_response.tool_calls:
            # No tool calls - conversation is complete
            return history, False, final_response.content, validation_result
        else:
            # Handle tool calls
            tools_for_print = []
            for tool_call in final_response.tool_calls:
                args = json.loads(tool_call.function.arguments)
                tool_response = TOOL_FUNCTIONS[tool_call.function.name](**args) if tool_call.function.name in TOOL_FUNCTIONS else {"error": f"Tool {tool_call.function.name} not implemented yet"}
                
                tool_dict = {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(tool_response),
                }
                history.append(tool_dict)
                tools_for_print.append(tool_dict)
            
            # Return with continue=True since we executed tools
            return history, True, f"🔧 Executed tools: {tools_for_print}", validation_result
