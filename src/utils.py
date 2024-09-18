import yfinance as yf
import pandas as pd


def download_data_ticker(stock_symbol):
    ticker = yf.Ticker(stock_symbol)
    list_fields = ['symbol', 'country', 'industry', 'sector', 'fullTimeEmployees',
                    'ebitda', 'totalDebt', 'totalRevenue', 'debtToEquity',
                    'grossMargins', 'ebitdaMargins']
    ticker = pd.DataFrame.from_dict({k:v for k,v in ticker.info.items() if k in list_fields},
                                    orient='index').T
    ticker.columns = ticker.columns.str.lower()
    return ticker

def download_data_stocks(stock_symbol, start_date, end_date):
    stock_data = yf.download(stock_symbol, start=start_date, end=end_date)
    stock_data['symbol'] = stock_symbol
    stock_data = stock_data.reset_index()
    stock_data.columns = stock_data.columns.str.lower()
    stock_data = stock_data.drop(['adj close'], axis=1)
    return stock_data