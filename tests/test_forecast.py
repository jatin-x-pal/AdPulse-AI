from ml.forecast import forecast_future_performance
import pandas as pd

def test_forecast_future_performance():
    df = pd.DataFrame()
    forecast = forecast_future_performance(df, "Revenue", 7)
    assert len(forecast) == 7
