import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import math

try:
    import xgboost as xgb
    HAS_XGB = True
except ImportError:
    HAS_XGB = False

def extract_time_features(df: pd.DataFrame, date_col='Date') -> pd.DataFrame:
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])
    df['Day_of_Year'] = df[date_col].dt.dayofyear
    df['Day_of_Week'] = df[date_col].dt.dayofweek
    df['Month'] = df[date_col].dt.month
    df['Trend'] = (df[date_col] - df[date_col].min()).dt.days
    return df

def train_and_evaluate(df: pd.DataFrame, target_metric: str):
    """Train model and return model along with evaluation metrics."""
    df_features = extract_time_features(df)
    features = ['Day_of_Year', 'Day_of_Week', 'Month', 'Trend']
    
    # Needs to be sorted by date to evaluate properly
    df_features = df_features.sort_values(by='Date')
    X = df_features[features]
    y = df_features[target_metric]
    
    # Train-test split (80-20 chronological)
    split_idx = int(len(X) * 0.8)
    if split_idx == 0:
        split_idx = 1 # fallback for tiny datasets
        
    X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
    y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]
    
    if HAS_XGB:
        model = xgb.XGBRegressor(n_estimators=100, random_state=42)
    else:
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    
    rmse = math.sqrt(mean_squared_error(y_test, predictions))
    mae = mean_absolute_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)
    
    # Calculate predicted series against the entire X for Actual vs Predicted
    all_predictions = model.predict(X)
    
    metrics = {"RMSE": rmse, "MAE": mae, "R2": r2}
    return model, features, metrics, df_features['Date'], all_predictions
