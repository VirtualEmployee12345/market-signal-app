# Vee Signal

## Overview
Vee Signal is a Market Analysis & Signal App that leverages Python with Flask for the backend and HTML with Tailwind for the frontend. 

## Architecture
The main application manages four specialized sub-agents:
1. Technical Analysis
2. Fundamental Analysis
3. Sentiment Analysis
4. Risk Manager

## Integrations
- **MCP Connections:**
  - yfinance
  - exa
  - custom telegram-mcp

## Skills
- **/analyze:** This script orchestrates the agents to ingest market data and produce a daily game-plan.

## Scheduling
- A cron job is set up to run the analysis before market open.