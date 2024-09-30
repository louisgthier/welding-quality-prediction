# Basic imports
import re
import pandas as pd
import numpy as np

# Import paths from paths.py
from paths import FILE_MODIFIED_NAME, FILE_NAME, ORIGINAL_DATA_PATH

@staticmethod
def preprocess_text_file(input_file: str, output_file: str):
    """
    # WE NEED TO MODIFY THE FILE TO REMOVE TRAILING WHITESPACES
    # WE ALSO NEED TO REMOVE DOUBLE SPACES
    # TO DO THAT, WE WILL DEFINE A FUNCTION TO PREPROCESS THE DATA

    Removes trailing whitespaces from a file
    Takes in a file and output it in ./data/ section
    """
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    processed_lines = [
        re.sub(r'\s\s+', ' ', line.rstrip()) + '\n' for line in lines]

    with open(output_file, 'w', encoding='utf-8') as file:
        file.writelines(processed_lines)


def data_import(file_path: str):
    """
    Produces the data Import
    - Removes unnecesary spaces
    - Removes trailing spaces
    - Changes "N" to NaN values
    """

    preprocess_text_file(FILE_NAME, FILE_MODIFIED_NAME)

    # Définir les types de données des colonnes
    dtype_dict = {
        'Carbon concentration / weight %': 'float64',
        'Silicon concentration / weight %': 'float64',
        'Manganese concentration / weight %': 'float64',
        'Sulphur concentration / weight %': 'float64',
        'Phosphorus concentration / weight %': 'float64',
        'Nickel concentration / weight %': 'float64',
        'Chromium concentration / weight %': 'float64',
        'Molybdenum concentration / weight %': 'float64',
        'Vanadium concentration / weight %': 'float64',
        'Copper concentration / weight %': 'float64',
        'Cobalt concentration / weight %': 'float64',
        'Tungsten concentration / weight %': 'float64',
        'Oxygen concentration / parts per million by weight': 'float64',
        'Titanium concentration / parts per million by weight': 'float64',
        'Nitrogen concentration / parts per million by weight': 'float64',
        'Aluminium concentration / parts per million by weight': 'float64',
        'Boron concentration / parts per million by weight': 'float64',
        'Niobium concentration / parts per million by weight': 'float64',
        'Tin concentration / parts per million by weight': 'float64',
        'Arsenic concentration / parts per million by weight': 'float64',
        'Antimony concentration / parts per million by weight': 'float64',
        'Current / A': 'float64',
        'Voltage / V': 'float64',
        'AC or DC': 'str',  # AC or DC, we will one-hot encode it later
        'Electrode positive or negative': 'str',
        'Heat input / kJ mm^{-1}': 'float64',
        'Interpass temperature / °C': 'float64',
        'Type of weld': 'str',  # Catégorisation du type de soudure
        'Post weld heat treatment temperature / °C': 'float64',
        'Post weld heat treatment time / hours': 'float64',
        'Yield strength / MPa': 'float64',
        'Ultimate tensile strength / MPa': 'float64',
        'Elongation / %': 'float64',
        'Reduction of Area / %': 'float64',
        'Charpy temperature / °C': 'float64',
        'Charpy impact toughness / J': 'float64',
        'Hardness / kg mm^{-2}': 'float64',
        '50% FATT': 'float64',
        'Primary ferrite in microstructure / %': 'float64',
        'Ferrite with second phase / %': 'float64',
        'Acicular ferrite / %': 'float64',
        'Martensite / %': 'float64',
        'Ferrite with carbide aggregate / %': 'float64',
        'Weld ID': 'str'  # Identifiant
    }

    # Importer le fichier CSV avec spécification des types
    basic_dataframe = pd.read_csv(FILE_MODIFIED_NAME,
                                names=[
                                    'Carbon concentration / weight %',
                                    'Silicon concentration / weight %',
                                    'Manganese concentration / weight %',
                                    'Sulphur concentration / weight %',
                                    'Phosphorus concentration / weight %',
                                    'Nickel concentration / weight %',
                                    'Chromium concentration / weight %',
                                    'Molybdenum concentration / weight %',
                                    'Vanadium concentration / weight %',
                                    'Copper concentration / weight %',
                                    'Cobalt concentration / weight %',
                                    'Tungsten concentration / weight %',
                                    'Oxygen concentration / parts per million by weight',
                                    'Titanium concentration / parts per million by weight',
                                    'Nitrogen concentration / parts per million by weight',
                                    'Aluminium concentration / parts per million by weight',
                                    'Boron concentration / parts per million by weight',
                                    'Niobium concentration / parts per million by weight',
                                    'Tin concentration / parts per million by weight',
                                    'Arsenic concentration / parts per million by weight',
                                    'Antimony concentration / parts per million by weight',
                                    'Current / A',
                                    'Voltage / V',
                                    'AC or DC',
                                    'Electrode positive or negative',
                                    'Heat input / kJ mm^{-1}',
                                    'Interpass temperature / °C',
                                    'Type of weld',
                                    'Post weld heat treatment temperature / °C',
                                    'Post weld heat treatment time / hours',
                                    'Yield strength / MPa',
                                    'Ultimate tensile strength / MPa',
                                    'Elongation / %',
                                    'Reduction of Area / %',
                                    'Charpy temperature / °C',
                                    'Charpy impact toughness / J',
                                    'Hardness / kg mm^{-2}',
                                    '50% FATT',
                                    'Primary ferrite in microstructure / %',
                                    'Ferrite with second phase / %',
                                    'Acicular ferrite / %',
                                    'Martensite / %',
                                    'Ferrite with carbide aggregate / %',
                                    'Weld ID'
                                ],
                                delimiter=' ',
                                decimal='.',
                                na_values=["N"]
                                )

    # On remplace les valeurs 'N' par des NaN values
    # Il s'agit d'une bonne pratique pour travailler avec pandas
    basic_dataframe.replace("N", np.nan, inplace=True)

    # Save the dataframe to a csv
    basic_dataframe.to_csv(file_path, index=False)
    basic_dataframe.head(5)

if __name__ == "__main__":
    data_import(ORIGINAL_DATA_PATH)