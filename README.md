# Insurance Outcome Intelligence — Team 54 Capstone

A decision intelligence framework for health insurance portfolio optimization using predictive modeling and real-time decision simulation.

## Quick Start

### Prerequisites

- Python 3.12+
- pip package manager

### Installation

```bash
# 1. Install dependencies
pip install -r requirements.txt --break-system-packages

# If any are missing after that:
pip install xgboost imbalanced-learn streamlit plotly python-pptx --break-system-packages
```

### Run the Pipeline

```bash
# Train both models and generate all outputs
python3 src/train_pipeline.py
```

This will:
1. Load and preprocess 228,711 rows from `Dataset_of_health_insurance_portfolio.xlsx`
2. Train a **lapse prediction model** (XGBoost classifier)
3. Train a **claim cost prediction model** (XGBoost regressor)
4. Build the **Decision Intelligence Framework** (4 action categories)
5. Generate visualizations and save to `output/`
6. Save models and inference metadata to `models/`

The current pipeline excludes direct target-derived leakage fields such as
`exposure_time`, `loss_ratio`, `claim_premium_ratio_capped`, `avg_claim_per_service`,
`over_claim`, and `high_claim_flag` from model inputs. These fields are still kept
for EDA and business reporting where appropriate.

### Launch the Dashboard

```bash
# After training, start the interactive dashboard
streamlit run dashboard.py --server.port 8502 --server.headless true
```

Then open: **http://localhost:8502**

### Streamlit Community Cloud

Use these fields when deploying:

- Repository: `zzddddzz/insurance-outcome-intelligence-capstone`
- Branch: `main`
- Main file path: `streamlit_app.py`
- App URL suggestion: `insurance-outcome-intelligence-capstone`

## Project Structure

```
Health_Insurance_Datasets/
├── dashboard.py                    # Streamlit interactive dashboard
├── requirements.txt                # Python dependencies
├── src/
│   ├── data_pipeline.py            # Data loading, cleaning, feature engineering
│   ├── models.py                   # Model training + Decision Intelligence Framework
│   ├── train_pipeline.py           # End-to-end training script
│   ├── visualizations.py           # Static plots (PNG)
│   └── inference.py                # Production inference class
├── models/
│   ├── lapse_model.pkl             # Trained XGBoost lapse classifier
│   ├── lapse_model_bundle.pkl      # Lapse model + encoders/feature metadata for inference
│   ├── claim_model.pkl             # Trained XGBoost claim cost regressor
│   └── claim_model_bundle.pkl      # Claim model + encoders/feature metadata for inference
├── output/
│   ├── model_summary.json          # All model metrics
│   ├── decision_summary.csv        # Portfolio by decision action
│   ├── segment_summary.csv         # Segment-level analytics
│   ├── predictions_full.csv.gz     # Full 228K modeled records for dashboard
│   ├── predictions_sample.csv      # 20K preview predictions for fast QA
│   └── *.png                       # Generated visualizations
└── Dataset_of_health_insurance_portfolio.xlsx   # Source data
```

## Models

| Model | Task | Algorithm | Test AUC / R² |
|-------|------|-----------|---------------|
| Lapse Prediction | Binary classification | XGBoost | AUC: 0.8674 |
| Claim Cost Prediction | Regression | XGBoost | R²: 0.3468 |

## Decision Intelligence Framework

Customers are classified into 4 action categories:

- **STANDARD** (152,310) — Normal risk profile, standard management
- **RETAIN_HIGH** (56,394) — High lapse risk + profitable, prioritize retention
- **EARLY_RISK** (19,855) — High cost + unprofitable, early intervention
- **LOW_PRIORITY** (152) — Low value + high lapse, standard outreach only

## Dashboard Sections

1. **Key Performance Indicators** — Real-time portfolio metrics
2. **Exploratory Data Analysis** — Distributions and segment breakdowns
3. **Decision Intelligence Framework** — Visual risk classification
4. **Predictive Model Performance** — Model metrics and feature importance
5. **Decision Support Simulator** — Simulate pricing changes and retention strategies
6. **Customer-Level Risk View** — Ranked at-risk customer table

## Troubleshooting

- **`ModuleNotFoundError`**: Run `pip install -r requirements.txt`
- **Dashboard data missing**: Make sure `output/predictions_full.csv.gz` or `output/predictions_sample.csv` exists (run `python3 src/train_pipeline.py` first)
- **Port 8502 in use**: Change port with `--server.port 8503`

## Data Source

Pavani Katamreddy, Ashin Katwala, HyunChul Lee, Di Zhang, Savannah Lucero.
"Dataset of Health Insurance Portfolio." Mendeley Data, Version 4, 2025.
https://doi.org/10.17632/386vmj2tbk.4

Note: Dataset originates from a Spanish health insurer.
