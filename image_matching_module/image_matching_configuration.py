from decimal import Decimal
from typing import List, Tuple, Dict
from image_matching_module.algorithms.comparison_algorithm import ComparisonAlgorithm as algorithm
from image_matching_module.algorithms.bhattacharyya_comparison_algorithm import BhattacharyyaComparisonAlgorithm
from image_matching_module.algorithms.correlation_comparison_algorithm import CorrelationComparisonAlgorithm
from image_matching_module.algorithms.intersection_comparison_algorithm import IntersectionComparisonAlgorithm
from image_matching_module.algorithms.orb_feature_comparisson_algorithm import ORBFeatureComparisonAlgorithm
from image_matching_module.reading_module import ReadingModule as RM


class ImageMatchingConfiguration:
    """
    This class represents the configurations for the image matching module.

    Attributes
    ----------
    batch_size : int
        an integer that represents the amount of images compared in each batch.
    initial_threshold : Decimal
        a Decimal that represents the threshold for the initial filtering's score.
    in_depth_threshold : Decimal
        a Decimal that represents the threshold for the in depth filtering's score.
    initial_score_weight : Decimal
        a Decimal that represents the weight of the total initial filtering score as
        part of the in depth filtering.
    initial_algorithms_weights : List[Tuple[algorithm, Decimal]]
        a list of tuples containing an algorithm and its weight for the initial score filtering.
    in_depth_algorithms_weights : List[Tuple[algorithm, Decimal]]
        a list of tuples containing an algorithm and its weight for the in depth score filtering.
    """

    def __init__(self):
        alg_names_dict = {'bhattacharyya': BhattacharyyaComparisonAlgorithm(),
                          'correlation': CorrelationComparisonAlgorithm(),
                          'intersection': IntersectionComparisonAlgorithm(),
                          'orb_feature': ORBFeatureComparisonAlgorithm()}
        batch_size, initial_threshold, in_depth_threshold, initial_score_weight, \
        initial_algorithms_and_weights_dict, in_depth_algorithms_and_weights_dict = \
            RM.read_config_file("image_matching_configurations.txt")
        self.batch_size = int(batch_size)
        self.initial_threshold = Decimal(initial_threshold)
        self.in_depth_threshold = Decimal(in_depth_threshold)
        self.initial_score_weight = Decimal(initial_score_weight)
        self.initial_algorithms_weights = ImageMatchingConfiguration.create_algorithms_weights(alg_names_dict,
                                                                                               initial_algorithms_and_weights_dict)
        self.in_depth_algorithms_weights = ImageMatchingConfiguration.create_algorithms_weights(alg_names_dict,
                                                                                                in_depth_algorithms_and_weights_dict)

    @staticmethod
    def create_algorithms_weights(alg_names_dict, initial_algorithms_and_weights_dict):
        algorithms_weights_list = []
        for key, value in initial_algorithms_and_weights_dict.items():
            algorithms_weights_list.append((alg_names_dict[key], Decimal(value)))
        return algorithms_weights_list
