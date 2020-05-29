#INIT FILE
import definitions as def_
import configparser
init_file= def_.init_file; ROOT_DIR=def_.ROOT_DIR
#config file
config = configparser.ConfigParser(); config.read(init_file)
filmaffinity_otherusersid=ROOT_DIR+config['paths']['filmaffinity_otherusersid']
filmaffinity_otheruservotes=ROOT_DIR+config['paths']['filmaffinity_otherusersvotes']

import requests
from bs4 import BeautifulSoup
import csv
import json
#System
import os
import time
import urllib

#OWN MODULES
from api_queries.browser_connection import browsers_selenium
from api_queries.utils_filmaffinity import auxfuncs_requests as aux_req
from api_queries.utils import formatting_strings


#Get users ids
with open(filmaffinity_otherusersid, "r") as f:
    data_csv=csv.reader(f)
    lst_movies=list(data_csv)
lst_user=[user[0] for user in lst_movies]


dic_user_votes={}
for idx, user in enumerate(lst_user[180:]):
    print(idx, user)
    dic_user_votes[user]={'movie_votes':{}}

    #First page to user
    pag=1
    params={'user_id':user,'p':pag,'orderby':4}
    response= requests.get('https://www.filmaffinity.com/es/userratings.php?', headers=aux_req.setting_headers(authority='https://www.filmaffinity.com'), params=params)
    html_soup =  BeautifulSoup(response.text, 'html.parser')
    if html_soup=="break":
        break

    for el in html_soup.find_all("div", class_="user-ratings-movie fa-shadow"):
        dic_user_votes[user]["movie_votes"][el.a['title']]=el.find('div', class_='ur-mr-rat').text.replace(',','.')

    #Check last page
    last_page=aux_req.check_last_page(html_soup)
    print('number of pages', last_page)

    #Next pages of votes
    pag=pag+1
    while pag<=last_page:
        params={'user_id':user,'p':pag,'orderby':4}
        response= requests.get('https://www.filmaffinity.com/es/userratings.php?', params=params)
        html_soup=aux_req.check_if_correct_request(response)

        for el in html_soup.find_all("div", class_="user-ratings-movie fa-shadow"):
            dic_user_votes[user]["movie_votes"][el.a['title']]=el.find('div', class_='ur-mr-rat').text.replace(',','.')

        pag=pag+1
        #Sleeping time
        time.sleep(2)

    #Write json file
    with open(filmaffinity_otheruservotes, 'w', encoding='utf-8') as f:
        json.dump(dic_user_votes, f, ensure_ascii=False)


print(dic_user_votes)
