import csv
import time

import configUtils
from crawler.shop_finder import search_for_stores
from crawler.product_downloader import download_products_for_all_stores
from image_matching_module.image_matching import ImageMatching
import controllers.ReaderWriterLockManager as LockManager
import os


downloaded_products_path = "resources/photos"


def search_stores(signal_status_search):
    multi_threading_downloaded_stores = configUtils.get_property('multi_threading_downloaded_stores')
    if os.path.exists(multi_threading_downloaded_stores):
        os.remove(multi_threading_downloaded_stores)
    user_main_category = configUtils.get_property('main_category')
    user_sub_categories = configUtils.get_property('sub_categories')
    search_for_stores(user_main_category, user_sub_categories, signal_status_search)


def download_products(signal_start_image_matching, signal_status_download, signal_finished):
    user_stores = configUtils.get_property('store_name').split(',')
    download_products_for_all_stores(user_stores, signal_start_image_matching, signal_status_download, signal_finished)


def get_num_of_rows_from_file(stores_dict_path):
    with open(stores_dict_path, "r") as f:
        reader = csv.reader(f, delimiter=",")
        data = list(reader)
        return len(data)


def compare_images(signal_status, total_store_number):
    user_photos_path = configUtils.get_property('dataset_path')
    stores_dict_path = configUtils.get_property('stores_dict')
    multi_threading_downloaded_stores = configUtils.get_property('multi_threading_downloaded_stores')
    multi_threading_end_file = configUtils.get_property('multi_threading_end_of_file')
    image_matcher = ImageMatching(user_photos_path, downloaded_products_path)
    next_store_index = 1

    lock_manager = LockManager.LockManager()
    while True:
        multi_threading_downloaded_stores_index = next_store_index - 1
        if next_store_index > 2:  # todo - whole if condition with if and else, only for ---- DEMO
            if next_store_index <= total_store_number:
                time.sleep(0.001)
                signal_status.emit(str(next_store_index))
                next_store_index += 1
            else:
                break

        if not os.path.exists(multi_threading_downloaded_stores):
            continue
        elif os.stat(multi_threading_downloaded_stores).st_size == 0:
            continue
        else:
            current_store = lock_manager.read(multi_threading_downloaded_stores, multi_threading_downloaded_stores_index)
            if current_store is None:
                continue
            current_store = current_store.strip('\n')
            if current_store == multi_threading_end_file:
                continue  # todo - only for demo. change back to break.
                # break
            else:
                store_path = "resources/photos/" + current_store
            signal_status.emit(str(next_store_index))

            print("starting to compare for store:" + str(next_store_index))
            image_matcher.run_matching_for_store(None, store_path)
            next_store_index += 1


def compare_images_all_stores():
    user_photos_path = configUtils.get_property('dataset_path')
    image_matcher = ImageMatching(user_photos_path, downloaded_products_path)
    image_matcher.run_matching_for_all_stores()
