# Urban Mobility Analysis

This module compares subway accessibility and road congestion in Beijing, Shanghai, Guangzhou, and Shenzhen using AMap transit data, live traffic layers, Python visualization, and GIS processing.

## Subway Analysis

- Extracts line names, colors, station sequences, coordinates, and station names
- Standardizes line-to-station relationships
- Produces network maps, station counts, and station-name word clouds

## Road Congestion Analysis

- Captures live traffic conditions at regular intervals
- Processes raster layers through channel separation and reclassification
- Vectorizes road segments and derives segment midpoints
- Estimates the share of congested roads over time

## Repository Layout

```text
urban_mobility_analysis/
├── data_collection/
│   ├── subway/       # Subway collection notebook
│   └── road_network/ # City notebooks, map exports, and GIS layers
└── visualizations/
    ├── subway/       # Source tables and visualization notebooks
    └── road_network/ # Processed summaries and visualization notebooks
```

AMap pages, APIs, and browser behavior may change, so collection notebooks may require current credentials, endpoints, or selectors before rerunning.
