import json


def match_category_callback(callback_query):
    try:
        json.loads(callback_query.data)
    except Exception:
        return False

    data = json.loads(callback_query)
    return data.get('button_name') == 'BUTTON_CATEGORY'
