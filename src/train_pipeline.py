"""
Main training pipeline.
Loads data, preprocesses, trains models, evaluates, saves artifacts, and generates plots.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from data_pipeline import load_data, clean_and_preprocess, prepare_lapse_model, prepare_claim_model, split_data
from models import train_lapse_model, train_claim_model, compute_decision_matrix
from visualizations import (
    plot_feature_importance, plot_lapse_distribution, plot_claim_distribution,
    plot_decision_matrix, create_dashboard_data, plot_sensitivity_analysis,
)
import pandas as pd
import numpy as np
import json
import joblib
import shutil
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, roc_auc_score,
    mean_squared_error, mean_absolute_error, r2_score,
)


def _summary_metadata(metadata):
    """Return metadata fields that can be written to JSON."""
    return {
        "features": metadata["features"],
        "numerical_cols": metadata["numerical_cols"],
        "categorical_cols": metadata["categorical_cols"],
        "excluded_leakage_features": metadata.get("excluded_leakage_features", []),
        "target": metadata.get("target"),
    }


def _claim_metrics(y_true_log, y_pred_log):
    """Compute claim metrics on the original claim-cost scale."""
    y_true = np.expm1(y_true_log)
    y_pred = np.expm1(y_pred_log)
    return {
        "rmse": float(np.sqrt(mean_squared_error(y_true, y_pred))),
        "mae": float(mean_absolute_error(y_true, y_pred)),
        "r2": float(r2_score(y_true, y_pred)),
        "mape": float(np.mean(np.abs((y_true - y_pred) / np.maximum(y_true, 1))) * 100),
    }


def main():
    os.makedirs("output", exist_ok=True)

    print("Loading data...")
    df = load_data()
    print(f"Loaded {df.shape[0]:,} rows, {df.shape[1]} columns\n")

    print("Preprocessing...")
    df = clean_and_preprocess(df)

    # --- Lapse Model ---
    print("\nPreparing lapse model data...")
    X_lapse, y_lapse, lapse_meta = prepare_lapse_model(df)
    X_tr, X_va, X_te, y_tr, y_va, y_te = split_data(X_lapse, y_lapse, stratify=y_lapse)
    print(f"Train: {X_tr.shape[0]}, Val: {X_va.shape[0]}, Test: {X_te.shape[0]}")
    print(f"Train lapse rate: {y_tr.mean():.3f}, Val lapse rate: {y_va.mean():.3f}, Test lapse rate: {y_te.mean():.3f}")

    lapse_model, lapse_metrics, lapse_feat_imp = train_lapse_model(
        X_tr, y_tr, X_va, y_va, feature_names=lapse_meta["features"]
    )
    lapse_feat_imp.rename_axis("feature").reset_index(name="importance").to_csv(
        "output/feature_importance.csv", index=False
    )

    # Test set evaluation
    y_prob_test = lapse_model.predict_proba(X_te)[:, 1]
    y_pred_test = lapse_model.predict(X_te)
    test_metrics = {
        "accuracy": float(accuracy_score(y_te, y_pred_test)),
        "precision": float(precision_score(y_te, y_pred_test, zero_division=0)),
        "recall": float(recall_score(y_te, y_pred_test, zero_division=0)),
        "f1": float(f1_score(y_te, y_pred_test, zero_division=0)),
        "roc_auc": float(roc_auc_score(y_te, y_prob_test)),
    }
    print(f"\nTest Metrics: {json.dumps(test_metrics, indent=2)}")
    joblib.dump(
        {"model": lapse_model, "metadata": lapse_meta},
        "models/lapse_model_bundle.pkl",
    )

    # --- Claim Cost Model ---
    print("\nPreparing claim model data...")
    X_claim, y_claim, claim_meta = prepare_claim_model(df)
    X_tr, X_va, X_te, y_tr, y_va, y_te = split_data(X_claim, y_claim)
    print(f"Train: {X_tr.shape[0]}, Val: {X_va.shape[0]}, Test: {X_te.shape[0]}")

    claim_model, claim_metrics, claim_feat_imp = train_claim_model(
        X_tr, y_tr, X_va, y_va, feature_names=claim_meta["features"]
    )
    claim_feat_imp.rename_axis("feature").reset_index(name="importance").to_csv(
        "output/claim_feature_importance.csv", index=False
    )
    claim_test_metrics = _claim_metrics(y_te, claim_model.predict(X_te))
    print(f"\nClaim Test Metrics: {json.dumps(claim_test_metrics, indent=2)}")
    joblib.dump(
        {"model": claim_model, "metadata": claim_meta},
        "models/claim_model_bundle.pkl",
    )

    # --- Predictions on full dataset for decision framework ---
    print("\nGenerating predictions for full dataset...")
    lapse_probs = lapse_model.predict_proba(X_lapse)[:, 1]
    claim_preds = np.expm1(claim_model.predict(X_claim))

    df["lapse_probability"] = lapse_probs
    df["predicted_claim_cost"] = claim_preds

    # --- Decision Intelligence Framework ---
    print("Building Decision Intelligence Framework...")
    df = compute_decision_matrix(df, lapse_probs, claim_preds)

    # Save decision analysis
    decision_summary = df.groupby("decision_action").agg(
        count=("ID", "count"),
        avg_premium=("premium", "mean"),
        avg_claim=("cost_claims_year", "mean"),
        avg_predicted_claim=("predicted_claim_cost", "mean"),
        avg_lapse_prob=("lapse_probability", "mean"),
        avg_loss_ratio=("loss_ratio", "mean"),
    ).reset_index()
    decision_summary.to_csv("output/decision_summary.csv", index=False)
    print(f"\nDecision Action Distribution:")
    print(decision_summary.to_string(index=False))

    # --- Generate Visualizations ---
    print("\nGenerating visualizations...")
    plot_feature_importance(lapse_feat_imp)
    plot_lapse_distribution(df)
    plot_claim_distribution(df)
    plot_decision_matrix(df)

    # Sensitivity analyses
    sensitivity_paths = []
    for param in ["age", "premium", "n_medical_services", "type_product", "distribution_channel"]:
        if param in df.columns:
            try:
                save_path = f"output/sensitivity_{param}.png"
                plot_sensitivity_analysis(df, param, save_path=save_path)
                sensitivity_paths.append(save_path)
            except Exception as e:
                print(f"  Skipped {param}: {e}")
    if sensitivity_paths:
        shutil.copyfile(sensitivity_paths[0], "output/sensitivity.png")

    # Save dashboard data
    seg, age, actions = create_dashboard_data(df)
    seg.to_csv("output/segment_summary.csv", index=False)
    age.to_csv("output/age_summary.csv", index=False)
    actions.to_csv("output/action_counts.csv", index=False)

    # Save full predictions for dashboard sampling
    sample = df.sample(n=20000, random_state=42)
    sample[["ID", "ID_policy", "ID_insured", "age", "gender", "type_product",
             "type_policy_dg", "premium", "cost_claims_year", "n_medical_services",
             "distribution_channel", "seniority_policy", "loss_ratio",
             "lapse_probability", "predicted_claim_cost", "decision_action",
             "age_group", "tenure_group"]].to_csv("output/predictions_sample.csv", index=False)

    # Summary stats
    summary = {
        "lapse_model": {"val": lapse_metrics, "test": test_metrics},
        "claim_model": {**claim_metrics, "val": claim_metrics, "test": claim_test_metrics},
        "data_shape": list(df.shape),
        "total_customers": df["ID_insured"].nunique(),
        "total_policies": df["ID_policy"].nunique(),
        "decision_actions": {k: int(v) for k, v in df["decision_action"].value_counts().items()},
        "split": {"train": 0.70, "validation": 0.15, "test": 0.15},
        "model_metadata": {
            "lapse": _summary_metadata(lapse_meta),
            "claim": _summary_metadata(claim_meta),
        },
        "sensitivity_outputs": sensitivity_paths,
    }
    with open("output/model_summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    print("\n" + "=" * 60)
    print("TRAINING PIPELINE COMPLETE")
    print("=" * 60)
    print(f"Lapse Model Val AUC:     {lapse_metrics['roc_auc']:.4f}")
    print(f"Lapse Model Test AUC:    {test_metrics['roc_auc']:.4f}")
    print(f"Claim Model Val R2:      {claim_metrics['r2']:.4f}")
    print(f"Decision categories:     {len(decision_summary)}")
    print(f"\nAll outputs saved to output/")


if __name__ == "__main__":
    main()
