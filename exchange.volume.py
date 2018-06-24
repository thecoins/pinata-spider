import requests
import bs4
import datetime
import time
import re
from peewee import *

#db = SqliteDatabase('./exchange.db')

db = MySQLDatabase(host = '127.0.0.1', user = 'root', passwd = '123456', database = 'coinmarketcap')


# Exchange 24h volume every 5 minute
class Exchange(Model):
    rank = IntegerField()
    name = CharField()
    volume = CharField()  
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db

# Exchange 12h volume and 24h volume
class ExchangeVolume(Model):
    lastrank = IntegerField()
    lastvolume = FloatField()
    name = CharField()
    volume = TextField()  
    # volume24 = TextField()
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db          

db.connect()

if not Exchange.table_exists():
  db.create_tables([Exchange])  
if not ExchangeVolume.table_exists():
  db.create_tables([ExchangeVolume])    


queryname = (Exchange
         .select(Exchange.name)
         .group_by(Exchange.name))

for exchange in queryname:
    name = exchange.name        
    updatedAt = datetime.datetime.now()
    
    # Query volume from Exchange to ExchangeVolume
    volume = []
    queryexchange = Exchange.select(Exchange.volume,Exchange.rank).where(Exchange.name == name).order_by(Exchange.timestamp.desc()).limit(144).dicts()
    last = queryexchange[-1]
    lastrank = last['rank']
    lastvolume = float(str(last['volume']))
    for item in queryexchange:
        volume.insert(0,float(str(item['volume'])))
    # print name
    updatevolume = (ExchangeVolume
            .update(lastrank=lastrank,lastvolume=lastvolume,volume=volume,timestamp=updatedAt)
            .where(ExchangeVolume.name == name))
    volumerows =  updatevolume.execute()    
    # print volumerows
    if volumerows == 0:
        print 'new ExchangeVolume: ' + name     
        exchangevolume = ExchangeVolume(lastrank=lastrank,name=name,lastvolume=lastvolume,volume=volume)
        exchangevolume.save()  
       
db.close()

