import pandas as pd
import numpy as np

def is_excel(filename):
    return filename.lower().endswith(('.xls', '.xlsx'))


def dimension_validation(file, expected_rows, expected_columns):

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
    # Assign the dataframes to shorter variables
    df_data = raw_sample_df
    df_diagram = raw_sample_diagram_df

    # Set the first column as the index, remove whitespace and add a space to the "dup" values
    df_diagram = df_diagram.set_index(df_diagram.columns[0])
    df_diagram = df_diagram.replace('\s+', '', regex=True)
    df_diagram = df_diagram.replace('dup', ' dup', regex=True)

    sample_map = {}

    for row in df_diagram.index:
        for col in df_diagram.columns[1:]:
            well_id = f"{row}{int(col):02d}"
            sample_name = df_diagram.loc[row, col]
            sample_map[well_id] = sample_name

    """Use rows and columns (besides the first one) to relate the well ID to the sample name.

    For example, the first row name is A and the first column name is 1.
    The well ID will be A01 and the sample name will the sample in that row/column.

    """

    # Read in the raw qPCR data and map the well IDs to sample names using the dictionary
    df_data["Sample"] = df_data["Well"].map(sample_map)

    # Select relevant columns (Well, Cq, and Sample)
    df = df_data[['Well', 'Cq', 'Sample']].copy()

    # Create mtDNA1 and mtDNA2 columns
    df['mtDNA1'] = "mtDNA1"
    df['mtDNA2'] = "mtDNA2"

    # Arrange columns like this: "Well", "Sample", "mtDNA1", "mtDNA2", "Cq"
    df = df.loc[:, ["Well", "Sample", "mtDNA1", "mtDNA2", "Cq"]]

    # Drop rows with NA values
    df = df.dropna()

    # set mtDNA1 and mtDNA2 values to Cq values by treating mtDNA1 as the Cq for the first sample and mtDNA2 as the Cq for the duplicate sample if it exists as "Sample dup"

    # Note, exactly "Sample dup" is used to avoid matching "Sample dup **" or any additions to the name

    for row, index in df.iterrows():
        df.loc[row, 'mtDNA1'] = df.loc[row, 'Cq']
        if df.loc[row, 'Sample'] + ' dup' in df['Sample'].values:
            df.loc[row, 'mtDNA2'] = df.loc[df['Sample'] == df.loc[row, 'Sample'] + ' dup', 'Cq'].values[0]
        else:
            df.loc[row, 'mtDNA2'] = np.NAN

    """ Assign mtDNA1 and mtNDA2 value

        For each row, set the mtDNA1 value to the Cq value and set the mtDNA2 value to the Cq value of the duplicate sample if it exists.

        For example, if the sample name is "D12", set the mtDNA1 value to its Cq value and set the mtDNA2 value to the Cq value of "D12 Dup" (if it exists).

        If the duplicate ("D12 Dup") does not exist, set the mtDNA2 value to NaN, which is then dropped later.
    """

    # Drop the Cq column and drop NA values
    df = df.drop(columns=['Cq'])
    df = df.dropna()

    # calculate standard deviation of each row
    df['St.Dev'] = df[['mtDNA1', 'mtDNA2']].std(axis=1)

    # Drop index, sort by standard deviation (descending), and download the file
    df = df.sort_values(by=['St.Dev'], ascending=False)
    df = df.reset_index(drop=True)

    warnings_list = stdev_warnings(df)

    return df, warnings_list


def stdev_warnings(combined_df):

    df = combined_df
    warnings_list = []

    # Throw warnings for standard deviations greater than .22

    for row, index in df.iterrows():
        if df.loc[row, 'St.Dev'] > .22:
            warnings_list.append(
                f"Warning: Standard deviation for {df.loc[row, 'Sample']} is {round(df.loc[row, 'St.Dev'], ndigits=3)} "
                f"(Sample 1: {round(df.loc[row, 'mtDNA1'], ndigits=3)} vs Sample 2: {round(df.loc[row, 'mtDNA2'], ndigits=2)})")

    return warnings_list
