from image_matching_module.algorithms.histogram_comparison_algorithm import   HistogramComparisonAlgorithm
import numpy as np


class IntersectionComparisonAlgorithm(HistogramComparisonAlgorithm):

    def __init__(self):
        HistogramComparisonAlgorithm.__init__(self,"intersection")

    def calculate_score(self, customer_image, store_image):
        customer_hist_base = self.create_hist_pic(customer_image)
        store_hist_base = self.create_hist_pic(store_image)
        minima = np.minimum(customer_hist_base, store_hist_base)
        intersection = np.true_divide(np.sum(minima), np.sum(store_hist_base))
        return intersection
