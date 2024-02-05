# Get Different IP with Proxy

import requests

def get_ip(proxy_url):
    proxies = {
        'http': proxy_url,
        'https': proxy_url
    }

    try:
        r = requests.get('https://api64.ipify.org?format=json', proxies=proxies)
        r.raise_for_status()
        ip = r.json()['ip']
        return ip
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

def main():
    # Replace 'your_proxy_url' with your actual proxy URL (e.g., 'http://your_proxy_server:port')
    proxy_url = 'http://your_proxy_url'
    ip = get_ip(proxy_url)
    
    if ip:
        print(f"Your IP address: {ip}")

if __name__ == "__main__":
    main()
