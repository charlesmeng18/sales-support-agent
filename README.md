# 🚀 AgentForce - Simplified Sales Support Agent

A focused Streamlit-based sales support agent with core CRM capabilities, powered by OpenAI and enhanced with Cleanlab validation for AI safety.

## ✨ Core Features

- **5 Essential Sales Tools**: Focused on the most important sales queries
- **ReACT Agent Architecture**: Reasoning and Acting approach for sales workflows
- **AI Safety Monitoring**: Cleanlab Codex integration for response validation
- **Modern Streamlit UI**: Beautiful, responsive interface with real-time chat
- **Context-Aware Conversations**: Maintains conversation history and context
- **Secure API Management**: Environment variables and Streamlit secrets support

## 🛠️ Available Tools

### 🏢 Customer Management
- `get_customers_closed_summary` - Get customers closed within a timeframe with revenue
- `get_customer_details` - Get detailed customer information and next steps
- `search_customers` - Search for existing customers by name or company

### 📊 Pipeline & Analytics
- `get_pipeline_report` - Get detailed pipeline breakdown with stage analysis
- `get_sales_analytics` - Get basic sales KPIs and metrics

## 🎯 Core Query Types

The agent is optimized to handle these key sales questions:

1. **"Who are our customers closed last month?"**
   - Returns customer list, total revenue, and breakdown
   - Uses `get_customers_closed_summary`

2. **"What are next steps with customer Y?"**
   - Returns customer details, opportunities, and actionable next steps
   - Uses `get_customer_details`

3. **"Show me total pipeline of opportunities that are active and projected to close next month"**
   - Returns pipeline breakdown, stage analysis, and next month projections
   - Uses `get_pipeline_report`

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

### 3. Test Core Functionality

```bash
python test_query.py
```

### 4. Run the Application

```bash
streamlit run frontend.py
```

## 🧪 Testing

Run the test script to verify core functionality:

```bash
python test_query.py
```

This will test all three main query types and demonstrate the simplified tool set.

## 🚀 Streamlit Cloud Deployment

### 1. Create a GitHub Repository

```bash
# Initialize git repository
git init
git add .
git commit -m "Initial commit: Simplified Sales Support Agent"
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
├── tools.py             # Simplified tool definitions and implementations
├── sales_db.py          # Mock CRM database
├── test_query.py        # Test script for core functionality
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── .env                # Environment variables (create this)
```

## 💡 Example Usage

### Customer Analysis
```
User: "Who are our customers closed last month?"
Agent: [Returns customer list, total revenue, and breakdown]

User: "What are next steps with TechCorp?"
Agent: [Returns customer details, opportunities, and actionable next steps]
```

### Pipeline Management
```
User: "Show me total pipeline of opportunities that are active and projected to close next month"
Agent: [Returns pipeline breakdown, stage analysis, and next month projections]

User: "Get sales analytics for this month"
Agent: [Returns KPIs, pipeline metrics, and insights]
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
- Run `python test_query.py` to verify functionality
- Ensure all API keys are properly configured
- Check the debug output in the console

## 🔮 Future Enhancements

- Database integration (PostgreSQL, MongoDB)
- Advanced analytics and reporting
- Email integration (SMTP, API)
- Calendar integration
- Multi-user support
- Advanced AI safety features
