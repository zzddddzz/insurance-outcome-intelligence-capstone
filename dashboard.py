"""Interactive Streamlit dashboard for the Team 54 capstone."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


ROOT = Path(__file__).resolve().parent

ACTION_COLORS = {
    "RETAIN_HIGH": "#2f7d51",
    "REVIEW_PRICING": "#b9484a",
    "EARLY_RISK": "#8f3d3d",
    "LOW_PRIORITY": "#76629c",
    "STANDARD": "#315f86",
}

ACTION_LABELS = {
    "ALL": "All",
    "RETAIN_HIGH": "Retain",
    "REVIEW_PRICING": "Reprice",
    "EARLY_RISK": "Early risk",
    "LOW_PRIORITY": "Low priority",
    "STANDARD": "Standard",
}

PRODUCT_LABELS = {
    "S": "Savings",
    "P": "Personal",
    "D": "Death",
    "I": "Individual",
}

CHANNEL_LABELS = {
    "A": "Agent",
    "I": "Intermediary",
    "D": "Direct",
}

GENDER_LABELS = {
    "F": "Female",
    "M": "Male",
}

FEATURE_LABELS = {
    "n_medical_services": "Medical service usage",
    "new_business_flag": "New business flag",
    "type_product": "Product type",
    "seniority_insured": "Customer tenure",
    "new_business": "New business",
    "tenure_group": "Tenure band",
    "distribution_channel": "Distribution channel",
    "age_group": "Age band",
    "seniority_policy": "Policy tenure",
    "IICIPROV": "Province indicator",
    "age": "Age",
    "type_policy": "Policy type",
    "type_policy_dg": "Policy group",
    "premium": "Premium",
    "loss_ratio": "Loss ratio",
    "n_insured_mun": "Insured count by municipality",
    "n_insured_prov": "Insured count by province",
}

PLOT_ACTION_LABELS = {
    "RETAIN_HIGH": "Retain",
    "REVIEW_PRICING": "Reprice",
    "EARLY_RISK": "Early risk",
    "LOW_PRIORITY": "Low priority",
    "STANDARD": "Standard",
}
PLOT_ACTION_COLORS = {
    PLOT_ACTION_LABELS[action]: color for action, color in ACTION_COLORS.items()
}

ACTION_NOTES = {
    "RETAIN_HIGH": "High lapse risk and profitable. Prioritize retention outreach.",
    "REVIEW_PRICING": "Underpriced relative to expected claims. Review pricing.",
    "EARLY_RISK": "High expected claims. Route to clinical or financial intervention.",
    "LOW_PRIORITY": "High lapse and limited margin. Keep light-touch outreach.",
    "STANDARD": "No immediate escalation. Keep normal portfolio management.",
}


st.set_page_config(
    page_title="Portfolio Action Console",
    page_icon="PA",
    layout="wide",
    initial_sidebar_state="expanded",
)


def add_css() -> None:
    st.markdown(
        """
        <style>
        :root {
            --bg-page: #f4f5f3;
            --bg-card: #ffffff;
            --bg-rail: #fafbf9;
            --ink-1: #0e1a1f;
            --ink-2: #29363c;
            --ink-3: #46565e;
            --ink-4: #687780;
            --line-1: #dde0db;
            --line-2: #e8eae5;
            --teal: #2f6f67;
            --red: #b9484a;
            --amber: #c08a2d;
            --violet: #76629c;
        }

        #MainMenu, footer, [data-testid="stDecoration"] { display: none !important; }
        header[data-testid="stHeader"] { display: none !important; }

        .stApp {
            background: var(--bg-page);
            color: var(--ink-1);
        }

        .block-container {
            max-width: 1320px;
            padding-top: 1rem;
            padding-bottom: 2rem;
        }

        section[data-testid="stSidebar"] {
            background: var(--bg-rail);
            border-right: 1px solid var(--line-1);
        }

        h1, h2, h3, p, label, span, div { letter-spacing: 0; }

        .topbar {
            align-items: center;
            background: var(--bg-card);
            border: 1px solid var(--line-1);
            border-radius: 6px;
            display: flex;
            justify-content: space-between;
            margin-bottom: 12px;
            padding: 10px 12px;
        }

        .brand {
            align-items: center;
            display: flex;
            gap: 10px;
            min-width: 0;
        }

        .brand-mark {
            align-items: center;
            background: var(--ink-1);
            border-radius: 3px;
            color: white;
            display: inline-flex;
            font-size: 11px;
            font-weight: 700;
            height: 22px;
            justify-content: center;
            letter-spacing: 0;
            width: 22px;
        }

        .brand-title {
            color: var(--ink-1);
            font-size: 14px;
            font-weight: 700;
            line-height: 1.1;
        }

        .brand-subtitle {
            color: var(--ink-3);
            font-size: 12.5px;
            line-height: 1.2;
        }

        .live-pill {
            align-items: center;
            background: #eef3ef;
            border: 1px solid var(--line-2);
            border-radius: 999px;
            color: var(--ink-2);
            display: inline-flex;
            font-size: 12.5px;
            font-weight: 650;
            gap: 6px;
            padding: 3px 9px;
        }

        .live-pill::before {
            background: #64a36f;
            border-radius: 50%;
            content: "";
            height: 7px;
            width: 7px;
        }

        .page-kicker {
            color: var(--ink-3);
            font-size: 12.5px;
            font-weight: 700;
            letter-spacing: 0.08em;
            margin-bottom: 3px;
            text-transform: uppercase;
        }

        .page-title {
            color: var(--ink-1);
            font-size: clamp(28px, 4vw, 42px);
            font-weight: 750;
            line-height: 1;
            margin: 0;
        }

        .page-copy {
            color: var(--ink-3);
            font-size: 15px;
            line-height: 1.45;
            margin: 8px 0 16px;
        }

        .exec-brief {
            background: var(--ink-1);
            border: 1px solid var(--ink-1);
            border-radius: 6px;
            color: #ffffff;
            margin: 14px 0 14px;
            padding: 18px 18px 16px;
        }

        .exec-eyebrow {
            color: #aec6bd;
            font-size: 11.5px;
            font-weight: 800;
            letter-spacing: 0.08em;
            margin-bottom: 8px;
            text-transform: uppercase;
        }

        .exec-title {
            color: #ffffff;
            font-size: clamp(20px, 3vw, 30px);
            font-weight: 760;
            line-height: 1.12;
            margin-bottom: 9px;
        }

        .exec-copy {
            color: #d8e1dd;
            font-size: 15px;
            line-height: 1.45;
            max-width: 980px;
        }

        .exec-grid {
            display: grid;
            gap: 10px;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            margin: 0 0 14px;
        }

        .exec-card {
            background: var(--bg-card);
            border: 1px solid var(--line-1);
            border-radius: 5px;
            min-height: 104px;
            padding: 12px 13px;
        }

        .exec-label {
            color: var(--ink-3);
            font-size: 11.5px;
            font-weight: 800;
            letter-spacing: 0.06em;
            text-transform: uppercase;
        }

        .exec-value {
            color: var(--ink-1);
            font-size: 22px;
            font-weight: 760;
            line-height: 1.12;
            margin-top: 7px;
        }

        .exec-note {
            color: var(--ink-2);
            font-size: 12.5px;
            line-height: 1.35;
            margin-top: 7px;
        }

        .kpi-card {
            background: var(--bg-card);
            border: 1px solid var(--line-1);
            border-radius: 5px;
            min-height: 116px;
            padding: 13px 14px;
        }

        .kpi-label {
            color: var(--ink-3);
            font-size: 11.5px;
            font-weight: 700;
            letter-spacing: 0.08em;
            line-height: 1.2;
            text-transform: uppercase;
        }

        .kpi-value {
            color: var(--ink-1);
            font-size: 27px;
            font-weight: 650;
            line-height: 1.05;
            margin-top: 8px;
        }

        .kpi-delta {
            color: var(--ink-2);
            font-size: 12.5px;
            line-height: 1.35;
            margin-top: 7px;
        }

        .panel {
            background: var(--bg-card);
            border: 1px solid var(--line-1);
            border-radius: 5px;
            margin-bottom: 12px;
            padding: 13px 14px;
        }

        .panel-head {
            align-items: baseline;
            border-bottom: 1px solid var(--line-2);
            display: flex;
            gap: 10px;
            justify-content: space-between;
            margin: 0 0 12px;
            padding: 0 0 10px;
        }

        .panel-title {
            color: var(--ink-1);
            font-size: 16px;
            font-weight: 700;
            line-height: 1.25;
        }

        .panel-meta {
            color: var(--ink-3);
            font-size: 12.5px;
            font-weight: 600;
            line-height: 1.35;
            text-align: right;
        }

        .action-chip {
            border: 1px solid;
            border-radius: 3px;
            display: inline-block;
            font-size: 11.5px;
            font-weight: 800;
            letter-spacing: 0;
            padding: 2px 7px;
            text-transform: none;
            white-space: nowrap;
        }

        .chip-retain { background: #eaf3e7; border-color: #bfd8bb; color: #2f7d51; }
        .chip-review_pricing { background: #f7e6e3; border-color: #e2c0bd; color: #9b3f42; }
        .chip-early_risk { background: #f3dbd9; border-color: #dbaaa7; color: #8f3d3d; }
        .chip-low_priority { background: #eee8f7; border-color: #cdc1e0; color: #67518c; }
        .chip-standard { background: #e7edf3; border-color: #bfd0df; color: #315f86; }

        .segment-card {
            background: var(--bg-card);
            border: 1px solid var(--line-1);
            border-left: 3px solid var(--teal);
            border-radius: 5px;
            margin-bottom: 8px;
            padding: 10px 12px;
        }

        .segment-name {
            color: var(--ink-1);
            font-size: 14px;
            font-weight: 750;
            line-height: 1.3;
        }

        .segment-grid {
            display: grid;
            gap: 7px;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            margin-top: 8px;
        }

        .mini-label {
            color: var(--ink-3);
            font-size: 10.5px;
            font-weight: 700;
            letter-spacing: 0.06em;
            text-transform: uppercase;
        }

        .mini-value {
            color: var(--ink-1);
            font-size: 13px;
            font-weight: 650;
        }

        div[data-testid="stRadio"] > label { display: none; }
        div[role="radiogroup"] {
            background: var(--bg-card);
            border: 1px solid var(--line-1);
            border-radius: 5px;
            gap: 0.35rem;
            padding: 5px;
        }

        div[role="radiogroup"] label {
            border: 1px solid transparent;
            border-radius: 4px;
            color: var(--ink-2) !important;
            font-weight: 700;
            min-height: 34px;
            padding: 4px 12px;
        }

        div[role="radiogroup"] label p,
        div[role="radiogroup"] label span,
        div[role="radiogroup"] label div {
            color: var(--ink-2) !important;
            font-size: 15px !important;
            font-weight: 700 !important;
        }

        div[role="radiogroup"] label:has(input:checked) {
            background: var(--ink-1) !important;
            border-color: var(--ink-1) !important;
            box-shadow: 0 0 0 1px var(--ink-1);
            color: #ffffff !important;
        }

        div[role="radiogroup"] label:has(input:checked) p,
        div[role="radiogroup"] label:has(input:checked) span,
        div[role="radiogroup"] label:has(input:checked) div {
            color: #ffffff !important;
        }

        div[role="radiogroup"] input {
            accent-color: var(--ink-1);
        }

        div[data-testid="stMultiSelect"] span,
        div[data-testid="stSlider"] p {
            color: var(--ink-2) !important;
            font-weight: 650;
        }

        @media (max-width: 800px) {
            .topbar { align-items: flex-start; gap: 10px; }
            .exec-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
            .segment-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
            .panel-head { align-items: flex-start; flex-direction: column; }
            .panel-meta { text-align: left; }
        }

        @media (max-width: 520px) {
            .exec-grid { grid-template-columns: 1fr; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


@st.cache_data(ttl=3600)
def load_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, dict]:
    predictions = pd.read_csv(ROOT / "output" / "predictions_sample.csv")
    segments = pd.read_csv(ROOT / "output" / "segment_summary.csv")
    decisions = pd.read_csv(ROOT / "output" / "decision_summary.csv")
    ages = pd.read_csv(ROOT / "output" / "age_summary.csv")
    model_summary = json.loads((ROOT / "output" / "model_summary.json").read_text())
    return predictions, segments, decisions, ages, model_summary


def fmt_int(value: float) -> str:
    return f"{value:,.0f}"


def fmt_money(value: float) -> str:
    return f"${value:,.0f}"


def fmt_signed_int(value: float) -> str:
    return f"{value:+,.0f}"


def fmt_signed_money(value: float) -> str:
    sign = "+" if value >= 0 else "-"
    return f"{sign}${abs(value):,.0f}"


def fmt_pct(value: float) -> str:
    return f"{value * 100:.1f}%"


def product_label(value: str) -> str:
    return PRODUCT_LABELS.get(str(value), str(value))


def policy_label(value: str) -> str:
    return f"Group {value}"


def channel_label(value: str) -> str:
    return CHANNEL_LABELS.get(str(value), str(value))


def gender_label(value: str) -> str:
    return GENDER_LABELS.get(str(value), str(value))


def business_feature_label(value: str) -> str:
    return FEATURE_LABELS.get(str(value), str(value).replace("_", " ").title())


def action_chip(action: str) -> str:
    css = action.lower()
    return (
        f'<span class="action-chip chip-{css}">'
        f"{ACTION_LABELS.get(action, action)}</span>"
    )


def panel_header(title: str, meta: str = "") -> None:
    st.markdown(
        f"""
        <div class="panel-head">
            <div class="panel-title">{title}</div>
            <div class="panel-meta">{meta}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def kpi_card(label: str, value: str, delta: str) -> None:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-delta">{delta}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def segment_cards(segment_frame: pd.DataFrame, limit: int = 5) -> None:
    ranked = segment_frame.sort_values(
        ["lapse_rate", "loss_ratio", "count"],
        ascending=[False, False, False],
    ).head(limit)

    if ranked.empty:
        st.info("No segments match the current filters.")
        return

    for idx, row in enumerate(ranked.itertuples(index=False), start=1):
        label = f"{product_label(row.type_product)} · {policy_label(row.type_policy_dg)}"
        action = "REVIEW_PRICING" if row.loss_ratio > 1 else "RETAIN_HIGH"
        if row.lapse_rate < 0.08 and row.loss_ratio < 0.8:
            action = "STANDARD"
        elif row.loss_ratio > 2:
            action = "EARLY_RISK"

        st.markdown(
            f"""
            <div class="segment-card">
                <div style="display:flex;justify-content:space-between;gap:10px;align-items:flex-start;">
                    <div class="segment-name">#{idx:02d} {label}</div>
                    {action_chip(action)}
                </div>
                <div class="segment-grid">
                    <div><div class="mini-label">Members</div><div class="mini-value">{fmt_int(row.count)}</div></div>
                    <div><div class="mini-label">Lapse</div><div class="mini-value">{row.lapse_rate * 100:.1f}%</div></div>
                    <div><div class="mini-label">Claim</div><div class="mini-value">{fmt_money(row.avg_claim)}</div></div>
                    <div><div class="mini-label">Loss ratio</div><div class="mini-value">{row.loss_ratio:.2f}</div></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def empty_filter_guard(frame: pd.DataFrame) -> None:
    if frame.empty:
        st.warning("No records match the current filters. Loosen the filters above.")
        st.stop()


add_css()
df, seg_summary, decision_summary, age_summary, model_summary = load_data()

st.markdown(
    """
    <div class="topbar">
        <div class="brand">
            <span class="brand-mark">PA</span>
            <div>
                <div class="brand-title">Insurance Outcome Intelligence</div>
                <div class="brand-subtitle">Portfolio risk and retention outlook</div>
            </div>
        </div>
        <span class="live-pill">Q3 view</span>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.expander("Filters", expanded=False):
    product_options = sorted(df["type_product"].dropna().unique())
    policy_options = sorted(df["type_policy_dg"].dropna().unique())
    channel_options = sorted(df["distribution_channel"].dropna().unique())
    gender_options = sorted(df["gender"].dropna().unique())

    f1, f2, f3, f4 = st.columns(4)
    with f1:
        products = st.multiselect(
            "Product",
            product_options,
            default=product_options,
            format_func=product_label,
        )
    with f2:
        policies = st.multiselect(
            "Policy type",
            policy_options,
            default=policy_options,
            format_func=policy_label,
        )
    with f3:
        channels = st.multiselect(
            "Channel",
            channel_options,
            default=channel_options,
            format_func=channel_label,
        )
    with f4:
        genders = st.multiselect(
            "Gender",
            gender_options,
            default=gender_options,
            format_func=gender_label,
        )

    r1, r2, r3 = st.columns([1.4, 1, 1])
    with r1:
        age_range = st.slider(
            "Age range",
            int(df["age"].min()),
            int(df["age"].max()),
            (int(df["age"].min()), int(df["age"].max())),
        )
    with r2:
        lapse_percentile = st.slider("High lapse percentile", 50, 95, 75, 1)
    with r3:
        top_n = st.slider("Rows in action list", 10, 500, 75, 5)

mask = (
    df["type_product"].isin(products)
    & df["type_policy_dg"].isin(policies)
    & df["distribution_channel"].isin(channels)
    & df["gender"].isin(genders)
    & df["age"].between(age_range[0], age_range[1])
)
filtered = df.loc[mask].copy()
empty_filter_guard(filtered)
filtered["expected_claim_cost"] = filtered["predicted_claim_cost"].clip(lower=0)
filtered["product_display"] = filtered["type_product"].map(product_label)
filtered["policy_display"] = filtered["type_policy_dg"].map(policy_label)
filtered["channel_display"] = filtered["distribution_channel"].map(channel_label)
filtered["gender_display"] = filtered["gender"].map(gender_label)
portfolio_view = filtered.copy()

action_options = ["ALL"] + [a for a in ACTION_LABELS if a != "ALL" and a in df["decision_action"].unique()]
retain_view = portfolio_view[portfolio_view["decision_action"] == "RETAIN_HIGH"]
early_view = portfolio_view[portfolio_view["decision_action"] == "EARLY_RISK"]
pricing_segments = seg_summary[
    seg_summary["type_product"].isin(products)
    & seg_summary["type_policy_dg"].isin(policies)
    & (seg_summary["loss_ratio"] > 1)
]
priority_records = retain_view.shape[0] + early_view.shape[0]
retention_premium = retain_view["premium"].sum()
early_expected_claim = early_view["expected_claim_cost"].sum()
pricing_count = pricing_segments.shape[0]
if pricing_count == 1:
    pricing_note = "One segment should move to pricing review."
elif pricing_count > 1:
    pricing_note = f"{fmt_int(pricing_count)} segments should move to pricing review."
else:
    pricing_note = "No selected segment currently needs pricing review."

st.markdown('<div class="page-kicker">Q3 2026 portfolio review</div>', unsafe_allow_html=True)
st.markdown('<h1 class="page-title">Protect revenue and reduce claim exposure</h1>', unsafe_allow_html=True)
st.markdown(
    f"""
    <p class="page-copy">
    {fmt_int(filtered["ID_policy"].nunique())} policies in view ·
    {fmt_int(filtered.shape[0])} customers evaluated · actions prioritized by expected financial impact.
    </p>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div class="exec-brief">
        <div class="exec-eyebrow">Current exposure</div>
        <div class="exec-title">Protect {fmt_money(retention_premium)} in premium at risk while addressing {fmt_money(early_expected_claim)} in expected claim exposure.</div>
        <div class="exec-copy">
        Start with {fmt_int(priority_records)} priority customers:
        {fmt_int(retain_view.shape[0])} profitable customers likely to lapse and {fmt_int(early_view.shape[0])}
        high-claim-risk customers for early intervention. {pricing_note}
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div class="exec-grid">
        <div class="exec-card">
            <div class="exec-label">First wave</div>
            <div class="exec-value">Focused outreach</div>
            <div class="exec-note">Direct retention spend to customers with the clearest business upside.</div>
        </div>
        <div class="exec-card">
            <div class="exec-label">Premium at risk</div>
            <div class="exec-value">{fmt_money(retention_premium)}</div>
            <div class="exec-note">{fmt_int(retain_view.shape[0])} profitable customers likely to lapse.</div>
        </div>
        <div class="exec-card">
            <div class="exec-label">Claim exposure</div>
            <div class="exec-value">{fmt_money(early_expected_claim)}</div>
            <div class="exec-note">{fmt_int(early_view.shape[0])} customers flagged for early intervention.</div>
        </div>
        <div class="exec-card">
            <div class="exec-label">Confidence</div>
            <div class="exec-value">Use for sequencing</div>
            <div class="exec-note">The ranking supports outreach and intervention order.</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

k1, k2, k3, k4 = st.columns(4)
book_lapse = df["lapse_probability"].mean()
book_loss = df["loss_ratio"].mean()
with k1:
    kpi_card("Policies viewed", fmt_int(filtered["ID_policy"].nunique()), f"{fmt_int(df['ID_policy'].nunique())} total policies")
with k2:
    kpi_card("Avg lapse risk", fmt_pct(filtered["lapse_probability"].mean()), f"{(filtered['lapse_probability'].mean() - book_lapse) * 100:+.1f} pp vs book")
with k3:
    kpi_card(
        "Expected claim",
        fmt_money(filtered["expected_claim_cost"].mean()),
        f"{fmt_money(df['predicted_claim_cost'].clip(lower=0).mean())} book avg",
    )
with k4:
    kpi_card("Loss ratio", f"{filtered['loss_ratio'].mean():.2f}", f"{filtered['loss_ratio'].mean() - book_loss:+.2f} vs book")

selected_action = st.radio(
    "Action category",
    action_options,
    format_func=lambda value: ACTION_LABELS.get(value, value),
    horizontal=True,
    label_visibility="collapsed",
)

if selected_action != "ALL":
    filtered = filtered[filtered["decision_action"] == selected_action].copy()
empty_filter_guard(filtered)
filtered["action_label"] = (
    filtered["decision_action"].map(PLOT_ACTION_LABELS).fillna(filtered["decision_action"])
)

left, right = st.columns([1.35, 1])

with left:
    panel_header("Lapse risk vs claim exposure", "each point is one customer")
    threshold = filtered["lapse_probability"].quantile(lapse_percentile / 100)
    cost_median = filtered["expected_claim_cost"].median()

    plot_sample = filtered.sort_values("lapse_probability", ascending=False).head(5000)
    fig = px.scatter(
        plot_sample,
        x="expected_claim_cost",
        y="lapse_probability",
        color="action_label",
        size="premium",
        size_max=18,
        color_discrete_map=PLOT_ACTION_COLORS,
        hover_data={
            "ID": True,
            "age": True,
            "product_display": True,
            "policy_display": True,
            "premium": ":$,.0f",
            "expected_claim_cost": ":$,.0f",
            "lapse_probability": ":.1%",
            "loss_ratio": ":.2f",
            "action_label": False,
            "decision_action": False,
        },
        labels={
            "expected_claim_cost": "Expected claim cost",
            "lapse_probability": "Lapse risk",
            "action_label": "Action",
            "product_display": "Product",
            "policy_display": "Policy group",
        },
    )
    fig.add_vline(x=cost_median, line_dash="dash", line_color="#8a949b")
    fig.add_hline(y=threshold, line_dash="dash", line_color="#8a949b")
    fig.update_layout(
        height=420,
        margin=dict(l=10, r=10, t=5, b=10),
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        font=dict(family="Inter Tight, Arial", color="#29363c", size=14),
    )
    fig.update_xaxes(gridcolor="#e8eae5", title_font=dict(size=15), tickfont=dict(size=13, color="#46565e"))
    fig.update_yaxes(gridcolor="#e8eae5", tickformat=".0%", title_font=dict(size=15), tickfont=dict(size=13, color="#46565e"))
    st.plotly_chart(fig, use_container_width=True)

with right:
    panel_header("Work queue split", f"{fmt_int(filtered.shape[0])} records")
    action_counts = (
        filtered["decision_action"]
        .value_counts()
        .rename_axis("decision_action")
        .reset_index(name="count")
    )
    action_counts["action_label"] = action_counts["decision_action"].map(PLOT_ACTION_LABELS)
    fig_mix = px.bar(
        action_counts,
        x="count",
        y="action_label",
        orientation="h",
        color="action_label",
        color_discrete_map=PLOT_ACTION_COLORS,
        labels={"count": "Records", "action_label": ""},
    )
    fig_mix.update_layout(
        height=240,
        showlegend=False,
        margin=dict(l=0, r=5, t=5, b=5),
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        font=dict(family="Inter Tight, Arial", color="#29363c", size=14),
    )
    fig_mix.update_xaxes(gridcolor="#e8eae5", title_font=dict(size=15), tickfont=dict(size=13, color="#46565e"))
    fig_mix.update_yaxes(categoryorder="total ascending", tickfont=dict(size=13, color="#46565e"))
    st.plotly_chart(fig_mix, use_container_width=True)
    for action in action_counts["decision_action"].tolist():
        st.markdown(
            f"{action_chip(action)} "
            f"<span style='color:#5d6970;font-size:13px'>{ACTION_NOTES.get(action, '')}</span>",
            unsafe_allow_html=True,
        )

seg_filtered = seg_summary[
    seg_summary["type_product"].isin(products)
    & seg_summary["type_policy_dg"].isin(policies)
].copy()

rank_col, detail_col = st.columns([1, 1])
with rank_col:
    panel_header("Highest-risk segments", f"{len(seg_filtered)} active segments")
    segment_cards(seg_filtered)

with detail_col:
    panel_header("Segment detail", "sortable by risk and margin")
    segment_table = pd.DataFrame(
        {
            "Product": seg_filtered["type_product"].map(product_label),
            "Policy": seg_filtered["type_policy_dg"].map(policy_label),
            "Members": seg_filtered["count"],
            "Premium": seg_filtered["avg_premium"],
            "Claim": seg_filtered["avg_claim"],
            "Lapse": seg_filtered["lapse_rate"] * 100,
            "Loss": seg_filtered["loss_ratio"],
            "Age": seg_filtered["avg_age"],
        }
    ).sort_values(["Lapse", "Loss", "Members"], ascending=[False, False, False])
    st.dataframe(
        segment_table,
        column_config={
            "Members": st.column_config.NumberColumn("Members", format="%d"),
            "Premium": st.column_config.NumberColumn("Premium", format="$%d"),
            "Claim": st.column_config.NumberColumn("Claim", format="$%d"),
            "Lapse": st.column_config.NumberColumn("Lapse", format="%.1f%%"),
            "Loss": st.column_config.NumberColumn("Loss", format="%.2f"),
            "Age": st.column_config.NumberColumn("Age", format="%.1f"),
        },
        use_container_width=True,
        hide_index=True,
        height=492,
    )

tab_overview, tab_model, tab_sim, tab_records, tab_appendix = st.tabs(
    ["Portfolio outlook", "Confidence", "Planning", "Action list", "Appendix"]
)

with tab_overview:
    c1, c2 = st.columns(2)
    with c1:
        panel_header("Risk by age group", "selected portfolio")
        fig_age = px.bar(
            age_summary,
            x="age_group",
            y="lapse_rate",
            color="lapse_rate",
            color_continuous_scale="Reds",
            labels={"age_group": "Age group", "lapse_rate": "Lapse rate"},
        )
        fig_age.update_layout(height=330, margin=dict(l=5, r=5, t=5, b=5), showlegend=False)
        fig_age.update_yaxes(tickformat=".0%")
        st.plotly_chart(fig_age, use_container_width=True)
    with c2:
        panel_header("Premium vs claim distribution", "selected portfolio")
        fig_hist = go.Figure()
        fig_hist.add_trace(go.Histogram(x=filtered["premium"], name="Premium", opacity=0.72, marker_color="#315f86"))
        fig_hist.add_trace(go.Histogram(x=filtered["expected_claim_cost"], name="Expected claim", opacity=0.62, marker_color="#b9484a"))
        fig_hist.update_layout(
            barmode="overlay",
            height=330,
            margin=dict(l=5, r=5, t=5, b=5),
            legend=dict(orientation="h"),
            xaxis_title="Annual amount",
            yaxis_title="Records",
        )
        st.plotly_chart(fig_hist, use_container_width=True)

with tab_model:
    lapse_val = model_summary["lapse_model"]["val"]
    lapse_test = model_summary["lapse_model"]["test"]
    claim_val = model_summary["claim_model"].get("val", model_summary["claim_model"])
    claim_test = model_summary["claim_model"].get("test", claim_val)
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        kpi_card("Risk ranking strength", "Strong", f"{lapse_test['roc_auc']:.3f} score on unseen cases")
    with m2:
        kpi_card("High-risk capture", f"{lapse_test['recall']:.1%}", "coverage of known high-risk cases")
    with m3:
        kpi_card("Claim forecast error", fmt_money(claim_test["rmse"]), f"typical error {fmt_money(claim_test['mae'])}")
    with m4:
        kpi_card("Claim forecast fit", "Moderate", f"{claim_test['r2']:.3f} fit on unseen cases")

    feat_path = ROOT / "output" / "feature_importance.csv"
    if feat_path.exists():
        feat = pd.read_csv(feat_path).head(15).sort_values("importance")
        feat["Driver"] = feat["feature"].map(business_feature_label)
        fig_feat = px.bar(feat, x="importance", y="Driver", orientation="h", color_discrete_sequence=["#2f6f67"])
        fig_feat.update_layout(height=420, margin=dict(l=5, r=5, t=10, b=5), yaxis_title="", xaxis_title="Driver strength")
        st.plotly_chart(fig_feat, use_container_width=True)

with tab_sim:
    sim_l, sim_r = st.columns(2)
    with sim_l:
        premium_change = st.slider("Premium change", -20, 20, 0, 1, format="%d%%")
    with sim_r:
        retention_lift = st.slider("Retention lift", 0, 30, 5, 1, format="%d%%")

    sim = filtered.copy()
    sim["sim_premium"] = sim["premium"] * (1 + premium_change / 100)
    sim["sim_lapse_probability"] = sim["lapse_probability"] * (1 - retention_lift / 100)
    sim["sim_underpriced"] = sim["sim_premium"] < (sim["expected_claim_cost"] * 0.8)
    sim["sim_profitable"] = sim["sim_premium"] > sim["expected_claim_cost"]
    sim_threshold = filtered["lapse_probability"].quantile(lapse_percentile / 100)

    def sim_action(row: pd.Series) -> str:
        high_lapse = row["sim_lapse_probability"] >= sim_threshold
        if high_lapse and row["sim_profitable"]:
            return "RETAIN_HIGH"
        if row["sim_underpriced"] and row["sim_profitable"]:
            return "REVIEW_PRICING"
        if row["sim_underpriced"] and not row["sim_profitable"]:
            return "EARLY_RISK"
        if high_lapse and not row["sim_profitable"]:
            return "LOW_PRIORITY"
        return "STANDARD"

    sim["sim_action"] = sim.apply(sim_action, axis=1)
    before = sim["decision_action"].value_counts()
    after = sim["sim_action"].value_counts()
    action_order = sorted(set(before.index) | set(after.index))
    impact = pd.DataFrame(
        {
            "Action": action_order,
            "Before": [before.get(a, 0) for a in action_order],
            "After": [after.get(a, 0) for a in action_order],
            "Change": [after.get(a, 0) - before.get(a, 0) for a in action_order],
        }
    )
    impact["Action"] = impact["Action"].map(PLOT_ACTION_LABELS).fillna(impact["Action"])

    rev_before = sim["premium"].sum()
    rev_after = sim["sim_premium"].sum()
    profit_before = rev_before - sim["expected_claim_cost"].sum()
    profit_after = rev_after - sim["expected_claim_cost"].sum()

    standard_change = after.get("STANDARD", 0) - before.get("STANDARD", 0)
    retain_change = after.get("RETAIN_HIGH", 0) - before.get("RETAIN_HIGH", 0)
    s1, s2, s3 = st.columns(3)
    with s1:
        kpi_card("Standard queue change", fmt_signed_int(standard_change), "customers moving out of priority queues")
    with s2:
        kpi_card("Retain queue change", fmt_signed_int(retain_change), "profitable high-lapse customers")
    with s3:
        kpi_card("Profit impact", fmt_signed_money(profit_after - profit_before), f"{premium_change:+d}% premium move")

    impact_long = impact.melt(
        id_vars="Action",
        value_vars=["Before", "After"],
        var_name="Scenario",
        value_name="Records",
    )
    change_labels = impact.set_index("Action")["Change"].to_dict()
    impact_long["Bar label"] = impact_long.apply(
        lambda row: f"{row['Records']:,.0f}<br>{fmt_signed_int(change_labels[row['Action']])}"
        if row["Scenario"] == "After"
        else f"{row['Records']:,.0f}<br>base",
        axis=1,
    )
    fig_impact = px.bar(
        impact_long,
        x="Action",
        y="Records",
        color="Scenario",
        text="Bar label",
        barmode="group",
        labels={"Action": "Action", "Records": "Records"},
        color_discrete_map={"Before": "#cfd6d8", "After": "#146c94"},
    )
    planning_axis_records = max(int(before.max()) if not before.empty else 1, 1)
    planning_axis_max = max(16000, ((planning_axis_records * 115 + 99999) // 100000) * 1000)
    fig_impact.update_layout(
        height=360,
        margin=dict(l=5, r=5, t=10, b=5),
        yaxis=dict(range=[0, planning_axis_max], tickmode="linear", dtick=2000),
    )
    fig_impact.update_traces(texttemplate="%{text}", textposition="outside", cliponaxis=False)
    st.plotly_chart(fig_impact, use_container_width=True)

    f1, f2, f3 = st.columns(3)
    with f1:
        kpi_card("Revenue impact", fmt_signed_money(rev_after - rev_before), f"{premium_change:+d}% premium move")
    with f2:
        kpi_card("Profit impact", fmt_signed_money(profit_after - profit_before), f"{fmt_money(profit_after)} simulated")
    with f3:
        kpi_card("Avg lapse after lift", fmt_pct(sim["sim_lapse_probability"].mean()), f"{retention_lift}% retention lift")

with tab_records:
    panel_header("Priority action list", f"top {top_n} by lapse risk")
    records = filtered.sort_values("lapse_probability", ascending=False).head(top_n).copy()
    records_display = pd.DataFrame(
        {
            "Customer": records["ID"],
            "Age": records["age"],
            "Gender": records["gender_display"],
            "Product": records["product_display"],
            "Policy": records["policy_display"],
            "Premium": records["premium"],
            "Expected claim": records["expected_claim_cost"],
            "Lapse risk": records["lapse_probability"] * 100,
            "Loss": records["loss_ratio"],
            "Action": records["decision_action"].map(ACTION_LABELS),
        }
    )
    st.dataframe(
        records_display,
        column_config={
            "Premium": st.column_config.NumberColumn("Premium", format="$%d"),
            "Expected claim": st.column_config.NumberColumn("Expected claim", format="$%d"),
            "Lapse risk": st.column_config.NumberColumn("Lapse risk", format="%.1f%%"),
            "Loss": st.column_config.NumberColumn("Loss", format="%.2f"),
        },
        use_container_width=True,
        hide_index=True,
    )

with tab_appendix:
    st.markdown(
        "Deeper diagnostics for review. The filters above and action category selection apply here too."
    )

    diag_l, diag_r = st.columns(2)
    with diag_l:
        panel_header("Premium distribution", "filtered portfolio")
        fig_prem = px.histogram(
            filtered,
            x="premium",
            nbins=50,
            color_discrete_sequence=["#315f86"],
            labels={"premium": "Annual premium"},
        )
        fig_prem.update_layout(
            height=320,
            showlegend=False,
            margin=dict(l=5, r=5, t=5, b=5),
            paper_bgcolor="#ffffff",
            plot_bgcolor="#ffffff",
            yaxis_title="Records",
        )
        st.plotly_chart(fig_prem, use_container_width=True)

    with diag_r:
        panel_header("Expected claim distribution", "filtered portfolio")
        fig_claim = px.histogram(
            filtered,
            x="expected_claim_cost",
            nbins=50,
            color_discrete_sequence=["#b9484a"],
            labels={"expected_claim_cost": "Expected claim"},
        )
        fig_claim.update_layout(
            height=320,
            showlegend=False,
            margin=dict(l=5, r=5, t=5, b=5),
            paper_bgcolor="#ffffff",
            plot_bgcolor="#ffffff",
            yaxis_title="Records",
        )
        st.plotly_chart(fig_claim, use_container_width=True)

    seg_l, seg_r = st.columns(2)
    with seg_l:
        panel_header("Lapse by product and policy", "filtered segments")
        seg_diag = seg_filtered.copy()
        seg_diag["Product"] = seg_diag["type_product"].map(product_label)
        seg_diag["Policy"] = seg_diag["type_policy_dg"].map(policy_label)
        fig_lapse = px.bar(
            seg_diag,
            x="Product",
            y="lapse_rate",
            color="Policy",
            barmode="group",
            labels={"lapse_rate": "Lapse rate"},
            color_discrete_sequence=["#315f86", "#b9484a", "#2f6f67", "#c08a2d", "#76629c", "#687780"],
        )
        fig_lapse.update_layout(
            height=340,
            margin=dict(l=5, r=5, t=5, b=5),
            paper_bgcolor="#ffffff",
            plot_bgcolor="#ffffff",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        )
        fig_lapse.update_yaxes(tickformat=".0%")
        st.plotly_chart(fig_lapse, use_container_width=True)

    with seg_r:
        panel_header("Segment heatmap", "average lapse rate")
        heat_data = (
            filtered.groupby(["product_display", "policy_display"], observed=False)
            .agg(lapse_rate=("lapse_probability", "mean"))
            .reset_index()
        )
        pivot = heat_data.pivot(index="product_display", columns="policy_display", values="lapse_rate")
        heat_text = pivot.copy()
        for column in heat_text.columns:
            heat_text[column] = heat_text[column].map(
                lambda value: "" if pd.isna(value) else f"{value:.1%}"
            )
        fig_heat = go.Figure(
            data=go.Heatmap(
                z=pivot.values,
                x=pivot.columns.tolist(),
                y=pivot.index.tolist(),
                text=heat_text.values,
                texttemplate="%{text}",
                colorscale="RdYlGn_r",
                colorbar=dict(title="Lapse"),
            )
        )
        fig_heat.update_layout(
            height=340,
            margin=dict(l=5, r=5, t=5, b=5),
            paper_bgcolor="#ffffff",
            plot_bgcolor="#ffffff",
            xaxis_title="Policy",
            yaxis_title="Product",
        )
        st.plotly_chart(fig_heat, use_container_width=True)

    age_l, age_r = st.columns(2)
    age_diag = (
        filtered.groupby("age_group", observed=False)
        .agg(lapse_rate=("lapse_probability", "mean"), avg_claim=("expected_claim_cost", "mean"))
        .reset_index()
    )
    age_order = age_summary["age_group"].tolist()
    age_diag["age_group"] = pd.Categorical(age_diag["age_group"], categories=age_order, ordered=True)
    age_diag = age_diag.sort_values("age_group")
    with age_l:
        panel_header("Lapse by age group", "filtered portfolio")
        fig_age_lapse = px.bar(
            age_diag,
            x="age_group",
            y="lapse_rate",
            color="lapse_rate",
            color_continuous_scale="Reds",
            labels={"age_group": "Age group", "lapse_rate": "Lapse rate"},
        )
        fig_age_lapse.update_layout(height=320, margin=dict(l=5, r=5, t=5, b=5), showlegend=False)
        fig_age_lapse.update_yaxes(tickformat=".0%")
        st.plotly_chart(fig_age_lapse, use_container_width=True)
    with age_r:
        panel_header("Claim exposure by age group", "filtered portfolio")
        fig_age_claim = px.bar(
            age_diag,
            x="age_group",
            y="avg_claim",
            color="avg_claim",
            color_continuous_scale="Blues",
            labels={"age_group": "Age group", "avg_claim": "Expected claim"},
        )
        fig_age_claim.update_layout(height=320, margin=dict(l=5, r=5, t=5, b=5), showlegend=False)
        st.plotly_chart(fig_age_claim, use_container_width=True)

    panel_header("Work queue detail", "filtered action split")
    action_detail = (
        filtered.groupby("decision_action", observed=False)
        .agg(
            Records=("ID", "count"),
            Premium=("premium", "mean"),
            Claim=("expected_claim_cost", "mean"),
            Lapse=("lapse_probability", "mean"),
            Loss=("loss_ratio", "mean"),
        )
        .reset_index()
    )
    action_detail["Action"] = action_detail["decision_action"].map(ACTION_LABELS)
    action_detail["Portfolio"] = action_detail["Records"] / action_detail["Records"].sum() * 100
    action_detail["Lapse"] = action_detail["Lapse"] * 100
    action_detail["Operating note"] = action_detail["decision_action"].map(ACTION_NOTES)
    action_detail = action_detail[
        ["Action", "Records", "Portfolio", "Premium", "Claim", "Lapse", "Loss", "Operating note"]
    ].sort_values("Records", ascending=False)
    st.dataframe(
        action_detail,
        column_config={
            "Records": st.column_config.NumberColumn("Records", format="%d"),
            "Portfolio": st.column_config.NumberColumn("Portfolio", format="%.1f%%"),
            "Premium": st.column_config.NumberColumn("Premium", format="$%d"),
            "Claim": st.column_config.NumberColumn("Claim", format="$%d"),
            "Lapse": st.column_config.NumberColumn("Lapse", format="%.1f%%"),
            "Loss": st.column_config.NumberColumn("Loss", format="%.2f"),
        },
        use_container_width=True,
        hide_index=True,
    )

    metric_tabs = st.tabs(["Lapse model", "Claim forecast"])
    with metric_tabs[0]:
        lapse_val = model_summary["lapse_model"]["val"]
        lapse_test = model_summary["lapse_model"]["test"]
        v1, v2, v3, v4, v5 = st.columns(5)
        with v1:
            kpi_card("Validation accuracy", f"{lapse_val['accuracy']:.4f}", "lapse classifier")
        with v2:
            kpi_card("Validation precision", f"{lapse_val['precision']:.4f}", "high-risk flag")
        with v3:
            kpi_card("Validation recall", f"{lapse_val['recall']:.4f}", "high-risk coverage")
        with v4:
            kpi_card("Validation F1", f"{lapse_val['f1']:.4f}", "balanced score")
        with v5:
            kpi_card("Test ROC AUC", f"{lapse_test['roc_auc']:.4f}", "unseen cases")

        feat_path = ROOT / "output" / "feature_importance.csv"
        if feat_path.exists():
            feat = pd.read_csv(feat_path).head(15).copy()
            feat["Driver"] = feat["feature"].map(business_feature_label)
            feat_plot = feat.sort_values("importance")
            fig_feat = px.bar(
                feat_plot,
                x="importance",
                y="Driver",
                orientation="h",
                color_discrete_sequence=["#2f6f67"],
                labels={"importance": "Importance", "Driver": ""},
            )
            fig_feat.update_layout(height=420, margin=dict(l=5, r=5, t=10, b=5))
            st.plotly_chart(fig_feat, use_container_width=True)
            st.dataframe(
                feat.rename(columns={"importance": "Importance"})[["Driver", "Importance"]],
                use_container_width=True,
                hide_index=True,
            )

    with metric_tabs[1]:
        claim_val = model_summary["claim_model"].get("val", model_summary["claim_model"])
        claim_test = model_summary["claim_model"].get("test", claim_val)
        c1, c2, c3, c4, c5 = st.columns(5)
        with c1:
            kpi_card("Validation RMSE", fmt_money(claim_val["rmse"]), "claim forecast")
        with c2:
            kpi_card("Validation MAE", fmt_money(claim_val["mae"]), "typical error")
        with c3:
            kpi_card("Validation R²", f"{claim_val['r2']:.4f}", "fit score")
        with c4:
            kpi_card("Validation MAPE", f"{claim_val['mape']:.2f}%", "percent error")
        with c5:
            kpi_card("Test R²", f"{claim_test['r2']:.4f}", "unseen cases")

        claim_feat_path = ROOT / "output" / "claim_feature_importance.csv"
        if claim_feat_path.exists():
            claim_feat = pd.read_csv(claim_feat_path).head(15).copy()
            claim_feat["Driver"] = claim_feat["feature"].map(business_feature_label)
            claim_feat_plot = claim_feat.sort_values("importance")
            fig_claim_feat = px.bar(
                claim_feat_plot,
                x="importance",
                y="Driver",
                orientation="h",
                color_discrete_sequence=["#315f86"],
                labels={"importance": "Importance", "Driver": ""},
            )
            fig_claim_feat.update_layout(height=420, margin=dict(l=5, r=5, t=10, b=5))
            st.plotly_chart(fig_claim_feat, use_container_width=True)
            st.dataframe(
                claim_feat.rename(columns={"importance": "Importance"})[["Driver", "Importance"]],
                use_container_width=True,
                hide_index=True,
            )

    panel_header("Scenario financial detail", "uses the planning controls")
    s1, s2, s3, s4, s5 = st.columns(5)
    with s1:
        kpi_card("Original revenue", fmt_money(rev_before), "filtered portfolio")
    with s2:
        kpi_card("Simulated revenue", fmt_money(rev_after), f"{premium_change:+d}% premium move")
    with s3:
        kpi_card("Original profit", fmt_money(profit_before), "before changes")
    with s4:
        kpi_card("Simulated profit", fmt_money(profit_after), "after changes")
    with s5:
        profit_pct = (profit_after / profit_before - 1) * 100 if profit_before else 0
        kpi_card("Profit change", fmt_signed_money(profit_after - profit_before), f"{profit_pct:+.1f}%")

    panel_header("Filtered risk sample", f"top {top_n} by lapse risk")
    appendix_records = filtered.sort_values("lapse_probability", ascending=False).head(top_n).copy()
    appendix_display = pd.DataFrame(
        {
            "Customer": appendix_records["ID"],
            "Policy": appendix_records["ID_policy"],
            "Age": appendix_records["age"],
            "Gender": appendix_records["gender_display"],
            "Product": appendix_records["product_display"],
            "Policy group": appendix_records["policy_display"],
            "Channel": appendix_records["channel_display"],
            "Premium": appendix_records["premium"],
            "Actual claims": appendix_records["cost_claims_year"],
            "Expected claim": appendix_records["expected_claim_cost"],
            "Lapse risk": appendix_records["lapse_probability"] * 100,
            "Loss": appendix_records["loss_ratio"],
            "Action": appendix_records["decision_action"].map(ACTION_LABELS),
        }
    )
    st.dataframe(
        appendix_display,
        column_config={
            "Premium": st.column_config.NumberColumn("Premium", format="$%d"),
            "Actual claims": st.column_config.NumberColumn("Actual claims", format="$%d"),
            "Expected claim": st.column_config.NumberColumn("Expected claim", format="$%d"),
            "Lapse risk": st.column_config.NumberColumn("Lapse risk", format="%.1f%%"),
            "Loss": st.column_config.NumberColumn("Loss", format="%.2f"),
        },
        use_container_width=True,
        hide_index=True,
    )

st.caption(
    "Insurance Outcome Intelligence | Portfolio planning view."
)
