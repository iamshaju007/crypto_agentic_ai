from fastapi import FastAPI
from api.crypto import router as crypto_router
from api.predictions import router as predictions_router
from api.agents import router as agents_router
from utils.logger import logger
from db.database import init_db

app = FastAPI(title="Crypto AI API")

# Include routers
app.include_router(crypto_router, prefix="/crypto")
app.include_router(predictions_router, prefix="/predictions")
app.include_router(agents_router, prefix="/agents")

# Initialize database
@app.on_event("startup")
async def startup_event():
    await init_db()
    logger.info("Application startup: Database initialized")

@app.get("/")
async def root():
    return {"message": "Crypto AI API"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
