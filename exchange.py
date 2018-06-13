import requests
from bs4 import BeautifulSoup
import datetime
import time
from peewee import *

db = MySQLDatabase(host = '127.0.0.1', user = 'root', passwd = '123456', database = 'coinmarketcap')

class Exchange(Model):
    rank = IntegerField()
    name = CharField()
    volume = CharField()  
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db

db.connect()

if not Exchange.table_exists():
  db.create_tables([Exchange])

response = requests.get('https://coinmarketcap.com/exchanges/volume/24-hour/all/')

soup = BeautifulSoup(response.text,"html.parser")

tr = soup.select('.table tr')

prevItem = []
prevName = ''
prevVolume = ''

rank = 0

for index,item in enumerate(tr):

    if (index ==0):
        prevName = item.attrs['id']

    if (item.has_attr('id') and index > 0):
        volumeTag = prevItem.select('.volume')[0]
        prevVolume = volumeTag.attrs['data-usd']
        
        if prevVolume == '?':
            prevVolume = '0'
        rank = rank + 1

        exchangedb = Exchange(rank=rank,name=prevName,volume=prevVolume)
        exchangedb.save()

        prevName = item.attrs['id']

    prevItem = item    

db.close()

