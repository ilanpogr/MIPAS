
import unittest
from typing import List
from image_matching_module import image_matching_utils
from image_matching_module import reading_utils
from image_matching_module import image_matching_configuration



class ImageMatchingUtils(unittest.TestCase):

    customer_path = "F:/avi/test_image_maching/tmpCustomer"
    stores_path = "F:/avi/test_image_maching/stores"
    store_path = "F:/avi/test_image_maching/stores/3"
    store_images_paths = reading_utils.ReadingUtils.get_images_names_in_folder(store_path)
    customer_images_paths = reading_utils.ReadingUtils.get_images_names_in_folder(customer_path)
    configuration = image_matching_configuration.ImageMatchingConfiguration()

    def test_divide_images_to_batches(self):
        self.assertAlmostEqual(image_matching_utils.ImageMatchingUtils.divide_images_to_batches(self.store_images_paths, 0), ValueError)
        self.assertAlmostEqual(image_matching_utils.ImageMatchingUtils.divide_images_to_batches(self.store_images_paths, -1), ValueError)
        self.assertAlmostEqual(image_matching_utils.ImageMatchingUtils.divide_images_to_batches(self.store_images_paths, 0.8), TypeError)
        self.assertAlmostEqual(image_matching_utils.ImageMatchingUtils.divide_images_to_batches(self.store_images_paths, "test"), TypeError)
        self.assertIsInstance(image_matching_utils.ImageMatchingUtils.divide_images_to_batches(self.store_images_paths, 10), List)

    def test_get_combined_initial_score(self):
        customer_images_paths = reading_utils.ReadingUtils.get_images_names_in_folder(self.customer_path)
        customer_images_batches = image_matching_utils.ImageMatchingUtils.divide_images_to_batches(customer_images_paths, 10)
        customer_images_batch = reading_utils.ReadingUtils.reading_all_images_from_given_tuple_path_list(customer_images_batches[0])

        store_images_paths = reading_utils.ReadingUtils.get_images_names_in_folder(self.store_path)
        stores_images_batches = image_matching_utils.ImageMatchingUtils.divide_images_to_batches(store_images_paths, 10)
        stores_images_batch = reading_utils.ReadingUtils.reading_all_images_from_given_tuple_path_list(stores_images_batches[0])

        self.assertIsInstance(image_matching_utils.ImageMatchingUtils.get_combined_initial_score(self.customer_path,customer_images_batch
                                                                                                 ,self.store_path,stores_images_batch,
                                                                                                 self.configuration.initial_algorithms_weights,
                                                                                                 self.configuration.initial_threshold), list)

        self.assertAlmostEqual(image_matching_utils.ImageMatchingUtils.get_combined_initial_score(1,customer_images_batch
                                                                                                 ,self.store_path,stores_images_batch,
                                                                                                 self.configuration.initial_algorithms_weights,
                                                                                                 self.configuration.initial_threshold), TypeError)

        self.assertAlmostEqual(image_matching_utils.ImageMatchingUtils.get_combined_initial_score(self.customer_path,1
                                                                                                 ,self.store_path,stores_images_batch,
                                                                                                 self.configuration.initial_algorithms_weights,
                                                                                                 self.configuration.initial_threshold), TypeError)

        self.assertAlmostEqual(image_matching_utils.ImageMatchingUtils.get_combined_initial_score(self.customer_path,customer_images_batch
                                                                                                 ,1,stores_images_batch,
                                                                                                 self.configuration.initial_algorithms_weights,
                                                                                                 self.configuration.initial_threshold), TypeError)

        self.assertAlmostEqual(image_matching_utils.ImageMatchingUtils.get_combined_initial_score(self.customer_path,customer_images_batch
                                                                                                 ,self.store_path,1,
                                                                                                 self.configuration.initial_algorithms_weights,
                                                                                                 self.configuration.initial_threshold), TypeError)

        self.assertAlmostEqual(image_matching_utils.ImageMatchingUtils.get_combined_initial_score(self.customer_path,customer_images_batch
                                                                                                 ,self.store_path,stores_images_batch,
                                                                                                 1,
                                                                                                 self.configuration.initial_threshold), TypeError)

        self.assertAlmostEqual(image_matching_utils.ImageMatchingUtils.get_combined_initial_score(self.customer_path,customer_images_batch
                                                                                                 ,self.store_path,stores_images_batch,
                                                                                                 self.configuration.initial_algorithms_weights,
                                                                                                 1), TypeError)

    def test_get_combined_in_depth_score(self):
        customer_images_paths = reading_utils.ReadingUtils.get_images_names_in_folder(self.customer_path)
        customer_images_batches = image_matching_utils.ImageMatchingUtils.divide_images_to_batches(customer_images_paths, 10)

        self.assertAlmostEqual(image_matching_utils.ImageMatchingUtils.get_combined_in_depth_score(1,
                                                                                                  self.configuration.in_depth_algorithms_weights,
                                                                                                   self.configuration.initial_score_weight,
                                                                                                  self.configuration.in_depth_threshold), TypeError)

        self.assertAlmostEqual(image_matching_utils.ImageMatchingUtils.get_combined_in_depth_score(customer_images_batches,
                                                                                                   2,
                                                                                                   self.configuration.initial_score_weight,
                                                                                                   self.configuration.in_depth_threshold), TypeError)

        self.assertAlmostEqual(image_matching_utils.ImageMatchingUtils.get_combined_in_depth_score(customer_images_batches,
                                                                                                   self.configuration.in_depth_algorithms_weights,
                                                                                                   3,
                                                                                                   self.configuration.in_depth_threshold), TypeError)

        self.assertAlmostEqual(image_matching_utils.ImageMatchingUtils.get_combined_in_depth_score(customer_images_batches,
                                                                                                   self.configuration.in_depth_algorithms_weights,
                                                                                                   self.configuration.initial_score_weight,
                                                                                                   4), TypeError)
