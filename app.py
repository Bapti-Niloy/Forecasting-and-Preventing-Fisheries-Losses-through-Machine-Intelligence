# app.py

import streamlit as st
import pandas as pd
import geopandas as gpd
from pathlib import Path

# ─── Paths ─────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent
DATASETS = BASE_DIR / "DATASETS"
CLEANED = DATASETS / "Cleaned_Data"
GEO_CLEANED = CLEANED / "GEO_DATA"
SHAPEFILE = DATASETS / "shape_files" / "shape.shp"

# ─── Import Chart Functions ─────────────────────────────────────
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

# ─── Cache Loaders ──────────────────────────────────────────────
@st.cache_data
def load_csv(fname: str) -> pd.DataFrame:
    return pd.read_csv(CLEANED / fname)

@st.cache_data
def load_geo_csv(fname: str) -> pd.DataFrame:
    return pd.read_csv(GEO_CLEANED / fname)

@st.cache_data
def load_shapefile() -> gpd.GeoDataFrame:
    gdf = gpd.read_file(SHAPEFILE)
    if "ADM2_EN" in gdf.columns:
        gdf.rename(columns={"ADM2_EN": "q1_d_zila"}, inplace=True)
    gdf["q1_d_zila"] = gdf["q1_d_zila"].astype(str)
    return gdf

# ─── Sidebar Page Switcher ──────────────────────────────────────
st.set_page_config(page_title="Bangladesh Fisheries Dashboard", layout="wide")
st.sidebar.title("📂 Navigation")
page = st.sidebar.radio("Go to", ["📊 Dashboard", "📄 Data & Reports"])

# ────────────────────────────────────────────────────────────────
# 🟢 PAGE 1: DASHBOARD
# ────────────────────────────────────────────────────────────────
if page == "📊 Dashboard":
# ─── Landing Page Intro ──────────────────────────────────────────────

    st.title("Forecasting-and Preventing Fisheries Losses through Machine Intelligence Dashboard")
    st.markdown("---")
    
    # 🔍 Project Overview
    st.markdown("""
    ### 🎣 Empowering Sustainable Inland Fisheries Through Data
    
    Inland fisheries play a critical role in global and national food security, offering employment to  over **200 million people worldwide** and delivering affordable, protein-rich nutrition to vulnerable populations.  
    In **Bangladesh**, diverse inland water bodies — rivers, floodplains, ponds, haors, baors and more — support over **260 fish species** and contribute around **3.5% to national GDP** (FAO, 2021).
    
    Yet, these systems face mounting pressure from **climate change**, **overfishing**, **transport inefficiencies**, and **data fragmentation**. Traditional data tools like Excel struggle with the scale and complexity of modern fisheries datasets.
    
    ---
    """)
    
    # 📊 About This Dashboard
    st.markdown("""
    ### 📊 Why This Dashboard?
    
    This interactive dashboard was developed as part of a research project to modernize the data infrastructure behind a national-scale study:  
    > **“Post-harvest Losses, Supply and Value Chain Analysis of Fisheries Sub-sector in Bangladesh”**  
    > Led by **Bangladesh Agricultural University (BAU)**, funded by **IDA & IFAD**, through **BARC**
    
    The project gathered data from **24,000+ stakeholders**, across **64 districts and 1,400+ markets** between 2018 and 2021 — producing rich but overwhelming datasets.
    
    This dashboard solves that problem, providing:
    - ✅ Clean, geospatially-enabled datasets
    - ✅ Interactive maps, charts, and tables
    - ✅ High-level analytics of **catch**, **waste**, **value chains**, and **distribution flows**
    - ✅ Downloadable data for transparency and future research
    """)
    
    # 🎯 Objectives
    st.markdown("### 🎯 Project Objectives")
    
    st.markdown("""
    1. **Design a Cloud-Ready Data Architecture**  
       Transform raw BAU survey files (CSV, shapefiles) into a scalable, secure data platform  
       → Automated ETL, geospatial integration, validation, and schema documentation
    
    2. **Visualize Post-Harvest Losses in Context**  
       Provide meaningful insights on spoilage across:
       - 📍 **Location** (District-level maps)
       - 📅 **Time** (Seasonal & festival trends)
       - 🐟 **Product** (Species-specific vulnerabilities)
    
    3. **Support Policy and Decision-Making**  
       Reveal “hotspots” of waste, identify critical intervention points, and support planning of cold chains, market access, and resource allocation.
    """)
    
    # 📌 Notebook Summary
    with st.expander("📘 Project Data & Notebooks Summary"):
        st.markdown("""
    - **Q3:** District-level counts of fishing techniques  
    - **Q4:** Monthly fish catch by volume & species  
    - **Q5–Q7:** Analysis of loss reasons, monthly spoilage, and wastage trends  
    - **Q12:** Sankey diagram showing post-harvest distribution paths  
    - Cleaned datasets prepared using Python (Pandas, GeoPandas), joined with shapefiles  
    """)
    
    # 📥 Call to Action
    st.markdown("---")
    st.markdown("### 🚀 Get Started Below")
    st.markdown("""
    - Use the **sidebar** to explore:
      - 📊 **Dashboard**: Visualize interactive charts and maps  
      - 📄 **Data & Reports**: Preview or download cleaned datasets  
    """)


    tab1, tab2 = st.tabs(["📊 Interactive Visuals", "🗺️ Geospatial Maps"])

    with tab1:
        section = st.selectbox("Choose a Data Category", (
            "Q3 – Fishing Techniques",
            "Q4 – Monthly Catch Trends",
            "Q4 – Top 10 Species",
            "Q5 – Annual Catch by Source",
            "Q6 – Monthly Wastage",
            "Q6 – Wastage by Species",
            "Q7 – Loss by Reason",
            "Q12 – Distribution Channels"
        ))

        if section == "Q3 – Fishing Techniques":
            df = load_csv("Q3_SOURCE_OF_FISHING.csv")
            st.plotly_chart(plot_q3_source_bar(df), use_container_width=True)
            st.plotly_chart(plot_q3_source_grouped_bar(df), use_container_width=True)

        elif section == "Q4 – Monthly Catch Trends":
            df = load_csv("Q4_MONTHLY_CATCH.csv")
            chart = st.radio("Select chart type", ["Bar", "Line", "Area"])
            st.plotly_chart({
                "Bar": plot_q4_monthly_catch_bar,
                "Line": plot_q4_monthly_catch_line,
                "Area": plot_q4_monthly_catch_area
            }[chart](df), use_container_width=True)

        elif section == "Q4 – Top 10 Species":
            df = load_csv("Q4_MONTHLY_FISH_CATCH.csv")
            chart = st.radio("Select chart type", ["Bar", "Box", "Stacked Bar", "Line"])
            st.plotly_chart({
                "Bar": plot_q4_top_species_bar,
                "Box": plot_q4_top_species_box,
                "Stacked Bar": plot_q4_top_species_stacked_bar,
                "Line": plot_q4_top_species_line
            }[chart](df), use_container_width=True)

        elif section == "Q5 – Annual Catch by Source":
            df = load_csv("Q5_MONTHLY_TOTALS_BY_SOURCE.csv")
            st.plotly_chart(plot_q5_annual_catch_by_source_bar(df), use_container_width=True)
            st.plotly_chart(plot_q5_monthly_catch_by_source_line(df), use_container_width=True)

        elif section == "Q6 – Monthly Wastage":
            df = load_csv("Q6_MONTHLY_WASTE.csv")
            chart = st.radio("Select chart type", ["Bar", "Line", "Area"])
            st.plotly_chart({
                "Bar": plot_q6_monthly_waste_bar,
                "Line": plot_q6_monthly_waste_line,
                "Area": plot_q6_monthly_waste_area
            }[chart](df), use_container_width=True)

        elif section == "Q6 – Wastage by Species":
            df = load_csv("Q6_MONTHLY_FISH_WASTE.csv")
            st.plotly_chart(plot_q6_top_waste_species_bar(df), use_container_width=True)
            st.plotly_chart(plot_q6_top_waste_species_box(df), use_container_width=True)

        elif section == "Q7 – Loss by Reason":
            df = load_csv("Q7_ANNUAL_LOSS_BY_REASON.csv")
            st.plotly_chart(plot_q7_loss_by_reason_bar(df), use_container_width=True)

        elif section == "Q12 – Distribution Channels":
            df = load_csv("Q12_WHERE_DOES_THE_FISH_END_UP.csv")
            st.plotly_chart(plot_q12_distribution_sankey(df), use_container_width=True)

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

