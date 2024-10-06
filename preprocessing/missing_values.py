"""
Functions to work with Missing Values
"""
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Import paths from variables.py
from paths import CLEANED_CSV_PATH, MISSING_PERCENTAGE_CSV_PATH, CHARPY_CSV_PATH, QUALITY_CSV_PATH

def _get_dataframe(file_path: str):
    """
    returns the dataframe of the file
    """
    return pd.read_csv(file_path)

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

@staticmethod
def print_column_types(filepath: str):
    """
    Lit un fichier CSV et affiche les types de données de chaque colonne.
    :param filepath: Chemin du fichier CSV.
    """
    try:
        # Lire le fichier CSV dans un DataFrame
        df = pd.read_csv(filepath)
        
        # Afficher les types de données de chaque colonne
        print("Types de données des colonnes :")
        print(df.dtypes)

    except Exception as e:
        print(f"Une erreur s'est produite lors de la lecture du fichier : {e}")
    

@staticmethod
def drop_unnecessary_columns(file_path: str) -> pd.DataFrame:
    """
    Supprime les colonnes jugées non nécessaires.
    """

    # Liste des colonnes à supprimer
    columns_to_drop = [
        'Primary ferrite in microstructure / %',
        'Ferrite with second phase / %',
        'Acicular ferrite / %',
        'Martensite / %',
        'Ferrite with carbide aggregate / %', 
        '50% FATT', 
        'Hardness / kg mm^{-2}'
        ]

    df = pd.read_csv(file_path)

    df = df.drop(columns=columns_to_drop)

    df.to_csv(file_path, index=False)

# @staticmethod
# def remove_rows_with_missing_quality_values(file_path: str):
#     """
#     Supprime les lignes contenant au moins une valeur manquante dans les colonnes liées à la qualité de la soudure :
#     'Yield strength / MPa', 'Ultimate tensile strength / MPa', 'Elongation / %', 'Reduction of Area / %'.
#     """
#     df = pd.read_csv(file_path)

#     quality_columns = ['Yield strength / MPa', 
#                         'Ultimate tensile strength / MPa', 
#                         'Elongation / %', 
#                         'Reduction of Area / %']

#     df = df.dropna(subset=quality_columns)

#     df.to_csv(file_path, index=False)

#     print("Les lignes contenant des valeurs manquantes dans les colonnes d'intérêt ont été supprimées.")

#     df.to_csv(file_path, index=False)
    
@staticmethod
def replace_missing_concentration_with_zero(filepath: str):
    """
    Remplace les valeurs manquantes par 0 dans toutes les colonnes contenant le mot 'concentration'.
    """
    df = pd.read_csv(filepath)
    
    concentration_columns = [col for col in df.columns if 'concentration' in col] # sélectionne les colonnes qui ont 'concentration' dans leur nom

    df[concentration_columns] = df[concentration_columns].fillna(0) # remplace les valeurs manquantes par 0 dans ces colonnes

    df.to_csv(filepath, index=False)
    print(f"Les valeurs manquantes dans les colonnes 'concentration' ont été remplacées par 0.")


@staticmethod
def remove_inferior_signs(file_path: str) -> pd.DataFrame:
    """
    Remplace les valeurs contenant des signes "<" dans un fichier CSV et retourne le DataFrame modifié.
    
    :param file_path: Le chemin du fichier CSV à nettoyer.
    :return: Le DataFrame avec les signes "<" supprimés des valeurs.
    """
    df = pd.read_csv(file_path)
    df = df.applymap(lambda value: re.sub(r'<(\d+\.?\d*)', r'\1', value) if isinstance(value, str) else value)
    df.to_csv(file_path, index=False)


@staticmethod
def print_correlation_matrix(file_path: str):
    """
    Prints the correlation matrix
    """
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

    df.drop(columns=['Nitrogen residual concentration'], inplace=True)

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

    df[ac_dc_column] = df[ac_dc_column].replace({'AC': 0, 'DC': 1}) # on remplace tous les DC par 1 et les AC par 0

    missing_ac_dc = df[ac_dc_column].isna() # on récupère les valeurs manquantes

    df.loc[missing_ac_dc & df[electrode_column].isin(['+', '-']), ac_dc_column] = 1 # on remplace les valeurs manquantes par 1 si la polarité de l'électrode est spécifiée

    proportion_dc = df[ac_dc_column].value_counts(normalize=True).get(1, 0) 
    print('proportion de DC', proportion_dc)
    if proportion_dc > 0.9:
        df[ac_dc_column].fillna(1, inplace=True)

    df.to_csv(file_path, index=False)

