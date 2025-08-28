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
            "Show me the pipeline report by stage, then create follow-up emails for all leads in the Negotiation stage",
            "Search for active customers, show me their details, and schedule follow-up tasks for any with opportunities closing this month"
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
                ("get_qualified_leads_summary", "Show me qualified leads this month with revenue and tasks")
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
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                if message["role"] == "assistant":
                    st.markdown(message["content"])
                    # Show validation info if available (minimal)
                    if "validation" in message and message["validation"] and message["validation"].get("should_guardrail"):
                        st.caption("⚠️ Response flagged by safety validation")
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
                        history, continue_loop, response, extra_info = agent.process_message(
                            user_input, current_history, st.session_state.thread_id
                        )
                        current_history = history
                    
                    if continue_loop:
                        # Show tool usage (minimal)
                        tool_placeholder.caption(f"Processing step {iteration + 1}...")
                        
                        # Show validation for intermediate steps (minimal)
                        if isinstance(extra_info, dict) and extra_info.get("should_guardrail"):
                            st.warning("Safety alert: Response flagged by validation")
                    else:
                        # Final response
                        message_placeholder.markdown(response)
                        
                        # Show validation info (minimal)
                        if isinstance(extra_info, dict) and extra_info.get("should_guardrail"):
                            st.warning("Safety alert: Response flagged by validation")
                        
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
