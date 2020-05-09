import csv

import configUtils
from crawler.shop_finder import search_for_stores
from crawler.product_downloader import download_products_for_all_stores
from image_matching_module.image_matching import ImageMatching
import controllers.ReaderWriterLockManager as LockManager
import os


downloaded_products_path = "resources/photos"


def search_stores(signal_process, signal_status, signal_task):
    multi_threading_downloaded_stores = configUtils.get_property('multi_threading_downloaded_stores')
    if os.path.exists(multi_threading_downloaded_stores):
        os.remove(multi_threading_downloaded_stores)
    signal_task.emit("Searching Relevant Stores In Platform")
    user_main_category = configUtils.get_property('main_category')
    user_sub_categories = configUtils.get_property('sub_categories')
    search_for_stores(user_main_category, user_sub_categories, signal_process, signal_status)


def download_products(signal_process, signal_status, signal_task, signal_start_image_matching):
    signal_task.emit("Download Products From Stores")
    user_stores = configUtils.get_property('store_name').split(',')
    download_products_for_all_stores(signal_process, signal_status, user_stores, signal_start_image_matching)


def get_num_of_rows_from_file(stores_dict_path):
    with open(stores_dict_path, "r") as f:
        reader = csv.reader(f, delimiter=",")
        data = list(reader)
        return len(data)


def compare_images(signal_process, signal_status, signal_task):
    user_photos_path = configUtils.get_property('dataset_path')
    stores_dict_path = configUtils.get_property('stores_dict')
    total_num_of_stores = get_num_of_rows_from_file(stores_dict_path)
    multi_threading_downloaded_stores = configUtils.get_property('multi_threading_downloaded_stores')
    multi_threading_end_file = configUtils.get_property('multi_threading_end_of_file')
    image_matcher = ImageMatching(user_photos_path, downloaded_products_path)
    next_store_index = 0
    lock_manager = LockManager.LockManager()
    done = False
    while not done:
        if not os.path.exists(multi_threading_downloaded_stores):
            continue
        elif os.stat(multi_threading_downloaded_stores).st_size == 0:
            continue
        else:
            current_store = lock_manager.read(multi_threading_downloaded_stores, next_store_index)
            if current_store == multi_threading_end_file:
                done = True
            elif current_store is None:
                continue
            else:  # todo - implement correctly image matching in multi-threading
                signal_task.emit("Comparing Images For Store: " + current_store +
                                 " --> " + str(next_store_index + 1) + "/" + str(total_num_of_stores))
                image_matcher.run_matching_for_all_stores(signal_process, signal_status)
                next_store_index += 1
