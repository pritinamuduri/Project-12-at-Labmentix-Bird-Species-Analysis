import sqlite3
import pandas as pd
def load_dat_from_sqlite():
    conn = sqlite3.connect("bird_species_analysis.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND 'bird_observations';")
    if not cursor.fetchone():
        df_temp = pd.read_csv("cleaned_ecological_data.csv")
        df_temp.to_sql("bird_observations", conn, if_exists="replace", index=False)
    df = pd.read_sql("SELECT * FROM bird_observations", conn)
    conn.close()
    return df    
