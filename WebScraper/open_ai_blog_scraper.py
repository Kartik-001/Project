import requests
from bs4 import BeautifulSoup

# Send a GET request to the website
url = "https://openai.com/blog"
response = requests.get(url)

# Create a BeautifulSoup object to parse the HTML content
soup = BeautifulSoup(response.text, "html.parser")

# Find all the article titles and URLs
articles = soup.find_all("h4", class_="content-item-title")

# Extract the data and print it
for article in articles:
    title = article.text.strip()
    url = article.a["href"]
    print("Title:", title)
    print("URL:", url)
    print()
