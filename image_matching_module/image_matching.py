from image_matching_module.image_matching_utils import ImageMatchingUtils as IMU
from image_matching_module.in_depth_image_pair import InDepthImagePair as InDepthIP
from image_matching_module.initial_image_pair import InitialImagePair as InitialIP
from image_matching_module.reading_module import ReadingModule as RM
from image_matching_module.writing_module import WritingModule as WM
from image_matching_module.image_matching_configuration import ImageMatchingConfiguration as IMC
from typing import List


class ImageMatching:

    def __init__(self, customer_path: str, stores_path: str, configurations: IMC, reading_module: RM,
                 writing_module: WM):
        self.customer_path = customer_path
        self.stores_path = stores_path
        self.settings = configurations
        self.reader = reading_module
        self.writer = writing_module

    def run_matching_for_all_stores(self):
        """run image comparison for all the customer's images with all stores"""

        customer_images_paths = self.reader.get_images_names_in_folder(self.customer_path)
        store_paths = self.reader.reading_all_folders_in_given_path(self.stores_path)

        for store_path in store_paths:
            self.run_matching_for_store(customer_images_paths, store_path)

    def run_matching_for_store(self, customer_images_paths, store_path):
        """run image comparison for all the customer's images with the given store"""

        # if we wanted to run image matching only for a single store, we don't get the customer images paths beforehand
        if customer_images_paths is None:
            customer_images_paths = self.reader.get_images_names_in_folder(self.customer_path)

        # get image paths of all images of the store
        store_images_paths = self.reader.get_images_names_in_folder(store_path)

        # run initial image matching on all store images
        initial_results = self.run_initial_filtering(customer_images_paths, store_images_paths)

        # run in-depth image matching on all images that passed the initial filtering
        in_depth_results = self.run_in_depth_filtering(initial_results)

        # write results to store results file (overwrite old file if exists)
        self.writer.write_store_results_to_file(store_path,in_depth_results)

        # check if there is a final results file
        # if no -> create it and write the results to it
        # if yes -> read its first record and compare with in-depths result first record.
        # if in-depth results has a higher score -> write it to the new final results file
        # else -> write the first record to the new results file and pull the next record from the old results file
        # repeat this until both in depth list and final results file are empty
        self.writer.update_final_results_file(self.stores_path,in_depth_results)
        # delete old final results file

        # rename new final results file

    def run_initial_filtering(self, customer_images_paths, store_images_paths) -> List[InitialIP]:
        """runs initial filtering by image matching for given customer images and store images"""

        # getting the paths to the store so it will be able to add the path to the initial_score
        customer_path = customer_images_paths[0][0]
        store_path = store_images_paths[0][0]

        # divide customer and image paths to batches
        customer_images_batches = IMU.divide_images_to_batches(customer_images_paths, self.settings.batch_size)
        store_images_batches = IMU.divide_images_to_batches(store_images_paths, self.settings.batch_size)

        # run initial comparison algorithms according to given weights [list(algorithm, weight)]
        total_initial_results = []
        for customer_images_batch in customer_images_batches:

            customer_images_batch = self.reader.reading_all_images_from_given_tuple_path_list(customer_images_batch)

            for store_images_batch in store_images_batches:
                store_images_batch = self.reader.reading_all_images_from_given_tuple_path_list(store_images_batch)
                # combine results from all initial comparison algorithms according to given weights
                initial_batch_results = IMU.get_combined_initial_score(customer_path, customer_images_batch, store_path,
                                                                       store_images_batch,
                                                                       self.settings.initial_algorithms_weights,
                                                                       self.settings.initial_threshold)
                total_initial_results.extend(initial_batch_results)

        return total_initial_results

    def run_in_depth_filtering(self, initial_results: List[InitialIP]) -> List[InDepthIP]:
        """runs in depth filtering by image matching for given customer images and store images"""

        # divide initial results to batches
        image_pairs_batches = IMU.divide_images_to_batches(initial_results, self.settings.batch_size)

        # run in-depth comparison algorithm(s) on pairs
        total_in_depth_results = []
        for image_pair_batch in image_pairs_batches:
            # image_pairs_list -> [ [ (c1_name, c1_image), (s1_name, s1_image), (cs1_initial_score)],
            #                       [ (c2_name, c2_image), (s2_name, s2_image), (cs2_initial_score) ],
            #                       ................................................................ ]
            image_pairs_list = []
            for image_pair in image_pair_batch:
                image_pair_tuples = [(image_pair.customer_path, image_pair.customer_name),
                                     (image_pair.store_path, image_pair.store_name)]

                image_pair_data = self.reader.reading_all_images_from_given_tuple_path_list(image_pair_tuples)
                image_pair_data.append((image_pair.initial_score,))

                image_pairs_list.append(self.reader.reading_all_images_from_given_tuple_path_list(image_pair_tuples))

            in_depth_batch_results = IMU.get_combined_in_depth_score(image_pairs_list,
                                                                     self.settings.in_depth_algorithms_weights,
                                                                     self.settings.initial_score_weight,
                                                                     self.settings.in_depth_threshold)
            total_in_depth_results.extend(in_depth_batch_results)

        # sort results according to highest score
        total_in_depth_sorted_results = sorted(total_in_depth_results)

        return total_in_depth_sorted_results