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
