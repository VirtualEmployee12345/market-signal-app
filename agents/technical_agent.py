import yfinance as yf
from typing import Dict, Any

class TechnicalAgent:
    def __init__(self, symbol: str):
        self.symbol = symbol

    def _detect_candlesticks(self, df):
        """Simple candlestick pattern detection logic for Weekly timeframe"""
        if len(df) < 2: return "No Pattern"
        
        last_week = df.iloc[-1]
        prev_week = df.iloc[-2]
        
        # Bullish Engulfing
        if (last_week['Close'] > last_week['Open'] and 
            prev_week['Close'] < prev_week['Open'] and
            last_week['Close'] > prev_week['Open'] and
            last_week['Open'] < prev_week['Close']):
            return "Bullish Engulfing"
            
        # Hammer
        body = abs(last_week['Close'] - last_week['Open'])
        lower_shadow = last_week['Open'] - last_week['Low'] if last_week['Close'] > last_week['Open'] else last_week['Close'] - last_week['Low']
        if lower_shadow > (2 * body) and (last_week['High'] - max(last_week['Open'], last_week['Close'])) < body:
            return "Hammer"

        return "Neutral / No Clear Pattern"

    def analyze(self) -> Dict[str, Any]:
        ticker = yf.Ticker(self.symbol)
        
        # Daily for MA
        hist_daily = ticker.history(period="3mo")
        # Weekly for Candlesticks
        hist_weekly = ticker.history(period="6mo", interval="1wk")
        
        if hist_daily.empty or hist_weekly.empty:
            return {"error": "No data found"}
            
        current_price = hist_daily['Close'].iloc[-1]
        ma_20 = hist_daily['Close'].rolling(window=20).mean().iloc[-1]
        ma_50 = hist_daily['Close'].rolling(window=50).mean().iloc[-1]
        
        candle_pattern = self._detect_candlesticks(hist_weekly)
        
        signal = "Neutral"
        if current_price > ma_20 and current_price > ma_50:
            signal = "Bullish"
        elif current_price < ma_20:
            signal = "Bearish"
            
        return {
            "symbol": self.symbol,
            "current_price": round(current_price, 2),
            "ma_20": round(ma_20, 2),
            "ma_50": round(ma_50, 2),
            "signal": signal,
            "weekly_pattern": candle_pattern,
            "summary": f"Trend is {signal}. Weekly Pattern: {candle_pattern}."
        }
