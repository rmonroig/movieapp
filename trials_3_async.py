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
from api_queries.utils_filmaffinity import auxfuncs_requests as aux_req
import asyncio
from proxybroker import Broker
import random


#Get users ids
with open('data/filmaffinity_data/user_information.csv', "r") as f:
    data_csv=csv.reader(f)
    lst_movies=list(data_csv)
lst_user=[user[0] for user in lst_movies]



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
    loop.close()

    return lst_proxies

print(get_list_proxies())




#if __name__ == '__main__':


'''






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

