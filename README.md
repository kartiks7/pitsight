# PitSight — BMW Customer Intelligence Platform

**Turning 102,848 customer voices into actionable intelligence.**

Every year, thousands of BMW owners walk into service centers, wait for their cars, and form opinions. Some leave satisfied. Some never come back. The difference between those two outcomes isn't age, gender, or warranty length — it's how often the car broke down and how long it sat in the workshop.

PitSight is an end-to-end data science project that proves this. It connects BMW sales performance with customer sentiment using NLP and Machine Learning, then surfaces the findings through an interactive Power BI dashboard.

---

## The Problem

Sales dashboards show what happened. Revenue dropped 80% for the BMW X6. Units went from 113 to 22.

But they don't show *why*.

Is it pricing? Reliability? Dealership experience? Software quality? Without analyzing customer voice at scale, product teams are guessing. PitSight was built to answer that question.

---

## What I Built

### 1. Data Engineering

Publicly available BMW sales datasets had a fundamental problem — top-selling models didn't match real regional patterns. A BMW 7 Series outselling the 3 Series in the United States, for example. That's not how the real market works.

So I built both datasets from scratch. I used AI-assisted web scraping to research actual BMW sales distributions by country, model pricing, seasonal trends, and channel breakdowns. The result:

- **Table 1 (Sales):** 22,145 transactions across 25 models, 21 countries, 7 years (2019–2025)
- **Table 2 (Customer Experience):** 102,848 individual customer records with reviews, service history, and NLP scores

Regional accuracy matters. X5 and X3 lead the US. 3 Series leads Germany. EVs show realistic adoption curves. The data makes sense.

### 2. NLP Sentiment Analysis

Each of the 102,848 customer reviews is scored across 6 aspects:

| Aspect | What It Measures | Example Keywords |
|--------|-----------------|-----------------|
| Maintenance | Repair costs, reliability | "minimal repairs", "expensive to maintain" |
| Comfort | Ride quality, cabin experience | "smooth and refined", "seats are uncomfortable" |
| Technology | iDrive, software, connected features | "years ahead of competition", "software is buggy" |
| Service Experience | Dealership staff, workshop process | "professional and efficient", "long wait times" |
| Fuel/Range | Fuel economy (ICE) / Range (EV) | "impressive mileage", "range anxiety" |
| Performance | Driving dynamics (M-series, Z4, i8 only) | "thrilling acceleration", "handles like a go-kart" |

The scoring uses a lexicon-based approach with zero keyword overlap between categories. EV and ICE reviews are scored with separate logic — "range anxiety" doesn't contaminate ICE fuel scores, and "fuel consumption" doesn't appear in EV range scores. Performance is scored only for sporty models (M2, M3, M4, M5, M8, Z4, i8) because asking a 3 Series about "track performance" doesn't make sense.

Each aspect gets a score from 1 (very negative) to 5 (very positive). A score of 0 means the aspect wasn't mentioned. The Sentiment Score is the average of non-zero scores. A threshold of 3.25 (optimized through a sweep from 3.0 to 4.0) classifies each customer as Satisfied or Dissatisfied.

### 3. Machine Learning

A Random Forest classifier (200 trees, max depth 12) was trained to predict satisfaction using only operational and demographic data — no review text, no aspect scores. Just numbers.

**Results:**
- Cross-validation accuracy: 90.6% (5-fold stratified)
- Test accuracy: 90.7%
- Models compared: Logistic Regression (90.8%), Random Forest (90.6%), Gradient Boosting (91.4%)

Random Forest was selected for interpretability. The feature importance told the real story:

| Feature | Importance |
|---------|-----------|
| Service History (workshop visits) | 44.9% |
| Service Time (days in service center) | 42.5% |
| Customer Age | 9.2% |
| Warranty Years | 2.6% |
| EV Status | 0.8% |

**Two operational metrics — service frequency and service duration — explain 87.4% of customer satisfaction.** Demographics explain less than 10%. This is the core finding. It means you don't need to read a single review to predict whether a customer is happy — just check how many times their car broke and how long the service took.

---

## Key Findings

### BMW X6 — Reliability Crisis
- Service visits rose from 1.5 to 6.6 per owner over 6 years
- Satisfaction collapsed from 96% to 0%
- Sales declined 80% (113 → 22 units)
- Lowest scores in ALL 6 sentiment aspects across the entire portfolio
- Maintenance score crashed from 3.7 to 1.4

### BMW X5 — The Recovery Proof
- 2022 quality dip: service visits spiked to 4.0, satisfaction crashed to 21%
- 2023 intervention: service visits brought back to 1.2, satisfaction restored to 99%
- Proof that targeted operational fixes directly restore customer satisfaction

### EV Models — Best in Portfolio
- Service visits dropped 65% (2.9 → 1.0)
- Satisfaction rose from 54% to 99% — lowest to highest segment
- i4, iX, iX3 now top the portfolio ranking at 96%
- Fewer mechanical parts = fewer repairs = happier customers

