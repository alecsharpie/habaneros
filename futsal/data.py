import requests
from bs4 import BeautifulSoup

def get_history(link):

    html = requests.get(link).content

    soup = BeautifulSoup(html, 'html.parser')

    return soup


def get_positions_table():

    base_url = 'https://www.revolutionise.com.au/futsalhqsuper5s/pointscores/7347/&d=15983'

    html = requests.get(base_url).content

    soup = BeautifulSoup(html, 'html.parser')

    return soup
