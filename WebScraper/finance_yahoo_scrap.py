import requests
from bs4 import BeautifulSoup

# Define the stock symbol you want to monitor
stock_symbol = "AAPL"

# Create a function to scrape and display stock data
def get_stock_data(stock_symbol):
    url = f"https://finance.yahoo.com/lookup/{stock_symbol}"
    response = requests.get(url)
    print(response.text)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        price_element = soup.find("div", {"data-test": "OPEN-value"})
        price = price_element.text if price_element else "N/A"
        
        print(f"Stock Symbol: {stock_symbol}")
        print(f"Current Price: {price}")
    else:
        print("Failed to retrieve data from Yahoo Finance.")

# Call the function to get and display stock data
get_stock_data(stock_symbol)
