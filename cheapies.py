from bs4 import BeautifulSoup
from discord_webhook import DiscordWebhook, DiscordEmbed
from time import sleep
from playwright.sync_api import sync_playwright

import requests
import datetime
import sqlite3
import sys
sys.path.append(r"C:\Users\wills\Desktop\Coding\web-scraping")
sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')
from discordWebhooks import *
          

def cheapiesSearch():
  ## Create DB if needed ###
  conn = sqlite3.connect(r'C:\Users\wills\Desktop\Coding\web-scraping\cheapies\deals.db')
  c = conn.cursor() 
  c.execute("CREATE TABLE IF NOT EXISTS deals(ID integer, Name TEXT, DateAdded TEXT)")
  conn.commit()
  c.execute("SELECT ID FROM deals ORDER BY DateAdded DESC ")
  allResult = str(c.fetchall())

    
  r = requests.get("https://www.cheapies.nz/deals?noexpired=1")

  if r.status_code != 200:
    print('Cheapies down, exiting')
    exit()
  soup = BeautifulSoup(r.text, "html.parser")
  container = soup.select(".node")

  try:
    for eachDeal in container:
      dealTitle = eachDeal.select('.title')[0].text
      dealURL = "https://www.cheapies.nz" + eachDeal.select('.title a')[0]['href']
      dealContent = eachDeal.select('.content')[0].text.strip()
      dealID = eachDeal.select('.title a')[0]['href'].split('/node/').pop(-1)
      dealImage = eachDeal.select('.foxshot-container img')[0]['src'].rsplit('?').pop(0)

      if dealID not in allResult:
        dateAdded = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print(f"Adding new data - {dealTitle}")

        webhook = DiscordWebhook(url=discordListings)
        embed = DiscordEmbed(description=f"{dealContent}", color='03b2f8', url=dealURL)
        embed.set_author(name=dealTitle, url=dealURL, icon_url='https://cdn.virtualpornhd.com/wp-content/uploads/2022/08/vrphd_2.png')
        embed.set_image(url=dealImage)
        webhook.add_embed(embed)
        webhook.execute()

        c.execute("INSERT INTO deals VALUES(?,?,?)", (dealID, dealTitle, dateAdded))
        conn.commit() 
  except:
    pass
  finally:
    pass