"""
This script, data_handling.py, is dedicated to handling data operations for the basic analytics part of the OrestisCompany analytics dashboard. 
It primarily focuses on reading and processing CSV files that contain basic analytics data.

Functionality:
1. read_data_basic: 
    Reads CSV files from the '/app/data/analytics/basic' directory. 
    It offers optional sorting functionality based on specified columns. 

Key Parameters:
- file_name: The name of the CSV file to be read.
- sort_by: Optional. The column name on which the data frame should be sorted.
- ascending: Optional. A boolean that defines the sorting order (ascending or descending).

The function tries to read the specified file and, if sorting parameters are provided, sorts the data accordingly. In case of any errors, it safely returns None. This function is crucial for retrieving and preparing basic analytics data for visualization in the dashboard.

Usage:
    To read and optionally sort a basic analytics data file, call:
    df = read_data_basic('file_name.csv', sort_by='column_name', ascending=True/False)
"""

import pandas as pd
import os

def read_data_basic(file_name, sort_by=None, ascending=False):
    DATA_DIR = '/app/data/analytics/basic'
    try:
        df = pd.read_csv(os.path.join(DATA_DIR, file_name))
        if sort_by and sort_by in df.columns:
            df = df.sort_values(by=sort_by, ascending=ascending)
        return df
    except:
        return None