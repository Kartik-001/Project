import re, requests, sys
from bs4 import BeautifulSoup

# Get the product keyword from the command-line arguments
product = sys.argv[1]

# Construct the URL for the Newegg search page with the product keyword
url = f'https://www.newegg.com/p/pl?d={product}&n=4841'
headers = {'User-Agent': 'Mozilla/5.0'}

# Send a GET request to the URL and parse the HTML content
page = requests.get(url, headers=headers)
doc = BeautifulSoup(page.text, 'html.parser')

# Uncomment the following line to print the entire HTML content of the page
# print(doc.text)
# Use this to see whether you can actually scrape the web or not

# Find the page navigation information, which contains the total number of pages
page_info = doc.find(class_="list-tool-pagination-text")
pages = int(str(page_info).split('/')[-2].split('>')[-1][:-1])

# Initialize a dictionary to store found items
items_found = {}

# Loop through each page of search results
for page in range(1, pages + 1):
    # Construct the URL for the current search page
    url = f'https://www.newegg.com/p/pl?d={product}&n=4841&page={page}'
    page = requests.get(url, headers=headers)
    doc = BeautifulSoup(page.text, 'html.parser')

    # Find the div containing the item listings
    div = doc.find(class_="item-cells-wrap border-cells items-grid-view four-cells expulsion-one-cell")
    
    # Find all items on the page that match the product keyword using regular expressions
    items = div.find_all(text=re.compile(product))
    
    # Loop through the found items
    for item in items:
        parent = item.parent
        # Check if the parent element is an 'a' (link) element
        if parent.name != 'a':
            continue
        # Get the link from the 'href' attribute of the 'a' element
        link = parent['href']
        # Find the parent container of the item and extract the price
        parent2 = item.find_parent(class_='item-container')
        try:
            price = parent2.find(class_='price-current').strong.string

            # Store the item and its details in the items_found dictionary
            items_found[item] = {'price': int(price.replace(',', '')), 'link': link}
        except:
            pass

# Use .find_parent() to find a particular parent

# Sort items_found by price in ascending order
sorted_items_found = dict(sorted(items_found.items(), key=lambda x: x[1]['price']))

# Print the sorted items_found dictionary with item names, prices, and links
for item, data in sorted_items_found.items():
    print(f"Item: {item}, Price: {data['price']}, Link: {data['link']}", sep='\n')
