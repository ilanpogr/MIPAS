import configUtils
import controllers.threadCreation as Thread
import crawler.shop_finder as ShopFinder
# import crawler.product_downloader as ProductDownloader


def start_search(main_screen):
    user_main_category = configUtils.get_property('main_category')
    user_sub_categories = configUtils.get_property('sub_categories')
    worker = Thread.Worker(ShopFinder.search_for_stores(user_main_category, user_sub_categories))
    main_screen.threadpool.start(worker)

def start_button_clicked(main_screen):
    start_search(main_screen)

