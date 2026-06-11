import json
import datetime

def build_analysis_prompt(metrics: dict, audiences: list, forecast: list) -> str:
    """Constructs the system prompt asking the LLM to format insights correctly based on data."""
    prompt = f"""
    You are an expert AI Marketing Analyst for a high-end data analytics firm.
    Review the following platform metrics, audience segmentation, and future forecast data to generate an actionable marketing report.
    
    Structure your response strictly using these Markdown headers:
    ## Executive Summary
    ## Campaign Performance Analysis
    ## Audience Analysis
    ## Forecast Analysis
    ## Optimization Recommendations
    
    Avoid inserting any other H2s (##) to maintain template integrity. Use bullet points and paragraphs effectively.
    
    ### Current Metrics Overview:
    {json.dumps(metrics, indent=2, default=str)}
    
    ### Selected Audience Performance:
    {json.dumps(audiences, indent=2, default=str)}
    
    ### 15-Day Revenue Forecast Sample:
    {json.dumps(forecast, indent=2, default=str)}
    """
    return prompt
