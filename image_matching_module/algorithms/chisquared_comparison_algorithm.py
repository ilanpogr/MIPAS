from image_matching_module.algorithms.histogram_comparison_algorithm import HistogramComparisonAlgorithm
import numpy as np


class ChiSquaredComparisonAlgorithm(HistogramComparisonAlgorithm):

    def __init__(self):
        HistogramComparisonAlgorithm.__init__(self, "chi_squared")

    def calculate_score(self, origin_hist_base, to_compare_hist_base):
        eps = 1e-10
        dist = 0.1 * np.sum([((a - b) ** 2) / (a + b + eps)
                             for (a, b) in zip(origin_hist_base, to_compare_hist_base)])
        dist = dist / 10
        dist = self.normalize_bounbdries(dist)
        return 1 - dist

