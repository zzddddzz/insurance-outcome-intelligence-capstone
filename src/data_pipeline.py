"""
Data processing pipeline for health insurance portfolio analysis.
Handles loading, cleaning, feature engineering, and splitting for
lapse prediction and claim cost modeling.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder


LEAKAGE_FEATURES = [
    "exposure_time",
    "loss_ratio",
    "claim_premium_ratio_capped",
    "avg_claim_per_service",
    "over_claim",
    "high_claim_flag",
]

MODEL_FEATURES = [
    "age", "gender", "seniority_insured", "seniority_policy",
    "type_policy", "type_policy_dg", "type_product",
    "reimbursement", "new_business", "distribution_channel",
    "premium", "n_medical_services", "C_H", "C_C",
    "C_GI", "C_II", "C_IE_P", "C_IE_S", "C_IE_T",
    "C_GE_P", "C_GE_S", "C_GE_T",
    "IICIMUN", "IICIPROV",
    "n_insured_pc", "n_insured_mun", "n_insured_prov",
    "age_group", "tenure_group", "premium_pctile",
    "new_business_flag",
]

CATEGORICAL_COLS = [
    "gender", "type_policy", "type_policy_dg", "type_product",
    "reimbursement", "new_business", "distribution_channel",
    "C_H", "C_C", "age_group", "tenure_group",
]

NUMERICAL_COLS = [col for col in MODEL_FEATURES if col not in CATEGORICAL_COLS]


def load_data(path="Dataset_of_health_insurance_portfolio.xlsx"):
    """Load the main insurance portfolio dataset."""
    df = pd.read_excel(path)
    return df


def clean_and_preprocess(df):
    """Clean raw data and create analysis-ready features."""
    df = df.copy()

    # Keep only individual-level rows (drop policy-level aggregation rows)
    # ID pattern: "policy_insured" — keep rows where insured_id matches
    df["policy_id"] = df["ID"].str.rsplit("_", n=1).str[0].astype(int)
    df["insured_num"] = df["ID"].str.rsplit("_", n=1).str[1].astype(int)

    # Keep primary insured per policy (insured_num == 1) for cleaner modeling
    # but keep all rows since some analyses need all insureds
    # We'll keep all rows for modeling since lapse is at the insured level

    if "cost_claims_year" in df.columns:
        claim_cost = pd.to_numeric(df["cost_claims_year"], errors="coerce")

        # EDA-only derived claim metrics. These are intentionally excluded from
        # predictive model inputs to avoid target leakage.
        df["loss_ratio"] = claim_cost / df["premium"].clip(lower=1)
        df["claim_premium_ratio_capped"] = (
            claim_cost / df["premium"].clip(lower=1)
        ).clip(upper=10)
        df["avg_claim_per_service"] = claim_cost / df["n_medical_services"].clip(lower=1)
        df["over_claim"] = (claim_cost > df["premium"]).astype(int)
        df["high_claim_flag"] = (claim_cost > claim_cost.quantile(0.75)).astype(int)
    else:
        df["loss_ratio"] = np.nan
        df["claim_premium_ratio_capped"] = np.nan
        df["avg_claim_per_service"] = np.nan
        df["over_claim"] = 0
        df["high_claim_flag"] = 0

    # Age groups
    df["age_group"] = pd.cut(
        df["age"], bins=[0, 25, 35, 45, 55, 65, 75, 85, 100],
        labels=["18-25", "26-35", "36-45", "46-55", "56-65", "66-75", "76-85", "85+"]
    )

    # Tenure groups
    df["tenure_group"] = pd.cut(
        df["seniority_policy"], bins=[0, 2, 5, 10, 20, 40],
        labels=["<2yr", "2-5yr", "5-10yr", "10-20yr", "20+yr"]
    )

    # Premium percentile (for stratification)
    df["premium_pctile"] = df["premium"].rank(pct=True)

    df["new_business_flag"] = (df["new_business"] == "Yes").astype(int)

    return df


def prepare_feature_matrix(df, metadata=None, fit=True):
    """
    Build a model feature matrix with training-time preprocessing artifacts.

    When fit=True, label encoders and numeric medians are learned and returned
    in metadata. When fit=False, the supplied metadata is reused so inference
    applies the same column order, imputations, and categorical mappings.
    """
    df_encoded = df.copy()
    metadata = metadata or {}
    features = list(metadata.get("features", MODEL_FEATURES))
    categorical_cols = [col for col in metadata.get("categorical_cols", CATEGORICAL_COLS) if col in features]
    numerical_cols = [col for col in metadata.get("numerical_cols", NUMERICAL_COLS) if col in features]

    missing = [col for col in features if col not in df_encoded.columns]
    if missing:
        raise ValueError(f"Missing required feature columns: {missing}")

    numeric_medians = dict(metadata.get("numeric_medians", {}))
    label_encoders = dict(metadata.get("label_encoders", {}))

    for col in numerical_cols:
        df_encoded[col] = pd.to_numeric(df_encoded[col], errors="coerce")
        if fit:
            median = df_encoded[col].median()
            if pd.isna(median):
                median = 0.0
            numeric_medians[col] = float(median)
        df_encoded[col] = df_encoded[col].fillna(numeric_medians.get(col, 0.0))

    for col in categorical_cols:
        values = df_encoded[col].astype("object").where(df_encoded[col].notna(), "Unknown").astype(str)
        if fit:
            le = LabelEncoder()
            fit_values = pd.concat([values, pd.Series(["Unknown"])], ignore_index=True)
            le.fit(fit_values)
            label_encoders[col] = le
        else:
            if col not in label_encoders:
                raise ValueError(f"Missing label encoder for categorical column: {col}")
            le = label_encoders[col]
            known_values = set(le.classes_)
            fallback = "Unknown" if "Unknown" in known_values else le.classes_[0]
            values = values.where(values.isin(known_values), fallback)
        df_encoded[col] = le.transform(values)

    output_metadata = {
        "features": features,
        "numerical_cols": numerical_cols,
        "categorical_cols": categorical_cols,
        "label_encoders": label_encoders,
        "numeric_medians": numeric_medians,
        "excluded_leakage_features": LEAKAGE_FEATURES,
    }

    return df_encoded[features].values, output_metadata


def prepare_lapse_model(df):
    """
    Prepare features for lapse prediction (binary classification).
    Target: lapse == 1 (churned) vs lapse == 2 (retained).
    """
    df = df.copy()

    # Binary target: 1 = lapsed, 0 = retained
    df["lapse_binary"] = (df["lapse"] == 1).astype(int)

    X, metadata = prepare_feature_matrix(df, fit=True)
    y = df["lapse_binary"].values
    metadata["target"] = "lapse_binary"

    return X, y, metadata


def prepare_claim_model(df):
    """
    Prepare features for claim cost prediction (regression).
    Target: cost_claims_year (continuous, log-transformed for stability).
    """
    df = df.copy()

    if "cost_claims_year" not in df.columns:
        raise ValueError("cost_claims_year is required to train the claim model")

    X, metadata = prepare_feature_matrix(df, fit=True)
    claim_cost = pd.to_numeric(df["cost_claims_year"], errors="coerce").fillna(0).clip(lower=0)
    y = np.log1p(claim_cost.values)  # log transform for regression
    metadata["target"] = "cost_claims_year"

    return X, y, metadata


def split_data(X, y, test_size=0.3, random_state=42, stratify=None):
    """Split data into train/validation/test sets, defaulting to 70/15/15."""
    if stratify is not None:
        X_train, X_temp, y_train, y_temp = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=stratify
        )
        X_val, X_test, y_val, y_test = train_test_split(
            X_temp, y_temp, test_size=0.5, random_state=random_state, stratify=y_temp
        )
    else:
        X_train, X_temp, y_train, y_temp = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )
        X_val, X_test, y_val, y_test = train_test_split(
            X_temp, y_temp, test_size=0.5, random_state=random_state
        )

    return X_train, X_val, X_test, y_train, y_val, y_test
