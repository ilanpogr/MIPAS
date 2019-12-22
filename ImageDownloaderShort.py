import re
import httplib2
import random
from bs4 import SoupStrainer, BeautifulSoup
from pandas import DataFrame
import csv
from PIL import Image
from io import BytesIO

'''------------------------------------
TMP IMPORTS
------------------------------------'''


import time
from pprint import pprint
import os
import psutil

'''------------------------------------
GLOBAL VARS
------------------------------------'''

http = httplib2.Http()

stores_dict_file_name = 'stores_dict.csv'
downloadded_stores_file_name = 'downloaded_stores_dict.txt'
init_path = 'photos/'
search_page_counter = 0


stores = {}
downloaded_stores = set()

default_image_size_str = '340x270.'

store_products = set()
failed_stores = set()
failed_products = {}

'''------------------------------------
PRINTING AND DEBUGGING METHODS
------------------------------------'''


def convert_time(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%d:%02d:%02d" % (hour, minutes, seconds)


def print_output_for_debug(start_time):
    process = psutil.Process(os.getpid())
    print('------------------------------------------------------------------------------------')
    print('CURRENT RUNTIME: ' + convert_time(time.time() - start_time))
    print('------------------------------------------------------------------------------------')
    print("CURRENT MEMORY USAGE: " + str(float(process.memory_info().rss / 1000000)) + " MB")
    print('------------------------------------------------------------------------------------')


def program_initial_print(start_time):
    print('------------------------------------------------------------------------------------')
    print('START TIME: %s' % start_time)
    print('------------------------------------------------------------------------------------')
    process = psutil.Process(os.getpid())
    print("INITIAL MEMORY USAGE: " + str(float(process.memory_info().rss / 1000000)) + " MB")
    print('------------------------------------------------------------------------------------')
    print()


'''------------------------------------
TIMING AND HTTP REQUEST METHODS
------------------------------------'''


def sleeper():
    '''wait random time between "min_time" and "max_time" seconds'''
    min_time = 1.5
    max_time = 4.5
    num = random.uniform(min_time, max_time)
    time.sleep(num)


def response_handler(url, status):
    print("\nDEBUG: ERROR WITH PAGE REQUEST: " + url)
    print("\tdue to response status: " + str(status))
    print("\nCURRENT PAGE: " + str(search_page_counter))


def make_http_req(url):
    sleeper()
    try:
        resp, data = http.request(url)
        if resp.status == 200:
            return data
        else:
            time.sleep(20)
            print('---------???????????????????????????????????????????????????????????????????---------')
            pprint(resp)
            print('---------???????????????????????????????????????????????????????????????????---------')
            resp, data = http.request(url)
            if resp.status == 200:
                return data
            else:
                response_handler(url, resp.status)
                return None
    except (httplib2.HttpLib2Error, ConnectionError, TimeoutError):
        print('--------------EXCEPTION RAISED, CHECK YOUR INTERNET CONNECTION.--------------')
        return None


'''------------------------------------
PRE-RUNNING METHODS - STORES LIST AND DICT INITIALIZE
------------------------------------'''


def get_all_stores_urls():
    with open(stores_dict_file_name, "r") as f:
        reader = csv.reader(f, delimiter="\t")
        next(reader, None)
        for _, line in enumerate(reader):
            slots = line[0].split(',')
            url = slots[-1]
            name = slots[1]
            stores[name] = url


def get_all_downloaded_stores():
    with open(downloadded_stores_file_name, "r") as f:
        lines = f.readlines()
        for line in lines:
            line = line.replace('\n', '')
            downloaded_stores.add(line)


def append_store_to_chache(url):
    with open(downloadded_stores_file_name, 'a') as f:
        f.write(url + '\n')


'''------------------------------------
IMAGE DOWNLOAD SCRIPT
------------------------------------'''


def get_number_of_pages_in_store(data):
    pages_a_links = SoupStrainer('a', {'data-page': re.compile('^[0-9]*$')})
    link_elements = BeautifulSoup(data, 'lxml', parse_only=pages_a_links).findAll('span')
    pages = set()
    for span in link_elements:
        if re.match(r'^[0-9]*$', span.text) and span.text != '':
            pages.add(int(span.text))
    try:
        return max(pages, key=int)
    except ValueError:
        return None


def download_image(resp, content, store_name, img_url):
    if not os.path.exists(init_path + store_name):
        os.makedirs(init_path + store_name)
    rest = img_url.split('?version', 1)[0].split(default_image_size_str)[1]
    file_path = init_path + store_name + '/' + rest
    with open(file_path, 'wb') as f:
        f.write(content)


def get_products_from_page(data, store_name, current_url):
    if data is not None:
        products_a_links_in_page = SoupStrainer('a', {'class': re.compile('listing-link')})
        products_links_elements = BeautifulSoup(data, 'lxml', parse_only=products_a_links_in_page).findAll('a')
        for a in products_links_elements:
            img = a.find('img')
            try:
                resp, data = http.request(img['src'])
                if resp.status == 200:
                    download_image(resp, data, store_name, img['src'])
                else:
                    failed_products[store_name + ',' + current_url] = img['src']
            except (httplib2.HttpLib2Error, ConnectionError, TimeoutError):
                failed_products[store_name + ',' + current_url] = img['src']
            except(KeyError, AttributeError):
                try:
                    resp, data = http.request(img['data-src'])
                    if resp.status == 200:
                        download_image(resp, data, store_name, img['data-src'])
                    else:
                        failed_products[store_name + ',' + current_url] = img['data-src']
                except (httplib2.HttpLib2Error, ConnectionError, TimeoutError):
                    failed_products[store_name + ',' + current_url] = img['data-src']
                except(KeyError, AttributeError):
                    failed_products[store_name + ',' + current_url] = a['href']


def download_all_products_from_store(store_name, store_url):
    search_page_counter = 1
    data = make_http_req(store_url)
    if data is None:
        failed_stores.add(store_url)
        return
    get_products_from_page(data, store_name, store_url)
    num_of_pages = get_number_of_pages_in_store(data)
    if num_of_pages is not None:
        page_url_sefix = '&page={page_num}#items'
        #     page_url = store_url + page_url_sefix.format(page_num=1)
        for i in range(2, num_of_pages + 1):
            page_url = store_url + page_url_sefix.format(page_num=i)
            search_page_counter = i
            data = make_http_req(page_url)
            get_products_from_page(data, store_name, page_url)


'''------------------------------------
SCRIPT METHOD CALL
------------------------------------'''


start_time = time.ctime()
program_initial_print(start_time)
start_time = time.time()
get_all_stores_urls()
get_all_downloaded_stores()
if not os.path.exists(init_path.replace('/', '')):
    os.makedirs(init_path.replace('/', ''))
i = 0
for name, url in stores.items():
    i += 1
    if url in downloaded_stores:
        continue
    print('************************************************************************************')
    print('STORE: ' + name + ' --- ' + str(i) + '/' + str(len(stores)))
    print('************************************************************************************')
    download_all_products_from_store(name, url)
    append_store_to_chache(url)
    store_products = set()
    print_output_for_debug(start_time)

