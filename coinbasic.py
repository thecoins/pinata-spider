import requests
import json
import datetime
import time
from peewee import *

db = MySQLDatabase(host = '127.0.0.1', user = 'root', passwd = '123456', database = 'coinmarketcap')

class Coinbasic(Model):
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

db.connect()

if not Coinbasic.table_exists():
  db.create_tables([Coinbasic])

response = requests.get('https://api.coinmarketcap.com/v1/ticker/?convert=CNY&limit=1500')

ticker = json.loads(response.text)
# print ticker
print type(ticker)
for index,item in enumerate(ticker):
    
    coinbasic = Coinbasic(
    coin_id = item['id'],
    name = item['name'],
    symbol = item['symbol'],
    rank = item['rank'],
    price_usd = item['price_usd'],
    price_btc = item['price_btc'],
    volume_24h_usd = item['24h_volume_usd'],
    market_cap_usd = item['market_cap_usd'],
    available_supply = item['available_supply'],
    total_supply = item['total_supply'],
    max_supply = item['max_supply'],
    percent_change_1h = item['percent_change_1h'],
    percent_change_24h = item['percent_change_24h'],
    percent_change_7d = item['percent_change_7d'],
    last_updated =  item['last_updated'],
    price_cny = item['price_cny'],
    volume_24h_cny = item['24h_volume_cny'],
    market_cap_cny = item['market_cap_cny'])

    coinbasic.save()

db.close()

