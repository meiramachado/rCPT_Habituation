import pandas as pd
import numpy as np
import os
import re  # Add import for regular expressions

def apply_formulas(df):
    # Creating a new DataFrame with calculated measures
    binary_df = pd.DataFrame()
    binary_df['Time'] = df.iloc[:, 0]  # Column A
    binary_df['TTL #1'] = np.where(df.iloc[:, 3] == "TTL #1", 1, 0)  # Column D
    binary_df['Reward Tray Light on (priming excluded)'] = np.where(df.iloc[:, 3].isin(["Feed again"]), 1, 0)  # Column D
    binary_df['Reward Tray Entered (priming excluded)'] = np.where(df.iloc[:, 3].isin(["Note Tray Entry"]), 1, 0)  # Column D
    binary_df['Reward Tray Light on (priming included)'] = np.where((df.iloc[:, 2] == "Output On Event") & (df.iloc[:, 3] == "TrayLight #1"), 1, 0)  # Columns C & D
    binary_df['Reward Tray Entered (priming included)'] = np.where(df.iloc[:, 3].isin(["Note Tray Entry"]), 1, 0)  # Column D
    return binary_df

def generate_binary_file(input_folder, output_folder, filename_prefix="DESKTOP"):
    input_folder = os.path.abspath(input_folder)  # Get absolute path for compatibility
    output_folder = os.path.abspath(output_folder)  # Get absolute path for compatibility
    
    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)
    
    for file in os.listdir(input_folder):
        if file.startswith(filename_prefix) and file.endswith(".csv"):
            input_path = os.path.join(input_folder, file)
            
            # Read the file to find where data starts
            with open(input_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            data_start_index = None
            animal_id = None
            date_time = None
            
            for i, line in enumerate(lines):
                if "Evnt_Time" in line:
                    data_start_index = i
                    break
                elif "Animal ID" in line:
                    animal_id = line.strip().split(",")[1].strip()
                elif "Date/Time" in line:
                    date_time = line.strip().split(",")[1].strip()
            
            if data_start_index is None:
                print(f"Skipping file {file}: 'Evnt_Time' column not found.")
                continue
            
            # Read the actual data skipping metadata
            df = pd.read_csv(input_path, skiprows=data_start_index, encoding='utf-8')
            binary_df = apply_formulas(df)
            
            # Ensure a safe filename for the output
            if animal_id and date_time:
                safe_date_time = re.sub(r'[: /]', '_', date_time)
                output_filename = f"{animal_id}_{safe_date_time}.csv"
            else:
                output_filename = f"Binary_{file}"
            
            output_path = os.path.join(output_folder, output_filename)
            binary_df.to_csv(output_path, index=False)
            print(f"Binary file saved: {output_path}")

# Example usage
generate_binary_file(
    input_folder=r"/Users/meiramaria/Documents/Data/Dopamine Sensor/Autoshaping/Cohort 1 (M1 to M14)/Coh 1 - Habituation/Habituation 2 - Day 1", 
    output_folder=r"/Users/meiramaria/Documents/Data/Dopamine Sensor/Autoshaping/Cohort 1 (M1 to M14)/Coh 1 - Habituation/Habituation 2 - Day 1"
)