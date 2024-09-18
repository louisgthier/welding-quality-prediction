# -*- coding: utf-8 -*-
import os

# DEFINING PATHS

dirname = os.path.dirname(__file__)

DATA_PATH = "./data/"

# RAW FILE NAME
DATA_OBJECT_NAME = "welddb.data"
DATA_OBJECT_CLEANED_NAME = "welddb_no_trailing_space.data"

# RELATIVE PATH TO FILE NAME
DATA_FILE = DATA_PATH + DATA_OBJECT_NAME
DATA_FILE_MODIFIED = DATA_PATH + DATA_OBJECT_CLEANED_NAME

# FILE NAMES ON OS
FILE_NAME = os.path.join(dirname, DATA_FILE)
FILE_MODIFIED_NAME = os.path.join(dirname, DATA_FILE_MODIFIED)
