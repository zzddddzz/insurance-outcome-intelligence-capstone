"""
Interactive Streamlit Dashboard for Health Insurance Decision Intelligence.
Provides exploration of lapse risk, claim costs, loss ratios, and decision recommendations.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json

# Page config
st.set_page_config(
    page_title="Insurance Outcome Intelligence",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Insurance Outcome Intelligence")
st.markdown("### Decision Intelligence Framework for Health Insurance Portfolio Optimization")
st.markdown("*Team 54 - MSDS 498 Capstone | Pavani Katamreddy, Ashin Katwala, HyunChul Lee, Di Zhang, Savannah Lucero*")

# Load data
@st.cache_data(ttl=3600)
def load_predictions(path="output/predictions_sample.csv"):
    return pd.read_csv(path)

@st.cache_data(ttl=3600)
def load_summary(path="output/model_summary.json"):
    with open(path) as f:
        return json.load(f)

@st.cache_data(ttl=3600)
def load_segment_summary(path="output/segment_summary.csv"):
    return pd.read_csv(path)

@st.cache_data(ttl=3600)
def load_decision_summary(path="output/decision_summary.csv"):
    return pd.read_csv(path)

@st.cache_data(ttl=3600)
def load_age_summary(path="output/age_summary.csv"):
    return pd.read_csv(path)


# Load all data
df = load_predictions()
model_summary = load_summary()
seg_summary = load_segment_summary()
decision_summary = load_decision_summary()
age_summary = load_age_summary()

# Sidebar filters
st.sidebar.header("Filters")
product_filter = st.sidebar.multiselect(
    "Product Type",
    options=sorted(df["type_product"].unique()),
    default=sorted(df["type_product"].unique()),
)
policy_type_filter = st.sidebar.multiselect(
    "Policy Type (DG)",
    options=sorted(df["type_policy_dg"].unique()),
    default=sorted(df["type_policy_dg"].unique()),
)
gender_filter = st.sidebar.multiselect(
    "Gender",
    options=sorted(df["gender"].unique()),
    default=sorted(df["gender"].unique()),
)
channel_filter = st.sidebar.multiselect(
    "Distribution Channel",
    options=sorted(df["distribution_channel"].unique()),
    default=sorted(df["distribution_channel"].unique()),
)
age_min, age_max = st.sidebar.slider(
    "Age Range",
    min_value=int(df["age"].min()),
    max_value=int(df["age"].max()),
    value=(int(df["age"].min()), int(df["age"].max())),
)
lapse_threshold = st.sidebar.slider(
    "Lapse Risk Threshold (top %)",
    min_value=50,
    max_value=95,
    value=75,
    help="Top N% of lapse probability = high risk",
)

# Apply filters
mask = (
    (df["type_product"].isin(product_filter)) &
    (df["type_policy_dg"].isin(policy_type_filter)) &
    (df["gender"].isin(gender_filter)) &
    (df["distribution_channel"].isin(channel_filter)) &
    (df["age"] >= age_min) &
    (df["age"] <= age_max)
)
df_filtered = df[mask].copy()

# KPI Cards
st.header("Key Performance Indicators")
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Policies Viewed", f"{df_filtered['ID_policy'].nunique():,}",
            f"{df_filtered['ID_policy'].nunique()}/{df['ID_policy'].nunique():,}")
col2.metric("Avg Premium", f"${df_filtered['premium'].mean():.0f}",
            f"{(df_filtered['premium'].mean()/df['premium'].mean()-1)*100:+.1f}% vs total")
col3.metric("Avg Claim Cost", f"${df_filtered['cost_claims_year'].mean():.0f}",
            f"{(df_filtered['cost_claims_year'].mean()/df['cost_claims_year'].mean()-1)*100:+.1f}% vs total")
col4.metric("Avg Lapse Probability", f"{df_filtered['lapse_probability'].mean():.3f}",
            f"{(df_filtered['lapse_probability'].mean()/df['lapse_probability'].mean()-1)*100:+.1f}% vs total")
col5.metric("Avg Loss Ratio", f"{df_filtered['loss_ratio'].mean():.2f}",
            f"{(df_filtered['loss_ratio'].mean()/df['loss_ratio'].mean()-1)*100:+.1f}% vs total")

# Section 1: EDA
st.header("Exploratory Data Analysis")
col1, col2 = st.columns(2)
with col1:
    st.subheader("Premium Distribution")
    fig_prem = px.histogram(df_filtered, x="premium", nbins=50,
                            title="Premium Distribution",
                            color_discrete_sequence=["#1f77b4"])
    fig_prem.update_layout(showlegend=False, template="plotly_white")
    st.plotly_chart(fig_prem, width='stretch')

with col2:
    st.subheader("Predicted Claim Cost Distribution")
    fig_claim = px.histogram(df_filtered, x="predicted_claim_cost", nbins=50,
                             title="Predicted Claim Cost Distribution",
                             color_discrete_sequence=["#ff7f0e"])
    fig_claim.update_layout(showlegend=False, template="plotly_white")
    st.plotly_chart(fig_claim, width='stretch')

# Lapse rate by segments
st.subheader("Lapse Rate by Product Type")
fig_lapse = px.bar(
    seg_summary[seg_summary["type_product"].isin(product_filter)].groupby(
        ["type_product", "type_policy_dg"]
    ).agg(avg_lapse=("lapse_rate", "mean")).reset_index(),
    x="type_product", y="avg_lapse", color="type_policy_dg",
    barmode="group", title="Avg Lapse Rate by Product & Policy Type",
    color_discrete_sequence=["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"],
)
fig_lapse.update_layout(template="plotly_white")
st.plotly_chart(fig_lapse, width="stretch")

# Age analysis
st.subheader("Risk by Age Group")
col1, col2 = st.columns(2)
with col1:
    fig_age_lapse = px.bar(
        age_summary, x="age_group", y="lapse_rate",
        title="Lapse Rate by Age Group", color="lapse_rate",
        color_continuous_scale="Reds",
    )
    fig_age_lapse.update_layout(template="plotly_white")
    st.plotly_chart(fig_age_lapse, width="stretch")

with col2:
    fig_age_claim = px.bar(
        age_summary, x="age_group", y="avg_claim",
        title="Avg Claim Cost by Age Group", color="avg_claim",
        color_continuous_scale="Blues",
    )
    fig_age_claim.update_layout(template="plotly_white")
    st.plotly_chart(fig_age_claim, width="stretch")

# Section 2: Decision Intelligence Framework
st.header("Decision Intelligence Framework")
st.markdown(
    "Each customer is classified into one of five action categories based on "
    "their lapse risk and predicted claim cost relative to premium."
)

# Update lapse threshold for this filter
lapse_thresh_val = df_filtered["lapse_probability"].quantile(lapse_threshold / 100)

# Decision action counts
action_counts = df_filtered["decision_action"].value_counts().reset_index()
action_counts.columns = ["action", "count"]

action_colors = {
    "RETAIN_HIGH": "#2ca02c",
    "REVIEW_PRICING": "#ff7f0e",
    "EARLY_RISK": "#d62728",
    "LOW_PRIORITY": "#7f7f7f",
    "STANDARD": "#1f77b4",
}
action_desc = {
    "RETAIN_HIGH": "High lapse risk + profitable — prioritize personalized outreach",
    "REVIEW_PRICING": "High predicted cost + underpriced — pricing review needed",
    "EARLY_RISK": "High cost + unprofitable — early clinical/financial intervention",
    "LOW_PRIORITY": "Low value + high lapse — standard outreach only",
    "STANDARD": "Normal risk — standard portfolio management",
}

col1, col2 = st.columns([1, 2])
with col1:
    st.subheader("Action Distribution")
    fig_actions = px.pie(
        action_counts, values="count", names="action",
        title="Portfolio by Decision Action",
        color="action", color_discrete_map=action_colors,
    )
    fig_actions.update_layout(template="plotly_white")
    st.plotly_chart(fig_actions, width="stretch")

with col2:
    st.subheader("Action Summary")
    action_df = pd.DataFrame({
        "Action": action_counts["action"],
        "Count": action_counts["count"],
        "Portfolio %": (action_counts["count"] / action_counts["count"].sum() * 100).round(1),
        "Description": action_counts["action"].map(action_desc),
    })
    st.dataframe(action_df, width="stretch")

# Decision scatter plot
st.subheader("Decision Space: Lapse Risk vs Predicted Claim Cost")
col1, col2 = st.columns([1, 1])

with col1:
    fig_scatter = px.scatter(
        df_filtered, x="lapse_probability", y="predicted_claim_cost",
        color="decision_action", size="premium",
        hover_data=["ID", "age", "type_product", "premium", "cost_claims_year"],
        title="Customer Decision Space (sample of 20K)",
        color_discrete_map=action_colors,
        opacity=0.6,
    )
    fig_scatter.add_vline(
        x=lapse_thresh_val,
        line_dash="dash", line_color="gray",
        annotation_text=f"Lapse threshold: {lapse_thresh_val:.3f}",
    )
    fig_scatter.add_hline(
        y=df_filtered["predicted_claim_cost"].median(),
        line_dash="dash", line_color="gray",
        annotation_text=f"Cost median: ${df_filtered['predicted_claim_cost'].median():.0f}",
    )
    fig_scatter.update_layout(template="plotly_white", hovermode="closest")
    st.plotly_chart(fig_scatter, width="stretch")

with col2:
    st.subheader("Segment Risk Heatmap")
    heat_data = df_filtered.groupby(["type_product", "type_policy_dg"]).agg(
        lapse_rate=("lapse_probability", "mean"),
        avg_loss_ratio=("loss_ratio", "mean"),
    ).reset_index()
    pivot = heat_data.pivot(index="type_product", columns="type_policy_dg", values="lapse_rate")
    fig_heat = px.imshow(
        pivot, labels={"color": "Lapse Rate"},
        title="Lapse Rate Heatmap: Product x Policy Type (DG)",
        color_continuous_scale="RdYlGn_r",
        text_auto=".3f",
    )
    fig_heat.update_layout(template="plotly_white")
    st.plotly_chart(fig_heat, width="stretch")

# Section 3: Predictive Model Insights
st.header("Predictive Model Performance")
tabs = st.tabs(["Lapse Model", "Claim Cost Model"])

with tabs[0]:
    val_m = model_summary["lapse_model"]["val"]
    test_m = model_summary["lapse_model"]["test"]
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Val Accuracy", f"{val_m['accuracy']:.4f}")
    col2.metric("Val Precision", f"{val_m['precision']:.4f}")
    col3.metric("Val Recall", f"{val_m['recall']:.4f}")
    col4.metric("Val F1", f"{val_m['f1']:.4f}")
    col5.metric("Val ROC AUC", f"{val_m['roc_auc']:.4f}")
    st.metric("Test ROC AUC", f"{test_m['roc_auc']:.4f}")

    st.markdown("**Top 15 Important Features:**")
    # Load feature importance from output if available
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(10, 8))
        try:
            feat_df = pd.read_csv("output/feature_importance.csv")
            top = feat_df.head(15).sort_values("importance", ascending=True)
            ax.barh(range(len(top)), top["importance"], color="#1f77b4")
            ax.set_yticks(range(len(top)))
            ax.set_yticklabels(top["feature"])
            ax.set_xlabel("Importance")
            ax.set_title("Top 15 Feature Importance (Lapse Model)")
            ax.invert_yaxis()
        except FileNotFoundError:
            ax.text(0.5, 0.5, "Train the pipeline first: `python src/train_pipeline.py`",
                    ha="center", va="center", fontsize=14)
            ax.set_title("Top 15 Feature Importance (Lapse Model)")
        plt.tight_layout()
        st.pyplot(fig)
    except Exception as e:
        st.info(f"Train models first: `python src/train_pipeline.py`")

with tabs[1]:
    cm = model_summary["claim_model"].get("val", model_summary["claim_model"])
    cm_test = model_summary["claim_model"].get("test")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Val RMSE", f"${cm['rmse']:.2f}")
    col2.metric("Val MAE", f"${cm['mae']:.2f}")
    col3.metric("Val R²", f"{cm['r2']:.4f}")
    col4.metric("Val MAPE", f"{cm['mape']:.2f}%")
    if cm_test:
        st.metric("Test R²", f"{cm_test['r2']:.4f}")

# Section 4: Decision Support Simulator
st.header("Decision Support Simulator")
st.markdown(
    "Simulate the impact of pricing changes or retention strategies on portfolio outcomes."
)

sim_col1, sim_col2 = st.columns(2)
with sim_col1:
    premium_change = st.slider("Premium Change (%)", -20, 20, 0, 1)
with sim_col2:
    retention_lift = st.slider("Retention Lift (reduce lapse by %)", 0, 30, 5, 1)

# Simulate impact
df_sim = df_filtered.copy()
df_sim["sim_premium"] = df_sim["premium"] * (1 + premium_change / 100)
sim_lapse_thresh = df_sim["lapse_probability"].quantile(lapse_threshold / 100)

# Reduced lapse probability
df_sim["sim_lapse_prob"] = df_sim["lapse_probability"] * (1 - retention_lift / 100)

# Recompute decisions
df_sim["sim_profitable"] = df_sim["sim_premium"] > df_sim["predicted_claim_cost"]
df_sim["sim_high_lapse"] = df_sim["sim_lapse_prob"] >= sim_lapse_thresh
df_sim["sim_underpriced"] = df_sim["sim_premium"] < (df_sim["predicted_claim_cost"] * 0.8)

old_actions = df_sim["decision_action"].value_counts().to_dict()
new_conditions = []
for _, row in df_sim.iterrows():
    if row["sim_high_lapse"] and row["sim_profitable"]:
        new_conditions.append("RETAIN_HIGH")
    elif row["sim_underpriced"] and row["sim_profitable"]:
        new_conditions.append("REVIEW_PRICING")
    elif row["sim_underpriced"] and not row["sim_profitable"]:
        new_conditions.append("EARLY_RISK")
    elif row["sim_high_lapse"] and not row["sim_profitable"]:
        new_conditions.append("LOW_PRIORITY")
    else:
        new_conditions.append("STANDARD")
df_sim["sim_action"] = new_conditions
new_actions = df_sim["sim_action"].value_counts().to_dict()

st.subheader("Impact of Changes")
action_names = ["RETAIN_HIGH", "REVIEW_PRICING", "EARLY_RISK", "LOW_PRIORITY", "STANDARD"]
impact_df = pd.DataFrame({
    "Action": action_names,
    "Before": [old_actions.get(a, 0) for a in action_names],
    "After": [new_actions.get(a, 0) for a in action_names],
    "Change": [new_actions.get(a, 0) - old_actions.get(a, 0) for a in action_names],
})
impact_df["Change_Pct"] = (impact_df["Change"] / impact_df["Before"].clip(lower=1) * 100).round(1)

fig_impact = px.bar(
    impact_df, x="Action", y=["Before", "After"],
    title="Decision Action Distribution: Before vs After Changes",
    color_discrete_sequence=["#1f77b4", "#ff7f0e"],
)
fig_impact.update_layout(template="plotly_white")
st.plotly_chart(fig_impact, width="stretch")

# Financial impact
original_revenue = df_sim["premium"].sum()
sim_revenue = df_sim["sim_premium"].sum()
original_claims = df_sim["predicted_claim_cost"].sum()
original_profit = original_revenue - original_claims
sim_profit = sim_revenue - original_claims

st.markdown("---")
st.subheader("Financial Impact Summary")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Original Revenue", f"${original_revenue:,.0f}")
col2.metric("Simulated Revenue", f"${sim_revenue:,.0f}")
col3.metric("Original Portfolio Profit", f"${original_profit:,.0f}")
col4.metric("Simulated Portfolio Profit", f"${sim_profit:,.0f}")
st.metric("Profit Change", f"${sim_profit - original_profit:,.0f} ({(sim_profit/original_profit-1)*100:.1f}%)")

# Bottom section: Data Table
st.header("Customer-Level Risk View")
top_n = st.slider("Show top N at-risk customers", 10, 500, 50)
high_risk = df_filtered[df_filtered["lapse_probability"] >= sim_lapse_thresh].sort_values(
    "lapse_probability", ascending=False
).head(top_n)

st.dataframe(
    high_risk[[
        "ID", "age", "gender", "type_product", "type_policy_dg",
        "premium", "cost_claims_year", "predicted_claim_cost",
        "lapse_probability", "loss_ratio", "decision_action",
    ]],
    width="stretch",
)

# Footer
st.markdown("---")
st.caption(
    "Insurance Outcome Intelligence | Built for Team 54 - MSDS 498 Capstone | "
    "Models trained on Spanish health insurer portfolio data (2017-2022) | "
    "For decision support purposes only"
)
