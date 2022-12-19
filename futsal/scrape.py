import requests
from bs4 import BeautifulSoup

url = 'https://www.revolutionise.com.au/futsalhqsuper5s/games/7347/&d=15983'

html = requests.get(url).content

soup = BeautifulSoup(html, 'html.parser')

fixtures = soup.find('div', class_ = 'card box-shadow-lg')

round_links = fixtures.find_all('a')

print([link.get('href') for link in round_links])