def drop_rows(file_path: str):    
    df = pd.read_csv(file_path)
    columns_to_check = [
        'Yield strength / MPa', 
        'Ultimate tensile strength / MPa', 
        'Elongation / %', 
        'Reduction of Area / %', 
    ]

    df = df.dropna(subset=columns_to_check, how='any')
    df.to_csv(file_path, index=False)

from sklearn.preprocessing import OneHotEncoder
def one_hot_encode_weld_type(file_path: str):
    df = pd.read_csv(file_path)
    
    column_to_encode = 'Type of weld'
    
    if column_to_encode in df.columns:
        encoder = OneHotEncoder(sparse=False)

        encoded_columns = encoder.fit_transform(df[[column_to_encode]])

        encoded_column_names = encoder.get_feature_names_out([column_to_encode])
        
        encoded_df = pd.DataFrame(encoded_columns, columns=encoded_column_names)
        
        df = pd.concat([df, encoded_df], axis=1)
        
        df.drop(columns=[column_to_encode], inplace=True)
        
        df.to_csv(file_path, index=False)
    else:
        print(f"La colonne '{column_to_encode}' n'existe pas dans le fichier.")

def impute_with_median(file_path: str, column_name: str):
    """
    Impute missing values in the specified column with the median of that column
    """
    df = pd.read_csv(file_path)
    
    if column_name in df.columns:
        df[column_name].fillna(df[column_name].median(), inplace=True)
    
        df.to_csv(file_path, index=False)
        print(f"Missing values in column '{column_name}' have been imputed with the median.")
    else:
        print(f"Column '{column_name}' does not exist in the data.")

def process_interpass_temperature(file_path: str):
    """
    Traite la colonne 'Interpass temperature' pour remplacer les valeurs avec un tiret (par exemple, '150-200')
    par la moyenne des deux bornes.
    """
    df = pd.read_csv(file_path)
    
    column_name = 'Interpass temperature'
    
    # Fonction pour calculer la moyenne si la valeur contient un tiret
    def calculate_average(val):
        if isinstance(val, str) and '-' in val:
            # Séparer les valeurs avant et après le tiret
            parts = val.split('-')
            lower = float(parts[0].strip())  # Supprimer les espaces avant la conversion en float
            upper = float(parts[1].strip())
            # Retourner la moyenne des deux bornes
            return (lower + upper) / 2
        return val

    df[column_name] = df[column_name].apply(calculate_average)
    
    df.to_csv(file_path, index=False)
    print(f"Les valeurs avec un tiret dans la colonne '{column_name}' ont été remplacées par la moyenne des deux bornes.")

def process_electrode_column(file_path: str):
    """
    Traite la colonne Electrode positive or negative, en la divisant en deux colonnes de valeurs binaires -Electrode positive- et -Electrode negative-
    """

    df = pd.read_csv(file_path)

    electrode_column = 'Electrode positive or negative'

    df['Electrode Positive'] = df[electrode_column].apply(lambda x: 1 if x == '+' else 0)
    df['Electrode Negative'] = df[electrode_column].apply(lambda x: 1 if x == '-' else 0)

    df.drop(columns=[electrode_column], inplace=True)

    df.to_csv(file_path, index=False)

def one_hot_encode_weld_ids(file_path: str):
    """
    Cette fonction extrait les groupes à partir de la colonne 'Weld ID', effectue le one-hot encoding
    uniquement sur la colonne 'Group', et enregistre le fichier résultant dans le chemin donné.
    """
    
    df = pd.read_csv(file_path)

    def extract_group(weld_id: str) -> str:
        if weld_id.startswith("EvansLetter"):
            return "EvansLetter"
        
        if weld_id.startswith("p") and "-RR82011" in weld_id:
            return "p-RR82011"
        
        return weld_id.split('-')[0]

    df['Group'] = df['Weld ID'].apply(extract_group)

    one_hot_encoded_df = pd.get_dummies(df, columns=['Group'], prefix='Group')

    group_columns = [col for col in one_hot_encoded_df.columns if col.startswith('Group_')]
    one_hot_encoded_df[group_columns] = one_hot_encoded_df[group_columns].astype(int)

    print('One-hot encoding effectué avec succès.')
    one_hot_encoded_df.drop(columns=['Weld ID'], inplace=True)

    one_hot_encoded_df.to_csv(file_path, index=False)


