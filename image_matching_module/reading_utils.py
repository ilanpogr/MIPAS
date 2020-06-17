import os
from typing import List, Tuple, Set
import cv2
from PIL import Image
from image_matching_module import manipulation
import numpy as np


class ReadingUtils:
    """
    This class in change of all the reading functionality of the system.
    All reading of csv file and images.
    """

    # a set representing the extensions of images files
    image_extensions = {".jpg", ".JPG", ".png", ".PNG", ".JPEG", ".jpeg"}
    # a string representing the extension of csv files
    csv_extensions = ".csv"

    @staticmethod
    def reading_image_from_tuple_path_open_cv(tuple_image_path_and_name: Tuple):
        """
        This functions reading an images from given tuple of path and image name using the open_cv library.

        :param tuple_image_path_and_name: The given tuple of (path to image, image name).
        :return: The image of the given tuple.
        """
        if not (type(tuple_image_path_and_name) is tuple and type(tuple_image_path_and_name[0]) is str and
            type(tuple_image_path_and_name[1]) is str):
            return TypeError
        image_name = tuple_image_path_and_name[0] + "/" + tuple_image_path_and_name[1]
        if not os.path.isfile(image_name):
            return FileNotFoundError
        return cv2.imread(image_name)

    @staticmethod
    def reading_image_from_tuple_path_using_image(tuple_image_path_and_name: Tuple):
        """
        This functions reading an images from given tuple of path and image name using the PIL library.

        :param tuple_image_path_and_name: The given tuple of (path to image, image name).
        :return: The image of the given tuple.
        """
        if not (type(tuple_image_path_and_name) is tuple and type(tuple_image_path_and_name[0]) is str and
                type(tuple_image_path_and_name[1]) is str):
            return TypeError
        image_name = tuple_image_path_and_name[0] + "/" + tuple_image_path_and_name[1]
        if not os.path.isfile(image_name):
            return FileNotFoundError
        return Image.open(image_name)

    @staticmethod
    def reading_all_images_from_given_tuple_path_list(tuple_path_list: Tuple) -> List[Tuple]:
        """
        This read all images from given tuple of path and image name.

        :param tuple_path_list: List of tuple (path to image, image name)
        :return: List of tuples containing (image name, image)
        """
        if not type(tuple_path_list) is list:
            return TypeError
        if not os.path.isfile(tuple_path_list[0][0] + "/" + tuple_path_list[0][1]):
            return FileNotFoundError
        all_images = []
        for image_path in tuple_path_list:
            all_images.append((image_path[1], ReadingUtils.reading_image_from_tuple_path_open_cv(image_path)))
        return all_images

    @staticmethod
    def get_images_names_in_folder(path: str) -> List[Tuple[str, str]]:
        """
        This function return all the images paths and name.

        :param path: The given path of the images.
        :return: List of tuples containing (path to image, image name)
        """
        if type(path) is not str:
            return TypeError
        images = []
        for r, d, f in os.walk(path):
            for file in f:
                for ext in ReadingUtils.image_extensions:
                    if ext in file:
                        to_add = os.path.join(r), file
                        images.append(to_add)
        return images

    @staticmethod
    def read_all_csv_paths_from_path(path_to_csv_files: str) -> List[str]:
        """
        This function returns all the csv paths and names.

        :param path_to_csv_files: The given path to csv files.
        :return: List of the path to the csv files.
        """
        if type(path_to_csv_files) is not str:
            return TypeError
        if not os.path.isdir(path_to_csv_files):
            return NotADirectoryError
        csv_files_paths = []
        for r, d, f in os.walk(path_to_csv_files):
            for file in f:
                if ReadingUtils.csv_extensions in file:
                    to_add = os.path.join(r) + file
                    csv_files_paths.append(to_add)
        return csv_files_paths

    @staticmethod
    def reading_all_folders_paths_in_given_path(stores_path: str) -> List[str]:
        """
        This function returns a list of full paths of the store names.

        :param stores_path: The path to the stores folder.
        :return: A list of the full path to the store.
        """
        if type(stores_path) is not str:
            return TypeError
        if not os.path.isdir(stores_path):
            return NotADirectoryError
        sub_folders = [stores_path + "/" + dI for dI in os.listdir(stores_path) if os.path.isdir
                                                                (os.path.join(stores_path, dI))]
        return sub_folders

    @staticmethod
    def get_prev_store_results(store_path: str) -> Set[str]:
        """
        This function returns the previous results of a store.

        :param store_path: the path of the store.
        :return: A set of the results of the store previous results.
        """
        file_name = store_path + "/results.csv"
        prev_store_results = set()
        first = True
        if not os.path.isfile(file_name):
            return None
        with open(file_name) as csv_file:
            for line in csv_file:
                if first:
                    first = False
                    continue
                line = line.rstrip()
                prev_store_results.add(line)
        csv_file.close()
        return prev_store_results

    @staticmethod
    def init_algorithm_and_weights_dict(algorithms_and_weights_list):
        if type(algorithms_and_weights_list) is not list:
            return TypeError
        algorithms_and_weights_dict = {}
        for algorithm_and_weight in algorithms_and_weights_list:
            algorithm , weight = algorithm_and_weight.split(",")
            if "\n" in weight:
                weight = weight.strip()
            if float(weight) > 1:
                return ValueError
            algorithms_and_weights_dict[algorithm] = weight
        return algorithms_and_weights_dict

    @staticmethod
    def read_config_file(file_name):
        script_dir = os.path.dirname(__file__)
        abs_file_path = os.path.join(script_dir, file_name)
        with open(abs_file_path,'r') as config_file:

            line = config_file.readline()
            batch_size = line.split(":")[1].strip()

            line = config_file.readline()
            initial_threshold = line.split(":")[1].strip()

            line = config_file.readline()
            in_depth_threshold = line.split(":")[1].strip()

            line = config_file.readline()
            initial_score_weight = line.split(":")[1].strip()

            line = config_file.readline()
            initial_algorithms_and_weights_list = line.split(":")[1].split(";")
            initial_algorithms_and_weights_dict = ReadingUtils.init_algorithm_and_weights_dict(initial_algorithms_and_weights_list)

            line = config_file.readline()
            in_depth_algorithms_and_weights_list = line.split(":")[1].split(";")
            in_depth_algorithms_and_weights_dict = ReadingUtils.init_algorithm_and_weights_dict(in_depth_algorithms_and_weights_list)

            return batch_size,initial_threshold, in_depth_threshold, initial_score_weight,  initial_algorithms_and_weights_dict, in_depth_algorithms_and_weights_dict
