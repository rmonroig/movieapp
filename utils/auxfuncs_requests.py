from bs4 import BeautifulSoup
import time
from utils import formatting_strings as formatstr
from utils import browsers_selenium
import requests
import asyncio
from proxybroker import Broker
import os
import sys
import random

def setting_headers(authority=''):
    headers = {
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'upgrade-insecure-requests': '1',
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9'}

    return headers



def get_users_comments_movies(soup):
    user_id=[]
    user_country=[]
    user_rating=[]
    for el in soup.find_all('div', class_ = "fa-shadow movie-review-wrapper rw-item"):
        user_id.extend([i.attrs['data-user-id'] for i in  el.find_all("div", class_="user-info")])
        user_country.extend([i.text for i in  el.find_all("div", class_="mr-user-country")])
        user_rating.extend([i.text for i in  el.find_all("div", class_="user-reviews-movie-rating")])


    final_rows=[list(a) for a in zip(user_id, user_country, user_rating)]
    final_rows=formatstr.remv_str(final_rows, "\n", "")
    final_rows=formatstr.remv_str(final_rows, "\r", "")
    final_rows=formatstr.remove_extraspaces(final_rows)

    return final_rows

def check_last_page(soup):
    try:
        pages=[]
        for el in soup.find("div", class_="pager").findAll("a"):
            pages.append(el.text)
        last_page=int(pages[-2])
    except:
        last_page=1
    return last_page



async def show(proxies, lst_proxies):

    while True:
        proxy = await proxies.get()
        if proxy is None: break
        #print('Found proxy: %s' % proxy)
        lst_proxies.append(proxy)


def get_list_proxies(limit=20):
    lst_proxies=[]
    proxies = asyncio.Queue()
    broker = Broker(proxies)
    tasks = asyncio.gather(
        broker.find(types=['HTTPS'], limit=limit),
        show(proxies, lst_proxies))

    loop = asyncio.get_event_loop()
    loop.run_until_complete(tasks)
    loop.close()
    return lst_proxies


def check_if_correct_request(response):

    url=response.url
    status_code=response.status_code
    html_soup =  BeautifulSoup(response.text, 'html.parser')
    i=0
    #Check status code:
    while status_code!=200:
        proxy=get_list_proxies()[random.choice(list(range(0,10)))]
        proxyDict = {"https" : 'https://'+ str(proxy.host)+':'+str(proxy.port),}
        response=requests.get(url, headers=setting_headers(), proxies=proxyDict)
        html_soup =  BeautifulSoup(response.text, 'html.parser')
        status_code=response.status_code
        if i==3:
            html_soup='break'
            break
        i=i+1
    return html_soup


def check_if_correct_request_all(url, params, proxy):
    proxy=proxy
    print('the proxy:port', proxy.host, ':', proxy.port)
    proxyDict = {"https" : 'https://'+ str(proxy.host)+':'+str(proxy.port),}

    try:
        #Try to do request
        response= requests.get(url, headers=setting_headers(authority=''), params=params, proxies=proxyDict)
        status_code=response.status_code
        print(response.status_code)
        sys.stdout.flush()
        html_soup =  BeautifulSoup(response.text, 'html.parser')
    except Exception as e:
        time.sleep(2)
        print('error', e)
        sys.stdout.flush()
        proxy=get_list_proxies()[random.choice(list(range(0,10)))]
        print('new proxy-------------->', proxy.host, ':', proxy.host)
        sys.stdout.flush()
        proxyDict = {"https" : 'https://'+ str(proxy.host)+':'+str(proxy.port),}
        response= requests.get(url, headers=setting_headers(authority=''), params=params, proxies=proxyDict)
        status_code=response.status_code
        print(response.status_code)
        sys.stdout.flush()
        html_soup =  BeautifulSoup(response.text, 'html.parser')


    #print(html_soup)
    b=0
    #Check status code:
    while status_code!=200:
        time.sleep(5)
        print('error ', status_code, ' sleeping...')
        sys.stdout.flush()
        proxy=get_list_proxies()[random.choice(list(range(0,10)))]
        proxyDict = {"https" : 'https://'+ str(proxy.host)+':'+str(proxy.port),}
        response= requests.get(url, headers=setting_headers(authority=''), params=params, proxies=proxyDict)
        status_code=response.status_code
        print('2 try',response.status_code)
        sys.stdout.flush()

        html_soup =  BeautifulSoup(response.text, 'html.parser')


        if b==3:
            html_soup='break'
            break
        b=b+1

    return html_soup, proxy
