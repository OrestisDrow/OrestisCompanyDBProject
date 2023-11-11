"""
This script, data_handling.py, handles data operations for the advanced analytics section of the OrestisCompany analytics dashboard. 
Its primary role is to read and process CSV files that store advanced analytics data, providing vital information for visualization and analysis.

Functionality:
1. read_data_advanced: 
    Reads CSV files from the '/app/data/analytics/advanced' directory. It includes an option to sort the data based on specified columns, enhancing the flexibility and utility of the data retrieval process.

Key Parameters:
- file_name: The name of the CSV file to be read.
- sort_by: Optional. The column name based on which the data frame should be sorted.
- ascending: Optional. A boolean that determines the sorting order (ascending by default).

The function attempts to read the specified file from the advanced analytics data directory. If sorting parameters are provided, it sorts the data accordingly. This functionality is critical for preparing and presenting advanced analytics data in a meaningful way on the dashboard. In case of any issues during file reading or processing, the function returns None as a fail-safe.

Usage:
    To read and optionally sort an advanced analytics data file, use:
    df = read_data_advanced('file_name.csv', sort_by='column_name', ascending=True/False)
"""

import pandas as pd
import os

def read_data_advanced(file_name, sort_by=None, ascending=True):
    DATA_DIR = '/app/data/analytics/advanced'
    try:
        df = pd.read_csv(os.path.join(DATA_DIR, file_name))
        if sort_by and sort_by in df.columns:
            df = df.sort_values(by=sort_by, ascending=ascending)
        return df
    except:
        return None