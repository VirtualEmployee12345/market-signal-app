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

def run_orchestration(symbol="SPY"):
    print(f"Starting analysis for {symbol}...")
    
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
    
    # Save results
    results = []
    if os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, 'r') as f:
            try:
                results = json.load(f)
            except json.JSONDecodeError:
                results = []
    
    results.insert(0, final_result)
    with open(RESULTS_FILE, 'w') as f:
        json.dump(results[:50], f, indent=4)
        
    # Telegram Signal Loop
    recommendation = risk.get('recommendation', 'Hold')
    emoji = "🟢" if recommendation == "Buy" else "🔴" if recommendation == "Sell" else "🟡"
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
    
    # Trigger telegram send via clawdbot message tool (this will be handled by the session when this script is run via cron or manual trigger)
    print(f"TELEGRAM_SIGNAL: {msg}")
    
    print(f"Analysis complete for {symbol}.")
    return final_result

if __name__ == "__main__":
    run_orchestration()
