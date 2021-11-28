import requests
from bs4 import BeautifulSoup
import csv
from os.path import exists

CSV = 'cof.csv'
HOST = 'https://www.ohdm.ru/'
URL = 'https://www.ohdm.ru/tovary/k-11482148-kofevarka'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
}

def get_html(url,params=''):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('li', class_='copmany-product-gallery-item')
    cof =[]

    for item in items:
        cof.append(
            {
                'title': item.find('a', class_='cpgi-title').get_text(strip=True),
                'link_product': item.find('a', class_='cpgi-image-link').get('href'),
                'prise': (item.find('div', class_='cpgi-price').get_text()).replace("\n","")
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

    # with open(path, 'w', newline='') as file:
    #     writer = csv.writer(file, delimiter=';')
    #     writer.writerow(['Название товара', 'Ссылка на товар', 'Цена'])
    #     for item in items:
    #         writer.writerow([item['title'], item['link_product'], item['prise']])


def parser1():
    PAGENATION = input('Укажите количество страниц для парсинга: ')
    PAGENATION = int(PAGENATION.strip())
    html = get_html(URL)
    if html.status_code == 200:
        cof = []
        for page in range(1, PAGENATION+1):
            print(f'Парсим страницу:{page}')
            html = get_html(URL, params={'page': page})
            cof.extend(get_content(html.text))
        save_doc(cof,CSV)
    else:
        print('Error')

#parser1()