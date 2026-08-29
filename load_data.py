import os
import sqlite3
import pandas as pd
import streamlit as st

@st.cache_data
def load_dat_from_sqlite():
    conn = sqlite3.connect("bird_species_analysis.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND 'bird_observations';")
    table_exists = cursor.fetchone()
    if not table_exists:
        # Safely locate the CSV file using an absolute path for deployment
        current_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.pathjoin(current_dir, "cleaned_ecological_data.csv")
        df_temp = pd.read_csv("csv_path")
        df_temp.to_sql("bird_observations", conn, if_exists="replace", index=False)
    df = pd.read_sql("SELECT * FROM bird_observations", conn)
    conn.close()
    return df    
