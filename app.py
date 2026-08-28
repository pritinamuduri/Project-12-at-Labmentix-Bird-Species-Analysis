


import sqlite3
import pandas as pd
df = pd.read_csv("cleaned_ecological_data.csv", sep=";")
conn = sqlite3.connect("bird_observations", conn, if_exists="replace", index=False)

conn.close()
print("Data successfully loaded into the database!")

                    
st.set_page_config(
    page_title="Bird Species Analysis Home",
    page_icon="🦜",
    layout="wide"
)
# --- HERO SECTION ---
st.title(" Ecological Bird Monitoring & Species Analysis")
st.markdown("### *Bridging Data Engineering and Environmental Science*")
st.write("The project aims to analyze the distribution and diversity of bird species in two distinct ecosystems:forests and grasslands. By examining bird species  observations across these habitats, the goal is to understand how environmental factors, such as vegetation type, climate, and terrain, influence bird populations and their behavior.")
st.markdown("---")
# --- LIVE DATABASE STATS INTEGRATION ---
# Pulling quick metrics directly so the home page is dynamic and live
@st.cache_data
def get_quick_stats():
    try:
        conn = sqlite3.connect('bird_species_analysis.db')
        df = pd.read_sql("SELECT habitat_type, season, year FROM bird_observations", conn)
        conn.close()
        return df
    except Exception:
        return pd.DataFrame()

# Safely compute metrics only if columns exist and df is not empty
df_home = get_quick_stats()
total_obs = len(df_home) if not df_home.empty else 0
if not df_home.empty and 'habitat_type' in df_home.columns:
    habitats_count = df_home['habitat_type'].nunique()
else:
    habitats_count = 0
if not df_home.empty and 'season' in df_home.columns:
    seasons_count = df_home['season'].nunique() 
else:
    seasons_count = 0    
    st.write("Database connection test - Rows loaded:", len(df_home))
if  df_home.empty:
        st.warning("No data found in the database. Please verify your table name or data load script.")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Observations", len(df_home))
        col2.metric("Habitats", habitats_count)
        col3.metric("Seasons", seasons_count)
        col4.metric(" Database", "Connected")
        st.markdown("---")
# --- INTERESTING PROJECT HIGHLIGHTS ----
col_left, col_right = st.columns(2)
with col_left:
            st.subheader(" 🪜 Data Cleaning Pipeline")
            st.markdown("""
            * **Automated Data Pipeline:** Pulls messy multi-unit Excel sheets straight from Google Drive.
            * **Zero-Loss Data Cleaning:** Standardizes columns, handles missing values safely, and structures dates without dropping valuable rows.
            * **Relational Database Backend:** Persists clean ecological records into **SQLite database** for optomized query performance.
            * **Interactive Analytics:** Empowers researchers to slice data dynamically using multi-select, sliders, and Power BI stylr hover tooltips.
            """)
with col_right:
                st.subheader("🛠️ Tech Stack & Architecture")
                st.info("""
                * **Python & Pandas:** Core data manipulation and cleaning.
                * **Gdown:** Automated Google Drive integration.
                * **SQLite3:** High-performance local SQL database storage.
                * **Streamlit & Plotly:** Multi-page interactive UI and dynamic visualization engine.
                """)
# --- NAVIGATION CALLOUT ---
st.markdown("---")
st.success("👍 **Ready to explore the findings?** Head over to the **visualizations** page using the sidebar navigation on the left to start filtering bird observations, analyzing seasonal trends, and exploring datasets!")
                             
                            
