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


http = httplib2.Http()

search_page_counter = 1
search_page_last = 250
stores_dict = {}
store_category = ''
sub_category = []
file_name = 'resources/app_files/stores_dict.csv'
search_iteration_counter = 0
pages_counter = 0


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
    df.to_csv('BACKUP_' + file_name)


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


def search_for_stores_with_url(url, signal_process, signal_status, status):
    global pages_counter, search_iteration_counter
    search_iteration_counter += 1
    for _ in range(1, search_page_last + 1):
        current_status = status + " - " + str(_) + "/" + str(search_page_last)
        signal_status.emit(current_status)  # signal task
        full_url = url + str(search_page_counter)
        time.sleep(0.005)  # todo - comment sleep and uncomment next lines ---- DEMO
        # data = get_next_page_search_shops(full_url)
        # get_stores_from_products_page(data)
        pages_counter += 1
        num_of_categories = len(sub_category) + 1  # 1 - main category
        signal_process.emit((pages_counter/(num_of_categories * search_page_last)) * 100)


def search_for_stores(user_store_category, user_sub_category, signal_process, signal_status):
    global search_page_counter, store_category, sub_category
    current_status = "Searching by store's main category: " + store_category
    signal_status.emit(current_status)  # signal task
    store_category = user_store_category
    sub_category = user_sub_category.split(",")
    get_stores_dict_from_file()
    main_category_url_without_page_number = 'https://www.etsy.com/il-en/c/{category}?explicit=1&order=most_relevant&ref=pagination&page='.format(
        category=store_category)
    search_for_stores_with_url(main_category_url_without_page_number, signal_process, signal_status, current_status)
    for sub_c in sub_category:
        search_page_counter = 1
        sub_category_url_without_page_number = 'https://www.etsy.com/il-en/c/{category}/{sub_category}?explicit=1&order=most_relevant&ref=pagination&page='.format(
            category=store_category, sub_category=sub_c)
        current_status = "Searching by store's sub-category: " + sub_c
        signal_status.emit(current_status)  # signal task
        search_for_stores_with_url(sub_category_url_without_page_number, signal_process, signal_status, current_status)
    # save_stores_dict_to_csv() # todo - uncomment next lines  ---- DEMO
    # save_stores_dict_to_csv_as_backup()

