import requests
from bs4 import BeautifulSoup as bs
from string import ascii_lowercase
import lxml
import csv

base_url = "https://www.basketball-reference.com/"


# Functions to write data into csv, json files
def output_csv(filename, data, header):
    with open('asd.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(data)
    return print("Writing to CSV successful.....")


def output_json(filename, data):
    with open('qwerty.json', 'w') as file:
        json.dump(data, file, indent=4)
    return print("Json write successful...", end='\n\n')


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
    with open('trial123.csv', 'w') as csvfile:
        csvfile.close()
    global base_url
    players_url = base_url + "players"
    a = list(map(chr, range(97, 120)))
    for l in a:
    #for l in ascii_lowercase:
        resp = requests.get(players_url + "/" + l + "/")

        soup = bs(resp.text, 'lxml')

        table = soup.find(id='players')
        tbody = table.tbody
        for person_row in tbody.find_all('tr')[5:6]:
            print(person_row)
            link = base_url + person_row.th.a['href']
            player_info=get_players_info(link)

            name = person_row.th.a.text

    output_csv('popular', list(zip(name, player_info, link)), ['name', 'ratings', 'links'])
    output_json('popular', dict(zip(['movies', 'ratings', 'links'], zip(*list(zip(movies, ratings, posters_links))))))
    print('Completed.', end='\n\n')


get_all_nba_players_after_1950()



