import pandas as pd
import datetime
from ml.train import train_and_evaluate, extract_time_features

def forecast_future_performance(historical_df: pd.DataFrame, target_metric: str, steps: int = 30):
    """Forecast a metric for number of days ahead."""
    if historical_df.empty:
        return pd.DataFrame(), pd.DataFrame(), {}
        
    df_daily = historical_df.groupby('Date')[target_metric].sum().reset_index()
    df_daily['Date'] = pd.to_datetime(df_daily['Date'])
    
    # Train and Eval
    model, features, metrics, dates, actual_preds = train_and_evaluate(df_daily, target_metric)
    
    # Generating Future Dataframe
    last_date = df_daily['Date'].max()
    future_dates = [pd.to_datetime(last_date) + datetime.timedelta(days=x) for x in range(1, steps + 1)]
    future_df = pd.DataFrame({'Date': future_dates})
    future_df['Date'] = pd.to_datetime(future_df['Date'])
    
    min_date = df_daily['Date'].min()
    future_df['Day_of_Year'] = future_df['Date'].dt.dayofyear
    future_df['Day_of_Week'] = future_df['Date'].dt.dayofweek
    future_df['Month'] = future_df['Date'].dt.month
    future_df['Trend'] = (future_df['Date'] - min_date).dt.days
    
    X_future = future_df[features]
    future_preds = model.predict(X_future)
    future_df['Predicted_' + target_metric] = future_preds
    
    # Prep Actual vs Predicted dataframe mapping
    df_eval = pd.DataFrame({
        'Date': dates,
        'Actual': df_daily.set_index('Date').loc[dates][target_metric].values,
        'Predicted': actual_preds
    }).sort_values(by='Date')
    
    return df_eval, future_df, metrics
