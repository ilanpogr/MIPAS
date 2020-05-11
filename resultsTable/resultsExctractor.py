import os
import webbrowser

import pandas as pd
from PIL import Image


class ResultsExtractor:

    def __init__(self, file_path):
        self.data = pd.read_csv(file_path)
        self.user_image_path_col = "Your Image"
        self.user_image_name_col = "Your Image Name"
        self.store_name_col = "Suspected Store Name"
        self.store_image_path_col = "Store's Image"
        # self.store_image_name_col = "Store's Image Name"
        self.product_url_col = "Product URL"

    def read_results(self):
        res = pd.DataFrame(columns=[self.user_image_path_col, self.user_image_name_col, self.store_name_col,
                                    self.store_image_path_col, self.product_url_col])
        i = 0
        for _, row in self.data.iterrows():
            user_image_name = row["origin_image_name"]
            user_image_path = row["origin_image_path"] + "/" + user_image_name
            store_name = row["to_compare_image_path"].split("/")[-1]
            store_image_name = row["to_compare_image_name"]
            product_url = self.get_product_url(row["to_compare_image_path"], store_image_name)
            store_image_path = row["to_compare_image_path"] + "/" + store_image_name
            res.loc[i] = [user_image_path] + [user_image_name] + [store_name] + \
                         [store_image_path] + [product_url]
            i += 1
        return res

    @staticmethod
    def get_product_url(path, image_name):
        store_name = path.split("/")[-1]
        file = path + "/" + store_name + "_products.csv"
        df = pd.read_csv(file)
        relevant = df.loc[df['File'] == image_name]
        url = None
        for _, row in relevant.iterrows():
            if row['File'] == image_name:
                url = row['URL']
                break
        return url

    @staticmethod
    def open_link(item):
        if item.column() == 4:  # product URL
            webbrowser.open(item.data())
        elif item.column() == 0 or item.column() == 3:
            img = Image.open(os.path.abspath(item.data()))
            img.show()
        elif item.column() == 2:  # product URL
            store_url = "https://www.etsy.com/il-en/shop/{}?ref=ss_profile".format(item.data())
            webbrowser.open(store_url)
