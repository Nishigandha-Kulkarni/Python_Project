import requests
from bs4 import BeautifulSoup as bs
from string import ascii_lowercase
import lxml
import csv

base_url = "https://www.basketball-reference.com/"


def get_players_info(player_url):
    resp = requests.get(player_url)
    soup = bs(resp.text, 'lxml')
    div = soup.find(id="info")

    # meta = div.find(id="meta")
    src = div.find(class_="media-item")
    if not src == None:
        src=src.img["src"]
    pargraphs=div.div.find_all("p")
    player_details=""
    for p in pargraphs:
        player_details+=p.text
    return (src,player_details)
def get_all_nba_players_after_1950():
    global base_url
    players_url = base_url + "players"
    a = list(map(chr, range(97, 120)))
    for l in a:

        resp = requests.get(players_url + "/" + l + "/")

        soup = bs(resp.text, 'lxml')

        table = soup.find(id='players')


get_all_nba_players_after_1950()



