import cv2
from image_matching_module.algorithms.histogram_comparison_algorithm import HistogramComparisonAlgorithm


class BhattacharyyaComparisonAlgorithm(HistogramComparisonAlgorithm):

    def __init__(self):

        HistogramComparisonAlgorithm.__init__(self, "bhattacharyya")

    def calculate_score(self, customer_image, store_image):
        customer_hist_base = self.create_hist_pic(customer_image)
        store_hist_base = self.create_hist_pic(store_image)
        bhattacharyya = cv2.compareHist(customer_hist_base, store_hist_base, cv2.HISTCMP_BHATTACHARYYA)
        return 1 - bhattacharyya
