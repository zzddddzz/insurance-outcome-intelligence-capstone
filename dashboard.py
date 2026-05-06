from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components


APP_ROOT = Path(__file__).resolve().parent
DESIGN_PROJECT = (
    APP_ROOT
    / "claude_design"
    / "team-54-streamlit-dashboard-redesign"
    / "project"
)
JSX_FILES = [
    "atoms.jsx",
    "parts-shell.jsx",
    "parts-mid.jsx",
    "parts-detail.jsx",
    "parts-states.jsx",
    "app-exec.jsx",
    "app-review.jsx",
]


def _read_text(name: str) -> str:
    return (DESIGN_PROJECT / name).read_text(encoding="utf-8")


def _inline_script(source: str, script_type: str = "text/javascript") -> str:
    safe_source = source.replace("</script", "<\\/script")
    type_attr = f' type="{script_type}"' if script_type else ""
    presets = ' data-presets="react"' if script_type == "text/babel" else ""
    return f"<script{type_attr}{presets}>\n{safe_source}\n</script>"


@st.cache_data(show_spinner=False)
def build_design_app_html() -> str:
    tokens = _read_text("tokens.css")
    data_js = _read_text("data.js")
    jsx_bundle = "\n\n".join(_read_text(name) for name in JSX_FILES)

    boot_jsx = """
const ProductionApp = () => {
  const [width, setWidth] = React.useState(window.innerWidth);

  React.useEffect(() => {
    const onResize = () => setWidth(window.innerWidth);
    window.addEventListener('resize', onResize);
    return () => window.removeEventListener('resize', onResize);
  }, []);

  if (width < 760) {
    return (
      <div className="production-root production-root-review">
        <ReviewPane />
      </div>
    );
  }

  return (
    <div className="production-root">
      <ExecDashboard
        withDrawer={width >= 1280}
        initialSelected="S-014"
        compact={width < 1120}
      />
    </div>
  );
};

ReactDOM.createRoot(document.getElementById('root')).render(<ProductionApp />);
"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Portfolio Action Console</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@400;500;600;700&family=Source+Serif+4:opsz,wght@8..60,400;8..60,500;8..60,600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
{tokens}

html, body, #root {{
  width: 100%;
  min-height: 100%;
  margin: 0;
  background: var(--bg-page);
}}

body {{
  overflow: hidden;
}}

.production-root {{
  width: 100%;
  height: 1100px;
  background: var(--bg-page);
  overflow: hidden;
}}

.production-root-review {{
  height: 1180px;
}}

@media (max-width: 759px) {{
  body {{
    overflow: auto;
  }}
}}
</style>
</head>
<body>
<div id="root"></div>
<script src="https://unpkg.com/react@18.3.1/umd/react.development.js"></script>
<script src="https://unpkg.com/react-dom@18.3.1/umd/react-dom.development.js"></script>
<script src="https://unpkg.com/@babel/standalone@7.29.0/babel.min.js"></script>
{_inline_script(data_js)}
{_inline_script(jsx_bundle, "text/babel")}
{_inline_script(boot_jsx, "text/babel")}
</body>
</html>"""


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

if not DESIGN_PROJECT.exists():
    st.error(f"Claude Design export is missing: {DESIGN_PROJECT}")
    st.stop()

components.html(build_design_app_html(), height=1180, scrolling=True)
