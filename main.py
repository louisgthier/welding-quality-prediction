"""
This file is the general script to obtain the final dataframes
Used for Machine Learning Algorithms.

welddb_data.csv is the original dataframe
welddb_cleaned.csv is the cleaned dataframe
"""

import os

# Import functions from files
from preprocessing.data_import import data_import
from preprocessing.missing_values import print_missing_values, remove_inferior_signs
from preprocessing.missing_values import print_unique_values, process_hardness_column
from preprocessing.missing_values import process_nitrogen_column, print_missing_percentage
from preprocessing.weld_type_cleaning import divide_by_weld_type, update_csv, fill_with_mean_strategy
from preprocessing.weld_type_cleaning import WELD_TYPE_PATH, WELD_TYPES


# Import paths used to store data
from paths import CLEANED_CSV_PATH, MISSING_PERCENTAGE_CSV_PATH, ORIGINAL_DATA_PATH


@staticmethod
def delete_if_exists(file_path: str):
    """
    Removes a file if it is found in the path
    """
    if os.path.exists(file_path):
        os.remove(file_path)

if __name__ == "__main__":
    
    # Delete files to restart the process
    delete_if_exists(CLEANED_CSV_PATH)
    delete_if_exists(MISSING_PERCENTAGE_CSV_PATH)
    delete_if_exists(ORIGINAL_DATA_PATH)
    for welding_type in WELD_TYPES:
        SPEC_WELD_TYPE_PATH = WELD_TYPE_PATH + welding_type + '_group.csv'
        delete_if_exists(SPEC_WELD_TYPE_PATH)

    # 1 - Import the data
    #   Remove trailing whitespace
    #   Remove double spaces messing with the import
    data_import(ORIGINAL_DATA_PATH)
    # This creates the welddb_data.csv
    data_import(CLEANED_CSV_PATH) # We create a duplicate on which we will perform preprocessing

    # 2 - Print Missing Values
    #   Plots two graphs (one quantitative, the other in %)
    print_missing_values(ORIGINAL_DATA_PATH)
    print_missing_percentage(ORIGINAL_DATA_PATH, MISSING_PERCENTAGE_CSV_PATH)
    
    # 3 - Print unique Values
    #   Helps finding the category of a column
    #   Also helps identifying wrong placed values
    print_unique_values(ORIGINAL_DATA_PATH)

    # 4 - Consequentially adapt data for some columns
    process_nitrogen_column(CLEANED_CSV_PATH)
    process_hardness_column(CLEANED_CSV_PATH)

    # 4 - Strategically remove inferior Signs
    #   Method Upper Bound
    #   It means our result represents the results for upper bound of concentration.
    remove_inferior_signs(CLEANED_CSV_PATH)

    # 5 - We go back to our percentage now that the data is a bit more cleaned
    print_missing_percentage(CLEANED_CSV_PATH, MISSING_PERCENTAGE_CSV_PATH)
    # Same for our unique values
    print_unique_values(CLEANED_CSV_PATH)

    # Divide by weld type
    divide_by_weld_type(CLEANED_CSV_PATH)
    # Finalize preprocess on each weld_type .csv
    for welding_type in WELD_TYPES:
        SPEC_WELD_TYPE_PATH = WELD_TYPE_PATH + welding_type + '_group.csv'
        update_csv(fill_with_mean_strategy(SPEC_WELD_TYPE_PATH), SPEC_WELD_TYPE_PATH)
    # We observe missing columns by type of weld, which is logic:
    # (Electric welding does not produce Nitrogen)


    # 6 - We delete / place apart useless columns for now
    ######
    # Delete new columns
    ######

    # 7 - Change type of each column
    ######
    # change to float
    ######
     
    # 8 - Outliers
    ######
    # Remove outliers?
    ######

    # 9 - Standardization
    ######
    #
    ######

    # 10 - Create diff strategies pipelines

    # 11 - Create sub datasets ?