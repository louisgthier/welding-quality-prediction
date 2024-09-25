"""
Functions to work with Missing Values
"""
import re
import pandas as pd
import matplotlib.pyplot as plt

# Import paths from variables.py
from paths import CLEANED_CSV_PATH, MISSING_PERCENTAGE_CSV_PATH

@staticmethod
def analyze_nan_in_csv(file_path: str):
    """
    Analyzes the NaN values in a csv file passed in hyperparameter
    Produces graphs to show off the NaN values
    """

    # Load the CSV file into a DataFrame
    df = pd.read_csv(file_path)

    # Calculate the number of NaN per column
    nan_per_column = df.isna().sum()

    # Calculate the percentage of NaN per column
    nan_percentage_column = (df.isna().mean() * 100).round(2)

    # Plot the total number of NaNs per column
    plt.figure(figsize=(10, 6))
    nan_per_column.plot(kind='bar', color='skyblue')
    plt.title('Total NaN Values per Column')
    plt.xlabel('Columns')
    plt.ylabel('Number of NaN values')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

    # Plot the total number of NaNs in % per column
    plt.figure(figsize=(10, 6))
    nan_percentage_column.plot(kind='bar', color='skyblue')
    plt.title('Total NaN Values (%) per Column')
    plt.xlabel('Columns')
    plt.ylabel('Percentage of NaN values')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

@staticmethod
def print_missing_percentage(file_path: str):
    """
    Prints the % of missing values in columns
    """
    # Load the CSV file into a DataFrame
    df = pd.read_csv(file_path)

    # Calculate the percentage of NaN per column
    nan_percentage_column = (df.isna().mean() * 100).round(2)

    nan_percentage_column.to_csv(MISSING_PERCENTAGE_CSV_PATH)


def data_cleaning(file_path: str) -> pd.DataFrame:
    """
    Cleans the data in a DataFrame:
    1. Replaces values with less than signs ("<") by the values without the sign.
    2. Removes specified columns.
    
    :param file_path: The CSV file path to clean.
    :param columns_to_drop: List of columns to drop from the DataFrame.
    :return: The cleaned DataFrame.
    """

    # List of columns with many missing values that we want to analyze
    columns_to_drop = [
        'Primary ferrite in microstructure / %',
        'Ferrite with second phase / %',
        'Acicular ferrite / %',
        'Martensite / %',
        'Ferrite with carbide aggregate / %']

    df = pd.read_csv(file_path)

    # 1. Drop unnecessary columns (explained in the readme)
    df = df.drop(columns=columns_to_drop)

    # 2. Replace the less than signs with the values without the sign
    def replace_inferior_signs(value):
        if isinstance(value, str):
            return re.sub(r'<(\d+\.?\d*)', r'\1', value)
        return value

    df = df.apply(lambda col: col.apply(replace_inferior_signs))
    
    return df


@staticmethod
def print_correlation_matrix(file_path: str):
    """
    Prints the correlation matrix
    """

    # Load the CSV file into a DataFrame
    df = pd.read_csv(file_path)

    correlation_matrix = df.corr(method='pearson')

    print(correlation_matrix)


# Run the analysis
if __name__ == "__main__":
    analyze_nan_in_csv(CLEANED_CSV_PATH)
    print_missing_percentage(CLEANED_CSV_PATH)
    data_without_inferior_signs = data_cleaning(CLEANED_CSV_PATH)
