# geospatial_outputs.py

import pandas as pd
import geopandas as gpd
import plotly.graph_objects as go
import streamlit as st

MONTHS = [
    'January--Magh','February--Falgun','March--Chaitra','April--Boishakh',
    'May--Jeystho','June--Asharh','July--Srabon','August--Bhadro',
    'September--Ashwin','October--Kartik','November--Aghrahan','December--Poush'
]
COLOR_SCALE = 'OrRd'


def plot_q3_choropleth(gdf: gpd.GeoDataFrame, q3_df: pd.DataFrame) -> go.Figure:
    """
    Q3: Dropdown‐style choropleth showing counts per fishing source by district.
    """
    # Ensure district column is string
    gdf = gdf.rename(columns={'ADM2_EN': 'q1_d_zila'})
    gdf['q1_d_zila'] = gdf['q1_d_zila'].astype(str)
    q3 = q3_df.copy()
    q3['q1_d_zila'] = q3['q1_d_zila'].astype(str)

    # Merge geodata with Q3 counts
    merged = gdf.merge(q3, on='q1_d_zila')
    geojson = merged.to_crs(epsg=4326).__geo_interface__

    # Build traces for each source
    sources = [col for col in q3.columns if col != 'q1_d_zila']
    zmax_dict = {src: merged[src].max() for src in sources}

    fig = go.Figure()
    for i, src in enumerate(sources):
        fig.add_trace(go.Choroplethmap(
            geojson=geojson,
            locations=merged['q1_d_zila'],
            z=merged[src],
            featureidkey='properties.q1_d_zila',
            colorscale=COLOR_SCALE,
            zmin=0,
            zmax=zmax_dict[src],
            marker_line_width=0.5,
            colorbar=dict(
                title=f"{src} count",
                thickness=15,
                len=0.5,
                yanchor='middle',
                y=0.5
            ),
            hovertemplate=(
                "<b>%{properties.q1_d_zila}</b><br>"
                f"{src}: " + "%{z:,}<extra></extra>"
            ),
            visible=(i == 0)
        ))

    # Dropdown to select source
    buttons = [
        dict(method="update",
             label=src,
             args=[
                 {"visible": [j == i for j in range(len(sources))]},
                 {"title": {
                     "text": f"Distribution of <i>{src}</i> Fishing Source by District",
                     "x": 0.5
                 }}
             ])
        for i, src in enumerate(sources)
    ]

    fig.update_layout(
        template='plotly_white',
        title={
            "text": f"Distribution of <i>{sources[0]}</i> Fishing Source by District",
            "x": 0.5, "xanchor": "center"
        },
        updatemenus=[dict(
            buttons=buttons,
            direction="down",
            showactive=True,
            x=0, xanchor="left",
            y=1.1, yanchor="top"
        )],
        map=dict(
            style="carto-positron",
            zoom=7,
            center={"lat": 24.1860, "lon": 90.3563}
        ),
        margin=dict(l=10, r=10, t=120, b=40),
        width=1000,
        height=800,
        font=dict(family="Arial", color="#333")
    )

    # Annotations
    fig.add_annotation(
        text="Data: Bangladesh Fisheries Census 2024",
        showarrow=False,
        x=0.5, y=1.05,
        xref="paper", yref="paper",
        font=dict(size=12, color="gray")
    )
    fig.add_annotation(
        text="(Scroll to zoom, drag to pan)",
        showarrow=False,
        x=0.5, y=-0.02,
        xref="paper", yref="paper",
        font=dict(size=10, color="gray")
    )

    return fig


