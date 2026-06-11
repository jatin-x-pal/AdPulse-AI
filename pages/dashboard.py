import streamlit as st
import datetime
from etl.extract import get_filtered_data, extract_campaigns
from analytics.metrics import calculate_ctr, calculate_cpc, calculate_roas

st.title("KPI Dashboard")
st.markdown("Overview of high-level marketing performance indicators.")

# Add Filters in Sidebar
st.sidebar.header("Filters")
try:
    df_global = extract_campaigns()
    all_campaigns = df_global['Campaign_Name'].dropna().unique().tolist()
    all_platforms = df_global['Platform'].dropna().unique().tolist()
except Exception:
    all_campaigns, all_platforms = [], []

selected_camps = st.sidebar.multiselect("Campaigns", options=all_campaigns)
selected_plats = st.sidebar.multiselect("Platforms", options=all_platforms)
start_date = st.sidebar.date_input("Start Date", value=None)
end_date = st.sidebar.date_input("End Date", value=None)

try:
    df_campaigns, _ = get_filtered_data(
        start_date=start_date, 
        end_date=end_date, 
        campaigns=selected_camps, 
        platforms=selected_plats
    )
    
    total_spend = df_campaigns['Spend'].sum() if not df_campaigns.empty else 0.0
    total_revenue = df_campaigns['Revenue'].sum() if not df_campaigns.empty else 0.0
    total_clicks = df_campaigns['Clicks'].sum() if not df_campaigns.empty else 0
    total_impressions = df_campaigns['Impressions'].sum() if not df_campaigns.empty else 0
    total_conversions = df_campaigns['Conversions'].sum() if not df_campaigns.empty else 0
    
    st.subheader("Aggregate KPIs")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Spend", f"${total_spend:,.2f}")
    col2.metric("Total Revenue", f"${total_revenue:,.2f}")
    col3.metric("Total Clicks", f"{total_clicks:,}")
    col4.metric("Conversions", f"{total_conversions:,}")
    
    ctr = calculate_ctr(total_clicks, total_impressions)
    cpc = calculate_cpc(total_spend, total_clicks)
    roas = calculate_roas(total_revenue, total_spend)
    
    col5, col6, col7, col8 = st.columns(4)
    col5.metric("CTR", f"{ctr:.2f}%")
    col6.metric("CPC", f"${cpc:.2f}")
    col7.metric("ROAS", f"{roas:.2f}x")
    col8.metric("Conv. Rate", f"{(total_conversions/total_clicks)*100 if total_clicks > 0 else 0:.2f}%")
    
    st.divider()
    st.subheader("Raw Campaign Data")
    st.dataframe(df_campaigns, use_container_width=True)
except Exception as e:
    st.warning("Sample data not found. Please ensure generation is complete.")
    st.error(f"Error: {str(e)}")
