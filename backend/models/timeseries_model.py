import pandas as pd
from prophet import Prophet

class TimeSeriesModel:
    def prophet_forecast(self, df, periods=30):
        df_prophet = df[["date", "close"]].rename(columns={"date": "ds", "close": "y"})
        model = Prophet()
        model.fit(df_prophet)
        future = model.make_future_dataframe(periods=periods)
        forecast = model.predict(future)
        return forecast[["ds", "yhat"]].rename(columns={"ds": "date", "yhat": "predicted"})