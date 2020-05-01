import csv
import os
import cv2
from PIL import Image


class ReadingModule:
    """a reading module."""

    def __init__(self):
        self.image_extensions = {".jpg", ".JPG" , ".png" , ".PNG" , ".JPEG"}
        self.csv_extensions = ".csv"

    def reading_image_from_tuple_path_open_cv(self, tuple_image_path_and_name):
        """reading an image from path."""
        image_name = tuple_image_path_and_name[0] + "/" + tuple_image_path_and_name[1]
        return cv2.imread(image_name)

    def reading_image_from_tuple_path_using_image(self, tuple_image_path_and_name):
        image_name = tuple_image_path_and_name[0] + "/" + tuple_image_path_and_name[1]
        return Image.open(image_name)

    def reading_all_images_from_given_tuple_path_list(self, tuple_path_list):
        """reading all images from a given path, the names of the pics are in the given list."""
        all_images = []
        for image_path in tuple_path_list:
            all_images.append((image_path[1], self.reading_image_from_tuple_path_open_cv(image_path)))
        return all_images

    def get_images_names_in_folder(self, path):
        """getting all the images names from a given path."""
        images = []
        for r, d, f in os.walk(path):
            for file in f:
                for ext in self.image_extensions:
                    if ext in file:
                        to_add = os.path.join(r), file
                        images.append(to_add)
        return images

    def reading_all_folders_in_given_path(self, path):
        """return all the sub-folder names (one level down) in a given path."""
        folders_names = []
        subfolders = [path + "/" + dI for dI in os.listdir(path) if os.path.isdir(os.path.join(path, dI))]
        for subfolder in subfolders:
            splitted = subfolder.split("/")
            folders_names.append(splitted[len(splitted) - 1])
        return folders_names

    def read_histogram_csv_file(self, path_to_file):
        with open(path_to_file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            origin_images = []
            to_compare_images = []
            counter = 0
            for row in csv_reader:
                if counter == 0:
                    counter += 1
                    continue
                origin_iamge_data = row[0], row[1]
                if origin_iamge_data not in origin_images:
                    origin_images.append(origin_iamge_data)

                to_comapre_images_data = row[2], row[3]
                if to_comapre_images_data not in to_compare_images:
                    to_compare_images.append(to_comapre_images_data)
        return origin_images, to_compare_images

    def get_images_after_histogram_test(self, passed_histogram_test):
        origin_images = []
        to_compare_images = []
        similar_images = []
        for row in passed_histogram_test:
            row = row.split(",")
            similar_images_to_add = row[1], row[3]
            similar_images.append(similar_images_to_add)
            origin_iamge_data = row[0], row[1]
            if origin_iamge_data not in origin_images:
                # origin_iamge_data = origin_iamge_data , row[4]
                origin_images.append(origin_iamge_data)

            to_comapre_images_data = row[2], row[3]
            if to_comapre_images_data not in to_compare_images:
                # to_comapre_images_data = to_comapre_images_data , row[4]
                to_compare_images.append(to_comapre_images_data)
        return origin_images, to_compare_images, similar_images

    def get_image_name_and_path(self, images_list, image_index):
        """reading the path and the name of an image."""
        origin_image_name = images_list[image_index][1]
        origin_image_path = images_list[image_index][0]
        return origin_image_path, origin_image_name

    def read_all_csv_paths_from_path(self, path_to_csv_files):
        """getting all the images names from a given path."""
        csv_files_paths = []
        for r, d, f in os.walk(path_to_csv_files):
            for file in f:
                if self.csv_extensions in file:
                    to_add = os.path.join(r) + file
                    csv_files_paths.append(to_add)
        return csv_files_paths