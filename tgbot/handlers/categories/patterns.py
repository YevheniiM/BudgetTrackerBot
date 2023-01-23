import json


def match_category_callback(callback_query):
    data = json.loads(callback_query)
    return data.get('button_name') == 'BUTTON_CATEGORY'
