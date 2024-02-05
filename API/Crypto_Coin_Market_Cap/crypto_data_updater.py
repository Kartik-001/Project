# Import necessary libraries
import requests  # For making HTTP requests
import json      # For handling JSON data
import pandas as pd  # For working with data in tabular format
import time     # For managing time and adding delays
import os       # For interacting with the operating system


# Define a function to fetch cryptocurrency data from an API and save it to a CSV file
def fetch_and_save_crypto_data():
    # Define the API URL and parameters
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
        'start': '1',
        'limit': '5000',
        'convert': 'USD'
    }
    
    # Define API headers with an API key
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': '5216a4af-6743-4923-9f31-7d1a8ffcc395',
    }

    try:
        # Make an HTTP GET request to the API
        response = requests.get(url, params=parameters, headers=headers)
        data = response.json()  # Parse the JSON response

        # Normalize the data into a DataFrame and add a timestamp column
        df = pd.json_normalize(data['data'])
        df['timestamp'] = pd.to_datetime('now')

        # Define the path for the CSV file
        filename = r'C:\Users\ASUS\Doing\Project\API\Crypto_Coin_Market_Cap\Crypto_Data1.csv'

        # Check if the CSV file exists
        if not os.path.isfile(filename):
            # If the file doesn't exist, create it with headers
            df.to_csv(filename, header='column_names', index=False)
        else:
            # If the file exists, read it into a DataFrame
            existing_df = pd.read_csv(filename)
            
            # Create a temporary DataFrame by concatenating existing data and new data
            temp_df = pd.concat([df, existing_df], axis=0, ignore_index=True)
            
            # Save the combined DataFrame to the CSV file with headers
            temp_df.to_csv(filename, header=True, index=False)
        
        # Print a message indicating that the data has been updated and saved
        print("Data updated and saved to CSV at", time.ctime())
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout, requests.exceptions.TooManyRedirects) as e:
        # Handle exceptions related to the HTTP request
        print(e)

# Run the data fetching and saving process in a loop with a 5-minute delay
while True:
    fetch_and_save_crypto_data()
    time.sleep(300)
