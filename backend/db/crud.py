from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import HistoricalData
from sqlalchemy.future import select
from datetime import datetime

async def save_historical_data(symbol: str, data: list, db: AsyncSession):
    for item in data:
        record = HistoricalData(symbol=symbol, date=datetime.strptime(item["date"], "%Y-%m-%d"), close=item["close"])
        db.add(record)
    await db.commit()

async def get_historical_data(symbol: str, start_date: str = None, end_date: str = None, db: AsyncSession = None):
    query = select(HistoricalData).filter(HistoricalData.symbol == symbol)
    if start_date:
        query = query.filter(HistoricalData.date >= datetime.strptime(start_date, "%Y-%m-%d"))
    if end_date:
        query = query.filter(HistoricalData.date <= datetime.strptime(end_date, "%Y-%m-%d"))
    result = await db.execute(query)
    records = result.scalars().all()
    return [{"date": r.date.strftime("%Y-%m-%d"), "close": r.close} for r in records]