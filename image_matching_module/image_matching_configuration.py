from decimal import Decimal
from typing import List, Tuple, Dict
from image_matching_module.algorithms.comparison_algorithm import ComparisonAlgorithm as algorithm
from image_matching_module.algorithms.bhattacharyya_comparison_algorithm import BhattacharyyaComparisonAlgorithm
from image_matching_module.algorithms.correlation_comparison_algorithm import CorrelationComparisonAlgorithm
from image_matching_module.algorithms.intersection_comparison_algorithm import IntersectionComparisonAlgorithm
from image_matching_module.algorithms.orb_feature_comparisson_algorithm import ORBFeatureComparisonAlgorithm


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

    # TODO: need to everything from the configuration file.
    def __init__(self):
        alg_names_dict = {'bhattacharyya': BhattacharyyaComparisonAlgorithm(),
                          'correlation': CorrelationComparisonAlgorithm(),
                          'intersection': IntersectionComparisonAlgorithm(),
                          'orb_feature': ORBFeatureComparisonAlgorithm()}
        self.batch_size = self.__read_batch_size()
        self.initial_threshold, self.in_depth_threshold = self.__read_thresholds()
        self.initial_score_weight = self.__read_initial_score_weight()
        self.initial_algorithms_weights = self.__read_initial_algorithms_and_weights(alg_names_dict)
        self.in_depth_algorithms_weights = self.__read_in_depth_algorithms_and_weights(alg_names_dict)

    def __read_batch_size(self) -> int:
        """
        Reads the batch size from the configuration file.

        :return: the batch size from the configuration file.
        """
        return 100

    def __read_thresholds(self) -> [Decimal, Decimal]:
        """
        Reads the initial and in-depth thresholds from the configuration file.

        :return: the initial threshold and the in-depth threshold.
        """
        return Decimal('0.87'), Decimal('0.64')

    def __read_initial_score_weight(self) -> Decimal:
        """
        Reads the initial score weight (as part of the in-depth filtering) from the
        configurations file.

        :return: the initial score weight for the in-depth filtering.
        """
        return Decimal('0.5')

    def __read_initial_algorithms_and_weights(self,
                                              alg_names_dict: Dict[str, algorithm]) -> List[Tuple[algorithm, Decimal]]:
        """
        Reads the initial algorithms names and weights from the configuration file
        and returns a list with the actual algorithms and their respective weights
        in tuples.

        :param alg_names_dict: a dictionary for getting an actual algorithm instance
        given the algorithm's name.
        :return: a list with the actual algorithms and their respective weights, in tuples.
        """
        return [(alg_names_dict['bhattacharyya'], Decimal('0.7')),
                (alg_names_dict['correlation'], Decimal('0.25')),
                (alg_names_dict['intersection'], Decimal('0.05'))]

    def __read_in_depth_algorithms_and_weights(self,
                                               alg_names_dict: Dict[str, algorithm]) -> List[Tuple[algorithm, Decimal]]:
        """
        Reads the in depth algorithms names and weights from the configuration file
        and returns a list with the actual algorithms and their respective weights
        in tuples.

        :param alg_names_dict: a dictionary for getting an actual algorithm instance
        given the algorithm's name.
        :return: a list with the actual algorithms and their respective weights, in tuples.
        """
        return [(alg_names_dict['orb_feature'], Decimal('1.0'))]
