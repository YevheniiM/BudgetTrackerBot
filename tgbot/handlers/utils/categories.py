import re


def split_categories(string):
    return re.findall(r'\b\w[\w\s]*\b', string)
