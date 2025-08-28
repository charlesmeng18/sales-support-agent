import json
import random
from datetime import datetime, timedelta

# Comprehensive Mock CRM Database for Sales Data
sales_data = {
    "leads": {
        "LEAD001": {
            "name": "John Smith", "company": "TechCorp Inc", "email": "john@techcorp.com", "phone": "+1-555-0123", "status": "Qualified", "value": 50000, "source": "Website", "created": "2024-01-15", "industry": "Technology", "company_size": "50-200", "location": "San Francisco, CA", "title": "VP of Engineering", "notes": "Interested in enterprise solution, budget approved"
        },
        "LEAD002": {
            "name": "Sarah Johnson", "company": "Global Solutions", "email": "sarah@globalsolutions.com", "phone": "+1-555-0456", "status": "Contacted", "value": 75000, "source": "LinkedIn", "created": "2024-01-20", "industry": "Consulting", "company_size": "200-500", "location": "New York, NY", "title": "Director of Operations", "notes": "Looking for process automation tools"
        },
        "LEAD003": {
            "name": "Mike Chen", "company": "StartupXYZ", "email": "mike@startupxyz.com", "phone": "+1-555-0789", "status": "Proposal Sent", "value": 120000, "source": "Referral", "created": "2024-01-25", "industry": "SaaS", "company_size": "10-50", "location": "Austin, TX", "title": "CEO", "notes": "Fast-growing startup, needs scalable solution"
        },
        "LEAD004": {
            "name": "Emily Rodriguez", "company": "Healthcare Plus", "email": "emily@healthcareplus.com", "phone": "+1-555-1111", "status": "Qualified", "value": 85000, "source": "Trade Show", "created": "2024-02-01", "industry": "Healthcare", "company_size": "500-1000", "location": "Boston, MA", "title": "IT Director", "notes": "HIPAA compliance requirements, long sales cycle"
        },
        "LEAD005": {
            "name": "David Kim", "company": "Manufacturing Co", "email": "david@manufacturingco.com", "phone": "+1-555-2222", "status": "New", "value": 65000, "source": "Cold Call", "created": "2024-02-05", "industry": "Manufacturing", "company_size": "100-250", "location": "Detroit, MI", "title": "Operations Manager", "notes": "Interested in supply chain optimization"
        },
        "LEAD006": {
            "name": "Lisa Wang", "company": "Financial Services Inc", "email": "lisa@financialservices.com", "phone": "+1-555-3333", "status": "Qualified", "value": 95000, "source": "Website", "created": "2024-02-10", "industry": "Financial Services", "company_size": "1000+", "location": "Chicago, IL", "title": "VP of Technology", "notes": "Regulatory compliance focus, enterprise deal"
        },
        "LEAD007": {
            "name": "Alex Thompson", "company": "Retail Chain", "email": "alex@retailchain.com", "phone": "+1-555-4444", "status": "Contacted", "value": 45000, "source": "LinkedIn", "created": "2024-02-12", "industry": "Retail", "company_size": "500-1000", "location": "Los Angeles, CA", "title": "Store Operations Director", "notes": "Multi-location retail, inventory management needs"
        },
        "LEAD008": {
            "name": "Maria Garcia", "company": "Education First", "email": "maria@educationfirst.com", "phone": "+1-555-5555", "status": "Qualified", "value": 35000, "source": "Referral", "created": "2024-02-15", "industry": "Education", "company_size": "50-200", "location": "Seattle, WA", "title": "Technology Coordinator", "notes": "School district, budget constraints, long approval process"
        },
        "LEAD009": {
            "name": "James Wilson", "company": "CloudTech Solutions", "email": "james@cloudtech.com", "phone": "+1-555-6666", "status": "Qualified", "value": 180000, "source": "Website", "created": "2024-02-18", "industry": "Technology", "company_size": "500-1000", "location": "Seattle, WA", "title": "CTO", "notes": "Cloud migration project, large budget available"
        },
        "LEAD010": {
            "name": "Jennifer Lee", "company": "Legal Associates", "email": "jennifer@legalassociates.com", "phone": "+1-555-7777", "status": "Contacted", "value": 55000, "source": "Referral", "created": "2024-02-20", "industry": "Legal", "company_size": "50-200", "location": "Washington, DC", "title": "Managing Partner", "notes": "Document management system needed, compliance focus"
        },
        "LEAD011": {
            "name": "Robert Chen", "company": "Pharma Innovations", "email": "robert@pharmainnovations.com", "phone": "+1-555-8888", "status": "New", "value": 220000, "source": "Trade Show", "created": "2024-02-22", "industry": "Pharmaceuticals", "company_size": "1000+", "location": "Boston, MA", "title": "VP of R&D", "notes": "Clinical trial management system, FDA compliance required"
        },
        "LEAD012": {
            "name": "Amanda Foster", "company": "Green Energy Co", "email": "amanda@greenenergy.com", "phone": "+1-555-9999", "status": "Qualified", "value": 75000, "source": "LinkedIn", "created": "2024-02-25", "industry": "Energy", "company_size": "200-500", "location": "Denver, CO", "title": "Operations Director", "notes": "Renewable energy monitoring, IoT integration needed"
        },
        "LEAD013": {
            "name": "Carlos Martinez", "company": "Hospitality Group", "email": "carlos@hospitalitygroup.com", "phone": "+1-555-0000", "status": "Contacted", "value": 40000, "source": "Cold Call", "created": "2024-02-28", "industry": "Hospitality", "company_size": "100-250", "location": "Miami, FL", "title": "IT Manager", "notes": "Hotel management system, multi-property setup"
        },
        "LEAD014": {
            "name": "Rachel Green", "company": "Media Productions", "email": "rachel@mediaproductions.com", "phone": "+1-555-1112", "status": "Qualified", "value": 65000, "source": "Website", "created": "2024-03-01", "industry": "Media", "company_size": "50-200", "location": "Los Angeles, CA", "title": "Production Manager", "notes": "Content management system, video processing capabilities"
        },
        "LEAD015": {
            "name": "Michael Brown", "company": "Logistics Express", "email": "michael@logisticsexpress.com", "phone": "+1-555-2223", "status": "New", "value": 95000, "source": "Referral", "created": "2024-03-03", "industry": "Logistics", "company_size": "500-1000", "location": "Atlanta, GA", "title": "VP of Operations", "notes": "Supply chain optimization, real-time tracking needed"
        },
        "LEAD016": {
            "name": "Sofia Rodriguez", "company": "Insurance Partners", "email": "sofia@insurancepartners.com", "phone": "+1-555-3334", "status": "Qualified", "value": 110000, "source": "LinkedIn", "created": "2024-03-05", "industry": "Insurance", "company_size": "1000+", "location": "Hartford, CT", "title": "Chief Technology Officer", "notes": "Claims processing system, AI integration required"
        },
        "LEAD017": {
            "name": "Daniel Kim", "company": "Construction Dynamics", "email": "daniel@constructiondynamics.com", "phone": "+1-555-4445", "status": "Contacted", "value": 85000, "source": "Trade Show", "created": "2024-03-08", "industry": "Construction", "company_size": "200-500", "location": "Houston, TX", "title": "Project Director", "notes": "Project management system, safety compliance tracking"
        },
        "LEAD018": {
            "name": "Nicole Taylor", "company": "Real Estate Partners", "email": "nicole@realestatepartners.com", "phone": "+1-555-5556", "status": "Qualified", "value": 45000, "source": "Website", "created": "2024-03-10", "industry": "Real Estate", "company_size": "50-200", "location": "Phoenix, AZ", "title": "Broker", "notes": "Property management system, client relationship management"
        },
        "LEAD019": {
            "name": "Kevin Johnson", "company": "Food Services Inc", "email": "kevin@foodservices.com", "phone": "+1-555-6667", "status": "New", "value": 70000, "source": "Cold Call", "created": "2024-03-12", "industry": "Food & Beverage", "company_size": "100-250", "location": "Portland, OR", "title": "Operations Manager", "notes": "Inventory management system, supplier integration"
        },
        "LEAD020": {
            "name": "Laura Davis", "company": "Nonprofit Alliance", "email": "laura@nonprofitalliance.com", "phone": "+1-555-7778", "status": "Contacted", "value": 25000, "source": "Referral", "created": "2024-03-15", "industry": "Nonprofit", "company_size": "10-50", "location": "Austin, TX", "title": "Executive Director", "notes": "Donor management system, grant tracking capabilities"
        }
    },
    
    "opportunities": {
        "OPP001": {
            "lead_id": "LEAD001", 
            "name": "TechCorp Software License", 
            "stage": "Negotiation", 
            "value": 50000, 
            "probability": 75, 
            "close_date": "2024-02-15", 
            "owner": "Alex Rodriguez",
            "created": "2024-01-20",
            "last_activity": "2024-02-01",
            "notes": "Contract review in progress, legal team involved"
        },
        "OPP002": {
            "lead_id": "LEAD002", 
            "name": "Global Solutions Implementation", 
            "stage": "Proposal", 
            "value": 75000, 
            "probability": 60, 
            "close_date": "2024-02-28", 
            "owner": "Maria Garcia",
            "created": "2024-01-25",
            "last_activity": "2024-02-03",
            "notes": "Proposal submitted, waiting for stakeholder review"
        },
        "OPP003": {
            "lead_id": "LEAD003", 
            "name": "StartupXYZ Platform", 
            "stage": "Discovery", 
            "value": 120000, 
            "probability": 40, 
            "close_date": "2024-03-15", 
            "owner": "David Kim",
            "created": "2024-01-30",
            "last_activity": "2024-02-05",
            "notes": "Technical requirements gathering, demo scheduled"
        },
        "OPP004": {
            "lead_id": "LEAD004", 
            "name": "Healthcare Plus Compliance", 
            "stage": "Qualification", 
            "value": 85000, 
            "probability": 25, 
            "close_date": "2024-04-01", 
            "owner": "Sarah Johnson",
            "created": "2024-02-05",
            "last_activity": "2024-02-10",
            "notes": "Initial discovery call completed, needs assessment"
        },
        "OPP005": {
            "lead_id": "LEAD006", 
            "name": "Financial Services Enterprise", 
            "stage": "Negotiation", 
            "value": 95000, 
            "probability": 80, 
            "close_date": "2024-02-20", 
            "owner": "Alex Rodriguez",
            "created": "2024-02-12",
            "last_activity": "2024-02-12",
            "notes": "High priority deal, executive sponsorship confirmed"
        },
        "OPP006": {
            "lead_id": "LEAD008", 
            "name": "Education First Implementation", 
            "stage": "Proposal", 
            "value": 35000, 
            "probability": 70, 
            "close_date": "2024-03-01", 
            "owner": "Maria Garcia",
            "created": "2024-02-18",
            "last_activity": "2024-02-18",
            "notes": "Proposal ready, waiting for budget approval"
        },
        "OPP007": {
            "lead_id": "LEAD009", 
            "name": "CloudTech Cloud Migration", 
            "stage": "Negotiation", 
            "value": 180000, 
            "probability": 85, 
            "close_date": "2024-03-15", 
            "owner": "Alex Rodriguez",
            "created": "2024-02-20",
            "last_activity": "2024-03-01",
            "notes": "Enterprise cloud migration, technical review completed"
        },
        "OPP008": {
            "lead_id": "LEAD011", 
            "name": "Pharma Innovations Clinical Trials", 
            "stage": "Discovery", 
            "value": 220000, 
            "probability": 30, 
            "close_date": "2024-04-15", 
            "owner": "Sarah Johnson",
            "created": "2024-02-25",
            "last_activity": "2024-03-05",
            "notes": "FDA compliance requirements, long sales cycle expected"
        },
        "OPP009": {
            "lead_id": "LEAD012", 
            "name": "Green Energy IoT Platform", 
            "stage": "Qualification", 
            "value": 75000, 
            "probability": 50, 
            "close_date": "2024-03-30", 
            "owner": "David Kim",
            "created": "2024-02-28",
            "last_activity": "2024-03-08",
            "notes": "Renewable energy monitoring, technical requirements gathering"
        },
        "OPP010": {
            "lead_id": "LEAD014", 
            "name": "Media Productions CMS", 
            "stage": "Proposal", 
            "value": 65000, 
            "probability": 75, 
            "close_date": "2024-03-20", 
            "owner": "Maria Garcia",
            "created": "2024-03-03",
            "last_activity": "2024-03-10",
            "notes": "Content management system, video processing demo completed"
        },
        "OPP011": {
            "lead_id": "LEAD015", 
            "name": "Logistics Express Supply Chain", 
            "stage": "Discovery", 
            "value": 95000, 
            "probability": 40, 
            "close_date": "2024-04-01", 
            "owner": "Alex Rodriguez",
            "created": "2024-03-05",
            "last_activity": "2024-03-12",
            "notes": "Supply chain optimization, real-time tracking requirements"
        },
        "OPP012": {
            "lead_id": "LEAD016", 
            "name": "Insurance Partners Claims System", 
            "stage": "Negotiation", 
            "value": 110000, 
            "probability": 80, 
            "close_date": "2024-03-25", 
            "owner": "Sarah Johnson",
            "created": "2024-03-08",
            "last_activity": "2024-03-15",
            "notes": "Claims processing with AI integration, contract review in progress"
        },
        "OPP013": {
            "lead_id": "LEAD017", 
            "name": "Construction Dynamics Project Management", 
            "stage": "Qualification", 
            "value": 85000, 
            "probability": 45, 
            "close_date": "2024-04-10", 
            "owner": "David Kim",
            "created": "2024-03-10",
            "last_activity": "2024-03-18",
            "notes": "Project management system, safety compliance requirements"
        },
        "OPP014": {
            "lead_id": "LEAD018", 
            "name": "Real Estate Partners Property Management", 
            "stage": "Proposal", 
            "value": 45000, 
            "probability": 70, 
            "close_date": "2024-03-28", 
            "owner": "Maria Garcia",
            "created": "2024-03-12",
            "last_activity": "2024-03-20",
            "notes": "Property management system, client relationship features"
        },
        "OPP015": {
            "lead_id": "LEAD019", 
            "name": "Food Services Inventory Management", 
            "stage": "Discovery", 
            "value": 70000, 
            "probability": 35, 
            "close_date": "2024-04-05", 
            "owner": "David Kim",
            "created": "2024-03-15",
            "last_activity": "2024-03-22",
            "notes": "Inventory management, supplier integration requirements"
        }
    },
    
    "customers": {
        "CUST001": {
            "name": "Enterprise Solutions Ltd", 
            "contact": "Lisa Wang", 
            "email": "lisa@enterprise.com", 
            "phone": "+1-555-1111", 
            "status": "Active", 
            "revenue": 250000, 
            "onboarding_date": "2023-06-15",
            "closed_date": "2023-07-20",
            "industry": "Technology",
            "company_size": "1000+",
            "location": "San Francisco, CA",
            "account_manager": "Alex Rodriguez",
            "last_activity": "2024-02-01",
            "notes": "Enterprise customer, annual contract renewal due"
        },
        "CUST002": {
            "name": "Innovation Corp", 
            "contact": "Tom Davis", 
            "email": "tom@innovation.com", 
            "phone": "+1-555-2222", 
            "status": "Active", 
            "revenue": 180000, 
            "onboarding_date": "2023-08-20",
            "closed_date": "2023-09-15",
            "industry": "Consulting",
            "company_size": "200-500",
            "location": "New York, NY",
            "account_manager": "Maria Garcia",
            "last_activity": "2024-01-25",
            "notes": "Mid-market customer, quarterly business review scheduled"
        },
        "CUST003": {
            "name": "Future Tech", 
            "contact": "Emma Wilson", 
            "email": "emma@futuretech.com", 
            "phone": "+1-555-3333", 
            "status": "Churned", 
            "revenue": 95000, 
            "onboarding_date": "2023-03-10",
            "closed_date": "2023-04-05",
            "industry": "SaaS",
            "company_size": "50-200",
            "location": "Austin, TX",
            "account_manager": "David Kim",
            "last_activity": "2023-12-15",
            "notes": "Churned due to budget cuts, potential re-engagement"
        },
        "CUST004": {
            "name": "Healthcare Systems", 
            "contact": "Dr. Robert Chen", 
            "email": "robert@healthcaresystems.com", 
            "phone": "+1-555-4444", 
            "status": "Active", 
            "revenue": 320000, 
            "onboarding_date": "2023-01-15",
            "closed_date": "2023-02-10",
            "industry": "Healthcare",
            "company_size": "1000+",
            "location": "Boston, MA",
            "account_manager": "Sarah Johnson",
            "last_activity": "2024-02-05",
            "notes": "Large healthcare system, compliance-focused"
        },
        "CUST005": {
            "name": "Manufacturing Solutions", 
            "contact": "Jennifer Lee", 
            "email": "jennifer@manufacturingsolutions.com", 
            "phone": "+1-555-5555", 
            "status": "Active", 
            "revenue": 150000, 
            "onboarding_date": "2023-09-10",
            "closed_date": "2023-10-20",
            "industry": "Manufacturing",
            "company_size": "500-1000",
            "location": "Detroit, MI",
            "account_manager": "Alex Rodriguez",
            "last_activity": "2024-01-30",
            "notes": "Manufacturing customer, supply chain optimization focus"
        },
        "CUST006": {
            "name": "Financial Services Inc", 
            "contact": "Michael Brown", 
            "email": "michael@financialservices.com", 
            "phone": "+1-555-6666", 
            "status": "Active", 
            "revenue": 450000, 
            "onboarding_date": "2023-11-01",
            "closed_date": "2023-12-15",
            "industry": "Financial Services",
            "company_size": "1000+",
            "location": "Chicago, IL",
            "account_manager": "Sarah Johnson",
            "last_activity": "2024-02-10",
            "notes": "Financial services enterprise, regulatory compliance"
        },
        "CUST007": {
            "name": "Retail Chain", 
            "contact": "Sofia Rodriguez", 
            "email": "sofia@retailchain.com", 
            "phone": "+1-555-7777", 
            "status": "Active", 
            "revenue": 280000, 
            "onboarding_date": "2023-12-01",
            "closed_date": "2024-01-10",
            "industry": "Retail",
            "company_size": "500-1000",
            "location": "Los Angeles, CA",
            "account_manager": "Maria Garcia",
            "last_activity": "2024-01-15",
            "notes": "Multi-location retail, inventory management"
        },
        "CUST008": {
            "name": "Education First", 
            "contact": "Daniel Kim", 
            "email": "daniel@educationfirst.com", 
            "phone": "+1-555-8888", 
            "status": "Active", 
            "revenue": 120000, 
            "onboarding_date": "2024-01-05",
            "closed_date": "2024-02-01",
            "industry": "Education",
            "company_size": "200-500",
            "location": "Seattle, WA",
            "account_manager": "David Kim",
            "last_activity": "2024-02-20",
            "notes": "School district, budget constraints"
        },
        "CUST009": {
            "name": "CloudTech Solutions", 
            "contact": "Nicole Taylor", 
            "email": "nicole@cloudtech.com", 
            "phone": "+1-555-9999", 
            "status": "Active", 
            "revenue": 380000, 
            "onboarding_date": "2024-01-15",
            "closed_date": "2024-02-20",
            "industry": "Technology",
            "company_size": "500-1000",
            "location": "Seattle, WA",
            "account_manager": "Alex Rodriguez",
            "last_activity": "2024-03-01",
            "notes": "Cloud migration project, large budget"
        },
        "CUST010": {
            "name": "Insurance Partners", 
            "contact": "Kevin Johnson", 
            "email": "kevin@insurancepartners.com", 
            "phone": "+1-555-0000", 
            "status": "Active", 
            "revenue": 520000, 
            "onboarding_date": "2024-02-01",
            "closed_date": "2024-03-01",
            "industry": "Insurance",
            "company_size": "1000+",
            "location": "Hartford, CT",
            "account_manager": "Sarah Johnson",
            "last_activity": "2024-03-05",
            "notes": "Claims processing system, AI integration"
        }
    },
    
    "tasks": {
        "TASK001": {
            "task_id": "TASK001",
            "lead_id": "LEAD001",
            "lead_name": "John Smith",
            "company": "TechCorp Inc",
            "task_type": "Follow-up Call",
            "due_date": "2024-02-01",
            "status": "Pending",
            "notes": "Discuss proposal feedback and next steps",
            "assigned_to": "Alex Rodriguez",
            "priority": "High"
        },
        "TASK002": {
            "task_id": "TASK002", 
            "lead_id": "LEAD002",
            "lead_name": "Sarah Johnson",
            "company": "Global Solutions",
            "task_type": "Email Follow-up",
            "due_date": "2024-02-03",
            "status": "Completed",
            "notes": "Sent discovery call invitation",
            "assigned_to": "Maria Garcia",
            "priority": "Medium"
        },
        "TASK003": {
            "task_id": "TASK003",
            "lead_id": "LEAD003",
            "lead_name": "Mike Chen",
            "company": "StartupXYZ",
            "task_type": "Demo",
            "due_date": "2024-02-08",
            "status": "Pending",
            "notes": "Technical demo for engineering team",
            "assigned_to": "David Kim",
            "priority": "High"
        },
        "TASK004": {
            "task_id": "TASK004",
            "lead_id": "LEAD004",
            "lead_name": "Emily Rodriguez",
            "company": "Healthcare Plus",
            "task_type": "Proposal Review",
            "due_date": "2024-02-10",
            "status": "Pending",
            "notes": "Review proposal with compliance team",
            "assigned_to": "Sarah Johnson",
            "priority": "Medium"
        },
        "TASK005": {
            "task_id": "TASK005",
            "lead_id": "LEAD006",
            "lead_name": "Lisa Wang",
            "company": "Financial Services Inc",
            "task_type": "Contract Negotiation",
            "due_date": "2024-02-15",
            "status": "Pending",
            "notes": "Final contract terms discussion",
            "assigned_to": "Alex Rodriguez",
            "priority": "High"
        },
        "TASK006": {
            "task_id": "TASK006",
            "lead_id": "LEAD008",
            "lead_name": "Maria Garcia",
            "company": "Education First",
            "task_type": "Budget Approval Follow-up",
            "due_date": "2024-02-20",
            "status": "Pending",
            "notes": "Check on budget approval status",
            "assigned_to": "Maria Garcia",
            "priority": "Medium"
        }
    },
    
    "activities": {
        "ACT001": {
            "activity_id": "ACT001",
            "lead_id": "LEAD001",
            "type": "Call",
            "date": "2024-01-30",
            "duration": "30 minutes",
            "notes": "Discovery call completed, requirements gathered",
            "outcome": "Qualified lead, proposal requested"
        },
        "ACT002": {
            "activity_id": "ACT002",
            "lead_id": "LEAD002",
            "type": "Email",
            "date": "2024-02-01",
            "duration": "5 minutes",
            "notes": "Proposal sent via email",
            "outcome": "Proposal delivered, waiting for feedback"
        },
        "ACT003": {
            "activity_id": "ACT003",
            "lead_id": "LEAD003",
            "type": "Meeting",
            "date": "2024-02-05",
            "duration": "60 minutes",
            "notes": "Technical requirements meeting with engineering team",
            "outcome": "Requirements confirmed, demo scheduled"
        },
        "ACT004": {
            "activity_id": "ACT004",
            "lead_id": "LEAD004",
            "type": "Call",
            "date": "2024-02-10",
            "duration": "45 minutes",
            "notes": "Initial discovery call, compliance requirements discussed",
            "outcome": "Qualified lead, needs assessment required"
        },
        "ACT005": {
            "activity_id": "ACT005",
            "lead_id": "LEAD006",
            "type": "Meeting",
            "date": "2024-02-12",
            "duration": "90 minutes",
            "notes": "Executive presentation, all stakeholders present",
            "outcome": "High interest, contract negotiation phase"
        }
    },
    
    "sales_team": {
        "Alex Rodriguez": {
            "name": "Alex Rodriguez",
            "title": "Senior Sales Executive",
            "email": "alex@company.com",
            "phone": "+1-555-1000",
            "territory": "West Coast",
            "quota": 1000000,
            "ytd_sales": 750000,
            "specialization": "Enterprise Sales"
        },
        "Maria Garcia": {
            "name": "Maria Garcia",
            "title": "Sales Manager",
            "email": "maria@company.com",
            "phone": "+1-555-1001",
            "territory": "East Coast",
            "quota": 800000,
            "ytd_sales": 600000,
            "specialization": "Mid-Market Sales"
        },
        "David Kim": {
            "name": "David Kim",
            "title": "Sales Executive",
            "email": "david@company.com",
            "phone": "+1-555-1002",
            "territory": "Central",
            "quota": 600000,
            "ytd_sales": 450000,
            "specialization": "SMB Sales"
        },
        "Sarah Johnson": {
            "name": "Sarah Johnson",
            "title": "Account Executive",
            "email": "sarah@company.com",
            "phone": "+1-555-1003",
            "territory": "Northeast",
            "quota": 700000,
            "ytd_sales": 520000,
            "specialization": "Healthcare Sales"
        }
    }
}

