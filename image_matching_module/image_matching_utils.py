from typing import List, Tuple, Any
from image_matching_module.initial_image_pair import InitialImagePair as InitialIPair
from image_matching_module.in_depth_image_pair import InDepthImagePair as InDepthIPair
from decimal import Decimal
from image_matching_module.algorithms.comparison_algorithm import ComparisonAlgorithm as comp_algorithm


class ImageMatchingUtils:
    """
    This class represents the utilities for the image matching module.
    """

    @staticmethod
    def get_images(image_pair: List[tuple]) -> [Tuple, Tuple]:
        """
        Gets the customer and store's image from a given image pair.

        :param image_pair: a list containing 3 tuples, the first and second being the customer
        and store images' properties.
        :return: two tuples for the customer and store images, each containing the image's
        name and image's vector representation.
        """
        customer_image = image_pair[0]
        store_image = image_pair[1]
        return customer_image, store_image

    @staticmethod
    def divide_images_to_batches(images_list: List[Tuple[str, str]], batch_size: int) -> List[List[Tuple[str, str]]]:
        """
        Divides a given images list to batches with a given batch size.
        
        :param images_list: a list of images' paths.
        :param batch_size: the size of each batch.
        :return: a list containing lists with images' paths that represent batches (each inner list is a batch).
        """
        list_of_batches = []
        for i in range(0, len(images_list), batch_size):
            list_of_batches.append(images_list[i:i + batch_size])
        return list_of_batches

    @staticmethod
    def get_combined_initial_score(customer_path: str, customer_images_batch: List[List[str]],
                                   store_path: str, store_images_batch: List[List[str]],
                                   initial_algorithms: List[Tuple[comp_algorithm, Decimal]],
                                   initial_threshold: Decimal) -> List[InitialIPair]:
        """
        Calculates the combined weighted score of every initial algorithm and returns a list of
        InitialImagePair objects that passed the given threshold.

        :param customer_path: the customer images' directory path.
        :param customer_images_batch: a list of lists, each containing strings that represents customer images' paths.
        :param store_path: the store images' directory path.
        :param store_images_batch: a list of lists, each containing strings that represents store images' paths.
        :param initial_algorithms: a list of tuples, each containing an algorithm and its weight.
        :param initial_threshold: a Decimal representing the threshold to pass to initial score filtering.
        :return: a list of InitialImagePair objects containing only the image pairs that got a valid
        score from the initial filtering algorithms.
        """

        initial_score_passed_list = []
        for customer_image in customer_images_batch:

            for store_image in store_images_batch:
                weighted_score = 0.0

                # calculate the weighted score for for each algorithm
                for algorithm, weight in initial_algorithms:
                    algorithm_score = algorithm.calculate_score(customer_image[1], store_image[1])
                    weighted_score += algorithm_score * float(weight)

                # adds the pair to the initial filtering passed list if the weighted score passes the threshold
                if weighted_score >= float(initial_threshold):
                    initial_score_passed_list.append(
                        InitialIPair(customer_path, customer_image[0], store_path, store_image[0], weighted_score))
        return initial_score_passed_list

    @staticmethod
    def get_combined_in_depth_score(image_pair_batch: List[List[Tuple]],
                                    in_depth_algorithms: List[Tuple[comp_algorithm, Decimal]],
                                    initial_score_weight: Decimal,
                                    in_depth_threshold: Decimal) -> List[InDepthIPair]:
        """
        Calculates the combined weighted score of every in-depth algorithm, and the weighted score of
        the initial filtering, and returns a list of InitialImagePair objects that passed the given threshold.

        :param image_pair_batch: a list, representing a batch of image pairs, containing lists of 3 tuples that
        represent an image pair. Each tuple list contains the customer image and image name in the first tuple,
        the store's image and image name in the second tuple and additional image pair properties in the third tuple.
        :param in_depth_algorithms: a list of tuples, each containing an algorithm and its weight.
        :param initial_score_weight: a Decimal representing the weight of the initial filtering score, as part of
        the in depth filtering total score.
        :param in_depth_threshold: a Decimal representing the threshold to pass to in depth score filtering.
        :return: a list of InDepthImagePair objects containing only the image pairs that got a valid score
        from the in depth filtering algorithms.
        """

        in_depth_passed_list = []

        # calculate the final score for each image pair
        for image_pair in image_pair_batch:
            combined_in_depth_score = 0.0
            customer_image, store_image = ImageMatchingUtils.get_images(image_pair)
            initial_score = image_pair[2][0]
            customer_image_path = image_pair[2][1]
            store_image_path = image_pair[2][2]

            # get the weighted score for each in depth algorithm
            for algorithm, weight in in_depth_algorithms:
                algorithm_score = algorithm.calculate_score(customer_image[1], store_image[1])
                combined_in_depth_score += algorithm_score * float(weight)

            # calculate the final score gathered from the weighted initial score and weighted combined in depth score
            weighted_final_score = float(initial_score_weight) * initial_score + \
                                   float((Decimal('1') - initial_score_weight)) * combined_in_depth_score

            # adds the pair to the in depth filtering passed list if the weighted score passes the threshold
            if weighted_final_score >= in_depth_threshold:
                in_depth_passed_list.append(InDepthIPair(customer_image_path, customer_image[0], store_image_path,
                                                         store_image[0], weighted_final_score))

        # sort the in depth final list by final score
        in_depth_passed_list.sort(key=lambda x: x.final_score, reverse=True)

        return in_depth_passed_list
