import configUtils
import crawler.shop_finder as ShopFinder
import crawler.product_downloader as ProductDownloader


def search_stores(signal_process, signal_status):
    user_main_category = configUtils.get_property('main_category')
    user_sub_categories = configUtils.get_property('sub_categories')
    ShopFinder.search_for_stores(user_main_category, user_sub_categories, signal_process, signal_status)


def download_products(signal_process, signal_status):
    ProductDownloader.download_products_for_all_stores(signal_process, signal_status)


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

