import datetime
import yfinance as yf
import time
import matplotlib.pyplot as plt
import io
import base64

def get_stock_price(symbol):
    today = datetime.date.today()
    stock = yf.Ticker(symbol)
    data = stock.history(end=today)
    currency = stock.history_metadata['currency']
    price = data.tail(2).to_json()
    return {"previous_close_price":price,"currency":currency}
    
def get_historical_data(symbol, ndays):
    start_data_delta = datetime.timedelta(days = ndays)
    end_data = datetime.date.today() 
    start_data = end_data - start_data_delta
    stock = yf.Ticker(symbol)
    data = stock.history(start=start_data,end=end_data)[['Open','High','Low','Close']]
    data_json = data.reset_index().to_json(orient="records", date_format="iso")
    currency = stock.history_metadata.get('currency', 'USD')
    
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
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plot_markdown = f"![{symbol} Chart](data:image/png;base64,{img_base64})"
    
    return {"data_json": data_json, "plot_markdown": plot_markdown}
    
def compare_stocks(symbols):
    data = yf.download(
                tickers = symbols,
                period = "1mo",
                interval = "1d",
                group_by = 'ticker',
                threads = True
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
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plot_markdown = f"![Comparison Chart](data:image/png;base64,{img_base64})"
    
    data_json=[]
    for i in symbols:
        jsonified = { "company" : i ,"data":data[i].reset_index().to_json(orient="records", date_format="iso")}    
        data_json.append(jsonified)

    return {"data_json": data_json, "plot_markdown": plot_markdown}


def get_stock_fundamentals(symbol):  
    data = yf.Ticker(symbol)
    keys = ['trailingPE','marketCap','epsTrailingTwelveMonths','epsForward','epsCurrentYear','priceEpsCurrentYear']
    data_required = {}
    for key, value in data.info.items():
        if key in keys: 
            data_required[key]=value
            
    return data_required


def get_stock_news(symbol):
    return yf.Search(symbol,include_nav_links=True).news