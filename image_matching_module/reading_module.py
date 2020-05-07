import os
from typing import List, Tuple, Set

import cv2
from PIL import Image


class ReadingModule:
    """
    This class in change of all the reading functionality of the system.
    All reading of csv file and images.

    Attributes
    ----------
    image_extensions : set
        a set representing the extensions of images files.
    csv_extensions : str
        a string representing the extension of csv files.
    """

    image_extensions = {".jpg", ".JPG", ".png", ".PNG", ".JPEG"}
    csv_extensions = ".csv"

    @staticmethod
    def reading_image_from_tuple_path_open_cv(tuple_image_path_and_name: Tuple):
        """
        This functions reading an images from given tuple of path and image name using the open_cv library.

        :param tuple_image_path_and_name: The given tuple of (path to image, image name).
        :return: The image of the given tuple.
        """
        image_name = tuple_image_path_and_name[0] + "/" + tuple_image_path_and_name[1]
        return cv2.imread(image_name)

    @staticmethod
    def reading_image_from_tuple_path_using_image(tuple_image_path_and_name: Tuple):
        """
        This functions reading an images from given tuple of path and image name using the PIL library.

        :param tuple_image_path_and_name: The given tuple of (path to image, image name).
        :return: The image of the given tuple.
        """
        image_name = tuple_image_path_and_name[0] + "/" + tuple_image_path_and_name[1]
        return Image.open(image_name)

    @staticmethod
    def reading_all_images_from_given_tuple_path_list(tuple_path_list: Tuple) -> List[Tuple]:
        """
        This read all images from given tuple of path and image name.

        :param tuple_path_list: List of tuple (path to image, image name)
        :return: List of tuples containing (image name, image)
        """
        all_images = []
        for image_path in tuple_path_list:
            all_images.append((image_path[1], ReadingModule.reading_image_from_tuple_path_open_cv(image_path)))
        return all_images

    @staticmethod
    def get_images_names_in_folder(path: str) -> List[Tuple[str, str]]:
        """
        This function return all the images paths and name.

        :param path: The given path of the images.
        :return: List of tuples containing (path to image, image name)
        """
        images = []
        for r, d, f in os.walk(path):
            for file in f:
                for ext in ReadingModule.image_extensions:
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
        csv_files_paths = []
        for r, d, f in os.walk(path_to_csv_files):
            for file in f:
                if ReadingModule.csv_extensions in file:
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
