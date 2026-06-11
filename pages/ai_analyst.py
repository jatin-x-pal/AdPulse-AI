import streamlit as st
import datetime
from etl.extract import get_filtered_data
from ml.forecast import forecast_future_performance
from analytics.audience import get_audience_performance, segment_by_age
from ai.insight_engine import generate_marketing_insights
from analytics.metrics import calculate_ctr, calculate_cpc, calculate_roas

st.title("AI Campaign Analyst")
st.markdown("Generate natural language insights from your integrated campaign data using standard AI analysis.")

st.sidebar.header("Filters")
start_date = st.sidebar.date_input("Start Date", value=None)
end_date = st.sidebar.date_input("End Date", value=None)

if st.button("Generate AI Insights", type="primary"):
    with st.spinner("Compiling cross-layer analytical data for OpenAI..."):
        # 1. Gather KPIs
        df_campaigns, df_audiences = get_filtered_data(start_date=start_date, end_date=end_date)
        if df_campaigns.empty or df_audiences.empty:
            st.error("Insufficient data available to analyze using current filters.")
            st.stop()
            
        total_spend = df_campaigns['Spend'].sum()
        total_revenue = df_campaigns['Revenue'].sum()
        total_clicks = int(df_campaigns['Clicks'].sum())
        total_impressions = int(df_campaigns['Impressions'].sum())
        total_conversions = int(df_campaigns['Conversions'].sum())
        
        metrics = {
            "Total Spend": float(total_spend),
            "Total Revenue": float(total_revenue),
            "Total Clicks": total_clicks,
            "Total Conversions": total_conversions,
            "CTR (%)": float(calculate_ctr(total_clicks, total_impressions)),
            "ROAS": float(calculate_roas(total_revenue, total_spend))
        }
        
        # 2. Gather Audience Data
        df_merged = get_audience_performance(df_audiences, df_campaigns)
        aud_df = segment_by_age(df_merged)
        aud_metrics = aud_df.to_dict(orient='records')
        
        # 3. Gather Forecast Data
        try:
            _, future_df, _ = forecast_future_performance(df_campaigns, "Revenue", steps=15)
            forecast_metrics = future_df[['Date', 'Predicted_Revenue']].tail(5).to_dict(orient='records') if not future_df.empty else []
            # convert timestamp to string
            for row in forecast_metrics:
                row['Date'] = str(row['Date'].date())
        except Exception as e:
            st.warning(f"Failed to generate forecast metrics for AI context: {e}")
            forecast_metrics = []
            
    with st.spinner("Generating AI Analysis... This may take up to 20 seconds depending on OpenAI load."):
        insights_md = generate_marketing_insights(metrics, aud_metrics, forecast_metrics)
        
    if "Error:" in insights_md:
        st.error(insights_md)
    else:
        st.divider()
        sections = insights_md.split("## ")
        for section in sections:
            if not section.strip():
                continue
            lines = section.split("\n", 1)
            header = lines[0].strip()
            content = lines[1].strip() if len(lines) > 1 else ""
            
            with st.expander(header, expanded=True):
                st.markdown(content)
                
        st.download_button(
            label="Download Text Report",
            data=insights_md,
            file_name=f"AdPulse_AI_Report_{datetime.date.today()}.md",
            mime="text/markdown"
        )
