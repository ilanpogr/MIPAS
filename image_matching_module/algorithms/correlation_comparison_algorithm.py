import cv2
from image_matching_module.algorithms.histogram_comparison_algorithm import HistogramComparisonAlgorithm


class CorrelationComparisonAlgorithm(HistogramComparisonAlgorithm):

    def __init__(self):
        HistogramComparisonAlgorithm.__init__(self, "correlation")

    def calculate_score(self, customer_image, store_image):
        customer_hist_base = self.create_hist_pic(customer_image)
        store_hist_base = self.create_hist_pic(store_image)
        correlation_result = cv2.compareHist(customer_hist_base, store_hist_base, cv2.HISTCMP_CORREL)
        correlation_result = self.normalize_bounbdries(correlation_result)
        return correlation_result
