"""
Handles outliers values
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Import paths from variables.py
# from paths import CLEANED_CSV_PATH, MISSING_PERCENTAGE_CSV_PATH

def plot_outliers(file_path: str, column_name: str):
    """
    Affiche un diagramme en boîte (boxplot) pour visualiser les quartiles et les outliers d'une colonne du DataFrame.
    
    Args:
        df (pd.DataFrame): Le DataFrame contenant la colonne à analyser.
        column_name (str): Le nom de la colonne à analyser et visualiser.
    
    Returns:
        None: Affiche une boxplot avec les outliers.
    """
    df = pd.read_csv(file_path)

    # Supprimer les valeurs NaN
    col_data = df[column_name].dropna()

    # Définir la taille de la figure
    plt.figure(figsize=(8, 6))

    # Tracer la boxplot avec seaborn
    sns.boxplot(x=col_data)

    # Ajouter des labels et un titre
    plt.title(f"Visualisation des outliers pour '{column_name}'", fontsize=14)
    plt.xlabel(column_name, fontsize=12)

    # Afficher le plot
    plt.show()
