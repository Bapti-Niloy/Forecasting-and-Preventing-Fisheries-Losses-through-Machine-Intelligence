# app.py

import streamlit as st
import pandas as pd
import geopandas as gpd
from pathlib import Path

# ─── Your existing viz functions ──────────────────────────────────────────────
from outputs import (
    plot_q3_source_bar,
    plot_q3_source_grouped_bar,
    plot_q4_monthly_catch_bar,
    plot_q4_monthly_catch_line,
    plot_q4_monthly_catch_area,
    plot_q4_top_species_bar,
    plot_q4_top_species_box,
    plot_q4_top_species_stacked_bar,
    plot_q4_top_species_line,
    plot_q5_annual_catch_by_source_bar,
    plot_q5_monthly_catch_by_source_line,
    plot_q6_monthly_waste_bar,
    plot_q6_monthly_waste_line,
    plot_q6_monthly_waste_area,
    plot_q6_top_waste_species_bar,
    plot_q6_top_waste_species_box,
    plot_q7_loss_by_reason_bar,
    plot_q12_distribution_sankey,
)
from geospatial_outputs import plot_q3_choropleth, plot_q4_choropleth

# ─── Paths ─────────────────────────────────────────────────────────────────────
BASE_DIR     = Path(__file__).parent
DATASETS     = BASE_DIR / "DATASETS"
CLEANED      = DATASETS / "Cleaned_Data"
GEO_CLEANED  = CLEANED  / "GEO_DATA"
SHAPE_FOLDER = DATASETS / "shape_files"
SHAPEFILE    = SHAPE_FOLDER / "shape.shp"   # adjust if yours is named differently

# ─── CACHING HELPERS ────────────────────────────────────────────────────────────
@st.cache_data
def load_csv(fname: str) -> pd.DataFrame:
    return pd.read_csv(CLEANED / fname)

@st.cache_data
def load_geo_csv(fname: str) -> pd.DataFrame:
    return pd.read_csv(GEO_CLEANED / fname)

@st.cache_data
def load_shapefile() -> gpd.GeoDataFrame:
    if not SHAPEFILE.exists():
        st.error(f"Could not find shapefile at {SHAPEFILE}")
        return gpd.GeoDataFrame()
    gdf = gpd.read_file(SHAPEFILE)
    # Rename ADM2_EN → q1_d_zila so our choropleth code lines up
    if "ADM2_EN" in gdf.columns:
        gdf = gdf.rename(columns={"ADM2_EN": "q1_d_zila"})
    return gdf

# ─── STREAMLIT LAYOUT ──────────────────────────────────────────────────────────
st.set_page_config(page_title="Bangladesh Fisheries Dashboard", layout="wide")
st.title("🇧🇩 Bangladesh Fisheries Dashboard")

tab1, tab2 = st.tabs(["Tabular Data", "Geospatial Data"])

with tab1:
    st.header("Q3: Overview of Fishing Techniques")
    df3 = load_csv("Q3_SOURCE_OF_FISHING.csv")
    st.plotly_chart(plot_q3_source_bar(df3), use_container_width=True)
    st.plotly_chart(plot_q3_source_grouped_bar(df3), use_container_width=True)

    st.header("Q4: Total Monthly Catch (MT)")
    df4 = load_csv("Q4_MONTHLY_CATCH.csv")
    st.plotly_chart(plot_q4_monthly_catch_bar(df4), use_container_width=True)
    st.plotly_chart(plot_q4_monthly_catch_line(df4), use_container_width=True)
    st.plotly_chart(plot_q4_monthly_catch_area(df4), use_container_width=True)

    st.header("Q4: Yearly Totals for Top 10 Species")
    df4top = load_csv("Q4_MONTHLY_FISH_CATCH.csv")
    st.plotly_chart(plot_q4_top_species_bar(df4top), use_container_width=True)
    st.plotly_chart(plot_q4_top_species_box(df4top), use_container_width=True)
    st.plotly_chart(plot_q4_top_species_stacked_bar(df4top), use_container_width=True)
    st.plotly_chart(plot_q4_top_species_line(df4top), use_container_width=True)

    st.header("Q5: Annual Catch by Source")
    df5 = load_csv("Q5_MONTHLY_TOTALS_BY_SOURCE.csv")
    st.plotly_chart(plot_q5_annual_catch_by_source_bar(df5), use_container_width=True)
    st.plotly_chart(plot_q5_monthly_catch_by_source_line(df5), use_container_width=True)

    st.header("Q6: Monthly Wastage (MT)")
    df6 = load_csv("Q6_MONTHLY_WASTE.csv")
    st.plotly_chart(plot_q6_monthly_waste_bar(df6), use_container_width=True)
    st.plotly_chart(plot_q6_monthly_waste_line(df6), use_container_width=True)
    st.plotly_chart(plot_q6_monthly_waste_area(df6), use_container_width=True)

    st.header("Q6: Top-Species Wastage")
    df6top = load_csv("Q6_MONTHLY_FISH_WASTE.csv")
    st.plotly_chart(plot_q6_top_waste_species_bar(df6top), use_container_width=True)
    st.plotly_chart(plot_q6_top_waste_species_box(df6top), use_container_width=True)

    st.header("Q7: Wastage by Reason")
    df7 = load_csv("Q7_ANNUAL_LOSS_BY_REASON.csv")
    st.plotly_chart(plot_q7_loss_by_reason_bar(df7), use_container_width=True)

    st.header("Q12: Distribution Channels")
    df12 = load_csv("Q12_WHERE_DOES_THE_FISH_END_UP.csv")
    st.plotly_chart(plot_q12_distribution_sankey(df12), use_container_width=True)

with tab2:
    st.header("Geospatial Analysis")
    gdf = load_shapefile()
    if not gdf.empty:
        st.subheader("Q3: Fishing Sources by District")
        geo3 = load_geo_csv("Q3_SOURCE_OF_FISHING.csv")
        st.plotly_chart(plot_q3_choropleth(gdf, geo3), use_container_width=True)

        st.subheader("Q4: Per-District Monthly Catch")
        geo4 = load_geo_csv("Q4_MONTHLY_CATCH.csv")
        # ─── Rename 'District' → 'q1_d_zila' so it matches the GeoDataFrame ───
        if "District" in geo4.columns:
            geo4 = geo4.rename(columns={"District": "q1_d_zila"})
        st.plotly_chart(plot_q4_choropleth(gdf, geo4), use_container_width=True)

