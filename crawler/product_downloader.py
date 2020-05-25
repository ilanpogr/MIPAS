import configUtils
import controllers.ReaderWriterLockManager as LockManager

import re
import httplib2
import random
from bs4 import SoupStrainer, BeautifulSoup
from pandas import DataFrame
import csv
from PIL import Image
from io import BytesIO
import os
import glob

import time
from pprint import pprint
import psutil


'''------------------------------------
GLOBAL VARS
------------------------------------'''

http = httplib2.Http(".cache")

stores_dict_file_name = 'resources/app_files/stores_dict.csv'
downloaded_stores_file_name = 'resources/app_files/downloaded_stores_dict.txt'
init_path = 'resources/photos/'
search_page_counter = 0
num_of_updates = 0
known_products = 0
signal_num_of_products = None

multi_threading_downloaded_stores = ""
multi_threading_end_of_file = ""
lock_manager = LockManager.LockManager()


stores = {}
downloaded_stores = set()

# DO NOT CHANGE THOSE VARS IF NOT EDITING THE CODE
full_image_size_str = 'fullxfull.'
# high_image_size_str = '1360x1080.'
default_image_size_str = '340x270.'
o_pixels = 1000
min_image_size = 800

store_products = set()
product_img_url_dict = {}
failed_stores = set()
failed_updated_stores = set()
failed_products = {}


'''------------------------------------
TIMING AND HTTP REQUEST METHODS
------------------------------------'''


def sleeper():
    # wait random time between "min_time" and "max_time" seconds
    min_time = 1.0
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


def response_handler(current_url, status):
    print("\nDEBUG: ERROR WITH PAGE REQUEST: " + current_url)
    print("\tdue to response status: " + str(status))
    if search_page_counter == 0:
        print("\nREASON: STORE NOT FOUND.")
    else:
        print("\nCURRENT PAGE: " + str(search_page_counter))


def make_http_req(current_url):
    sleeper()
    try:
        resp, data = http.request(current_url, "GET")
        if resp.status == 200:
            return data
        else:
            time.sleep(20)
            print('---------???????????????????????????????????????????????????????????????????---------')
            pprint(resp)
            print('---------???????????????????????????????????????????????????????????????????---------')
            resp, data = http.request(current_url, "GET")
            if resp.status == 200:
                return data
            else:
                response_handler(current_url, resp.status)
                return None
    except (httplib2.HttpLib2Error, ConnectionError, TimeoutError):
        print('--------------EXCEPTION RAISED, CHECK YOUR INTERNET CONNECTION.--------------')
        return None
    except OSError:
        print('--------------OS EXCEPTION RAISED..............................--------------')
        return None


'''------------------------------------
PRE-RUNNING METHODS
------------------------------------'''


def get_all_stores_urls():
    global stores
    stores = {}
    with open(stores_dict_file_name, "r") as f:
        reader = csv.reader(f, delimiter="\t")
        next(reader, None)
        for _, line in enumerate(reader):
            slots = line[0].split(',')
            url = slots[-1]
            name = slots[1]
            stores[name] = url


def get_all_downloaded_stores():
    with open(downloaded_stores_file_name, "r") as f:
        lines = f.readlines()
        for line in lines:
            line = line.replace('\n', '')
            downloaded_stores.add(line)


'''------------------------------------
PRINT AND DEBUG METHODS
------------------------------------'''


def print_output_for_debug(current_start_time):
    process = psutil.Process(os.getpid())
    print('------------------------------------------------------------------------------------')    
    print('CURRENT RUNTIME: ' + convert_time(time.time() - current_start_time))
    print('------------------------------------------------------------------------------------')    
    print("CURRENT MEMORY USAGE: " + str(float(process.memory_info().rss/1000000)) + " MB")
    print('------------------------------------------------------------------------------------') 


