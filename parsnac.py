from bs4 import BeautifulSoup
import requests
import csv
from datetime import datetime


def save():
    with open('nac_index.csv', 'a') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow ([f"{comp['text']}", f"{comp['date']}",f"{comp['link']}" , datetime.now()])
        

def parse():
    URL = 'https://www.nbkr.kg/index.jsp?lang=RUS'
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0'
    }
    
    response = requests.get(URL, headers = HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.findAll('div', class_ = 'col-md-10 col-xs-12 main-news-txt-cont')
    comps = []

    for item in items:
        comps.append({
            'text': item.find('div', class_ = 'col-md-12 main-news-text').get_text(strip = True),
            'date': item.find('div', class_ = 'visible-xs-block visible-sm-block main-news-date-mob').get_text(strip = True),
            'link': item.find('div', class_ = 'col-md-12 main-news-more').find('a').find('a').get('href')
        })

        global comp
        for comp in comps:
            print(f"{comp['text']} -> Date: {comp['date']} -> Link^ {comp['link']}")
        save()

parse()