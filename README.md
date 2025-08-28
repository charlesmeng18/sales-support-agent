# 🚀 AgentForce - Sales Support Agent

A comprehensive Streamlit-based sales support agent with advanced CRM capabilities, powered by OpenAI and enhanced with Cleanlab validation for AI safety.

## ✨ Features

- **15+ Specialized Sales Tools**: Lead management, opportunity tracking, sales analytics, and more
- **ReACT Agent Architecture**: Reasoning and Acting approach for complex sales workflows
- **AI Safety Monitoring**: Cleanlab Codex integration for response validation
- **Modern Streamlit UI**: Beautiful, responsive interface with real-time chat
- **Context-Aware Conversations**: Maintains conversation history and context
- **Secure API Management**: Environment variables and Streamlit secrets support

## 🛠️ Available Tools

### 👥 Lead Management
- `search_leads` - Search and filter leads by criteria
- `create_lead` - Create new leads in the CRM
- `update_lead_status` - Update lead status and add notes

### 🎯 Opportunity Management
- `get_opportunity_details` - Get detailed opportunity information
- `create_opportunity` - Create new sales opportunities
- `update_opportunity` - Update opportunity details and stage

### 🏢 Customer Management
- `search_customers` - Search for existing customers
- `get_customer_details` - Get detailed customer information

### 📊 Sales Analytics
- `get_sales_analytics` - Get KPIs and pipeline metrics
- `get_pipeline_report` - Detailed pipeline breakdown by stage

### 📧 Communication
- `generate_sales_email` - Generate personalized sales emails
- `schedule_follow_up` - Schedule follow-up tasks

### 📋 Task Management
- `get_tasks` - Get scheduled tasks and follow-ups
- `complete_task` - Mark tasks as completed

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
CODEX_API_KEY=your_cleanlab_codex_key_here
CLEANLAB_PROJECT_ID=d3f73335-0fdc-4995-b1d1-a40a5d52886b
```

### 3. Run the Application

```bash
streamlit run frontend.py
```

## 🚀 Streamlit Cloud Deployment

### 1. Create a GitHub Repository

```bash
# Initialize git repository
git init
git add .
git commit -m "Initial commit: Sales Support Agent"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```

### 2. Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository
5. Set the main file path to: `frontend.py`
6. Add your secrets in the Streamlit Cloud dashboard:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `CODEX_API_KEY`: Your Cleanlab Codex API key
   - `CLEANLAB_PROJECT_ID`: `d3f73335-0fdc-4995-b1d1-a40a5d52886b`

### 3. Your app will be live at: `https://your-app-name.streamlit.app`

## 🔧 Configuration

### API Keys

The application supports multiple ways to configure API keys:

1. **Environment Variables** (for local development):
   ```bash
   export OPENAI_API_KEY="your_key"
   export CODEX_API_KEY="your_key"
       export CLEANLAB_PROJECT_ID="your key"
   ```

2. **Streamlit Secrets** (for Streamlit Cloud deployment):
   Create a `.streamlit/secrets.toml` file:
   ```toml
   OPENAI_API_KEY = "your_key"
   CODEX_API_KEY = "your_key"
   CLEANLAB_PROJECT_ID = "your key"
   ```

### Cleanlab Integration

The application includes optional Cleanlab Codex integration for AI safety monitoring:

- Validates agent responses for safety and accuracy
- Provides guardrails for tool selection
- Logs validation results for analysis
- Falls back gracefully if Cleanlab is not configured

## 📁 Project Structure

```
cleanlab_salesforce_agent/
├── frontend.py          # Streamlit frontend application
├── backend.py           # Sales agent backend implementation
├── tools.py             # Tool definitions and implementations
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── .env                # Environment variables (create this)
```

## 💡 Example Usage

### Lead Management
```
User: "Search for qualified leads from TechCorp"
Agent: [Searches CRM and returns matching leads]

User: "Create a new lead: John Doe from ABC Corp, john@abc.com"
Agent: [Creates lead and provides confirmation]
```

### Sales Analytics
```
User: "Show me sales analytics for this month"
Agent: [Returns KPIs, pipeline metrics, and insights]

User: "Get pipeline report by stage"
Agent: [Provides detailed breakdown of opportunities by stage]
```

### Communication
```
User: "Generate follow-up email for LEAD001"
Agent: [Creates personalized email template]

User: "Schedule follow-up for LEAD002 on 2024-02-15"
Agent: [Creates task and confirms scheduling]
```

## 🔒 Security Features

- **API Key Protection**: Secure handling of sensitive credentials
- **Input Validation**: Sanitized user inputs and tool parameters
- **AI Safety**: Cleanlab validation for response safety
- **Session Management**: Isolated conversation threads

## 🚀 Deployment

### Local Development
```bash
streamlit run frontend.py
```

### Streamlit Cloud
1. Push code to GitHub
2. Connect repository to Streamlit Cloud
3. Configure secrets in Streamlit Cloud dashboard
4. Deploy automatically

### Docker (Optional)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "streamlit_app.py"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
- Check the documentation
- Review example queries in the sidebar
- Ensure all API keys are properly configured
- Check the debug output in the console

## 🔮 Future Enhancements

- Database integration (PostgreSQL, MongoDB)
- Advanced analytics and reporting
- Email integration (SMTP, API)
- Calendar integration
- Multi-user support
- Advanced AI safety features
