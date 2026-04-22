import datetime
import io
import base64
import matplotlib.pyplot as plt
import yfinance as yf
from google.genai import types
from google.adk.tools import ToolContext  

def get_stock_price(symbol: str) -> dict:
    today = datetime.date.today()
    stock = yf.Ticker(symbol)
    data = stock.history(end=today)

    if data.empty:
        return {"error": f"No data found for symbol '{symbol}'. For Indian stocks use suffix: TCS.NS, INFY.NS, RELIANCE.NS"}

    currency = stock.history_metadata.get('currency', 'USD')
    price = data.tail(2).to_json()
    return {"previous_close_price": price, "currency": currency}
    

async def get_historical_data(symbol: str, ndays: int, tool_context: ToolContext) -> dict:
    start_delta = datetime.timedelta(days=ndays)
    end_date = datetime.date.today()
    start_date = end_date - start_delta

    stock = yf.Ticker(symbol)
    data = stock.history(start=start_date, end=end_date)[['Open', 'High', 'Low', 'Close']]
    currency = stock.history_metadata.get('currency', 'USD')
    data_json = data.reset_index().to_json(orient="records", date_format="iso")

    
    data.plot(figsize=(10, 6))
    plt.title(f"{symbol} Stock Price (Last {ndays} days)")
    plt.xlabel("Date")
    plt.ylabel(f"Price ({currency})")
    plt.grid(True)
    plt.legend()

    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()
    buf.seek(0)

    image_artifact = types.Part(
        inline_data=types.Blob(mime_type="image/png", data=buf.read())
    )
    filename = f"{symbol}_chart_{ndays}d.png"
    await tool_context.save_artifact(filename, image_artifact)

    return {
        "data_json": data_json,
        "chart_artifact": filename,   # tell the LLM the filename
        "status": f"Chart saved as artifact: {filename}"
    }
    
async def compare_stocks(symbols: list[str], ndays: int, tool_context: ToolContext) -> dict:
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=ndays)

    data = yf.download(
        tickers=symbols,
        start=start_date,
        end=end_date,
        interval="1d",
        group_by='ticker',
        threads=True
    )

    data.plot(figsize=(10, 6))
    plt.title(f"{symbols} Stock Price (Last 30 days)")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.grid(True)
    plt.legend()

    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()
    buf.seek(0)

    
    image_artifact = types.Part(
        inline_data=types.Blob(mime_type="image/png", data=buf.read())
    )
    filename = f"compare_{'_'.join(symbols)}.png"
    await tool_context.save_artifact(filename, image_artifact)

    data_json = [
        {"company": i, "data": data[i].reset_index().to_json(orient="records", date_format="iso")}
        for i in symbols
    ]
    return {
        "data_json": data_json,
        "chart_artifact": filename,
        "status": f"Chart saved as artifact: {filename}"
    }

def get_stock_fundamentals(symbol: str) -> dict: 
    data = yf.Ticker(symbol)
    keys = ['trailingPE','marketCap','epsTrailingTwelveMonths','epsForward','epsCurrentYear','priceEpsCurrentYear']
    data_required = {}
    for key, value in data.info.items():
        if key in keys: 
            data_required[key]=value
            
    return data_required


def get_stock_news(symbol: str) -> list:
    return yf.Search(symbol,include_nav_links=True).news
