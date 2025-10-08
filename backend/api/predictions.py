from typing import List
from fastapi import APIRouter, HTTPException
import requests

router = APIRouter()

# CoinGecko base URL (free, no API key needed)
COINGECKO_BASE = "https://api.coingecko.com/api/v3"

# Nomics base URL (free tier, no key for basic historical data)
NOMICS_BASE = "https://api.nomics.com/v1"

@router.get("/")
async def predictions_root():
    """
    Root endpoint for predictions API.
    """
    return {"message": "Predictions API"}

@router.get("/trend/{coin_id}")
async def get_trend(coin_id: str, days: int = 14, vs_currency: str = "usd"):
    """
    Fetch historical data and compute a simple trend prediction (e.g., moving average slope).
    Example: /predictions/trend/bitcoin?days=14&vs_currency=usd
    This is a demo—extend with ML for real predictions.
    """
    try:
        url = f"{NOMICS_BASE}/candles"
        params = {
            "currency": f"{coin_id.upper()}-USD",  # e.g., BTC-USD
            "start": f"{days}d",  # Last N days
            "interval": "1d",  # Daily intervals
            "limit": days
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if not data:
            raise HTTPException(status_code=404, detail="No historical data found")
        
        # Extract closing prices
        prices = [float(candle[1]) for candle in data]
        if len(prices) < 2:
            raise HTTPException(status_code=404, detail="Insufficient data for trend analysis")
        
        # Compute simple moving average (SMA) and slope
        sma = sum(prices) / len(prices)
        slope = (prices[-1] - prices[0]) / len(prices)
        
        return {
            "coin_id": coin_id,
            "days": days,
            "trend": {
                "direction": "bullish" if slope > 0 else "bearish" if slope < 0 else "neutral",
                "slope": slope,
                "current_sma": sma,
                "last_price": prices[-1],
                "disclaimer": "This is a basic trend indicator using open-source data. Not financial advice."
            }
        }
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"API request failed: {str(e)}") from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}") from e

@router.get("/volatility")
async def get_volatility(coin_ids: str, days: int = 7, vs_currency: str = "usd"):
    """
    Compare volatility (standard deviation of daily returns) for multiple coins.
    Example: /predictions/volatility?coin_ids=bitcoin,ethereum&days=7&vs_currency=usd
    """
    try:
        coin_list = coin_ids.split(",")
        if not coin_list:
            raise HTTPException(status_code=400, detail="At least one coin_id is required")
        
        results = []
        for coin_id in coin_list:
            url = f"{NOMICS_BASE}/candles"
            params = {
                "currency": f"{coin_id.upper()}-USD",
                "start": f"{days}d",
                "interval": "1d",
                "limit": days
            }
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if not data:
                continue  # Skip if no data for this coin
            
            # Calculate daily returns and volatility
            prices = [float(candle[1]) for candle in data]
            if len(prices) < 2:
                continue
            
            # Daily returns: (price[i] - price[i-1]) / price[i-1]
            returns = [(prices[i] - prices[i-1]) / prices[i-1] for i in range(1, len(prices))]
            if not returns:
                continue
            
            # Volatility: standard deviation of returns
            mean_return = sum(returns) / len(returns)
            variance = sum((r - mean_return) ** 2 for r in returns) / len(returns)
            volatility = (variance ** 0.5) if variance > 0 else 0
            
            results.append({
                "coin_id": coin_id,
                "volatility": volatility,
                "last_price": prices[-1],
                "days": days
            })
        
        if not results:
            raise HTTPException(status_code=404, detail="No data available for the specified coins")
        
        return {
            "coins": results,
            "vs_currency": vs_currency,
            "disclaimer": "Volatility based on daily returns from open-source data. Not financial advice."
        }
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"API request failed: {str(e)}") from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}") from e
