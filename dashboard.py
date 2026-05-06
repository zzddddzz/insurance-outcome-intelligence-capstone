from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components


APP_ROOT = Path(__file__).resolve().parent
DESIGN_HTML = (
    APP_ROOT
    / "claude_design"
    / "team-54-streamlit-dashboard-redesign"
    / "project"
    / "Portfolio Action Console (offline).html"
)


st.set_page_config(
    page_title="Portfolio Action Console",
    page_icon="PA",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    #MainMenu, header, footer, [data-testid="stToolbar"],
    [data-testid="stDecoration"], [data-testid="stStatusWidget"] {
        display: none !important;
    }

    .stApp {
        background: #f4f5f3;
    }

    .block-container {
        max-width: none;
        padding: 0;
    }

    iframe {
        display: block;
        border: 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if not DESIGN_HTML.exists():
    st.error(f"Claude Design export is missing: {DESIGN_HTML}")
    st.stop()

components.html(DESIGN_HTML.read_text(encoding="utf-8"), height=1180, scrolling=True)
