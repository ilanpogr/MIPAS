import cv2
from PIL import Image
import os
from image_matching_module import reading_utils


def resize_all_images_in_path(path_to_origin):
    splitted_paths_to_origin = path_to_origin.split("/")
    new_path = os.path.dirname(path_to_origin) + "/" + str(splitted_paths_to_origin[-1]) + "_resized"
    old_customer_pics = []
    if not os.path.isdir(new_path):
        #create
        os.mkdir(new_path)
    else:
        old_customer_pics = reading_utils.ReadingUtils.get_images_names_in_folder(new_path)
    old_customer_pics_name = []
    for pic_path_and_name in old_customer_pics:
        old_customer_pics_name.append(pic_path_and_name[1])
    images_names = reading_utils.ReadingUtils.get_images_names_in_folder(path_to_origin)
    size = 750
    for image_name in images_names:
        if not old_customer_pics_name.__contains__(image_name[1]):
            image = resize_image(image_name,size)
            image.save(new_path+ "/" + image_name[1], 'JPEG')

def resize_image(image_name,size):
    image = Image.open(image_name[0] + "/" + image_name[1])
    basewidth = size
    wpercent = (basewidth / float(image.size[0]))
    hsize = int((float(image.size[1]) * float(wpercent)))
    image = image.resize((basewidth, hsize), Image.ANTIALIAS)
    return image


def flipped_image_horizontal(image):
    flipped_horizontal = cv2.flip(image, 1)
    return flipped_horizontal

