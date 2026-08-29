


import streamlit as st
import sqlite3
import pandas as pd
st.set_page_config(
    page_title="Bird Species Analysis Home",
    page_icon="🦜",
    layout="wide"
)
# --- HERO SECTION ---
st.title(" Ecological Bird Monitoring & Species Analysis")
st.markdown("### *Bridging Data Engineering and Environmental Science*")
st.write("The project aims to analyze the distribution and diversity of bird species in two distinct ecosystems:forests and grasslands. By examining bird species  observations across these habitats, the goal is to understand how environmental factors, such as vegetation type, climate, and terrain, influence bird populations and their behavior.")

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
