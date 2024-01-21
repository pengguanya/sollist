import pandas as pd
import numpy as np

def process_amount_column(data):
    split_amount = data['Amount'].str.split('-', n=1, expand=True)
    data[['Amount_low','Amount_high']] = split_amount.apply(pd.to_numeric, errors='coerce')
    mask = data['Amount_high'].isna()
    data.loc[mask, ['Amount_high','Amount_low']] = data.loc[mask, 'Amount_low']
    return data

def add_dirty_amount_column(data):
    data['Dirty amount in SOLL'] = data['Amount'].astype(str).str.contains('[^\d\s-]', na=False, regex=True)
    data['Dirty amount in SOLL'] = data['Dirty amount in SOLL'].map({True: 'Yes', False: 'No'})
    return data

def handle_nan_inf_values(data, column):
    data[column] = pd.to_numeric(data[column], errors='coerce')

    if data[column].isna().any() or (data[column] == float('Inf')).any():
        print(f"Problematic values detected in column: {column}")
        data.loc[data[column].replace([np.inf, -np.inf], np.nan).isna(), column] = 0

    return data
