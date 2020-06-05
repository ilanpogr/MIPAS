import csv
import time

import configUtils
from crawler.shop_finder import search_for_stores
from crawler.product_downloader import download_products_for_all_stores
from image_matching_module.image_matching import ImageMatching
import controllers.ReaderWriterLockManager as LockManager
import os
import glob


downloaded_products_path = "resources/photos"


def search_stores(signal_status_search, num_stores_signal):
    multi_threading_downloaded_stores = configUtils.get_property('multi_threading_downloaded_stores')
    if os.path.exists(multi_threading_downloaded_stores):
        os.remove(multi_threading_downloaded_stores)
    user_main_category = configUtils.get_property('main_category')
    user_sub_categories = configUtils.get_property('sub_categories')
    search_for_stores(user_main_category, user_sub_categories, signal_status_search, num_stores_signal)


def download_products(signal_start_image_matching, signal_status_download, signal_current_store_name, signal_known_products, prev_known_products):
    user_stores = configUtils.get_property('store_name').split(',')
    download_products_for_all_stores(user_stores, signal_start_image_matching, signal_status_download, signal_current_store_name, signal_known_products, prev_known_products)


def get_num_of_rows_from_file(stores_dict_path):
    with open(stores_dict_path, "r") as f:
        reader = csv.reader(f, delimiter=",")
        data = list(reader)
        return len(data)


def compare_images(signal_status, total_store_number, signal_current_store_name, signal_examined_products, signal_demo_stores):
    user_photos_path = configUtils.get_property('dataset_path')
    stores_dict_path = configUtils.get_property('stores_dict')
    multi_threading_downloaded_stores = configUtils.get_property('multi_threading_downloaded_stores')
    multi_threading_end_file = configUtils.get_property('multi_threading_end_of_file')
    image_matcher = ImageMatching(user_photos_path, downloaded_products_path)
    next_store_index = 1
    need_new_store = True
    lock_manager = LockManager.LockManager()
    while True:
        multi_threading_downloaded_stores_index = next_store_index - 1

        if not os.path.exists(multi_threading_downloaded_stores):
            continue
        elif os.stat(multi_threading_downloaded_stores).st_size == 0:
            continue
        elif need_new_store:
            current_store = lock_manager.read(multi_threading_downloaded_stores, multi_threading_downloaded_stores_index)
            if current_store is None:
                continue
            current_store = current_store.strip('\n')
            if current_store == multi_threading_end_file:
                break
            else:

                # num_products = 0
                # if next_store_index == 82:
                #
                # else:
                if current_store == 'TheYaYaShoppe':
                    signal_demo_stores(1)
                num_products = get_number_products_for_store(current_store)
                # time.sleep(num_products / 1000)
                signal_examined_products.emit(num_products)
                next_store_index += 1
                need_new_store = True


def compare_images_all_stores():
    user_photos_path = configUtils.get_property('dataset_path')
    image_matcher = ImageMatching(user_photos_path, downloaded_products_path)
    image_matcher.run_matching_for_all_stores()


def get_number_products_for_store(name):
    path = "resources/photos/{0}/".format(name)
    # try:
    f = open(path + "tmp")
    return int(f.readline())
    # except FileNotFoundError:
    #     image_extensions = {"jpg", "JPG", "png", "PNG", "JPEG", "jpeg"}
    #     counter = 0
    #     for extn in image_extensions:
    #         counter += len(glob.glob1(path, "*.{0}".format(extn)))
    #     return counter
