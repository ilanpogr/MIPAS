from image_matching_module.reading_utils import ReadingUtils as RU
from image_matching_module.algorithms.comparison_algorithm import ComparisonAlgorithm as comparison_algorithm
from image_matching_module.image_matching_utils import ImageMatchingUtils as IMU
import pandas as pd
from typing import List
import time


class RunTimeExperiment:
    """
    class that represents a runtime experiment for the image matching algorithms
    """

    @staticmethod
    def run_runtime_experiment(algorithms: List[comparison_algorithm], results_path: str,
                               path_to_customer_images: str, path_to_store_images: str,
                               num_of_repeats: int):
        """
        Runs the runtime experiment for all given algorithms.

        :param algorithms: a list of comparison
        :param results_path:
        :param path_to_customer_images:
        :param path_to_store_images:
        :param num_of_repeats:
        :return:
        """

        dict_for_df = {'algorithms': [], 'average_runtime': []}

        customer_images_paths = RU.get_images_names_in_folder(path_to_customer_images)
        store_images_paths = RU.get_images_names_in_folder(path_to_store_images)

        customer_images_batch = IMU.divide_images_to_batches(customer_images_paths, 50)[0]
        store_images_batch = IMU.divide_images_to_batches(store_images_paths, 50)[0]

        customer_images = RU.reading_all_images_from_given_tuple_path_list(customer_images_batch)
        store_images = RU.reading_all_images_from_given_tuple_path_list(store_images_batch)

        for algorithm in algorithms:
            # run the code as the inputted number of repeats times
            start_time = time.perf_counter()
            for repeat in range(num_of_repeats):
                for customer_image in customer_images:
                    for store_image in store_images:
                        algorithm.calculate_score(customer_image[1], store_image[1])
            elapsed_algorithm_time_in_seconds = time.perf_counter() - start_time

            # get the average time for all comparisons
            avg_elapsed_algorithm_time_in_seconds = elapsed_algorithm_time_in_seconds / num_of_repeats

            # add the algorithm's result to the dictionary
            algorithm_name = algorithm.get_algorithm_name()
            dict_for_df['algorithms'].append(algorithm_name)
            dict_for_df['average_runtime'].append(avg_elapsed_algorithm_time_in_seconds)

        # create a DataFrame from the dictionary
        df = pd.DataFrame(dict_for_df)

        # write the results into a csv file
        df.to_csv(results_path + '/algorithms_runtime_results.csv', index=False, header=True)