# Helper functions for data access
def get_leads_by_status(status=None, source=None, industry=None):
    """Get leads filtered by various criteria"""
    filtered_leads = []
    for lead_id, lead in sales_data["leads"].items():
        if status and lead["status"] != status:
            continue
        if source and lead["source"] != source:
            continue
        if industry and lead["industry"] != industry:
            continue
        filtered_leads.append({"lead_id": lead_id, **lead})
    return filtered_leads

def get_opportunities_by_stage(stage=None, owner=None):
    """Get opportunities filtered by stage or owner"""
    filtered_opps = []
    for opp_id, opp in sales_data["opportunities"].items():
        if stage and opp["stage"] != stage:
            continue
        if owner and opp["owner"] != owner:
            continue
        filtered_opps.append({"opportunity_id": opp_id, **opp})
    return filtered_opps

def get_tasks_by_status(status=None, assigned_to=None):
    """Get tasks filtered by status or assignee"""
    filtered_tasks = []
    for task_id, task in sales_data["tasks"].items():
        if status and task["status"] != status:
            continue
        if assigned_to and task["assigned_to"] != assigned_to:
            continue
        filtered_tasks.append(task)
    return filtered_tasks

def get_customers_by_status(status=None, industry=None):
    """Get customers filtered by status or industry"""
    filtered_customers = []
    for cust_id, customer in sales_data["customers"].items():
        if status and customer["status"] != status:
            continue
        if industry and customer["industry"] != industry:
            continue
        filtered_customers.append({"customer_id": cust_id, **customer})
    return filtered_customers

