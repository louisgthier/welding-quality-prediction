# --------------------------------
# Creator: Martin
# Date: 2024-10-06
# Description: This file contains utility functions for model retrieval, training, and evaluation.
# --------------------------------

# Importing required libraries

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn
import importlib
from collections import defaultdict

# --------------------------------
# SKLEARN models
# --------------------------------

def get_sklearn_algorithms(verbose = False):
    """
    Explore all submodule of sklearn and fetch functions having a 'fit' attribute.

    Be careful : some functions are not models (ex : crossvalidators)
    Parameters :
        debug = print or not stuff on console
    Return :
        dict : { module : [ fit_functions] }
    """
    algos = defaultdict(list)
    if verbose: 
      print(dir(sklearn))
    for nom_module in dir(sklearn):
        if verbose:
           print(nom_module)
        try:
            to_import = "sklearn.%s"%nom_module
            module = importlib.import_module(to_import)
            for nom_fonction in dir(module):
                fonction = getattr(module, nom_fonction)
                if hasattr(fonction, "fit"):
                    if verbose : print (" nom algorithme  = ", nom_fonction)
                    algos[nom_module].append(fonction)
        except Exception as e:
            if verbose : print( e)
        if verbose: print ("="*30)
    return algos

def print_algos_structure(algos):
    """
    Print the structure of the algorithms dictionnary
    Parameters :
        algos : dict : { module : [ fit_functions] }
    """
    for key, value in algos.items():
        print(key)
        for algo in value:
            # print algo basename
            print('   ', algo.__name__.split('.')[-1])
        print()