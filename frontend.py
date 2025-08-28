import streamlit as st

# Must be the first Streamlit command
st.set_page_config(
    page_title="AgentForce - Sales Support Agent",
    page_icon="💼",
    layout="wide"
)

import os
import time
import json
import uuid
import random
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
from openai import OpenAI
from cleanlab_codex.client import Client as CleanlabClient

# Import from our separated modules
from tools import tools, TOOL_FUNCTIONS
from backend import SalesAgent

# Load environment variables
load_dotenv()

# SECURE: Use Streamlit secrets or environment variables
def get_api_keys():
    """Securely retrieve API keys from Streamlit secrets or environment variables"""
    try:
        # Try Streamlit secrets first (for Streamlit Cloud deployment)
        openai_key = st.secrets.get("OPENAI_API_KEY")
        codex_key = st.secrets.get("CODEX_API_KEY")
        project_id = st.secrets.get("CLEANLAB_PROJECT_ID")
    except:
        # Fallback to environment variables (for local development)
        openai_key = os.getenv("OPENAI_API_KEY")
        codex_key = os.getenv("CODEX_API_KEY")
        project_id = os.getenv("CLEANLAB_PROJECT_ID")
    
    return openai_key, codex_key, project_id

# Get API keys securely
OPENAI_API_KEY, CODEX_API_KEY, CLEANLAB_PROJECT_ID = get_api_keys()

# Validate that required keys are present
if not OPENAI_API_KEY:
    st.error("🚨 **Missing OpenAI API Key!** Please set OPENAI_API_KEY in your secrets or environment variables.")
    st.stop()

if not CODEX_API_KEY:
    st.warning("⚠️ **Missing Codex API Key!** Cleanlab validation will be disabled.")

# Set environment variables securely (only if keys exist)
if CODEX_API_KEY:
    os.environ["CODEX_API_KEY"] = CODEX_API_KEY
if OPENAI_API_KEY:
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# Use default project ID if not provided
if CLEANLAB_PROJECT_ID:
    os.environ["CLEANLAB_PROJECT_ID"] = CLEANLAB_PROJECT_ID

if not CLEANLAB_PROJECT_ID:
    st.warning("⚠️ **Missing Cleanlab Project ID!** Cleanlab validation will be disabled.")

# Initialize Cleanlab client (with error handling)
@st.cache_resource
def get_cleanlab_client():
    try:
        cl_client = CleanlabClient()
        return cl_client.get_project(CLEANLAB_PROJECT_ID)
    except Exception as e:
        st.warning(f"⚠️ Cleanlab client initialization failed: {str(e)}")
        return None

cl_project = get_cleanlab_client()

# Initialize the SalesAgent
@st.cache_resource
def get_sales_agent():
    agent = SalesAgent(OPENAI_API_KEY, cl_project)
    return agent

agent = get_sales_agent()

# System prompt for conversation history
SYSTEM_PROMPT = agent.system_prompt

