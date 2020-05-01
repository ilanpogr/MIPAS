



def write_histogram_score_of_two_images(csv_output, origin_image_name,to_compare_image_name, scores_list):
    csv_output.append("Correlation," + origin_image_name + "," + to_compare_image_name + "," + str(scores_list[0]))
    csv_output.append("chi_Squared," + origin_image_name + "," + to_compare_image_name + "," + str(scores_list[1]))
    csv_output.append("intersection," + origin_image_name + "," + to_compare_image_name + "," + str(scores_list[2]))
    csv_output.append("bhattacharyya," + origin_image_name + "," + to_compare_image_name + "," + str(scores_list[3]))



def write_histogram_score_of_wto_images_passed_test(passed_histogram_test, origin_image_path, origin_image_name,
                                                    to_compare_image_path, to_compare_image_name, score):

    passed_histogram_test.append(origin_image_path + "," + origin_image_name + "," + to_compare_image_path +
                                 "," + to_compare_image_name + "," + str(score))