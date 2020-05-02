from typing import List, Set, Tuple
import cv2
import os
import csv
from image_matching_module.in_depth_image_pair import InDepthImagePair as InDepthIP


class WritingModule:

    @staticmethod
    def writing_vintage_to_path(tuple_image_path_and_name: Tuple[str, str], index: int, vintage_im, filter_name: str):
        """
        This function saves a vintage filter image.

        :param tuple_image_path_and_name: The given tuple of (image path, image name).
        :param index: The index of the vintage filter.
        :param vintage_im: The image to save.
        :param filter_name: The filter name.
        """
        image_name = tuple_image_path_and_name[1].split(".")[0]
        cv2.imwrite(tuple_image_path_and_name[
                        0] + "\\" + image_name + "\\" + filter_name + "\\" + image_name + filter_name + str(
            index) + ".jpg", vintage_im)

    @staticmethod
    def writing_img_to_path(tuple_image_path_and_name: Tuple[str, str], img, filter_name: str):
        """
        This function saves a median, cropped and gery scale images.

        :param tuple_image_path_and_name: The given tuple of (image path, image name).
        :param img: The image to save.
        :param filter_name: The filter name.
        """
        image_name = tuple_image_path_and_name[1].split(".")[0]
        cv2.imwrite(tuple_image_path_and_name[0] + "\\" + image_name + "\\" + filter_name + "\\" + image_name
                    + filter_name + ".jpg", img)

    @staticmethod
    def writing_img_to_path_mirrored(tuple_image_path_and_name: Tuple[str, str], img, filter_name: str):
        """
        This function saves a mirrored filter image.

        :param tuple_image_path_and_name: The given tuple of (image path, image name).
        :param img: The image to save.
        :param filter_name: The filter name.
        """
        image_name = tuple_image_path_and_name[1].split(".")[0]
        cv2.imwrite(tuple_image_path_and_name[0] + "\\" + image_name + "\\" + "mirrored" + "\\" + image_name
                    + filter_name + ".jpg", img)

    @staticmethod
    def writing_rotate_to_path(tuple_image_path_and_name: Tuple[str, str], angle: int, folder_name: str, img):
        """
        This function saves a mirrored filter image.

        :param tuple_image_path_and_name: The given tuple of (image path, image name).
        :param angle: the angle of the rotated image.
        :param folder_name: The folder name to save in it the image.
        :param img: The image to save.
        """
        image_name = tuple_image_path_and_name[1].split(".")[0]
        img.save(tuple_image_path_and_name[0] + "\\" + image_name + "\\" + folder_name + "\\" + image_name + "rotate"
                 + str(angle) + ".jpg")

    @staticmethod
    def create_folders_for_images(list_of_tuple_path_image_name: List[Tuple[str, str]]):
        """
        This function create folders by given images names.

        :param list_of_tuple_path_image_name: The given tuple of (path to image , image name)
        """
        for image_name in list_of_tuple_path_image_name:
            split = image_name[1].split(".")[0]
            if not os.path.isdir(image_name[0] + "\\" + split):
                os.mkdir(image_name[0] + "\\" + split)

    @staticmethod
    def create_sub_folders_in_pic_folder(images_list: List[Tuple[str, str]]):
        """
        This functions creates a folder for each image that been
         manipulated for testing.

        :param images_list: The given tuple of (path to image , image name)
        """
        for image in images_list:
            path_to_pic_folder = image[0] + "\\" + image[1].split(".")[0]
            if not os.path.isdir(path_to_pic_folder + "\\" + "cropped"):
                os.mkdir(path_to_pic_folder + "\\" + "cropped")
                os.mkdir(path_to_pic_folder + "\\" + "rotated")
                os.mkdir(path_to_pic_folder + "\\" + "median")
                os.mkdir(path_to_pic_folder + "\\" + "mirrored")
                os.mkdir(path_to_pic_folder + "\\" + "vintage")
                os.mkdir(path_to_pic_folder + "\\" + "greyscale")

    @staticmethod
    def write_store_results_to_file(store_path: str, in_depth_results: List[InDepthIP]):
        """
        This function write the results of a store to csv file.

        :param store_path: The path to the store.
        :param in_depth_results: The results who needed to be written.
        """
        file_name = store_path + "/results.csv"
        if os.path.isfile(file_name):
            os.remove(file_name)
        with open(file_name, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',', lineterminator='\n')
            origin_image_path = "origin_image_path"
            origin_image_name = "origin_image_name"
            to_compare_image_path = "to_compare_image_path"
            to_compare_image_name = "to_compare_image_name"
            score = "score"
            csv_writer.writerow([origin_image_path, origin_image_name, to_compare_image_path,
                                to_compare_image_name, score])
            for row in in_depth_results:
                csv_writer.writerow([row.customer_image_path, row.customer_image_name, row.store_image_path,
                                    row.store_image_name, str(row.final_score)])
        csv_file.close()

    @staticmethod
    def write_final_results_file(stores_path: str, in_depth_results: List[InDepthIP]):
        """
        This function write the final results file.

        :param stores_path: The path to the folder of the stores.
        :param in_depth_results: The results to be written.
        """
        file_name = stores_path + "/final_results.csv"
        with open(file_name, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',', lineterminator='\n')
            origin_image_path = "origin_image_path"
            origin_image_name = "origin_image_name"
            to_compare_image_path = "to_compare_image_path"
            to_compare_image_name = "to_compare_image_name"
            score = "score"
            csv_writer.writerow([origin_image_path, origin_image_name, to_compare_image_path,
                                 to_compare_image_name, score])
            for row in in_depth_results:
                csv_writer.writerow([row.customer_image_path, row.customer_image_name, row.store_image_path,
                                     row.store_image_name, str(row.final_score)])
        csv_file.close()

    @staticmethod
    def merge_final_results_file_and_new_results(stores_path: str, in_depth_results: List[InDepthIP],
                                                 prev_store_results: Set = None):
        """
        This function merge the current final results file with the new results from a store
        and write the results to a new file of final results.

        :param stores_path: The folder of all stores path.
        :param in_depth_results: The list of the results of the store.
        :param prev_store_results: The results of the previous results of the store.
        """
        prev_store_results_exists = prev_store_results is not None
        file_name = stores_path + "/final_results.csv"
        file_name_tmp = stores_path + "/final_results_tmp.csv"
        in_depth_results_index = 0
        first = True
        WritingModule.write_column_names(stores_path)
        with open(file_name, newline='') as csvfile:
            line = csvfile.readline()
            while line and in_depth_results_index < len(in_depth_results):
                if first:
                    line = csvfile.readline()
                    first = False
                    continue
                # check if image pair already exists in previous final results file
                line = line.rstrip()
                if prev_store_results_exists:
                    if line in prev_store_results:
                        line = csvfile.readline()
                        continue
                spllited_line = line.split(",")
                old_score = spllited_line[4]
                if float(old_score) > in_depth_results[in_depth_results_index]:
                    WritingModule.write_spllitted_line_to_csv(spllited_line, file_name_tmp)
                    line = csvfile.readline()
                else:
                    WritingModule.write_object_to_csv(in_depth_results[in_depth_results_index], file_name_tmp)
                    in_depth_results_index += 1
            while line and line != '"\n':
                line = line.rstrip()
                spllited_line = line.split(",")
                WritingModule.write_spllitted_line_to_csv(spllited_line, file_name_tmp)
                line = csvfile.readline()
            while in_depth_results_index < len(in_depth_results):
                WritingModule.write_object_to_csv(in_depth_results[in_depth_results_index], file_name_tmp)
                in_depth_results_index += 1
        csvfile.close()
        os.remove(file_name)
        os.rename(file_name_tmp, file_name)

    @staticmethod
    def update_final_results_file(stores_path: str, in_depth_results: List[InDepthIP], prev_store_results=None):
        """
        This function write the final results file, if it is already exists merge the new results with the
        final results, else write the file as new one.

        :param stores_path: The path to the stores folder.
        :param in_depth_results: The results of a store
        :param prev_store_results: The results of the previous store, if there is no
        previous results will be assigned as None
        """
        file_name = stores_path + "/final_results.csv"
        if os.path.isfile(file_name):
            if prev_store_results is None:
                WritingModule.merge_final_results_file_and_new_results(stores_path, in_depth_results)
            else:
                WritingModule.merge_final_results_file_and_new_results(stores_path, in_depth_results,
                                                                       prev_store_results)
        else:
            WritingModule.write_final_results_file(stores_path, in_depth_results)

    @staticmethod
    def write_spllitted_line_to_csv(splitted_line: List[str], file_name_tmp):
        """
        This function write the splitted line to the file.

        :param splitted_line: The given line to write.
        :param file_name_tmp: The given file name to write to.
        """
        with open(file_name_tmp, 'a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',', lineterminator='\n')
            csv_writer.writerow([splitted_line[0], splitted_line[1], splitted_line[2],
                                 splitted_line[3], splitted_line[4]])
        csv_file.close()

    @staticmethod
    def write_object_to_csv(result: InDepthIP, file_name_tmp):
        """
        This function write an object to a file.
        :param result: The given object to write.
        :param file_name_tmp: The given file name to wrtie to.
        """
        with open(file_name_tmp, 'a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',', lineterminator='\n')
            csv_writer.writerow([result.customer_image_path, result.customer_image_name, result.store_image_path,
                                result.store_image_name, result.final_score])
        csv_file.close()

    @staticmethod
    def write_column_names(stores_path: str):
        """
        This function write The column names of the temporary results file.

        :param stores_path: The path to the folder of the stores.
        """
        file_name = stores_path + "/final_results_tmp.csv"
        with open(file_name, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',', lineterminator='\n')
            origin_image_path = "origin_image_path"
            origin_image_name = "origin_image_name"
            to_compare_image_path = "to_compare_image_path"
            to_compare_image_name = "to_compare_image_name"
            score = "score"
            csv_writer.writerow([origin_image_path, origin_image_name, to_compare_image_path,
                                to_compare_image_name, score])
        csv_file.close()
