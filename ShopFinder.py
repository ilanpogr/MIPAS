import httplib2
from bs4 import SoupStrainer, BeautifulSoup
from pandas import DataFrame

import csv
from os import path


'''------------------------------------
TMP IMPORTS
------------------------------------'''

import time
import re
import random


'''------------------------------------
GLOBAL VARS
------------------------------------'''


http = httplib2.Http()

search_page_counter = 1
search_page_last = 250
stores_dict = {}
store_category = 'jewelry'
sub_category = ['necklaces', 'earrings', 'bracelets', 'rings']
file_name = 'stores_dict.csv'


'''------------------------------------
TIMING AND HTTP REQUEST METHODS
------------------------------------'''


def sleeper():
    '''wait random time between "min_time" and "max_time" seconds'''
    min_time = 1.5
    max_time = 4.5
    num = random.uniform(min_time, max_time)
    time.sleep(num)


def convert_time(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%d:%02d:%02d" % (hour, minutes, seconds)


def save_stores_dict_to_csv():
    df = DataFrame(list(stores_dict.items()), columns=['NAME', 'URL'])
    df.to_csv(file_name)


def response_handler(url, status):
    save_stores_dict_to_csv()


def make_http_req(url):
    sleeper()
    try:
        resp, data = http.request(url)
        if resp.status == 200:
            return data
        else:
            time.sleep(20)
            resp, data = http.request(url)
            if resp.status == 200:
                return data
            else:
                response_handler(url, resp.status)
                return None
    except (httplib2.HttpLib2Error, ConnectionError, TimeoutError):
        return None


'''------------------------------------
PRE-RUNNING METHODS - STORES LIST AND DICT INITIALIZE
------------------------------------'''


def get_stores_dict_from_file():
    if path.exists(file_name):
        with open(file_name, mode='r') as file:
            reader = csv.reader(file)
            next(reader)
            for line in reader:
                stores_dict[line[1]] = line[2]


'''------------------------------------
SHOPS FINDING SCRIPT
------------------------------------'''


def get_next_page_search_shops(url):
    global search_page_counter
    data = make_http_req(url)
    search_page_counter += 1
    if data is not None:
        return data


def add_store_to_dict(name, url):
    if name not in stores_dict:
        stores_dict[name] = url


def get_stores_from_products_page(data):
    if data is not None:
        products_a_links_in_page = SoupStrainer('a', {'class': re.compile('display-inline-block')})
        products_links_elements = BeautifulSoup(data, 'lxml', parse_only=products_a_links_in_page).findAll('a')
        for a in products_links_elements:
            try:
                product_shop_name = a.find('p', {'class': 'text-gray-lighter'}).text.strip()
                if product_shop_name not in stores_dict:
                    generic_store_url = 'https://www.etsy.com/il-en/shop/{shop_name}?ref=ss_profile'.format(
                        shop_name=product_shop_name)
                    add_store_to_dict(product_shop_name, generic_store_url)
            except (KeyError, AttributeError):
                continue


def search_for_stores_with_url(url):
    for _ in range(1, search_page_last + 1):
        full_url = url + str(search_page_counter)
        data = get_next_page_search_shops(full_url)
        get_stores_from_products_page(data)


def search_for_stores():
    global search_page_counter
    get_stores_dict_from_file()
    main_category_url_without_page_number = 'https://www.etsy.com/il-en/c/{category}?explicit=1&order=most_relevant&ref=pagination&page='.format(
        category=store_category)
    search_for_stores_with_url(main_category_url_without_page_number)
    for sub_c in sub_category:
        search_page_counter = 1
        sub_category_url_without_page_number = 'https://www.etsy.com/il-en/c/{category}/{sub_category}?explicit=1&order=most_relevant&ref=pagination&page='.format(
            category=store_category, sub_category=sub_c)
        search_for_stores_with_url(sub_category_url_without_page_number)
    save_stores_dict_to_csv()


'''------------------------------------
SCRIPT METHOD CALL
------------------------------------'''

search_for_stores()


def save_stores_dict_to_csv_as_backup():
    df = DataFrame(list(stores_dict.items()), columns=['NAME', 'URL'])
    df.to_csv('BACKUP_' + file_name)


save_stores_dict_to_csv_as_backup()