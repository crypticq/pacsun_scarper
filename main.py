import sys
import time
import logging
import json
import requests
from pprint import pprint
from bs4 import BeautifulSoup

headers = {
    "Accept": "*/*", "Accept-Language": "en-US,en;q=0.9", "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0"
                  " (Linux; Android 12)"
                  " AppleWebKit/537.36 (KHTML, like Gecko)"
                  " Chrome/104.0.5112.69 Mobile Safari/537.36",
    "Referer": "https://www.pacsun.com/mens"
               "/graphic-tees/?country=SA&FABUILD=iosmobileapp&start=100",
    "Accept-Encoding": "gzip, deflate"}

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

s = requests.Session()



def dol_to_sar(amount: str) -> int:
    """
    convert $ to SAR
    """
    return int(amount.split('.')[0].split('$')[1]) * 3.75


result = []


def pacsun_scraper(product_type:str="mens-graphic-tees"):
    """
    Scrape all product in the link and append each product to a list
    and convert it to json .

    """
    page_counter = 0

    while page_counter <= loop:
        page_counter += 100
        try:
            response = s.get(f'https://www.pacsun.com/on/demandware.store/Sites-pacsun-Site/'
                             f'default/Search-ShowAjax?cgid={product_type}'
                             f'&start={page_counter}&sz=100&country=SA', headers=headers)

            logger.info('Visiting %s with status code %d ' , response.url , response.status_code)
            print('Sleeping just to bypass cloudFlare <--')
            time.sleep(3)
            soup = BeautifulSoup(response.content, 'html.parser')

            product_len = len(soup.findAll('div', class_='product'))

            for i in range(product_len):
                product_name = soup.findAll('a', class_='link')[i].text.strip()
                product_brand = soup.findAll('div', class_='text-product-brand flex-row align-items-center')[i].text.strip()
                product_image = soup.findAll('img', {'class': 'w-100'})[i]['src'].split('?')[0]
                price = dol_to_sar(soup.findAll('span', {'class':'value bfx-price bfx-list-price'})[i].text.strip())
                link = "https://www.pacsun.com" + soup.findAll('div', class_="product-tile")[i].find('a').get('href')
                result.append(
                    {'name': product_name,
                     'brand': product_brand,
                     'price': price,
                     'link': link,
                     'img': product_image,
                     }

                )


        except Exception as e:
            logger.error(e)


if __name__ == '__main__':

    PACSUN_URL = "https://www.pacsun.com/on/demandware.store/" \
                 "Sites-pacsun-Site/default/Search-ShowAjax?cgid=mens-graphic-tees" \
                 "&start=1&sz=1&country=SA "

    if s.get(PACSUN_URL, headers=headers).status_code == 403:
        print('YOU ARE blocked try to tweek with headers .')

        sys.exit('chenge your user-agent .')

    how_many = BeautifulSoup(s.get(PACSUN_URL, headers=headers)
                             .content, 'lxml').find('p', {'class': 'item-search-p'})
    loop = int(how_many.text.split()[0].strip('('))

    pacsun_scraper()

    with open('product.json', 'w') as f:
        json.dump(result, f)
    pprint(json.dumps(result))
    print('ALL product saved in product.json file ')
