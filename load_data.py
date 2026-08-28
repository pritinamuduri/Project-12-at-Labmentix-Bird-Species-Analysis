<<<<<<< HEAD
import sqlite3
import pandas as pd
# 1. Read your Excel files
df_forest = pd.read_excel('Bird_Monitoring_Data_FOREST.XLSX')
df_grassland = pd.read_excel('Bird_Monitoring_Data_GRASSLAND.XLSX')
# 2. Connect to your SQLite database (this creates it if it dosent exists)
conn = sqlite3.connect('bird_species_analysis.db')
# 3. Write the dataframe into database tables
df_forest.to_sql('bird_observations', conn, if_exists='append', index=False)
df_grassland.to_sql('bird_observations', conn, if_exists='append', index=False)
# Close the connection
conn.close()
print("Data successfully loaded into the database!")

=======
import sqlite3
import pandas as pd
# 1. Read your Excel files
df_forest = pd.read_excel('Bird_Monitoring_Data_FOREST.XLSX')
df_grassland = pd.read_excel('Bird_Monitoring_Data_GRASSLAND.XLSX')
# 2. Connect to your SQLite database (this creates it if it dosent exists)
conn = sqlite3.connect('bird_species_analysis.db')
# 3. Write the dataframe into database tables
df_forest.to_sql('bird_observations', conn, if_exists='append', index=False)
df_grassland.to_sql('bird_observations', conn, if_exists='append', index=False)
# Close the connection
conn.close()
print("Data successfully loaded into the database!")

>>>>>>> 7dd07cb (Fix video path for cloud deployment)
                    