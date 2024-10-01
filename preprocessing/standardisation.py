import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler

def standardize_column(file_path: str, column_name: str, strategy: str) -> pd.DataFrame:
    # Lire le fichier CSV dans un DataFrame
    df = pd.read_csv(file_path)
    
    # Vérifier que la colonne existe
    if column_name not in df.columns:
        raise ValueError(f"La colonne '{column_name}' n'existe pas dans le fichier.")
    
    # Standardiser la colonne selon la stratégie donnée
    if strategy == 'z-score':
        scaler = StandardScaler()
        df[[column_name]] = scaler.fit_transform(df[[column_name]])
    elif strategy == 'min-max':
        scaler = MinMaxScaler()
        df[[column_name]] = scaler.fit_transform(df[[column_name]])
    elif strategy == 'mean':
        mean_value = df[column_name].mean()
        df[column_name] = df[column_name] - mean_value
    elif strategy == 'median':
        median_value = df[column_name].median()
        df[column_name] = df[column_name] - median_value
    else:
        raise ValueError(f"Stratégie inconnue: {strategy}. Les stratégies valides sont 'mean' et 'median'.")
    
    return df
