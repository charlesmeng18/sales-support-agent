import json
import random
import datetime
import uuid
from datetime import datetime, timedelta

# Import from the separate sales database
from sales_db import sales_data, get_leads_by_status, get_opportunities_by_stage, get_tasks_by_status, get_customers_by_status, get_activities_by_lead

# SALES SUPPORT TOOLS
tools = [
    # Lead Management Tools
    {
        "type": "function",
        "function": {
            "name": "search_leads",
            "description": "Search and filter leads in the CRM by name, company, status, or source",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query for name, company, or email"},
                    "status": {"type": "string", "description": "Filter by lead status (New, Contacted, Qualified, etc.)"},
                    "source": {"type": "string", "description": "Filter by lead source (Website, LinkedIn, Referral, etc.)"}
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_lead",
            "description": "Create a new lead in the CRM system",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Contact person's name"},
                    "company": {"type": "string", "description": "Company name"},
                    "email": {"type": "string", "description": "Contact email address"},
                    "phone": {"type": "string", "description": "Contact phone number (optional)"},
                    "source": {"type": "string", "description": "Lead source (Website, LinkedIn, Referral, etc.)"},
                    "value": {"type": "integer", "description": "Estimated deal value in dollars"}
                },
                "required": ["name", "company", "email"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_lead_status",
            "description": "Update the status of a lead and add notes",
            "parameters": {
                "type": "object",
                "properties": {
                    "lead_id": {"type": "string", "description": "Lead ID to update"},
                    "new_status": {"type": "string", "description": "New status (New, Contacted, Qualified, Proposal, Closed Won, Closed Lost)"},
                    "notes": {"type": "string", "description": "Notes about the status change"}
                },
                "required": ["lead_id", "new_status"]
            }
        }
    },
    
    # Opportunity Management
    {
        "type": "function",
        "function": {
            "name": "get_opportunity_details",
            "description": "Get detailed information about sales opportunities and their associated leads",
            "parameters": {
                "type": "object",
                "properties": {
                    "opportunity_id": {"type": "string", "description": "Specific opportunity ID to look up"},
                    "lead_id": {"type": "string", "description": "Lead ID to find all associated opportunities"}
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_opportunity",
            "description": "Create a new sales opportunity",
            "parameters": {
                "type": "object",
                "properties": {
                    "lead_id": {"type": "string", "description": "Associated lead ID"},
                    "name": {"type": "string", "description": "Opportunity name"},
                    "stage": {"type": "string", "description": "Sales stage (Discovery, Proposal, Negotiation, Closed Won, Closed Lost)"},
                    "value": {"type": "integer", "description": "Deal value in dollars"},
                    "probability": {"type": "integer", "description": "Probability percentage (0-100)"},
                    "close_date": {"type": "string", "description": "Expected close date (YYYY-MM-DD)"},
                    "owner": {"type": "string", "description": "Sales rep assigned"}
                },
                "required": ["lead_id", "name", "stage", "value"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_opportunity",
            "description": "Update opportunity details and stage",
            "parameters": {
                "type": "object",
                "properties": {
                    "opportunity_id": {"type": "string", "description": "Opportunity ID to update"},
                    "stage": {"type": "string", "description": "New sales stage"},
                    "value": {"type": "integer", "description": "Updated deal value"},
                    "probability": {"type": "integer", "description": "Updated probability percentage"},
                    "close_date": {"type": "string", "description": "Updated close date"},
                    "notes": {"type": "string", "description": "Update notes"}
                },
                "required": ["opportunity_id"]
            }
        }
    },
    
    # Customer Management
    {
        "type": "function",
        "function": {
            "name": "search_customers",
            "description": "Search for existing customers in the CRM",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query for company name or contact"},
                    "status": {"type": "string", "description": "Filter by customer status (Active, Inactive, Churned)"}
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_customer_details",
            "description": "Get detailed customer information and history",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {"type": "string", "description": "Customer ID to look up"}
                },
                "required": ["customer_id"]
            }
        }
    },
    
    # Sales Analytics
    {
        "type": "function",
        "function": {
            "name": "get_sales_analytics",
            "description": "Get sales analytics, KPIs, and pipeline metrics",
            "parameters": {
                "type": "object",
                "properties": {
                    "timeframe": {"type": "string", "description": "Timeframe for analytics (week, month, quarter, year)"}
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_pipeline_report",
            "description": "Get detailed pipeline report with stage breakdown",
            "parameters": {
                "type": "object",
                "properties": {
                    "owner": {"type": "string", "description": "Filter by sales rep (optional)"},
                    "min_value": {"type": "integer", "description": "Minimum deal value filter"},
                    "max_value": {"type": "integer", "description": "Maximum deal value filter"}
                },
                "required": []
            }
        }
    },
    
    # Communication Tools
    {
        "type": "function",
        "function": {
            "name": "generate_sales_email",
            "description": "Generate personalized sales emails for leads",
            "parameters": {
                "type": "object",
                "properties": {
                    "lead_id": {"type": "string", "description": "Lead ID to generate email for"},
                    "email_type": {"type": "string", "description": "Type of email (follow_up, proposal, discovery)"}
                },
                "required": ["lead_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "schedule_follow_up",
            "description": "Schedule a follow-up task for a lead",
            "parameters": {
                "type": "object",
                "properties": {
                    "lead_id": {"type": "string", "description": "Lead ID to schedule follow-up for"},
                    "follow_up_date": {"type": "string", "description": "Date for follow-up (YYYY-MM-DD)"},
                    "notes": {"type": "string", "description": "Notes about the follow-up task"}
                },
                "required": ["lead_id", "follow_up_date"]
            }
        }
    },
    
    # Task Management
    {
        "type": "function",
        "function": {
            "name": "get_tasks",
            "description": "Get scheduled tasks and follow-ups",
            "parameters": {
                "type": "object",
                "properties": {
                    "lead_id": {"type": "string", "description": "Filter by lead ID (optional)"},
                    "due_date": {"type": "string", "description": "Filter by due date (YYYY-MM-DD)"},
                    "status": {"type": "string", "description": "Filter by task status (Pending, Completed, Overdue)"}
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "complete_task",
            "description": "Mark a task as completed",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {"type": "string", "description": "Task ID to complete"},
                    "completion_notes": {"type": "string", "description": "Notes about task completion"}
                },
                "required": ["task_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_qualified_leads_summary",
            "description": "Get comprehensive summary of qualified leads including revenue and pending tasks",
            "parameters": {
                "type": "object",
                "properties": {
                    "timeframe": {"type": "string", "description": "Timeframe for leads (this_month, last_month, this_quarter)"},
                    "include_revenue": {"type": "boolean", "description": "Include revenue calculations"},
                    "include_tasks": {"type": "boolean", "description": "Include pending tasks for leads"}
                },
                "required": []
            }
        }
    }
]

# TOOL IMPLEMENTATIONS
def search_leads(query: str = None, status: str = None, source: str = None) -> dict:
    """Search and filter leads based on criteria"""
    results = []
    for lead_id, lead in sales_data["leads"].items():
        if query and query.lower() not in f"{lead['name']} {lead['company']} {lead['email']}".lower():
            continue
        if status and lead['status'].lower() != status.lower():
            continue
        if source and lead['source'].lower() != source.lower():
            continue
        
        results.append({
            "lead_id": lead_id,
            **lead
        })
    
    return {
        "query": query,
        "filters": {"status": status, "source": source},
        "results": results,
        "total_count": len(results),
        "timestamp": datetime.now().isoformat()
    }

def create_lead(name: str, company: str, email: str, phone: str = None, source: str = "Manual", value: int = 0) -> dict:
    """Create a new lead in the CRM"""
    lead_id = f"LEAD{str(uuid.uuid4())[:8].upper()}"
    
    new_lead = {
        "name": name,
        "company": company,
        "email": email,
        "phone": phone or "Not provided",
        "status": "New",
        "value": value,
        "source": source,
        "created": datetime.now().strftime("%Y-%m-%d")
    }
    
    sales_data["leads"][lead_id] = new_lead
    
    return {
        "lead_id": lead_id,
        "lead": new_lead,
        "status": "Created Successfully",
        "timestamp": datetime.now().isoformat()
    }

def update_lead_status(lead_id: str, new_status: str, notes: str = None) -> dict:
    """Update lead status and add notes"""
    if lead_id not in sales_data["leads"]:
        return {"error": "Lead not found"}
    
    old_status = sales_data["leads"][lead_id]["status"]
    sales_data["leads"][lead_id]["status"] = new_status
    
    return {
        "lead_id": lead_id,
        "old_status": old_status,
        "new_status": new_status,
        "notes": notes,
        "status": "Updated Successfully",
        "timestamp": datetime.now().isoformat()
    }

def get_opportunity_details(opportunity_id: str = None, lead_id: str = None) -> dict:
    """Get detailed opportunity information"""
    if opportunity_id and opportunity_id in sales_data["opportunities"]:
        opp = sales_data["opportunities"][opportunity_id]
        lead = sales_data["leads"][opp["lead_id"]]
        return {
            "opportunity_id": opportunity_id,
            "opportunity": opp,
            "lead": lead,
            "timestamp": datetime.now().isoformat()
        }
    elif lead_id and lead_id in sales_data["leads"]:
        opportunities = [opp for opp in sales_data["opportunities"].values() if opp["lead_id"] == lead_id]
        return {
            "lead_id": lead_id,
            "opportunities": opportunities,
            "timestamp": datetime.now().isoformat()
        }
    
    return {"error": "Opportunity or lead not found"}

def create_opportunity(lead_id: str, name: str, stage: str, value: int, probability: int = 50, close_date: str = None, owner: str = None) -> dict:
    """Create a new sales opportunity"""
    if lead_id not in sales_data["leads"]:
        return {"error": "Lead not found"}
    
    opportunity_id = f"OPP{str(uuid.uuid4())[:8].upper()}"
    
    new_opportunity = {
        "lead_id": lead_id,
        "name": name,
        "stage": stage,
        "value": value,
        "probability": probability,
        "close_date": close_date or (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"),
        "owner": owner or "Unassigned",
        "created": datetime.now().strftime("%Y-%m-%d")
    }
    
    sales_data["opportunities"][opportunity_id] = new_opportunity
    
    return {
        "opportunity_id": opportunity_id,
        "opportunity": new_opportunity,
        "status": "Created Successfully",
        "timestamp": datetime.now().isoformat()
    }

def update_opportunity(opportunity_id: str, stage: str = None, value: int = None, probability: int = None, close_date: str = None, notes: str = None) -> dict:
    """Update opportunity details and stage"""
    if opportunity_id not in sales_data["opportunities"]:
        return {"error": "Opportunity not found"}
    
    opp = sales_data["opportunities"][opportunity_id]
    old_values = opp.copy()
    
    if stage:
        opp["stage"] = stage
    if value:
        opp["value"] = value
    if probability:
        opp["probability"] = probability
    if close_date:
        opp["close_date"] = close_date
    
    return {
        "opportunity_id": opportunity_id,
        "old_values": old_values,
        "new_values": opp,
        "notes": notes,
        "status": "Updated Successfully",
        "timestamp": datetime.now().isoformat()
    }

def search_customers(query: str = None, status: str = None) -> dict:
    """Search for existing customers in the CRM"""
    results = []
    for customer_id, customer in sales_data["customers"].items():
        if query and query.lower() not in f"{customer['name']} {customer['contact']} {customer['email']}".lower():
            continue
        if status and customer['status'].lower() != status.lower():
            continue
        
        results.append({
            "customer_id": customer_id,
            **customer
        })
    
    return {
        "query": query,
        "filters": {"status": status},
        "results": results,
        "total_count": len(results),
        "timestamp": datetime.now().isoformat()
    }

def get_customer_details(customer_id: str) -> dict:
    """Get detailed customer information and history"""
    if customer_id not in sales_data["customers"]:
        return {"error": "Customer not found"}
    
    customer = sales_data["customers"][customer_id]
    
    # Get associated opportunities
    opportunities = [opp for opp in sales_data["opportunities"].values() 
                    if opp.get("lead_id") and sales_data["leads"][opp["lead_id"]].get("company") == customer["name"]]
    
    return {
        "customer_id": customer_id,
        "customer": customer,
        "opportunities": opportunities,
        "total_opportunities": len(opportunities),
        "total_value": sum(opp["value"] for opp in opportunities),
        "timestamp": datetime.now().isoformat()
    }

def get_sales_analytics(timeframe: str = "month") -> dict:
    """Get sales analytics and KPIs"""
    total_leads = len(sales_data["leads"])
    qualified_leads = len([l for l in sales_data["leads"].values() if l["status"] == "Qualified"])
    total_opportunities = len(sales_data["opportunities"])
    total_value = sum(opp["value"] for opp in sales_data["opportunities"].values())
    weighted_value = sum(opp["value"] * opp["probability"] / 100 for opp in sales_data["opportunities"].values())
    
    return {
        "timeframe": timeframe,
        "total_leads": total_leads,
        "qualified_leads": qualified_leads,
        "qualification_rate": round(qualified_leads / total_leads * 100, 2) if total_leads > 0 else 0,
        "total_opportunities": total_opportunities,
        "total_pipeline_value": total_value,
        "weighted_pipeline_value": round(weighted_value, 2),
        "average_deal_size": round(total_value / total_opportunities, 2) if total_opportunities > 0 else 0,
        "timestamp": datetime.now().isoformat()
    }

def get_pipeline_report(owner: str = None, min_value: int = None, max_value: int = None) -> dict:
    """Get detailed pipeline report with stage breakdown"""
    opportunities = sales_data["opportunities"].values()
    
    # Apply filters
    if owner:
        opportunities = [opp for opp in opportunities if opp["owner"] == owner]
    if min_value:
        opportunities = [opp for opp in opportunities if opp["value"] >= min_value]
    if max_value:
        opportunities = [opp for opp in opportunities if opp["value"] <= max_value]
    
    # Group by stage
    stage_breakdown = {}
    for opp in opportunities:
        stage = opp["stage"]
        if stage not in stage_breakdown:
            stage_breakdown[stage] = {"count": 0, "value": 0, "weighted_value": 0}
        stage_breakdown[stage]["count"] += 1
        stage_breakdown[stage]["value"] += opp["value"]
        stage_breakdown[stage]["weighted_value"] += opp["value"] * opp["probability"] / 100
    
    return {
        "filters": {"owner": owner, "min_value": min_value, "max_value": max_value},
        "total_opportunities": len(opportunities),
        "total_value": sum(opp["value"] for opp in opportunities),
        "weighted_value": sum(opp["value"] * opp["probability"] / 100 for opp in opportunities),
        "stage_breakdown": stage_breakdown,
        "timestamp": datetime.now().isoformat()
    }

def generate_sales_email(lead_id: str, email_type: str = "follow_up") -> dict:
    """Generate personalized sales emails for leads"""
    if lead_id not in sales_data["leads"]:
        return {"error": "Lead not found"}
    
    lead = sales_data["leads"][lead_id]
    
    email_templates = {
        "follow_up": {
            "subject": f"Following up on {lead['company']} - Next Steps",
            "body": f"Hi {lead['name']},\n\nI hope this email finds you well. I wanted to follow up on our recent conversation about how our solution could benefit {lead['company']}.\n\nBased on what we discussed, I believe we can help you achieve your goals of [specific benefit].\n\nWould you be available for a 15-minute call this week to discuss this further?\n\nBest regards,\n[Your Name]\n[Your Title]\n[Company Name]"
        },
        "proposal": {
            "subject": f"Proposal for {lead['company']} - Custom Solution",
            "body": f"Hi {lead['name']},\n\nThank you for the opportunity to present a proposal for {lead['company']}.\n\nI've prepared a comprehensive solution that addresses your specific needs:\n\n• [Key Benefit 1]\n• [Key Benefit 2]\n• [Key Benefit 3]\n\nInvestment: ${lead['value']:,}\n\nI'm available to walk through this proposal and answer any questions you may have.\n\nBest regards,\n[Your Name]"
        },
        "discovery": {
            "subject": f"Discovery Call - Understanding {lead['company']}'s Needs",
            "body": f"Hi {lead['name']},\n\nThank you for your interest in our solution. I'd love to learn more about {lead['company']} and how we can help you achieve your objectives.\n\nI've scheduled a 30-minute discovery call to understand:\n\n• Your current challenges\n• Your goals and objectives\n• How our solution can help\n\nPlease let me know if this time works for you.\n\nBest regards,\n[Your Name]"
        }
    }
    
    template = email_templates.get(email_type, email_templates["follow_up"])
    
    return {
        "lead_id": lead_id,
        "lead_name": lead['name'],
        "company": lead['company'],
        "email_type": email_type,
        "subject": template["subject"],
        "body": template["body"],
        "timestamp": datetime.now().isoformat()
    }

def schedule_follow_up(lead_id: str, follow_up_date: str, notes: str = None) -> dict:
    """Schedule a follow-up task for a lead"""
    if lead_id not in sales_data["leads"]:
        return {"error": "Lead not found"}
    
    task_id = f"TASK{str(uuid.uuid4())[:8].upper()}"
    
    return {
        "task_id": task_id,
        "lead_id": lead_id,
        "lead_name": sales_data["leads"][lead_id]["name"],
        "company": sales_data["leads"][lead_id]["company"],
        "follow_up_date": follow_up_date,
        "notes": notes or "Follow-up scheduled",
        "status": "Scheduled",
        "timestamp": datetime.now().isoformat()
    }

def get_tasks(lead_id: str = None, due_date: str = None, status: str = None) -> dict:
    """Get scheduled tasks and follow-ups"""
    # Get tasks from the sales database
    tasks_list = list(sales_data["tasks"].values())
    
    # Apply filters
    if lead_id:
        tasks_list = [task for task in tasks_list if task["lead_id"] == lead_id]
    if due_date:
        tasks_list = [task for task in tasks_list if task["due_date"] == due_date]
    if status:
        tasks_list = [task for task in tasks_list if task["status"].lower() == status.lower()]
    
    return {
        "filters": {"lead_id": lead_id, "due_date": due_date, "status": status},
        "tasks": tasks_list,
        "total_count": len(tasks_list),
        "timestamp": datetime.now().isoformat()
    }

def complete_task(task_id: str, completion_notes: str = None) -> dict:
    """Mark a task as completed"""
    # Mock task completion - in real implementation this would update a database
    return {
        "task_id": task_id,
        "status": "Completed",
        "completion_notes": completion_notes or "Task completed",
        "completed_at": datetime.now().isoformat(),
        "timestamp": datetime.now().isoformat()
    }

def get_qualified_leads_summary(timeframe: str = "this_month", include_revenue: bool = True, include_tasks: bool = True) -> dict:
    """Get comprehensive summary of qualified leads including revenue and pending tasks"""
    
    # Get qualified leads for the specified timeframe
    current_month = datetime.now().month
    current_year = datetime.now().year
    
    qualified_leads = []
    total_revenue = 0
    
    for lead_id, lead in sales_data["leads"].items():
        if lead["status"] == "Qualified":
            # Check if lead was created this month (simplified logic)
            lead_created = datetime.strptime(lead["created"], "%Y-%m-%d")
            if timeframe == "this_month" and lead_created.month == current_month and lead_created.year == current_year:
                qualified_leads.append({
                    "lead_id": lead_id,
                    **lead
                })
                total_revenue += lead["value"]
    
    # Get pending tasks for these leads
    pending_tasks = []
    if include_tasks:
        all_tasks = get_tasks()
        for task in all_tasks["tasks"]:
            if task["status"] == "Pending":
                # Check if task is for one of our qualified leads
                for lead in qualified_leads:
                    if task["lead_id"] == lead["lead_id"]:
                        pending_tasks.append(task)
    
    # Get revenue breakdown
    revenue_breakdown = {}
    if include_revenue:
        for lead in qualified_leads:
            company = lead["company"]
            if company not in revenue_breakdown:
                revenue_breakdown[company] = 0
            revenue_breakdown[company] += lead["value"]
    
    return {
        "timeframe": timeframe,
        "qualified_leads": qualified_leads,
        "total_leads": len(qualified_leads),
        "total_revenue": total_revenue,
        "revenue_breakdown": revenue_breakdown if include_revenue else None,
        "pending_tasks": pending_tasks if include_tasks else None,
        "total_pending_tasks": len(pending_tasks) if include_tasks else 0,
        "timestamp": datetime.now().isoformat()
    }

# Tool function registry for easy access
TOOL_FUNCTIONS = {
    "search_leads": search_leads,
    "create_lead": create_lead,
    "update_lead_status": update_lead_status,
    "get_opportunity_details": get_opportunity_details,
    "create_opportunity": create_opportunity,
    "update_opportunity": update_opportunity,
    "search_customers": search_customers,
    "get_customer_details": get_customer_details,
    "get_sales_analytics": get_sales_analytics,
    "get_pipeline_report": get_pipeline_report,
    "generate_sales_email": generate_sales_email,
    "schedule_follow_up": schedule_follow_up,
    "get_tasks": get_tasks,
    "complete_task": complete_task,
    "get_qualified_leads_summary": get_qualified_leads_summary
}
