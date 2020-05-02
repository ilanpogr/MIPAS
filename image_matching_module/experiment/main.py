from decimal import Decimal
from image_matching_module.algorithms.random_comparison_algorithm import RandomComparisonAlgorithm
from image_matching_module.algorithms.bhattacharyya_comparison_algorithm import BhattacharyyaComparisonAlgorithm
from image_matching_module.algorithms.correlation_comparison_algorithm import CorrelationComparisonAlgorithm
from image_matching_module.algorithms.chisquared_comparison_algorithm import ChiSquaredComparisonAlgorithm
from image_matching_module.algorithms.orb_feature_comparisson_algorithm import ORBFeatureComparisonAlgorithm
from image_matching_module.experiment.experiments.comparison_experiment import ComparisonExperiment
from image_matching_module.algorithms.intersection_comparison_algorithm import IntersectionComparisonAlgorithm
from image_matching_module.experiment.experiments.precision_recall_experiment import PrecisionRecallExperiment
import itertools
from itertools import chain, permutations
from image_matching_module.image_matching import ImageMatching
from image_matching_module.image_matching_configuration import ImageMatchingConfiguration
from image_matching_module.writing_module import WritingModule
from image_matching_module.reading_module import ReadingModule
def main():

    experiment = ComparisonExperiment("/Users/avig/myStuff/final_project/test1", "/Users/avig/myStuff/final_project/test2")
    chi_squre = ChiSquaredComparisonAlgorithm()
    correlation = CorrelationComparisonAlgorithm()
    intersection = IntersectionComparisonAlgorithm()
    bhattacharyya = BhattacharyyaComparisonAlgorithm()
    orb_features = ORBFeatureComparisonAlgorithm(0.6)
    random = RandomComparisonAlgorithm()
    precision_recall_experiment = PrecisionRecallExperiment()
    algorithms = [chi_squre,correlation,intersection,bhattacharyya,random]
    # thresholds = [0.65,0.66,0.67,0.68,0.69,0.7,0.71,0.72,0.73,0.74,0.75,0.76,0.77,0.78,0.79,0.8,0.81,0.82,0.83,0.84,0.85,0.86,0.87,0.88,0.89,0.9]
    thresholds = []
    i = Decimal('0.30')
    while i <= 0.9:
        thresholds.append(i)
        i += Decimal('0.01')

    numbers = [Decimal('0.05'), Decimal('0.1'), Decimal('0.05'), Decimal('0.1'),
               Decimal('0.2'), Decimal('0.2'), Decimal('0.25'), Decimal('0.25'),
               Decimal('0.3'), Decimal('0.3'), Decimal('0.33'), Decimal('0.33'),
               Decimal('0.34'), Decimal('0.4'), Decimal('0.4'), Decimal('0.5'),
               Decimal('0.6'), Decimal('0.7'), Decimal('0.75'), Decimal('0.8'),
               Decimal('0.9')]
    new_results = get_all_permutations(numbers)

    algorithms_weights_list = []
    for new_result in new_results:
        algorithms_weights_list.append([(bhattacharyya, new_result[0]), (intersection, new_result[1]),
                          (correlation, new_result[2])])

    csv_path = "F:/avi/image_matching_module/results/precision_recall_results/"
    precision_recall_experiment.run_multiple_advanced_experiments(csv_path,algorithms_weights_list,thresholds)


def get_all_permutations(numbers):
    results = [seq for i in range(len(numbers), 0, -1) for seq in itertools.combinations(numbers, i)
               if sum(seq) == Decimal(1) and len(seq) == 3]
    new_results = []
    for result in results:
        result_list = list(result)
        splitted_results = list(chain.from_iterable(permutations(result_list, r) for r in range(len(result_list) + 1)))
        for splitted_result in splitted_results:
            if len(splitted_result) == 3 and splitted_result not in new_results:
                new_results.append(splitted_result)
    return new_results


def test_image_matching():
    image_maching = ImageMatching("F:/avi/test_image_maching/customer","F:/avi/test_image_maching/stores",ImageMatchingConfiguration(),
                                  ReadingModule(),WritingModule())
    image_maching.run_matching_for_all_stores()


if __name__ == '__main__':
    #main()
    test_image_matching()