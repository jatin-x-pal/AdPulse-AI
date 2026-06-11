import streamlit as st
import datetime
from etl.extract import get_filtered_data
from analytics.audience import get_audience_performance, segment_by_age
from ml.forecast import forecast_future_performance
from analytics.metrics import calculate_ctr, calculate_roas
from reports.report_builder import build_comprehensive_report
from reports.pdf_generator import generate_pdf_from_md

st.title("Automated Reporting")
st.markdown("Generate and export comprehensive performance reports in Markdown or PDF.")

st.sidebar.header("Report Configuration")
start_date = st.sidebar.date_input("Start Date", value=None)
end_date = st.sidebar.date_input("End Date", value=None)

if st.button("Generate Final Report", type="primary"):
    with st.spinner("Extracting comprehensive data arrays..."):
        # Gather all metrics quickly
        df_campaigns, df_audiences = get_filtered_data(start_date=start_date, end_date=end_date)
        if df_campaigns.empty:
            st.error("No data available for the chosen config range.")
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
        
        df_merged = get_audience_performance(df_audiences, df_campaigns)
        aud_metrics = segment_by_age(df_merged).to_dict(orient='records')
        
        try:
            _, future_df, _ = forecast_future_performance(df_campaigns, "Revenue", steps=15)
            forecast_metrics = future_df[['Date', 'Predicted_Revenue']].tail(5).to_dict(orient='records') if not future_df.empty else []
            for row in forecast_metrics:
                row['Date'] = str(row['Date'].date())
        except Exception as e:
            forecast_metrics = []
            
    with st.spinner("Invoking AI Analyst for Executive Report..."):
        report_md = build_comprehensive_report(metrics, aud_metrics, forecast_metrics)
        
    if "Error:" in report_md:
        st.error(report_md)
        st.stop()
        
    with st.spinner("Compiling PDF Payload..."):
        try:
            pdf_bytes = generate_pdf_from_md(report_md)
        except Exception as e:
            st.error(f"PDF Compilation failed: {e}")
            pdf_bytes = None
            
    st.success("Report successfully generated!")
    
    st.subheader("Report Export Options")
    col1, col2, _ = st.columns([1,1,2])
    
    date_str = datetime.date.today().strftime('%Y-%m-%d')
    if pdf_bytes:
        col1.download_button(
            label="📄 Download PDF",
            data=pdf_bytes,
            file_name=f"AdPulse_Report_{date_str}.pdf",
            mime="application/pdf"
        )
        
    col2.download_button(
        label="📝 Download Markdown",
        data=report_md,
        file_name=f"AdPulse_Report_{date_str}.md",
        mime="text/markdown"
    )
    
    st.divider()
    st.subheader("Preview Report Output")
    st.markdown(report_md, unsafe_allow_html=True)
