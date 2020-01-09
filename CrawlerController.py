from crawler import ShopFinder, ProductsDownloader


def _new_search():
    ShopFinder.search_for_stores_demo()
    _update_found_stores()


def _update_found_stores():
    ProductsDownloader.download_all_products_demo()


def _no_search():
    pass


def crawl_by_option(option):
    switcher = {
        1: _new_search,
        2: _update_found_stores,
        3: _no_search,
    }
    # Get the function from switcher dictionary
    executor = switcher.get(option, lambda: "Invalid Option")
    executor()

