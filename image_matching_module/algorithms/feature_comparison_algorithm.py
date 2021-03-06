import cv2
from image_matching_module.algorithms.comparison_algorithm import ComparisonAlgorithm
from image_matching_module import manipulation


class FeatureComparisonAlgorithm(ComparisonAlgorithm):
    def __init__(self, name_of_algorithm):
        super().__init__(name_of_algorithm)

    def calculate_score(self, origin_image, to_compare_image):
        pass

    def run(self, customer_images, compared_images):
        index = 1
        passed_features_test = {}
        for to_compare_image in compared_images:
            for origin_image in customer_images:

                # create a tuple for the compared pairs
                image_pair_tuple = (origin_image[0],to_compare_image[0])

                origin_image_mirror_horizontal = manipulation.flipped_image_horizontal(origin_image[1])

                # get the score
                score = self.calculate_score(origin_image[1], to_compare_image[1], origin_image_mirror_horizontal)

                index += 1
                # insert the pair's score into the dictionary
                passed_features_test[image_pair_tuple] = score

        return passed_features_test
