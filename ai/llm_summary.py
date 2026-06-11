from ai.insight_engine import generate_insights

def summarize_campaign(campaign_data: dict) -> str:
    \"\"\"Format campaign data and send to LLM for summary.\"\"\"
    prompt = f"Summarize to a marketing executive the campaign performance: {campaign_data}"
    return generate_insights(prompt)
