"""
This script, data_handling.py, is focused on data operations for the intermediate analytics part of the OrestisCompany analytics dashboard. 
It handles the reading and optional sorting of CSV files containing intermediate analytics data.

Functionality:
1. read_data_intermediate: 
    Reads CSV files from the '/app/data/analytics/intermediate' directory. 
    It provides the capability to sort the data based on specified columns, including a special sorting feature for the 'weekday' column.

Key Parameters:
- file_name: The name of the CSV file to be read.
- sort_by: Optional. The column name on which the data frame should be sorted. Special handling is included for sorting by the 'weekday' column.
- ascending: Optional. A boolean that defines the sorting order (ascending or descending).

The function attempts to read the specified file, and if sorting parameters are provided, it sorts the data as requested. 
Special handling for the 'weekday' column allows for sorting data in the natural order of the days of the week. 
In case of any errors during file reading or processing, the function returns None. 
This functionality is key in preparing intermediate analytics data for visualization.

Usage:
    To read and optionally sort an intermediate analytics data file, use:
    df = read_data_intermediate('file_name.csv', sort_by='column_name', ascending=True/False)
"""

import pandas as pd
import os

def read_data_intermediate(file_name, sort_by=None, ascending=False):
    DATA_DIR = '/app/data/analytics/intermediate'
    try:
        df = pd.read_csv(os.path.join(DATA_DIR, file_name))

        # Check if we need to sort by weekday and if 'weekday' is a column
        if sort_by == 'weekday' and 'weekday' in df.columns:
            days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            # Create a categorical data type with the days of the week in order
            weekday_category = pd.CategoricalDtype(categories=days_of_week, ordered=True)
            # Convert the 'weekday' column to this categorical data type
            df['weekday'] = df['weekday'].astype(weekday_category)
            # Sort the DataFrame by the 'weekday' column
            df.sort_values(by='weekday', ascending=ascending, inplace=True)
        elif sort_by and sort_by in df.columns:
            # If we're sorting by another column, just sort it as usual
            df.sort_values(by=sort_by, ascending=ascending, inplace=True)
        return df
    except: 
        return None
