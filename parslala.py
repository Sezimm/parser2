from bs4 import BeautifulSoup
import requests
import csv
from datetime import datetime

CSV = 'Kivano_nout.csv'
HOST = 'https://www.kivano.kg/'
URL = 'https://www.kivano.kg/noutbuki'
HEADERS = {
   'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0'
}

def get_html(url, params=''):
    r = requests.get(url, headers = HEADERS, params=params)
    return r
        

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.findAll('div', class_ = 'pull-right rel')
    new_list = []

    for item in items:
        new_list.append({
            'title': item.find('div', class_ = 'product_text pull-left').find('div', class_ = 'listbox_title oh').find('a').get_text(strip = True),
            'price': item.find('div', class_ = 'motive_box pull-right').find('div', class_ = 'listbox_price text-center').get_text(strip = True),
            'link': item.find('div', class_ = 'product_text pull-left').find('div', class_ = 'listbox_title oh').find('a').get('href')
        })
    return new_list


def save(items, path):
    with open(path, 'a') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow (['Название','Цена','Ссылка'])
        for item in items:
            writer.writerow([item['title'], item['price'], item['link']])


def parser():
    PAGENATION = input("Введите количество страниц: ")
    PAGENATION = int(PAGENATION.strip())
    html = get_html(URL)
    if html.status_code == 200:
        news_list = []
        for page in range(1, PAGENATION):
            print(f'Страница №{page} готова')
            html = get_html(URL, params={'page' : page})
            news_list.extend(get_content(html.text))
        save(news_list, CSV)
        print('Парсинг готов')
        # print(news_list)
    else:
        print('Error')


parser()