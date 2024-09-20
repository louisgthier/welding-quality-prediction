# Import pandas
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Import paths from variables.py
from paths import CLEANED_CSV_PATH

@staticmethod
def analyze_nan_in_csv(file_path: str):
    """
    Analyzes the NaN values in a csv file passed in hyperparameter
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
    plt.title('Total NaN Values per Column')
    plt.xlabel('Columns')
    plt.ylabel('Number of NaN values')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

# Run the analysis
if __name__ == "__main__":
    analyze_nan_in_csv(CLEANED_CSV_PATH)
