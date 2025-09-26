import pandas as PD
from bs4 import BeautifulSoup as BS
import requests
from requests.exceptions import HTTPError
from function import CAGR as cagr
import yfinance as yf

ticker = input("Enter a ticker: ")

try:
    url = f"https://www.screener.in/company/{ticker}/"
    response = requests.get(url)
    response.raise_for_status()
except HTTPError:
    if response.status_code == 404 :
        print("Name a valid ticker! 404")
    else:
        print(f"Some error occured! {response.status_code}")
    quit()

def get_stock_data(ticker):
    stock_data = PD.read_html(f"https://www.screener.in/company/{ticker}/")
    return stock_data
    
def get_yearly_profit_loss_account(ticker):
    stock_data = get_stock_data(ticker)
    yearly_profit_loss_account = PD.DataFrame(stock_data[1])
    return yearly_profit_loss_account

# 0 for latest
def get_sales_yearly(ticker, year = 0):
    yearly_profit_loss_account = get_yearly_profit_loss_account(ticker)
    if year < 0 :
        print("Year cannot be less than 0")
        quit()
    Sales = yearly_profit_loss_account.loc[0]
    return Sales.iloc[year-2]

def get_PE(ticker):
    ticker+=".NS"
    Ticker = yf.Ticker(ticker).info
    return Ticker["trailingPE"]

def get_PB(ticker):
    ticker+=".NS"
    Ticker = yf.Ticker(ticker).info
    return Ticker["priceToBook"]

def get_ROE(ticker):
    ticker+=".NS"
    Ticker = yf.Ticker(ticker).info
    return Ticker["returnOnEquity"]

def get_MARCAP(ticker):
    ticker+=".NS"
    Ticker = yf.Ticker(ticker).info
    return float(Ticker["marketCap"]/10000000)

def get_CMP(ticker):
    ticker+=".NS"
    Ticker = yf.Ticker(ticker)
    price = Ticker.history(period="1d")['Close'].iloc[0]
    return float(price)

def get_sales_cagr(ticker, years = 3):
    if years < 3 :
        print("Year cannot be less than 3")
        quit()
    if years > 10 :
        print("Year cannot be more than 10")
        quit()
    year = 0
    yearly_profit_loss_account = get_yearly_profit_loss_account(ticker)
    Sales = yearly_profit_loss_account.loc[0]
    current = Sales.iloc[year-2]
    past = Sales.iloc[year-2-years]
    return cagr(past, current, years)

def get_peer_data(ticker):
    PE = []
    ROE = []
    MARCAP = []
    CMP = []
    peers = get_peer_names(ticker)
    for peer in peers:
        PE.append(get_PE(peer))
        ROE.append(get_ROE(peer))
        MARCAP.append(get_MARCAP(peer))
        CMP.append(get_CMP(peer))
    return {
        "P/E": PE,
        "ROE": ROE,
        "Market Cap": MARCAP,
        "CMP": CMP
    }
    

def get_peer_names(ticker):
    link = f"https://www.screener.in/company/{ticker}"
    response = requests.get(link)
    response.raise_for_status()
    soup = BS(response.text, 'html.parser')
    randomNumber = soup.find(id = "peers").find('p').find_all('a')[-1]['href'].strip()
    link = f"https://www.screener.in{randomNumber}"
    response = requests.get(link)
    response.raise_for_status()
    soup = BS(response.text, 'html.parser')
    del randomNumber
    table = soup.find('table')
    companiesTD = table.find_all('td')
    list = []
    for company in companiesTD:
        anchor_tag = company.find('a')
        if anchor_tag and anchor_tag.has_attr("href"):
            anchor = anchor_tag["href"].strip()
            anchor = anchor[:-13]
            list.append(anchor[9:-1])
    return list

# # Most Recent FY -> Apr '24 - Mar'25
# # Most Recent Quarter -> Jun '25