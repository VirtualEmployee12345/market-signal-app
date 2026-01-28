import yfinance as yf
from typing import Dict, Any

class TechnicalAgent:
    def __init__(self, symbol: str):
        self.symbol = symbol

    def analyze(self) -> Dict[str, Any]:
        ticker = yf.Ticker(self.symbol)
        hist = ticker.history(period="1mo")
        
        if hist.empty:
            return {"error": "No data found"}
            
        current_price = hist['Close'].iloc[-1]
        ma_20 = hist['Close'].rolling(window=20).mean().iloc[-1]
        
        signal = "Neutral"
        if current_price > ma_20:
            signal = "Bullish"
        elif current_price < ma_20:
            signal = "Bearish"
            
        return {
            "symbol": self.symbol,
            "current_price": round(current_price, 2),
            "ma_20": round(ma_20, 2),
            "signal": signal,
            "summary": f"Price is {'above' if signal == 'Bullish' else 'below'} 20-day MA."
        }
