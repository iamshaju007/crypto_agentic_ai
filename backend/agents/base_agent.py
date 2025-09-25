from abc import ABC, abstractmethod
from crewai import Agent
from utils.config import get_config

class BaseAgent(ABC):
    def __init__(self):
        self.config = get_config()
        self.llm = self._init_llm()

    def _init_llm(self):
        from langchain.llms import LLaMACpp
        return LLaMACpp(model_path=self.config["llm_model_path"], n_ctx=2048)

    @abstractmethod
    def create_agent(self):
        pass