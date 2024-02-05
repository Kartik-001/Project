import requests
from bs4 import BeautifulSoup
import pandas as pd

# Define the URL of the Wikipedia page to scrape
url = 'https://en.wikipedia.org/wiki/List_of_largest_companies_by_revenue'

# Send a GET request to the URL and parse the HTML content
r = requests.get(url)
html = BeautifulSoup(r.text, 'html.parser')

# Find the table with the data
table = html.find('table', {'class': 'wikitable'})

# Extract the column titles
titles = [title.text.strip() for title in table.find_all('th')[:7]]

# Create an empty DataFrame with the extracted column titles
df = pd.DataFrame(columns=titles)

# Find all the rows in the table (excluding the header row)
rows = table.find_all('tr')[2:52]  # Adjust the range as needed

for row in rows:
    # Extract the rank from the first cell (th)
    row_rank = row.find('th').text.strip()
    
    # Extract data from the remaining cells (td)
    row_data = [data.text.strip() for data in row.find_all('td')[:6]]
    
    # Add the rank to the data list
    row_data.insert(0, row_rank)
    
    # Append the data as a new row to the DataFrame
    df.loc[len(df)] = row_data

# Save the DataFrame to a CSV file without the index column
df.to_csv('companies.csv', index=False)