# Housing Market Analysis

This module examines second-hand housing listings in Beijing, Shanghai, Guangzhou, and Shenzhen. It combines listing-level web data, geocoding, feature cleaning, statistical modelling, and interactive geospatial visualization.

## Research Scope

- Approximately 100 listing pages per city
- Price, unit price, floor area, layout, floor level, orientation, decoration, listing date, ownership, and other attributes
- Up to 43 variables assembled from listing and detail pages
- District-level and cross-city comparison

## Workflow

1. `data_collection/get_data_yqx.py` collects listing and detail-page attributes.
2. `data_processing/data_clear.ipynb` standardizes fields, units, missing values, and derived variables.
3. `data_processing/geography_get.ipynb` enriches records with geographic coordinates.
4. `visualizations/` contains city-level notebooks, maps, interactive HTML charts, GeoJSON boundaries, and an R mapping workflow.

## Analytical Methods

- Distribution, KDE, box-plot, and pairwise analysis
- Price–area–unit-price relationships
- OLS regression and feature-importance analysis
- K-means segmentation
- Choropleth, heatmap, Sankey, parallel-coordinate, and 3D visualization

## Running the Module

```bash
python data_collection/get_data_yqx.py
jupyter notebook data_processing/data_clear.ipynb
```

City-specific visualization notebooks are located in `visualizations/`. Some notebooks retain paths from the original course environment; update those paths before executing them locally.
