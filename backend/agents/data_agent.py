from .base_agent import BaseAgent
from crewai import Agent, Task
from services.coingecko_service import CoinGeckoService
from db.crud import save_historical_data

class DataAgent(BaseAgent):
    def create_agent(self):
        return Agent(
            role="Data Agent",
            goal="Fetch and preprocess cryptocurrency data",
            backstory="Expert in crypto data ingestion and preprocessing",
            llm=self.llm,
            tools=[CoinGeckoService()]
        )

    def fetch_and_store_data(self, symbol: str, start_date: str, end_date: str):
        service = CoinGeckoService()
        data = service.get_historical_data(symbol, start_date, end_date)
        save_historical_data(symbol, data)
        return data