import requests
from bs4 import BeautifulSoup
import json
import time
import logging
import random





headers = {"Accept": "*/*", "Accept-Language": "en-US,en;q=0.9", "X-Requested-With": "XMLHttpRequest", "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Safari/604.18 FABUILD/7.3.0 FABUILD-iOS/7.3.0 APP/7.3.0", "Referer": "https://www.pacsun.com/mens/graphic-tees/?country=SA&FABUILD=iosmobileapp&start=24", "Accept-Encoding": "gzip, deflate"}

print(headers)

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
        '%(asctime)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

s = requests.Session()


url = "https://www.pacsun.com/on/demandware.store/Sites-pacsun-Site/default/Search-ShowAjax?cgid=mens-graphic-tees&start=1&sz=1&country=SA"

how_many = BeautifulSoup(s.get(url , headers=headers).content , 'lxml').find('p' , {'class':'item-search-p'})
loop =  int(how_many.text.split()[0].strip('('))
print(f'Total t-shrits found {loop}')

def dol_to_sar(amount):
	return int(amount.split()[0].split('.')[0].strip('$')) * 3.75

u = 0
result = []
while u <= loop:
    u+= 100
    try:
        response = s.get(f'https://www.pacsun.com/on/demandware.store/Sites-pacsun-Site/'
                         'default/Search-ShowAjax?cgid=mens-graphic-tees'
                         f'&start={u}&sz=100&country=SA' , headers=headers)

        logger.info(f' Visiting {response.url} with status code {response.status_code} ')
        print('Sleeping just to bypass cloudFlare <--')
        time.sleep(4)
        soup = BeautifulSoup(response.content , 'html.parser')


        product_len = len(soup.findAll('span' , class_='value bfx-price bfx-sale-price'))

        for i in range(product_len):
            product_name = soup.findAll('a' , class_='link')[i].text.strip()
            product_brand = soup.findAll('div' , class_='text-product-brand flex-row align-items-center')[i].text.strip()
            product_image = soup.findAll('img' , {'class':'w-100'})[i]['src'].split('?')[0]
            price = dol_to_sar(soup.findAll('span' , class_='value bfx-price bfx-sale-price')[i].text.strip())
            link =  "https://www.pacsun.com" + soup.findAll('div' , class_="product-tile")[i].find('a').get('href')
            result.append({'name':product_name , 'brand':product_brand , 'price':price , 'img':product_image , 'link':link} )
    except Exception as e:
        logger.error(e)
        pass
    
    

with open('product.json'  , 'w') as f:
    json.dump(result, f)



