import pandas as pd
import numpy as np

# —— Constants & Lookups ——
MONTHS = [
    'January--Magh','February--Falgun','March--Chaitra','April--Boishakh',
    'May--Jeystho','June--Asharh','July--Srabon','August--Bhadro',
    'September--Ashwin','October--Kartik','November--Aghrahan','December--Poush'
]

SOURCE = {
     1:  "Marsh", 2:  "Haor", 3:  "Canal", 4:  "River",
     5:  "Mohona", 6:  "River (Cultivation)", 7:  "Pond",
     8:  "Seasonal Cultivation", 9:  "Fish Farming in Cages",
    10: "Pen Culture (Net)", 11: "Flooded Reservoirs", 99: "Others"
}

REASONS = {
    1: "Damage During Harvesting", 2: "Too Long In Nets (Physical Damage)",
    3: "High Temperature, Delay In Taking To Market", 4: "Not Enough Ice or Insulated Containers",
    5: "Inadequacy of Fish Preservation Materials", 6: "Inadequate Cold Storage Facilities",
    7: "Inadequacy of Communication Systems", 8: "Spoilage of Fish During Transportation",
    9: "Loss of Fish From Unloading & Loading", 10: "Result of Medication Used On Fish",
    99: "Other Unrecorded Reason For Loss"
}

DISTRIBUTION = {
    'f': 'Local Agent','b': 'Wholesaler (Dealer)','p': 'Wholesaler (Wholesale)',
    'a': 'Wholesaler (Merchant)','c': 'Merchant (Commission Agent)','k': 'Retailer',
    'v': 'Consumer','h': 'Hotel Restaurant','d': 'Depot Owner',
    'ac':'Account Holder','r':'Exporter'
}


