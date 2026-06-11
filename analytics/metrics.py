import pandas as pd

def calculate_ctr(clicks, impressions) -> float:
    return (clicks / impressions) * 100 if impressions > 0 else 0.0

def calculate_cpc(spend, clicks) -> float:
    return spend / clicks if clicks > 0 else 0.0

def calculate_cpm(spend, impressions) -> float:
    return (spend / impressions) * 1000 if impressions > 0 else 0.0

def calculate_roas(revenue, spend) -> float:
    return revenue / spend if spend > 0 else 0.0

def calculate_cpa(spend, conversions) -> float:
    return spend / conversions if conversions > 0 else 0.0

def calculate_conversion_rate(conversions, clicks) -> float:
    return (conversions / clicks) * 100 if clicks > 0 else 0.0
