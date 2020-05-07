import configUtils
from crawler.shop_finder import search_for_stores
from crawler.product_downloader import download_products_for_all_stores
from image_matching_module.image_matching import ImageMatching

downloaded_products_path = "resources/photos"


def search_stores(signal_process, signal_status):
    user_main_category = configUtils.get_property('main_category')
    user_sub_categories = configUtils.get_property('sub_categories')
    search_for_stores(user_main_category, user_sub_categories, signal_process, signal_status)


def download_products(signal_process, signal_status):
    download_products_for_all_stores(signal_process, signal_status)


def compare_images(signal_process, signal_status):
    user_photos_path = configUtils.get_property('dataset_path')
    image_matcher = ImageMatching(user_photos_path, downloaded_products_path)
    image_matcher.run_matching_for_all_stores(signal_process, signal_status)


def start_button_clicked(signal_process, signal_status, signal_task, state):
    if state == 0:
        signal_task.emit("Searching Relevant Stores In Platform")
        search_stores(signal_process, signal_status)
        state += 1
    if state == 1:
        signal_task.emit("Download Products From Stores")
        download_products(signal_process, signal_status)
        state += 1
    if state == 2:
        signal_task.emit("Looking For Intellectual Property Violation Using Image Matching Algorithms")
        compare_images(signal_process, signal_status)

