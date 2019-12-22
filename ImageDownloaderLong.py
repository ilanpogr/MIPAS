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

stores = {}
downloaded_stores = set()

full_image_size_str = 'fullxfull.'
o_pixels = 300

store_products = set()
failed_stores = set()
failed_products = {}


'''------------------------------------
IMAGE SIZE MANIPULATION
------------------------------------'''


def resize_image_to_default_size(image_content, resp):
    img = Image.open(BytesIO(image_content))
    pxl_width, pxl_height = Image.open(BytesIO(image_content)).size
    new_width = pxl_width
    new_height = pxl_height
    if pxl_width % 10 != 0:
            new_width = int(str(pxl_width)[:-1] + '0')
    if pxl_height % 10 != 0:
            new_height = int(str(pxl_height)[:-1] + '0')
    if new_width != pxl_width or new_height != pxl_height:
        new_size = (new_width, new_height)
        img = img.resize(new_size)
        img_byte_arr = BytesIO()
        img.save(img_byte_arr,resp['content-type'].split('/')[1])
        img_byte_arr = img_byte_arr.getvalue()
        return img_byte_arr
    else:
        return image_content


def get_pxl_width_pxl_height_by_common_division_close_to_o_pixels(image_content, resp):
    image_content = resize_image_to_default_size(image_content, resp)
    pxl_width, pxl_height = Image.open(BytesIO(image_content)).size
    for i in range(2, min(pxl_width, pxl_height)+1):
        if pxl_width%i==pxl_height%i==0:
            if int(pxl_width/i) < o_pixels or int(pxl_height/i) < o_pixels:
                return (int(pxl_width/i),int(pxl_height/i))


def is_smaller_then_one_hundred(image_size):
    for i in image_size:
        if i < 100:
            return True
    return False


'''------------------------------------
TIMING AND HTTP REQUEST METHODS
------------------------------------'''


def small_sleeper():
    min_time = 0.5
    max_time = 2.5
    num = random.uniform(min_time, max_time)
    time.sleep(num)

def sleeper():
    '''wait random time between "min_time" and "max_time" seconds'''
    min_time = 1.0
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
    print('************************************************************************************')
    print('TIME RUNNING SO FAR: ' + convert_time(time.time() - start_time))
    print('************************************************************************************')
    print("CURRENT MEMORY USAGE: " + str(float(process.memory_info().rss/1000000)) + " MB")
    print('************************************************************************************')



def program_initial_print(start_time):
    print('************************************************************************************')
    print('START TIME: %s' % start_time)
    print('************************************************************************************')
    process = psutil.Process(os.getpid())
    print("INITIAL MEMORY USAGE: " + str(float(process.memory_info().rss/1000000)) + " MB")
    print('************************************************************************************')
    print()


'''------------------------------------
IMAGE DOWNLOAD SCRIPT
------------------------------------'''


def get_number_of_pages_in_store(data):
    pages_a_links = SoupStrainer('a', {'data-page':re.compile('^[0-9]*$')})
    link_elements = BeautifulSoup(data, 'lxml', parse_only=pages_a_links).findAll('span')
    pages = set()
    for span in link_elements:
        if re.match(r'^[0-9]*$', span.text) and span.text != '':
            pages.add(int(span.text))
    return max(pages, key=int)

def get_products_from_page(data):
    if data is not None:
        products_a_links_in_page = SoupStrainer('a', {'class':re.compile('listing-link')})
        products_links_elements = BeautifulSoup(data, 'lxml', parse_only=products_a_links_in_page).findAll('a')
        for a in products_links_elements:
            try:
                store_products.add(a['href'])
            except (KeyError, AttributeError):
                continue

def get_photo_to_disk(store_name, img_url):
    resp, content = http.request(img_url)
    if (resp.status == 200):
        rest = img_url.split('?version', 1)[0].split(full_image_size_str)[1]
        file_path = init_path + store_name + '/' + rest
        new_image_size = get_pxl_width_pxl_height_by_common_division_close_to_o_pixels(content, resp)
        if new_image_size is None or is_smaller_then_one_hundred(new_image_size):
            if new_image_size is not None and new_image_size[0] == new_image_size[1]:
                new_image_size = (300, 300)
                img = Image.open(BytesIO(content))
                img.thumbnail(new_image_size)
                img.save(file_path)
            else:
                with open(file_path , 'wb') as f:
                    f.write(content)
        else:
            img = Image.open(BytesIO(content))
            img.thumbnail(new_image_size)
            img.save(file_path)
    else:
            print('§§§§§§§§§§§§§§§§§§§§§§§')
            print('RESPONSE ISSUE')
            print('URL:  ' + img_url)
            pprint(resp)
            print('§§§§§§§§§§§§§§§§§§§§§§§')


def download_photos_from_pages(store_name, store_url):
    if not os.path.exists(init_path + store_name):
        os.makedirs(init_path + store_name)
    for product_page in store_products:
        data = make_http_req(product_page)
        if data is None:
            failed_products[store_url] = product_page
        products_img_in_page = SoupStrainer('img', {'data-src-delay':re.compile('75x75.')})
        products_img_elements = BeautifulSoup(data, 'lxml', parse_only=products_img_in_page).findAll('img')
        for img in products_img_elements:
            img_url = img['data-src-delay']
            img_url = img_url.replace('75x75.', full_image_size_str)
            get_photo_to_disk(store_name, img_url)



def download_all_products_from_store(store_name, store_url):
    data = make_http_req(store_url)
    if data is None:
        failed_stores.add(store_url)
        return
    get_products_from_page(data)
    num_of_pages = get_number_of_pages_in_store(data)
    page_url_sefix = '&page={page_num}#items'
    page_url = store_url + page_url_sefix.format(page_num=1)
    for i in range (2, num_of_pages + 1):
        page_url = store_url + page_url_sefix.format(page_num=i)
        data = make_http_req(page_url)
        get_products_from_page(data)
    download_photos_from_pages(store_name, store_url)


'''------------------------------------
SCRIPT METHOD CALL
------------------------------------'''


start_time = time.ctime()
program_initial_print(start_time)
start_time = time.time()
get_all_stores_urls()
get_all_downloaded_stores()
if not os.path.exists(init_path.replace('/','')):
        os.makedirs(init_path.replace('/',''))
i = 0
for name, url in stores.items():
    i += 1
    if url in downloaded_stores:
        continue
    print('------------------------------------------------------------------------------------')
    print('STORE: ' + name + ' --- ' + str(i) + '/' + str(len(stores)))
    print('------------------------------------------------------------------------------------')
    download_all_products_from_store(name, url)
    append_store_to_chache(url)
    store_products = set()
    print_output_for_debug(start_time)

