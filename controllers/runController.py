import configUtils
import controllers.threadCreation as Thread
import crawler.shop_finder as ShopFinder
# import crawler.product_downloader as ProductDownloader


# def update_progress_bar(n):
#     print("%d% done" % n)


def search_stores(main_screen):  # todo - try different Thread approach....
    user_main_category = configUtils.get_property('main_category')
    user_sub_categories = configUtils.get_property('sub_categories')
    print(user_main_category)
    print(user_sub_categories)


def start_search(main_screen):
    search_stores(main_screen)
    # worker = Thread.Worker(search_stores(main_screen))
    # worker.signals.progress.connect(update_progress_bar)
    # main_screen.threadpool.start(worker)


def start_button_clicked(main_screen):
    start_search(main_screen)

