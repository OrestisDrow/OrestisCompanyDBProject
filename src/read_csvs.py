import os
import pandas as pd

def display_csv_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            filepath = os.path.join(directory, filename)
            if os.path.getsize(filepath) == 0:
                print(f"{filename} is empty!")
            else:
                print(f"Content of {filename}:")
                df = pd.read_csv(filepath)
                print(df)
                print('-' * 50)  # A separator for better readability


directory_path = "/app/data/analytics/basic"  # Adjust this path
display_csv_files(directory_path)
