import unittest
from image_matching_module.algorithms import correlation_comparison_algorithm
from image_matching_module.algorithms import intersection_comparison_algorithm
from image_matching_module.algorithms import bhattacharyya_comparison_algorithm
from image_matching_module.algorithms import orb_feature_comparisson_algorithm
from image_matching_module import reading_utils


class TestAlgorithmTests(unittest.TestCase):
    image1 = reading_utils.ReadingUtils.reading_image_from_tuple_path_open_cv(("F:/avi/test_image_maching/tmpCustomer", "1.jpg"))
    image1_mirroredHorizontal = reading_utils.ReadingUtils.reading_image_from_tuple_path_open_cv(("F:/avi/test_image_maching/tmpCustomer", "1mirroredHorizontal.jpg"))
    image2 = reading_utils.ReadingUtils.reading_image_from_tuple_path_open_cv(("F:/avi/test_image_maching/tmpCustomer", "2.jpg"))

    def test_correlation(self):
        correlation = correlation_comparison_algorithm.CorrelationComparisonAlgorithm()
        self.assertAlmostEqual(correlation.calculate_score(self.image1, self.image1), 1)
        self.assertGreaterEqual(correlation.calculate_score(self.image1, self.image1_mirroredHorizontal), 0.6)
        self.assertLessEqual(correlation.calculate_score(self.image1, self.image2), 0.2)
        self.assertAlmostEqual(correlation.calculate_score(None, self.image1), TypeError)

    def test_intersection(self):
        intersection = intersection_comparison_algorithm.IntersectionComparisonAlgorithm()
        self.assertAlmostEqual(intersection.calculate_score(self.image1, self.image1), 1)
        self.assertGreaterEqual(intersection.calculate_score(self.image1, self.image1_mirroredHorizontal), 0.6)
        self.assertLessEqual(intersection.calculate_score(self.image1, self.image2), 0.2)
        self.assertAlmostEqual(intersection.calculate_score(None, self.image1), TypeError)

    def test_bhattacharyya(self):
        bhattacharyya = bhattacharyya_comparison_algorithm.BhattacharyyaComparisonAlgorithm()
        self.assertAlmostEqual(bhattacharyya.calculate_score(self.image1, self.image1), 1)
        self.assertGreaterEqual(bhattacharyya.calculate_score(self.image1, self.image1_mirroredHorizontal), 0.6)
        self.assertLessEqual(bhattacharyya.calculate_score(self.image1, self.image2), 0.2)
        self.assertAlmostEqual(bhattacharyya.calculate_score(None, self.image1), TypeError)

    def test_orb_features(self):
        orb_features = orb_feature_comparisson_algorithm.ORBFeatureComparisonAlgorithm()
        self.assertAlmostEqual(orb_features.calculate_score(self.image1, self.image1), 1)
        self.assertGreaterEqual(orb_features.calculate_score(self.image1, self.image1_mirroredHorizontal), 0.6)
        self.assertLessEqual(orb_features.calculate_score(self.image1, self.image2), 0.2)
        self.assertAlmostEqual(orb_features.calculate_score(None, self.image1), TypeError)

