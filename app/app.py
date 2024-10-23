# app.py

from flask import Flask, request, jsonify, send_file, render_template
import pandas as pd
import numpy as np
import joblib
from io import BytesIO

# For preprocessing and modeling
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import KNNImputer, SimpleImputer
from sklearn.metrics import mean_squared_error
from sklearn.decomposition import PCA
import xgboost as xgb

# Additional imports
from sklearn.model_selection import GroupKFold
import warnings

warnings.filterwarnings('ignore')

app = Flask(__name__)

# Global variables
models = {}
scaler_X = None
scaler_Y = None
encoder = None
numerical_cols_X = None
categorical_cols_X = None
Y_min = None
Y_max = None
numerical_imputer = None
categorical_imputer = None
df_columns_info = None
target_variables = ['Yield strength / MPa', 'Ultimate tensile strength / MPa', 'Elongation / %', 'Reduction of Area / %', 'Charpy impact toughness / J']
pca = None

def load_data():
    """
    Load the dataset from the local CSV file.
    """
    df = pd.read_csv('data/welddb_data.csv')
    return df

def preprocess_data(df, is_train=True):
    """
    Preprocess the data.
    
    Parameters:
    - df: pandas DataFrame to preprocess.
    - is_train: bool, True if preprocessing for training, False for inference.
    
    Returns:
    - Preprocessed DataFrame.
    """
    global numerical_cols_X, categorical_cols_X, scaler_X, scaler_Y, encoder, Y_min, Y_max, numerical_imputer, categorical_imputer, df_columns_info, pca

    # Drop columns not relevant
    df = df.drop(columns=['Weld ID'], errors='ignore')
    
    # Drop non-target columns known only with destructive testing
    df = df.drop(columns=['50% FATT'], errors='ignore')
    
    if not is_train:
        # Drop columns not present in the training data
        columns_to_keep = [x["name"] for x in df_columns_info if x["name"] in df.columns.tolist()]
        columns_to_drop = [col for col in df.columns if col not in columns_to_keep]
        df = df.drop(columns=columns_to_drop)
        
        # Add columns that are missing in the input data, and fill with missing values
        columns_to_add = [x["name"] for x in df_columns_info if x["name"] not in df.columns.tolist()]
        for col in columns_to_add:
            df[col] = np.nan
                    
        # Reorder columns in the same order as the training data
        df = df[[x["name"] for x in df_columns_info if x["name"]]]
        
        # Replace all Charpy temperature values with -40
        df['Charpy temperature / °C'] = -40.0
    
    # Handle columns with special characters
    columns_to_convert = [
        "Sulphur concentration / weight %",
        "Molybdenum concentration / weight %",
        "Vanadium concentration / weight %",
        "Copper concentration / weight %",
        "Cobalt concentration / weight %",
        "Tungsten concentration / weight %",
        "Titanium concentration / parts per million by weight",
        "Nitrogen concentration / parts per million by weight",
        "Aluminium concentration / parts per million by weight",
        "Boron concentration / parts per million by weight",
        "Niobium concentration / parts per million by weight",
        "Tin concentration / parts per million by weight",
        "Arsenic concentration / parts per million by weight",
        "Antimony concentration / parts per million by weight",
        "Primary ferrite in microstructure / %",
        "Electrode positive or negative",
        "Interpass temperature / °C"
    ]

    columns_to_convert = [col for col in columns_to_convert if col in df.columns]
    df[columns_to_convert] = df[columns_to_convert].replace({'<': '', '>': ''}, regex=True)

    # Handle 'Hardness / kg mm^{-2}'
    if 'Hardness / kg mm^{-2}' in df.columns:
        df['Hardness / kg mm^{-2}'] = df['Hardness / kg mm^{-2}'].str.extract('(\d+)', expand=False)
        df['Hardness / kg mm^{-2}'] = pd.to_numeric(df['Hardness / kg mm^{-2}'], errors='coerce')

    # Handle 'Electrode positive or negative'
    if 'Electrode positive or negative' in df.columns:
        df['Electrode positive or negative'] = df['Electrode positive or negative'].replace({'+': 1, '-': -1})

    # Handle 'Interpass temperature / °C'
    if 'Interpass temperature / °C' in df.columns and df['Interpass temperature / °C'].dtype == 'O':
        # Replace ranges with their average
        mask = df['Interpass temperature / °C'].str.contains('-', na=False)
        df.loc[mask, 'Interpass temperature / °C'] = df.loc[mask, 'Interpass temperature / °C'].str.split('-').apply(
            lambda x: (int(x[0]) + int(x[1])) / 2 if len(x) == 2 else np.nan
        )
        df['Interpass temperature / °C'] = pd.to_numeric(df['Interpass temperature / °C'], errors='coerce')

    # Convert specified columns to numeric
    for column in columns_to_convert:
        df[column] = pd.to_numeric(df[column], errors='coerce')
        
    
    numerical_cols = df.select_dtypes(include=['float64', 'int64']).columns
    categorical_cols = df.select_dtypes(include=['object']).columns

    # Add Missingness Indicators
    interesting_missingness =  ['Chromium concentration / weight %', 'Tungsten concentration / weight %', 'Copper concentration / weight %', 'Molybdenum concentration / weight %', 'Tin concentration / parts per million by weight', 'Antimony concentration / parts per million by weight', 'Nickel concentration / weight %', 'Arsenic concentration / parts per million by weight', 'Cobalt concentration / weight %']
    for col in interesting_missingness:
        if col in df.columns:
            df[f'{col}_missing'] = df[col].isnull().astype(int)
        else:
            # If the column is not present in the input data, add it with all missing values
            df[f'{col}_missing'] = 1

    if is_train:
        # Drop columns with too many missing values (more than 80%)
        threshold = 0.80 * len(df)
        missing_values = df.isnull().sum()
        columns_to_keep = missing_values[missing_values <= threshold].index
        removed_columns = missing_values[missing_values > threshold].index
        df = df[columns_to_keep]
        
        numerical_cols = [col for col in numerical_cols if col not in removed_columns]

        # Separate features and targets
        X = df.drop(columns=target_variables, errors='ignore')
        Y = df[target_variables] if any(target in df.columns for target in target_variables) else pd.DataFrame()

        # Define numerical and categorical columns
        numerical_cols_X = [col for col in X.columns if col in numerical_cols]
        categorical_cols_X = X.select_dtypes(include=['object']).columns
    else:
        X = df.drop(columns=target_variables, errors='ignore')
    # Handle Imputation
    if is_train:
        # Initialize imputers
        numerical_imputer = SimpleImputer(strategy='median')
        X[numerical_cols_X] = numerical_imputer.fit_transform(X[numerical_cols_X])
    else:
        # Load the imputer
        X[numerical_cols_X] = numerical_imputer.transform(X[numerical_cols_X])

    # Handle Categorical Imputation
    if is_train:
        # Fit the mode for each categorical column
        categorical_imputer = SimpleImputer(strategy='most_frequent')
        X[categorical_cols_X] = categorical_imputer.fit_transform(X[categorical_cols_X])
    else:
        # Load the imputer
        X[categorical_cols_X] = categorical_imputer.transform(X[categorical_cols_X])

    # Handle Encoding
    if is_train:
        # Initialize OneHotEncoder with predefined categories
        known_categories = [
            ['AC', 'DC'],  # Categories for 'AC or DC'
            ['MMA', 'FCA', 'ShMA', 'SAA', 'TSA', 'NGSAW', 'GMAA', 'SA', 'GTAA', 'NGGMA']  # Categories for 'Type of weld'
        ]
        encoder = OneHotEncoder(categories=known_categories, drop='first', sparse_output=False, handle_unknown='ignore')
        encoded_nominal = encoder.fit_transform(X[['AC or DC', 'Type of weld']])
        encoded_nominal_df = pd.DataFrame(encoded_nominal, columns=encoder.get_feature_names_out(['AC or DC', 'Type of weld']), index=X.index)

        # Drop original categorical columns and concatenate encoded ones
        X = X.drop(columns=['AC or DC', 'Type of weld'], errors='ignore')
        X = pd.concat([X, encoded_nominal_df], axis=1)
    else:
        # Transform categorical columns
        encoded_nominal = encoder.transform(X[['AC or DC', 'Type of weld']])
        encoded_nominal_df = pd.DataFrame(encoded_nominal, columns=encoder.get_feature_names_out(['AC or DC', 'Type of weld']), index=X.index)

        # Drop original categorical columns and concatenate encoded ones
        X = X.drop(columns=['AC or DC', 'Type of weld'], errors='ignore')
        X = pd.concat([X, encoded_nominal_df], axis=1)

    # Handle Scaling
    if is_train:
        scaler_X = StandardScaler()
        X[numerical_cols_X] = scaler_X.fit_transform(X[numerical_cols_X])
    else:
        X[numerical_cols_X] = scaler_X.transform(X[numerical_cols_X])

    # Handle PCA (optional, uncomment to use)
    if is_train:
        pca = PCA(n_components=0.95)  # Retain 95% variance
        principal_components = pca.fit_transform(X[numerical_cols_X])
    else:
        principal_components = pca.transform(X[numerical_cols_X])
    # Create DataFrame for PCA components with renamed columns
    pca_columns = [f'PC{i+1}' for i in range(principal_components.shape[1])]
    principal_components_df = pd.DataFrame(principal_components, columns=pca_columns, index=X.index)
    # Add PCA components back to X if PCA is used
    X = pd.concat([X.drop(columns=numerical_cols_X), principal_components_df], axis=1)
    
    if is_train:
        # Prepare df_columns_info for the /get_fields endpoint
        df_columns_info = []
        # Numerical fields
        for col in numerical_cols_X:
            df_columns_info.append({
                'name': col,
                'type': 'numerical'
            })
        # Categorical fields with possible values
        for idx, col in enumerate(categorical_cols_X):
            categories = known_categories[idx]
            df_columns_info.append({
                'name': col,
                'type': 'categorical',
                'values': categories
            })
            
    # If training, also handle target variables
    if is_train and not Y.empty:
        # Store min and max of Y
        Y_min = Y.min()
        Y_max = Y.max()

        # Scale Y
        scaler_Y = StandardScaler()
        Y_scaled = pd.DataFrame(scaler_Y.fit_transform(Y), columns=Y.columns)

        return X, Y_scaled
    else:
        return X

