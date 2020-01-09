import json

settings_json = json.dumps([
    {
        'type': 'title',
        'title': 'Platform'
    },
    {
        'type': 'options',
        'title': 'Platform',
        'desc': 'e-commerce website for images theft search',
        'section': 'preferences',
        'key': 'platform',
        'options': ['Etsy', 'Shopify', 'Ebay'],
    },
    {
        'type': 'string',
        'title': 'Store Name',
        'desc': 'Store\'s name in chosen platform. if you have several stores, please use comma \' , \' as separator',
        'section': 'preferences',
        'key': 'stores_name',
    },
    {
        'type': 'title',
        'title': 'Paths'
    },
    {
        'type': 'path',
        'title': 'Dataset Path',
        'desc': 'Path to your pictures you would like to verify',
        'section': 'preferences',
        'key': 'dataset_path',
    },
    {
        'type': 'title',
        'title': 'Categories'
    },
    {
        'type': 'string',
        'title': 'Main Category',
        'desc': 'Store\'s main category',
        'section': 'preferences',
        'key': 'main_category',
    },
    {
        'type': 'string',
        'title': 'Sub Categories',
        'desc': 'Store\'s sub categories - please use comma \' , \' as separator',
        'section': 'preferences',
        'key': 'sub_categories',
    },
    {
        'type': 'title',
        'title': 'Shop Searching'
    },
    {
        'type': 'options',
        'title': 'Shop Searching Method',
        'desc': 'choose an option how to perform the next shop searching, after chosen method '
                '- found products will be compare to given dataset',
        'section': 'preferences',
        'key': 'crawler_option',
        'options': ['Start New Search', 'Update Found Stores', 'Don\'t Search'],
    },
])