def parse_cleanlab_validation(validation_result):
    """Parse Cleanlab validation results and extract all available data"""
    if not validation_result or not isinstance(validation_result, dict):
        return {}
    
    parsed_data = {
        "should_guardrail": validation_result.get("should_guardrail", False),
        "expert_answer": validation_result.get("expert_answer"),
        "escalated_to_sme": validation_result.get("escalated_to_sme", False)
    }
    
    # Try multiple ways to access the validation object
    validation_obj = None
    if validation_result.get("validation_object"):
        validation_obj = validation_result["validation_object"]
    elif validation_result.get("raw_validation_response"):
        validation_obj = validation_result["raw_validation_response"]
    
    # Debug: Print what we found
    print(f"Validation result keys: {list(validation_result.keys())}")
    print(f"Validation object found: {validation_obj is not None}")
    
    if validation_obj:
        try:
            # Extract eval_scores - this is where the detailed scores are
            if hasattr(validation_obj, 'eval_scores') and validation_obj.eval_scores:
                scores_dict = {}
                for score_name, score_obj in validation_obj.eval_scores.items():
                    if hasattr(score_obj, 'score'):
                        scores_dict[score_name] = score_obj.score
                    else:
                        scores_dict[score_name] = str(score_obj)
                parsed_data["eval_scores"] = scores_dict
                
                # Also try to extract additional score details
                detailed_scores = {}
                for score_name, score_obj in validation_obj.eval_scores.items():
                    detailed_scores[score_name] = {}
                    if hasattr(score_obj, 'score'):
                        detailed_scores[score_name]['score'] = score_obj.score
                    if hasattr(score_obj, 'triggered'):
                        detailed_scores[score_name]['triggered'] = score_obj.triggered
                    if hasattr(score_obj, 'triggered_escalation'):
                        detailed_scores[score_name]['triggered_escalation'] = score_obj.triggered_escalation
                    if hasattr(score_obj, 'triggered_guardrail'):
                        detailed_scores[score_name]['triggered_guardrail'] = score_obj.triggered_guardrail
                    if hasattr(score_obj, 'failed'):
                        detailed_scores[score_name]['failed'] = score_obj.failed
                    if hasattr(score_obj, 'log'):
                        detailed_scores[score_name]['log'] = score_obj.log
                parsed_data["detailed_scores"] = detailed_scores
            
            # Extract deterministic_guardrails_results
            if hasattr(validation_obj, 'deterministic_guardrails_results') and validation_obj.deterministic_guardrails_results:
                parsed_data["guardrail_results"] = validation_obj.deterministic_guardrails_results
            
            # Extract log_id
            if hasattr(validation_obj, 'log_id') and validation_obj.log_id:
                parsed_data["log_id"] = validation_obj.log_id
            
            # Extract is_bad_response
            if hasattr(validation_obj, 'is_bad_response'):
                parsed_data["is_bad_response"] = validation_obj.is_bad_response
            
            # Extract any other available attributes
            for attr in ['confidence', 'risk_level', 'flags', 'metadata']:
                if hasattr(validation_obj, attr):
                    value = getattr(validation_obj, attr)
                    if value is not None:
                        parsed_data[attr] = value
                        
        except Exception as e:
            st.error(f"Error parsing validation results: {e}")
    
    return parsed_data

