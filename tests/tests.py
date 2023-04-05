import unittest
from io import StringIO
import pandas as pd
from pandas.testing import assert_frame_equal
from resources import is_excel, dimension_validation, dup_validation, upload_files_preprocessing, stdev_warnings, \
    update_log_text


class TestFunctions(unittest.TestCase):

    def test_is_excel(self):
        """Tes if we can identify Excel files with the custom function in resources

        On upload, the file name should be read and passed to the is_excel function.
        If the file is an Excel file, the function should return True. If the file is not an Excel file,

        :return: Boolean value
        """
        self.assertTrue(is_excel('test.xlsx'))
        self.assertTrue(is_excel('test.XLS'))
        self.assertFalse(is_excel('test.csv'))
        self.assertFalse(is_excel('test.pdf'))

    def test_dimension_validation(self):
        """Validating the dimension of the uploaded file for each entry type

        The dimension_validation function takes in a dataframe, the expected number of rows, and the expected number of
        columns. It returns a string with the result of the validation, a string with the color of the result, and a
        boolean value with the result of the validation.

        :input: dataframe, int, int (expected number of rows, expected number of columns)
        :return: String, String, Boolean  (result, color, result_bool)
        """
        test_df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        result, color, result_bool = dimension_validation(test_df, 3, 2)
        self.assertEqual(result, "✓ File looks good")
        self.assertEqual(color, "green")
        self.assertTrue(result_bool)

        result, color, result_bool = dimension_validation(test_df, 4, 2)
        self.assertEqual(result, "✗ File should be 4 x 2, but is 3 x 2")
        self.assertEqual(color, "red")
        self.assertFalse(result_bool)

    def test_dup_validation(self):
        """Validating that each sample in the file has its duplicate ran sample and no more

        There should never be an exactly duplicated name of each sample, only itself (X205),
        it's second run (X205 dup) and possibly a clearly-marked error that will be automatically
        removed (X205 **, or X205 dup (needs to be removed)).

        If there are more than 2 samples with the same name, the function should return a string with the result of the
        validation, a string with the color of the result, and a boolean value with the result of the validation.
        - This is fed into the interface to display the result of the validation.

        :input: dataframe, int, int (expected number of rows, expected number of columns)
        :return: String, String, Boolean  (result, color, result_bool)
        """
        test_df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        result, color = dup_validation(StringIO(test_df.to_csv(index=False)))
        self.assertEqual(result, "✓ File looks good")
        self.assertEqual(color, "green")


        test_df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 2]})
        result, color = dup_validation(StringIO(test_df.to_csv(index=False)))
        self.assertEqual(result, "✗ File contains duplicate rows")
        self.assertEqual(color, "red")

    # TODO: add test cases for upload_files_preprocessing, stdev_warnings, and update_log_text


if __name__ == '__main__':
    unittest.main()
