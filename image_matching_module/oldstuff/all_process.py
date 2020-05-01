import image_matching_module.reading_module
from image_matching_module.oldstuff import manipulation_module


# function to resize image, doing manipulation, copying all origin images to each folder
# and preform te feature and histogram.
def do_all_process(source,size):
    images_list = reading_files_module.get_images_names_in_folder(source)
    for image in images_list:
       manipulation_module.resize_image(image, size)
    manipulation_module.main_func_manipulation(source, images_list)


