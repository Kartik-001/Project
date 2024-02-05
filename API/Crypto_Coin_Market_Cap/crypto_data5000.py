# Import necessary libraries
import requests  # For making HTTP requests
import json      # For handling JSON data
import pandas as pd  # For working with data in tabular format
import time     # For managing time and adding delays

def fetch_and_save_crypto_data():
    # Define the API URL, parameters, and headers
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
        'start': '1',
        'limit': '5000',
        'convert': 'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': '5216a4af-6743-4923-9f31-7d1a8ffcc395',
    }

    try:
        # Make an HTTP GET request to the specified API
        response = requests.get(url, params=parameters, headers=headers)
        
        # Parse the JSON response into a Python dictionary
        data = response.json()
        
        # Convert the dictionary to a nicely formatted JSON string and print it
        # data = json.dumps(response.json(), indent=2)
        # print(data)
        
        # Normalize the data and save it to a CSV file
        df = pd.json_normalize(data['data'])
        df['timestamp'] = pd.to_datetime('now')
        df.to_csv('Crypto_Data5000.csv', index=False)
        
        # Print a message indicating that the data has been updated and saved
        print("Data updated and saved to CSV at", time.ctime())
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout, requests.exceptions.TooManyRedirects) as e:
        # Handle exceptions related to the HTTP request
        print(e)

while True:
    fetch_and_save_crypto_data()
    # Sleep for 300 seconds (5 minutes) before making the next request
    time.sleep(300)