def load_main_data(data_dir: str = "DATASETS") -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Load the three raw survey CSVs plus the fish‐labels CSV.
    Returns: (fisher_df_1, fisher_df_2, fisher_df_3, fish_labels)
    """
    fisher_df_1 = pd.read_csv(f"{data_dir}/Fisher_slno.1-101.csv", low_memory=False)
    fisher_df_2 = pd.read_csv(f"{data_dir}/Fisher_slno.102-4291.csv", low_memory=False)
    fisher_df_3 = pd.read_csv(f"{data_dir}/Fisher_slno.4292-7217.csv", low_memory=False)
    fish_labels = pd.read_csv(f"{data_dir}/fish_species.csv",    low_memory=False)
    return fisher_df_1, fisher_df_2, fisher_df_3, fish_labels


def clean_main_data(
    fisher_df_1: pd.DataFrame,
    fisher_df_2: pd.DataFrame,
    fisher_df_3: pd.DataFrame,
    fish_labels: pd.DataFrame
) -> dict[str, pd.DataFrame]:
    """
    Apply cleaning & aggregation steps for Q3–Q12.
    Returns a dict of DataFrames keyed by question.
    """
    # 1) Build fish‐label lookup
    FISH_LABELS = pd.Series(
        fish_labels.Species_Name.values,
        index=fish_labels.Fish_Species_Serial_Number
    ).to_dict()

    # —— Q3: Overview of Fishing Techniques ——
    source_of_fishing = pd.concat([
        fisher_df_1.iloc[:, 22:27],
        fisher_df_2.iloc[:, 22:27],
        fisher_df_3.iloc[:, 22:27]
    ]).reset_index(drop=True)

    source_count = (
        source_of_fishing
        .melt(var_name='Question', value_name='Source')
        .Source
        .value_counts()
        .rename_axis('Source')
        .reset_index(name='Count')
    )
    source_count['Source Desc'] = source_count['Source'].map(SOURCE).fillna('Others')
    SOURCE_OF_FISHING_DF = (
        source_count
        .groupby('Source Desc', as_index=False)['Count']
        .sum()
        .sort_values('Count', ascending=False)
    )

    # —— Q4: Annual Catch Volumes & Species Harvest ——
    annual_catch_totals = pd.concat([
        fisher_df_1.iloc[:, 41:181],
        fisher_df_2.iloc[:, 41:181],
        fisher_df_3.iloc[:, 41:181]
    ]).reset_index(drop=True)

    # Map species codes to names
    for x in range(1, 11):
        col = f'q4_{x}_n'
        if col in annual_catch_totals:
            annual_catch_totals[col] = annual_catch_totals[col].map(FISH_LABELS).fillna('Other Species')

    # Total per month
    MONTHLY_CATCH_DF = pd.DataFrame({
        'Month': MONTHS,
        'Total': [
            (annual_catch_totals.get(f'q4_f_1_{m+1}', pd.Series()).sum()) / 1000
            for m in range(12)
        ]
    }).round(2)

    # Top 10 species annual totals
    species_totals = []
    for x in range(1, 11):
        fish_col = f'q4_{x}_n'
        if fish_col not in annual_catch_totals:
            continue
        for species in annual_catch_totals[fish_col].dropna().unique():
            row = {'Fish Name': species, 'Year Total': 0}
            for idx, mon in enumerate(MONTHS, start=1):
                col = f'q4_f_{x}_{idx}'
                val = (
                    annual_catch_totals.loc[annual_catch_totals[fish_col] == species, col].sum() / 1000
                    if col in annual_catch_totals else 0
                )
                row[mon] = val
                row['Year Total'] += val
            species_totals.append(row)

    MONTHLY_FISH_CATCH_DF = (
        pd.DataFrame(species_totals)
        .query("`Fish Name` != 'Other Species'")
        .sort_values('Year Total', ascending=False)
        .head(10)
        .round(2)
    )

    # —— Q5: Yearly Catch Totals by Harvesting Source ——
    catch_src = pd.concat([
        fisher_df_1.iloc[:, 181:322],
        fisher_df_2.iloc[:, 251:392],
        fisher_df_3.iloc[:, 251:392]
    ]).reset_index(drop=True)
    catch_src['q5'] = catch_src['q5'].map(SOURCE).fillna('Others')

    data = []
    for src in catch_src['q5'].dropna().unique():
        row = {'Source': src}
        for idx, mon in enumerate(MONTHS, start=1):
            cols = [
                c for c in catch_src
                if c.startswith(f'q5_') and c.endswith(f'_{idx}') and 't' not in c
            ]
            row[mon] = catch_src.loc[catch_src['q5'] == src, cols].sum(axis=1).sum() / 1000
        row['Total'] = sum(row[m] for m in MONTHS)
        data.append(row)
    MONTHLY_TOTALS_BY_SOURCE_DF = pd.DataFrame(data).round(2)

    # —— Q6: Annual Wastage Volumes & Species Waste ——
    annual_waste_totals = pd.concat([
        fisher_df_1.iloc[:, 322:434],
        fisher_df_2.iloc[:, 392:504],
        fisher_df_3.iloc[:, 392:504]
    ]).reset_index(drop=True)

    for x in range(1, 11):
        col = f'q6_{x}_n'
        if col in annual_waste_totals:
            annual_waste_totals[col] = annual_waste_totals[col].map(FISH_LABELS).fillna('Other Species')

    # Total wastage per month (all species)
    monthly_waste = []
    for m in range(1, 13):
        total = 0
        for x in range(1, 11):
            col = f'q6_{x}_{m}'
            if col in annual_waste_totals:
                total += annual_waste_totals[col].sum()
        monthly_waste.append(total / 1000)
    MONTHLY_WASTE_DF = pd.DataFrame({'Month': MONTHS, 'Total': monthly_waste}).round(2)

    # Top 10 waste species
    species_data = []
    for x in annual_waste_totals.filter(like='_n').columns:
        num = x.split('_')[1]
        for sp in annual_waste_totals[x].dropna().unique():
            vals = []
            for idx, mon in enumerate(MONTHS, start=1):
                c = f'q6_{num}_{idx}'
                vals.append(
                    (annual_waste_totals.loc[annual_waste_totals[x] == sp, c].sum() / 1000)
                    if c in annual_waste_totals else 0
                )
            species_data.append({'Fish Name': sp, **dict(zip(MONTHS, vals)), 'Year Total': sum(vals)})

    MONTHLY_FISH_WASTE_DF = (
        pd.DataFrame(species_data)
        .query("`Fish Name` != 'Other Species'")
        .sort_values('Year Total', ascending=False)
        .head(10)
        .round(2)
    )

    # —— Q7: Specific Causes of Fish Waste ——
    waste_reason_df = pd.concat([
        fisher_df_1.iloc[:, 434:714],
        fisher_df_2.iloc[:, 504:784],
        fisher_df_3.iloc[:, 504:784]
    ]).reset_index(drop=True)

    for x in range(1, 11):
        col = f'q7_{x}_n'
        if col in waste_reason_df:
            waste_reason_df[col] = waste_reason_df[col].map(FISH_LABELS).fillna('Other Species')

    portions = []
    for x in range(1, 11):
        req = [
            f'q7_{x}_n', f'q7_{x}_o_1',
            f'q7_{x}_o_2_1', f'q7_{x}_o_2_2', f'q7_{x}_o_3_1'
        ]
        if all(c in waste_reason_df for c in req):
            tmp = waste_reason_df[req].copy()
            tmp.columns = [
                'Fish Name', 'Quantity_Lost_mt',
                'Reason_1', 'Reason_2', 'Quantity_Lost_Reasons_mt'
            ]
            portions.append(tmp)

    df7 = pd.concat(portions)
    df7['Reason_1'] = df7['Reason_1'].map(REASONS)
    df7['Reason_2'] = df7['Reason_2'].map(REASONS)
    df7 = df7[
        (df7.Quantity_Lost_mt > 0) |
        (df7.Quantity_Lost_Reasons_mt > 0)
    ]

    melted = pd.melt(
        df7,
        id_vars=['Fish Name','Quantity_Lost_mt','Quantity_Lost_Reasons_mt'],
        value_vars=['Reason_1','Reason_2'],
        var_name='Reason_type', value_name='Reason'
    )
    final7 = (
        melted
        .dropna(subset=['Reason'])
        .groupby('Reason', as_index=False)['Quantity_Lost_Reasons_mt']
        .sum()
        .rename(columns={'Quantity_Lost_Reasons_mt':'total_quantity_lost_mt'})
    )
    ANNUAL_LOSS_BY_REASON_DF = (
        final7
        .assign(total_quantity_lost_mt=lambda d: d.total_quantity_lost_mt/1000)
        .sort_values('total_quantity_lost_mt', ascending=False)
        .round(2)
    )

    # —— Q12: Distribution Channels of the Fish ——
    fish_sold_df = pd.concat([
        fisher_df_1.iloc[:, 792:1114],
        fisher_df_2.iloc[:, 891:1213],
        fisher_df_3.iloc[:, 891:1213]
    ]).reset_index(drop=True)

    return {
        "Q3_source_of_fishing": SOURCE_OF_FISHING_DF,
        "Q4_monthly_catch": MONTHLY_CATCH_DF,
        "Q4_top_species": MONTHLY_FISH_CATCH_DF,
        "Q5_by_source": MONTHLY_TOTALS_BY_SOURCE_DF,
        "Q6_monthly_waste": MONTHLY_WASTE_DF,
        "Q6_top_waste_species": MONTHLY_FISH_WASTE_DF,
        "Q7_loss_by_reason": ANNUAL_LOSS_BY_REASON_DF,
        "Q12_distribution": fish_sold_df
    }
