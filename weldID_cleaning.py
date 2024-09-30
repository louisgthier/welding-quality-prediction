import pandas as pd

from paths import CLEANED_CSV_PATH, DATA_PATH
from missing_values import print_missing_percentage
from data_cleaning import fill_with_mean_strategy, update_csv

WELD_ID_PATH = DATA_PATH + "weldID_analysis/"

def extract_group(weld_id: str) -> str:
    """
    Extracts the group name from the Weld ID by taking into account:
    - Special handling for "EvansLetter"
    - Grouping "pXX" identifiers with a common pattern like "RR82011"
    - Default behavior: first part before the dash
    """
    if weld_id.startswith("EvansLetter"):
        return "EvansLetter"
    
    if weld_id.startswith("p") and "-RR82011" in weld_id:
        return "p-RR82011"

    return weld_id.split('-')[0]

def divide_by_weld_type(file_path: str):
    """
    This function will divide a pandas dataframe stored at file_path location.
    It will divide it by weld group based on refined grouping logic, and then we will
    try to observe the change in missing values.
    """
    df = pd.read_csv(file_path)

    df['Group'] = df['Weld ID'].apply(extract_group)

    groups = df.groupby('Group')

    for group_name, group_data in groups:
        destination_path = WELD_ID_PATH + group_name + '_group.csv'
        missing_percent_path = WELD_ID_PATH + group_name + "_missing_values.csv"

        group_data.to_csv(destination_path, index=False)

        print_missing_percentage(destination_path, missing_percent_path)

    return df

if __name__ == "__main__":
    df = divide_by_weld_type(CLEANED_CSV_PATH)

    for welding_type in df['Group'].unique():
        SPEC_WELD_ID_PATH = WELD_ID_PATH + welding_type + '_group.csv'
        # update_csv(fill_with_mean_strategy(SPEC_WELD_ID_PATH), SPEC_WELD_ID_PATH)
