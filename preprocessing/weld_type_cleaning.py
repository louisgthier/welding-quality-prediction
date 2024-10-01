# To handle path
import os
import sys
# Data Treatement Lib
import pandas as pd

# Import paths used to store data
from paths import CLEANED_CSV_PATH, DATA_PATH
from preprocessing.missing_values import print_missing_percentage
from preprocessing.data_fill import fill_with_mean_strategy, update_csv

# Ajouter le répertoire racine du projet au sys.path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

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

    for welding_type in WELD_TYPES:

        SPEC_WELD_TYPE_PATH = WELD_TYPE_PATH + welding_type + '_group.csv'
        update_csv(fill_with_mean_strategy(SPEC_WELD_TYPE_PATH), SPEC_WELD_TYPE_PATH)