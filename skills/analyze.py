import json
import os
from datetime import datetime
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agents.technical_agent import TechnicalAgent
from agents.fundamental_agent import FundamentalAgent
from agents.sentiment_agent import SentimentAgent
from agents.risk_agent import RiskAgent

RESULTS_FILE = 'analysis_results.json'

def run_orchestration(symbols=["SPY", "ES=F", "NQ=F", "CL=F", "GC=F", "BTC-USD", "ETH-USD", "SOL-USD", "TSLA", "PLTR", "NVDA", "GOOGL", "AAPL", "MSFT", "AMZN", "META", "BRK-B", "LLY", "AVGO", "V", "NVO", "JPM", "TSM", "WMT", "UNH", "MA", "PG", "ASML", "ORCL", "COST", "HD", "TM"]):
    print(f"Starting analysis for {len(symbols)} symbols...")
    
    results = []
    if os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, 'r') as f:
            try:
                results = json.load(f)
            except json.JSONDecodeError:
                results = []

    for symbol in symbols:
        tech = TechnicalAgent(symbol).analyze()
        fund = FundamentalAgent(symbol).analyze()
        sent = SentimentAgent(symbol).analyze()
        
        risk = RiskAgent(symbol).analyze({
            "technical": tech,
            "fundamental": fund,
            "sentiment": sent
        })
        
        final_result = {
            "timestamp": datetime.now().isoformat(),
            "symbol": symbol,
            "technical": tech,
            "fundamental": fund,
            "sentiment": sent,
            "risk": risk
        }
        
        results.insert(0, final_result)
        
        # Telegram Signal Loop (Only send if there is a clear recommendation or for high-priority futures)
        recommendation = risk.get('recommendation', 'Hold')
        if recommendation in ["Buy", "Sell"]:
            emoji = "🟢" if recommendation == "Buy" else "🔴"
            weekly_p = tech.get('weekly_pattern', 'N/A')
            
            msg = (
                f"{emoji} *VEE SIGNAL: {symbol}*\n\n"
                f"*Recommendation:* {recommendation}\n"
                f"*Price:* ${tech.get('current_price')}\n"
                f"*Weekly Pattern:* {weekly_p}\n"
                f"*Risk:* {risk.get('risk_level')}\n\n"
                f"*GAME PLAN:*\n"
                f"1. *Technical:* {tech.get('summary')}\n"
                f"2. *Fundamental:* {fund.get('summary')}\n"
                f"3. *Sentiment:* {sent.get('summary')}\n\n"
                f"_[VEE_SIGNAL_AUTONOMOUS_ORCHESTRATION]_"
            )
            print(f"TELEGRAM_SIGNAL: {msg}")

    with open(RESULTS_FILE, 'w') as f:
        json.dump(results[:100], f, indent=4)
        
    print(f"Analysis complete for all symbols.")
    return results

if __name__ == "__main__":
    run_orchestration()
