import pandas as pd

def fill_with_mean_strategy(file_path):
    """
    Cette fonction prend en entrée le chemin d'un fichier CSV contenant des données de compositions chimiques et de propriétés mécaniques
    et renvoie un DataFrame nettoyé. Elle suit les étapes de preprocessing suivantes :
    
    - Suppression des colonnes entièrement vides
    - Suppression des lignes avec plus de 70% de valeurs manquantes
    - Suppression de la colonne d'index inutile ('Unnamed: 0')
    - Remplacement des valeurs manquantes dans les colonnes numériques par la moyenne de la colonne

    Args:
    file_path (str): Le chemin du fichier CSV contenant les données.

    Returns:
    pd.DataFrame: Le DataFrame nettoyé.
    """

    # Charger les données à partir du fichier CSV
    data = pd.read_csv(file_path)

    # 1. Suppression des colonnes vides (colonnes où toutes les valeurs sont manquantes)
    data_cleaned = data.dropna(axis=1, how='all')

    # 2. Suppression des lignes avec plus de 30% de valeurs manquantes
    # On garde seulement les lignes où au moins 70% des colonnes contiennent des données
    threshold = len(data_cleaned.columns) * 0.6
    data_cleaned = data_cleaned.dropna(thresh=threshold)

    # 3. Suppression de la colonne 'Unnamed: 0' qui est un ancien index inutile
    if 'Unnamed: 0' in data_cleaned.columns:
        data_cleaned = data_cleaned.drop(columns=['Unnamed: 0'])

    # 4. Remplacement des valeurs manquantes dans les colonnes numériques par la moyenne de chaque colonne
    # On identifie d'abord les colonnes numériques (types 'float64' ou 'int64')
    numeric_cols = data_cleaned.select_dtypes(include=['float64', 'int64']).columns

    # Ensuite, on remplace les valeurs manquantes dans ces colonnes par la moyenne
    data_cleaned[numeric_cols] = data_cleaned[numeric_cols].fillna(data_cleaned[numeric_cols].mean())

    # Retourner le DataFrame nettoyé
    return data_cleaned

def update_csv(df: pd.DataFrame, file_path: str):
    """
    Updates the DF to a csv
    """
    df.to_csv(file_path)