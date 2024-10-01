# -*- coding: utf-8 -*-
import os

# DEFINING PATHS

dirname = os.path.dirname(__file__)

DATA_PATH = "./data/"
WELD_TYPE_PATH = DATA_PATH + "weld_type_analysis/"

# RAW FILE NAME
DATA_OBJECT_NAME = "welddb.data"
DATA_OBJECT_CLEANED_NAME = "welddb_no_trailing_space.data"

# RELATIVE PATH TO FILE NAME
DATA_FILE = DATA_PATH + DATA_OBJECT_NAME
DATA_FILE_MODIFIED = DATA_PATH + DATA_OBJECT_CLEANED_NAME

# FILE NAMES ON OS
FILE_NAME = os.path.join(dirname, DATA_FILE)
FILE_MODIFIED_NAME = os.path.join(dirname, DATA_FILE_MODIFIED)

# CSV FILE
ORIGINAL_DATA_PATH = DATA_PATH + "welddb_data.csv"
CLEANED_CSV_PATH = DATA_PATH + "welddb_cleaned.csv"
MISSING_PERCENTAGE_CSV_PATH = DATA_PATH + "missing_percent.csv"
FCA_CSV_PATH = WELD_TYPE_PATH + "FCA_group.csv"
CHARPY_CSV_PATH = DATA_PATH + "Charpy_group.csv"
QUALITY_CSV_PATH = DATA_PATH + "Quality_group.csv"