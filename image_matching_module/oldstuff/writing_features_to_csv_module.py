


def write_features_horizontal_result_of_two_images(csv_output, origin_image_name, des3, to_compare_image_name, des2,
                                            matches_origin_horizontal_to_compare, score_origin_horizontal_to_compare):

    csv_output.append(origin_image_name + "Horizontal" + "," + str(len(des3)) + "," + to_compare_image_name + "," +
                      str(len(des2)) + "," + str(len(matches_origin_horizontal_to_compare)) + "," +
                      str(score_origin_horizontal_to_compare))


def write_features_result_of_two_images(csv_output, origin_image_name, des1, to_compare_image_name, des2,
                                        matches_origin_to_compare, score_origin_to_compare):

    csv_output.append(origin_image_name + "," + str(len(des1)) + "," + to_compare_image_name + "," + str(len(des2)) +
                      "," + str(len(matches_origin_to_compare)) + "," + str(score_origin_to_compare))




def write_features_score_of_wto_images_passed_test(passed_features_test, origin_image_path, origin_image_name,
                                                   to_compare_image_path, to_compare_image_name, score):

    passed_features_test.append(origin_image_path + "," + origin_image_name + "," + to_compare_image_path +
                                "," + to_compare_image_name + "," + str(score))
