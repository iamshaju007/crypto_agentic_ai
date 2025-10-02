from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List #type:ignore
from services.coingecko_service import CoinGeckoService
from db.crud import save_historical_data, get_historical_data

router = APIRouter()

class HistoricalDataRequest(BaseModel):
    symbol: str
    start_date: str
    end_date: str

@router.get("/list")
async def list_cryptos():
    service = CoinGeckoService()
    return service.get_crypto_list()

@router.get("/historical")
async def get_historical(symbol: str, start_date: str, end_date: str):
    try:
        data = get_historical_data(symbol, start_date, end_date)
        if not data:
            service = CoinGeckoService()
            data = service.get_historical_data(symbol, start_date, end_date)
            save_historical_data(symbol, data)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))