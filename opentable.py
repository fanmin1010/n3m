import requests
import json
from bs4 import BeautifulSoup

id = '261196'
url = 'http://www.opentable.com/restaurant/profile/'
url = url + id
url = url +'/search'
covers = '2'
dateTime = '2016-11-26 19:30'
#url = 'http://www.opentable.com/restaurant/profile/261196/search'
payload = {'covers':covers, 'dateTime':dateTime}
headers = {'Content-Type': 'application/json; charset=UTF-8'}
r = requests.post(url, params=payload, headers=headers)
#print (r.text)
soup = BeautifulSoup(r.text, 'html.parser')
for tag in soup.select('.dtp-results-times li'):
	print(tag.string)
#print(soup.prettify())

