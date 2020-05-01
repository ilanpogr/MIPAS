from random import random
from image_matching_module.algorithms.comparison_algorithm import ComparisonAlgorithm


class RandomComparisonAlgorithm(ComparisonAlgorithm):

    def __init__(self):
        super().__init__("random")

    def run(self, customer_images, compared_images):
        passed_test = {}
        for to_compare_image in compared_images:
            for origin_image in customer_images:
                # create a tuple for the compared pairs
                image_pair_tuple = (origin_image[0],to_compare_image[0])

                # get the score
                score = random()

                # insert the pair's score into the dictionary
                passed_test[image_pair_tuple] = score
        return passed_test
