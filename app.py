# existing import statements
import yaml
import streamlit as st
import base64
from io import BytesIO
import pandas as pd
from utils.load_data import load_data
from utils.computing import compare_soll_ist

def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1', index=False)
    writer.close()
    processed_data = output.getvalue()
    return processed_data

def get_table_download_link(df, filename='data.xlsx', text='Download Excel file'):
    val = to_excel(df)
    b64 = base64.b64encode(val)  # val looks like b'...'
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}">{text}</a>'

def main():
    st.title('Compare SOLL and IST')

    st.markdown("""
    Please upload an Excel file with two worksheets. 
    
    One worksheet should be named **'SOLL'**, and the other should be named **'IST'**. 
    
    Both of these worksheets need to have the mandatory columns 'Name', 'Material', and 'Amount'.
    """)

    uploaded_file = st.file_uploader("Upload the excel file", type=['xlsx'])

    with open('config.yml') as file:
        config = yaml.safe_load(file)

    ist_sheet = config.get('ist_sheet')
    soll_sheet = config.get('soll_sheet')
    ist_col_map = config.get('ist_col_map')
    soll_col_map = config.get('soll_col_map')
    ist_cols = config.get('ist_cols')
    soll_cols = config.get('soll_cols')

    if uploaded_file:
        ist = load_data(uploaded_file, ist_sheet)
        soll = load_data(uploaded_file, soll_sheet)

        output_df = compare_soll_ist(ist, soll, ist_col_map, soll_col_map, ist_cols, soll_cols)
        download_link = get_table_download_link(output_df, 'processed_data.xlsx', 'Download data as Excel')
        st.markdown(download_link, unsafe_allow_html=True)

if __name__ == '__main__':
    main()
