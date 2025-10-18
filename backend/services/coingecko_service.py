"""
CoinGecko Service Module.

Provides methods to interact with the CoinGecko API, including fetching
the list of cryptocurrencies and historical price data.
"""

# --- Standard Library Imports ---
from datetime import datetime

# --- Third-Party Imports ---
from pycoingecko import CoinGeckoAPI

# --- Local Imports ---
from utils.config import get_config


class CoinGeckoService:
    """
    Service class for interacting with the CoinGecko API.
    Provides methods to fetch crypto lists and historical price data.
    """

    def __init__(self):
        self.client = CoinGeckoAPI()
        self.config = get_config()

    def get_crypto_list(self):
        """
        Fetch a list of all available cryptocurrencies from CoinGecko.
        :return: List of coin dictionaries
        """
        try:
            coin_list = self.client.get_coins_list()
            return coin_list
        except RuntimeError as e:
            print(f"❌ Runtime error fetching crypto list: {e}")
            return []
        except Exception as e:  # fallback for unexpected errors
            print(f"❌ Unexpected error fetching crypto list: {e}")
            return []

    def get_historical_data(self, symbol: str, start_date: str, end_date: str):
        """
        Fetch historical price data for a given crypto symbol between two dates.

        :param symbol: The cryptocurrency symbol (e.g., 'bitcoin')
        :param start_date: Start date in 'YYYY-MM-DD' format
        :param end_date: End date in 'YYYY-MM-DD' format
        :return: List of dicts containing 'date' and 'price'
        """
        try:
            # Convert dates to UNIX timestamps
            start_ts = int(datetime.strptime(start_date, "%Y-%m-%d").timestamp())
            end_ts = int(datetime.strptime(end_date, "%Y-%m-%d").timestamp())

            # Fetch market data in USD
            market_data = self.client.get_coin_market_chart_range_by_id(
                id=symbol,
                vs_currency="usd",
                from_timestamp=start_ts,
                to_timestamp=end_ts
            )

            # Extract and format price data
            raw_prices = market_data.get("prices", [])
            formatted_data = [
                {
                    "date": datetime.utcfromtimestamp(item[0] / 1000).strftime("%Y-%m-%d"),
                    "price": round(item[1], 2)
                }
                for item in raw_prices
            ]
            return formatted_data

        except RuntimeError as e:
            print(f"❌ Runtime error fetching historical data for {symbol}: {e}")
            return []
        except Exception as e:
            print(f"❌ Unexpected error fetching historical data for {symbol}: {e}")
            return []


# --- Quick Test (Remove in Production) ---
if __name__ == "__main__":
    service = CoinGeckoService()
    coin_list = service.get_crypto_list()
    print(f"✅ Total coins fetched: {len(coin_list)}")

    sample_data = service.get_historical_data("bitcoin", "2023-01-01", "2023-01-10")
    print(f"📊 Sample historical data: {sample_data[:3]}")
