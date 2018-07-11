
import requests
import bs4
import datetime
import time
import re
from peewee import *

#db = SqliteDatabase('./exchange.db')

db = MySQLDatabase(host = '127.0.0.1', user = 'root', passwd = '123456', database = 'coinmarketcap')


# Coin info every 5 minute
class Coin(Model):
    coin_id = CharField()
    name = CharField()
    symbol = CharField()
    rank = IntegerField()
    price_usd = FloatField(null=True)
    price_btc = FloatField(null=True)
    volume_24h_usd = FloatField(null=True)
    market_cap_usd = FloatField(null=True)
    available_supply = FloatField(null=True)
    total_supply = FloatField(null=True)
    max_supply = FloatField(null=True)
    percent_change_1h = FloatField(null=True)
    percent_change_24h = FloatField(null=True)
    percent_change_7d = FloatField(null=True)
    last_updated =  IntegerField(null=True)
    price_cny = FloatField(null=True)
    volume_24h_cny = FloatField(null=True)
    market_cap_cny = FloatField(null=True)
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db

# Coin 12h price
class CoinPrices(Model):
    lastrank = IntegerField()
    lastprice = FloatField()
    name = CharField()
    prices = TextField()  
    # volume24 = TextField()
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db          

db.connect()

if not Coin.table_exists():
  db.create_tables([Coin])  
if not CoinPrices.table_exists():
  db.create_tables([CoinPrices])    


queryname = (Coin
         .select(Coin.name)
         .group_by(Coin.name))

for coin in queryname:
    name = coin.name        
    updatedAt = datetime.datetime.now()
    
    # Query volume from Exchange to ExchangeVolume
    prices = []
    querycoin = Coin.select(Coin.price_usd,coin.rank).where(Coin.name == name).order_by(Coin.timestamp.desc()).limit(144).dicts()
    last = querycoin[len(querycoin) -1]
    lastrank = last['rank']
    lastprice = float(str(last['price_usd']))
    for item in querycoin:
        prices.insert(0,float(str(item['price_usd'])))
    # print name
    updateprice = (CoinPrices
            .update(lastrank=lastrank,lastprice=lastprice,prices=prices,timestamp=updatedAt)
            .where(CoinPrices.name == name))
    pricesrows =  updateprice.execute()    
    # print volumerows
    if pricesrows == 0:
        print 'new Coinprices: ' + name     
        coinprice = CoinPrices(lastrank=lastrank,name=name,lastprice=lastprice,prices=prices)
        coinprice.save()  
       
db.close()

