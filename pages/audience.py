import streamlit as st
import datetime
import plotly.express as px
from etl.extract import extract_campaigns, extract_audiences, get_filtered_data
from analytics.audience import get_audience_performance, segment_by_age, segment_by_device

st.title("Audience Insights")
st.markdown("Analyze conversions and performance by demographics, location, and device.")

st.sidebar.header("Filters")
try:
    df_global_camp = extract_campaigns()
    df_global_aud = extract_audiences()
    all_campaigns = df_global_camp['Campaign_Name'].dropna().unique().tolist()
    all_platforms = df_global_camp['Platform'].dropna().unique().tolist()
    all_locations = df_global_aud['Location'].dropna().unique().tolist()
except Exception:
    all_campaigns, all_platforms, all_locations = [], [], []

selected_camps = st.sidebar.multiselect("Campaigns", options=all_campaigns)
selected_plats = st.sidebar.multiselect("Platforms", options=all_platforms)
selected_locs = st.sidebar.multiselect("Locations", options=all_locations)
start_date = st.sidebar.date_input("Start Date", value=None)
end_date = st.sidebar.date_input("End Date", value=None)

try:
    df_campaigns, df_audiences = get_filtered_data(
        start_date=start_date, 
        end_date=end_date, 
        campaigns=selected_camps, 
        platforms=selected_plats,
        locations=selected_locs
    )
    
    if df_campaigns.empty or df_audiences.empty:
        st.warning("No data found for the selected filters.")
    else:
        df_merged = get_audience_performance(df_audiences, df_campaigns)
    
    # Age Segment
    df_age = segment_by_age(df_merged)
    st.subheader("Performance by Age Group")
    fig_age = px.bar(df_age, x='Age_Group', y='Segment_Conversions', color='Segment_Revenue',
                     title="Conversions & Revenue by Age", labels={'Segment_Conversions': 'Conversions', 'Age_Group': 'Age'})
    st.plotly_chart(fig_age, use_container_width=True)
    
    # Device Segment
    df_device = segment_by_device(df_merged)
    st.subheader("Performance by Device")
    fig_dev = px.pie(df_device, names='Device', values='Segment_Spend', title="Ad Spend Allocation by Device")
    st.plotly_chart(fig_dev, use_container_width=True)
    
    st.divider()
    st.subheader("Raw Segment Data")
    st.dataframe(df_merged.head(100), use_container_width=True)
except Exception as e:
    st.error(f"Failed to load audience analytical data: {e}")
