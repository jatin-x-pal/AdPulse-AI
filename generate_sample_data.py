import pandas as pd
import numpy as np
import os
import random
from datetime import datetime, timedelta

def generate_sample_data():
    os.makedirs("data/sample", exist_ok=True)
    
    # 1. Generate Campaigns
    platforms = ['Google Ads', 'Meta Ads', 'LinkedIn Ads', 'TikTok Ads']
    campaign_names = [f'Campaign_{i}' for i in range(1, 101)]
    
    campaigns = []
    start_date = datetime.now() - timedelta(days=90)
    
    for i, name in enumerate(campaign_names):
        platform = random.choice(platforms)
        spend = round(random.uniform(500, 10000), 2)
        impressions = int(spend * random.uniform(10, 50))
        clicks = int(impressions * random.uniform(0.01, 0.05))
        conversions = int(clicks * random.uniform(0.05, 0.20))
        revenue = round(conversions * random.uniform(50, 200), 2)
        
        # generate dates across the last 90 days
        c_date = start_date + timedelta(days=random.randint(0, 90))
        
        campaigns.append({
            "Campaign_ID": i + 1,
            "Campaign_Name": name,
            "Platform": platform,
            "Spend": spend,
            "Revenue": revenue,
            "Clicks": clicks,
            "Impressions": impressions,
            "Conversions": conversions,
            "Date": c_date.strftime("%Y-%m-%d")
        })
        
    df_campaigns = pd.DataFrame(campaigns)
    df_campaigns.to_csv("data/sample/campaigns.csv", index=False)
    
    # 2. Generate Audiences
    age_groups = ['18-24', '25-34', '35-44', '45-54', '55+']
    devices = ['Mobile', 'Desktop', 'Tablet']
    genders = ['Male', 'Female', 'Unknown']
    locations = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Miami', 'London', 'Berlin', 'Tokyo', 'Sydney', 'Delhi']
    
    audiences = []
    # simulate audience breakdown for each campaign
    audience_id = 1
    for camp in campaigns:
        # Create 5-10 audience segments for each campaign
        num_segments = random.randint(5, 10)
        for _ in range(num_segments):
            audiences.append({
                "Audience_ID": audience_id,
                "Age_Group": random.choice(age_groups),
                "Gender": random.choice(genders),
                "Device": random.choice(devices),
                "Location": random.choice(locations),
                "Campaign_ID": camp['Campaign_ID']
            })
            audience_id += 1
            
    df_audiences = pd.DataFrame(audiences)
    df_audiences.to_csv("data/sample/audiences.csv", index=False)
    print("Sample data generated successfully in data/sample/")

if __name__ == "__main__":
    generate_sample_data()
