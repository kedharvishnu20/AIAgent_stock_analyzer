from yahoo_fetch_data.yahoo_fetcher import (
    get_stock_price, 
    get_historical_data, 
    compare_stocks, 
    get_stock_fundamentals, 
    get_stock_news
)
from google.adk.agents import Agent

root_agent = Agent(
    name="Stock_Analyser",
    model="gemini-3.1-flash-lite-preview", 
    description="Agent to analyze stock market data and news.",
    instruction=(
        "You are a helpful financial expert. Use tools for real-time data. "
        "When a tool returns a 'plot_markdown' key, you MUST include that exact "
        "markdown string directly in your response so the user can see the graph."
    ),
    tools=[get_stock_price, get_historical_data, compare_stocks, get_stock_fundamentals, get_stock_news],
)