import pandas as pd

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    \"\"\"Handle missing values, remove duplicates, etc.\"\"\"
    df = df.drop_duplicates()
    df = df.fillna(0)
    return df

def feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    \"\"\"Add new features like CTR, CPC, ROAS, etc.\"\"\"
    return df