def train_models(X, Y_scaled):
    """
    Train models for each target variable.
    
    Parameters:
    - X: Preprocessed feature DataFrame.
    - Y_scaled: Scaled target DataFrame.
    
    Returns:
    - Trained models dictionary.
    """
    global models, Y_min, Y_max

    target_variables = ['Yield strength / MPa', 'Ultimate tensile strength / MPa', 'Elongation / %', 'Reduction of Area / %', 'Charpy impact toughness / J']

    # Initialize dictionary to hold models
    models = {}

    # Define GroupKFold for cross-validation
    group_kfold = GroupKFold(n_splits=5)

    for target in target_variables:
        print(f"Training model for {target}")
        
        # Create labeled mask
        labeled_mask = Y_scaled[target].notnull()

        # Define features and target
        X_labeled = X[labeled_mask]
        y_labeled = Y_scaled[target][labeled_mask]

        # Initialize model (XGBoost as an example)
        model = xgb.XGBRegressor(
            objective='reg:squarederror',
            subsample=0.75,
            n_estimators=900,
            max_depth=3,
            learning_rate=0.1,
            colsample_bytree=1.0,
            random_state=42
        )

        # Fit the model
        model.fit(X_labeled, y_labeled)

        # Save the model
        models[target] = model

    return models

def make_predictions(df_processed):
    """
    Make predictions for each target variable.
    
    Parameters:
    - df_processed: Preprocessed DataFrame ready for prediction.
    
    Returns:
    - Dictionary of predictions.
    """
    global models, scaler_Y, Y_min, Y_max

    predictions = {}
    
    print("DF_Processed_columns:", df_processed.columns)

    # For each target variable, make prediction
    for target in target_variables:
        model = models.get(target)
        if model:
            y_pred_scaled = model.predict(df_processed)
            # Prepare array to store predictions for all target variables
            y_pred_scaled_full = np.zeros((len(y_pred_scaled), len(target_variables)))
            # Place the scaled predictions at the correct position
            idx = target_variables.index(target)
            y_pred_scaled_full[:, idx] = y_pred_scaled
            # Inverse transform
            y_pred_full = scaler_Y.inverse_transform(y_pred_scaled_full)
            y_pred = y_pred_full[:, idx]
            predictions[target + "_prediction"] = y_pred.tolist()
        else:
            predictions[target + "_prediction"] = None

    # Compute combined score (normalized between 0 and 1)
    for target in target_variables:
        min_value = Y_min[target]
        max_value = Y_max[target]
        predictions[target + '_prediction_normalized'] = [
            (x - min_value) / (max_value - min_value) if max_value != min_value else 0
            for x in predictions[target + "_prediction"]
        ]

    # Compute combined score as average of normalized predictions
    combined_score = np.mean(
        [predictions[target + '_prediction_normalized'] for target in target_variables],
        axis=0
    )
    predictions['combined_score'] = combined_score.tolist()

    return predictions

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    # Convert data to DataFrame
    df = pd.DataFrame([data])

    # Preprocess the input data (is_train=False)
    df_processed = preprocess_data(df, is_train=False)

    # Make predictions
    predictions = make_predictions(df_processed)

    return jsonify(predictions)

