import requests
import bs4
import datetime
import time
from peewee import *

#db = SqliteDatabase('./exchange.db')

db = MySQLDatabase(host = '127.0.0.1', user = 'root', passwd = '123456', database = 'exchange')

class Exchange(Model):
    rank = IntegerField()
    name = CharField()
    volume = CharField()      
    url = CharField()
    timestamp = DateTimeField(default=datetime.datetime.now)


    class Meta:
        database = db

db.connect()

db.drop_tables([Exchange])

db.create_tables([Exchange])

response = requests.get('https://coinmarketcap.com/exchanges/volume/24-hour/')

# print response.text

soup = bs4.BeautifulSoup(response.text,"html.parser")

html = soup.select('.volume-header a')

for index,item in enumerate(html):

    link = "https://coinmarketcap.com" + item.attrs['href']
    time.sleep(3)
    subpage = requests.get(link)

    subsoup = bs4.BeautifulSoup(subpage.text,"html.parser")

    name = subsoup.select('.text-large')
    volume = subsoup.select('.text-large2')
    url = subsoup.select('.list-unstyled a')

    print index + 1
    print name[0].text
    print volume[0].text
    print url[0].text


    exchange = Exchange(rank=index+1,name=name[0].text,volume=volume[0].text,url=url[0].text)
    exchange.save()

db.close()