# ────────────────────────────────────────────────────────────────
# 🟦 PAGE 2: DATA & REPORTS
# ────────────────────────────────────────────────────────────────
elif page == "📄 Data & Reports":
    st.title("📄 Cleaned Data & Reports")
    st.markdown("""
    This page presents the cleaned datasets used in this project  
    and summarizes what was produced from the notebooks.  
    You can preview or download any dataset below.
    """)

    with st.expander("🧪 Summary of Notebook Outputs", expanded=True):
        st.markdown("""
        - Q3: District-level counts of fishing techniques  
        - Q4: Monthly and species-wise fish catch  
        - Q5–Q7: Wastage, losses, and sources by month  
        - Q12: Fish distribution flows (Sankey diagram)  
        """)

    datasets = {
        "Q3 – Source of Fishing": CLEANED / "Q3_SOURCE_OF_FISHING.csv",
        "Q4 – Monthly Catch (All)": CLEANED / "Q4_MONTHLY_CATCH.csv",
        "Q4 – Monthly Catch by Species": CLEANED / "Q4_MONTHLY_FISH_CATCH.csv",
        "Q5 – Catch by Source": CLEANED / "Q5_MONTHLY_TOTALS_BY_SOURCE.csv",
        "Q6 – Monthly Waste": CLEANED / "Q6_MONTHLY_WASTE.csv",
        "Q6 – Species Waste": CLEANED / "Q6_MONTHLY_FISH_WASTE.csv",
        "Q7 – Loss by Reason": CLEANED / "Q7_ANNUAL_LOSS_BY_REASON.csv",
        "Q12 – Distribution Channels": CLEANED / "Q12_WHERE_DOES_THE_FISH_END_UP.csv",
        "GEO – Q3 Source of Fishing": GEO_CLEANED / "Q3_SOURCE_OF_FISHING.csv",
        "GEO – Q4 Monthly Catch": GEO_CLEANED / "Q4_MONTHLY_CATCH.csv",
    }

    for i, (name, path) in enumerate(datasets.items()):
        if path.exists():
            df = load_csv(path.name) if "GEO" not in name else load_geo_csv(path.name)
            with st.expander(f"📁 {name}"):
                st.dataframe(df.head(20), use_container_width=True)
                st.download_button(
                    label="⬇️ Download CSV",
                    data=df.to_csv(index=False).encode("utf-8"),
                    file_name=path.name,
                    mime="text/csv",
                    key=f"download_{i}_{path.name}"  # ✅ now fully unique
                )
        else:
            st.warning(f"❌ File missing: {path.name}")



