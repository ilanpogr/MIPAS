from image_matching_module.image_matching_utils import ImageMatchingUtils as IMU
from image_matching_module.in_depth_image_pair import InDepthImagePair as InDepthIP
from image_matching_module.initial_image_pair import InitialImagePair as InitialIP
from image_matching_module.reading_utils import ReadingUtils as RU
from image_matching_module.writing_utils import WritingUtils as WU
from image_matching_module.image_matching_configuration import ImageMatchingConfiguration as IMC
from typing import List, Tuple


class ImageMatching:
    """
    This class represents the image matching module, part of the MIPAS system.

    Attributes
    ----------
    customer_path : str
        a string that contains the path for the folder containing all the customer images.
    stores_path : str
        a string that contains the path for the folder containing all folders for all
        the stores to compare with.
    configurations : ImageMatchingConfiguration
        a class that holds all the settings for the image matching module.
    """

    def __init__(self, customer_path: str, stores_path: str):
        """
        :param customer_path: a string that contains the path for the folder containing
        all the customer images.
        :param stores_path: a string that contains the path for the folder containing
        all folders for all the stores to compare with.
        """
        self.__customer_path = customer_path
        self.__stores_path = stores_path
        self.__configurations = IMC()

    def run_matching_for_all_stores(self, signal_process, signal_status):
        """
        Run image comparison for all the customer's images with all stores and write the results to the
        final results file.
        """
        customer_images_paths = RU.get_images_names_in_folder(self.__customer_path)
        store_paths = RU.reading_all_folders_paths_in_given_path(self.__stores_path)

        counter = 0
        for store_path in store_paths:
            counter += 1
            store_name = store_path.split("/")[-1]
            current_status = str(counter) + "/" + str(len(store_paths)) + \
                             "\nComparing your images with products from store: " + store_name
            signal_status.emit(current_status)  # signal task
            self.run_matching_for_store(customer_images_paths, store_path)
            signal_process.emit(counter / len(store_paths) * 100)

    def run_matching_for_store(self, customer_images_paths: List[Tuple[str, str]], store_path: str):
        """
        Run image comparison for all the customer's images with a given store and write the results to the
        final results file.

        :param customer_images_paths: a list of tuples containing 2 strings that represent the path to an image
         and the image's name for all the customer's images.
        :param store_path: a string that contains the path for the folder of the store.
        """

        # if we want to run image matching only for a single store we don't get the customer
        # images paths beforehand
        if customer_images_paths is None:
            customer_images_paths = RU.get_images_names_in_folder(self.__customer_path)

        # get image paths of all images of the store
        store_images_paths = RU.get_images_names_in_folder(store_path)

        # run initial image matching on all store images
        initial_results = self.run_initial_filtering(customer_images_paths, store_images_paths)

        # run in-depth image matching on all images that passed the initial filtering
        in_depth_results = self.run_in_depth_filtering(initial_results)

        # write results to store results file (overwrite old file if exists)
        WU.write_store_results_to_file(store_path, in_depth_results)

        # get list of previous store results, if exists
        prev_store_results = RU.get_prev_store_results(store_path)

        # merge results with total results file (create one if doesn't exist)
        if prev_store_results is None:
            WU.update_final_results_file(self.__stores_path, in_depth_results)
        else:
            WU.update_final_results_file(self.__stores_path, in_depth_results, prev_store_results)

    def run_initial_filtering(self, customer_images_paths: List[Tuple[str, str]],
                              store_images_paths: List[Tuple[str, str]]) -> List[InitialIP]:
        """
        Run initial filtering for the image matching for given customer images and store images.

        :param customer_images_paths: a list of tuples containing 2 strings that represent the path to an image
         and the image's name for all the customer's images.
        :param store_images_paths: a list of tuples containing 2 strings that represent the path to an image
         and the image's name for all the store's images.
        :return: a list of InitialImagePair objects containing only the image pairs that got a valid
        score from the initial filtering algorithms.
        """

        # getting the paths to the store so it will be able to add the path to the initial_score
        customer_path = customer_images_paths[0][0]
        store_path = store_images_paths[0][0]

        # divide customer and image paths to batches
        customer_images_batches = IMU.divide_images_to_batches(customer_images_paths, self.__configurations.batch_size)
        store_images_batches = IMU.divide_images_to_batches(store_images_paths, self.__configurations.batch_size)

        # run initial comparison algorithms
        total_initial_results = []
        for customer_images_batch in customer_images_batches:
            # get all customer images for this batch
            customer_images_batch = RU.reading_all_images_from_given_tuple_path_list(customer_images_batch)
            for store_images_batch in store_images_batches:
                # get all store images for this batch
                store_images_batch = RU.reading_all_images_from_given_tuple_path_list(store_images_batch)

                # get combined weighted score of all initial comparison algorithms for all image pairs
                # that passed the initial threshold
                initial_batch_results = IMU.get_combined_initial_score(customer_path, customer_images_batch, store_path,
                                                                       store_images_batch,
                                                                       self.__configurations.initial_algorithms_weights,
                                                                       self.__configurations.initial_threshold)
                # add the batch's results to the total initial results list
                total_initial_results.extend(initial_batch_results)
        return total_initial_results

    def run_in_depth_filtering(self, initial_results: List[InitialIP]) -> List[InDepthIP]:
        """
        Run in depth filtering for the image matching for the image pairs that passed the initial
        image matching filtering.

        :param initial_results: a list of InitialImagePair objects containing only the image pairs
        that got a valid score from the initial filtering algorithms.
        :return: a list of InDepthImagePair objects containing only the image pairs
        that got a valid score from the in depth filtering algorithms.
        """

        # divide initial results to batches
        image_pairs_batches = IMU.divide_images_to_batches(initial_results, self.__configurations.batch_size)

        # run in-depth comparison algorithms on pairs
        total_in_depth_results = []
        for image_pair_batch in image_pairs_batches:
            image_pairs_list = []
            # image_pairs_list structure -> [ [ (c1_name, c1_image), (s1_name, s1_image)
            #                                   (cs1_initial_score, c1_image_path, s1_image_path) ],
            #                                 [ (c2_name, c2_image), (s2_name, s2_image),
            #                                   (cs2_initial_score, c2_image_path, s2_image_path) ],
            #                                 ...................................................  ]

            for image_pair in image_pair_batch:
                image_pair_tuples = [(image_pair.customer_image_path, image_pair.customer_image_name),
                                     (image_pair.store_image_path, image_pair.store_image_name)]

                # get customer and store images
                image_pair_data = RU.reading_all_images_from_given_tuple_path_list(image_pair_tuples)
                # add the initial score, the customer image path and the store image path for the current image pair
                image_pair_data.append((image_pair.initial_score, image_pair.customer_image_path,
                                        image_pair.store_image_path))
                # add the pair to the batch pair list
                image_pairs_list.append(image_pair_data)

            # get combined weighted score of all in depth comparison algorithms for all image pairs
            # that passed the in depth threshold
            in_depth_batch_results = IMU.get_combined_in_depth_score(image_pairs_list,
                                                                     self.__configurations.in_depth_algorithms_weights,
                                                                     self.__configurations.initial_score_weight,
                                                                     self.__configurations.in_depth_threshold)
            # add the batch's results to the total in depth results list
            total_in_depth_results.extend(in_depth_batch_results)

        # sort results according to highest score
        total_in_depth_results.sort(key=lambda x: x.final_score, reverse=True)

        return total_in_depth_results
