# -*- coding: utf-8 -*-

# DATA IMPORT

import pandas as pd
import numpy as np
import re

from variables import FILE_MODIFIED_NAME, FILE_NAME


# WE NEED TO MODIFY THE FILE TO REMOVE TRAILING WHITESPACES
# WE ALSO NEED TO REMOVE DOUBLE SPACES
# TO DO THAT, WE WILL DEFINE A FUNCTION TO PREPROCESS THE DATA


@staticmethod
def preprocess_text_file(input_file: str, output_file: str):
    """
    Removes trailing whitespaces from a file
    """
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    processed_lines = [
        re.sub(r'\s\s+', ' ', line.rstrip()) + '\n' for line in lines]

    with open(output_file, 'w', encoding='utf-8') as file:
        file.writelines(processed_lines)


preprocess_text_file(FILE_NAME, FILE_MODIFIED_NAME)

# IMPORT THE FILE WITH PANDAS
BASIC_DATAFRAME = pd.read_csv(FILE_MODIFIED_NAME, names=[
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
    na_values=["N"]
)

BASIC_DATAFRAME.replace("N", np.nan, inplace=True)

BASIC_DATAFRAME.head(5)
