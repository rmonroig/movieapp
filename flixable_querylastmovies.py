import os
import re
import csv
import pathlib
import time
import urllib
import urllib.parse as urlparse
from urllib.parse import urlencode
import requests
from bs4 import BeautifulSoup

#OWN MODULES
from utils.auxfuncs_requests import setting_headers
from utils.browsers_selenium import chrome_browser
import flixable_informationlists as flixinfo

with open("data/NetflixViewingHistory.csv", mode='r', encoding='UTF-8') as f:
    all_movies=csv.reader(f, delimiter=',')
    all_shows_netflix=[r[0] for r in all_movies]
    shows_netflix=[]
    for show in all_shows_netflix:
        if 'Temporada' in show:
            shows_netflix.append(show.split(':')[0])
        else:
            shows_netflix.append(show)
    shows_netflix=list(set(shows_netflix))


class Flixable():
    def __init__(self, tipo_show='series', min_rating=0, genero='', ano_minimo=1920, ano_maximo=2020, order="rating", npages=1):
        self.tipo_show=tipo_show
        self.genero=flixinfo.dic_genres[self.tipo_show][genero]
        self.end_point='https://es.flixable.com/genre/'+self.genero+'/'
        self.min_rating= min_rating
        self.genero=genero
        self.ano_minimo=ano_minimo
        self.ano_maximo=ano_maximo
        self.order=order
        self.url_string=self.url_encoding()
        self.npages=npages
        self.soup=self.query_recent_netflix()

    def url_encoding(self):
        url=f'{self.end_point}?min-rating={self.min_rating}&min-year={self.ano_minimo}&max-year={self.ano_maximo}&order={self.order}#filterForm'
        print(urllib.parse.quote_plus(url, safe=':/'))
        return url

    def query_recent_netflix(self):

        #query to flixable with requests only one page
        if self.npages==1:
            dict_query={'min-rating': self.min_rating, 'min-year': self.ano_minimo, 'max-year': self.ano_maximo, 'order': self.order}
            response=requests.get(self.end_point, params=dict_query, headers= setting_headers())
            print(response.url)
            print(response.status_code)
            html_source=BeautifulSoup(response.content, 'html.parser')


        #query with selenium more than one page
        else:
            browser=chrome_browser()
            browser.get(self.url_string)
            #Scroll down
            i=0
            SCROLL_PAUSE_TIME = 1
            last_height = browser.execute_script("return document.body.scrollHeight")
            while i<self.npages:
                # Scroll down to bottom
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                # Wait to load page
                time.sleep(SCROLL_PAUSE_TIME)
                # Calculate new scroll height and compare with last scroll height
                new_height = browser.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
                #Counting
                i=i+1
            html_source=BeautifulSoup(browser.page_source, 'html.parser')
            browser.close()
        #Assign attribute
        return html_source

    def get_allmovies(self):
        movies_flixable=[]
        for idx, el in enumerate(self.soup.find_all("div", class_="col-sm-6 col-lg-3 item")):
            #print(idx, el.h5.text)
            movies_flixable.append(el.h5.text)
        return movies_flixable


    def get_mynewmovies(self):
        
        movies_flixable=self.get_allmovies()
        print(len(movies_flixable))
        return [movie for movie in movies_flixable if movie not in shows_netflix]


flixable=Flixable(min_rating=60, npages=1)
#new_movies=flixable.get_allmovies()
#print(new_movies)
mynewmovies=flixable.get_mynewmovies()
print(len(mynewmovies))