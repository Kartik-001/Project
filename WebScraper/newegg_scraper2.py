import re
import requests
import sys
from bs4 import BeautifulSoup
import time

def scrape_newegg(product):
    try:
        max_retries = 5  # Maximum number of retries
        retries = 0

        while retries < max_retries:
            # Construct the URL for the Newegg search page with the product keyword
            url = f'https://www.newegg.com/p/pl?d={product}&n=4841'

            # Define a user-agent header to mimic a real browser
            headers = {'User-Agent': 'Mozilla/5.0'}

            try:
                # Send a GET request to the URL with the user-agent header
                page = requests.get(url, headers=headers)
                page.raise_for_status()  # Raise an exception for unsuccessful requests
            except requests.exceptions.RequestException as e:
                print(f"Error: {e}")
                # Delay before retrying (to avoid overwhelming the server)
                time.sleep(5)  # You can adjust the delay as needed
                retries += 1
                continue

            doc = BeautifulSoup(page.text, 'html.parser')

            # Find the page navigation information, which contains the total number of pages
            page_info = doc.find(class_="list-tool-pagination-text")
            if page_info is not None:
                try:
                    pages = int(re.search(r'(\d+)$', page_info.text).group(1))
                except Exception as e:
                    print(f"Error extracting 'pages': {e}")
                    pages = 0  # Set a default value or handle the error accordingly
            else:
                print("Page navigation information not found.")
                pages = 0  # Set a default value since the information is not available

            # Initialize a list to store found items
            items_found = []

            # Loop through each page of search results
            for page in range(1, pages + 1):
                # Construct the URL for the current search page
                url = f'https://www.newegg.com/p/pl?d={product}&n=4841&page={page}'
                try:
                    # Send a GET request to the URL with the user-agent header
                    page = requests.get(url, headers=headers)
                    page.raise_for_status()  # Raise an exception for unsuccessful requests
                except requests.exceptions.RequestException as e:
                    print(f"Error: {e}")
                    # Delay before retrying (to avoid overwhelming the server)
                    time.sleep(5)  # You can adjust the delay as needed
                    retries += 1
                    continue

                doc = BeautifulSoup(page.text, 'html.parser')

                # Find the div containing the item listings
                div = doc.find(class_="item-cells-wrap border-cells items-grid-view four-cells expulsion-one-cell")

                # Find all items on the page that match the product keyword using regular expressions
                items = div.find_all(text=re.compile(product))

                # Extract items and their details using list comprehensions
                items_data = [
                    {
                        'item': item.parent['title'],
                        'link': item.parent['href'],
                        'price': int(item.find_parent(class_='item-container').find(class_='price-current').strong.string.replace(',', '')),
                    }
                    for item in items if item.parent.name == 'a'
                ]

                # Extend the items_found list with the items_data list
                items_found.extend(items_data)

            # Sort items_found by price in ascending order
            sorted_items_found = sorted(items_found, key=lambda x: x['price'])

            # Print the sorted items_found list with item names, prices, and links
            for item_data in sorted_items_found:
                print(f"Item: {item_data['item']}, Price: {item_data['price']}, Link: {item_data['link']}")

            break  # Break out of the retry loop if successful

        if retries == max_retries:
            print("Max retries reached. Unable to connect to the server.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python your_script.py <product_keyword>")
        sys.exit(1)

    product_keyword = sys.argv[1]
    scrape_newegg(product_keyword)
