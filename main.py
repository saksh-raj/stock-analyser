import pandas as PD
from bs4 import BeautifulSoup as BS
import requests
from requests.exceptions import HTTPError
from function import CAGR as cagr

ticker = input("Enter a ticker: ")

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

def get_peer_names(ticker):
    try:
        link = f"https://www.screener.in/company/{ticker}"
        response = requests.get(link)
        response.raise_for_status()
        soup = BS(response.text, 'html.parser')
        randomNumber = soup.find(id = "peers").find('p').find_all('a')[-1]['href'].strip()
        peerURL = f"https://www.screener.in/{randomNumber}"
        
    except HTTPError:
        if response.status_code == 404 :
            print("Name a valid ticker! 404")
        else:
            print(f"Some error occured! {response.status_code}")
    quit()



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

# # Most Recent FY -> Apr '24 - Mar'25
# # Most Recent Quarter -> Jun '25

print(get_peer_names(ticker))

# # print("All values are in Rs. Crores and these are standalone figures.")
# tables = get_stock_data(ticker)
# YearlyPL = get_yearly_profit_loss_account(tables)

# #Peers
# soup = BS(response.text, 'html.parser')
# peerSec = soup.find(id = "peers")
# peerSecP = peerSec.find('p')
# peerSecPATags = peerSecP.find_all('a')
# relevantATag = peerSecPATags[-1]["href"]
# industryHREF = relevantATag.strip()
# peerURL = "https://www.screener.in/"+industryHREF
# print(peerURL)

# #Sales Section
# latest_Sales = get_sales_yearly(ticker)
# y3_sales = get_sales_yearly(ticker, -3)
# y5_sales = get_sales_yearly(ticker, -5)
# y10_sales = get_sales_yearly(ticker, -10)

# sales_y3_cagr = (float(cagr(int(y3_sales), int(latest_Sales), 3))*100)
# sales_y5_cagr = (float(cagr(int(y5_sales), int(latest_Sales), 5))*100)
# sales_y10_cagr = (float(cagr(int(y10_sales), int(latest_Sales), 10))*100)

# sales_y3_cagr_string = f"{(float(cagr(int(y3_sales), int(latest_Sales), 3))*100):.2f}%"
# sales_y5_cagr_string = f"{(float(cagr(int(y5_sales), int(latest_Sales), 5))*100):.2f}%"
# sales_y10_cagr_string = f"{(float(cagr(int(y10_sales), int(latest_Sales), 10))*100):.2f}%"

