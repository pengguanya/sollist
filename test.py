import pandas as pd
import numpy as np
import yaml
from utils.load_data import load_data, rename_columns, select_columns
from utils.column_processing import process_amount_column, add_dirty_amount_column, handle_nan_inf_values
from utils.computing import compare_soll_ist

with open('config.yml') as file:
    config = yaml.full_load(file)

ist_col_map = config.get('ist_col_map')
soll_col_map = config.get('soll_col_map')
ist_cols = config.get('ist_cols')
soll_cols = config.get('soll_cols')

def main():
    dt = 'data/soll_ist_differenz_lokal.xlsx'

    # Load excel sheets
    ist = load_data(dt, 'aus SAP')
    soll = load_data(dt, 'LHV-Liste (nur J und D)')

    if ist is None or soll is None:
        return

    df = compare_soll_ist(ist, soll, ist_col_map, soll_col_map, ist_cols, soll_cols)
    print(df)


if __name__ == "__main__":
    main()