def program_initial_print(current_start_time):
    print('------------------------------------------------------------------------------------')
    print('START TIME: %s' % current_start_time)
    print('------------------------------------------------------------------------------------')
    process = psutil.Process(os.getpid())
    print("INITIAL MEMORY USAGE: " + str(float(process.memory_info().rss/1000000)) + " MB")
    print('------------------------------------------------------------------------------------')
    print()


'''------------------------------------
PRODUCTS DOWNLOADER FROM STORES
------------------------------------'''


def write_number_products(name):
    image_extensions = {"jpg", "JPG", "png", "PNG", "JPEG", "jpeg"}
    path = "resources/photos/{0}/".format(name)
    counter = 0
    for extn in image_extensions:
        counter += len(glob.glob1(path, "*.{0}".format(extn)))
    path += "num_products"
    with open(path, 'w') as f:
        f.write(str(counter))


def append_store_to_cache(current_url):
    with open(downloaded_stores_file_name, 'a') as f:
        f.write(current_url + '\n')


def append_store_to_multi_threading(store_name):
    lock_manager.write(multi_threading_downloaded_stores, store_name)
        

def save_products_img_url_dict(store_name):
    csv_file = init_path + store_name + '/' + store_name + '_products.csv'
    df = DataFrame(product_img_url_dict.items())
    if not os.path.isfile(csv_file):
        df.to_csv(csv_file, index=False, header=['File', 'URL'])
    else:
        df.to_csv(csv_file, mode='a', index=False, header=False)


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
        img.save(img_byte_arr, resp['content-type'].split('/')[1])
        img_byte_arr = img_byte_arr.getvalue()
        return img_byte_arr
    else:
        return image_content


def get_pxl_width_pxl_height_by_common_division_close_to_o_pixels(image_content, resp):
    image_content = resize_image_to_default_size(image_content, resp)
    pxl_width, pxl_height = Image.open(BytesIO(image_content)).size
    for i in range(2, min(pxl_width, pxl_height) + 1):
        if pxl_width % i == pxl_height % i == 0:
            if int(pxl_width / i) < o_pixels or int(pxl_height / i) < o_pixels:
                return int(pxl_width / i), int(pxl_height / i)


def is_smaller_then_min_size(image_size):
    for i in image_size:
        if i < min_image_size:
            return True
    return False


def is_file_exist(file_name, path):
    full_path = path + '/' + file_name
    if os.path.isfile(full_path):
        return True
    else:
        return False


def get_products_from_updated_page(data, store_name, current_url):
    if data is not None:
        global num_of_updates
        store_path = init_path + store_name
        new_images = False
        products_a_links_in_page = SoupStrainer('a', {'class': re.compile('listing-link')})
        products_links_elements = BeautifulSoup(data, 'html.parser', parse_only=products_a_links_in_page).findAll('a')
        for a in products_links_elements:
            img = a.find('img')
            pruduct_url = ''
            if img is not None:
                try:
                    resp, data = http.request(img['src'])
                    if resp.status == 200:
                        file_name = img['src'].split('?version', 1)[0].split(default_image_size_str)[1]
                        if not is_file_exist(file_name, store_path):
                            product_url = a['href']
                            download_image(resp, data, store_name, img['src'], product_url)
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
                                product_url = a['href']
                                download_image(resp, data, store_name, img['data-src'], product_url)
                                new_images = True
                                num_of_updates += 1 
                        else:
                            failed_products[store_name + ',' + current_url] = img['data-src']
                    except (httplib2.HttpLib2Error, ConnectionError, TimeoutError):
                        failed_products[store_name + ',' + current_url] = img['data-src']
                    except(KeyError, AttributeError):
                        failed_products[store_name + ',' + current_url] = a['href']
        return new_images
    else:
        return 0


