from typing import Dict, Any

class RiskAgent:
    def __init__(self, symbol: str):
        self.symbol = symbol

    def analyze(self, results: Dict[str, Any]) -> Dict[str, Any]:
        tech = results.get('technical', {})
        tech_signal = tech.get('signal', 'Neutral')
        weekly_pattern = tech.get('weekly_pattern', '')
        
        # Bullish Conditions
        is_bullish_pattern = any(p in weekly_pattern for p in ["Engulfing", "Hammer", "Morning Star"]) and "Bullish" in weekly_pattern
        is_bearish_pattern = any(p in weekly_pattern for p in ["Engulfing", "Shooting Star"]) and "Bearish" in weekly_pattern

        recommendation = "Hold"
        
        # Weighting Weekly Patterns Heavily
        if tech_signal == "Bullish":
            recommendation = "Buy"
            if is_bearish_pattern:
                recommendation = "Hold (Weekly Divergence)"
        elif tech_signal == "Bearish":
            recommendation = "Sell"
            if is_bullish_pattern:
                recommendation = "Hold (Weekly Support)"
        
        # Overriding with high-conviction weekly patterns
        if "🔥 Bullish Engulfing" in weekly_pattern:
            recommendation = "Strong Buy"
        elif "💀 Bearish Engulfing" in weekly_pattern:
            recommendation = "Strong Sell"
            
        return {
            "symbol": self.symbol,
            "recommendation": recommendation,
            "risk_level": "High" if "Strong" in recommendation else "Medium",
            "summary": f"Recommendation: {recommendation}. Priority given to Weekly Patterns."
        }
