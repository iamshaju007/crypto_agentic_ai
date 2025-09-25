from dotenv import load_dotenv
import os

def get_config():
    load_dotenv()
    return {
        "DATABASE_URL": os.getenv("DATABASE_URL"),
        "REDIS_URL": os.getenv("REDIS_URL"),
        "COINGECKO_API_KEY": os.getenv("COINGECKO_API_KEY"),
        "llm_model_path": os.getenv("LLM_MODEL_PATH", "/path/to/llama2")
    }