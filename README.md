# PitSight — BMW Intelligence Platform

Premium analytics dashboard combining sales intelligence with NLP-powered customer sentiment analysis.

## Deploy
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Files
- `app.py` — Main application
- `table1.csv` — Sales data (22K rows)
- `table2.csv.gz` — Customer reviews + NLP scores (103K rows, gzipped)
- `requirements.txt` — Dependencies
- `.streamlit/config.toml` — Theme
