import unittest
from image_matching_module import writing_utils
from image_matching_module import reading_utils
import os


class WritingUtilsTests(unittest.TestCase):

    image_to_save = reading_utils.ReadingUtils.reading_image_from_tuple_path_open_cv((os.getcwd(), "1.jpeg"))

    def test_writing_vintage_to_path(self):
        path = os.getcwd()
        image_name = "1.jpg"
        index = 1
        save_image_name = "1vintage1.jpg"
        writing_utils.WritingUtils.writing_vintage_to_path((path, image_name), index, self.image_to_save, "vintage")
        image_path = path + "/1/vintage/" + save_image_name
        self.assertTrue(os.path.isfile(image_path), True)
        os.remove(image_path)

    def test_writing_vintage_to_path_invalid_input(self):
        path = os.getcwd()
        image_name = "1.jpg"
        index = 1
        self.assertAlmostEqual(writing_utils.WritingUtils.writing_vintage_to_path((1, image_name), index, self.image_to_save, "vintage"),TypeError)
        self.assertAlmostEqual(writing_utils.WritingUtils.writing_vintage_to_path((path, 1), index, self.image_to_save, "vintage"),TypeError)
        self.assertAlmostEqual(writing_utils.WritingUtils.writing_vintage_to_path((path, image_name), "1", self.image_to_save, "vintage"),TypeError)
        self.assertAlmostEqual(writing_utils.WritingUtils.writing_vintage_to_path((path, image_name), index, self.image_to_save, 1),TypeError)
        self.assertAlmostEqual(writing_utils.WritingUtils.writing_vintage_to_path((path, 8.0), index, self.image_to_save, "vintage"),TypeError)
        self.assertAlmostEqual(writing_utils.WritingUtils.writing_vintage_to_path((None, image_name), index, self.image_to_save, "vintage"),TypeError)
        self.assertAlmostEqual(writing_utils.WritingUtils.writing_vintage_to_path((path, image_name), None, self.image_to_save, "vintage"),TypeError)
        self.assertAlmostEqual(writing_utils.WritingUtils.writing_vintage_to_path((path, image_name), index, self.image_to_save, 6),TypeError)
        self.assertAlmostEqual(writing_utils.WritingUtils.writing_vintage_to_path((path, image_name), index, self.image_to_save, -1),TypeError)
        self.assertAlmostEqual(writing_utils.WritingUtils.writing_vintage_to_path((path, image_name), 5.0, self.image_to_save, "vintage"),TypeError)
        self.assertAlmostEqual(writing_utils.WritingUtils.writing_vintage_to_path((path, None), index, self.image_to_save, "vintage"),TypeError)
        self.assertAlmostEqual(writing_utils.WritingUtils.writing_vintage_to_path(("illegal_path", image_name), index, self.image_to_save, "vintage"),FileNotFoundError)


    def test_writing_img_to_path(self):
        path = os.getcwd()
        image_name = "1.jpg"
        save_image_name = "1vintage.jpg"
        writing_utils.WritingUtils.writing_img_to_path((path,image_name),self.image_to_save,"vintage")
        image_path = path + "/1/vintage/" + save_image_name
        self.assertTrue(os.path.isfile(image_path), True)
        os.remove(image_path)


    def test_writing_img_to_path_invalid_input(self):
        path = os.getcwd()
        image_name = "1.jpg"
        self.assertAlmostEqual(writing_utils.WritingUtils.writing_img_to_path((1, image_name), self.image_to_save, "vintage"),TypeError)
        self.assertAlmostEqual(writing_utils.WritingUtils.writing_img_to_path((path, 1), self.image_to_save, "vintage"),TypeError)
        self.assertAlmostEqual(writing_utils.WritingUtils.writing_img_to_path((path, image_name), self.image_to_save, 1),TypeError)
        self.assertAlmostEqual(writing_utils.WritingUtils.writing_img_to_path((None, image_name), self.image_to_save, "vintage"),TypeError)
        self.assertAlmostEqual(writing_utils.WritingUtils.writing_img_to_path((path, None), self.image_to_save, "vintage"),TypeError)
        self.assertAlmostEqual(writing_utils.WritingUtils.writing_img_to_path((path, image_name), self.image_to_save, None),TypeError)
        self.assertAlmostEqual(writing_utils.WritingUtils.writing_img_to_path(None, self.image_to_save, "vintage"),TypeError)
        self.assertAlmostEqual(writing_utils.WritingUtils.writing_img_to_path(1, self.image_to_save, "vintage"),TypeError)
        self.assertAlmostEqual(writing_utils.WritingUtils.writing_img_to_path("string", self.image_to_save, "vintage"),TypeError)
        self.assertAlmostEqual(writing_utils.WritingUtils.writing_img_to_path(("string", image_name), self.image_to_save, "vintage"),FileNotFoundError)