def plot_q4_choropleth(gdf: gpd.GeoDataFrame, q4_df: pd.DataFrame) -> go.Figure:
    """
    Q4: Slider‐style choropleth showing per-capita catch by month.
    """
    # Prepare data
    gdf = gdf.rename(columns={'ADM2_EN': 'District'})
    gdf['District'] = gdf['District'].astype(str)
    q4 = q4_df.copy()
    q4['District'] = q4['District'].astype(str)

    merged = gdf.merge(q4, on='District')
    geojson = merged.to_crs(epsg=4326).__geo_interface__

    zmax = {m: merged[m].max() for m in MONTHS}

    fig = go.Figure()
    for i, month in enumerate(MONTHS):
        fig.add_trace(go.Choroplethmap(
            geojson=geojson,
            locations=merged['District'],
            z=merged[month],
            featureidkey='properties.District',
            colorscale=COLOR_SCALE,
            zmin=0,
            zmax=zmax[month],
            marker_line_width=0.5,
            hovertemplate=(
                "<b>%{properties.District}</b><br>"
                f"{month}: " + "%{z:,}<extra></extra>"
            ),
            visible=(i == 0)
        ))

    # Slider steps
    steps = [
        dict(method="update",
             label=month,
             args=[
                 {"visible": [j == i for j in range(len(MONTHS))]},
                 {"title.text": f"Per Capita Fishing Catch — {month}"}
             ])
        for i, month in enumerate(MONTHS)
    ]

    sliders = [dict(
        active=0,
        pad={'t': 60, 'b': 10},
        x=0.05, y=0,
        xanchor='left', yanchor='top',
        len=0.9,
        steps=steps,
        currentvalue={'visible': True, 'font': {'size': 14}}
    )]

    fig.update_layout(
        template='plotly_white',
        title={
            "text": f"Per Capita Fishing Catch — {MONTHS[0]}",
            "x": 0.5, "xanchor": "center"
        },
        sliders=sliders,
        transition=dict(duration=500, easing='cubic-in-out'),
        map=dict(
            style="carto-positron",
            zoom=7,
            center={"lat": 24.1860, "lon": 90.3563}
        ),
        margin=dict(l=20, r=20, t=140, b=100),
        width=1000,
        height=800,
        font=dict(family="Arial", color="#333")
    )

    # Annotations
    fig.add_annotation(
        text="Data: Bangladesh Fisheries Census 2024",
        showarrow=False,
        x=0.5, y=0.97,
        xref="paper", yref="paper",
        font=dict(size=12, color="gray")
    )
    fig.add_annotation(
        text="(Scroll to zoom, drag to pan)",
        showarrow=False,
        x=0.5, y=-0.05,
        xref="paper", yref="paper",
        font=dict(size=10, color="gray")
    )

    # Legend for Bangla months
    legend_text = (
        "<b>Bangla Months</b><br>"
        "1. Boishakh (Apr–May)<br>"
        "2. Jeystho (May–Jun)<br>"
        "3. Asharh (Jun–Jul)<br>"
        "4. Srabon (Jul–Aug)<br>"
        "5. Bhadro (Aug–Sep)<br>"
        "6. Ashwin (Sep–Oct)<br>"
        "7. Kartik (Oct–Nov)<br>"
        "8. Aghrahan (Nov–Dec)<br>"
        "9. Poush (Dec–Jan)<br>"
        "10. Magh (Jan–Feb)<br>"
        "11. Falgun (Feb–Mar)<br>"
        "12. Chaitra (Mar–Apr)"
    )
    fig.add_annotation(
        x=0.01, y=0.92,
        xref="paper", yref="paper",
        text=legend_text,
        showarrow=False,
        align="left",
        font=dict(size=12, color="#333"),
        bgcolor="rgba(255, 255, 255, 0.8)",
        bordercolor="black",
        borderwidth=1,
        borderpad=4
    )

    return fig


def show_maps(shapefile_path: str, q3_csv: str, q4_csv: str) -> None:
    """
    Load shapefile and cleaned CSVs, then render both maps in Streamlit.
    """
    # Load data
    gdf = gpd.read_file(shapefile_path)
    q3_df = pd.read_csv(q3_csv, dtype={'q1_d_zila': str})
    q4_df = pd.read_csv(q4_csv, dtype={'District': str})

    # Plot and display
    fig1 = plot_q3_choropleth(gdf, q3_df)
    fig2 = plot_q4_choropleth(gdf, q4_df)

    st.plotly_chart(fig1, use_container_width=True)
    st.plotly_chart(fig2, use_container_width=True)