# Streamlit UI
def main():
    # Initialize session state FIRST - before any other code
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "history" not in st.session_state:
        st.session_state.history = [SYSTEM_PROMPT]
    
    if "thread_id" not in st.session_state:
        st.session_state.thread_id = uuid.uuid4().hex
    
    st.title("AgentForce - Sales Support Agent")
    st.markdown("*CRM and sales management assistant*")
    
    # Cleanlab project link (minimal)
    if CLEANLAB_PROJECT_ID:
        codex_url = f"https://codex.cleanlab.ai/projects/{CLEANLAB_PROJECT_ID}/"
        st.caption(f"Cleanlab Project for AI safety controls and observability: [View Project]({codex_url})")
    
    # Simple sample queries - Show when no conversation has started
    if len(st.session_state.messages) == 0:
        st.markdown("---")
        st.markdown("**Try these realistic multi-turn queries:**")
        
        sample_queries = [
            "Show me qualified leads this month, their total revenue, and all their pending tasks",
            "Search for customers with status Active and show me their details",
            "Get a pipeline report by stage and show me the total value"
        ]
        
        for query in sample_queries:
            if st.button(query, key=f"main_{hash(query)}", use_container_width=True):
                st.session_state.example_query = query
                st.rerun()
        
        st.markdown("---")
    
    # Minimal sidebar
    with st.sidebar:
        st.header("Conversation")
        
        if st.button("New Conversation"):
            st.session_state.messages = []
            st.session_state.history = [SYSTEM_PROMPT]
            st.session_state.thread_id = uuid.uuid4().hex
            st.rerun()
        
        st.caption(f"Thread: {st.session_state.thread_id[:8]}...")
        
        # Status indicators (minimal)
        if not OPENAI_API_KEY:
            st.error("OpenAI API Key Missing")
        if not cl_project:
            st.caption("Cleanlab: Disabled")
        
        # Available tools
        st.header("Available Tools")
        tool_categories = {
            "Lead Management": [
                ("search_leads", "Search for qualified leads from TechCorp"),
                ("create_lead", "Create a new lead: John Doe from ABC Corp"),
                ("update_lead_status", "Update LEAD001 status to Qualified")
            ],
            "Opportunities": [
                ("get_opportunity_details", "Show me details for OPP001"),
                ("create_opportunity", "Create opportunity for LEAD001: Software License"),
                ("update_opportunity", "Update OPP002 stage to Negotiation")
            ],
            "Customers": [
                ("search_customers", "Search for customers with status Active"),
                ("get_customer_details", "Show customer details for CUST001")
            ],
            "Analytics": [
                ("get_sales_analytics", "Show me sales analytics for this month"),
                ("get_pipeline_report", "Get pipeline report by stage"),
                ("get_qualified_leads_summary", "Show me qualified leads this month with revenue and tasks"),
                ("get_customers_closed_summary", "Show me customers closed last month and their total revenue")
            ],
            "Activities": [
                ("search_activities", "When did we last meet with Innovation Corp?"),
                ("schedule_follow_up", "Schedule follow-up for LEAD002 on 2024-02-15")
            ],
            "Communication": [
                ("generate_sales_email", "Generate follow-up email for LEAD001"),
                ("schedule_follow_up", "Schedule follow-up for LEAD002 on 2024-02-15")
            ],
            "Tasks": [
                ("get_tasks", "Show me all pending tasks"),
                ("complete_task", "Complete task TASK001")
            ]
        }
        
        for category, tool_list in tool_categories.items():
            with st.expander(category):
                for tool_name, sample_question in tool_list:
                    st.write(f"• **{tool_name}**")
                    st.caption(f"  *e.g., \"{sample_question}\"*")
    
    # Main chat interface
    chat_container = st.container()
    
    # Display chat messages
    with chat_container:
        for i, message in enumerate(st.session_state.messages):
            with st.chat_message(message["role"]):
                if message["role"] == "assistant":
                    st.markdown(message["content"])
                    
                    # Show Cleanlab validation results in a dropdown
                    if "validation" in message and message["validation"]:
                        validation = parse_cleanlab_validation(message["validation"])
                        
                        # Create a clean dropdown for validation details
                        with st.expander("🔍 View AI Safety Validation Results", expanded=False):
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.subheader("Safety Assessment")
                                
                                # Guardrail status
                                guardrail_status = "🛡️ **Guarded**" if validation.get("should_guardrail") else "✅ **Safe**"
                                st.markdown(f"**Status:** {guardrail_status}")
                                
                                # Escalation status
                                if validation.get("escalated_to_sme"):
                                    st.markdown("**Escalation:** 🔴 **Escalated to Expert**")
                                else:
                                    st.markdown("**Escalation:** ✅ **No Escalation Needed**")
                                
                                # Error handling
                                if validation.get("error"):
                                    st.error(f"**Error:** {validation['error']}")
                            
                            with col2:
                                st.subheader("Validation Details")
                                
                                # Show evaluation scores if available (these are the actual scores from Cleanlab)
                                if validation.get("eval_scores"):
                                    st.markdown("**Evaluation Scores:**")
                                    for eval_name, eval_score in validation["eval_scores"].items():
                                        if isinstance(eval_score, (int, float)):
                                            st.markdown(f"- {eval_name}: {eval_score:.3f}")
                                        else:
                                            st.markdown(f"- {eval_name}: {eval_score}")
                                
                                # Show detailed scores with pass/fail status
                                if validation.get("detailed_scores"):
                                    st.markdown("**Score Status:**")
                                    for score_name, score_details in validation["detailed_scores"].items():
                                        if 'score' in score_details and 'failed' in score_details:
                                            status = "❌ Failed" if score_details['failed'] else "✅ Passed"
                                            st.markdown(f"- {score_name}: {score_details['score']:.3f} ({status})")
                                
                                # Show guardrail results if available
                                if validation.get("guardrail_results"):
                                    st.markdown("**Guardrail Results:**")
                                    for guardrail_name, guardrail_result in validation["guardrail_results"].items():
                                        st.markdown(f"- {guardrail_name}: {guardrail_result}")
                                
                                # Show if response was flagged as bad
                                if validation.get("is_bad_response") is not None:
                                    bad_status = "🔴 **Flagged as Bad**" if validation["is_bad_response"] else "✅ **Good Response**"
                                    st.markdown(f"**Response Quality:** {bad_status}")
                                
                                # Show confidence if available
                                if validation.get("confidence"):
                                    st.markdown(f"**Confidence:** {validation['confidence']:.3f}")
                                
                                # Show risk level if available
                                if validation.get("risk_level"):
                                    st.markdown(f"**Risk Level:** {validation['risk_level']}")
                                
                                # Show expert answer if available
                                if validation.get("expert_answer"):
                                    st.markdown("**Expert Answer:**")
                                    st.info(validation["expert_answer"])
                            
                            # Additional metadata
                            if validation.get("validation_id") or validation.get("timestamp"):
                                st.markdown("---")
                                if validation.get("validation_id"):
                                    st.caption(f"**Validation ID:** {validation['validation_id']}")
                                if validation.get("timestamp"):
                                    st.caption(f"**Timestamp:** {validation['timestamp']}")
                else:
                    st.markdown(message["content"])
    
    # Handle example query from sidebar
    if "example_query" in st.session_state:
        user_input = st.session_state.example_query
        del st.session_state.example_query
    else:
        # Chat input
        user_input = st.chat_input("Ask about leads, opportunities, or sales analytics...")
    
    # Process user input
    if user_input:
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Show user message immediately
        with st.chat_message("user"):
            st.markdown(user_input)
        
        # Process with SalesAgent
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            tool_placeholder = st.empty()
            
            max_iterations = 5
            current_history = st.session_state.history.copy()
            
            try:
                for iteration in range(max_iterations):
                    with st.spinner(f"🤔 Thinking... (Step {iteration + 1})"):
                        result = agent.process_message(
                            user_input, current_history, st.session_state.thread_id
                        )
                        history, continue_loop, response, extra_info = result[:4]
                        tool_calls_info = result[4] if len(result) > 4 else []
                        current_history = history
                    
                    # Show tool calls and their parameters (regardless of loop status)
                    if tool_calls_info:
                        with st.expander(f"🔧 Agent Tool Calls (Step {iteration + 1})", expanded=True):
                            for i, tool_call in enumerate(tool_calls_info):
                                st.markdown(f"**Tool {i+1}: {tool_call['tool_name']}**")
                                
                                # Display arguments
                                if tool_call['arguments']:
                                    st.markdown("**Parameters:**")
                                    for key, value in tool_call['arguments'].items():
                                        st.markdown(f"- `{key}`: `{value}`")
                                
                                # Display response summary
                                if isinstance(tool_call['response'], dict):
                                    if 'error' in tool_call['response']:
                                        st.error(f"❌ Error: {tool_call['response']['error']}")
                                    elif 'total_count' in tool_call['response']:
                                        st.success(f"✅ Found {tool_call['response']['total_count']} results")
                                    elif 'status' in tool_call['response']:
                                        st.success(f"✅ {tool_call['response']['status']}")
                                    else:
                                        st.success("✅ Tool executed successfully")
                                else:
                                    st.success("✅ Tool executed successfully")
                                
                                st.markdown("---")
                    
                    if continue_loop:
                        # Show tool usage - match the working pattern
                        tool_placeholder.info(f"🔧 **Step {iteration + 1}:** {response}")
                        
                        # Show validation for intermediate steps
                        if isinstance(extra_info, dict):
                            if extra_info.get("should_guardrail"):
                                st.warning(f"🛡️ **Safety Alert (Step {iteration + 1}):** Tool selection was flagged by Cleanlab validation")
                            
                            with st.expander(f"🛡️ Cleanlab Validation (Step {iteration + 1})"):
                                st.json(extra_info)
                        elif isinstance(extra_info, str):
                            with st.expander(f"Tool Result (Step {iteration + 1})"):
                                st.code(extra_info, language="json")
                    else:
                        # Final response
                        message_placeholder.markdown(response)
                        
                        # Show validation info - match the working pattern
                        if isinstance(extra_info, dict):
                            if extra_info.get("should_guardrail"):
                                st.warning("🛡️ **Safety Alert:** This response was flagged by Cleanlab validation")
                            
                            with st.expander("🛡️ Cleanlab Validation Results"):
                                st.json(extra_info)
                        
                        # Add to session state
                        assistant_message = {
                            "role": "assistant", 
                            "content": response,
                            "validation": extra_info if isinstance(extra_info, dict) else None
                        }
                        st.session_state.messages.append(assistant_message)
                        break
                
                # Update session history
                st.session_state.history = current_history
            
            except Exception as e:
                st.error(f"🚨 Error processing request: {str(e)}")
                st.info("Please try again or contact support if the issue persists.")
        
        st.rerun()

if __name__ == "__main__":
    main()
