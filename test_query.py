#!/usr/bin/env python3
"""
Simple test script to demonstrate the core sales agent functionality.
Tests the three main query types:
1. "who are our customers closed last month"
2. "what are next steps with customer Y"
3. "show me total pipeline of opportunities that are active and projected to close next month"
"""

from tools import TOOL_FUNCTIONS
import json

def test_core_functionality():
    """Test the three core query types"""
    
    print("🧪 Testing Core Sales Agent Functionality\n")
    print("=" * 60)
    
    # Test 1: Customers closed last month
    print("\n1️⃣ Testing: 'Who are our customers closed last month?'")
    print("-" * 50)
    result = TOOL_FUNCTIONS["get_customers_closed_summary"](
        timeframe="last_month", 
        include_revenue_breakdown=True
    )
    print(f"✅ Found {result['total_customers']} customers closed last month")
    print(f"💰 Total revenue: ${result['total_revenue']:,}")
    print(f"📊 Average revenue per customer: ${result['average_revenue_per_customer']:,.0f}")
    if result['revenue_breakdown']:
        print("📈 Revenue breakdown:")
        for customer, revenue in result['revenue_breakdown'].items():
            print(f"   • {customer}: ${revenue:,}")
    
    # Test 2: Next steps with a customer
    print("\n2️⃣ Testing: 'What are next steps with customer TechCorp?'")
    print("-" * 50)
    result = TOOL_FUNCTIONS["get_customer_details"]("TechCorp")
    print(f"✅ Customer: {result['customer']['name']}")
    print(f"👤 Account Manager: {result['account_manager']}")
    print(f"📅 Last Activity: {result['last_activity']}")
    print(f"💼 Total Opportunities: {result['total_opportunities']}")
    print(f"💰 Total Value: ${result['total_value']:,}")
    print("📋 Next Steps:")
    for i, step in enumerate(result['next_steps'][:5], 1):  # Show first 5 steps
        print(f"   {i}. {step}")
    
    # Test 3: Pipeline report for next month
    print("\n3️⃣ Testing: 'Show me total pipeline of opportunities that are active and projected to close next month'")
    print("-" * 50)
    result = TOOL_FUNCTIONS["get_pipeline_report"](
        close_date_filter="next_month"
    )
    print(f"✅ Total Active Opportunities: {result['total_opportunities']}")
    print(f"💰 Total Pipeline Value: ${result['total_value']:,}")
    print(f"📊 Weighted Pipeline Value: ${result['weighted_value']:,.0f}")
    print(f"📅 Next Month Opportunities: {result['next_month_count']}")
    print(f"💰 Next Month Value: ${result['next_month_value']:,}")
    print("📈 Stage Breakdown:")
    for stage, data in result['stage_breakdown'].items():
        print(f"   • {stage}: {data['count']} deals, ${data['value']:,} value")
    
    # Test 4: Basic sales analytics
    print("\n4️⃣ Testing: Basic Sales Analytics")
    print("-" * 50)
    result = TOOL_FUNCTIONS["get_sales_analytics"](timeframe="month")
    print(f"📊 Total Leads: {result['total_leads']}")
    print(f"✅ Qualified Leads: {result['qualified_leads']}")
    print(f"📈 Qualification Rate: {result['qualification_rate']}%")
    print(f"💼 Total Opportunities: {result['total_opportunities']}")
    print(f"🔄 Active Opportunities: {result['active_opportunities']}")
    print(f"💰 Total Pipeline: ${result['total_pipeline_value']:,}")
    print(f"📊 Active Pipeline: ${result['active_pipeline_value']:,}")
    print(f"⚖️ Weighted Pipeline: ${result['weighted_pipeline_value']:,}")
    print(f"📊 Average Deal Size: ${result['average_deal_size']:,.0f}")
    
    print("\n" + "=" * 60)
    print("🎉 All core functionality tests completed successfully!")
    print("The simplified tool set is working correctly for the main query types.")

if __name__ == "__main__":
    test_core_functionality()
