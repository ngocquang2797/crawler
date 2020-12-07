import requests
from bs4 import BeautifulSoup
import json
import re

proxies = {
    'http': 'socks5://127.0.0.1:9050',
    'https': 'socks5://127.0.0.1:9050'
}
#
# url = 'http://icanhazip.com/'
url = 'https://coinmarketcap.com/'

from stem import Signal
from stem.control import Controller

c = Controller.from_port(port=9051)
c.authenticate()

class Crawler:
    def __init__(self):
        self.__page_url = 'https://coinmarketcap.com/'
        self.__data = []
        self.total_page = self.ttl_page()

    def ttl_page(self):
        r = requests.get(self.__page_url)
        soup = BeautifulSoup(r.text, 'html.parser')
        page_numbers = soup.find('ul', {'class': 'rc-pagination'})
        ttl = 0
        for page in page_numbers:
            if page.getText():
                ttl = int(page.getText())

        return ttl

    def getSlugs(self, url):
        cmc = requests.get(url)
        soup = BeautifulSoup(cmc.content, 'html.parser')
        data = soup.find('script', id="__NEXT_DATA__", type="application/json")
        coins = {}
        coin_data = json.loads(data.contents[0])
        listings = coin_data['props']['initialState']['cryptocurrency']['listingLatest']['data']

        slugs = []

        for i in listings:
            print(i['slug'])
            slugs.append(i['slug'])

        return slugs

    def crawl_coin_data(self, slug):
        try:
            # coin = requests.get(url='https://coinmarketcap.com/currencies/'+slug, proxies=proxies)
            coin = requests.get(url='https://coinmarketcap.com/currencies/' + slug)

            soup = BeautifulSoup(coin.text, 'html.parser')
            # print(soup)

            data = soup.find('div', {'class': 'cmc-details-panel-header__name'})
            img = data.find('img')['src']
            symbol = re.findall(r'[a-zA-Z]+', data.find('h1').find('span').getText())[0]
            name = data.find('h1').getText().strip(data.find('h1').find('span').getText())
            print(name + " Success")
            return {'name': name,
                    'symbol': symbol,
                    'slug': slug,
                    'image': img}
        except Exception as e:
            print('ERROR: {} - {}'.format(slug, e))
            c.signal(Signal.NEWNYM)
            self.crawl_coin_data(slug)
            return None

    def crawl(self):
        for i in range(self.total_page):

            page_url = self.__page_url + '/{}/'.format(i + 1)
            cmc = requests.get(page_url)
            soup = BeautifulSoup(cmc.content, 'html.parser')
            coin_slugs = self.getSlugs(page_url)

            for slug in coin_slugs:
                coin_data = self.crawl_coin_data(slug)
                if coin_data:
                    self.__data.append(coin_data)

    def get_data(self):
        print(len(self.__data))
        return self.__data

    def save_data(self):
        with open("data/coins.txt", 'w') as outfile:
            json.dump(self.__data, outfile)


def main():
    crawler = Crawler()
    crawler.crawl()
    print(crawler.get_data())
    # crawler.save_data()
    # proxi = getproxy()
    # print(proxi.proxies)


if __name__ == "__main__":
    main()