from .base_agent import BaseAgent
from crewai import Agent, Task
from models.sentiment_model import SentimentModel
from models.trading_rl import TradingRL
import pandas as pd

class StrategyAgent(BaseAgent):
    def create_agent(self):
        return Agent(
            role="Strategy Agent",
            goal="Provide staking and trading recommendations",
            backstory="Expert in crypto trading and staking strategies",
            llm=self.llm
        )

    def get_recommendation(self, symbol: str):
        sentiment_model = SentimentModel()
        sentiment = sentiment_model.analyze(symbol)
        trading_rl = TradingRL()
        action = trading_rl.get_action(symbol)

        if sentiment["score"] > 0.5 and action == "buy":
            return {"recommendation": f"Buy and stake {symbol}: Positive sentiment and RL suggests buy."}
        elif sentiment["score"] < 0.2:
            return {"recommendation": f"Avoid {symbol}: Negative sentiment detected."}
        else:
            return {"recommendation": f"Hold {symbol}: Neutral sentiment and no strong trading signal."}