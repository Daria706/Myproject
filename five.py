import requests
from bs4 import BeautifulSoup
import csv
from os.path import exists

CSV = 'cof.csv'
HOST = 'https://hozcity.ru/'
URL = 'https://hozcity.ru/catalog/termopoty/?digiSearch=true&term=%D0%BA%D0%BE%D1%84%D0%B5%D0%B2%D0%B0%D1%80%D0%BA%D0%B0&params=%7Cfilter%3Dcategories%3A3032%7Csort%3DDEFAULT'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
}

def get_html(url,params=''):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='digi-product')
    cof =[]

    for item in items:
        cof.append(
            {
                'title': item.find('a', class_='digi-product__label').get_text(strip=True),
                'link_product': item.find('a').get('href'),
                'prise': (item.find('div', class_='digi-product__price').get_text()).replace("\n","")
            }
        )
    return cof

def save_doc(items, path):
    if exists(path):
        file = open(path, 'a', newline='')
        writer = csv.writer(file, delimiter=';')
    else:
        file = open(path, 'w', newline='')
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Название товара', 'Ссылка на товар', 'Цена'])

    for item in items:
        writer.writerow([item['title'], item['link_product'], item['prise']])




def parser3():
    html = get_html(URL)
    if html.status_code == 200:
        print(f'Парсим')
        cof = get_content(html.text)
        save_doc(cof,CSV)
    else:
        print('Error')


parser3()