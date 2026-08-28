import os
import pandas as pd
import sqlite3
import gdown

def download_file(url_or_id, output_filename):
    if "http" in url_or_id:
        if '/file/d/' in url_or_id:
            file_id = url_or_id.split('/file/d')[1].split('/')[0]
        else:
            file_id = url_or_id
            url = f'https://drive.google.com/uc?id={file_id}'
    else:
        url = f'https://drive.google.com/uc?id={url_or_id}'
        print(f"Downloading {output_filename} directly from Google Drive...")
        gdown.download(url, output_filename, quiet=False, fuzzy=True)
def download_and_clean_data():
    forest_url = 'https://docs.google.com/spreadsheets/d/1vwL5JSM5_ox6EBzGbJIVq-BDgm_MUttH/edit?usp=drive_link&ouid=101586808747623920245&rtpof=true&sd=true'
    grassland_url = 'https://docs.google.com/spreadsheets/d/1buwl6kvAfoBlUgNJ5pDvD4ToWGXpbWr6/edit?usp=drive_link&ouid=101586808747623920245&rtpof=true&sd=true'
    forest_file = 'Bird_Monitoring_Data_FOREST.XLSX'
    grassland_file = 'Bird_Monitoring_Data_GRASSLAND.XLSX'
    # Download files straight from Google Drive into Project Folder
    download_file(forest_url, forest_file)
    download_file(grassland_url, grassland_file)
    all_dfs = []
    files_to_process = [
        (forest_file, 'Forest'),
        (grassland_file, 'Grassland')
    ]
    # 2. Loop through fikes and all administrative unit sheets (ANTI, CATO, CHOH, etc.)
    for file_name, habitat_label in files_to_process:
        if os.path.exists(file_name):
            print(f"Reading sheets from {file_name}...")
            excel_file = pd.ExcelFile(file_name)
            for sheet in excel_file.sheet_names:
                try:
                    df_sheet = pd.read_excel(excel_file, sheet_name=sheet)
                    if not df_sheet.empty:
                        df_sheet['sheet_name'] = sheet
                        df_sheet['habitat_type'] = habitat_label
                        all_dfs.append(df_sheet)
                except Exception as e:
                    print(f"Could not read sheet {sheet}: {e}")
    if not all_dfs:
        print("Error: No data loaded. Please verify your Google Drive links.")
        return
    # 3. Consolidate into  a single dataframe (ZERO rows dropped)
    df_combined = pd.concat(all_dfs, ignore_index=True)                        

    # 4. Data cleaning and Preprocessing
    df_combined.columns = df_combined.columns.str.strip().str.lower()

    text_cols = df_combined.select_dtypes(include=['object']).columns
    df_combined[text_cols] = df_combined[text_cols].fillna('Unknown')
    num_cols = df_combined.select_dtypes(include=['number']).columns
    df_combined[num_cols] = df_combined[num_cols].fillna(0)
# If there is a date column, extract temporal data for EDA without dropping any rows
    if 'date' in df_combined.columns:
     df_combined['date'] = pd.to_datetime(df_combined['date'],'coerce')
     df_combined['year'] = df_combined['date'].dt.year
     df_combined['month'] = df_combined['date'].dt.month
     def get_season(month):
        if pd.isna(month) or month == 0: return 'Unknown'
        m = int(month)
        if m in [12, 1, 2]: return 'Winter'
        elif m in [3, 4, 5]: return 'Spring'
        elif m in [6, 7, 8]: return 'Summer'
        elif m in [9, 10, 11]: return 'Fall'
        return 'Unknown'
    df_combined['season'] = df_combined['month'].apply(get_season)
    # 4. Save the cleaned/consolidated dataset (all rows preserved) 
    output_csv = 'cleaned_ecological_data.csv'
    df_combined.to_csv(output_csv, index=False)
    print(f"Data successfully downloaded from Drive, cleaned and saved to {output_csv}!") 
    # 6. Store data in an SQLite database for visualization requirements
    db_name = 'bird_species_analysis.db'
    conn = sqlite3.connect(db_name)
    df_combined.to_sql('bird_observations', conn, if_exists='replace', index=False)
    conn.close()
    print(f"Data successfully loaded into SQLite database: {db_name} (Table: bird_observations).")
# Run the pipeline
if __name__ == "__main__":
    df = download_and_clean_data()


