"""
Visualization module for health insurance analytics.
Generates key plots for EDA, model performance, and decision framework.
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import joblib

sns.set_style("whitegrid")
COLORS = {"primary": "#1f77b4", "blue": "#1f77b4", "orange": "#ff7f0e", "green": "#2ca02c",
          "red": "#d62728", "purple": "#9467bd", "gray": "#7f7f7f"}


def plot_feature_importance(feat_imp, top_n=20, save_path="output/feature_importance.png"):
    """Plot top N feature importance."""
    top = feat_imp.head(top_n).sort_values()
    plt.figure(figsize=(10, 8))
    bars = plt.barh(range(len(top)), top.values, color=COLORS["primary"])
    plt.yticks(range(len(top)), top.index)
    plt.xlabel("Importance")
    plt.title(f"Top {top_n} Feature Importance (Lapse Model)")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=150)
    plt.close()
    print(f"Saved: {save_path}")


def plot_lapse_distribution(df, save_path="output/lapse_distribution.png"):
    """Plot lapse rate by key segments."""
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    axes = axes.flatten()

    segments = [
        ("type_product", "Product Type"),
        ("type_policy_dg", "Policy Type (DG)"),
        ("gender", "Gender"),
        ("distribution_channel", "Distribution Channel"),
        ("reimbursement", "Reimbursement"),
        ("new_business", "New Business"),
    ]

    for idx, (col, title) in enumerate(segments):
        if col in df.columns:
            tbl = pd.crosstab(df[col], df.lapse, normalize="index")
            tbl.plot(kind="bar", stacked=True, ax=axes[idx],
                     color=[COLORS["red"], COLORS["green"], COLORS["orange"]])
            axes[idx].set_title(f"Lapse Rate by {title}")
            axes[idx].set_ylabel("Proportion")
            axes[idx].legend(["Lapsed", "Retained", "Other"])
            axes[idx].tick_params(axis="x", rotation=45)

    plt.suptitle("Lapse Distribution by Customer Segments", fontsize=16)
    plt.tight_layout()
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=150)
    plt.close()
    print(f"Saved: {save_path}")


def plot_claim_distribution(df, save_path="output/claim_distribution.png"):
    """Plot claim cost distribution and key relationships."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))

    # Claim cost distribution
    axes[0, 0].hist(df["cost_claims_year"], bins=100, edgecolor="black", alpha=0.7)
    axes[0, 0].axvline(df["cost_claims_year"].median(), color=COLORS["red"],
                        linestyle="--", label=f"Median: ${df['cost_claims_year'].median():.0f}")
    axes[0, 0].axvline(df["cost_claims_year"].mean(), color=COLORS["blue"],
                        linestyle="--", label=f"Mean: ${df['cost_claims_year'].mean():.0f}")
    axes[0, 0].set_title("Claim Cost Distribution")
    axes[0, 0].set_xlabel("Claim Cost ($)")
    axes[0, 0].set_ylabel("Frequency")
    axes[0, 0].legend()
    axes[0, 0].set_xscale("log")

    # Premium vs Claim Cost by age
    scatter = axes[0, 1].scatter(df["age"], df["cost_claims_year"],
                                  c=df["premium"], cmap="YlOrRd", alpha=0.3, s=10)
    axes[0, 1].set_title("Claim Cost vs Age (color=Premium)")
    axes[0, 1].set_xlabel("Age")
    axes[0, 1].set_ylabel("Claim Cost ($)")
    plt.colorbar(scatter, ax=axes[0, 1], label="Premium")
    axes[0, 1].set_yscale("log")

    # Loss ratio distribution
    lr = df["loss_ratio"].clip(upper=5)
    axes[1, 0].hist(lr, bins=100, edgecolor="black", alpha=0.7, color=COLORS["primary"])
    axes[1, 0].axvline(lr.mean(), color=COLORS["red"], linestyle="--",
                        label=f"Mean: {lr.mean():.2f}")
    axes[1, 0].set_title("Loss Ratio Distribution")
    axes[1, 0].set_xlabel("Loss Ratio (Claims/Premium)")
    axes[1, 0].set_ylabel("Frequency")
    axes[1, 0].legend()

    # Medical services vs claim cost
    axes[1, 1].scatter(df["n_medical_services"], df["cost_claims_year"],
                        c=df["lapse"], cmap="RdYlGn", alpha=0.3, s=10)
    axes[1, 1].set_title("Medical Services vs Claim Cost (color=Lapse)")
    axes[1, 1].set_xlabel("Number of Medical Services")
    axes[1, 1].set_ylabel("Claim Cost ($)")
    axes[1, 1].set_yscale("log")

    plt.suptitle("Claim Cost Analysis", fontsize=16)
    plt.tight_layout()
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=150)
    plt.close()
    print(f"Saved: {save_path}")


