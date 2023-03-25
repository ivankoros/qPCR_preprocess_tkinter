import pandas as pd


def is_excel(filename):
    return filename.lower().endswith(('.xls', '.xlsx'))


def dimension_validation(file, expected_rows, expected_columns):
    dimension_validation_result: str = ""
    dimension_validation_color = ""

    rows, columns = file.shape

    if (rows, columns) != (expected_rows, expected_columns):
        dimension_validation_result = f"✗ File should be {expected_rows} x {expected_columns}, but is {rows} x {columns}"
        dimension_validation_color = "red"
        dimension_validation_result_bool = False
    else:
        dimension_validation_result = "✓ File looks good"
        dimension_validation_color = "green"
        dimension_validation_result_bool = True

    return dimension_validation_result, dimension_validation_color, dimension_validation_result_bool

# TODO: add dup validation function here
# Check if file is properly formatted to contain "dup" labels
def dup_validation(file):
    dup_validation_result: str = ""
    dup_validation_color = ""

    df = pd.read_excel(file)
    dup = df.duplicated().any()

    if dup:
        dup_validation_result = "✗ File contains duplicate rows"
        dup_validation_color = "red"
    else:
        dup_validation_result = "✓ File looks good"
        dup_validation_color = "green"

    return dup_validation_result, dup_validation_color


def upload_files_preprocessing(raw_sample_df, raw_sample_diagram_df):

    pass
