import yfinance as yf
from typing import Dict, Any

class FundamentalAgent:
    def __init__(self, symbol: str):
        self.symbol = symbol

    def analyze(self) -> Dict[str, Any]:
        ticker = yf.Ticker(self.symbol)
        info = ticker.info
        
        pe_ratio = info.get('forwardPE', 'N/A')
        market_cap = info.get('marketCap', 'N/A')
        
        return {
            "symbol": self.symbol,
            "pe_ratio": pe_ratio,
            "market_cap": market_cap,
            "summary": f"P/E Ratio: {pe_ratio}. Market Cap: {market_cap}."
        }
