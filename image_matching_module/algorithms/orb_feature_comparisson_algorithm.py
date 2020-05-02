import cv2
from image_matching_module.algorithms.feature_comparison_algorithm import FeatureComparisonAlgorithm


class ORBFeatureComparisonAlgorithm(FeatureComparisonAlgorithm):

    def __init__(self):
        FeatureComparisonAlgorithm.__init__(self,"orb_features")
        self.orb = cv2.ORB_create(nfeatures=5000,scaleFactor=1.3,nlevels=8, edgeThreshold=60, firstLevel=0, WTA_K=3)
        self.bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    def calculate_features_matches(self,description1, description2, description3):
        """
            Calculate the number of matches between the given descriptions of the images.

            Parameters:
               bf (BFMatcher): The given matcher to compare between the images.
               description1 (ndarray): The given descriptions of the features of origin image.
               description2 (ndarray): The given descriptions of the features of to compare image.
               description3 (ndarray): The given descriptions of the features of horizontal origin image.

            Returns:
                matches_origin_to_compare: The matches between the origin image and the to compare.
                matches_origin_horizontal_to_compare: The matches between the horizontal origin image and the to compare.
        """
        matches_origin_to_compare = self.bf.match(description1, description2)
        matches_origin_horizontal_to_compare = self.bf.match(description3, description2)
        return matches_origin_to_compare, matches_origin_horizontal_to_compare

    def detect_and_compute(self, origin_image, to_compare_image, origin_image_mirror_horizontal):
        """"
            Compute the key points and their descriptions of the three images

            Parameters:
               orb (ORB): The object to detect features in am image.
               origin_image (ndarray): The origin image as ndarry.
               to_compare_image (ndarray): The to compare image as ndarry.
               origin_image_mirror_horizontal (ndarray): The origin mirror to horizontal image as ndarry.

            Returns:
                The key points and the descriptions of the key points of the three images.
        """
        key_points1, description1 = self.orb.detectAndCompute(origin_image, None)
        key_points2, description2 = self.orb.detectAndCompute(to_compare_image, None)
        key_points3, description3 = self.orb.detectAndCompute(origin_image_mirror_horizontal, None)

        return key_points1, description1, key_points2, description2, key_points3, description3

    @staticmethod
    def calc_less_featuers(description1, description2):
        """
            Compare the number of features in two images.

            Parameters:
               description1 (ndarray): Object of features of first image.
               description2 (ndarray): Object of features of second image.
            Returns:
                The smaller number of features between the two images.
        """
        if len(description1) > len(description2):
            return len(description2)
        else:
            return len(description1)

    def calculate_less_features_matches(self,description1, description2, description3):

        less_features_origin_to_compare = self.calc_less_featuers(description1, description2)
        less_features_origin_horizontal_compare = self.calc_less_featuers(description3, description2)
        return less_features_origin_to_compare, less_features_origin_horizontal_compare

    @staticmethod
    def calculate_score_of_two_images(matches, less_features):
        """"
            calculate the score of by dividing the number of matches by less features.

            Parameters:
               matches (list): The list of matches.
               less_features (int): The given number of less features.

            Returns:
                The score of the compared matches divided by the less features in an image.
        """
        return len(matches) / less_features

    def calculate_score(self,origin_image, to_compare_image):

        origin_image_mirror_horizontal = FeatureComparisonAlgorithm.flipped_image_horizontal(origin_image)
        key_points1, description1, key_points2, description2, key_points3, description3 = self.detect_and_compute(origin_image,to_compare_image,origin_image_mirror_horizontal)

        # TODO : no to rethink this method, what is the mirrored has features but origion not?
        # if is_there_no_features_found(description1, description2, description3):
        #    return 0

        matches_origin_to_compare, matches_origin_horizontal_to_compare = self.calculate_features_matches(description1,
                                                                                                          description2,
                                                                                                          description3)

        less_features_origin_to_compare, less_features_origin_horizontal_compare = self.calculate_less_features_matches(description1, description2, description3)

        score_origin_to_compare = self.calculate_score_of_two_images(matches_origin_to_compare,
                                                                     less_features_origin_to_compare)
        score_origin_horizontal_to_compare = self.calculate_score_of_two_images(matches_origin_horizontal_to_compare,
                                                                                less_features_origin_horizontal_compare)

        return max(score_origin_to_compare,score_origin_horizontal_to_compare)
