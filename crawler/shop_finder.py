import httplib2
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


http = httplib2.Http(".cache")

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
        resp, data = http.request(url, "GET")
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


def get_stores_from_products_page(data, num_stores_signal):
    if data is not None:
        products_a_links_in_page = SoupStrainer('a', {'class': re.compile('display-inline-block')})
        products_links_elements = BeautifulSoup(data, 'html.parser', parse_only=products_a_links_in_page).findAll('a')
        for a in products_links_elements:
            try:
                product_shop_name = a.find('p', {'class': 'text-gray-lighter'}).text.strip()
                if product_shop_name not in stores_dict:
                    generic_store_url = 'https://www.etsy.com/il-en/shop/{shop_name}?ref=ss_profile'.format(
                        shop_name=product_shop_name)
                    add_store_to_dict(product_shop_name, generic_store_url)
                    num_stores_signal.emit(len(stores_dict))
            except (KeyError, AttributeError):
                continue


def search_for_stores_with_url(url, num_stores_signal):
    global search_iteration_counter

    search_iteration_counter += 1
    # for _ in range(1, search_page_last + 1):  # todo - remove comment and delete next line
    for _ in range(1, 10):
        full_url = url + str(search_page_counter)
        data = get_next_page_search_shops(full_url)
        get_stores_from_products_page(data, num_stores_signal)


def search_for_stores(user_store_category, user_sub_category, signal_status_search, num_stores_signal):
    global search_page_counter, store_category, sub_category
    store_category = user_store_category
    sub_category = user_sub_category.split(",")

    signal_status_search.emit("Main Category: " + store_category)
    get_stores_dict_from_file()
    num_stores_signal.emit(len(stores_dict))

    main_category_url_without_page_number = 'https://www.etsy.com/il-en/c/{category}?explicit=1&order=most_relevant&ref=pagination&page='.format(
        category=store_category)
    search_for_stores_with_url(main_category_url_without_page_number, num_stores_signal)

    for sub_c in sub_category:
        signal_status_search.emit("Subcategory: " + sub_c)
        search_page_counter = 1
        sub_category_url_without_page_number = 'https://www.etsy.com/il-en/c/{category}/{sub_category}?explicit=1&order=most_relevant&ref=pagination&page='.format(
            category=store_category, sub_category=sub_c)
        current_status = "Searching by store's sub-category: " + sub_c
        # search_for_stores_with_url(sub_category_url_without_page_number, num_stores_signal) #  todo - uncomment

    save_stores_dict_to_csv()
    save_stores_dict_to_csv_as_backup()

