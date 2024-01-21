import pandas as pd

def load_data(filepath, sheet_name):
    try:
        data = pd.read_excel(filepath, sheet_name)
        return data
    except FileNotFoundError:
        print(f"File {filepath} not found")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def rename_columns(data, columns_map):
    return data.rename(columns = columns_map)

def select_columns(data, cols):
    available_cols = set(data.columns) & set(cols)
    if not available_cols:
        raise ValueError("None of the requested columns found in the DataFrame.")
    return data[list(available_cols)]
