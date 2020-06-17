from configparser import ConfigParser
from os import path

_properties_file_path = "./resources/properties.ini"


def is_all_settings_configured(welcome_screen):
    if not welcome_screen.store_names.text() or not welcome_screen.store_main_category.text() or \
            not welcome_screen.store_sub_categories.text() or not welcome_screen.store_names.text() \
            or welcome_screen.path_str.text() == "Please choose your intial directory":
        return False
    else:
        return True


def is_settings_file_exists():
    _settings_file = _properties_file_path
    return path.exists(_settings_file)


def __modify_list_of_arguments(store_name):
    tmp = store_name.split(",")
    res = ""
    index = 0
    for s in tmp:
        s = s.strip()
        if index == len(tmp) - 1:
            res += s
        else:
            res += s + ","
        index += 1
    return res


def create_config_file(platform, store_name, main_category, sub_categories, dataset_path):
    config = ConfigParser()
    store_name = __modify_list_of_arguments(store_name)
    main_category = main_category.strip()
    sub_categories = __modify_list_of_arguments(sub_categories)
    config['settings'] = {
        'platform': platform,
        'store_name': store_name,
        'main_category': main_category,
        'sub_categories': sub_categories,
        'dataset_path': dataset_path,
        'working_dataset_path': dataset_path + "_resized",
        'multi_threading_downloaded_stores': 'resources/app_files/downloaded_stores_multi_threading.txt',
        'multi_threading_end_of_file': '~~~',
        'stores_dict': 'resources/app_files/stores_dict.csv',
        'images_delimiter': '$,,$',
        'table_size_x': '0',
        'table_size_y': '0',
    }
    with open(_properties_file_path, "w") as f:
        config.write(f)


def get_property(prop):
    config = ConfigParser()
    config.read(_properties_file_path)
    return config.get('settings', prop)


def set_property(prop, value):
    parser = ConfigParser()
    parser.read('properties.ini')
    parser.set('settings', prop, value)
    with open("properties.ini", "w") as configfile:
        parser.write(configfile)







