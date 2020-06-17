import cv2
from image_matching_module.algorithms.histogram_comparison_algorithm import HistogramComparisonAlgorithm
import numpy as np

class BhattacharyyaComparisonAlgorithm(HistogramComparisonAlgorithm):

    def __init__(self):

        HistogramComparisonAlgorithm.__init__(self, "bhattacharyya")

    def calculate_score(self, customer_image, store_image):
        if not (type(customer_image) is np.ndarray and type(store_image) is np.ndarray):
            return TypeError
        customer_hist_base = self.create_hist_pic(customer_image)
        store_hist_base = self.create_hist_pic(store_image)
        bhattacharyya = cv2.compareHist(customer_hist_base, store_hist_base, cv2.HISTCMP_BHATTACHARYYA)
        return 1 - bhattacharyya
