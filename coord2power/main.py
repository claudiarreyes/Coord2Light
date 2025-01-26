import os
import pandas as pd
import numpy as np
from astropy.table import Table
from astropy.io import fits
import lightkurve as lk
from coord2power.utils import create_coord_string, save_lightcurves, download_lightcurves

# Define base directory for the project
BASE_DIR = '/Users/creyes/Projects/harps'
TABLE_DIR = os.path.join(BASE_DIR, 'tables')
LC_DIR = os.path.join(BASE_DIR, 'lightcurves')

# Ensure required directories exist
os.makedirs(TABLE_DIR, exist_ok=True)
os.makedirs(LC_DIR, exist_ok=True)

def main():
    # Load initial DataFrame
    df = pd.read_csv(os.path.join(BASE_DIR, 'input.csv'))  # Replace with your actual file path
    
    # Add coordinate strings
    df['coord_string'] = create_coord_string(df['alpha'], df['delta'])
    
    # Step 1: Search lightcurves and save tables
    for _, row in df.iterrows():
        try:
            search_table = lk.search_lightcurve(row['coord_string']).table
            file_path = os.path.join(TABLE_DIR, f"{row['target_name']}.ecsv")
            search_table.write(file_path, overwrite=True)
        except Exception as e:
            print(f"Error for {row['target_name']}: {e}")
    
    # Step 2: Process lightcurve tables
    mission_list, nobs, tables = [], [], []
    for _, row in df.iterrows():
        table_path = os.path.join(TABLE_DIR, f"{row['target_name']}.ecsv")
        if os.path.exists(table_path):
            try:
                table = Table.read(table_path)
                mission_list.append(list(set(table['project'])))
                nobs.append(len(table))
                tables.append(table)
            except Exception as e:
                print(f"Error reading {row['target_name']} table: {e}")
                mission_list.append([])
                nobs.append(0)
                tables.append(None)
        else:
            mission_list.append([])
            nobs.append(0)
            tables.append(None)
    
    # Add columns to DataFrame
    df['mission'] = mission_list
    df['number_of_lightcurves'] = nobs
    df['tables'] = tables

    # Save updated DataFrame as a pickle
    df.to_pickle(os.path.join(TABLE_DIR, 'updated_dataframe.pkl'))

    # Step 3: Download lightcurves
    df_with_tables = df[df['number_of_lightcurves'] > 0]
    for _, row in df_with_tables.iterrows():
        save_lightcurves(row['tables'], row['target_name'], LC_DIR)

if __name__ == "__main__":
    main()
