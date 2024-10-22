# app.py

from flask import Flask, request, jsonify, send_file, render_template
import pandas as pd
import numpy as np
import joblib
from io import BytesIO

# For preprocessing and modeling
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import KNNImputer, SimpleImputer
from sklearn.metrics import root_mean_squared_error
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

def load_and_preprocess_data():
    global numerical_cols_X, categorical_cols_X, scaler_X, scaler_Y, encoder, Y_min, Y_max, numerical_imputer, categorical_imputer, df_columns_info

    # Load dataset from the local file
    df = pd.read_csv('data/welddb_data.csv')

    df = df.drop(columns=['Weld ID'])
    
    # Drop non-target that are known only with destructive testing
    df = df.drop(columns=['Elongation / %', 'Reduction of Area / %', '50% FATT'])

    # Handle columns with special characters
    columns_to_convert = ["Sulphur concentration / weight %",
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
    if 'Interpass temperature / °C' in df.columns:
        index = df['Interpass temperature / °C'].str.contains('-', na=False)
        df.loc[index, 'Interpass temperature / °C'] = df.loc[index, 'Interpass temperature / °C'].str.split('-').apply(lambda x: (int(x[0]) + int(x[1])) / 2)
        df['Interpass temperature / °C'] = pd.to_numeric(df['Interpass temperature / °C'], errors='coerce')

    # Convert columns to numeric
    for column in columns_to_convert:
        df[column] = pd.to_numeric(df[column], errors='coerce')

    # Drop columns with too many missing values
    threshold = 0.80 * len(df)
    missing_values = df.isnull().sum()
    columns_to_keep = missing_values[missing_values <= threshold].index
    df = df[columns_to_keep]

    # Impute missing values
    numerical_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    numerical_cols_X = [col for col in numerical_cols if col not in ['Yield strength / MPa', 'Ultimate tensile strength / MPa', 'Charpy impact toughness / J', 'group_id', 'Weld ID']]
    categorical_cols_X = df.select_dtypes(include=['object']).columns.tolist()

    # Impute missing values using KNNImputer
    numerical_imputer = SimpleImputer(strategy='median')
    df[numerical_cols_X] = numerical_imputer.fit_transform(df[numerical_cols_X])

    # Keep a categorical imputer for later use (store mode for each column)
    categorical_imputer = {col: df[col].mode().iloc[0] for col in categorical_cols_X}
    
    # For categorical columns, fill with mode (use categorical_imputer)
    for col in categorical_cols_X:
        df[col] = df[col].fillna(categorical_imputer[col])

    # Scale numerical features
    scaler_X = StandardScaler()
    df[numerical_cols_X] = scaler_X.fit_transform(df[numerical_cols_X])

    # Encode categorical variables
    nominal_cols_X = ['AC or DC', 'Type of weld']
    known_categories = [
        ['AC', 'DC'],  # Categories for 'AC or DC'
        ['MMA', 'FCA', 'ShMA', 'SAA', 'TSA', 'NGSAW', 'GMAA', 'SA', 'GTAA', 'NGGMA'],  # Categories for 'Type of weld'
    ]
    encoder = OneHotEncoder(categories=known_categories, drop='first', sparse_output=False)
    df_encoded_nominal = pd.DataFrame(
        encoder.fit_transform(df[nominal_cols_X]),
        columns=encoder.get_feature_names_out(nominal_cols_X)
    )
    df = df.drop(columns=nominal_cols_X)
    df = df.reset_index(drop=True)
    df_encoded_nominal = df_encoded_nominal.reset_index(drop=True)
    df = pd.concat([df, df_encoded_nominal], axis=1)

    # Drop 'Weld ID' column
    if 'Weld ID' in df.columns:
        df = df.drop(columns='Weld ID')

    # Define target variables
    target_variables = ['Yield strength / MPa', 'Ultimate tensile strength / MPa', 'Charpy impact toughness / J']

    # Store min and max of Y
    Y = df[target_variables]
    Y_min = Y.min()
    Y_max = Y.max()

    # Prepare df_columns_info for the /get_fields endpoint
    df_columns_info = []

    # Numerical fields
    for col in numerical_cols_X:
        df_columns_info.append({
            'name': col,
            'type': 'numerical'
        })

    # Categorical fields with possible values
    for idx, col in enumerate(nominal_cols_X):
        categories = known_categories[idx]
        df_columns_info.append({
            'name': col,
            'type': 'categorical',
            'values': categories
        })

    return df

def train_models(df):
    global models, scaler_Y, Y_min, Y_max

    # Define target variables
    target_variables = ['Yield strength / MPa', 'Ultimate tensile strength / MPa', 'Charpy impact toughness / J']

    # Initialize dictionary to hold models
    models = {}

    # Prepare X and Y
    X = df.drop(columns=target_variables)
    Y = df[target_variables]

    # Store min and max of Y
    Y_min = Y.min()
    Y_max = Y.max()

    # Scale Y
    scaler_Y = StandardScaler()
    Y_scaled = pd.DataFrame(scaler_Y.fit_transform(Y), columns=Y.columns)

    # For each target variable, train a model
    for target in target_variables:
        print(f"Training model for {target}")

        # Create labeled mask
        labeled_mask = Y_scaled[target].notnull()

        # Get labeled data
        X_labeled = X[labeled_mask]
        y_labeled = Y_scaled[target][labeled_mask]

        # Train model
        # Use XGBoost with predefined hyperparameters
        model = xgb.XGBRegressor(objective='reg:squarederror', subsample=0.75, n_estimators=900, max_depth=3, learning_rate=0.1, colsample_bytree=1.0, random_state=42)
        model.fit(X_labeled, y_labeled)

        # Save the model
        models[target] = model

    # Return the trained models
    return models

def preprocess_input_data(df_input):
    global numerical_cols_X, categorical_cols_X, scaler_X, encoder
    
    # Drop columns not present in the training data
    columns_to_keep = [x["name"] for x in df_columns_info if x["name"] in df_input.columns.tolist()]
    columns_to_drop = [col for col in df_input.columns if col not in columns_to_keep]
    df_input = df_input.drop(columns=columns_to_drop)
    
    print("Columns kept:", df_input.columns.tolist())
    
    # Add columns that are missing in the input data, and fill with missing values
    columns_to_add = [x["name"] for x in df_columns_info if x["name"] not in df_input.columns.tolist()]
    for col in columns_to_add:
        df_input[col] = np.nan
        
    print("Columns added:", columns_to_add)
    
    # Reorder columns in the same order as the training data
    df_input = df_input[[x["name"] for x in df_columns_info if x["name"]]]
    
    # Replace all Charpy temperature values with -40
    df_input['Charpy temperature / °C'] = -40.0

    # Handle columns with special characters
    columns_to_convert = ["Sulphur concentration / weight %",
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

    columns_to_convert = [col for col in columns_to_convert if col in df_input.columns]
    df_input[columns_to_convert] = df_input[columns_to_convert].replace({'<': '', '>': ''}, regex=True)

    # Handle 'Hardness / kg mm^{-2}'
    if 'Hardness / kg mm^{-2}' in df_input.columns:
        df_input['Hardness / kg mm^{-2}'] = df_input['Hardness / kg mm^{-2}'].str.extract('(\d+)', expand=False)
        df_input['Hardness / kg mm^{-2}'] = pd.to_numeric(df_input['Hardness / kg mm^{-2}'], errors='coerce')

    # Handle 'Electrode positive or negative'
    if 'Electrode positive or negative' in df_input.columns:
        df_input['Electrode positive or negative'] = df_input['Electrode positive or negative'].replace({'+': 1, '-': -1})

    # Handle 'Interpass temperature / °C'
    if 'Interpass temperature / °C' in df_input.columns and df_input['Interpass temperature / °C'].dtype == 'O':
        index = df_input['Interpass temperature / °C'].str.contains('-', na=False)
        df_input.loc[index, 'Interpass temperature / °C'] = df_input.loc[index, 'Interpass temperature / °C'].str.split('-').apply(lambda x: (int(x[0]) + int(x[1])) / 2)
        df_input['Interpass temperature / °C'] = pd.to_numeric(df_input['Interpass temperature / °C'], errors='coerce')

    # Convert columns to numeric
    for column in columns_to_convert:
        df_input[column] = pd.to_numeric(df_input[column], errors='coerce')

    # Impute missing values
    # For numerical columns, use numerical_imputer
    df_input[numerical_cols_X] = numerical_imputer.transform(df_input[numerical_cols_X])

    # For categorical columns, use categorical_imputer
    for col in categorical_cols_X:
        df_input[col] = df_input[col].fillna(categorical_imputer[col])

    # Scale numerical features
    df_input[numerical_cols_X] = scaler_X.transform(df_input[numerical_cols_X])

    # Encode categorical variables
    nominal_cols_X = ['AC or DC', 'Type of weld']
    df_encoded_nominal = pd.DataFrame(
        encoder.transform(df_input[nominal_cols_X]),
        columns=encoder.get_feature_names_out(nominal_cols_X)
    )
    df_input = df_input.drop(columns=nominal_cols_X)
    df_encoded_nominal = df_encoded_nominal.reset_index(drop=True)
    df_input = df_input.reset_index(drop=True)
    df_input = df_input = pd.concat([df_input, df_encoded_nominal], axis=1)

    # Drop 'Weld ID' column if present
    if 'Weld ID' in df_input.columns:
        df_input = df_input.drop(columns='Weld ID')

    return df_input

def make_predictions(df_processed):
    global models, scaler_Y, Y_min, Y_max

    predictions = {}
    target_variables = ['Yield strength / MPa', 'Ultimate tensile strength / MPa', 'Charpy impact toughness / J']

    # For each target variable, make prediction
    for target in target_variables:
        model = models.get(target)
        if model:
            y_pred_scaled = model.predict(df_processed)
            # Prepare an array to hold the scaled predictions for all targets
            y_pred_scaled_full = np.zeros((len(y_pred_scaled), len(target_variables)))
            # Place the scaled predictions at the correct position
            idx = target_variables.index(target)
            y_pred_scaled_full[:, idx] = y_pred_scaled
            # Inverse transform
            y_pred_full = scaler_Y.inverse_transform(y_pred_scaled_full)
            y_pred = y_pred_full[:, idx]
            predictions[target+"_prediction"] = y_pred.tolist()
        else:
            predictions[target+"_prediction"] = None

    # Compute combined score (normalized between 0 and 1)
    # Normalize each prediction using Y_min and Y_max
    for target in target_variables:
        min_value = Y_min[target]
        max_value = Y_max[target]
        predictions[target+'_prediction_normalized'] = [(x - min_value) / (max_value - min_value) for x in predictions[target+"_prediction"]]

    # Compute combined score as average of normalized predictions
    combined_score = np.mean([predictions[target+'_prediction_normalized'] for target in target_variables], axis=0)
    predictions['combined_score'] = combined_score.tolist()

    return predictions

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    # Convert data to DataFrame
    df_input = pd.DataFrame([data])

    # Preprocess the input data in the same way as the training data
    df_processed = preprocess_input_data(df_input)

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
        df_input = pd.read_csv(file)
        
        # Replace all Charpy temperature values with -40 (Median)
        df_input['Charpy temperature / °C'] = -40.0

        # Preprocess the input data
        df_processed = preprocess_input_data(df_input)

        # Make predictions
        predictions = make_predictions(df_processed)

        # Create DataFrame with predictions
        df_predictions = pd.DataFrame(predictions)
        
        # RMSE Calculation for each target
        target_variables = ['Yield strength / MPa', 'Ultimate tensile strength / MPa', 'Charpy impact toughness / J']
        rmse_results = {}
        print("DF input columns:", df_input.columns)
        for target in target_variables:
            if target in df_input.columns:
                # Get true and predicted values, ignoring NaN values
                true_values = df_input[target].values
                predicted_values = df_predictions[target+"_prediction"].values
                
                # Mask to ignore NaN values in either true or predicted
                mask = ~np.isnan(true_values) & ~np.isnan(predicted_values)
                
                if mask.sum() > 0:
                    # Calculate RMSE only for non-NaN values
                    rmse = root_mean_squared_error(true_values[mask], predicted_values[mask])
                    rmse_results[target] = rmse
                else:
                    print(f"No valid values for target {target}")
                    rmse_results[target] = None
            else:
                print(f"Target {target} not found in input data")
                rmse_results[target] = None

        # Print RMSE for debugging or return it with the predictions (optional)
        # print("RMSE Results:", rmse_results)

        # Concatenate with input data if needed
        # df_output = df_predictions
        df_output = pd.concat([df_input.reset_index(drop=True), df_predictions], axis=1)

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
    # Load and preprocess data
    df = load_and_preprocess_data()

    # Train models
    models = train_models(df)

    # Run the app
    app.run(host="0.0.0.0", port=5123, debug=True)
