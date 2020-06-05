# import httplib2
import urllib.request
import urllib.error
from bs4 import SoupStrainer, BeautifulSoup
from pandas import DataFrame
import csv
from os import path

import time
import re
import random


'''------------------------------------
GLOBAL VARS
------------------------------------'''


# http = httplib2.Http(".cache")
http = urllib.request

search_page_counter = 1
search_page_last = 250
stores_dict = {}
store_category = ''
sub_category = []
file_name = 'resources/app_files/stores_dict.csv'
search_iteration_counter = 0


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


def save_stores_dict_to_csv_as_backup():
    df = DataFrame(list(stores_dict.items()), columns=['NAME', 'URL'])
    original_file_name = 'resources/app_files/stores_dict.csv'
    backup_file_name = 'BACKUP_' + original_file_name.split('/')[-1]
    path = '/'.join(original_file_name.split('/')[:-1]) + '/' + backup_file_name
    df.to_csv(path)


def response_handler(url, status):
    save_stores_dict_to_csv()


def make_http_req(url):
    sleeper()
    try:
        # resp, data = http.request(url, "GET")
        res = http.urlopen(url)
        resp = res.code
        data = res.read()
        # if resp.status == 200:
        if resp == 200:
            return data
        else:
            time.sleep(20)
            # resp, data = http.request(url)
            # if resp.status == 200:
            res = http.urlopen(url)
            resp = res.code
            data = res.read()
            if resp == 200:
                return data
            else:
                response_handler(url, resp)
                return None
    # except (httplib2.HttpLib2Error, ConnectionError, TimeoutError):
    except (urllib.error.HTTPError, urllib.error.URLError, urllib.error.ContentTooShortError, ConnectionError, TimeoutError):
        return None
    except OSError:
        print("OS Exception...")
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


def get_stores_from_products_page(data, num_stores_signal, demo_num):
    for _ in range(0, 90):
        demo_num += random.randint(30, 40)
        time.sleep(0.01)
        num_stores_signal.emit(demo_num)
    return demo_num


def search_for_stores_with_url(url, num_stores_signal, demo_num):
    data = 1
    return get_stores_from_products_page(data, num_stores_signal, demo_num)


def search_for_stores(user_store_category, user_sub_category, signal_status_search, num_stores_signal):
    global search_page_counter, store_category, sub_category
    demo_num = 0
    store_category = user_store_category
    sub_category = user_sub_category.split(",")

    signal_status_search.emit("Main Category: " + store_category)
    get_stores_dict_from_file()
    num_stores_signal.emit(len(stores_dict))

    main_category_url_without_page_number = 'https://www.etsy.com/il-en/c/{category}?explicit=1&order=most_relevant&ref=pagination&page='.format(
        category=store_category)
    demo_num = search_for_stores_with_url(main_category_url_without_page_number, num_stores_signal, demo_num)

    for sub_c in sub_category:
        signal_status_search.emit("Subcategory: " + sub_c)
        search_page_counter = 1
        sub_category_url_without_page_number = 'https://www.etsy.com/il-en/c/{category}/{sub_category}?explicit=1&order=most_relevant&ref=pagination&page='.format(
            category=store_category, sub_category=sub_c)
        current_status = "Searching by store's sub-category: " + sub_c
        demo_num = search_for_stores_with_url(sub_category_url_without_page_number, num_stores_signal, demo_num)

    while demo_num < 16438:
        demo_num += random.randint(30, 40)
        time.sleep(0.01)
        if demo_num < 16438:
            num_stores_signal.emit(demo_num)
    num_stores_signal.emit(16438)

    # save_stores_dict_to_csv()
    # save_stores_dict_to_csv_as_backup()

