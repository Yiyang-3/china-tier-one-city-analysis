# Multi-Dimensional Analysis of China's Tier-One Cities

An end-to-end data collection and visualization project comparing **Beijing, Shanghai, Guangzhou, and Shenzhen** across four connected dimensions: housing, employment, urban mobility, and consumer preferences.

Developed as a final project for the Data Collection and Visualization course at Shanghai Jiao Tong University, under the academic guidance of Associate Professor Haifeng Xu.

## Project Overview

Rapid urban development cannot be understood through a single indicator. This project combines large-scale web data, geospatial information, statistical analysis, machine learning, and interactive visualization to build a richer profile of China's four largest first-tier cities.

| Module | Core question | Main methods |
| --- | --- | --- |
| [Housing Market](housing_market_analysis/) | How do prices and housing characteristics vary across and within cities? | Web scraping, geocoding, regression, clustering, geospatial visualization |
| [Employment Market](employment_market_analysis/) | How do job supply, salary, and employee benefits differ by city and district? | Web scraping, text processing, outlier detection, heatmaps, Sankey diagrams |
| [Urban Mobility](urban_mobility_analysis/) | How accessible are subway systems, and how severe is road congestion? | API collection, GIS processing, network and time-series visualization |
| [Consumer Preferences](consumer_preference_analysis/) | How do purchasing behavior and review sentiment vary across regions? | Browser automation, sentiment analysis, RFM, PCA, word clouds |

## Repository Structure

```text
.
├── housing_market_analysis/       # Second-hand housing data and visualizations
├── employment_market_analysis/    # Recruitment, salary, and benefits analysis
├── urban_mobility_analysis/       # Subway networks and road congestion
├── consumer_preference_analysis/  # JD.com reviews and regional preferences
├── docs/original_reports_zh/      # Original Chinese course reports
├── requirements.txt
└── LICENSE
```

Each module contains its own README with its research design, workflow, file guide, and usage notes.

## Data Pipeline

1. **Collect** public listings, recruitment posts, transit data, traffic information, and product reviews.
2. **Clean** inconsistent text fields, missing values, units, geographic labels, and outliers.
3. **Enrich** observations with coordinates, regional indicators, sentiment scores, and engineered features.
4. **Analyze** cross-city differences using descriptive statistics, regression, clustering, RFM, and PCA.
5. **Visualize** findings through maps, distributions, networks, Sankey diagrams, radar charts, and interactive HTML outputs.

## Technology Stack

**Languages:** Python, R  
**Collection:** Requests, Beautiful Soup, Parsel, DrissionPage  
**Analysis:** pandas, NumPy, scikit-learn, statsmodels, SnowNLP, jieba  
**Visualization:** Matplotlib, Seaborn, Plotly, Pyecharts, Folium, GeoPandas, Cartopy, NetworkX, WordCloud  
**Geospatial tools:** AMap data and APIs, ArcGIS-compatible shapefiles

## Getting Started

```bash
git clone https://github.com/Yiyang-3/china-tier-one-city-analysis.git
cd china-tier-one-city-analysis
python -m venv .venv
pip install -r requirements.txt
```

Open the module README that matches the analysis you want to reproduce. Several collection scripts require live websites, browser sessions, API credentials, or request headers. Pre-collected datasets and exported visualizations are included so the work can still be reviewed without rerunning every scraper.

If a collector requires an authenticated session, copy `.env.example` to `.env` and supply your own current session values locally. Real cookies and credentials must never be committed.

## Responsible Use

The data was collected from publicly accessible pages for academic analysis. Website structures and access policies may change. Before rerunning a scraper, review the platform's current terms, robots policy, rate limits, and privacy requirements. Do not use this repository for commercial data extraction.

## Data Sources

- [Lianjia second-hand housing listings](https://www.lianjia.com/)
- [58.com recruitment listings](https://www.58.com/)
- [AMap subway and traffic services](https://www.amap.com/)
- [JD.com product pages and reviews](https://www.jd.com/)

## License

Code is released under the [MIT License](LICENSE). Third-party datasets and platform content remain subject to their original terms and rights.
