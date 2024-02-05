import requests
from bs4 import BeautifulSoup

url = "https://coinmarketcap.com/"

r = requests.get(url)
doc = BeautifulSoup(r.text, "html.parser")

tbody = doc.tbody

# return a list of all tags in tbody
trows = tbody.contents

# to see the first sibling (should see bitcoin somewhere)
print(trows[0])

# print trs[0].next_sibling to see trs[1]
# print trs[0].next_sibling to see trs[1:]
# print trs[1].previous_sibling to see trs[0]

# print trs[0].parent to see a tag above it
# print trs[0].contents or trs[0].descendants or trs[0].children to see tags inside it

prices = {}

for trow in trows[:10]:
    name, price = trow.contents[2:4]
    name = name.p.text
    price = price.a.text
    prices[name] = price

print(prices)