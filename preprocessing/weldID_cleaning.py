import pandas as pd

from paths import CLEANED_CSV_PATH, DATA_PATH
from missing_values import print_missing_percentage
from data_cleaning import fill_with_mean_strategy, update_csv

WELD_ID_PATH = DATA_PATH + "weldID_analysis/"

def extract_group(weld_id: str) -> str:
    if weld_id.startswith("EvansLetter"):
        return "EvansLetter"
    
    if weld_id.startswith("p") and "-RR82011" in weld_id:
        return "p-RR82011"

    return weld_id.split('-')[0]

def divide_by_weld_type(file_path: str):
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
        group_df = df[df['Group'] == welding_type]
        print(f'nombre de instances pour le groupe {welding_type} : ', len(group_df))
        SPEC_WELD_ID_PATH = WELD_ID_PATH + welding_type + '_group.csv'
        # update_csv(fill_with_mean_strategy(SPEC_WELD_ID_PATH), SPEC_WELD_ID_PATH)
