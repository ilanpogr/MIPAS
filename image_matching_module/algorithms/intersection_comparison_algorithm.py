from image_matching_module.algorithms.histogram_comparison_algorithm import   HistogramComparisonAlgorithm
import numpy as np


class IntersectionComparisonAlgorithm(HistogramComparisonAlgorithm):

    def __init__(self):
        HistogramComparisonAlgorithm.__init__(self,"intersection")

    def calculate_score(self, customer_image, store_image):
        if not (type(customer_image) is np.ndarray and type(store_image) is np.ndarray):
            return TypeError
        customer_hist_base = self.create_hist_pic(customer_image)
        store_hist_base = self.create_hist_pic(store_image)
        minimal = np.minimum(customer_hist_base, store_hist_base)
        minimal_sum = np.sum(minimal)
        store_hist_sum = np.sum(store_hist_base)

        # an issue with histogram which contains only zeroes.
        if minimal_sum == 0.0:
            return 0
        intersection = np.true_divide(minimal_sum, store_hist_sum)
        return intersection