def download_new_products_if_found(store_name, store_url):
    global search_page_counter
    write_number_products(store_name)
    search_page_counter = 0
    data = make_http_req(store_url)
    if data is None:
        failed_updated_stores.add(store_url)
        return
    search_page_counter = 1
    found_new_images = get_products_from_updated_page(data, store_name, store_url)
    if found_new_images:
        num_of_pages = get_number_of_pages_in_store(data)
        if num_of_pages is not None:
            page_url_sefix = '&page={page_num}#items'
            for i in range(2, num_of_pages + 1):
                if found_new_images:
                    page_url = store_url + page_url_sefix.format(page_num=i)
                    search_page_counter = i
                    data = make_http_req(page_url)
                    found_new_images = get_products_from_updated_page(data, store_name, page_url)
                else:
                    return
    save_products_img_url_dict(store_name)


def get_number_of_pages_in_store(data):
    pages_a_links = SoupStrainer('a', {'data-page': re.compile('^[0-9]*$')})
    link_elements = BeautifulSoup(data, 'html.parser', parse_only=pages_a_links).findAll('span')
    pages = set()
    for span in link_elements:
        if re.match(r'^[0-9]*$', span.text) and span.text != '':
            pages.add(int(span.text))
    try:
        return max(pages, key=int)
    except ValueError:
        return None


def download_image(resp, content, store_name, img_url, product_url):
    global known_products
    if not os.path.exists(init_path + store_name):
        os.makedirs(init_path + store_name)
    rest = img_url.split('?version', 1)[0].split(default_image_size_str)[1]
    file_path = init_path + store_name + '/' + rest
    store_path = init_path + store_name
    with open(file_path, 'wb') as f:
        f.write(content)
    if is_file_exist(rest, store_path):
        if rest not in product_img_url_dict:
            product_img_url_dict[rest] = product_url
            signal_num_of_products.emit(known_products + 1)
            known_products += 1
    # img_url = img_url.replace(default_image_size_str, full_image_size_str)
    #     before_time = time.time()
    # resp, content = http.request(img_url)
    #     print(convert_time(time.time() - before_time))
    # if resp.status == 200:
    #     rest = img_url.split('?version', 1)[0].split(full_image_size_str)[1]
    #     full_file_name = 'highQ_' + rest
    #     file_path = init_path + store_name + '/' + full_file_name
    #     new_image_size = get_pxl_width_pxl_height_by_common_division_close_to_o_pixels(content, resp)
    #     if new_image_size is None or is_smaller_then_min_size(new_image_size):
    #         if new_image_size is not None and new_image_size[0] == new_image_size[1]:
    #             new_image_size = (o_pixels, o_pixels)
    #             img = Image.open(BytesIO(content))
    #             img.thumbnail(new_image_size)
    #             img.save(file_path)
    #             if (is_file_exist(full_file_name, store_path)):
    #                 product_img_url_dict[full_file_name] = product_url
    #         else:
    #             with open(file_path, 'wb') as f:
    #                 f.write(content)
    #             if (is_file_exist(full_file_name, store_path)):
    #                 product_img_url_dict[full_file_name] = product_url
    #     else:
    #         img = Image.open(BytesIO(content))
    #         img.thumbnail(new_image_size)
    #         img.save(file_path)
    #         if (is_file_exist(full_file_name, store_path)):
    #             product_img_url_dict[full_file_name] = product_url
    # else:
    #     print('§§§§§§§§§§§§§§§§§§§§§§§')
    #     print('RESPONSE ISSUE')
    #     print('URL:  ' + img_url)
    #     pprint(resp)
    #     print('§§§§§§§§§§§§§§§§§§§§§§§')


