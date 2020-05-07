import configUtils
import crawler.shop_finder as ShopFinder
# import crawler.product_downloader as ProductDownloader


def search_stores(signal):
    user_main_category = configUtils.get_property('main_category')
    user_sub_categories = configUtils.get_property('sub_categories')
    print(user_main_category)
    print(user_sub_categories)
    ShopFinder.search_for_stores(user_main_category, user_sub_categories, signal)


def start_search(signal):
    search_stores(signal)


def start_button_clicked(signal):
    start_search(signal)

