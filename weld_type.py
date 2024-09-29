# Data Treatement Lib
import pandas as pd

# Import paths used to store data
from paths import CLEANED_CSV_PATH, DATA_PATH, FCA_CSV_PATH
from missing_values import print_missing_percentage
from data_cleaning import clean_fca, update_csv

WELD_TYPE_PATH = DATA_PATH + "weld_type_analysis/"
WELD_TYPES: list[str] = ['MMA',
              'ShMA',
              'FCA',
              'SA',
              'TSA',
              'SAA',
              'GTAA',
              'GMAA',
              'NGSAW',
              'NGGMA']

def divide_by_weld_type(file_path: str):
    """
    This function will divide a pandas dataframe stored at file_path location
    It will divide it by weld type, then we will try to observe the change in missing values
    """

    df = pd.read_csv(file_path)

    groups = df.groupby('Type of weld')

    for weld_type in WELD_TYPES:

        group = groups.get_group(weld_type)

        destination_path = WELD_TYPE_PATH + weld_type + '_group.csv'
        missing_percent_path = WELD_TYPE_PATH + weld_type + "_missing_values.csv"

        group.to_csv(destination_path)

        print_missing_percentage(destination_path, missing_percent_path)

    return groups

if __name__ == "__main__":
    divide_by_weld_type(CLEANED_CSV_PATH)
    update_csv(clean_fca(FCA_CSV_PATH), FCA_CSV_PATH)