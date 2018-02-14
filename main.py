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

class Exchange(Model):
    rank = IntegerField()
    name = CharField()
    volume = CharField()      
    # url = CharField()
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db

class Exchangelog(Model):
    start = DateTimeField()
    end = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db

db.connect()

# db.drop_tables([Exchange])
if not Exchangebasic.table_exists():
  db.create_tables([Exchangebasic])

if not Exchange.table_exists():
  db.create_tables([Exchange])

if not Exchangelog.table_exists():
  db.create_tables([Exchangelog])

response = requests.get('https://coinmarketcap.com/exchanges/volume/24-hour/')

# print response.text

soup = bs4.BeautifulSoup(response.text,"html.parser")

html = soup.select('.volume-header a')

start = datetime.datetime.now()

for index,item in enumerate(html):
    updatedAt = datetime.datetime.now()

    link = "https://coinmarketcap.com" + item.attrs['href']
    time.sleep(3)
    subpage = requests.get(link)

    subsoup = bs4.BeautifulSoup(subpage.text,"html.parser")

    nameobj = subsoup.select('.text-large')
    volumeobj = subsoup.select('.text-large2')
    urlobj = subsoup.select('.list-unstyled a')

    name = nameobj[0].text.strip()
    print name
    volume =  volumeobj[0].text
    url = urlobj[0].text

    twitter = ''
    if (len(urlobj) > 1):
      twitter = urlobj[1].attrs['href']

    query = (Exchangebasic
             .update(volume=volume,timestamp=updatedAt)
             .where(Exchangebasic.name == name))
    rows =  query.execute()    
    if rows == 0:
        print 'new Exchange: ' + name
        exchangebasic = Exchangebasic(rank=index+1,name=name,volume=volume,url=url,twitter=twitter)
        exchangebasic.save() 
    exchange = Exchange(rank=index+1,name=name,volume=volume)
    exchange.save()

exchangelog = Exchangelog(start=start) 
exchangelog.save()   

db.close()

