from google.adk.agents import Agent
from google.adk.artifacts import InMemoryArtifactService
from .yahoo_fetch_data.yahoo_fetcher import (
    get_stock_price,
    get_historical_data,
    compare_stocks,
    get_stock_fundamentals,
    get_stock_news
)

root_agent = Agent(
    name="Stock_Analyser",
    model="gemini-2.5-flash-lite",
    description="Agent to analyze stock market data and news.",
    instruction=(
    "You are a helpful financial expert. Use tools for real-time data. "
    "For Indian stocks listed on NSE, always append '.NS' to the ticker symbol (e.g., TCS.NS, INFY.NS, RELIANCE.NS). "
    "For BSE listed stocks, append '.BO'."
),
    tools=[get_stock_price, get_historical_data, compare_stocks, get_stock_fundamentals, get_stock_news],
)
