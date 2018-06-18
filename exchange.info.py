import requests
import bs4
import datetime
import time
import re
from peewee import *

#db = SqliteDatabase('./exchange.db')

db = MySQLDatabase(host = '127.0.0.1', user = 'root', passwd = '123456', database = 'coinmarketcap')

# Exchange basic info
class ExchangeInfo(Model):
    rank = IntegerField()
    name = CharField()
    nick = CharField()
    url = CharField()
    fees = CharField()
    chat = CharField()
    blog = CharField()
    twitter = CharField()
    alive = BooleanField(default=True)
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db

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
    name = CharField()
    volume12 = TextField()  
    volume24 = TextField()
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db          

db.connect()

if not ExchangeInfo.table_exists():
  db.create_tables([ExchangeInfo])
if not Exchange.table_exists():
  db.create_tables([Exchange])  
if not ExchangeVolume.table_exists():
  db.create_tables([ExchangeVolume])    

# index page
response = requests.get('https://coinmarketcap.com/exchanges/volume/24-hour/all/')

soup = bs4.BeautifulSoup(response.text,"html.parser")

# html = soup.select('.volume-header a')
tr = soup.select('.table tr')
rank = 0
# for index,item in enumerate(html):
for index,item in enumerate(tr):

    if (item.has_attr('id')):
        nick = item.attrs['id']
        print nick
        rank = rank + 1
        # exchange page
        link = "https://coinmarketcap.com/exchanges/" + nick
        time.sleep(3)
        subpage = requests.get(link)

        subsoup = bs4.BeautifulSoup(subpage.text,"html.parser")

        nameobj = subsoup.select('.logo-32x32')
        name = nameobj[0].attrs['alt']
        print name              

        urlobj = subsoup.select('.col-xs-12 .list-unstyled a')
        # Exchange property
        fees = ''
        chat = ''
        blog = ''
        url = ''
        twitter = ''

        for i,item in enumerate(urlobj):
            text = item.text
            href = item.attrs['href']

            if re.match(r"http", text):
                url = href
            if re.match(r"Fees", text):
                fees = href
            if re.match(r"Chat", text):
                chat = href
            if re.match(r"Blog", text):
                blog = href  
            if re.match(r"@", text):
                twitter = href   

        updatedAt = datetime.datetime.now()
        
        # Query volume from Exchange to ExchangeVolume
        volume12 = []
        query12 = Exchange.select(Exchange.volume).where(Exchange.name == nick).order_by(Exchange.timestamp.desc()).limit(144).dicts()
        for item12 in query12:
          volume12.insert(0,float(str(item12['volume'])))
        volume24 = []
        query24 = Exchange.select(Exchange.volume).where(Exchange.name == nick).order_by(Exchange.timestamp.desc()).limit(288).dicts()
        for item24 in query24:
          volume24.insert(0,float(str(item24['volume'])))
        
        queryVolume = (ExchangeVolume
                .update(volume12=volume12,volume24=volume24,timestamp=updatedAt)
                .where(ExchangeVolume.name == nick))
        volumerows =  queryVolume.execute()    
        if volumerows == 0:
            print 'new ExchangeVolume: ' + name     
            exchangevolume = ExchangeVolume(name=nick,volume12=volume12,volume24=volume24)
            exchangevolume.save()  
        
        # Update Exchange Rank
        queryExchange = (ExchangeInfo
                .update(rank=rank,timestamp=updatedAt,alive=True)
                .where(ExchangeInfo.name == name))
        rows =  queryExchange.execute()    
        if rows == 0:
            print 'new Exchange: ' + name     
            exchangeinfo = ExchangeInfo(rank=rank,name=name,nick=nick,fees=fees,chat=chat,blog=blog,url=url,twitter=twitter)
            exchangeinfo.save()   

# Set Exchange unalive if No more updates
thistime = datetime.datetime.now()
yesterday = thistime - datetime.timedelta(days=1)
yesterdayLast = yesterday.replace(hour=0,minute=0,second=0,microsecond=0)

query = (ExchangeInfo
            .update(rank=-1,alive=False)
            .where(ExchangeInfo.timestamp < yesterdayLast))
rows =  query.execute()    
print rows        
        
db.close()

