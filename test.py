import requests

proxies = {
    'http': 'socks5://127.0.0.1:9050',
    'https': 'socks5://127.0.0.1:9050'
}
#
url = 'http://icanhazip.com/'
#
# for i in range(5):
#     print(requests.get(url, proxies=proxies).text)
from stem import Signal
from stem.control import Controller

for i in range(5):
    with Controller.from_port(port=9051) as c:
        c.authenticate()
        c.signal(Signal.NEWNYM)
        print(requests.get(url, proxies=proxies).text)