# libraries

import urllib2 as url
from bs4 import BeautifulSoup
import re
import smtplib


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

if fcast.lower().find('rain') == -1:
    msg = 'No Snow Cone :('
else:
    msg = 'The fate of the world depends on you seeing this snow cone dude!!!'

# Send that message!

# Define the server
server = smtplib.SMTP('smtp.gmail.com', 587)
server.ehlo()
server.starttls()

#Next, log in to the server
server.login("olrustymccloud@gmail.com", "poopword")
me = 'olrustymccloud@gmail.com'
who = 'brettblock@gmail.com'
email = "\r\n".join([
  "From: "+me,
  "To: "+who,
  "Subject: A Communique from Cone Peak",
  "",
  msg
  ])

server.sendmail("olrustymccloud@gmail.com","brettblock@gmail.com",email)