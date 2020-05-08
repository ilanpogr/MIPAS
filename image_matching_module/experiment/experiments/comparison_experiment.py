import itertools
import os
import time
import pandas as pd
from image_matching_module.reading_utils import ReadingUtils


class ComparisonExperiment:
    """class that represents an image_matching_module on image matching algorithms"""

    def __init__(self, path_to_origin, path_to_compared):
        self.reader = ReadingUtils()
        self.origin_path = path_to_origin
        self.compared_path = path_to_compared
        self.actual_score_dict = {}
        self.fill_actual_score_dict()
        self.column_names = []

    def run_experiment(self, algorithms):
        starting_time = time.time()
        splitted_path = os.path.abspath(__file__).split("/")
        if not os.path.isdir("/".join(splitted_path[:-1]) + "/results"):
            os.mkdir("/".join(splitted_path[:-1]) +"/results")

        batch_number = 1
        differences_sums_total = {}

        for algorithm in algorithms:
            differences_sums_total[algorithm.get_algorithm_name() + "_difference"] = 0
        print("started comparison image_matching_module")
        # first for loop is for every batch of compared images, without loading all the batches
        to_compare_images_paths = self.reader.get_images_names_in_folder(self.compared_path)
        to_compare_batches = self.divide_images_to_batches(to_compare_images_paths)
        for to_compare_batch in to_compare_batches:
            to_compare_images_batch = self.reader.reading_all_images_from_given_tuple_path_list(to_compare_batch)
            # second (inner) for loop is for every batch of customer images, without loading all the batches
            customer_images_paths = self.reader.get_images_names_in_folder(self.origin_path)
            customer_images_batches = self.divide_images_to_batches(customer_images_paths)
            for customer_batch in customer_images_batches:
                # df = self.create_data_frame(algorithms)
                customer_images_batch = self.reader.reading_all_images_from_given_tuple_path_list(customer_batch)

                pair_dict_dict = {}
                first_run = True
                print("started histogram batch comparison number:", batch_number)
                start_batch_time = time.time()
                for algorithm in algorithms:
                    # get all scores for the current algorithm for the current batch pair
                    algorithm_score_dict = algorithm.run(customer_images_batch, to_compare_images_batch)

                    # change all algorithm scores to be the difference from the actual score
                    # and create dictionaries for the final dataframe
                    for image_pair in algorithm_score_dict:
                        actual_score = self.actual_score_dict.get(image_pair)
                        algorithm_score = algorithm_score_dict.get(image_pair)
                        algorithm_difference_column_name = algorithm.get_algorithm_name() + "_difference"
                        algorithm_score_column_name = algorithm.get_algorithm_name() + "_actual"
                        if actual_score == 1:
                            difference_score = actual_score - algorithm_score
                        else:
                            difference_score = algorithm_score

                        if first_run:
                            pair_dict_dict[image_pair] = {'customer_image': image_pair[0],
                                                          'to_compare_image': image_pair[1],
                                                          'actual_score': actual_score,
                                                          algorithm_score_column_name: algorithm_score,
                                                          algorithm_difference_column_name: difference_score}
                        else:
                            pair_dict_dict[image_pair][algorithm_score_column_name] = algorithm_score
                            pair_dict_dict[image_pair][algorithm_difference_column_name] = difference_score

                    first_run = False

                finish_batch_time = time.time()
                print("finished histogram batch comparison number:", batch_number)
                print("batch number:", batch_number , "took:", (finish_batch_time - start_batch_time) / 60 , "minutes")

                # initialize the batch dictionary with the appropriate keys
                ingestion_dict = {'customer_image': [],
                                 'to_compare_image': [],
                                 'actual_score': []}
                for algorithm in algorithms:
                    algorithm_difference_column_name = algorithm.get_algorithm_name() + "_difference"
                    algorithm_score_column_name = algorithm.get_algorithm_name() + "_actual"
                    ingestion_dict[algorithm_score_column_name] = []
                    ingestion_dict[algorithm_difference_column_name] = []

                # add all pair dictionaries into the ingestion dictionary
                for pair_dict in pair_dict_dict.values():
                    ingestion_dict['customer_image'].append(pair_dict['customer_image'])
                    ingestion_dict['to_compare_image'].append(pair_dict['to_compare_image'])
                    for key, value in pair_dict.items():
                        if key != 'customer_image' and key != 'to_compare_image':
                            ingestion_dict[key].append(value)

                # add all image pairs' results to dataframe
                df = pd.DataFrame(ingestion_dict)

                # write dataframe to a csv file
                csv_file_name = os.path.dirname("/".join(splitted_path)) + "/results/batch_number" + str(batch_number) +".csv"
                df.to_csv(csv_file_name, index=False, header=True)

                ## write local differences sum to csv
                differences_sums_local = df.select_dtypes(pd.np.number).sum().rename('total_differences')
                differences_sums_temp_dict = differences_sums_local.to_dict()
                differences_sums_local_dict = {}
                for name, value in differences_sums_temp_dict.items():
                    if '_difference' in name:
                        differences_sums_local_dict[name] = [value]
                differences_sums_local_df = pd.DataFrame(differences_sums_local_dict)
                differences_sums_local_file_name = os.path.dirname("/".join(splitted_path)) + "/results/" + "batch_number" + str(batch_number) +"_total.csv"
                differences_sums_local_df.to_csv(differences_sums_local_file_name, index=False, header=True)

                # total differences
                for name,difference in itertools.zip_longest(differences_sums_local.index, differences_sums_local):
                    if "_difference" in name:
                        differences_sums_total[name] = differences_sums_total[name] + difference

                batch_number += 1

        for name,difference in differences_sums_total.items():
            if name in differences_sums_total.keys():
                differences_sums_total[name] = [difference]

        df_total_sums = pd.DataFrame(differences_sums_total)

        csv_file_name_total = os.path.dirname("/".join(splitted_path)) + "/results/total_differences.csv"
        df_total_sums.to_csv(csv_file_name_total,index=False,header=True)

        finish_time = time.time()
        hours = int((finish_time - starting_time) // 3600)
        minutes = (finish_time - starting_time) / 60
        print("finished comparison image_matching_module")
        print ("time image_matching_module took:" ,hours , "hours and", minutes , "minutes")
        print("results:")
        for algorithm_difference, difference in differences_sums_total.items():
            print(algorithm_difference , "->" , str(difference))

    def fill_actual_score_dict(self):
        """fills the actual score dictionary with the actual scores for all image pairs"""
        customer_images_names = self.reader.get_images_names_in_folder(self.origin_path)
        for customer_image in customer_images_names:
            customer_image_name = customer_image[1].split(".")[0]
            images_names = self.reader.get_images_names_in_folder(self.compared_path)
            for image_name in images_names:
                image_pair = (customer_image[1], image_name[1])
                splitted_image_path = image_name[0].split("/")
                to_compare_image_directory = splitted_image_path[len(splitted_image_path) - 2]
                if customer_image_name == to_compare_image_directory:
                    self.actual_score_dict[image_pair] = 1
                else:
                    self.actual_score_dict[image_pair] = 0

    def divide_images_to_batches(self, image_list):
        list_of_batchers = []
        for i in range(0, len(image_list), 52):
            list_of_batchers.append(image_list[i:i + 52])
        return list_of_batchers
