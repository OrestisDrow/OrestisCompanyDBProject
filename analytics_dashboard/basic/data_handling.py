import pandas as pd
import os

def read_data_basic(file_name, sort_by=None, ascending=False):
    DATA_DIR = '/app/data/analytics/basic'
    try:
        df = pd.read_csv(os.path.join(DATA_DIR, file_name))
        if sort_by and sort_by in df.columns:
            df = df.sort_values(by=sort_by, ascending=ascending)
        return df
    except FileNotFoundError:
        print(f"The file {file_name} was not found in the directory.")
        return None
    except pd.errors.EmptyDataError:
        print(f"The file {file_name} is empty.")
        return None
    except pd.errors.ParserError:
        print(f"The file {file_name} contains parsing errors.")
        return None
    except Exception as e:  # Handle unforeseen errors
        print(f"An error occurred while reading {file_name}: {e}")
        return None