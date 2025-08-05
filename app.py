# app.py

import os
import streamlit as st
from preprocessing import load_main_data, clean_main_data
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
    plot_q12_distribution_sankey
)
from geospatial_preprocessing import load_geo_data, preprocess_geo
from geospatial_outputs import show_maps

# Page config
st.set_page_config(page_title="Bangladesh Fisheries Dashboard", layout="wide")

# Sidebar inputs
st.sidebar.header("Configuration")
data_dir = st.sidebar.text_input("Data folder", "DATASETS")
shapefile = st.sidebar.text_input("Shapefile path", "DATASETS/shape_files/shape.shp")

# Main Data Pipeline
if st.sidebar.checkbox("Run main data pipeline"):
    st.header("Survey Data Visualizations")

    # Load and clean
    df1, df2, df3, labels = load_main_data(data_dir)
    cleaned = clean_main_data(df1, df2, df3, labels)

    # Q3: Fishing sources
    st.subheader("Q3: Fishing Sources")
    st.plotly_chart(
        plot_q3_source_bar(cleaned["Q3_source_of_fishing"]),
        use_container_width=True
    )
    st.plotly_chart(
        plot_q3_source_grouped_bar(cleaned["Q3_source_of_fishing"]),
        use_container_width=True
    )

    # Q4: Monthly catch
    st.subheader("Q4: Total Monthly Catch")
    st.plotly_chart(
        plot_q4_monthly_catch_bar(cleaned["Q4_monthly_catch"]),
        use_container_width=True
    )
    st.plotly_chart(
        plot_q4_monthly_catch_line(cleaned["Q4_monthly_catch"]),
        use_container_width=True
    )
    st.plotly_chart(
        plot_q4_monthly_catch_area(cleaned["Q4_monthly_catch"]),
        use_container_width=True
    )

    # Q4: Top species
    st.subheader("Q4: Top 10 Fish Species")
    st.plotly_chart(
        plot_q4_top_species_bar(cleaned["Q4_top_species"]),
        use_container_width=True
    )
    st.plotly_chart(
        plot_q4_top_species_box(cleaned["Q4_top_species"]),
        use_container_width=True
    )
    st.plotly_chart(
        plot_q4_top_species_stacked_bar(cleaned["Q4_top_species"]),
        use_container_width=True
    )
    st.plotly_chart(
        plot_q4_top_species_line(cleaned["Q4_top_species"]),
        use_container_width=True
    )

    # Q5: Annual catch by source
    st.subheader("Q5: Annual Catch by Source")
    st.plotly_chart(
        plot_q5_annual_catch_by_source_bar(cleaned["Q5_by_source"]),
        use_container_width=True
    )
    st.plotly_chart(
        plot_q5_monthly_catch_by_source_line(cleaned["Q5_by_source"]),
        use_container_width=True
    )

    # Q6: Monthly wastage
    st.subheader("Q6: Monthly Wastage")
    st.plotly_chart(
        plot_q6_monthly_waste_bar(cleaned["Q6_monthly_waste"]),
        use_container_width=True
    )
    st.plotly_chart(
        plot_q6_monthly_waste_line(cleaned["Q6_monthly_waste"]),
        use_container_width=True
    )
    st.plotly_chart(
        plot_q6_monthly_waste_area(cleaned["Q6_monthly_waste"]),
        use_container_width=True
    )

    # Q6: Top waste species
    st.subheader("Q6: Top 10 Wasted Species")
    st.plotly_chart(
        plot_q6_top_waste_species_bar(cleaned["Q6_top_waste_species"]),
        use_container_width=True
    )
    st.plotly_chart(
        plot_q6_top_waste_species_box(cleaned["Q6_top_waste_species"]),
        use_container_width=True
    )

    # Q7: Loss by reason
    st.subheader("Q7: Loss by Reason")
    st.plotly_chart(
        plot_q7_loss_by_reason_bar(cleaned["Q7_loss_by_reason"]),
        use_container_width=True
    )

    # Q12: Distribution channels
    st.subheader("Q12: Distribution Channels")
    st.plotly_chart(
        plot_q12_distribution_sankey(cleaned["Q12_distribution"]),
        use_container_width=True
    )

# Geospatial Pipeline
if st.sidebar.checkbox("Run geospatial pipeline"):
    st.header("Geospatial Visualizations")

    # Preprocess and write geospatial CSVs
    gdf = load_geo_data(shapefile)
    preprocess_geo(
        gdf,
        survey_dir=data_dir,
        output_dir=os.path.join(data_dir, "Cleaned_Data", "GEO_DATA")
    )

    # Display maps
    show_maps(
        shapefile,
        os.path.join(data_dir, "Cleaned_Data", "GEO_DATA", "Q3_SOURCE_OF_FISHING.csv"),
        os.path.join(data_dir, "Cleaned_Data", "GEO_DATA", "Q4_MONTHLY_CATCH.csv")
    )