@app.route('/predict_file', methods=['POST'])
def predict_file():
    if 'file' not in request.files:
        return 'No file part in the request', 400

    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400

    if file:
        # Read the CSV file
        df = pd.read_csv(file)
        
        # Replace all Charpy temperature values with -40 (Median)
        df['Charpy temperature / °C'] = -40.0

        # Preprocess the input data (is_train=False)
        df_processed = preprocess_data(df, is_train=False)

        # Make predictions
        predictions = make_predictions(df_processed)

        # Create DataFrame with predictions
        df_predictions = pd.DataFrame(predictions)

        # RMSE Calculation for each target
        target_variables = [['Yield strength / MPa', 'Ultimate tensile strength / MPa', 'Elongation / %', 'Reduction of Area / %', 'Charpy impact toughness / J']]
        rmse_results = {}
        for target in target_variables:
            if target in df.columns:
                # Get true and predicted values, ignoring NaN values
                true_values = df[target].values
                predicted_values = df_predictions[target + "_prediction"].values

                # Mask to ignore NaN values in either true or predicted
                mask = ~np.isnan(true_values) & ~np.isnan(predicted_values)

                if mask.sum() > 0:
                    # Calculate RMSE only for non-NaN values
                    rmse = mean_squared_error(true_values[mask], predicted_values[mask], squared=False)
                    rmse_results[target] = rmse
                else:
                    print(f"No valid values for target {target}")
                    rmse_results[target] = None
            else:
                print(f"Target {target} not found in input data")
                rmse_results[target] = None

        # Optionally, you can add RMSE results to the output
        # For example, add a summary section
        summary_df = pd.DataFrame(list(rmse_results.items()), columns=['Target', 'RMSE'])
        df_output = pd.concat([df.reset_index(drop=True), df_predictions.reset_index(drop=True)], axis=1)
        
        # Optionally, save RMSE to a separate sheet or include in the CSV as needed

        # Convert DataFrame to CSV
        output = BytesIO()
        df_output.to_csv(output, index=False)
        output.seek(0)

        return send_file(output, mimetype='text/csv', download_name='predictions.csv', as_attachment=True)

@app.route('/get_fields', methods=['GET'])
def get_fields():
    global df_columns_info
    # Remove Charpy temperature from the list of fields
    fields = [x for x in df_columns_info if x["name"] != "Charpy temperature / °C"]
    return jsonify(fields)

@app.route('/')
def home():
    return render_template('index.html')


if __name__ == '__main__':
    # Load data
    df = load_data()

    # Preprocess data (is_train=True)
    X, Y_scaled = preprocess_data(df, is_train=True)

    # Train models
    models = train_models(X, Y_scaled)

    # Run the app
    app.run(host="0.0.0.0", port=5123, debug=True)
