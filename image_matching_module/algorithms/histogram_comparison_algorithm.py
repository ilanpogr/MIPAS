import cv2
from image_matching_module.algorithms.comparison_algorithm import ComparisonAlgorithm


class HistogramComparisonAlgorithm(ComparisonAlgorithm):

    def __init__(self, name_of_algorithm, threshold):
        super().__init__(name_of_algorithm)
        h_bins = 50
        s_bins = 60
        # hue varies from 0 to 179, saturation from 0 to 255
        h_range = [0, 180]
        s_range = [0, 256]
        self.hist_size = [h_bins, s_bins]
        self.ranges = h_range + s_range
        # Use the 0-th and 1-st channels
        self.channels = [0, 1]
        self.threshold = threshold

    def get_histogram_threshold_results(self, score):
        if score > self.threshold:
            return 1
        else:
            return 0

    def create_hist_pic(self, image):
        """creating histogram from an image."""
        image_hsv_base = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_hist_base = cv2.calcHist([image_hsv_base], self.channels, None, self.hist_size, self.ranges, accumulate=False)
        image_hist_base = cv2.normalize(image_hist_base, image_hist_base, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
        return image_hist_base

    def calculate_score(self, origin_hist_base, to_compare_hist_base):
        pass

    @staticmethod
    def normalize_bounbdries(dist):
        if dist < 0:
            dist = 0
        if dist > 1:
            dist = 1
        return dist

    def run(self, customer_images, compared_images):

        passed_histogram_test = {}
        for to_compare_image in compared_images:
            for origin_image in customer_images:

                # create a tuple for the compared pairs
                image_pair_tuple = (origin_image[0],to_compare_image[0])

                # histogram for the origin image
                customer_hist_base = self.create_hist_pic(origin_image[1])

                # histogram for the to_compare image
                to_compare_hist_base = self.create_hist_pic(to_compare_image[1])

                # get the score
                score = self.calculate_score(customer_hist_base, to_compare_hist_base)

                # insert the pair's score into the dictionary
                passed_histogram_test[image_pair_tuple] = score

        return passed_histogram_test
