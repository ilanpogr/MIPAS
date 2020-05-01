from image_matching_module.reading_module import ReadingModule
import pandas as pd
import os
import time


class PrecisionRecallExperiment:
    """class that represents an image_matching_module measuring the precision and recall"""

    def __init__(self):
        self.reader = ReadingModule()

    def run_multiple_simple_experiments(self, path_to_csv_files, algorithms, thresholds):
        """runs multiple experiments that calculates the precision and recall of the comparison algorithms' results"""
        starting_time = time.time()
        print("started simple precision recall image_matching_module")
        for algorithm in algorithms:
            start_file_time = time.time()
            print("started algorithm:", algorithm.get_algorithm_name())
            self.run_single_simple_experiment(path_to_csv_files, algorithm, thresholds)
            finish_file_time = time.time()
            print("finished algorithm:", algorithm.get_algorithm_name())
            print("time took:", (finish_file_time - start_file_time) / 60 , "minutes")
        finish_time = time.time()
        hours = int((finish_time - starting_time) // 3600)
        minutes = (finish_time - starting_time) / 60
        print("finished simple precision recall image_matching_module")
        print ("time image_matching_module took:" ,hours , "hours and", minutes , "minutes")

    def run_single_simple_experiment(self, path_to_csv_files, algorithm, thresholds):
        """runs an image_matching_module that calculates the precision and recall of the comparison algorithm's results"""

        splitted_path = os.path.abspath(__file__).split("/")
        if not os.path.isdir("/".join(splitted_path[:-1]) + "/results"):
            os.mkdir("/".join(splitted_path[:-1]) +"/results")

        experiment_dict, list_dict = self.create_experiment_dict(algorithm.get_algorithm_name() + "_actual", thresholds)

        csv_paths_list = self.reader.read_all_csv_paths_from_path(path_to_csv_files)
        file_number = 1
        for csv_path in csv_paths_list:
            if 'total' in csv_path:
                continue
            df = pd.read_csv(csv_path)
            start_file_time = time.time()
            print("started file number:", file_number)
            for index,row in df.iterrows():
                algorithm_column_name = algorithm.get_algorithm_name() + "_actual"
                actual_score = row['actual_score']
                for threshold in thresholds:
                    algorithm_score = row[algorithm_column_name]
                    if actual_score == 1:
                        if algorithm_score >= threshold:
                            experiment_dict[str(threshold)][algorithm_column_name][list_dict['TP']] += 1
                        else:
                            experiment_dict[str(threshold)][algorithm_column_name][list_dict['FN']] += 1
                    else:
                        if algorithm_score < threshold:
                            experiment_dict[str(threshold)][algorithm_column_name][list_dict['TN']] += 1
                        else:
                            experiment_dict[str(threshold)][algorithm_column_name][list_dict['FP']] += 1
            finish_file_time = time.time()
            print("finished file number:", file_number)
            print("file number:", file_number , "took:", (finish_file_time - start_file_time) / 60 , "minutes")
            file_number += 1

        # calculate the precision and recall for each threshold and algorithm
        experiment_dict = self.update_precision_and_recall(experiment_dict, list_dict, algorithm.get_algorithm_name() + "_actual", thresholds)

        # create a dictionary that can be ingested into a dataframe
        experiment_dict_for_csv = self.create_simple_experiment_dict_for_csv(experiment_dict, list_dict, algorithm, thresholds)

        # create a dataframe from the results
        experiment_dict_df = pd.DataFrame(experiment_dict_for_csv)

        # write the results into a csv file
        experiment_csv_file_name = os.path.dirname("/".join(splitted_path)) + "/results/precision_recall_results_" + algorithm.get_algorithm_name() + ".csv"
        experiment_dict_df.to_csv(experiment_csv_file_name, index=False, header=True)

    def run_multiple_advanced_experiments(self, path_to_csv_files, algorithms_weights_list, thresholds):
        """runs multiple experiments that calculates the precision and recall of multiple comparison algorithms' results"""
        starting_time = time.time()
        print("started advanced precision recall image_matching_module")
        for algorithms_weights in algorithms_weights_list:
            start_file_time = time.time()

            first_run = True
            for algorithm, weight in algorithms_weights:
                if first_run:
                    algorithm_name = algorithm.get_algorithm_name() + weight
                    first_run = False
                else:
                    algorithm_name = algorithm_name + "_" + algorithm.get_algorithm_name() + weight

            print("started algorithm:", algorithm_name)
            self.run_single_advanced_experiment(path_to_csv_files, algorithms_weights, thresholds)
            finish_file_time = time.time()
            print("finished algorithm:", algorithm_name)
            print("time took:", (finish_file_time - start_file_time) / 60 , "minutes")
        finish_time = time.time()
        hours = int((finish_time - starting_time) // 3600)
        minutes = (finish_time - starting_time) / 60
        print("finished advanced precision recall image_matching_module")
        print ("time image_matching_module took:" ,hours , "hours and", minutes , "minutes")

    def run_single_advanced_experiment(self, path_to_csv_files, algorithms_weights, thresholds):
        """runs an image_matching_module that calculates the precision and recall of multiple comparison algorithms' results"""

        splitted_path = os.path.abspath(__file__).split("/")
        if not os.path.isdir("/".join(splitted_path[:-1]) + "/results"):
            os.mkdir("/".join(splitted_path[:-1]) +"/results")

        first_run = True
        for algorithm, weight in algorithms_weights:
            if first_run:
                algorithm_name = algorithm.get_algorithm_name() + weight
                first_run = False
            else:
                algorithm_name = algorithm_name + "_" + algorithm.get_algorithm_name() + weight

        experiment_dict, list_dict = self.create_experiment_dict(algorithm_name, thresholds)

        csv_paths_list = self.reader.read_all_csv_paths_from_path(path_to_csv_files)
        file_number = 1
        for csv_path in csv_paths_list:
            if 'total' in csv_path:
                continue
            df = pd.read_csv(csv_path)
            start_file_time = time.time()
            print("started file number:", file_number)
            for index,row in df.iterrows():
                for algorithm_threshold in thresholds:

                    algorithm_scores = []
                    for algorithm, weight in algorithms_weights:
                        algorithm_column_name = algorithm.get_algorithm_name() + "_actual"
                        initial_algorithm_score = row[algorithm_column_name]
                        algorithm_scores.append(initial_algorithm_score * weight)

                    combined_score = 0.0
                    for algorithm_score in algorithm_scores:
                        combined_score += algorithm_score

                    actual_score = row['actual_score']
                    if actual_score == 1:
                        if combined_score >= algorithm_threshold:
                            experiment_dict[str(algorithm_threshold)][algorithm_name][list_dict['TP']] += 1
                        else:
                            experiment_dict[str(algorithm_threshold)][algorithm_name][list_dict['FN']] += 1
                    else:
                        if combined_score < algorithm_threshold:
                            experiment_dict[str(algorithm_threshold)][algorithm_name][list_dict['TN']] += 1
                        else:
                            experiment_dict[str(algorithm_threshold)][algorithm_name][list_dict['FP']] += 1

            finish_file_time = time.time()
            print("finished file number:", file_number)
            print("file number:", file_number , "took:", (finish_file_time - start_file_time) / 60 , "minutes")
            file_number += 1

        # calculate the precision and recall for each threshold and algorithm
        experiment_dict = self.update_precision_and_recall(experiment_dict, list_dict, algorithm_name, thresholds)

        # create a dictionary that can be ingested into a dataframe
        experiment_dict_for_csv = self.create_advanced_experiment_dict_for_csv(experiment_dict, list_dict, algorithm_name, thresholds)

        # create a dataframe from the results
        experiment_dict_df = pd.DataFrame(experiment_dict_for_csv)

        # write the results into a csv file
        experiment_csv_file_name = os.path.dirname("/".join(splitted_path)) + "/results/precision_recall_results_" + algorithm_name + ".csv"
        experiment_dict_df.to_csv(experiment_csv_file_name, index=False, header=True)

    @staticmethod
    def create_experiment_dict(algorithm_name, thresholds):
        """create the dictionary holding the image_matching_module's results"""
        experiment_dict = {}
        for threshold in thresholds:
            experiment_dict[str(threshold)] = {}
            experiment_dict[str(threshold)][algorithm_name] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        list_dict = {'TP': 0, 'FP': 1, 'TN': 2, 'FN': 3, 'TPR': 4, 'TNR': 5, 'PRECISION': 6, 'RECALL': 7, 'F1 MEASURE': 8, 'ACCURACY': 9}
        return experiment_dict, list_dict

    @staticmethod
    def update_precision_and_recall(experiment_dict, list_dict, algorithm_name, thresholds):
        """updates the precision and recall data in the image_matching_module's results"""
        for threshold in thresholds:
            algorithm_column_name = algorithm_name + "_actual"
            tp = experiment_dict[str(threshold)][algorithm_name][list_dict['TP']]
            fp = experiment_dict[str(threshold)][algorithm_name][list_dict['FP']]
            fn = experiment_dict[str(threshold)][algorithm_name][list_dict['FN']]
            tn = experiment_dict[str(threshold)][algorithm_name][list_dict['TN']]

            accuracy = (tp + tn) / (tp + tn + fp + fn)
            tpr = tp / (tp + fn)
            tnr = tn / (tn + fp)
            precision = tp / (tp + fp)
            recall = tpr
            f1_measure = 2 * ((precision * recall) / (precision + recall))

            experiment_dict[str(threshold)][algorithm_name][list_dict['TPR']] = tpr
            experiment_dict[str(threshold)][algorithm_name][list_dict['TNR']] = tnr
            experiment_dict[str(threshold)][algorithm_name][list_dict['PRECISION']] = precision
            experiment_dict[str(threshold)][algorithm_name][list_dict['RECALL']] = recall
            experiment_dict[str(threshold)][algorithm_name][list_dict['F1 MEASURE']] = f1_measure
            experiment_dict[str(threshold)][algorithm_name][list_dict['ACCURACY']] = accuracy
        return experiment_dict

    @staticmethod
    def create_simple_experiment_dict_for_csv(experiment_dict, list_dict, algorithm, thresholds):
        """ creates a dictionary that can be ingested by pandas dataframe to write to a csv file """
        experiment_dict_for_csv = {"attributes": ['TP', 'FP', 'TN', 'FN', 'TPR (Sensitivity)', 'TNR (Specificity)', 'Precision', 'Recall', 'F1 Measure', 'Accuracy']}
        for row_key in list_dict.values():
            for threshold in thresholds:
                algorithm_column_name = algorithm.get_algorithm_name() + "_actual"
                column_name = algorithm.get_algorithm_name() + "_" + str(threshold)
                row_value = experiment_dict[str(threshold)][algorithm_column_name][row_key]
                if column_name in experiment_dict_for_csv.keys():
                    experiment_dict_for_csv[column_name].append(row_value)
                else:
                    experiment_dict_for_csv[column_name] = [row_value]
        return experiment_dict_for_csv

    @staticmethod
    def create_advanced_experiment_dict_for_csv(experiment_dict, list_dict, algorithm_name, thresholds):
        """ creates a dictionary that can be ingested by pandas dataframe to write to a csv file """
        experiment_dict_for_csv = {
            "attributes": ['TP', 'FP', 'TN', 'FN', 'TPR (Sensitivity)', 'TNR (Specificity)', 'Precision', 'Recall',
                           'F1 Measure', 'Accuracy']}
        for row_key in list_dict.values():
            for threshold in thresholds:
                column_name = algorithm_name + "-" + str(threshold)
                row_value = experiment_dict[str(threshold)][algorithm_name][row_key]
                if column_name in experiment_dict_for_csv.keys():
                    experiment_dict_for_csv[column_name].append(row_value)
                else:
                    experiment_dict_for_csv[column_name] = [row_value]
        return experiment_dict_for_csv
