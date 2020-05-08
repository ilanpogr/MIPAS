from image_matching_module.reading_utils import ReadingUtils as RU
from pathlib import Path
import pandas as pd
from decimal import Decimal
from typing import List
import time
import os


class FNDetectionExperiment:
    """class that represents an experiment for getting the false negative results of each algorithm"""

    @staticmethod
    def run_fn_detection_experiment(path_to_csv_files,
                                    initial_algorithms_weights_thresholds,
                                    in_depth_algorithm_weight_threshold,
                                    combined_initial_threshold, combined_in_depth_threshold,
                                    combined_initial_score_weight):
        """
        get all images that were counted as False Negative (FN) in each algorithm / algorithm combinations
        """
        starting_time = time.time()
        print("started FN detection experiment")

        csv_paths_list = RU.read_all_csv_paths_from_path(path_to_csv_files)
        file_number = 1

        for csv_path in csv_paths_list:
            if 'total' in csv_path:
                continue
            df = pd.read_csv(csv_path)
            start_file_time = time.time()
            print("started file number:", file_number)
            for index, row in df.iterrows():
                # get the actual score of the image pair
                actual_score = row['actual_score']
                # no reason to check the image pair if it's not a Positive match (possibility for False Negative - FN)
                if actual_score == 1:
                    customer_image_directory_name = row['customer_image'].split('.')[0]
                    store_image_name = row['to_compare_image']
                    combined_initial_score = 0.0
                    combined_in_depth_score = 0.0
                    # check if the image pair is a FN in each initial algorithm
                    for algorithm, weight, threshold in initial_algorithms_weights_thresholds:
                        algorithm_column_name = algorithm.get_algorithm_name() + "_actual"
                        algorithm_score = row[algorithm_column_name]
                        combined_initial_score += combined_initial_score + algorithm_score * float(weight)
                        # check if its a False Negative results
                        if algorithm_score < threshold:
                            FNDetectionExperiment.add_store_images_to_fn_list(algorithm,
                                                                              customer_image_directory_name,
                                                                              store_image_name)
                    # check if the image pair is a FN in the combined initial algorithms score
                    if combined_initial_score < combined_initial_threshold:
                        # create both directories (if they don't exist)
                        full_customer_image_dir_path = 'initials_combined/' + customer_image_directory_name
                        Path('initials_combined/').mkdir(exist_ok=True)
                        Path(full_customer_image_dir_path).mkdir(exist_ok=True)
                        # add the customer image's name to a text file in the folder (create it if it doesn't exist)
                        with open(full_customer_image_dir_path + '/store_files.txt', 'a') as store_files:
                            store_files.write(store_image_name + "\n")
                    # check if the image pair is a FN in each in depth algorithm
                    for algorithm, weight, threshold in in_depth_algorithm_weight_threshold:
                        algorithm_column_name = algorithm.get_algorithm_name() + "_actual"
                        algorithm_score = row[algorithm_column_name]
                        combined_in_depth_score += combined_in_depth_score + algorithm_score * float(weight)
                        # check if its a False Negative results
                        if algorithm_score < threshold:
                            FNDetectionExperiment.add_store_images_to_fn_list(algorithm,
                                                                              customer_image_directory_name,
                                                                              store_image_name)

                    total_in_depth_score = combined_initial_score * float(combined_initial_score_weight) \
                                           + float((Decimal('1') - combined_initial_score_weight)) \
                                           * combined_in_depth_score

                    # check if the image pair is a FN in the total in depth score
                    if total_in_depth_score < combined_in_depth_threshold:
                        # create both directories (if they don't exist)
                        full_customer_image_dir_path = 'in_depth_combined/' + customer_image_directory_name
                        Path('in_depth_combined/').mkdir(exist_ok=True)
                        Path(full_customer_image_dir_path).mkdir(exist_ok=True)
                        # add the customer image's name to a text file in the folder (create it if it doesn't exist)
                        with open(full_customer_image_dir_path + '/store_files.txt', 'a') as store_files:
                            store_files.write(store_image_name + "\n")

            finish_file_time = time.time()
            print("finished file number:", file_number)
            print("file number:", file_number, "took:", (finish_file_time - start_file_time) / 60, "minutes")
            file_number += 1

        finish_time = time.time()
        hours = int((finish_time - starting_time) // 3600)
        minutes = (finish_time - starting_time) / 60
        print("finished FN detection experiment")
        print("time took:", hours, "hours and", minutes, "minutes")

    @staticmethod
    def add_store_images_to_fn_list(algorithm, customer_image_directory_name, store_image_name):
        # create both directories (if they don't exist)
        full_customer_image_dir_path = algorithm.get_algorithm_name() + '/' \
                                       + customer_image_directory_name
        Path(algorithm.get_algorithm_name()).mkdir(exist_ok=True)
        Path(full_customer_image_dir_path).mkdir(exist_ok=True)
        # add the customer image's name to a text file in the folder (create it if doesn't exist)
        with open(full_customer_image_dir_path + '/store_files.txt', 'a') as store_files:
            store_files.write(store_image_name + "\n")

    @staticmethod
    def get_list_of_files(dir_name: str):
        # create a list of file and sub directories
        # names in the given directory
        list_of_file = os.listdir(dir_name)
        all_files = list()
        # Iterate over all the entries
        for entry in list_of_file:
            # Create full path
            full_path = os.path.join(dir_name, entry)
            # If entry is a directory then get the list of files in this directory
            if os.path.isdir(full_path):
                all_files = all_files + FNDetectionExperiment.get_list_of_files(full_path)
            else:
                all_files.append(full_path)
        return all_files

    @staticmethod
    def get_count_of_fn_types(path_to_fn_results: str, algorithm_names: List[str], results_path: str):
        dict_for_df = {'algorithm': [], 'vintage1': [], 'vintage2': [], 'vintage3': [], 'cropped': [],
                       'greyscale': [], 'withText': [], 'watermark': [], 'rotate': [], 'mirrored': [], 'median': []}
        for algorithm_name in algorithm_names:
            dict_for_df['algorithm'].append(algorithm_name)
            manipulation_dict = {'vintage1': 0, 'vintage2': 0, 'vintage3': 0, 'cropped': 0, 'greyscale': 0,
                                 'withText': 0, 'watermark': 0, 'rotate': 0, 'mirrored': 0, 'median': 0}
            list_of_files_paths = FNDetectionExperiment.get_list_of_files(path_to_fn_results + '\\' + algorithm_name)
            for file_path in list_of_files_paths:
                with open(file_path) as txt_file:
                    line = txt_file.readline()
                    while line:
                        edited_line = line.strip('\n').split('.')[0]
                        edited_line = edited_line.lstrip('0123456789')
                        if 'vintage' not in edited_line:
                            edited_line = edited_line.rstrip('0123456789')
                        if 'mirrored' in edited_line:
                            edited_line = 'mirrored'
                        manipulation_dict[edited_line] = manipulation_dict[edited_line] + 1
                        line = txt_file.readline()

            for key, value in manipulation_dict.items():
                dict_for_df[key].append(value)

        # create a DataFrame from the dictionary
        df = pd.DataFrame(dict_for_df)

        # write the results into a csv file
        df.to_csv(results_path + '/fn_experiment_results.csv', index=False, header=True)

