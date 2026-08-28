import pandas as pd
# Load your cleaned dataset
df = pd.read_csv('cleaned_ecological_data.csv')
print("--- BIRD MONITORING DATA SUMMARY ---")
print(f"Total Rows/Observations: {len(df)}")
print(f"Total Columns: {len(df.columns)}")
if 'habitat_type' in df.columns:
    print(f"Habitats: {df['habitat_type'].unique()}")
print("\ncolumns available:")    
for col in df.columns:
    print(f" - {col}")
