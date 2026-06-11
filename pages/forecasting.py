import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from etl.extract import get_filtered_data, extract_campaigns
from ml.forecast import forecast_future_performance

st.title("Predictive Analytics")
st.markdown("Forecast clicks, conversions, and revenue using machine learning models (XGBoost/RandomForest).")

st.sidebar.header("Filters")
# Simple multiselect for campaigns based on global list
try:
    df_global = extract_campaigns()
    all_campaigns = df_global['Campaign_Name'].dropna().unique().tolist()
except Exception:
    all_campaigns = []

selected_camps = st.sidebar.multiselect("Campaigns", options=all_campaigns)
start_date = st.sidebar.date_input("Start Date", value=None)
end_date = st.sidebar.date_input("End Date", value=None)

df_campaigns, _ = get_filtered_data(start_date=start_date, end_date=end_date, campaigns=selected_camps)

if df_campaigns.empty:
    st.warning("No historical data to forecast. Adjust your filters.")
else:
    target_metric = st.selectbox("Select Metric to Forecast", options=["Revenue", "Clicks", "Conversions"])
    
    with st.spinner(f"Training ML model for {target_metric} and generating 30-day forecast..."):
        df_eval, future_df, metrics = forecast_future_performance(df_campaigns, target_metric, steps=30)
    
    if not df_eval.empty:
        st.subheader("Model Performance Metrics")
        mcol1, mcol2, mcol3 = st.columns(3)
        mcol1.metric("RMSE (Root Mean Square Error)", f"{metrics.get('RMSE', 0):.2f}")
        mcol2.metric("MAE (Mean Absolute Error)", f"{metrics.get('MAE', 0):.2f}")
        mcol3.metric("R² Score", f"{metrics.get('R2', 0):.4f}")
        
        st.subheader("Actual vs Predicted")
        fig_eval = go.Figure()
        fig_eval.add_trace(go.Scatter(x=df_eval['Date'], y=df_eval['Actual'], mode='lines+markers', name='Actual'))
        fig_eval.add_trace(go.Scatter(x=df_eval['Date'], y=df_eval['Predicted'], mode='lines', name='Predicted (Train/Test)', line=dict(dash='dash')))
        fig_eval.update_layout(title=f"Actual vs Predicted {target_metric}", xaxis_title="Date", yaxis_title=target_metric)
        st.plotly_chart(fig_eval, use_container_width=True)
        
        st.subheader("Next 30-Day Forecast")
        fig_future = px.line(future_df, x='Date', y=f'Predicted_{target_metric}', title=f"30-Day {target_metric} Projection", markers=True)
        st.plotly_chart(fig_future, use_container_width=True)
        
        st.divider()
        st.subheader("Forecast Extrapolation Data")
        st.dataframe(future_df[['Date', f'Predicted_{target_metric}']], use_container_width=True)
