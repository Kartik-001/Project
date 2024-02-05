# Import necessary libraries
import requests  # For making HTTP requests
import json      # For handling JSON data

# Define API URL, parameters, and headers
url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
  'start': '1',
  'limit': '10',
  'convert': 'USD'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '5216a4af-6743-4923-9f31-7d1a8ffcc395',
}

try:
  # Make an HTTP GET request to the API
  response = requests.get(url, params=parameters, headers=headers)
  data = response.json()
  # Uncomment the following lines to see the data in JSON format
  # data = json.dumps(response.json(), indent=2)
  # print(data)
except (requests.exceptions.ConnectionError, requests.exceptions.Timeout, requests.exceptions.TooManyRedirects) as e:
  print(e)

# Import additional libraries
import pandas as pd  # For working with data in tabular format
import time, os     # For managing time, adding delays, and interacting with the operating system

# Normalize the data into a DataFrame and add a timestamp column
df = pd.json_normalize(data['data'])
df['timestamp'] = pd.to_datetime('now')

# Define the path for the CSV file
filename = r'C:\Users\ASUS\Doing\Project\API\Crypto_Coin_Market_Cap\Crypto_Data2.csv'

# Check if the CSV file exists
if not os.path.isfile(filename):
    # If the file doesn't exist, create it with headers
    df.to_csv(filename, header='column_names', index=False)
else:
    # If the file exists, append the data to the CSV file
    df.to_csv(filename, header=False, index=False, mode='a')

# reading the csv which has the data
df2 = pd.read_csv(filename)

# Group and calculate the mean of selected columns
changes = ['quote.USD.percent_change_1h','quote.USD.percent_change_24h','quote.USD.percent_change_7d','quote.USD.percent_change_30d','quote.USD.percent_change_60d','quote.USD.percent_change_90d']
group = ['id','name','symbol','slug']
df3 = df.groupby('name', sort=False)[changes].mean()

# Stack the DataFrame
df4 = df3.stack()

# Convert to a DataFrame
df5 = df4.to_frame(name='values')

# Reset the index
df6 = df5.reset_index()

# Rename columns
df7 = df6.rename(columns={'level_1': 'percent_change'})

# Replace the specified string in the 'percent_change' column
df8 = df7.assign(percent_change=df7['percent_change'].str.replace('quote.USD.percent_change_', ''))

# Import visualization libraries
import seaborn as sns
import matplotlib.pyplot as plt

# Create a categorical point plot
sns.catplot(x='percent_change', y='values', hue='name', data=df8, kind='point', height=5, aspect=1.5)
plt.show()

# Create a line plot
plt.figure(figsize=(10, 6))
sns.lineplot(x='percent_change', y='values', hue='name', data=df8)
plt.show()

# Select specific columns from the DataFrame
df9 = df2[['name', 'quote.USD.price', 'timestamp']]

# Filter data for a specific cryptocurrency (Bitcoin)
df10 = df9.query("name == 'Bitcoin'")
print(df10)