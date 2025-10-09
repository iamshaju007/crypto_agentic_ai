from fastapi import FastAPI
from backend.api.crypto import router as crypto_router
from backend.api.predictions import router as predictions_router
from backend.api.agents import router as agents_router
from backend.utils.logger import logger
from backend.db.database import init_db

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
