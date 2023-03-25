import pandas as pd


def is_excel(filename):
    return filename.lower().endswith(('.xls', '.xlsx'))


def dimension_validation(filename, expected_rows, expected_columns):
    dimension_validation_result: str = ""
    dimension_validation_color = ""

    df = pd.read_excel(filename)
    rows, columns = df.shape

    if (rows, columns) != (expected_rows, expected_columns):
        dimension_validation_result = f"✗ File should be {expected_rows} x {expected_columns}, but is {rows} x {columns}"
        dimension_validation_color = "red"
    else:
        dimension_validation_result = "✓ File looks good"
        dimension_validation_color = "green"

    return dimension_validation_result, dimension_validation_color


        # df_data.shape, (96, 16),
        #                      f"Raw data is {df_data.shape[0]} rows by {df_data.shape[1]} columns but should be 96 rows by 3 columns")
        #
        # def test_plate_diagram(self):
        #     self.assertEqual(df_diagram.shape, (8, 13),
        #                      f"Plate diagram is {df_diagram.shape[0]} rows by {df_diagram.shape[1]} columns but should be 8 rows by 13 columns")
