import os
import cv2
import numpy as np
from PIL import Image

import image_matching_module.reading_files_module
import image_matching_module.writing_utils


#vintage filter
def vintage_filter(tuple_image_path_and_name, index):
    im = reading_files_module.reading_image_from_tuple_path_open_cv(tuple_image_path_and_name)
    rows, cols = im.shape[:2]
    # Create a Gaussian filter
    kernel_x = cv2.getGaussianKernel(cols, cols - 100)
    kernel_y = cv2.getGaussianKernel(rows, rows - 100)
    kernel = kernel_y * kernel_x.T
    filter = 255 * kernel / np.linalg.norm(kernel)
    vintage_im = np.copy(im)
    # for each channel in the input image, we will apply the above filter
    for i in range(index):
        vintage_im[:, :, i] = vintage_im[:, :, i] * filter
    writing_module.writing_vintage_to_path(tuple_image_path_and_name, index, vintage_im, "vintage")

#median filter
def median_filter (tuple_image_path_and_name):
    img = reading_files_module.reading_image_from_tuple_path_open_cv(tuple_image_path_and_name)
    median = cv2.medianBlur(img,7)
    writing_module.writing_img_to_path(tuple_image_path_and_name, median, "median")

#roteting image.
def rotate(tuple_image_path_and_name,delta_given):
    rotate = 0
    delta = delta_given
    image = reading_files_module.reading_image_from_tuple_path_using_image(tuple_image_path_and_name)
    for i in range(0,int(360 / delta)):
        rotated_image = image.rotate(rotate, fillcolor='white', expand=True)
        name = rotate
        rotate += delta
        writing_module.writing_rotate_to_path(tuple_image_path_and_name, name, "rotated", rotated_image)


def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.2989, 0.5870, 0.1140])


#grey scale
def greyscale(tuple_image_path_and_name):
    image = reading_files_module.reading_image_from_tuple_path_open_cv(tuple_image_path_and_name)
    gray = rgb2gray(image)
    writing_module.writing_img_to_path(tuple_image_path_and_name, gray, "greyscale")


#crop  need to fix the sizes of the crop, first arg is y axis and then x axis
def crop(tuple_image_path_and_name):
    image = reading_files_module.reading_image_from_tuple_path_open_cv(tuple_image_path_and_name)
    (h1, w1) = image.shape[:2]
    top_left_height = int(h1 / 8)
    button_right_height = int (3 * h1 / 4) + top_left_height
    top_left_weight =  int(w1 / 8)
    button_right_weight = int (3 * w1 / 4) + top_left_weight
    crop_img = image[top_left_height : button_right_height,top_left_weight : button_right_weight]
    writing_module.writing_img_to_path(tuple_image_path_and_name, crop_img, "cropped")



#creating filters for the imgaes.
def create_filter_for_images(source,image_list):
    for image_name in image_list:
        create_filter_for_image(source,image_name)


def flipped_image_horizontal(image):
    return cv2.flip(image,1)

def flipped_image_vertical(image):
    return cv2.flip(image,0)

def flipped_image_horizontal_and_vertical(image):
    return cv2.flip(image,-1)


#creating filipped (mirrored) image.
def flipped_image(tuple_image_path_and_name):
    image = reading_files_module.reading_image_from_tuple_path_open_cv(tuple_image_path_and_name)
    flipVertical = flipped_image_vertical(image)
    writing_module.writing_img_to_path_mirrored(tuple_image_path_and_name, flipVertical, "mirroredVertical")
    flipHorizontal = flipped_image_horizontal(image)
    writing_module.writing_img_to_path_mirrored(tuple_image_path_and_name, flipHorizontal, "mirroredHorizontal")
    flipVerAndHori = flipped_image_horizontal_and_vertical(image)
    writing_module.writing_img_to_path_mirrored(tuple_image_path_and_name, flipVerAndHori, "mirroredVerAndHori")


#creating filters for an image.
def create_filter_for_image(source,image_name):
    crop(image_name)
    for i in range(1, 4):
        vintage_filter(image_name, i)
    median_filter(image_name)
    rotate(image_name, 10)
    greyscale(image_name)
    flipped_image(image_name)
    print("finish with picture number: " + image_name[1])


# main function to start manipulations.
def change_images_name(source,images_list):
    index = 1
    for image in images_list:
        splitted_name = image[1].split(".")
        new_name = str(index) + "." + splitted_name[len(splitted_name) - 1]
        os.rename(source + "/" + image[1],source + "/" + new_name)
        index += 1


def main_func_manipulation(source,images_list):
    #change_images_name(source,images_list)
    images_list = reading_files_module.get_images_names_in_folder(source)
    writing_module.create_folders_for_images(images_list)
    writing_module.create_sub_folders_in_pic_folder(images_list)
    print("folders created.")
    print("----------------------------")
    create_filter_for_images(source,images_list)


def resize_image(image_name,size):
    image = Image.open(image_name[0] + "\\" + image_name[1])
    basewidth = size
    wpercent = (basewidth / float(image.size[0]))
    hsize = int((float(image.size[1]) * float(wpercent)))
    image = image.resize((basewidth, hsize), Image.ANTIALIAS)
    image.save(image_name[0] + "\\" + image_name[1], 'JPEG')