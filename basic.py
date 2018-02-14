import requests
import bs4
import datetime
import time
from peewee import *

#db = SqliteDatabase('./exchange.db')

db = MySQLDatabase(host = '127.0.0.1', user = 'root', passwd = '123456', database = 'coinmarketcap')

class Exchangebasic(Model):
    rank = IntegerField()
    name = CharField()
    volume = CharField()  
    url = CharField()
    twitter = CharField()
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db

db.connect()

if not Exchangebasic.table_exists():
  db.create_tables([Exchangebasic])

response = requests.get('https://coinmarketcap.com/exchanges/volume/24-hour/')

soup = bs4.BeautifulSoup(response.text,"html.parser")

html = soup.select('.volume-header a')

for index,item in enumerate(html):

    link = "https://coinmarketcap.com" + item.attrs['href']
    time.sleep(3)
    subpage = requests.get(link)

    subsoup = bs4.BeautifulSoup(subpage.text,"html.parser")

    nameobj = subsoup.select('.text-large')
    urlobj = subsoup.select('.list-unstyled a')
    volumeobj = subsoup.select('.text-large2')

    name = nameobj[0].text.strip()
    print name
    url = urlobj[0].text
    volume =  volumeobj[0].text
    twitter = ''
    if (len(urlobj) > 1):
      twitter = urlobj[1].attrs['href']
    print twitter

    exchangebasic = Exchangebasic(rank=index+1,name=name,volume=volume,url=url,twitter=twitter)
    exchangebasic.save()

db.close()

