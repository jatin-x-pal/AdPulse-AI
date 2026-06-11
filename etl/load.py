import pandas as pd
from datetime import datetime
from database.db import SessionLocal, engine, Base
from database.models import Campaign, Audience

def init_db():
    """Initialize or reset the sqlite tables based on SQLAlchemy models."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

def run_etl_pipeline():
    """Extract CSVs, clean data, and load into SQLite using SQLAlchemy ORM."""
    init_db()
    db = SessionLocal()
    
    try:
        # Extract from local CSVs
        df_c = pd.read_csv("data/sample/campaigns.csv")
        df_a = pd.read_csv("data/sample/audiences.csv")
        
        # Clean Data (Transform)
        df_c = df_c.drop_duplicates()
        df_c['Spend'] = df_c['Spend'].fillna(0.0)
        df_c['Revenue'] = df_c['Revenue'].fillna(0.0)
        
        df_a = df_a.drop_duplicates().fillna("Unknown")
        
        # Load Campaigns
        campaigns_to_insert = []
        for _, row in df_c.iterrows():
            c = Campaign(
                id=int(row['Campaign_ID']),
                name=str(row['Campaign_Name']),
                platform=str(row['Platform']),
                spend=float(row['Spend']),
                revenue=float(row['Revenue']),
                clicks=int(row['Clicks']),
                impressions=int(row['Impressions']),
                conversions=int(row['Conversions']),
                date=datetime.strptime(row['Date'], "%Y-%m-%d").date()
            )
            campaigns_to_insert.append(c)
        
        db.add_all(campaigns_to_insert)
        db.commit()
        
        # Load Audiences
        audiences_to_insert = []
        for _, row in df_a.iterrows():
            a = Audience(
                id=int(row['Audience_ID']),
                age_group=str(row['Age_Group']),
                gender=str(row['Gender']),
                device=str(row['Device']),
                location=str(row['Location']),
                campaign_id=int(row['Campaign_ID'])
            )
            audiences_to_insert.append(a)
            
        db.add_all(audiences_to_insert)
        db.commit()
        print("Data loaded into SQLite database successfully.")
        
    except Exception as e:
        db.rollback()
        print(f"ETL transaction failed: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    run_etl_pipeline()
