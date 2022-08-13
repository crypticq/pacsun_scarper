import requests
from bs4 import BeautifulSoup
import json
import time
import logging


headers = {

    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:103.0) Gecko/20100101 Firefox/103.0",
}

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
        '%(asctime)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

s = requests.Session()
s.headers.update({'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:103.0) Gecko/20100101 Firefox/103.0'})

url = "https://www.pacsun.com/on/demandware.store/Sites-pacsun-Site/default/Search-ShowAjax?cgid=mens-graphic-tees&start=1&sz=1&country=SA"

how_many = BeautifulSoup(s.get(url).content , 'lxml').find('p' , {'class':'item-search-p'})
loop =  int(how_many.text.split()[0].strip('('))
print(f'Total products found {loop}')
time.sleep(10)
u = 0
result = []
while u <= loop:
    u+= 20
    try:
        response = s.get(f'https://www.pacsun.com/on/demandware.store/Sites-pacsun-Site/default/Search-ShowAjax?cgid=mens-graphic-tees&start={u}&sz=20&country=SA', headers=headers)

        logger.info(f' Visiting {response.url} with status code {response.status_code} ')
        print('Sleeping just to bypass cloudFlare <--')
        time.sleep(15)
        soup = BeautifulSoup(response.content , 'html.parser')


        product_len = len(soup.findAll('span' , class_='value bfx-price bfx-sale-price'))

        for i in range(product_len):
            product_name = soup.findAll('a' , class_='link')[i].text.strip()
            product_brand = soup.findAll('div' , class_='text-product-brand flex-row align-items-center')[i].text.strip()
            product_image = soup.findAll('img' , {'class':'w-100'})[i]['src'].split('?')[0]
            price = (soup.findAll('span' , class_='value bfx-price bfx-sale-price')[i].text.strip())
            result.append({'name':product_name , 'brand':product_brand , 'price':price , 'img':product_image})
    except Exception as e:
        logger.info(e)
        pass
    
    

with open('product.json'  , 'w') as f:
    json.dump(result, f)



