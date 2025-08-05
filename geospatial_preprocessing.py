# geospatial_preprocessing.py

import os
import re
import pandas as pd
import geopandas as gpd
import warnings

warnings.filterwarnings('ignore')

# —— Constants & Lookups ——
MONTH_MAPPING = {
    1: 'January--Magh',  2: 'February--Falgun', 3: 'March--Chaitra',
    4: 'April--Boishakh',5: 'May--Jeystho',      6: 'June--Asharh',
    7: 'July--Srabon',   8: 'August--Bhadro',    9: 'September--Ashwin',
    10:'October--Kartik',11:'November--Aghrahan',12:'December--Poush'
}
MONTHS = list(MONTH_MAPPING.values())

SOURCE = {
     1:  "Marsh", 2:  "Haor", 3:  "Canal", 4:  "River",
     5:  "Mohona", 6:  "River (Cultivation)", 7:  "Pond",
     8:  "Seasonal Cultivation", 9:  "Fish Farming in Cages",
    10: "Pen Culture (Net)", 11: "Flooded Reservoirs", 99: "Others"
}


def load_geo_data(path: str) -> gpd.GeoDataFrame:
    """
    Read in a GeoJSON or shapefile and return a GeoDataFrame.
    """
    return gpd.read_file(path)


def preprocess_geo(
    gdf: gpd.GeoDataFrame,
    survey_dir: str = "DATASETS",
    output_dir: str = "DATASETS/Cleaned_Data/GEO_DATA"
) -> dict[str, pd.DataFrame]:
    """
    Map district labels and compute geospatial tables for Q3 & Q4.

    - Loads the three Fisher survey CSVs plus species and district label lookups.
    - Applies district-name mapping.
    - Computes a district-by-source table (Q3) and writes it to CSV.
    - Computes a per-capita district catch table (Q4) and writes it to CSV.
    - Returns both DataFrames in a dict.
    """
    os.makedirs(output_dir, exist_ok=True)

    # 1) Load survey data & lookup tables
    df1 = pd.read_csv(f"{survey_dir}/Fisher_slno.1-101.csv",   low_memory=False)
    df2 = pd.read_csv(f"{survey_dir}/Fisher_slno.102-4291.csv",low_memory=False)
    df3 = pd.read_csv(f"{survey_dir}/Fisher_slno.4292-7217.csv",low_memory=False)
    fish_labels     = pd.read_csv(f"{survey_dir}/fish_species.csv",     low_memory=False)
    district_labels = pd.read_csv(f"{survey_dir}/new_district_labels.csv", low_memory=False)

    # 2) Build lookups
    FISH_LABELS = pd.Series(
        fish_labels.Species_Name.values,
        index=fish_labels.Fish_Species_Serial_Number
    ).to_dict()
    DIST_LABELS = pd.Series(
        district_labels.New_Labels.values,
        index=district_labels.Old_Labels
    ).to_dict()

    # 3) Map district codes in both survey data and geodataframe
    for df in (df1, df2, df3):
        df['q1_d_zila'] = df['q1_d_zila'].map(DIST_LABELS)
    gdf = gdf.rename(columns={'ADM2_EN':'q1_d_zila'})
    gdf['q1_d_zila'] = gdf['q1_d_zila'].astype(str)

    # —— Q3: Overview of Fishing Techniques by District ——
    # Collect columns [district + q3_1..q3_5]
    parts = []
    for df in (df1, df2, df3):
        sub = df[['q1_d_zila','q3_1','q3_2','q3_3','q3_4','q3_5']].copy()
        for col in ['q3_1','q3_2','q3_3','q3_4','q3_5']:
            sub[col] = sub[col].map(SOURCE)
        parts.append(sub)

    # Melt and pivot to wide format
    source_of_fishing = pd.concat(parts).reset_index(drop=True)
    melted = source_of_fishing.melt(
        id_vars=['q1_d_zila'],
        value_vars=['q3_1','q3_2','q3_3','q3_4','q3_5'],
        var_name='source_type',
        value_name='Source'
    ).dropna(subset=['Source'])

    GEO_Q3 = (
        melted
        .groupby(['q1_d_zila','Source'], as_index=False)
        .size()
        .unstack(fill_value=0)
        .reset_index()
    )
    GEO_Q3.to_csv(f"{output_dir}/Q3_SOURCE_OF_FISHING.csv", index=False)

    # —— Q4: Annual Catch Volumes & Per‐Capita by District ——
    # Grab [district + all q4_* fields]
    catch1 = df1.iloc[:, [df1.columns.get_loc('q1_d_zila')] + list(range(41, 181))]
    catch2 = df2.iloc[:, [df2.columns.get_loc('q1_d_zila')] + list(range(41, 181))]
    catch3 = df3.iloc[:, [df3.columns.get_loc('q1_d_zila')] + list(range(41, 181))]
    annual_catch = pd.concat([catch1, catch2, catch3]).reset_index(drop=True)

    # Map species codes to names
    for i in range(1, 11):
        ncol = f'q4_{i}_n'
        if ncol in annual_catch.columns:
            annual_catch[ncol] = annual_catch[ncol].map(FISH_LABELS).fillna('Other Species')

    # Replace unmapped codes
    for col in annual_catch.columns:
        if '_n' in col:
            annual_catch[col].fillna('Other Species', inplace=True)

    # Initialize a DataFrame to hold monthly & yearly totals
    data = {'District': annual_catch['q1_d_zila']}
    for month in MONTH_MAPPING.values():
        data[month] = [0] * len(annual_catch)
    data['Year Total'] = [0] * len(annual_catch)
    final_df = pd.DataFrame(data)

    # Identify annual‐total columns (those ending in '_t')
    year_cols = [c for c in annual_catch.columns if c.endswith('_t')]

    # Populate final_df
    for idx, row in annual_catch.iterrows():
        monthly = {m: 0 for m in MONTH_MAPPING.values()}
        year_total = 0
        for col, val in row.items():
            # month columns: q4_f_{i}_{month}
            m = re.match(r'q4_f_\d+_(\d+)', col)
            if m:
                mn = int(m.group(1))
                name = MONTH_MAPPING[mn]
                monthly[name] += 0 if pd.isna(val) else val
            # annual‐total columns
            if col in year_cols:
                year_total += 0 if pd.isna(val) else val
        for mon in MONTH_MAPPING.values():
            final_df.at[idx, mon] = monthly[mon] / 1000
        final_df.at[idx, 'Year Total'] = year_total / 1000

    # Save then reload to drop the first placeholder row (per original script)
    final_df.to_csv(f"{output_dir}/grouped_df.csv", index=False)
    grouped = pd.read_csv(f"{output_dir}/grouped_df.csv").drop(0).reset_index(drop=True)

    # Aggregate per‐district and convert to per‐capita
    sum_df   = grouped.groupby('District').sum().reset_index()
    count_df = grouped.groupby('District').count().reset_index()
    instances = count_df.iloc[:, -1]

    agg = pd.concat([sum_df, instances], axis=1)
    agg.columns = list(sum_df.columns) + ['Year Total.1']
    for mon in MONTHS:
        agg[mon] = agg[mon] / agg['Year Total.1']
    agg['Year Total'] = agg['Year Total'] / agg['Year Total.1']
    agg.drop(columns=['Year Total.1'], inplace=True)

    GEO_Q4 = agg.round(2)
    GEO_Q4.to_csv(f"{output_dir}/Q4_MONTHLY_CATCH.csv", index=False)

    return {
        "Q3_source_of_fishing": GEO_Q3,
        "Q4_monthly_catch": GEO_Q4
    }
