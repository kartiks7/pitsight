# PitSight — BMW Intelligence Platform

A premium analytics dashboard combining sales intelligence with NLP-powered customer sentiment analysis across BMW's global portfolio (2019–2025).

## Quick Start

### Local
```bash
pip install -r requirements.txt
streamlit run app.py
```

### Streamlit Cloud
1. Push all files to your GitHub repo (root level, not inside a subfolder)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo → select `app.py`
4. Deploy

## Files
```
├── app.py              ← Main Streamlit application
├── table1.csv          ← BMW Sales Summary (22,145 rows, 2019-2025)
├── table2.csv.gz       ← Customer Experience + NLP scores (102,848 rows, gzipped)
├── requirements.txt    ← Python dependencies
├── .streamlit/
│   └── config.toml     ← Dark theme configuration
└── README.md
```

**Important:** `table2.csv.gz` is the gzipped version of the customer reviews dataset. The app reads it automatically. Do NOT unzip it.

## Pages
1. **Dashboard** — Sales overview: revenue trends, top models, country breakdown, channel analysis
2. **All Models** — Model deep-dive: yearly performance, avg price, model comparison
3. **Sentiment Intelligence** — NLP analysis: aspect scores, satisfaction trends, ML insights, review explorer

## Tech Stack
- **NLP:** Lexicon-based aspect sentiment analysis (6 aspects, zero keyword overlap)
- **ML:** Random Forest Classifier — 91.5% accuracy predicting customer satisfaction
- **Viz:** Plotly interactive charts with BMW M-inspired dark theme
