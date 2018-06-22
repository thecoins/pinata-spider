import requests
import bs4
import datetime
import time
import re
from peewee import *

#db = SqliteDatabase('./exchange.db')

db = MySQLDatabase(host = '127.0.0.1', user = 'root', passwd = '123456', database = 'coinmarketcap')

class CoinInfo(Model):
    # rank = IntegerField()
    name = CharField()
    url = CharField()
    announcement = CharField()
    explorer = CharField()
    explorer2 = CharField()
    explorer3 = CharField()
    chat = CharField()
    chat2 = CharField()
    message = CharField()
    github = CharField()
    alive = BooleanField(default=True)
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db

db.connect()

if not CoinInfo.table_exists():
  db.create_tables([CoinInfo])

response = requests.get('https://coinmarketcap.com/all/views/all')

soup = bs4.BeautifulSoup(response.text,"html.parser")

html = soup.select('.currency-name-container')

for index,item in enumerate(html):

    link = "https://coinmarketcap.com" + item.attrs['href']
    time.sleep(3)
    subpage = requests.get(link)

    subsoup = bs4.BeautifulSoup(subpage.text,"html.parser")

    name = item.text
    print index 
    print name
    urlobj = subsoup.select('.col-sm-4 .list-unstyled a')

    url = ''
    announcement = ''
    explorer = ''
    explorer2 = ''
    explorer3 = ''
    chat = ''
    chat2 = ''
    message = ''
    github = ''

    for i,item in enumerate(urlobj):
        text = item.text
        href = item.attrs['href']

        if re.match(r"Website", text):
            url = href
        elif re.match(r"Announcement", text):
            announcement = href
        elif re.match(r"Explorer$", text):
            explorer = href    
        elif re.match(r"Explorer 2", text):
            explorer2 = href
        elif re.match(r"Explorer 3", text):
            explorer3 = href  
        elif re.match(r"Chat$", text):
            chat = href
        elif re.match(r"Chat 2", text):
            chat2 = href    
        elif re.match(r"Message", text):
            message = href     
        elif re.match(r"Source", text):
            github = href  
        else: 
            print "unknow item"   
            print text
            print href             
    
    coininfo = CoinInfo(name=name,url=url,announcement=announcement,explorer=explorer,explorer2=explorer2,explorer3=explorer3,chat=chat,chat2=chat2,message=message,github=github)
    coininfo.save()

db.close()

