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
num_of_updates = 0

stores = {}
downloaded_stores = set()

full_image_size_str = 'fullxfull.'
# high_image_size_str = '1360x1080.'
default_image_size_str = '340x270.'
o_pixels = 1000
min_image_size = 800

store_products = set()
failed_stores = set()
failed_updated_stores = set()
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
    if search_page_counter == 0:
        print("\nREASON: STORE NOT FOUND.")
    else:
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
IMAGE MANUPULATION
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
            
            
def is_smaller_then_min_size(image_size):
    for i in image_size:
        if i < min_image_size:
            return True
    return False
        
'''------------------------------------
NEW IMAGES - DOWNLOAD
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
    global search_page_counter
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
UPDATED IMAGES - DOWNLOAD
------------------------------------'''


def is_file_exist(file_name, path):
    full_path = path + '/' + file_name
    if os.path.isfile(full_path):
        return True
    else:
        return False


def get_products_from_updated_page(data, store_name, current_url):
    if data is not None:
        store_path = init_path + store_name
        new_images = False
        products_a_links_in_page = SoupStrainer('a', {'class':re.compile('listing-link')})
        products_links_elements = BeautifulSoup(data, 'lxml', parse_only=products_a_links_in_page).findAll('a')
        for a in products_links_elements:
            img = a.find('img')
            if img is not None:
                try:
                    resp, data = http.request(img['src'])
                    if resp.status == 200:
                        file_name = img['src'].split('?version', 1)[0].split(default_image_size_str)[1]
                        if not is_file_exist(file_name, store_path):
                            download_image(resp, data, store_name, img['src'])
                            new_images = True
                            num_of_updates += 1
                    else:
                        failed_products[store_name + ',' + current_url] = img['src']
                except (httplib2.HttpLib2Error, ConnectionError, TimeoutError):
                    failed_products[store_name + ',' + current_url] = img['src']
                except(KeyError, AttributeError):
                    try:
                        resp, data = http.request(img['data-src'])
                        if resp.status == 200:
                            file_name = img['src'].split('?version', 1)[0].split(default_image_size_str)[1]
                            if not is_file_exist(file_name, store_path):
                                download_image(resp, data, store_name, img['data-src'])
                                new_images = True
                                num_of_updates += 1 
                        else:
                            failed_products[store_name + ',' + current_url] = img['data-src']
                    except (httplib2.HttpLib2Error, ConnectionError, TimeoutError):
                        failed_products[store_name + ',' + current_url] = img['data-src']
                    except(KeyError, AttributeError):
                        failed_products[store_name + ',' + current_url] = a['href']
        return new_images


def download_new_products_if_found(store_name, store_url):
    global search_page_counter
    search_page_counter = 0
    data = make_http_req(store_url)
    if data is None:
        failed_updated_stores.add(store_url)
        return
    search_page_counter = 1
    found_new_pictures = False
    found_new_images = get_products_from_updated_page(data, store_name, store_url)
    num_of_pages = get_number_of_pages_in_store(data)
    if num_of_pages is not None:
        page_url_sefix = '&page={page_num}#items'
        for i in range (2, num_of_pages + 1):
            if found_new_images:
                page_url = store_url + page_url_sefix.format(page_num=i)
                search_page_counter = i
                data = make_http_req(page_url)
                up_to_date = get_products_from_updated_page(data, store_name, page_url)
            else:
                return
            


'''------------------------------------
MAIN METHOD --> NEEDS TO BE WRAPPED
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
        url = url + '&sort_order=date_desc'
        print('************************************************************************************')
        print('STORE UPDATE: ' + name + ' --- ' + str(i) + '/' + str(len(stores)))
        print('************************************************************************************')
        
        download_new_products_if_found(name, url)
        
        print('\t\t\tNUMBER OF NEW PRODUCTS FOUND: ' + str(num_of_updates))
        print('************************************************************************************')
        print_output_for_debug(start_time)
        num_of_updates = 0
        continue
    else:
        print('************************************************************************************')
        print('STORE: ' + name + ' --- ' + str(i) + '/' + str(len(stores)))
        print('************************************************************************************')
        download_all_products_from_store(name, url)
        append_store_to_chache(url)
        print_output_for_debug(start_time)
    store_products = set()