def get_activities_by_lead(lead_id=None, activity_type=None):
    """Get activities filtered by lead or type"""
    filtered_activities = []
    for act_id, activity in sales_data["activities"].items():
        if lead_id and activity["lead_id"] != lead_id:
            continue
        if activity_type and activity["type"] != activity_type:
            continue
        filtered_activities.append(activity)
    return filtered_activities

def get_customers_by_close_date(timeframe: str = "last_month") -> list:
    """Get customers closed within a specific timeframe"""
    from datetime import datetime, timedelta
    
    current_date = datetime.now()
    filtered_customers = []
    
    for customer_id, customer in sales_data["customers"].items():
        if "closed_date" not in customer:
            continue
            
        close_date = datetime.strptime(customer["closed_date"], "%Y-%m-%d")
        
        if timeframe == "last_month":
            last_month = current_date.replace(day=1) - timedelta(days=1)
            last_month = last_month.replace(day=1)
            if close_date >= last_month and close_date < current_date.replace(day=1):
                filtered_customers.append({"customer_id": customer_id, **customer})
        elif timeframe == "this_month":
            if close_date >= current_date.replace(day=1):
                filtered_customers.append({"customer_id": customer_id, **customer})
        elif timeframe == "last_quarter":
            quarter_start = current_date.replace(day=1)
            while quarter_start.month % 3 != 1:
                quarter_start = quarter_start.replace(day=1) - timedelta(days=1)
                quarter_start = quarter_start.replace(day=1)
            quarter_start = quarter_start.replace(month=quarter_start.month - 3)
            if close_date >= quarter_start and close_date < current_date.replace(day=1):
                filtered_customers.append({"customer_id": customer_id, **customer})
    
    return filtered_customers
