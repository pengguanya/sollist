import pandas as pd
from utils.load_data import rename_columns, select_columns
from utils.column_processing import process_amount_column, add_dirty_amount_column, handle_nan_inf_values

def compare_soll_ist(ist: pd.DataFrame, soll: pd.DataFrame, ist_col_map: dict, soll_col_map: dict, ist_cols: list, soll_cols: list):

    if ist is None or soll is None:
        return

    # Rename the columns
    ist = rename_columns(ist, ist_col_map)
    soll = rename_columns(soll, soll_col_map)

    # Select necessary columns
    ist = select_columns(ist, ist_cols)
    soll = select_columns(soll, soll_cols)
    
    # Process 'Amount' column
    soll = process_amount_column(soll)
    
    # Add 'Dirty amount in SOLL' column
    soll = add_dirty_amount_column(soll)
    
    # Group by 'Name', 'Material', 'Kunden-Nr', and 'Unit' and sum the 'Amount'
    ist = ist.groupby(['Name', 'Material'], as_index=False)['Amount'].sum()
    
    # Merge the two DataFrames on 'Name' and 'Material' with an outer join
    merged_df = pd.merge(soll, ist, on=['Name', 'Material'], how='outer', suffixes=('_soll', '_ist'))

    # Check and handle any NaN or Inf values
    for column in ['Amount_low', 'Amount_high', 'Amount_ist']:
        merged_df = handle_nan_inf_values(merged_df, column)

    # Calculate the differences
    merged_df['difference_low'] = merged_df['Amount_low'] - merged_df['Amount_ist']
    merged_df['difference_high'] = merged_df['Amount_high'] - merged_df['Amount_ist']

    return merged_df
