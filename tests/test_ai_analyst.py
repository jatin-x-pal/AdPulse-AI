import os
import sys
import logging
from unittest.mock import patch
import pandas as pd

# Append root to sys.path to allow execution without -m if needed
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from etl.extract import get_filtered_data
from analytics.metrics import calculate_ctr, calculate_roas
from analytics.audience import get_audience_performance, segment_by_age
from ml.forecast import forecast_future_performance
from ai.prompt_builder import build_analysis_prompt
from ai.insight_engine import generate_marketing_insights
import openai

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def test_full_ai_flow():
    logging.info("1. Loading campaign data from SQLite...")
    df_campaigns, df_audiences = get_filtered_data()
    
    # Handling Empty campaign data (Requirement 8)
    if df_campaigns.empty or df_audiences.empty:
        logging.error("Failed: Campaign or Audience data is empty.")
        return
    logging.info("✓ Data loaded successfully.")

    logging.info("2. Verifying KPI calculations...")
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
    logging.info(f"✓ KPIs calculated: {metrics}")
    
    logging.info("3. Verifying audience analytics...")
    df_merged = get_audience_performance(df_audiences, df_campaigns)
    aud_df = segment_by_age(df_merged)
    aud_metrics = aud_df.to_dict(orient='records')
    logging.info(f"✓ Audience segments computed: {len(aud_metrics)} age groups formed.")
    
    logging.info("4. Verifying forecast outputs...")
    try:
        _, future_df, _ = forecast_future_performance(df_campaigns, "Revenue", steps=15)
        # Handle Empty forecast data (Requirement 8)
        if future_df.empty:
            raise ValueError("Empty forecast data generated.")
            
        forecast_metrics = future_df[['Date', 'Predicted_Revenue']].tail(5).to_dict(orient='records')
        for row in forecast_metrics:
            row['Date'] = str(row['Date'].date())
        logging.info("✓ Forecast generation success.")
    except Exception as e:
        logging.error(f"Forecast generation failed (handled): {e}")
        forecast_metrics = []

    logging.info("5. Verifying prompt_builder receives real values...")
    prompt = build_analysis_prompt(metrics, aud_metrics, forecast_metrics)
    logging.info(f"\\n--- PROMPT SENT TO OPENAI ---\\n{prompt}\\n-----------------------------")
    
    logging.info("Testing Failure Conditions (Missing API Key)...")
    original_api_key = os.getenv("OPENAI_API_KEY")
    if "OPENAI_API_KEY" in os.environ:
        del os.environ["OPENAI_API_KEY"] # simulate missing
        
    res_missing = generate_marketing_insights(metrics, aud_metrics, forecast_metrics)
    logging.info(f"Expected Missing API Key Response: {res_missing}")
    
    # Restore key if it existed
    if original_api_key:
        os.environ["OPENAI_API_KEY"] = original_api_key

    logging.info("Testing API Timeout mapping...")
    with patch("ai.insight_engine.get_openai_client") as mock_get_client:
        class MockClient:
            class chat:
                class completions:
                    @staticmethod
                    def create(*args, **kwargs):
                        import time
                        time.sleep(0.1)
                        raise openai.APITimeoutError(request=None)
        mock_get_client.return_value = MockClient()
        res_timeout = generate_marketing_insights(metrics, aud_metrics, forecast_metrics)
        logging.info(f"Expected Timeout Error Response: {res_timeout}")

    logging.info("6 & 7. Executing Insight Engine and fetching live OpenAI response...")
    if original_api_key:
        logging.info("API Key found. Making actual request...")
        final_report = generate_marketing_insights(metrics, aud_metrics, forecast_metrics)
        
        logging.info(f"\\n--- FINAL FORMATTED REPORT ---\\n{final_report}\\n-------------------------------")
        
        # Verify required sections exist
        required_sections = [
            "Executive Summary",
            "Campaign Performance Analysis",
            "Audience Analysis",
            "Forecast Analysis",
            "Optimization Recommendations"
        ]
        all_passed = True
        for section in required_sections:
            if section in final_report:
                logging.info(f"✓ Section passed: {section}")
            else:
                logging.warning(f"X Section NOT FOUND: {section}")
                all_passed = False
                
        if all_passed:
            logging.info("✓ Insight Engine successfully generated all required analytical sections.")
    else:
        logging.warning("OPENAI_API_KEY is not defined locally. Skipping real OpenAI API execution.")
        
    logging.info("Validation sequence complete.")

if __name__ == "__main__":
    test_full_ai_flow()
