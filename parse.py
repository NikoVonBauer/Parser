import requests
from bs4 import BeautifulSoup as bs
import psycopg2
from config import host, user, password, db_name

class Shops:
    URLS = ["https://neptun66.ru/catalog/boylery/bosch/", "https://www.vodoparad.ru/catalog/vanny.html"]

class Parse:
    conn = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )

    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(
        '''DELETE FROM "Products";'''
    )

    for URL in Shops.URLS:
        r_get = requests.get(URL)
        soup = bs(r_get.text, "html.parser")
        if URL == "https://neptun66.ru/catalog/boylery/bosch/":
            prices = soup.find_all('price', class_='js-price')
            names = soup.find_all('a', class_='js-prodname')
            for price, name, link in zip(prices, names, soup.find_all('a', class_ = 'js-prodname')):
                cur.execute(
                    'INSERT INTO "Products" ("Product_Title", "Product_Price", "Product_Link") VALUES ({0}, {1}, {2})'.format(repr(name.text), repr(price.text), repr(link.get('href')))
                )

        elif URL == "https://www.vodoparad.ru/catalog/vanny.html":
            prices = soup.find_all('p', class_='product-item__price-new')
            names = soup.find_all('a', class_="product-item__name")
            for price, name, link in zip(prices, names, soup.find_all('a', class_ = 'product-item__name')):
                cur.execute(
                    'INSERT INTO "Products" ("Product_Title", "Product_Price", "Product_Link") VALUES ({0}, {1}, {2})'.format(repr(name.text), repr(price.text), repr(link.get('href')))
                )

        else:
            print("ERROR")
        
    conn.close()