import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
st.set_page_config(page_title="Interactive Bird Visualizations", page_icon="📊", layout="wide")
st.title("📊 Highly Interactive Ecological Data Dashboard")
st.markdown("Hover over any chart element to view rich, Power BI style tooltips with detailed metrics.")
# Function to load data from SQLite database
@st.cache_data
def load_dat_from_sqlite():
    conn = sqlite3.connect('bird_species_analysis.db')
    df = pd.read_sql("SELECT * FROM bird_observations", conn)
    conn.close()
    return df
df = load_dat_from_sqlite()
if df.empty:
    st.warning("No data found in the database. Please run your data cleaning script first!")
else:
    # --- SIDEBAR INTERACTIVE FILTERS ---
    st.sidebar.header("Interactive Filters")
    habitats_available = list(df['habitat_type'].unique()) if 'habitat_type' in df.columns else []
    selected_habitats = st.sidebar.multiselect("Select Habitats", habitats_available, default=habitats_available)    
    seasons_available = list(df['season'].unique()) if 'season' in df.columns else[]
    selected_seasons = st.sidebar.multiselect("Select Seasons", seasons_available, default=seasons_available)
    sheets_available = list(df['sheet_name'].unique()) if 'sheet_name' in df.columns else []
    selected_sheets = st.sidebar.multiselect("Select Administrative Units (Sheets)", sheets_available, default=sheets_available)
    # Safe Year Filter Logic
    selected_years = None
    if 'year' in df.columns:
         valid_years= df[df['year'] > 0]['year'].unique()
         if len(valid_years) > 1:
              min_yr = int(valid_years.min())
              max_yr = int(valid_years.max())
              selected_years = st.sidebar.slider("Select Year Range", min_value=min_yr, max_value=max_yr, value=(min_yr, max_yr))
         elif len(valid_years) == 1:
              st.sidebar.info(f"Note: Dataset contains only year {int(valid_years[0])}") 
             # Create an "About Project" section or tab
              with st.expander("📖About This Project & Administrative Units Guide"):
                   st.markdown("### 🎯Project Objectives & Business Use Cases")
                   st.markdown(
                        """
                        This dashboard analyzes bird species distribution across **Forest** and **Grassland** ecosystems to support:
                        * **Wildlife Conservation:** Protecting critical habitats and tracking vulnerable species
                        * **Land Management:** Optimizing habitat restoration and understanding avian preferences
                        * **Biodiversity Monitoring:** Assessing long-term ecosystem stability
                        
                    """
                        
                   )
                   st.markdown("---")
                   st.markdown("### National Park Service Administrative Units ")
                   st.markdown(
     
            """
            These codes represent specific parks and protected areas managed within the National Capital Region of thr U.S. National Park Service(NPS).
            * **ANTI:** Antietam National Battlefield
            * **CATO:** Catocin Mountain Park
            * **CHOH:** C&O Canal National Historical Park
            * **GWMP:** George Washington Memorial Parkway
            * **HAFE:** Harpers Ferry National Historical
            * **MANA:** Manassas National Battlefield Park
            * **MONO:** Monocacy National BAttlefield
            * **NACE:** National Capital East PArks
            * **PRWI:** Prince William Forest Park
            * **ROCR:** Rock Creek Park
            * **WOTR:** Wolf Trap NAtional Park.
            
            

"""
       )
    # --- APPLY FILTERS ---
    filtered_df = df.copy()
    if selected_habitats:
        filtered_df = filtered_df[filtered_df['habitat_type'].isin(selected_habitats)]
        # Check and apply season filter safely
    season_col = 'season' if 'season' in filtered_df.columns else ('Season' if 'Season' in filtered_df.columns else None)
    if selected_seasons:
        filtered_df = filtered_df[filtered_df['season'].isin(selected_seasons)]  
    if selected_sheets:
        filtered_df = filtered_df[filtered_df['sheet_name'].isin(selected_sheets)]
    if selected_years and 'year' in df.columns:
        filtered_df = filtered_df[(filtered_df['year'] >= selected_years[0]) & (filtered_df['year'] <= selected_years[1])]
    # --- TOP METRICS ROW ---
    st.markdown("### 📈 Key Performance Indicators")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Filtered Records", f"{len(filtered_df):,}")
    m2.metric("Active Habitats", filtered_df['habitat_type'].nunique() if 'habitat_type' in filtered_df.columns else 0)
    m3.metric("Admin Units Included", filtered_df['sheet_name'].nunique() if 'sheet_name' in  filtered_df.columns else 0)
    m4.metric("Total Dataset Size", f"{len(df):,}")
    st.markdown("---")
    # --- TABS WITH POWER BI STYLE TOOLTIP CHARTS ---
    tab1, tab2, tab3 = st.tabs(["📊Overview Charts", "🗓️Temporal & Trends", "🔍 Interactive Data Explorer"])
    with tab1:
        st.subheader("Habitat & Seasonal Breakdown (Hover for Details)")
        col_a, col_b = st.columns(2)
        with col_a:
            if not filtered_df.empty and 'habitat_type' in filtered_df.columns:
                # Group data to include breakdown details in the tooltip
                hab_counts = filtered_df['habitat_type'].value_counts().reset_index()
                hab_counts.columns = ['Habitat', 'Observation Count']
                # Bar chart with custom hover tooltip integration
                fig_hab = px.bar(
                    hab_counts,
                    x='Habitat',
                    y='Observation Count',
                    color='Habitat',
                    title="Observations by Habitat",
                    template="plotly_white",
                    hover_data={'Habitat': True, 'Observation Count': ':,'} # Power BI Style comma for formatting
                )
                fig_hab.update_traces(hovertemplate="<b>Habitat:</b> %{x}<br><b>Total Observations:</b> %{y:,}<extra></extra>")
                st.plotly_chart(fig_hab, use_container_width=True)
                st.markdown("---")
                with st.expander("📌 View Overview Observations & Business Recommendations"):
                 col1, col2 = st.columns(2)
                with col1:
                     st.markdown("### Observations")
                     st.markdown(
                          """
                          * **Habitat Disparity:** Forest ecosystems account for the majority of bird observations(67.2%) compared to grasslands (32.8%)
                          * **Activity Concentration:** Higher observation frequencies are localized in specific administrative units and vegetative plots
                          * **Temporal Consistency:** Sightings remain steady across standard observation windows, indicating stable baseline tracking
"""
                     )
                with col2:
                     st.markdown("### Recommendations")     
                     st.markdown(
                          """  
                          * **Wildlife Conservation:** Direct targeted protection efforts towards high-density forest plots to preserve critical available habitats
                          * **Land Management:** Optimize grassland restoration strategies to encourage higher species diversity and balanced population
                          * **Biodiversity Monitoring:** Increase monitoring frequency in underrepresented grassland sectors to mkitigate observation bias           

"""
                     )
        with col_b:
                if not filtered_df.empty and 'season' in filtered_df.columns:
                    seas_counts = filtered_df['season'].value_counts().reset_index()
                    seas_counts.columns = ['Season', 'Observation Count']
                    # Pie Chart with custom tooltip
                    fig_seas = px.pie(
                        seas_counts,
                        names='Season',
                        values='Observation Count',
                        title="Seasonal Distribution",
                        hole=0.4,
                        template="plotly_white"
                    )
                    fig_seas.update_traces(hovertemplate="<b>Season:</b> %{label}<br><b>Count:</b> %{Value:,}<br><b>Percentage:</b> %{percent}<extra></extra>")
                    st.plotly_chart(fig_seas, use_container_width=True)
                    col1, col2 = st.columns(2)
                    with st.expander("View Pie Chart Observations & Ecological Recommendations"):
                 
                         with col1:
                              st.markdown("### Key Observations")
                              st.markdown(
                                   """
                                   * ** Ecosystem Share:** Forest habitats comprise the dominant portion  of recorded observations (67.2%) while grassland represents a smaller share (32.8%)
                                   * **Habitat Skew:** The disproportionate share highlights a higher concentration of recording activity or native bird density within forested park units.
                                  """
                              )
                         with col2:
                            st.markdown("### Actionable Recommendations") 
                            st.markdown("- **Ecosystem Balancing:** Allocate future ecological survey evenly.")
                            

                              
                                        
    with tab2:
        st.subheader("Temporal Trends Over Years (Interactive Tooltips)")
        # Check what columns actually exist to prevent silent skipping
        df_cols = [c.lower() for c in filtered_df.columns]
        if not filtered_df.empty and ('year' in df_cols or'Date' in filtered_df.columns):
             # Automatically find the correct year column name regardless of casing
             year_col = 'year' if 'year' in filtered_df.columns else ('Year' if 'Year' in filtered_df.columns else 'Date')
             hab_col = 'habitat_type' if 'habitat_type' in filtered_df.columns else 'Location_Type'
             # Group data safely for the line chart
             trend_data = filtered_df.groupby([year_col, hab_col]).size().reset_index(name='Observation Count')
             fig_trend = px.line(
                  treand_data,
                  x=year_col,
                  y='Observation Count',
                  color=hab_col,
                  markers=True,
                  title="Bird Observation Trend Over Time",
                  template="plotly_white",
                  color_discrete_map={'Forest': '#2d6a4f', 'Grassland': '#d4a373'}
             )
             fig_trend.update_layout(
                  font=dict(family="sans-serif", size=12, color="#333333"),
                  plot_bgcolor="rgba(0,0,0,0)",
                  paper_bgcolor="rgba(0,0,0,0)",
                  margin=dict(t=30, b=30, l=40, r=40)


             )
             st.plotly_chart(fig_trend, use_container_width=True)
             # Interactive Expander for Insights
             with st.expander("📈 View Temporal Insights & Actionable Recommendations"):
                  col1, col2 = st.columns(2)
                  with col1:
                       st.markdown("### Key Observations")
                       st.markdown(
                            """
                            * **Year-over-Year Stability:** Bird observation frequencies remain relatively consistent across the recorded years.
                            * **Seasonal Patterns:** Sightings fluctuate based on observation schedules and weather conditions.

"""
                       )
                       
        else:
             st.info("No temporal data available for the current filter selection. Please adjust your filters above.")
    with tab3:
                    st.subheader("Search, Spatial & Data Export")
                    if filtered_df is None or filtered_df.empty:
                         st.warning("No data available for Tab 3.")
                    else:
                         # 1. Search and Filtering Features     
                         search_query = st.text_input(" Search Records", key="tab3_serach")
                         display_df = filtered_df.copy()
                         if search_query:
                            mask = display_df.astype(str).apply(lambda x: x.str.contains(search_query, case=False)).any(axis=1)
                            display_df = display_df[mask] 
                    st.success(f"Showing {len(display_df):,} matching rows.")        
                    st.dataframe(display_df, use_container_width=True)  
                    # 2. CSV Download Button (from previous code) 
                    csv_data = display_df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                         label="Download Filtered Data as CSV",
                         data=csv_data,
                         file_name="filtered_bird_data.csv",
                         mime="text/csv"
                    )
                    st.markdown("---")
                    # 3. Quick Spatial/Location Breakdown Chart
                    loc_col = 'Location_Type' if 'Location_Type' in display_df.columns else('location_type' if 'location_type' in display_df.columns else None)
                    if loc_col:
                     st.write("### Observations by Location Type")
                     loc_df = display_df.groupby(loc_col).size().reset_index(name='Count')
                    import plotly.express as px
                    fig_loc = px.bar(
                         loc_df,
                         x=loc_col,
                         y='Count',
                         color=loc_col,
                         template="plotly_white"
                    )
                    st.plotly_chart(fig_loc, use_container_width=True)
                    with st.expander ("View Location Type Insights & Recommendations"):
                         col1, col2 = st.columns(2)
                         with col1:
                              st.markdown("### Key Observations")
                              st.markdown(
                                        """
                                        * ** Habitat Distribution:** Forest observation counts outnumber Grassland counts, indicating a heavier density of recorded surveys in wooded environments
                                        * **Spatial Concentration:** Specific park sdministrative units drive a large portion of the forest-based activity totals

"""
                                   )
                         with col2:
                                      st.markdown("### Actionable Recommendations")
                                      st.markdown(
                                           """
                                           * **Habitat Protection:** Prioritize land management and conservation funding for high volume forest plots
                                           * **Resource Re-allocation:** Increase monitoring efforts in grassland sectors to balance data collection and assess open-habitat bird health
                                           """
                                      )
 

                          
                     
                


                    









                


