"""
Functions to work with Missing Values
"""
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Import paths from variables.py
from paths import CLEANED_CSV_PATH, MISSING_PERCENTAGE_CSV_PATH

def _get_dataframe(file_path: str):
    """
    returns the dataframe of the file
    """
    return pd.read_csv(file_path)

## Section 1

@staticmethod
def print_missing_values(file_path: str):
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
def print_missing_percentage(file_path: str, destination_path: str):
    """
    Prints the % of missing values in columns
    """
    # Load the CSV file into a DataFrame
    df = pd.read_csv(file_path)

    # Calculate the percentage of NaN per column
    nan_percentage_column = (df.isna().mean() * 100).round(2)

    nan_percentage_column.to_csv(destination_path)

## Section 2

@staticmethod
def drop_unnecessary_columns(file_path: str) -> pd.DataFrame:
    """
    Supprime les colonnes non nécessaires d'un fichier CSV et retourne le DataFrame nettoyé.
    
    :param file_path: Le chemin du fichier CSV à nettoyer.
    :return: Le DataFrame nettoyé sans les colonnes spécifiées.
    """

    # Liste des colonnes à supprimer
    columns_to_drop = [
        'Primary ferrite in microstructure / %',
        'Ferrite with second phase / %',
        'Acicular ferrite / %',
        'Martensite / %',
        'Ferrite with carbide aggregate / %']

    df = pd.read_csv(file_path)

    try:
        # Suppression des colonnes
        df = df.drop(columns=columns_to_drop)
    except Exception as e:
        print(f"Erreur lors de la suppression des colonnes : {e}")
    
    df.to_csv(file_path, index=False)

## Section 3

@staticmethod
def remove_inferior_signs(file_path: str) -> pd.DataFrame:
    """
    Remplace les valeurs contenant des signes "<" dans un fichier CSV et retourne le DataFrame modifié.
    
    :param file_path: Le chemin du fichier CSV à nettoyer.
    :return: Le DataFrame avec les signes "<" supprimés des valeurs.
    """

    df = pd.read_csv(file_path)

    try:
        # Appliquer la transformation à tout le DataFrame
        df = df.applymap(lambda value: re.sub(r'<(\d+\.?\d*)', r'\1', value) if isinstance(value, str) else value)
    except Exception as e:
        print(f"Erreur lors de la suppression des signes '<' : {e}")

    df.to_csv(file_path, index=False)


@staticmethod
def print_correlation_matrix(file_path: str):
    """
    Prints the correlation matrix
    """

    # Load the CSV file into a DataFrame
    df = pd.read_csv(file_path)

    correlation_matrix = df.corr(method='pearson')

    print(correlation_matrix)

@staticmethod
def print_unique_values(file_path: str):
    """
    Prints the unique values of each column of a df
    """

    df = _get_dataframe(file_path)

    for column in df.columns:
        unique_values = df[column].unique()
        print(f"Column '{column}' has {len(unique_values)} unique values:")
        print(unique_values)
        print("-" * 40)

def process_nitrogen_column(file_path: str):
    """
    Traite une colonne du DataFrame pour extraire les valeurs avant "tot" 
    et place les résidus (entre "tot" et "res") dans une nouvelle colonne.
    Remplace "nd" par NaN dans la nouvelle colonne.

    Args:
        df (pd.DataFrame): Le DataFrame contenant la colonne à traiter.

    Returns:
        pd.DataFrame: Le DataFrame avec la colonne modifiée et une nouvelle colonne 'Nitrogen residual concentration'.
    """
    df = _get_dataframe(file_path)
    column_name = 'Nitrogen concentration / parts per million by weight'
    
    # Fonction pour séparer les valeurs avec "tot" et créer une nouvelle colonne
    def extract_values(val):
        if isinstance(val, str) and 'tot' in val:
            # Extraire la partie avant 'tot'
            before_tot = val.split('tot')[0]
            
            # Extraire la partie entre 'tot' et 'res'
            between_tot_res = val.split('tot')[1].split('res')[0]
            
            # Gérer le cas où 'nd' doit être converti en NaN
            if between_tot_res == 'nd':
                between_tot_res = np.nan
            
            return before_tot, between_tot_res
        else:
            # Si "tot" n'est pas présent, retourner la valeur originale et NaN pour la nouvelle colonne
            return val, np.nan

    # Appliquer la fonction sur la colonne et créer une nouvelle colonne 'Nitrogen residual concentration'
    df[[column_name, 'Nitrogen residual concentration']] = df[column_name].apply(lambda x: extract_values(x)).apply(pd.Series)

    # Convertir les colonnes en types numériques (ignorer les erreurs pour les valeurs non numériques)
    df[column_name] = pd.to_numeric(df[column_name], errors='coerce')
    df['Nitrogen residual concentration'] = pd.to_numeric(df['Nitrogen residual concentration'], errors='coerce')

    df.to_csv(file_path, index = False)


