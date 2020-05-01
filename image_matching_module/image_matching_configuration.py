from decimal import Decimal
from image_matching_module.algorithms.bhattacharyya_comparison_algorithm import BhattacharyyaComparisonAlgorithm
from image_matching_module.algorithms.correlation_comparison_algorithm import CorrelationComparisonAlgorithm
from image_matching_module.algorithms.intersection_comparison_algorithm import IntersectionComparisonAlgorithm
from image_matching_module.algorithms.orb_feature_comparisson_algorithm import ORBFeatureComparisonAlgorithm


class ImageMatchingConfiguration:

    # TODO: read from the configuration file the correct numbers.
    def __init__(self):
        alg_name_to_alg_dict = {'bhattacharyya': BhattacharyyaComparisonAlgorithm(),
                                'correlation': CorrelationComparisonAlgorithm(),
                                'intersection': IntersectionComparisonAlgorithm(),
                                'orb_feature': ORBFeatureComparisonAlgorithm()}
        self.batch_size = 100
        self.initial_threshold = Decimal('0.87')
        self.in_depth_threshold = Decimal('0.64')
        self.initial_score_weight = Decimal('0.5')
        self.initial_algorithms_weights = [(alg_name_to_alg_dict['bhattacharyya'], Decimal('0.7')),
                                           (alg_name_to_alg_dict['correlation'], Decimal('0.25')),
                                           (alg_name_to_alg_dict['intersection'], Decimal('0.05'))]
        self.in_depth_algorithms_weights = [(alg_name_to_alg_dict['orb_feature'], Decimal('1.0'))]
