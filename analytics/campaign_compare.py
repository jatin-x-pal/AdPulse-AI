import pandas as pd

def compare_campaigns(df: pd.DataFrame, campaign_ids: list) -> pd.DataFrame:
    \"\"\"Return comparison of requested campaigns.\"\"\"
    return df[df['Campaign_ID'].isin(campaign_ids)]
