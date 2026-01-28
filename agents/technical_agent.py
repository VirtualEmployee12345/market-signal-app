import yfinance as yf
from typing import Dict, Any

class TechnicalAgent:
    def __init__(self, symbol: str):
        self.symbol = symbol

    def _detect_candlesticks(self, df):
        """Advanced candlestick pattern detection logic for Weekly timeframe"""
        if len(df) < 3: return "Scanning..."
        
        curr = df.iloc[-1]
        prev = df.iloc[-2]
        prev2 = df.iloc[-3]
        
        # Calculations
        body = abs(curr['Close'] - curr['Open'])
        prev_body = abs(prev['Close'] - prev['Open'])
        range_val = curr['High'] - curr['Low']
        
        # 1. Bullish Engulfing
        if (curr['Close'] > curr['Open'] and prev['Close'] < prev['Open'] and 
            curr['Close'] > prev['Open'] and curr['Open'] < prev['Close']):
            return "🔥 Bullish Engulfing"
            
        # 2. Bearish Engulfing
        if (curr['Close'] < curr['Open'] and prev['Close'] > prev['Open'] and 
            curr['Close'] < prev['Open'] and curr['Open'] > prev['Close']):
            return "💀 Bearish Engulfing"
            
        # 3. Hammer (Bottoming signal)
        lower_shadow = min(curr['Open'], curr['Close']) - curr['Low']
        if lower_shadow > (2 * body) and (curr['High'] - max(curr['Open'], curr['Close'])) < (0.1 * body):
            return "🔨 Bullish Hammer"
            
        # 4. Shooting Star (Topping signal)
        upper_shadow = curr['High'] - max(curr['Open'], curr['Close'])
        if upper_shadow > (2 * body) and (min(curr['Open'], curr['Close']) - curr['Low']) < (0.1 * body):
            return "☄️ Shooting Star"

        # 5. Morning Star
        if (prev2['Close'] < prev2['Open'] and body > 0 and 
            curr['Close'] > curr['Open'] and curr['Close'] > (prev2['Open'] + prev2['Close'])/2):
            return "🌅 Morning Star"

        return "Neutral / Consolidation"

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
