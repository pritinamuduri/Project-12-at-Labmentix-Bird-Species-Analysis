import sqlite3
import pandas as pd
# Loads processed dataframe
df = pd.read_csv("cleaned_ecological_data.csv")
# Connect to your SQLite database File
conn = sqlite3.connect("bird_species_analysis.db")
# write the dataframe to the required table name
df.to_sql("bird_observations", conn, if_exists="replace", index=False)
conn.close()
