import requests

url = "https://timesofindia.indiatimes.com/business/startups"

def fetch_and_save(url, path):
    r = requests.get(url)
    with open(path, "w") as f:
        f.write(r.text)

fetch_and_save(url, "scrap.html")
