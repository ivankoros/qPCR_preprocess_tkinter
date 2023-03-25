import pandas as pd


def is_excel(filename):
    return filename.lower().endswith(('.xls', '.xlsx'))


