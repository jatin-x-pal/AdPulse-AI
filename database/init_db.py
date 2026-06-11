import os
import pandas as pd
from sqlalchemy import text
from database.db import engine, Base
import database.models  # ensure models are registered with Base
from generate_sample_data import generate_sample_data
import streamlit as st

def populate_sample_data():
    """Generates the CSVs locally and ingests them into the SQLite database dynamically."""
    generate_sample_data()
    
    if os.path.exists("data/sample/campaigns.csv") and os.path.exists("data/sample/audiences.csv"):
        df_camp = pd.read_csv("data/sample/campaigns.csv")
        df_aud = pd.read_csv("data/sample/audiences.csv")
        
        # Add to database
        # `if_exists="append"` ensures we follow the SQLAlchemy schema constraints gracefully if possible.
        df_camp.to_sql("campaigns", con=engine, if_exists="append", index=False)
        df_aud.to_sql("audiences", con=engine, if_exists="append", index=False)
        return True
    return False

@st.cache_resource
def initialize_database():
    """Creates the schemas and seeds the database if no records exist."""
    # 1. Ensure all schemas defined in models.py are created (no-op if tables already exist)
    Base.metadata.create_all(bind=engine)
    
    # 2. Check if data exists within the main campaigns table
    try:
        with engine.connect() as con:
            result = con.execute(text("SELECT count(*) FROM campaigns")).scalar()
            
            if result == 0:
                print("Database is empty. Populating with initial sample data...")
                populate_sample_data()
                print("Database populated successfully.")
    except Exception as e:
        print(f"Error during database initialization: {e}")
