from typing import Dict, Any
import requests
import os

class SentimentAgent:
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.exa_api_key = os.environ.get("EXA_API_KEY")

    def analyze(self) -> Dict[str, Any]:
        if not self.exa_api_key:
            return {
                "symbol": self.symbol,
                "sentiment": "Neutral",
                "summary": "Exa API key missing. Defaulting to neutral sentiment."
            }
        
        # In a real MCP setup, we'd use the exa tool. 
        # Here we simulate the logic for the agent's internal process.
        query = f"latest stock market news and investor sentiment for {self.symbol} in the last 7 days"
        
        try:
            # Placeholder for actual Exa MCP call logic
            # This demonstrates how the agent expects to interact with the search layer
            return {
                "symbol": self.symbol,
                "sentiment": "Slightly Bullish",
                "sources": 3,
                "summary": f"Exa found positive momentum regarding {self.symbol}'s latest earnings preview."
            }
        except Exception:
            return {"symbol": self.symbol, "sentiment": "Error", "summary": "Failed to fetch sentiment via Exa."}
