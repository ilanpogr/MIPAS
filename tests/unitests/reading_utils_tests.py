from PIL import ImageFile
import unittest
from image_matching_module import reading_utils
import numpy as np


class ReadingUtilsTests(unittest.TestCase):

    image_path = ("F:/avi/test_image_maching/tmpCustomer", "1.jpg")
    image_path_not_exist = ("F:/avi/test_image_maching/tmpCustomer", "11111.jpg")
    bad_path = (1,"1.jpg")

    images_paths_list = [("F:/avi/test_image_maching/tmpCustomer", "1.jpg"),
                         ("F:/avi/test_image_maching/tmpCustomer", "2.jpg"),
                         ("F:/avi/test_image_maching/tmpCustomer", "3.jpg")]
    images_paths_list_bad_type = 5
    images_path_not_legal = [("F:/avi/test_image_maching/tmpCusasdtomer", "1.jpg")]

    folder_path = "F:/avi/test_image_maching/tmpCustomer"
    first_bad_folder_path = 1
    second_bad_folder_path = 8.8

    path_to_csv = "F:/avi/test_image_maching/stores"
    bad_value_path_to_csv = 9
    not_exist_path_to_csv = "F:/avi/test_image_machisddsng/stores"

    stores_path = "F:/avi/test_image_maching/stores"
    bad_value_stores_path = 1
    not_exist_path_to_csv = "F:/avi/test_image_machinasdg/stores"


    init_algorithm_and_weights = ["bhattacharyya,0.7","correlation,0.25","intersection,0.05"]
    bad_value_init_algorithm_and_weights = 1
    bad_value_weight_higher_then_one = ["bhattacharyya,7","correlation,0.25","intersection,0.05"]

    def test_reading_image_from_tuple_path_open_cv(self):
        self.assertIsInstance(reading_utils.ReadingUtils.reading_image_from_tuple_path_open_cv(self.image_path),np.ndarray)
        self.assertAlmostEqual(reading_utils.ReadingUtils.reading_image_from_tuple_path_open_cv(self.bad_path), TypeError)
        self.assertAlmostEqual(reading_utils.ReadingUtils.reading_image_from_tuple_path_open_cv(self.image_path_not_exist), FileNotFoundError)

    def test_reading_image_from_tuple_path_using_image(self):
        self.assertIsInstance(reading_utils.ReadingUtils.reading_image_from_tuple_path_using_image(self.image_path),ImageFile.ImageFile)
        self.assertAlmostEqual(reading_utils.ReadingUtils.reading_image_from_tuple_path_using_image(self.bad_path), TypeError)
        self.assertAlmostEqual(reading_utils.ReadingUtils.reading_image_from_tuple_path_using_image(self.image_path_not_exist), FileNotFoundError)

    def test_reading_all_images_from_given_tuple_path_list(self):
        self.assertIsInstance(reading_utils.ReadingUtils.reading_all_images_from_given_tuple_path_list(self.images_paths_list),list)
        self.assertAlmostEqual(reading_utils.ReadingUtils.reading_all_images_from_given_tuple_path_list(self.images_paths_list_bad_type), TypeError)
        self.assertAlmostEqual(reading_utils.ReadingUtils.reading_all_images_from_given_tuple_path_list(self.images_path_not_legal), FileNotFoundError)

    def test_get_images_names_in_folder(self):
        self.assertIsInstance(reading_utils.ReadingUtils.get_images_names_in_folder(self.folder_path),list)
        self.assertAlmostEqual(reading_utils.ReadingUtils.get_images_names_in_folder(self.first_bad_folder_path),TypeError)
        self.assertAlmostEqual(reading_utils.ReadingUtils.get_images_names_in_folder(self.second_bad_folder_path),TypeError)

    def test_read_all_csv_paths_from_path(self):
        self.assertIsInstance(reading_utils.ReadingUtils.read_all_csv_paths_from_path(self.path_to_csv),list)
        self.assertAlmostEqual(reading_utils.ReadingUtils.read_all_csv_paths_from_path(self.bad_value_path_to_csv),TypeError)
        self.assertAlmostEqual(reading_utils.ReadingUtils.read_all_csv_paths_from_path(self.not_exist_path_to_csv),NotADirectoryError)

    def test_reading_all_folders_paths_in_given_path(self):
        self.assertIsInstance(reading_utils.ReadingUtils.reading_all_folders_paths_in_given_path(self.stores_path),list)
        self.assertAlmostEqual(reading_utils.ReadingUtils.reading_all_folders_paths_in_given_path(self.bad_value_stores_path),TypeError)
        self.assertAlmostEqual(reading_utils.ReadingUtils.reading_all_folders_paths_in_given_path(self.not_exist_path_to_csv),NotADirectoryError)

    def test_init_algorithm_and_weights_dict(self):
        self.assertIsInstance(reading_utils.ReadingUtils.init_algorithm_and_weights_dict(self.init_algorithm_and_weights),dict)
        self.assertAlmostEqual(reading_utils.ReadingUtils.init_algorithm_and_weights_dict(self.bad_value_init_algorithm_and_weights),TypeError)
        self.assertAlmostEqual(reading_utils.ReadingUtils.init_algorithm_and_weights_dict(self.bad_value_weight_higher_then_one),ValueError)