def target_separations(file_path: str, output_path1: str, output_path2: str):
    """
    Crée deux CSV différents :
    - Le premier CSV est sans les colonnes 'Charpy temperature' et 'Charpy impact toughness / J',
      et supprime les lignes contenant des valeurs manquantes dans ces deux colonnes.
    - Le deuxième CSV est sans les colonnes 'Yield strength / MPa', 'Ultimate tensile strength / MPa',
      'Elongation / %' et 'Reduction of Area / %', et supprime les lignes avec des valeurs manquantes
      dans au moins une de ces colonnes.
    """
    df = pd.read_csv(file_path)

    # Premier csv : on enlève les colonnes liées au test Charpy, et on nettoie les 4 colonnes liées à la qualité de la soudure
    columns_to_remove_1 = ['Charpy temperature', 'Charpy impact toughness / J']
    quality_columns = ['Yield strength / MPa', 
                       'Ultimate tensile strength / MPa', 
                       'Elongation / %', 
                       'Reduction of Area / %']
    df1 = df.copy()
    df1 = df1.drop(columns=[col for col in columns_to_remove_1 if col in df.columns])
    df1 = df1.dropna(subset=quality_columns)
    df1.to_csv(output_path1, index=False)
    print(f"Premier CSV créé : {output_path1} (sans les colonnes {columns_to_remove_1} et sans valeurs manquantes dans les colonnes de qualité)")

    # Deuxième csv : on enlève les colonnes liées à la qualité de la soudure, et on nettoie les colonnes liées au test Charpy
    columns_to_remove_2 = quality_columns
    df2 = df.copy()
    df2 = df2.drop(columns=[col for col in columns_to_remove_2 if col in df.columns])
    charpy_columns = ['Charpy temperature', 'Charpy impact toughness / J']
    df2 = df2.dropna(subset=charpy_columns)
    df2.to_csv(output_path2, index=False)
    print(f"Deuxième CSV créé : {output_path2} (sans les colonnes {columns_to_remove_2} et sans valeurs manquantes dans les colonnes de test Charpy)")

def delete_columns(file_path: str):
    """
    Supprime les colonnes 'Group_Wolst' et 'Type of weld_ShMA' du fichier CSV, pour éviter les multicorrélations dues aux one-hot encoding.
    """
    df = pd.read_csv(file_path)
    columns_to_drop = ['Group_Wolst', 'Type of weld_ShMA']
    df = df.drop(columns=columns_to_drop)
    df.to_csv(file_path, index=False)
    print(f"Les colonnes {columns_to_drop} ont été supprimées du fichier.")

def display_column_value_types(file_path: str):
    """
    Affiche les types de valeurs pour chaque colonne dans un fichier CSV.
    """
    df = pd.read_csv(file_path)

    for column in df.columns:
        unique_values = df[column].apply(type).unique()
        print(f"Colonne '{column}' contient les types de données suivants : {unique_values}")

if __name__ == "__main__":
    df = pd.read_csv(CLEANED_CSV_PATH)
    print(df.columns)
    print_missing_values(CLEANED_CSV_PATH)
    print_missing_percentage(CLEANED_CSV_PATH, MISSING_PERCENTAGE_CSV_PATH)
    drop_unnecessary_columns(CLEANED_CSV_PATH)
    # drop_rows(CLEANED_CSV_PATH)
    replace_missing_concentration_with_zero(CLEANED_CSV_PATH)
    remove_inferior_signs(CLEANED_CSV_PATH)
    print_unique_values(CLEANED_CSV_PATH)
    process_nitrogen_column(CLEANED_CSV_PATH)
    # process_hardness_column(CLEANED_CSV_PATH)
    process_ac_dc_column(CLEANED_CSV_PATH)
    process_electrode_column(CLEANED_CSV_PATH)
    process_interpass_temperature(CLEANED_CSV_PATH)
    impute_with_median(CLEANED_CSV_PATH, 'Voltage / V')
    impute_with_median(CLEANED_CSV_PATH, 'Current / A')
    impute_with_median(CLEANED_CSV_PATH, 'Post weld heat treatment temperature')
    impute_with_median(CLEANED_CSV_PATH, 'Post weld heat treatment time / hours')
    impute_with_median(CLEANED_CSV_PATH, 'Interpass temperature')
    one_hot_encode_weld_type(CLEANED_CSV_PATH)
    one_hot_encode_weld_ids(CLEANED_CSV_PATH)
    delete_columns(CLEANED_CSV_PATH)
    target_separations(CLEANED_CSV_PATH, QUALITY_CSV_PATH, CHARPY_CSV_PATH)
    display_column_value_types(CLEANED_CSV_PATH)
    print_missing_values(CLEANED_CSV_PATH)

    # impute_charpy_impact_regression(CLEANED_CSV_PATH)
    # impute_reduction_of_area_regression(CLEANED_CSV_PATH)
    # impute_charpy_temperature_knn(CLEANED_CSV_PATH, n_neighbors=5, missing_threshold=0.2)



