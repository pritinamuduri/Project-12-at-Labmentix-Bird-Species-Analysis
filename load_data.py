from pathlib import Path
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
        # Use pathlib to safely locate the CSV file
        current_dir = Path(__file__).parent
        csv_path = current_dir / "cleaned_ecological_data.csv"
        df_temp = pd.read_csv(csv_path, engine='python', on_bad_lines='skip')
        df_temp.to_sql("bird_observations", conn, if_exists="replace", index=False)
    df = pd.read_sql("SELECT * FROM bird_observations", conn)
    conn.close()
    return df    
