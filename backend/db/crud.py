"""
CRUD operations for storing and retrieving cryptocurrency historical data.
"""

from datetime import datetime
from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError

from .schemas import HistoricalData


async def save_historical_data(symbol: str, data: List[dict], db: AsyncSession) -> None:
    """
    Save historical cryptocurrency data into the database.

    Args:
        symbol (str): Cryptocurrency symbol (e.g., 'bitcoin').
        data (List[dict]): List of data points with 'date' and 'close' values.
        db (AsyncSession): SQLAlchemy asynchronous session.
    """
    if db is None:
        raise ValueError("Database session (db) must be provided.")

    try:
        for item in data:
            record = HistoricalData(
                symbol=symbol,
                date=datetime.strptime(item["date"], "%Y-%m-%d"),
                close=item["close"],
            )
            db.add(record)
        await db.commit()
    except (KeyError, ValueError) as e:
        await db.rollback()
        raise ValueError(f"Invalid data format while saving: {str(e)}") from e
    except SQLAlchemyError as e:
        await db.rollback()
        raise RuntimeError(f"Database error while saving data: {str(e)}") from e


async def get_historical_data(
    symbol: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: Optional[AsyncSession] = None,
) -> List[dict]:
    """
    Retrieve historical cryptocurrency data for a given symbol and date range.

    Args:
        symbol (str): Cryptocurrency symbol (e.g., 'bitcoin').
        start_date (Optional[str]): Start date in 'YYYY-MM-DD' format.
        end_date (Optional[str]): End date in 'YYYY-MM-DD' format.
        db (Optional[AsyncSession]): SQLAlchemy asynchronous session.

    Returns:
        List[dict]: A list of historical records with 'date' and 'close' keys.
    """
    if db is None:
        raise ValueError("Database session (db) must be provided.")

    try:
        query = select(HistoricalData).filter(HistoricalData.symbol == symbol)

        if start_date:
            query = query.filter(
                HistoricalData.date >= datetime.strptime(start_date, "%Y-%m-%d")
            )
        if end_date:
            query = query.filter(
                HistoricalData.date <= datetime.strptime(end_date, "%Y-%m-%d")
            )

        result = await db.execute(query)
        records = result.scalars().all()

        return [
            {"date": r.date.strftime("%Y-%m-%d"), "close": r.close}
            for r in records
        ]
    except SQLAlchemyError as e:
        raise RuntimeError(f"Database query failed: {str(e)}") from e