def plot_decision_matrix(df, save_path="output/decision_matrix.png"):
    """Plot the Decision Intelligence Framework scatter plot."""
    fig, ax = plt.subplots(figsize=(10, 8))

    actions = df["decision_action"].unique()
    colors_map = {
        "RETAIN_HIGH": COLORS["green"],
        "REVIEW_PRICING": COLORS["orange"],
        "EARLY_RISK": COLORS["red"],
        "LOW_PRIORITY": COLORS["gray"],
        "STANDARD": COLORS["primary"],
    }

    for action in actions:
        mask = df["decision_action"] == action
        ax.scatter(df.loc[mask, "lapse_probability"],
                    df.loc[mask, "predicted_claim_cost"],
                    alpha=0.3, s=15, label=action,
                    color=colors_map.get(action, "blue"))

    ax.set_xlabel("Lapse Probability")
    ax.set_ylabel("Predicted Claim Cost ($)")
    ax.set_title("Decision Intelligence Framework")
    ax.legend(loc="upper left", fontsize=8)
    ax.set_xlim(0, 1)
    ax.set_yscale("log")

    # Add quadrant lines
    lapse_q = df["lapse_probability"].quantile(0.75)
    cost_q = df["predicted_claim_cost"].median()
    ax.axvline(lapse_q, color="black", linestyle=":", alpha=0.5)
    ax.axhline(cost_q, color="black", linestyle=":", alpha=0.5)

    plt.tight_layout()
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=150)
    plt.close()
    print(f"Saved: {save_path}")


def create_dashboard_data(df):
    """Prepare data for Streamlit dashboard."""
    # Segment summaries
    segment_summary = df.groupby(["type_product", "type_policy_dg"]).agg(
        count=("ID", "count"),
        avg_premium=("premium", "mean"),
        avg_claim=("cost_claims_year", "mean"),
        lapse_rate=("lapse", lambda x: (x == 1).mean()),
        avg_loss_ratio=("loss_ratio", "mean"),
        avg_age=("age", "mean"),
    ).reset_index()
    segment_summary["loss_ratio"] = segment_summary["avg_claim"] / segment_summary["avg_premium"].clip(lower=1)

    # Age-based analysis
    age_summary = df.groupby("age_group").agg(
        count=("ID", "count"),
        avg_premium=("premium", "mean"),
        avg_claim=("cost_claims_year", "mean"),
        lapse_rate=("lapse", lambda x: (x == 1).mean()),
    ).reset_index()
    age_summary["loss_ratio"] = age_summary["avg_claim"] / age_summary["avg_premium"].clip(lower=1)

    # Decision action distribution
    action_counts = df["decision_action"].value_counts().reset_index()
    action_counts.columns = ["action", "count"]

    return segment_summary, age_summary, action_counts


def plot_sensitivity_analysis(df, param_name, save_path="output/sensitivity.png"):
    """Sensitivity analysis of key model parameters."""
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # Lapse rate by parameter
    if param_name in df.columns:
        plot_df = df.copy()
        group_col = param_name
        if pd.api.types.is_numeric_dtype(plot_df[param_name]) and plot_df[param_name].nunique() > 20:
            group_col = f"{param_name}_bin"
            plot_df[group_col] = pd.qcut(plot_df[param_name], q=10, duplicates="drop").astype(str)

        tbl = plot_df.groupby(group_col).agg(
            lapse_rate=("lapse", lambda x: (x == 1).mean()),
            avg_claim=("cost_claims_year", "mean"),
            avg_premium=("premium", "mean"),
        ).reset_index()
        tbl["loss_ratio"] = tbl["avg_claim"] / tbl["avg_premium"].clip(lower=1)
        labels = tbl[group_col].astype(str).tolist()

        axes[0].bar(range(len(tbl)), tbl["lapse_rate"], color=COLORS["red"], alpha=0.7)
        axes[0].set_title(f"Lapse Rate by {param_name}")
        axes[0].set_xlabel(param_name)
        axes[0].set_ylabel("Lapse Rate")
        axes[0].set_xticks(range(len(tbl)))
        axes[0].set_xticklabels(labels, rotation=45, ha="right")
        axes[0].tick_params(axis="x", rotation=45)

        axes[1].bar(range(len(tbl)), tbl["avg_claim"], color=COLORS["orange"], alpha=0.7)
        axes[1].set_title(f"Avg Claim Cost by {param_name}")
        axes[1].set_xlabel(param_name)
        axes[1].set_ylabel("Avg Claim Cost ($)")
        axes[1].set_xticks(range(len(tbl)))
        axes[1].set_xticklabels(labels, rotation=45, ha="right")
        axes[1].tick_params(axis="x", rotation=45)

        axes[2].bar(range(len(tbl)), tbl["loss_ratio"], color=COLORS["green"], alpha=0.7)
        axes[2].set_title(f"Loss Ratio by {param_name}")
        axes[2].set_xlabel(param_name)
        axes[2].set_ylabel("Loss Ratio")
        axes[2].set_xticks(range(len(tbl)))
        axes[2].set_xticklabels(labels, rotation=45, ha="right")
        axes[2].tick_params(axis="x", rotation=45)

    plt.tight_layout()
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=150)
    plt.close()
    print(f"Saved: {save_path}")
