from typing import List, Tuple, Any
from image_matching_module.initial_image_pair import InitialImagePair as InitialIPair
from image_matching_module.in_depth_image_pair import InDepthImagePair as InDepthIPair
from decimal import Decimal
from image_matching_module.algorithms.comparison_algorithm import ComparisonAlgorithm as comp_algorithm


class ImageMatchingUtils:

    @staticmethod
    def get_images(image_pair: List[tuple]):
        customer_image = image_pair[0]
        store_image = image_pair[1]
        return customer_image, store_image

    @staticmethod
    def divide_images_to_batches(images_list, size) -> List[Tuple[Any]]:
        list_of_batches = []
        for i in range(0, len(images_list), size):
            list_of_batches.append(images_list[i:i + size])
        return list_of_batches

    @staticmethod
    def get_combined_initial_score(customer_path, customer_images_batch, store_path, store_images_batch,
                                   initial_algorithms: List[Tuple[comp_algorithm, Decimal]],
                                   initial_threshold: Decimal) -> List[InitialIPair]:
        initial_score_passed_list = []

        for customer_image in customer_images_batch:

            for store_image in store_images_batch:
                combined_score = 0.0

                for algorithm, weight in initial_algorithms:
                    algorithm_score = algorithm.calculate_score(customer_image[1], store_image[1])
                    combined_score += algorithm_score * weight

                if combined_score >= initial_threshold:
                    initial_score_passed_list.append(
                        InitialIPair(customer_path, customer_image[0], store_path, store_image[0], combined_score))

        return initial_score_passed_list

    @staticmethod
    def get_combined_in_depth_score(self, image_pair_batch: List[List[Tuple]],
                                    in_depth_algorithms: List[Tuple[comp_algorithm, Decimal]],
                                    initial_score_weight: Decimal,
                                    in_depth_threshold: Decimal) -> List[InDepthIPair]:

        in_depth_passed_list = []

        # calculate the final score for each image pair
        for image_pair in image_pair_batch:
            combined_in_depth_score = 0.0
            customer_image, store_image = self.get_images(image_pair)
            initial_score = image_pair[3][0]

            # get the weighted score for each in depth algorithm
            for algorithm, weight in in_depth_algorithms:
                algorithm_score = algorithm.calculate_score(customer_image[1], store_image[1])
                combined_in_depth_score += algorithm_score * weight

            # calculate the final score gathered from the weighted initial score and weighted combined in depth score
            combined_final_score = initial_score_weight * initial_score + \
                                   (Decimal('1') - initial_score_weight) * combined_in_depth_score

            if combined_final_score >= in_depth_threshold:
                in_depth_passed_list.append(InDepthIPair(customer_image[0], store_image[0], combined_final_score))

        # sort the in depth final list by final score
        in_depth_passed_list.sort(key=lambda x: x.final_score, reverse=True)

        return in_depth_passed_list
