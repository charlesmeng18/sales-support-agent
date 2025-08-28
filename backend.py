import json
from openai import OpenAI
from cleanlab_codex.client import Client as CleanlabClient

from tools import tools, TOOL_FUNCTIONS

class SalesAgent:
    def __init__(self, openai_api_key: str, cleanlab_project=None):
        self.openai_api_key = openai_api_key
        self.cleanlab_project = cleanlab_project
        self.llm_client = OpenAI(api_key=openai_api_key)
        
        # Simplified system prompt for the agent
        self.system_prompt = {
            "role": "system",
            "content": """
You are AgentForce, a focused sales assistant and CRM expert. You help answer key sales questions efficiently.

Available tools:
""" + "\n".join(f"- {t['function']['name']}: {t['function']['description']}" for t in tools) + """

Your core capabilities:
- Customer analysis and reporting
- Pipeline management and forecasting
- Sales analytics and KPIs
- Customer relationship insights

Key query types you handle:
1. "Who are our customers closed last month?" - Use get_customers_closed_summary
2. "What are next steps with customer Y?" - Use get_customer_details
3. "Show me total pipeline of opportunities that are active and projected to close next month" - Use get_pipeline_report

Instructions:
1. Use the most appropriate tool for each query type
2. Provide clear, actionable insights from the data
3. Focus on the specific information requested
4. Be concise but thorough in your responses
5. Always include relevant metrics and next steps when appropriate

Example responses:
- For customer closed reports: Include total customers, revenue, and breakdown
- For customer details: Include opportunities, next steps, and account manager
- For pipeline reports: Include stage breakdown, values, and next month projections

Use a professional, helpful tone. Focus on driving sales insights and actionable information.
"""
        }
    
    def call_openai(self, messages: list, **kwargs):
        """Call OpenAI API with error handling"""
        try:
            resp = self.llm_client.chat.completions.create(
                model="gpt-4o",
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
            # Simple validate call - let the frontend handle all the parsing
            vr = self.cleanlab_project.validate(
                response=response.content,
                query=query,
                context="",
                messages=messages,
                metadata=metadata or {"integration": "sales-support-streamlit", "thread_id": thread_id},
                tools=tools
            )
            
            # Just return the raw validation result
            return vr
            
        except Exception as e:
            return {"should_guardrail": False, "expert_answer": None, "error": str(e)}
    
    def process_message(self, user_input: str, history: list, thread_id: str):
        """Process a user message and return response - simplified per-turn logic"""
        
        # Add user input to history
        if not history or not (history[-1].get("role") == "user" and history[-1].get("content") == user_input):
            history.append({"role": "user", "content": user_input})
        
        # Make LLM call
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
        
        # Apply guardrail if needed
        if hasattr(validation_result, 'should_guardrail') and validation_result.should_guardrail:
            if hasattr(validation_result, 'expert_answer') and validation_result.expert_answer:
                response_content = validation_result.expert_answer
            else:
                response_content = "🛡️ **Safety Alert**: I cannot provide a response to this request as it has been flagged by our safety systems."
        else:
            response_content = response.content
        
        # Add response to history
        history.append({
            "role": "assistant",
            "content": response_content,
            "tool_calls": getattr(response, 'tool_calls', None)
        })
        
        # Check if tools needed
        if not response.tool_calls:
            # No tools - conversation complete
            return history, False, response_content, validation_result
        else:
            # Execute tools
            tools_for_print = []
            tool_calls_info = []
            
            for tool_call in response.tool_calls:
                args = json.loads(tool_call.function.arguments)
                tool_response = TOOL_FUNCTIONS[tool_call.function.name](**args) if tool_call.function.name in TOOL_FUNCTIONS else {"error": f"Tool {tool_call.function.name} not implemented yet"}
                
                # Capture tool info for frontend
                tool_call_info = {
                    "tool_name": tool_call.function.name,
                    "arguments": args,
                    "response": tool_response
                }
                tool_calls_info.append(tool_call_info)
                
                # Add tool response to history
                tool_dict = {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(tool_response),
                }
                history.append(tool_dict)
                tools_for_print.append(tool_dict)
            
            # Return with continue=True to indicate tools were executed
            return history, True, f"🔧 Executed tools: {tools_for_print}", validation_result, tool_calls_info
