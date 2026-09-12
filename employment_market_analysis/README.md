# Employment Market Analysis

This module studies recruitment activity, salaries, employee benefits, and spatial differences across Beijing, Shanghai, Guangzhou, and Shenzhen using public job-listing data from 58.com.

## Data and Processing

- Job title, location, salary range, and job-description information
- Ten standardized employee-benefit indicators
- Salary parsing and monthly normalization
- IQR-based outlier treatment
- Binary encoding of benefit descriptions

## Workflow

```text
job_scraper.py → data_preprocessing.py → visualizations/
```

## Visualization Guide

| File | Output |
| --- | --- |
| `city_comparison.py` | Cross-city salary and benefit comparison |
| `benefits_radar.py` | Benefit coverage radar chart |
| `benefits_heatmap.py` | Benefit co-occurrence heatmap |
| `spatial_salary_benefits.py` | District-level salary and benefit map |
| `job_salary_3d.py` | District × occupation × salary view |
| `salary_volcano_plot.py` | Salary-difference significance plot |
| `job_benefits_sankey.py` | Occupation-to-benefit flows |
| `job_salary_benefits_sankey.py` | Job-to-salary-to-benefit flows |
| `job_region_benefits_network.py` | Job, region, and benefit network |

## Running the Module

```bash
python job_scraper.py
python data_preprocessing.py
python visualizations/city_comparison.py
```

Collection scripts may require updates when the source website changes. Use moderate request rates and comply with current platform policies.
