import requests, sys
from bs4 import BeautifulSoup

url = "https://www.newegg.com/black-dowinx-ls-668901-chair-with-accessory/p/2T4-029X-00024?Item=9SIAKUYC438823"

r = requests.get(url)
doc = BeautifulSoup(r.text, 'html.parser')

prices = doc.find_all(text="$")
parent = prices[0].parent
strong = parent.find("strong")
print(strong.string)