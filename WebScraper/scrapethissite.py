import requests
from bs4 import BeautifulSoup

url = 'https://www.scrapethissite.com/pages/forms/'

r = requests.get(url)
html = BeautifulSoup(r.text, 'html.parser')

# print(html)

doc = html.find('p', class_='lead')

lead = '\n'.join(map(str.strip, doc.text.strip().split("\n")))
# print(lead)

teams = {}

tbody = html.find('table', class_='table')
# print(tbody)

rows = tbody.find_all('tr', class_='team')
for row in rows:
    try:
        win_rate = float(row.find('td', class_='pct text-success').string.strip())
    except Exception as e:
        # print(e)
        continue
    # print(win_rate)
    name = row.find('td', class_='name').string.strip()
    # print(name)
    teams[name] = win_rate

for name, win_rate in sorted(teams.items(), key=lambda x:x[1]):
    print(f'Team {name} has a win rate of {win_rate}')