from fastapi import APIRouter, HTTPException
import requests
from typing import Optional
import json

router = APIRouter()

# CoinGecko base URL (free, no API key needed)
COINGECKO_BASE = "https://api.coingecko.com/api/v3"

# Nomics base URL (free tier, no key for basic historical data)
NOMICS_BASE = "https://api.nomics.com/v1"

@router.get("/price/{coin_id}")
async def get_price(coin_id: str, vs_currency: str = "usd"):
    """
    Fetch real-time price and market data for a cryptocurrency.
    Example: /agents/price/bitcoin?vs_currency=usd
    """
    try:
        url = f"{COINGECKO_BASE}/simple/price"
        params = {
            "ids": coin_id,
            "vs_currencies": vs_currency,
            "include_market_cap": "true",
            "include_24hr_vol": "true",
            "include_24hr_change": "true"
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if coin_id not in data:
            raise HTTPException(status_code=404, detail="Coin not found")
        
        return {
            "coin_id": coin_id,
            "price": data[coin_id][vs_currency],
            "market_cap": data[coin_id].get(f"{vs_currency}_market_cap", None),
            "volume_24h": data[coin_id].get(f"{vs_currency}_24h_vol", None),
            "change_24h": data[coin_id].get(f"{vs_currency}_24h_change", None)
        }
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"API request failed: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.get("/history/{coin_id}")
async def get_history(coin_id: str, days: int = 30):
    """
    Fetch historical price data for a cryptocurrency (last N days).
    Example: /agents/history/bitcoin?days=30
    Uses Nomics for normalized historical data.
    """
    try:
        url = f"{NOMICS_BASE}/candles"
        params = {
            "currency": coin_id.upper() + "-USD",  # e.g., BTC-USD
            "start": f"{days}d",  # Last N days
            "interval": "1d",  # Daily intervals
            "limit": days
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if not data:
            raise HTTPException(status_code=404, detail="No historical data found")
        
        # Simplify response: list of [timestamp, price]
        history = [{"timestamp": int(candle[0]), "price": float(candle[1])} for candle in data]
        return {
            "coin_id": coin_id,
            "history": history,
            "days": days
        }
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"API request failed: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.get("/predict/{coin_id}")
async def predict_trend(coin_id: str, days: int = 7):
    """
    Simple prediction: Fetch historical data and compute a basic trend (7-day moving average slope).
    This is a naive demo—use for illustration only. Integrate ML for real predictions.
    Example: /agents/predict/bitcoin?days=7
    """
    try:
        # Fetch history
        history_url = f"{NOMICS_BASE}/candles"
        params = {
            "currency": coin_id.upper() + "-USD",
            "start": f"{days * 2}d",  # Fetch more data for averaging
            "interval": "1d",
            "limit": days * 2
        }
        response = requests.get(history_url, params=params, timeout=10)
        response.raise_for_status()
        candles = response.json()
        
        if len(candles) < days:
            raise HTTPException(status_code=404, detail="Insufficient historical data")
        
        # Extract prices
        prices = [float(candle[1]) for candle in candles[-days:]]  # Last N days
        
        # Simple moving average (SMA) for trend
        sma = sum(prices) / len(prices)
        
        # Basic slope (trend direction): (last - first) / days
        slope = (prices[-1] - prices[0]) / days
        
        prediction = {
            "predicted_trend": "bullish" if slope > 0 else "bearish" if slope < 0 else "neutral",
            "slope": slope,
            "current_sma": sma,
            "last_price": prices[-1],
            "disclaimer": "This is a basic trend indicator using open-source data. Not financial advice."
        }
        
        return {
            "coin_id": coin_id,
            "analysis_period_days": days,
            "prediction": prediction
        }
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"API request failed: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")