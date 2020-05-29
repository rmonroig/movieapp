import sys
sys.setrecursionlimit(25000)

import multiprocessing
import concurrent.futures
from multiprocessing import Process, Manager, Queue, Pool

import csv
import os
import pathlib
import time
import requests
from bs4 import BeautifulSoup
from utils import auxfuncs_requests as aux_req
import asyncio
from proxybroker import Broker
import random


#Get users ids
with open('data/user_information.csv', "r") as f:
    data_csv=csv.reader(f)
    lst_movies=list(data_csv)
lst_user=[user[0] for user in lst_movies]


#proxy=get_list_proxies()[0]
#proxyDict = {"https" : 'https://'+ str(proxy.host)+':'+str(proxy.port),}
#response=requests.get(r'https://www.filmaffinity.com/es/userratings.php?user_id=657063', headers=aux_req.setting_headers(), proxies=proxyDict)
#html_soup =  BeautifulSoup(response.text, 'html.parser')
#print(html_soup)

def get_votes_user(queue, user):

    #url
    url='https://www.filmaffinity.com/es/userratings.php?'
    #Get proxies
    proxy=aux_req.get_list_proxies()[random.choice(list(range(0,10)))]
    print(proxy)
    sys.stdout.flush()
    proxyDict = {"https" : 'https://'+ str(proxy.host)+':'+str(proxy.port),}
    #First page to user
    pag=1
    params={'user_id':user,'p':pag,'orderby':4}
    html_soup, proxy=aux_req.check_if_correct_request_all(url, params, proxy)
    print('FIRST QUERY')

    for el in html_soup.find_all("div", class_="user-ratings-movie fa-shadow"):
        queue.append([user, el.a['title'], el.find('div', class_='ur-mr-rat').text])
        #queue.put([user, el.a['title'], el.find('div', class_='ur-mr-rat').text])

    #Check last page
    last_page=aux_req.check_last_page(html_soup)
    print('number of pages', last_page)
    sys.stdout.flush()
    #Next pages of votes
    pag=pag+1
    while pag<=last_page:
        params={'user_id':user,'p':pag,'orderby':4}
        html_soup, proxy=aux_req.check_if_correct_request_all(url, params, proxy)
        #response= requests.get('https://www.filmaffinity.com/es/userratings.php?', params=params)
        #html_soup, proxy=aux_req.check_if_correct_request(response)
        if html_soup=='break':
            break

        for el in html_soup.find_all("div", class_="user-ratings-movie fa-shadow"):
            queue.append([user, el.a['title'], el.find('div', class_='ur-mr-rat').text])
            #queue.put([user, el.a['title'], el.find('div', class_='ur-mr-rat').text])

        pag=pag+1

        #Sleeping time
        time.sleep(2)

    return queue



if __name__ == '__main__':
    print('start')
    





'''
    with Manager() as manager:
        queue=manager.list()
        processes=[]
        for id_ in lst_user:
            print(id_)
            p=Process(target=get_votes_user, args=(queue, id_))
            p.start()
            processes.append(p)

        for p in processes:
            p.join()

        print(queue)
        final_data=list(queue)

        with open("data/filmaffinity_data/vote_user.csv", "w", newline='') as f:
            wr = csv.writer(f)
            wr.writerows(final_data)
'''
'''

    pool = multiprocessing.Pool(8)
    queue = Manager().Queue()
    for id_ in lst_user[2:4]:
        pool.apply(get_votes_user, args=(queue, id_))
    pool.close()
    pool.join()

    final_data=[]
    while queue.empty() is False:
        print(queue.get())
        final_data.append(queue.get())

    with open("data/filmaffinity_data/vote_user.csv", "w", newline='') as f:
        wr = csv.writer(f)
        wr.writerows(final_data)








def get_votes_user(queue, user):

    #Get proxies
    aux_req.get_list_proxies()
    proxy=aux_req.get_list_proxies()[0]
    proxyDict = {"https" : 'https://'+ str(proxy.host)+':'+str(proxy.port),}
    #First page to user
    pag=1
    params={'user_id':user,'p':pag,'orderby':4}
    response= requests.get('https://www.filmaffinity.com/es/userratings.php?', headers=aux_req.setting_headers(authority='https://www.filmaffinity.com'), params=params, proxies=proxyDict)
    html_soup =  BeautifulSoup(response.text, 'html.parser')

    for el in html_soup.find_all("div", class_="user-ratings-movie fa-shadow"):
        queue.append([user, el.a['title'], el.find('div', class_='ur-mr-rat').text])
        #lst_user_votes.append([user, el.a['title'], el.find('div', class_='ur-mr-rat')])
        #dic_user_votes[user]["movie_votes"][el.a['title']]=el.find('div', class_='ur-mr-rat').text.replace(',','.')

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
            queue.append([user, el.a['title'], el.find('div', class_='ur-mr-rat').text])
        pag=pag+1

        #Sleeping time
        time.sleep(2)

    return queue





async def show(proxies, lst_proxies):

    while True:
        proxy = await proxies.get()
        if proxy is None: break
        #print('Found proxy: %s' % proxy)
        lst_proxies.append(proxy)




def get_list_proxies():
    lst_proxies=[]
    proxies = asyncio.Queue()
    broker = Broker(proxies)
    tasks = asyncio.gather(
        broker.find(types=['HTTP', 'HTTPS'], limit=2),
        show(proxies, lst_proxies))

    loop = asyncio.get_event_loop()
    loop.run_until_complete(tasks)
    return lst_proxies

print(get_list_proxies())




#print((lst_proxies[0].__dict__))
#print((lst_proxies[0].host))

    #json.dump(data, f)

def howmany_within_range(row, minimum, maximum):
    """Returns how many numbers lie within `maximum` and `minimum` in a given `row`"""
    count = 0
    for n in row:
        if minimum <= n <= maximum:
            count = count + 1
    return count

def howmany_within_range_rowonly(row, minimum=4, maximum=8):
    count = 0
    for n in row:
        if minimum <= n <= maximum:
            count = count + 1
    return count


if __name__ == "__main__":
    import numpy as np
    import multiprocessing as mp

    np.random.RandomState(100)
    arr = np.random.randint(0, 10, size=[200000, 5])
    data = arr.tolist()

    start = time.time()

    results=[]
    for row in data:
        results.append(howmany_within_range(row, minimum=4, maximum=8))
    print(results[:10])

    end = time.time()
    print(end - start)

    # Step 1: Init multiprocessing.Pool()
            pool = mp.Pool(mp.cpu_count())


            # Step 2: `pool.apply` the `howmany_within_range()`
            results = [pool.apply(howmany_within_range, args=(row, 4, 8)) for row in data]

            # Step 3: Don't forget to close
            pool.close()
    start = time.time()
    pool = mp.Pool(mp.cpu_count())
    print('start process')
    results = pool.map(howmany_within_range_rowonly, [row for row in data])
    pool.close()
    end = time.time()
    print(end - start)
    print(results[:10])

'''

