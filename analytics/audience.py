import pandas as pd

def get_audience_performance(df_audiences: pd.DataFrame, df_campaigns: pd.DataFrame) -> pd.DataFrame:
    """Join audiences with campaigns to distribute metrics evenly across segments."""
    # Count segments per campaign to divide performance metrics uniformly
    segment_counts = df_audiences.groupby('Campaign_ID').size().to_frame(name='Segment_Count').reset_index()
    df_merged = df_audiences.merge(segment_counts, on='Campaign_ID', how='inner')
    df_full = df_merged.merge(df_campaigns[['Campaign_ID', 'Spend', 'Conversions', 'Revenue']], on='Campaign_ID', how='inner')
    
    # Prorate the campaign values by number of segments (simple approximation)
    df_full['Segment_Spend'] = df_full['Spend'] / df_full['Segment_Count']
    df_full['Segment_Conversions'] = df_full['Conversions'] / df_full['Segment_Count']
    df_full['Segment_Revenue'] = df_full['Revenue'] / df_full['Segment_Count']
    
    return df_full

def segment_by_age(df_merged: pd.DataFrame) -> pd.DataFrame:
    """Return aggregated conversions by age group."""
    return df_merged.groupby('Age_Group')[['Segment_Spend', 'Segment_Conversions', 'Segment_Revenue']].sum().reset_index()

def segment_by_device(df_merged: pd.DataFrame) -> pd.DataFrame:
    """Return aggregated metrics by device."""
    return df_merged.groupby('Device')[['Segment_Spend', 'Segment_Conversions', 'Segment_Revenue']].sum().reset_index()