### Technology — The Weakest Link
- Lowest-scoring aspect across ALL vehicle categories
- 66.5% of all negative aspect scores in the portfolio come from Technology alone (Pareto)
- 10× more negative reviews than Comfort
- Improving (3.37 → 3.70) but still the weakest link

### The Service Visit Cliff
- Satisfaction drops from 78% to 10% between the 3rd and 4th service visit
- A 68 percentage point collapse — the largest satisfaction cliff in the data
- Any customer approaching visit #3 is at extreme churn risk

### The Service Duration Threshold
- 95% satisfaction when service takes 3–5 days
- 48% satisfaction when service exceeds 20 days
- Day 15 is the tipping point where satisfaction drops below 90%

---

## Power BI Dashboard

The dashboard is split into two reports accessible from a landing page:

### Report 1: Portfolio Performance
- **Sales** — Global revenue combo chart, top models carousel, country table with sparklines, channel donut, year-wise comparison
- **Models** — Per-model yearly table, hero image, average price, model carousel

### Report 2: Customer Intelligence
- **Sentiment** — Per-model satisfaction bar chart with conditional colors, service frequency and duration combo chart, aspect health cards (scores out of 5), overall satisfaction gauge
- **Reviews** — Aspect score multi-line chart, score distribution stacked bar with Satisfied/Dissatisfied/All toggle, customer review text table
- **Health** — Service visit cliff chart, service duration impact chart, portfolio risk and strength horizontal bars

All visuals use cross-filtering through DAX measures referencing Table 2 directly. Disconnected lookup tables (Aspects, Delivery_Buckets, Service_Buckets) enable aspect-level scoring and bucket analysis without breaking the data model.

---

## Repository Structure

```
pitsight/
├── data/
│   ├── BMW_Sales_Table1.csv            # 22,145 sales transactions
│   └── BMW_Table2_with_NLP.csv         # 102,848 customer records with NLP scores
├── notebooks/
│   └── PitSight_NLP_ML_Pipeline.ipynb  # Full NLP + ML pipeline (Python)
├── presentations/
│   ├── PitSight_Final_Deck.pptx        # Executive presentation (10 slides)
│   ├── PitSight_Technical_DeepDive.pptx # Technical deep dive (15 slides)
│   └── PitSight_2_Slides.pptx         # Landing page + NLP explanation
├── docs/
│   └── DAX_Measures.md                 # Power BI DAX measures reference
└── README.md
```

---

## Data Dictionary

### Table 1 — Sales (BMW_Sales_Table1.csv)
| Column | Description |
|--------|------------|
| Date | Transaction date |
| Year | 2019–2025 |
| Model | BMW model name (25 models) |
| Revenue | Transaction revenue (USD) |
| Quantity Sold | Units in this transaction |
| Region | Geographic region |
| Country | Country (21 countries) |
| Channel | Dealership / Online / Wholesale |

### Table 2 — Customer Experience (BMW_Table2_with_NLP.csv)
| Column | Description |
|--------|------------|
| Customer_ID | Unique customer identifier (CX_000001 format) |
| Date | Review date |
| Year | 2019–2025 |
| Model | BMW model name |
| Country | Customer's country |
| Customer_Age | Age at time of review |
| Customer_Gender | Male / Female |
| Service_History | Number of service center visits |
| Delivery_Days | Days the car spent in service center |
| Warranty_Years | Warranty duration (3–7 years) |
| Customer_Review | Full review text |
| is_ev | 1 = Electric Vehicle, 0 = ICE |
| maintenance_score | NLP aspect score (0–5) |
| comfort_score | NLP aspect score (0–5) |
| technology_score | NLP aspect score (0–5) |
| service_experience_score | NLP aspect score (0–5) |
| fuel_or_range_score | NLP aspect score (0–5) |
| performance_score | NLP aspect score (0–5, sporty models only) |
| Sentiment_Score | Average of non-zero aspect scores |
| Sentiment_Label | Satisfied (≥3.25) / Dissatisfied (<3.25) |
| review_length | Character count of review |
| review_word_count | Word count of review |
| negative_word_ratio | Ratio of negative words in review |

---

## Tech Stack

- **Python** — pandas, scikit-learn, nltk, numpy
- **Machine Learning** — Random Forest, Logistic Regression, Gradient Boosting
- **NLP** — Lexicon-based aspect sentiment analysis
- **Visualization** — Power BI (DAX, Power Query, custom measures)
- **Presentation** — pptxgenjs (automated slide generation)

---

## The One-Line Takeaway

> "How often it broke + how long the service took = 87% of whether a customer is satisfied."

Everything else — age, gender, warranty, even whether it's an EV — barely moves the needle. Fix the service experience, and satisfaction follows.

---

*Built by Kartik Sharma*
