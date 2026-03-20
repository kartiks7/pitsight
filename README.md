# SentinelDrive — BMW Analytics Platform

## Quick Start

### Local
```bash
pip install -r requirements.txt
streamlit run app.py
```

### Streamlit Cloud (recommended for sharing)
1. Push this folder to a GitHub repo
2. Go to share.streamlit.io
3. Connect your repo → select app.py
4. Deploy

## Files
- `app.py` — Main Streamlit application
- `table1.csv` — BMW Sales Summary (22,145 rows, 2019-2025)
- `table2.csv` — Customer Experience with NLP scores (102,848 rows)
- `requirements.txt` — Python dependencies
- `.streamlit/config.toml` — Dark theme configuration

## Pages
1. **Dashboard** — Sales overview with revenue trends, top models, country breakdown, channel analysis
2. **All Models** — Model-specific deep dive with yearly performance, avg price, model carousel
3. **Sentiment Intelligence** — NLP analysis showing WHY sales trends happen, aspect scores, ML feature importance, review explorer
