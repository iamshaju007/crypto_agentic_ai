from pycoingecko import CoinGeckoAPI
from utils.config import get_config

class CoinGeckoService:
    def __init__(self):
        # CoinGecko free API does not require an API key
        self.client = CoinGeckoAPI()

    def get_crypto_list(self):
        return self.client.get_coins_list()

    def get_historical_data(self, symbol: str, start_date: str, end_date: str):
        # Placeholder: Fetch data for the given date range
        return [{"date": "2023-01-01", "close": 1000.0}]
