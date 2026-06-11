import pandas as pd
from database.db import engine
from database.init_db import initialize_database

def extract_campaigns() -> pd.DataFrame:
    """Extract campaign data from SQLite."""
    initialize_database()
    return pd.read_sql("SELECT * FROM campaigns", engine)

def extract_audiences() -> pd.DataFrame:
    """Extract audience data from SQLite."""
    initialize_database()
    return pd.read_sql("SELECT * FROM audiences", engine)

def get_filtered_data(start_date=None, end_date=None, campaigns=None, platforms=None, locations=None):
    """Retrieve filtered campaigns and audiences."""
    initialize_database()
    query_camp = "SELECT * FROM campaigns WHERE 1=1"
    if start_date:
        query_camp += f" AND Date >= '{start_date}'"
    if end_date:
        query_camp += f" AND Date <= '{end_date}'"
    if campaigns and len(campaigns) > 0:
        c_list = "','".join(campaigns)
        query_camp += f" AND Campaign_Name IN ('{c_list}')"
    if platforms and len(platforms) > 0:
        p_list = "','".join(platforms)
        query_camp += f" AND Platform IN ('{p_list}')"
        
    df_camp = pd.read_sql(query_camp, engine)
    
    query_aud = "SELECT * FROM audiences WHERE 1=1"
    if locations and len(locations) > 0:
        l_list = "','".join(locations)
        query_aud += f" AND Location IN ('{l_list}')"
        
    df_aud = pd.read_sql(query_aud, engine)
    
    # Filter audiences by the filtered campaigns
    if not df_camp.empty:
        df_aud = df_aud[df_aud['Campaign_ID'].isin(df_camp['Campaign_ID'])]
        
    return df_camp, df_aud

