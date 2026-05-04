"""
Model training and evaluation module.
Provides lapse prediction (classification) and claim cost prediction (regression)
using XGBoost with proper handling of class imbalance.
"""

import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, classification_report,
    mean_squared_error, mean_absolute_error, r2_score,
)
import xgboost as xgb
import joblib
import os


def train_lapse_model(X_train, y_train, X_val, y_val, output_dir="models", feature_names=None):
    """
    Train lapse prediction model with class imbalance handling.
    Returns best model, evaluation metrics, and feature importance.
    """
    print("=" * 60)
    print("TRAINING LAPSE PREDICTION MODEL")
    print("=" * 60)

    # Compute scale_pos_weight for imbalance
    n_neg = (y_train == 0).sum()
    n_pos = (y_train == 1).sum()
    scale_pos_weight = n_neg / max(n_pos, 1)
    print(f"Class distribution - Retained: {n_neg}, Lapsed: {n_pos}")
    print(f"scale_pos_weight: {scale_pos_weight:.2f}")
    if feature_names is None:
        feature_names = [f"feature_{i}" for i in range(X_train.shape[1])]

    # XGBoost Classifier
    model = xgb.XGBClassifier(
        n_estimators=300,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        scale_pos_weight=scale_pos_weight,
        reg_alpha=0.1,
        reg_lambda=1.0,
        random_state=42,
        eval_metric="logloss",
        n_jobs=-1,
    )

    model.fit(
        X_train, y_train,
        eval_set=[(X_val, y_val)],
        verbose=50,
    )

    # Evaluate
    y_pred = model.predict(X_val)
    y_prob = model.predict_proba(X_val)[:, 1]

    metrics = {
        "accuracy": accuracy_score(y_val, y_pred),
        "precision": precision_score(y_val, y_pred, zero_division=0),
        "recall": recall_score(y_val, y_pred, zero_division=0),
        "f1": f1_score(y_val, y_pred, zero_division=0),
        "roc_auc": roc_auc_score(y_val, y_prob),
    }

    print(f"\nVal Metrics:")
    print(f"  Accuracy:  {metrics['accuracy']:.4f}")
    print(f"  Precision: {metrics['precision']:.4f}")
    print(f"  Recall:    {metrics['recall']:.4f}")
    print(f"  F1 Score:  {metrics['f1']:.4f}")
    print(f"  ROC AUC:   {metrics['roc_auc']:.4f}")
    print(f"\nClassification Report:")
    print(classification_report(y_val, y_pred, target_names=["Retained", "Lapsed"]))

    # Feature importance
    importance = model.feature_importances_
    feat_imp = pd.Series(importance, index=feature_names).sort_values(ascending=False)

    print(f"\nTop 15 Features:")
    print(feat_imp.head(15).to_string())

    # Save model
    os.makedirs(output_dir, exist_ok=True)
    joblib.dump(model, os.path.join(output_dir, "lapse_model.pkl"))
    print(f"\nModel saved to {output_dir}/lapse_model.pkl")

    return model, metrics, feat_imp


def train_claim_model(X_train, y_train, X_val, y_val, output_dir="models", feature_names=None):
    """
    Train claim cost prediction model (log-transformed target).
    Returns best model, evaluation metrics, and feature importance.
    """
    print("=" * 60)
    print("TRAINING CLAIM COST PREDICTION MODEL")
    print("=" * 60)
    if feature_names is None:
        feature_names = [f"feature_{i}" for i in range(X_train.shape[1])]

    # XGBoost Regressor
    model = xgb.XGBRegressor(
        n_estimators=300,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        reg_alpha=0.1,
        reg_lambda=1.0,
        random_state=42,
        n_jobs=-1,
    )

    model.fit(X_train, y_train, eval_set=[(X_val, y_val)], verbose=50)

    # Evaluate
    y_pred_log = model.predict(X_val)
    y_pred = np.expm1(y_pred_log)
    y_true = np.expm1(y_val)

    metrics = {
        "rmse": np.sqrt(mean_squared_error(y_true, y_pred)),
        "mae": mean_absolute_error(y_true, y_pred),
        "r2": r2_score(y_true, y_pred),
        "mape": np.mean(np.abs((y_true - y_pred) / np.maximum(y_true, 1))) * 100,
    }

    print(f"\nVal Metrics (on original scale):")
    print(f"  RMSE:  {metrics['rmse']:.2f}")
    print(f"  MAE:   {metrics['mae']:.2f}")
    print(f"  R2:    {metrics['r2']:.4f}")
    print(f"  MAPE:  {metrics['mape']:.2f}%")

    # Feature importance
    importance = model.feature_importances_
    feat_imp = pd.Series(importance, index=feature_names).sort_values(ascending=False)

    print(f"\nTop 15 Features:")
    print(feat_imp.head(15).to_string())

    # Save model
    os.makedirs(output_dir, exist_ok=True)
    joblib.dump(model, os.path.join(output_dir, "claim_model.pkl"))
    print(f"\nModel saved to {output_dir}/claim_model.pkl")

    return model, metrics, feat_imp


def predict_lapse_prob(model, X, metadata):
    """Predict lapse probability for new data."""
    return model.predict_proba(X)[:, 1]


def predict_claim_cost(model, X):
    """Predict claim cost for new data (returns original scale)."""
    pred_log = model.predict(X)
    return np.expm1(pred_log)


def compute_decision_matrix(df, lapse_probs, claim_costs):
    """
    Build the Decision Intelligence Framework matrix.
    Classifies each customer into action categories:
    - RETAIN_HIGH: High lapse risk + high profitability (worth keeping)
    - REVIEW_PRICING: High claim cost + weak premium coverage
    - EARLY_RISK: Emerging high-cost segments
    - STANDARD: Normal risk profile
    - LOW_PRIORITY: Low risk, low value
    """
    df = df.copy()
    df["lapse_probability"] = lapse_probs
    df["predicted_claim_cost"] = claim_costs

    # Profitability: premium > predicted claim cost
    df["profitable"] = df["premium"] > df["predicted_claim_cost"]

    # Lapse risk threshold (top 25% probability)
    lapse_threshold = df["lapse_probability"].quantile(0.75)
    df["high_lapse_risk"] = df["lapse_probability"] >= lapse_threshold

    # Pricing adequacy: loss ratio < 0.8 means good coverage
    df["underpriced"] = df["premium"] < (df["predicted_claim_cost"] * 0.8)

    # Decision classification
    conditions = []
    actions = []

    for _, row in df.iterrows():
        if row["high_lapse_risk"] and row["profitable"]:
            actions.append("RETAIN_HIGH")
            conditions.append("High lapse risk + profitable - prioritize retention")
        elif row["underpriced"] and row["profitable"]:
            actions.append("REVIEW_PRICING")
            conditions.append("High predicted cost + underpriced - pricing review")
        elif row["underpriced"] and not row["profitable"]:
            actions.append("EARLY_RISK")
            conditions.append("High cost + unprofitable - early intervention")
        elif row["high_lapse_risk"] and not row["profitable"]:
            actions.append("LOW_PRIORITY")
            conditions.append("Low value + high lapse - standard outreach")
        else:
            actions.append("STANDARD")
            conditions.append("Normal risk - standard management")

    df["decision_action"] = actions
    df["action_description"] = conditions

    return df
