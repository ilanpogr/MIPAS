import unittest
from image_matching_module.algorithms import correlation_comparison_algorithm
from image_matching_module.algorithms import intersection_comparison_algorithm
from image_matching_module.algorithms import bhattacharyya_comparison_algorithm
from image_matching_module.algorithms import orb_feature_comparisson_algorithm
from image_matching_module import image_matching_utils
from image_matching_module import reading_utils
from image_matching_module import image_matching
import os



class TestImageMatching(unittest.TestCase):

    customer_path = "F:/avi/test_image_maching/tmpCustomer"
    stores_path = "F:/avi/test_image_maching/stores"
    store_path = "F:/avi/test_image_maching/stores/3"
    store_images_paths = reading_utils.ReadingUtils.get_images_names_in_folder(store_path)
    def test_run_matching_for_all_stores(self):
        image_matcher = image_matching.ImageMatching(self.customer_path, self.stores_path)
        image_matching.ImageMatching.run_matching_for_all_stores(image_matcher)
        self.assertTrue(os.path.isfile(self.stores_path + "/final_results.csv"))

    def run_matching_for_store(self):
        image_matcher = image_matching.ImageMatching(self.customer_path, self.stores_path)
        customer_images_paths = reading_utils.ReadingUtils.get_images_names_in_folder(self.customer_path)
        image_matching.ImageMatching.run_matching_for_store(image_matcher, customer_images_paths, self.store_path)
        self.assertTrue(os.path.isfile(self.store_path + "/results.csv"))
