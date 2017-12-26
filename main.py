import requests
import bs4

from peewee import *

db = SqliteDatabase('./exchange.db')

class Exchange(Model):
    name = CharField()
    volume = CharField()      
    url = CharField()

    class Meta:
        database = db

db.connect()

db.drop_tables([Exchange])

db.create_tables([Exchange])

response = requests.get('https://coinmarketcap.com/exchanges/volume/24-hour/')

# print response.text

soup = bs4.BeautifulSoup(response.text,"html.parser")

html = soup.select('.volume-header a')

for item in html:

    link = "https://coinmarketcap.com" + item.attrs['href']
    subpage = requests.get(link)

    subsoup = bs4.BeautifulSoup(subpage.text,"html.parser")

    name = subsoup.select('.text-large')
    volume = subsoup.select('.text-large2')
    url = subsoup.select('.list-unstyled a')

    print name[0].text
    print volume[0].text
    print url[0].text


    exchange = Exchange(name=name[0].text,volume=volume[0].text,url=url[0].text)
    exchange.save()

db.close()

