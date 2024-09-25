# Import functions from files
from data_import import data_import
from missing_values import print_missing_values, change_inferior_signs, print_unique_values, process_hardness_column, process_nitrogen_column, print_missing_percentage

# Import paths used to store data
from paths import CLEANED_CSV_PATH, MISSING_PERCENTAGE_CSV_PATH, ORIGINAL_DATA_PATH

if __name__ == "__main__":
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
    change_inferior_signs(CLEANED_CSV_PATH)

    # 5 - We go back to our percentage now that the data is a bit more cleaned
    print_missing_percentage(CLEANED_CSV_PATH, MISSING_PERCENTAGE_CSV_PATH)

    # 6 - We delete / place apart useless columns for now
    ######
    # Delete new columns
    ######

    # 7 - Change type of eache columns
    ######
    # change to float
    ######
     
    # 8 - Outliers
    ######
    # Remove outliers?
    ######

    # 9 - Create diff strategies pipelines

    # 10 - Create sub datasets ?