# Consumer Preference Analysis

This module uses more than 50,000 JD.com product reviews to compare regional purchasing behavior, customer sentiment, membership penetration, and product-language patterns across China.

## Collection

`jd_review_scraper.py` obtains product identifiers from search pages and uses DrissionPage with a Chromium session to capture structured review responses. The process may require manual sign-in and depends on JD.com's current page and request structure.

## Analysis

`visualization.py` covers review cleaning, province-name standardization, SnowNLP sentiment scoring, RFM-style regional segmentation, Chinese tokenization, stop-word filtering, PCA, geographic analysis, networks, radar charts, box plots, and word clouds.

## Key Files

| File | Purpose |
| --- | --- |
| `总评论final.xlsx` | Consolidated review dataset |
| `province_sentiment_metrics.csv` | Province-level sentiment metrics |
| `comment_driver_metrics.csv` | Review-driver summary features |
| `china_provinces.geojson` | Province boundaries |
| `stopwords_zh.txt` | Chinese stop-word list |
| `*.html` | Interactive exported charts |

## Running the Module

```bash
python jd_review_scraper.py
python visualization.py --task all
```

The scraper is intended only for academic reproduction with responsible request rates and compliance with current platform policies.
