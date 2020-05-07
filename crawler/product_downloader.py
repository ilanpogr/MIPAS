import re
import httplib2
import random
from bs4 import SoupStrainer, BeautifulSoup
from pandas import DataFrame
import csv
from PIL import Image
from io import BytesIO
import os

import time
from pprint import pprint
import psutil


'''------------------------------------
GLOBAL VARS
------------------------------------'''

http = httplib2.Http()

stores_dict_file_name = 'resources/app_files/stores_dict.csv'
downloaded_stores_file_name = 'resources/app_files/downloaded_stores_dict.txt'
init_path = 'resources/photos/'
search_page_counter = 0
num_of_updates = 0

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
        resp, data = http.request(current_url)
        if resp.status == 200:
            return data
        else:
            time.sleep(20)
            print('---------???????????????????????????????????????????????????????????????????---------')
            pprint(resp)
            print('---------???????????????????????????????????????????????????????????????????---------')
            resp, data = http.request(current_url)
            if resp.status == 200:
                return data
            else:
                response_handler(current_url, resp.status)
                return None
    except (httplib2.HttpLib2Error, ConnectionError, TimeoutError):
        print('--------------EXCEPTION RAISED, CHECK YOUR INTERNET CONNECTION.--------------')
        return None


'''------------------------------------
PRE-RUNNING METHODS
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


def append_store_to_cache(current_url):
    with open(downloaded_stores_file_name, 'a') as f:
        f.write(current_url + '\n')
        

def save_products_img_url_dict(store_name):
    csv_file = init_path + store_name + '/' + store_name + '_products.csv'
    print("number of pictures: " + str(len(product_img_url_dict)))
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


def download_new_products_if_found(store_name, store_url, signal_status, status):
    global search_page_counter
    search_page_counter = 0
    data = make_http_req(store_url)
    if data is None:
        failed_updated_stores.add(store_url)
        return
    search_page_counter = 1
    current_status = status + "\nChecking if have new products"
    signal_status.emit(current_status)
    found_new_pictures = False
    found_new_images = get_products_from_updated_page(data, store_name, store_url)
    if found_new_images:
        current_status = status + "\nDownloading only new products from known store: " + store_name
        signal_status.emit(current_status)
    num_of_pages = get_number_of_pages_in_store(data)
    if num_of_pages is not None:
        page_url_sefix = '&page={page_num}#items'
        for i in range(2, num_of_pages + 1):
            if found_new_images:
                page_url = store_url + page_url_sefix.format(page_num=i)
                search_page_counter = i
                data = make_http_req(page_url)
                up_to_date = get_products_from_updated_page(data, store_name, page_url)
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
    if not os.path.exists(init_path + store_name):
        os.makedirs(init_path + store_name)
    rest = img_url.split('?version', 1)[0].split(default_image_size_str)[1]
    file_path = init_path + store_name + '/' + rest
    store_path = init_path + store_name
    with open(file_path, 'wb') as f:
        f.write(content)
    if (is_file_exist(rest, store_path)):
        product_img_url_dict[rest] = product_url
    img_url = img_url.replace(default_image_size_str, full_image_size_str)
    #     before_time = time.time()
    resp, content = http.request(img_url)
    #     print(convert_time(time.time() - before_time))
    if resp.status == 200:
        # rest = img_url.split('?version', 1)[0].split(full_image_size_str)[1]
        # full_file_name = 'highQ_' + rest
        # file_path = init_path + store_name + '/' + full_file_name
        # new_image_size = get_pxl_width_pxl_height_by_common_division_close_to_o_pixels(content, resp)
        # if new_image_size is None or is_smaller_then_min_size(new_image_size):
        #     if new_image_size is not None and new_image_size[0] == new_image_size[1]:
        #         new_image_size = (o_pixels, o_pixels)
        #         img = Image.open(BytesIO(content))
        #         img.thumbnail(new_image_size)
        #         img.save(file_path)
        #         if (is_file_exist(full_file_name, store_path)):
        #             product_img_url_dict[full_file_name] = product_url
        #     else:
        #         with open(file_path, 'wb') as f:
        #             f.write(content)
        #         if (is_file_exist(full_file_name, store_path)):
        #             product_img_url_dict[full_file_name] = product_url
        # else:
        #     img = Image.open(BytesIO(content))
        #     img.thumbnail(new_image_size)
        #     img.save(file_path)
        #     if (is_file_exist(full_file_name, store_path)):
        #         product_img_url_dict[full_file_name] = product_url
        pass
    else:
        print('§§§§§§§§§§§§§§§§§§§§§§§')
        print('RESPONSE ISSUE')
        print('URL:  ' + img_url)
        pprint(resp)
        print('§§§§§§§§§§§§§§§§§§§§§§§')


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


def download_all_products_from_store(store_name, store_url, signal_status, status):
    global search_page_counter
    search_page_counter = 0
    data = make_http_req(store_url)
    if data is None:
        failed_stores.add(store_url)
        return
    current_status = status + "\nDownloading page #1"
    signal_status.emit(current_status)
    search_page_counter = 1
    get_products_from_page(data, store_name, store_url)
    num_of_pages = get_number_of_pages_in_store(data)
    got_data = False
    if num_of_pages is not None:
        page_url_sefix = '&page={page_num}#items'
        for i in range(2, num_of_pages + 1):
            current_status = status + "\nDownloading page #" + str(i)
            signal_status.emit(current_status)
            page_url = store_url + page_url_sefix.format(page_num=i)
            search_page_counter = i
            data = make_http_req(page_url)
            data_res = get_products_from_page(data, store_name, page_url)
            if (not got_data):
                got_data = data_res
    if got_data:
        save_products_img_url_dict(store_name)


'''------------------------------------
MAIN METHOD CALL
------------------------------------'''


def download_products_for_all_stores(signal_process, signal_status):
    global store_products, num_of_updates
    start_time = time.ctime()
    program_initial_print(start_time)
    start_time = time.time()
    get_all_stores_urls()
    if not os.path.exists(downloaded_stores_file_name):
        with open(downloaded_stores_file_name, "w") as file:
            pass
    else:
        get_all_downloaded_stores()
    if not os.path.exists(init_path):
        os.makedirs(init_path)
    i = 0
    for name, url in stores.items():
        i += 1
        current_status = str(i) + "/" + str(len(stores)) + "\nDownloading products for store: " + name
        signal_status.emit(current_status)  # signal task
        if url in downloaded_stores:
            url = url + '&sort_order=date_desc'
            # print('************************************************************************************')
            # print('STORE UPDATE: ' + name + ' --- ' + str(i) + '/' + str(len(stores)))
            # print('************************************************************************************')
            #
            # download_new_products_if_found(name, url, signal_status, current_status)
            # save_products_img_url_dict(name)
            # print('\t\t\tNUMBER OF NEW PRODUCTS FOUND: ' + str(num_of_updates))
            # print('************************************************************************************')
            # print_output_for_debug(start_time)
            # num_of_updates = 0
            time.sleep(0.001)  # todo - remove sleep and uncomment above lines
            signal_process.emit(i/len(stores) * 100)
        else:
            if i == 1:
                print('************************************************************************************')
                print('STORE: ' + name + ' --- ' + str(i) + '/' + str(len(stores)))
                print('************************************************************************************')
                download_all_products_from_store(name, url, signal_status, current_status)
                append_store_to_cache(url)
                print_output_for_debug(start_time)
            time.sleep(0.001)   # todo - remove sleep and uncomment above lines
            signal_process.emit(i/len(stores) * 100)

        store_products = set()
        product_img_url_dict.clear()
