from typing import List
import cv2
import os
import csv
from image_matching_module.reading_module import ReadingModule
from image_matching_module.in_depth_image_pair import InDepthImagePair as InDepthIP


class WritingModule:

    @staticmethod
    def writing_vintage_to_path(tuple_image_path_and_name, index, vintage_im, filter_name):
        """writing vintage image to given path, using the vintage index"""
        image_name = tuple_image_path_and_name[1].split(".")[0]
        cv2.imwrite(tuple_image_path_and_name[
                        0] + "\\" + image_name + "\\" + filter_name + "\\" + image_name + filter_name + str(
            index) + ".jpg", vintage_im)

    @staticmethod
    def writing_img_to_path(tuple_image_path_and_name, img, filter_name):
        """writing image to given path"""
        image_name = tuple_image_path_and_name[1].split(".")[0]
        cv2.imwrite(tuple_image_path_and_name[
                        0] + "\\" + image_name + "\\" + filter_name + "\\" + image_name + filter_name + ".jpg", img)

    @staticmethod
    def writing_img_to_path_mirrored(tuple_image_path_and_name, img, filter_name):
        """writing image to given path"""
        image_name = tuple_image_path_and_name[1].split(".")[0]
        tt = tuple_image_path_and_name[0] + "\\" + image_name + "\\" + filter_name + "\\" + image_name + filter_name \
             + ".jpg"
        cv2.imwrite(tuple_image_path_and_name[0] + "\\" + image_name + "\\" + "mirrored" + "\\" + image_name
                    + filter_name + ".jpg", img)

    @staticmethod
    def writing_rotate_to_path(tuple_image_path_and_name, name, folder_name, img):
        """writing rotated image to path"""
        image_name = tuple_image_path_and_name[1].split(".")[0]
        img.save(tuple_image_path_and_name[0] + "\\" + image_name + "\\" + folder_name + "\\" + image_name + "rotate"
                 + str(name) + ".jpg")

    @staticmethod
    def create_folders_for_images(tuple_path_and_name_image_list):
        """creating folder for each picture"""
        for image_name in tuple_path_and_name_image_list:
            split = image_name[1].split(".")[0]
            if not os.path.isdir(image_name[0] + "\\" + split):
                os.mkdir(image_name[0] + "\\" + split)

    @staticmethod
    def there_is_result_folder(path):
        """writing the histogram csv to given path"""
        all_folders_in_path = ReadingModule.reading_all_folders_in_given_path(path)
        for folder_name in all_folders_in_path:
            if folder_name == "results":
                return True
        return False

    @staticmethod
    def writing_histogram_results_to_csv_file(self, path, image_name, list_to_write):
        if not self.there_is_result_folder(path):
            self.create_folder_for_results(path, "results")
        path = path + "\\results"

        method = "method"
        origin_image = "origin_image"
        compared_image = "compared_image"
        score = "score"

        with open(os.path.join(path, image_name.split(".")[0] + 'HistogramOutput.csv'), "w") as f:
            csvwriter = csv.writer(f, delimiter=' ', lineterminator='\n')
            csvwriter.writerow(method + "," + origin_image + "," + compared_image + "," + score)
            for line in list_to_write:
                csvwriter.writerow(line)
        # print("finish with histogram working on image number: " + image_name)

    @staticmethod
    def writing_features_results_to_csv_file(self, path, image_name, list_to_write):
        """writing the features csv to given path"""
        if not self.there_is_result_folder(path):
            self.create_folder_for_results(path, "results")
        path = path + "\\results"

        origin_image_name = "origin_image_name"
        number_of_features = "number_of_features"
        compared_image = "compared_image"
        number_of_matchers = "number_of_matchers"
        score = "score"

        with open(os.path.join(path, image_name.split(".")[0] + 'FaeturesOutput.csv'), "w") as f:
            csvwriter = csv.writer(f, delimiter=' ', lineterminator='\n')
            csvwriter.writerow(origin_image_name + "," + number_of_features + "," + compared_image + "," +
                               number_of_features + "," + number_of_matchers + "," + score)
            for line in list_to_write:
                csvwriter.writerow(line)
        # print("finish with features working on image number: " + image_name)

    @staticmethod
    def create_folder_for_results(path, folder_name):
        """creating folder for results"""
        os.mkdir(path + "\\" + folder_name)

    @staticmethod
    def write_histogram_similar_images(path, list_to_write):
        path = path + "\\results"

        origin_image_path = "origin_image_path"
        origin_image_name = "origin_image_name"
        to_compare_image_path = "to_compare_image_path"
        to_compare_image_name = "to_compare_image_name"
        score = "score"

        with open(os.path.join(path, 'HistogramResults.csv'), "w") as f:
            csvwriter = csv.writer(f, delimiter=' ', lineterminator='\n')
            csvwriter.writerow(origin_image_path + "," + origin_image_name + "," + to_compare_image_path +
                               "," + to_compare_image_name + "," + score)
            for line in list_to_write:
                csvwriter.writerow(line)

    @staticmethod
    def write_features_similar_images_results(path, list_to_write):
        path = path + "\\results"

        origin_image_path = "origin_image_path"
        origin_image_name = "origin_image_name"
        to_compare_image_path = "to_compare_image_path"
        to_compare_image_name = "to_compare_image_name"
        score = "score"

        with open(os.path.join(path, 'FeaturesResults.csv'), "w") as f:
            csvwriter = csv.writer(f, delimiter=' ', lineterminator='\n')
            csvwriter.writerow(origin_image_path + "," + origin_image_name + "," + to_compare_image_path + "," +
                               to_compare_image_name + "," + score)
            for line in list_to_write:
                csvwriter.writerow(line)

    @staticmethod
    def create_sub_folders_in_pic_folder(images_list):
        for image in images_list:
            path_to_pic_folder = image[0] + "\\" + image[1].split(".")[0]
            if not os.path.isdir(path_to_pic_folder + "\\" + "cropped"):
                os.mkdir(path_to_pic_folder + "\\" + "cropped")
                os.mkdir(path_to_pic_folder + "\\" + "rotated")
                os.mkdir(path_to_pic_folder + "\\" + "median")
                os.mkdir(path_to_pic_folder + "\\" + "mirrored")
                os.mkdir(path_to_pic_folder + "\\" + "vintage")
                os.mkdir(path_to_pic_folder + "\\" + "greyscale")

    def write_store_results_to_file(self, stores_path, in_depth_results : List[InDepthIP]):
        file_name = stores_path + "/results.csv"
        if os.path.isfile(file_name):
            os.remove(file_name)
        with open(file_name,'w',newline='') as csv_file:
            csvwriter = csv.writer(csv_file ,delimiter=' ',lineterminator = '\n')
            origin_image_path = "origin_image_path"
            origin_image_name = "origin_image_name"
            to_compare_image_path = "to_compare_image_path"
            to_compare_image_name = "to_compare_image_name"
            score = "score"
            csvwriter.writerow(origin_image_path + "," + origin_image_name + "," + to_compare_image_path +
                               "," + to_compare_image_name + "," + score)
            for row in in_depth_results:
                csvwriter.writerow(row)

    def write_final_results_file(self,stores_path, in_depth_results : List[InDepthIP]):
        file_name = stores_path + "/final_results.csv"
        with open(file_name,'w',newline='') as csv_file:
            csvwriter = csv.writer(csv_file ,delimiter=' ',lineterminator = '\n')
            origin_image_path = "origin_image_path"
            origin_image_name = "origin_image_name"
            to_compare_image_path = "to_compare_image_path"
            to_compare_image_name = "to_compare_image_name"
            score = "score"
            csvwriter.writerow(origin_image_path + "," + origin_image_name + "," + to_compare_image_path +
                               "," + to_compare_image_name + "," + score)
            for row in in_depth_results:
                csvwriter.writerow(row)

    def merge_final_results_file_and_new_results(self, stores_path, in_depth_results : List[InDepthIP]):
        file_name = stores_path + "/final_results.csv"
        new_results = [InDepthIP]
        old_file_index = 1
        in_depth_results_index = 0
        with open(file_name, newline='') as csvfile:
            old_results_list = [line.rstrip() for line in csvfile]
            while old_file_index < len(old_results_list) and in_depth_results_index < len(in_depth_results):
                old_score = old_results_list[old_file_index][4]
                if old_score > in_depth_results[in_depth_results_index]:
                    new_results.append(old_results_list[old_file_index])
                    old_file_index += 1
                else:
                    new_results.append(in_depth_results[in_depth_results_index])
                    in_depth_results_index += 1
            while old_file_index < len(old_results_list):
                new_results.append(old_results_list[old_file_index])
                old_file_index += 1
            while in_depth_results_index < len(in_depth_results):
                new_results.append(old_results_list[old_file_index])
                old_file_index += 1
        csvfile.close()
        os.remove(file_name)
        self.write_final_results_file(stores_path,new_results)


    def update_final_results_file(self, stores_path, in_depth_results : List[InDepthIP]):
        file_name = stores_path + "/final_results.csv"
        if os.path.isfile(file_name):
            self.merge_final_results_file_and_new_results(stores_path,in_depth_results)
        else:
            self.write_final_results_file(stores_path,in_depth_results)