def process_hardness_column(file_path: str):
    """
    Traite une colonne du DataFrame pour extraire les valeurs avant les suffixes 'Hv5', 'Hv10', 'Hv30' 
    et place les suffixes dans une nouvelle colonne 'Hardness scale'.

    Args:
        df (pd.DataFrame): Le DataFrame contenant la colonne à traiter.
        column_name (str): Le nom de la colonne à traiter.

    Returns:
        pd.DataFrame: Le DataFrame avec la colonne modifiée et une nouvelle colonne 'Hardness scale'.
    """

    column_name = 'Hardness / kg mm^{-2}'
    df = pd.read_csv(file_path)
    
    # Fonction pour extraire la valeur de dureté et le suffixe (échelle de dureté)
    def extract_hardness(val):
        if isinstance(val, str):
            # Cherche les différents suffixes possibles (Hv5, Hv10, Hv30)
            if 'Hv5' in val:
                return val.replace('Hv5', ''), '5'
            elif 'Hv10' in val:
                return val.replace('Hv10', ''), '10'
            elif '(Hv30)' in val:
                return val.replace('(Hv30)', ''), '30'
            else:
                return val, np.nan
        else:
            return val, np.nan

    # Appliquer la fonction sur la colonne et créer une nouvelle colonne 'Hardness scale'
    df[[column_name, 'Hardness scale']] = df[column_name].apply(lambda x: extract_hardness(x)).apply(pd.Series)

    # Convertir les colonnes en types numériques pour les valeurs de dureté
    df[column_name] = pd.to_numeric(df[column_name], errors='coerce')

    df.to_csv(file_path, index = False)

def process_ac_dc_column(file_path: str):
    """
    Traite la colonne AC or DC en valeurs binaires exploitables (1 : DC et 0 : AC)
    """
    df = pd.read_csv(file_path)

    ac_dc_column = 'AC or DC'
    electrode_column = 'Electrode positive or negative'

    # Binarisation des valeurs
    df[ac_dc_column] = df[ac_dc_column].replace({'AC': 0, 'DC': 1})

    # Identification des valeurs manquantes
    missing_ac_dc = df[ac_dc_column].isna()

    # Remplacement de certaines valeurs manquantes (Si le signe de l'électrode est '+' ou '-', on impute la valeur 1 (DC))
    df.loc[missing_ac_dc & df[electrode_column].isin(['+', '-']), ac_dc_column] = 1

    df.to_csv(file_path, index=False)

def process_electrode_column(file_path: str):
    """
    Traite la colonne Electrode positive or negative, en la divisant en deux colonnes de valeurs binaires -Electrode positive- et -Electrode negative-
    """

    df = pd.read_csv(file_path)

    electrode_column = 'Electrode positive or negative'

    # Créer les deux nouvelles colonnes de valeurs binaires 'Electrode Positive' et 'Electrode Negative'
    df['Electrode Positive'] = df[electrode_column].apply(lambda x: 1 if x == '+' else 0)
    df['Electrode Negative'] = df[electrode_column].apply(lambda x: 1 if x == '-' else 0)

    df.drop(columns=[electrode_column], inplace=True)

    # Sauvegarder les modifications dans le fichier CSV
    df.to_csv(file_path, index=False)




# Run the analysis
if __name__ == "__main__":
    print_missing_values(CLEANED_CSV_PATH)
    drop_unnecessary_columns(CLEANED_CSV_PATH)
    remove_inferior_signs(CLEANED_CSV_PATH)
    print_unique_values(CLEANED_CSV_PATH)
    process_nitrogen_column(CLEANED_CSV_PATH)
    process_hardness_column(CLEANED_CSV_PATH)
    print_missing_percentage(CLEANED_CSV_PATH, MISSING_PERCENTAGE_CSV_PATH)
    process_ac_dc_column(CLEANED_CSV_PATH)
    process_electrode_column(CLEANED_CSV_PATH)