# Forecasting and Preventing Fisheries Losses through Machine Intelligence

_Interactive Streamlit dashboard & notebooks for analyzing post‑harvest fish losses in Bangladesh._

---

## 📸 Screenshots

![Dashboard Overview](docs/overview.gif)
*Figure 1. Landing page, Navigation, Visualizations and Choropleth Map.*

---

## 🧭 Project Overview

This repo contains four Jupyter notebooks for ETL + visualization and a Streamlit app (`app.py`) that renders pre‑computed charts and maps from cleaned datasets. The focus is on Bangladesh’s inland fisheries: understanding catch trends, wastage, distribution channels, and district‑level patterns.

**Why this repo?**  
Large government survey files and shapefiles are hard to explore with spreadsheets alone. We pre‑compute and export compact CSVs so the app renders instantly without heavy processing at runtime.

**What you get**
- Pre‑processed CSVs in `DATASETS/Cleaned_Data/` and geospatial files in `DATASETS/shape_files/` (tracked with Git LFS).
- Plotly charts for Q3–Q7 (techniques, catch & waste trends, loss reasons) and Q12 (distribution flows via Sankey).
- Choropleth maps of fishing sources and monthly catch with an interactive month slider.

---

## 🗂 Repository Layout

```
.
├── 1_main_visualisation_preprocessing.ipynb
├── 2_main_visualisation_geospatial_preprocessing.ipynb
├── 3_main_visualisation_outputs.ipynb
├── 4_main_visualisation_geospatial_outputs.ipynb
├── app.py                      # Streamlit dashboard
├── outputs.py                  # Plotly charts (Q3–Q12)
├── geospatial_outputs.py       # Choropleths (Q3, Q4)
├── preprocessing.py            # (Notebook 1 code) ETL & aggregation
├── geospatial_preprocessing.py # (Notebook 2 code) spatial joins & exports
├── requirements.txt            # Python dependencies
└── DATASETS/
    ├── Cleaned_Data/
    │   ├── Q3_SOURCE_OF_FISHING.csv
    │   ├── Q4_MONTHLY_CATCH.csv
    │   ├── Q4_MONTHLY_FISH_CATCH.csv
    │   ├── Q5_MONTHLY_TOTALS_BY_SOURCE.csv
    │   ├── Q6_MONTHLY_WASTE.csv
    │   ├── Q6_MONTHLY_FISH_WASTE.csv
    │   ├── Q7_ANNUAL_LOSS_BY_REASON.csv
    │   └── GEO_DATA/
    │       ├── Q3_SOURCE_OF_FISHING.csv
    │       └── Q4_MONTHLY_CATCH.csv
    └── shape_files/
        ├── shape.shp (plus .dbf/.shx/.prj companions)  # LFS-tracked
        └── ...
```

> **Note:** The Streamlit app only *reads* these cleaned CSVs and shapefiles. All heavy preprocessing is already done in the notebooks.

---

## 💻 Run Locally

1) **Clone & enter the repo**
```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
```

2) **Install dependencies**
```bash
pip install -r requirements.txt
```

3) **(Important) Fetch large files with Git LFS**
```bash
git lfs install
git lfs pull
```
> LFS is required because large CSVs and the shapefile are versioned via Git LFS.

4) **Launch the dashboard**
```bash
streamlit run app.py
```

---

## ☁️ Deploying to Streamlit Community Cloud

1. Push this repository to GitHub (ensure LFS is enabled and your large files are committed with LFS).  
2. In Streamlit Community Cloud, click **New app** → Select your GitHub repo/branch → set **Main file path** to `app.py` → **Deploy**.

### If the app fails to start on Streamlit Cloud
- Make sure the repo is **public** or the app has access to your private repo.
- Verify LFS is actually pulling the files—missing `.shp/.dbf/.shx` companions or CSVs will crash the app.
- If LFS bandwidth or size limits are an issue, consider:
  - Zipping the cleaned CSVs to stay under GitHub size limits and unzipping at startup.
  - Hosting large files on a public storage bucket (e.g., Google Drive, Dropbox, S3) and downloading to a temporary folder in `app.py` at runtime.
  - Committing only the smaller, pre‑aggregated CSVs required for the charts.

---

## 🔍 Notebooks

- **1_main_visualisation_preprocessing.ipynb** – Core ETL, cleaning, and aggregation steps.  
- **2_main_visualisation_geospatial_preprocessing.ipynb** – Spatial joins & district label harmonization; exports geo CSVs.  
- **3_main_visualisation_outputs.ipynb** – Builds the Plotly figures for Q3–Q12.  
- **4_main_visualisation_geospatial_outputs.ipynb** – Prototyping and validation for the choropleths and sliders.

Each notebook can be run independently; outputs are saved into `DATASETS/Cleaned_Data/` for the app.

---

## 🧩 Configuration Notes

- The app expects a district column named `q1_d_zila`. In the shapefile this is derived from `ADM2_EN`.  
- If your Q4 geo CSV has `District`, the app renames it to `q1_d_zila` before mapping.
- File paths in `app.py` assume this repository layout; adjust paths if you move files.

---

## 📜 License & Acknowledgements

- Educational use for MSc Data Science coursework (Cardiff Metropolitan University).  
- Data: Bangladesh Fisheries Census (BAU), derived and aggregated for research/teaching.  
- Mapping: Natural Earth / BBS administrative boundaries.

---

## 🙋 FAQ

**Q: The app runs locally but fails on Streamlit Cloud. Why?**  
A: Most often the LFS assets weren’t fetched. Ensure `git lfs pull` works and your repo is public. If you hit LFS bandwidth limits, host the files elsewhere and download them at runtime.

**Q: Can I use different shapefiles or districts?**  
A: Yes—rename your district column to `q1_d_zila` (or update the mapping in `app.py`).

**Q: How big can my CSVs be?**  
A: Keep them as small as practical for fast app startup. Consider aggregating down to the columns the app actually visualizes.

## 👨‍🎓 Author

**Name:** Bapti Niloy Sarkar  
**Student ID:** st20310829  
**University:** Cardiff Metropolitan University
