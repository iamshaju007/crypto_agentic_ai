from .base_agent import BaseAgent
from crewai import Agent, Task
from models.timeseries_model import TimeSeriesModel
from db.crud import get_historical_data
import pandas as pd

class PredictionAgent(BaseAgent):
    def create_agent(self):
        return Agent(
            role="Prediction Agent",
            goal="Generate price forecasts for cryptocurrencies",
            backstory="Expert in time-series forecasting using ML models",
            llm=self.llm
        )

    def forecast(self, symbol: str, periods: int = 30):
        data = get_historical_data(symbol)
        if not data:
            return []
        df = pd.DataFrame(data)
        model = TimeSeriesModel()
        forecast = model.prophet_forecast(df, periods)
        return forecast.to_dict(orient="records")