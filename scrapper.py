import requests
from bs4 import BeautifulSoup as bs
from string import ascii_lowercase
import lxml
import csv
from sqlalchemy import create_engine,Column,String,Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import re

base_url = "https://www.basketball-reference.com/"

Model=declarative_base()

engine = create_engine('sqlite:///mydb.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

class Players(Model):
    __tablename__="players"
    id=Column(Integer,primary_key=True,autoincrement=True)
    name=Column(String)
    image_link=Column(String)
    height=Column(Integer)
    weight=Column(Integer)
    dob=Column(String)
    place=Column(String)
    position=Column(String)

    def __repr__(self):
        return "<Players %s>" % self.name


Model.metadata.create_all(engine)

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
    position=None
    shoots=None
    height=None
    weight=None
    dob=None
    place=None
    try:
        for p in pargraphs:
            if "Position" in p.text:
                data=p.text.split(":")
                position=data[1].split("▪")[0].strip()
                
            if "cm," in p.text and "kg)" in p.text:
                height=p.text.split("cm")[0].split("(")[1].strip()
                weight=p.text.split("kg)")[0].split("cm,")[1].strip()
            if "Born:" in  p.text:
                dob=p.text.split("(Age")[0].split("Born:")[1].split("in")[0]
                dob=re.sub("[\n+\s+]"," ",dob)
                place=p.text.split("in")[1]
                place=re.sub("[\n+\s+]"," ",place)
    except:
            pass
        
    return (src,height,weight,dob,place,position)

def get_all_nba_players_after_1950():
    
    global base_url
    players_url = base_url + "players"
    a = list(map(chr, range(97, 120)))
    for l in a[4:]:
        resp = requests.get(players_url + "/" + l + "/")

        soup = bs(resp.text, 'lxml')

        table = soup.find(id='players')
        tbody = table.tbody
        for person_row in tbody.find_all('tr'):
            # print(person_row)
            link = base_url + person_row.th.a['href']
            player_info=get_players_info(link)

            name = person_row.th.a.text
            
            player=Players(name=name,image_link=player_info[0],height=player_info[1],weight=player_info[2],dob=player_info[3],place=player_info[4],position=player_info[5])
            session.add(player)
            session.commit()
           
    # output_csv('popular', list(zip(name, player_info, link)), ['name', 'ratings', 'links'])
    # output_json('popular', dict(zip(['movies', 'ratings', 'links'], zip(*list(zip(movies, ratings, posters_links))))))
    # print('Completed.', end='\n\n')


# get_all_nba_players_after_1950()
print(len(session.query(Players).all()))

# print(session.query(Players).all())