def get_products_from_page(data, store_name, current_url):
    got_data = False;
    if data is not None:
        got_data = True;
        products_a_links_in_page = SoupStrainer('a', {'class': re.compile('listing-link')})
        products_links_elements = BeautifulSoup(data, 'html.parser', parse_only=products_a_links_in_page).findAll('a')
        for a in products_links_elements:
            img = a.find('img')
            pruduct_url = ''
            if img is not None:
                try:
                    resp, data = http.request(img['src'])
                    if resp.status == 200:
                        product_url = a['href']
                        download_image(resp, data, store_name, img['src'], product_url)
                    else:
                        failed_products[store_name + ',' + current_url] = img['src']
                except (httplib2.HttpLib2Error, ConnectionError, TimeoutError):
                    failed_products[store_name + ',' + current_url] = img['src']
                except(KeyError, AttributeError):
                    try:
                        resp, data = http.request(img['data-src'])
                        if resp.status == 200:
                            product_url = a['href']
                            download_image(resp, data, store_name, img['data-src'], product_url)
                        else:
                            failed_products[store_name + ',' + current_url] = img['data-src']
                    except (httplib2.HttpLib2Error, ConnectionError, TimeoutError):
                        failed_products[store_name + ',' + current_url] = img['data-src']
                    except(KeyError, AttributeError):
                        failed_products[store_name + ',' + current_url] = a['href']
    return got_data


def download_all_products_from_store(store_name, store_url):
    global search_page_counter
    search_page_counter = 0
    data = make_http_req(store_url)
    if data is None:
        failed_stores.add(store_url)
        return
    search_page_counter = 1
    got_data = get_products_from_page(data, store_name, store_url)
    num_of_pages = get_number_of_pages_in_store(data)
    if num_of_pages is not None:
        page_url_sefix = '&page={page_num}#items'
        for i in range(2, num_of_pages + 1):
            page_url = store_url + page_url_sefix.format(page_num=i)
            search_page_counter = i
            data = make_http_req(page_url)
            data_res = get_products_from_page(data, store_name, page_url)
            if not got_data:
                got_data = data_res
    if got_data:
        append_store_to_multi_threading(store_name)
        save_products_img_url_dict(store_name)


'''------------------------------------
MAIN METHOD CALL
------------------------------------'''


def download_products_for_all_stores(user_stores, signal_start_image_matching, signal_status_download, signal_current_store_name, signal_known_products, prev_known_products):
    global store_products, num_of_updates, multi_threading_downloaded_stores, multi_threading_end_of_file, signal_num_of_products, known_products
    signal_num_of_products = signal_known_products
    known_products = prev_known_products
    multi_threading_downloaded_stores = configUtils.get_property('multi_threading_downloaded_stores')
    multi_threading_end_of_file = configUtils.get_property('multi_threading_end_of_file')
    start_time = time.ctime()
    program_initial_print(start_time)
    start_time = time.time()
    get_all_stores_urls()
    if not os.path.exists(multi_threading_downloaded_stores):
        with open(multi_threading_downloaded_stores, "w") as file:
            pass
    if not os.path.exists(downloaded_stores_file_name):
        with open(downloaded_stores_file_name, "w") as file:
            pass
    else:
        get_all_downloaded_stores()
    if not os.path.exists(init_path):
        os.makedirs(init_path)
    i = 0
    signal_status_download.emit("1/" + str(len(stores.items())))
    for name, url in stores.items():
        i += 1
        signal_current_store_name.emit(name)
        if i == 2:
            signal_start_image_matching.emit()
        if name not in user_stores:
            if url in downloaded_stores:
                url = url + '&sort_order=date_desc'
                print('************************************************************************************')
                print('STORE UPDATE: ' + name + ' --- ' + str(i) + '/' + str(len(stores)))
                print('************************************************************************************')

                download_new_products_if_found(name, url)
                save_products_img_url_dict(name)
                print('\t\t\tNUMBER OF NEW PRODUCTS FOUND: ' + str(num_of_updates))
                print('************************************************************************************')
                print_output_for_debug(start_time)

                if num_of_updates != 0:
                    append_store_to_multi_threading(name)
                    num_of_updates = 0

            else:
                if i < 6:  # todo - remove
                    print('************************************************************************************')
                    print('STORE: ' + name + ' --- ' + str(i) + '/' + str(len(stores)))
                    print('************************************************************************************')
                    download_all_products_from_store(name, url)
                    append_store_to_cache(url)
                    print_output_for_debug(start_time)
            store_products = set()
            product_img_url_dict.clear()
    append_store_to_multi_threading(multi_threading_end_of_file)
