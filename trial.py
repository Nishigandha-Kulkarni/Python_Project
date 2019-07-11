import requests
from bs4 import BeautifulSoup as bs
from string import ascii_lowercase
import pandas as pd

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
    a = []
    b = []
    c = []
    #dataset = pd.DataFrame({'Link':a})
    for l in ascii_lowercase:
        resp = requests.get(players_url + "/" + l + "/")

        soup = bs(resp.text, 'lxml')

        try:
            table = soup.find(id='players')
            tbody = table.tbody

        #page += 1

            for person_row in tbody.find_all('tr')[5:6]:
                print(person_row)
                link = base_url + person_row.th.a['href']
                player_info = get_players_info(link)

                name = person_row.th.a.text
                a.append(link)
                b.append(player_info)
                c.append(name)
        except AttributeError:
            break
    csvdata = [['Name','Player_Info','Link'], [c,b,a]]
    with open('trial.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(csvdata)


            #print(a)
            #print(name,link,player_info)

        #header = ["Name", "Player_Info", "Link"]
        #df = pd.DataFrame(c, b, a)
        #df.to_csv("trial.csv", columns = header, encoding = 'utf-8')



get_all_nba_players_after_1950()

