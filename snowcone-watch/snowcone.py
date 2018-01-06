# libs for NOAA web-scraping

import urllib2 as url
from bs4 import BeautifulSoup
import re
import smtplib
import datetime

# libs for Google Sheets API
from StringIO import StringIO
import pandas as pd



# NOAA forecast for Cone Peak in Big Sur

quote_page = 'http://forecast.weather.gov/MapClick.php?lon=-121.49632242355332&lat=36.05209089165366'

# Use BeautifulSoup to grab html

page = url.urlopen(quote_page)
soup = BeautifulSoup(page,'html.parser')

# Define a function to parse relevant
stringy_soup = str(soup)
start = '<!-- Everything between 7-Day Forecast and Footer goes in this row -->'
end = '<!-- Additional Forecasts and Information -->'

def extract_between(text, start, end, nth=1):
    if end not in text.split(start, nth)[-1]:
        return None
    return text.split(start, nth)[-1].split(end, nth)[0]

fcast = repr(extract_between(stringy_soup, start, end))
now = datetime.date.today().strftime("%B %d, %Y")

if fcast.lower().find('snow') == -1:
    msg = 'No Snow Cone forecasted for the week following ' + now
else:
    msg = 'The fate of the world depends on you seeing this snow cone dude!!!'

# import recipients from Google Sheets
#import requests
#r = requests.get('https://docs.google.com/spreadsheets/d/1xfP00wr0YvS7BU7_WTUJPTv2NEXiHnKc3w8Ko7F0J-0&output=csv')
#who = r.content
#who = pd.read_csv(StringIO(who), index_col=0)

# Send that message!

# Define the server
server = smtplib.SMTP('smtp.gmail.com', 587)
server.ehlo()
server.starttls()

#Next, log in to the server
server.login("olrustymccloud@gmail.com", "PCT4life!")
me = 'olrustymccloud@gmail.com'
who = 'brettvanderblock@gmail.com,brettblock@gmail.com,charlielewis@gmail.com,korydoran@gmail.com'

email = "\r\n".join([
  "From: "+me,
  "Bcc: "+who,
  "Subject: A Communique from Cone Peak - "+now,
  "",
  msg
  ])

server.sendmail(me,who,email)