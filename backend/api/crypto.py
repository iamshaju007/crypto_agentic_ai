from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.db.database import get_db
from backend.services.coingecko_service import CoinGeckoService
from backend.db.crud import save_historical_data, get_historical_data

router = APIRouter()


class HistoricalDataRequest(BaseModel):
    """
    Request schema for fetching historical cryptocurrency data.
    """
    symbol: str
    start_date: str
    end_date: str


@router.get("/list")
async def list_cryptos():
    """
    Fetch and return the list of available cryptocurrencies.
    """
    try:
        service = CoinGeckoService()
        return service.get_crypto_list()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching crypto list: {str(e)}"
        ) from e  # Added `from e` for clearer traceback


@router.get("/historical")
async def get_historical(symbol: str, start_date: str, end_date: str):
    """
    Fetch historical price data for a given crypto symbol and date range.
    Caches the data in the database if not already stored.
    """
    
    db = next(get_db())
    try:
        data = get_historical_data(symbol, start_date, end_date)

        if not data:
            service = CoinGeckoService()
            data = service.get_historical_data(symbol, start_date, end_date)

            if data:
                # Ensure this function signature matches your CRUD implementation
                await save_historical_data(symbol, data, db)

        return data

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid input: {str(e)}"
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        ) from e
