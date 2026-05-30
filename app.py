import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import io
import warnings
import base64
from datetime import datetime, timedelta

warnings.filterwarnings("ignore")

# ══════════════════════════════════════════════════════════════
#  PAGE CONFIG
# ══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="DataVision Pro — BI Analytics",
    page_icon="🔷",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════
#  THEME & DESIGN TOKENS
# ══════════════════════════════════════════════════════════════
GOLD    = "#f2c94c"
BLUE    = "#4e9af1"
GREEN   = "#6fcf97"
RED     = "#eb5757"
PURPLE  = "#a78bfa"
ORANGE  = "#f97316"
CYAN    = "#06b6d4"
PINK    = "#ec4899"
TEAL    = "#14b8a6"
INDIGO  = "#818cf8"
BG      = "#0f0f1a"
BG2     = "#141424"
CARD    = "#1e1e35"
CARD2   = "#252545"
BORDER  = "#2a2a48"
TEXT    = "#e2e8f0"
MUTED   = "#94a3b8"

PALETTE = [GOLD, BLUE, GREEN, RED, PURPLE, ORANGE, CYAN, PINK, TEAL, INDIGO,
           "#34d399", "#fb923c", "#60a5fa", "#f472b6", "#a3e635"]

PBI_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color=TEXT, family="Inter, Segoe UI, sans-serif", size=12),
    title_font=dict(color=GOLD, size=14, family="Inter, Segoe UI, sans-serif"),
    legend=dict(bgcolor="rgba(30,30,53,0.9)", bordercolor=BORDER,
                borderwidth=1, font=dict(color=TEXT, size=11)),
    margin=dict(l=45, r=20, t=50, b=45),
    colorway=PALETTE,
    xaxis=dict(gridcolor="#1e1e38", linecolor="#2a2a48",
               tickfont=dict(color=MUTED), zerolinecolor="#2a2a48"),
    yaxis=dict(gridcolor="#1e1e38", linecolor="#2a2a48",
               tickfont=dict(color=MUTED), zerolinecolor="#2a2a48"),
    hoverlabel=dict(bgcolor="#1a1a30", bordercolor=BORDER,
                    font=dict(color=TEXT, size=12)),
)

# ══════════════════════════════════════════════════════════════
#  GLOBAL CSS — FULLY REDESIGNED
# ══════════════════════════════════════════════════════════════
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

* {{ box-sizing: border-box; }}
html, body, [class*="css"] {{
    font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
}}

/* ─── Main background ─── */
.main {{ background: {BG}; color: {TEXT}; }}
.block-container {{ padding: 0.8rem 1.5rem 2rem; max-width: 100%; }}

/* ─── Scrollbar ─── */
::-webkit-scrollbar {{ width: 5px; height: 5px; }}
::-webkit-scrollbar-track {{ background: {BG}; }}
::-webkit-scrollbar-thumb {{ background: #3a3a60; border-radius: 4px; }}
::-webkit-scrollbar-thumb:hover {{ background: #4a4a70; }}

/* ─── Sidebar ─── */
[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, #0c0c18 0%, #12121f 100%);
    border-right: 1px solid {BORDER};
}}
[data-testid="stSidebar"] > div {{ padding-top: 0; }}

/* ─── App header ─── */
.app-header {{
    background: linear-gradient(135deg, #08081a 0%, #12122a 50%, #1a1a38 100%);
    border: 1px solid {BORDER};
    border-top: 3px solid {GOLD};
    padding: 20px 28px;
    border-radius: 14px;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 20px;
    position: relative;
    overflow: hidden;
}}
.app-header::before {{
    content: '';
    position: absolute;
    top: 0; right: 0;
    width: 300px; height: 100%;
    background: radial-gradient(ellipse at top right, rgba(242,201,76,0.06) 0%, transparent 70%);
}}
.app-header-logo {{
    font-size: 2.4rem;
    filter: drop-shadow(0 0 12px rgba(242,201,76,0.4));
}}
.app-header h1 {{
    color: {GOLD};
    font-size: 1.6rem;
    font-weight: 800;
    margin: 0 0 3px;
    letter-spacing: -0.02em;
}}
.app-header p {{ color: {MUTED}; margin: 0; font-size: 0.8rem; }}
.app-header-meta {{
    margin-left: auto;
    text-align: right;
}}
.app-header-meta .badge {{
    background: linear-gradient(135deg, {GOLD}, {ORANGE});
    color: #0f0f1a;
    font-size: 0.6rem;
    font-weight: 800;
    padding: 3px 10px;
    border-radius: 20px;
    letter-spacing: 1.5px;
    text-transform: uppercase;
}}
.app-header-meta .date-str {{
    color: {MUTED};
    font-size: 0.75rem;
    margin-top: 5px;
}}

/* ─── Sidebar logo area ─── */
.sidebar-logo {{
    padding: 20px 16px 16px;
    border-bottom: 1px solid {BORDER};
    margin-bottom: 4px;
}}
.sidebar-logo h2 {{
    color: {GOLD};
    font-size: 1.1rem;
    font-weight: 700;
    margin: 0;
}}
.sidebar-logo span {{
    color: {MUTED};
    font-size: 0.72rem;
}}

/* ─── Plan badge in sidebar ─── */
.plan-card {{
    background: linear-gradient(135deg, {CARD}, {CARD2});
    border: 1px solid {BORDER};
    border-radius: 10px;
    padding: 12px 14px;
    margin: 8px 0;
}}
.plan-free   {{ border-left: 3px solid {MUTED}; }}
.plan-pro    {{ border-left: 3px solid {GOLD}; }}
.plan-biz    {{ border-left: 3px solid {CYAN}; }}
.plan-name   {{ color: {GOLD}; font-weight: 700; font-size: 0.85rem; }}
.plan-detail {{ color: {MUTED}; font-size: 0.72rem; margin-top: 2px; }}

/* ─── Section headers ─── */
.sec-header {{
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 24px 0 14px;
    padding-bottom: 8px;
    border-bottom: 1px solid {BORDER};
}}
.sec-header .icon {{ font-size: 1.1rem; }}
.sec-header .title {{
    color: {GOLD};
    font-size: 0.82rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.5px;
}}
.sec-header .count {{
    background: {CARD2};
    color: {MUTED};
    font-size: 0.68rem;
    padding: 2px 8px;
    border-radius: 10px;
    border: 1px solid {BORDER};
    margin-left: auto;
}}

/* ─── KPI Cards — Premium redesign ─── */
.kpi-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
    gap: 14px;
    margin-bottom: 22px;
}}
.kpi-card {{
    background: linear-gradient(145deg, {CARD}, {CARD2});
    border: 1px solid {BORDER};
    border-radius: 14px;
    padding: 18px 20px;
    position: relative;
    overflow: hidden;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    cursor: default;
}}
.kpi-card::before {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: var(--accent, {GOLD});
    border-radius: 14px 14px 0 0;
}}
.kpi-card::after {{
    content: '';
    position: absolute;
    top: -20px; right: -20px;
    width: 80px; height: 80px;
    border-radius: 50%;
    background: radial-gradient(circle, var(--accent-glow, rgba(242,201,76,0.08)) 0%, transparent 70%);
}}
.kpi-card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 12px 32px rgba(0,0,0,0.5);
    border-color: var(--accent, {GOLD});
}}
.kpi-icon {{ font-size: 1.3rem; margin-bottom: 8px; opacity: 0.9; }}
.kpi-label {{
    color: {MUTED};
    font-size: 0.68rem;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    font-weight: 500;
    margin-bottom: 4px;
}}
.kpi-value {{
    color: #fff;
    font-size: 1.8rem;
    font-weight: 800;
    line-height: 1;
    letter-spacing: -0.03em;
}}
.kpi-sub {{
    color: {MUTED};
    font-size: 0.7rem;
    margin-top: 6px;
    display: flex;
    gap: 6px;
}}
.kpi-sub .up   {{ color: {GREEN}; }}
.kpi-sub .down {{ color: {RED}; }}
.kpi-trend {{
    position: absolute;
    bottom: 14px;
    right: 16px;
    font-size: 0.7rem;
    font-weight: 600;
}}

/* ─── Insight cards — redesigned ─── */
.insight-card {{
    background: {CARD};
    border: 1px solid {BORDER};
    border-left: 3px solid var(--c, {GOLD});
    border-radius: 10px;
    padding: 14px 16px;
    margin-bottom: 10px;
    font-size: 0.84rem;
    color: #cbd5e1;
    display: flex;
    gap: 10px;
    align-items: flex-start;
    transition: background 0.15s;
}}
.insight-card:hover {{ background: {CARD2}; }}
.insight-card .i-icon {{ font-size: 1.1rem; margin-top: 1px; flex-shrink: 0; }}
.insight-card .i-text {{ line-height: 1.5; }}
.insight-card b {{ color: var(--c, {GOLD}); }}

/* ─── Tabs — premium style ─── */
.stTabs [data-baseweb="tab-list"] {{
    background: transparent;
    border-bottom: 2px solid {BORDER};
    gap: 2px;
    padding: 0 0 0 2px;
}}
.stTabs [data-baseweb="tab"] {{
    color: {MUTED};
    font-weight: 500;
    font-size: 0.82rem;
    padding: 10px 18px;
    border-radius: 8px 8px 0 0;
    border: none;
    transition: all 0.15s;
}}
.stTabs [data-baseweb="tab"]:hover {{ color: {TEXT}; background: {CARD}; }}
.stTabs [aria-selected="true"] {{
    color: {GOLD} !important;
    background: {CARD} !important;
    border-bottom: 2px solid {GOLD};
    font-weight: 700 !important;
}}

/* ─── Streamlit metrics ─── */
[data-testid="stMetric"] {{
    background: {CARD};
    padding: 16px;
    border-radius: 12px;
    border: 1px solid {BORDER};
    border-top: 2px solid {GOLD};
    transition: transform 0.15s;
}}
[data-testid="stMetric"]:hover {{ transform: translateY(-2px); }}
[data-testid="stMetricLabel"] {{ color: {MUTED} !important; font-size: 0.7rem !important; text-transform: uppercase; letter-spacing: 1px; }}
[data-testid="stMetricValue"] {{ color: #fff !important; font-size: 1.65rem !important; font-weight: 800 !important; }}
[data-testid="stMetricDelta"]  {{ font-size: 0.8rem !important; }}

/* ─── Widgets ─── */
.stSelectbox label, .stMultiSelect label,
.stSlider label, .stRadio label, .stCheckbox label,
.stTextInput label, .stNumberInput label {{
    color: {TEXT} !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
}}
div[data-baseweb="select"] > div {{
    background: #1a1a2e !important;
    border: 1px solid {BORDER} !important;
    border-radius: 8px !important;
    color: {TEXT} !important;
}}
div[data-baseweb="select"] > div:focus-within {{
    border-color: {GOLD} !important;
    box-shadow: 0 0 0 2px rgba(242,201,76,0.15) !important;
}}
.stTextInput input, .stNumberInput input {{
    background: #1a1a2e !important;
    border: 1px solid {BORDER} !important;
    border-radius: 8px !important;
    color: {TEXT} !important;
    padding: 9px 12px !important;
}}
.stTextInput input:focus, .stNumberInput input:focus {{
    border-color: {GOLD} !important;
    box-shadow: 0 0 0 2px rgba(242,201,76,0.15) !important;
}}
.stDataFrame {{ border: 1px solid {BORDER}; border-radius: 10px; overflow: hidden; }}

/* ─── Buttons — redesigned ─── */
.stButton > button {{
    background: linear-gradient(135deg, {GOLD}, {ORANGE});
    color: #0f0f1a;
    font-weight: 700;
    border: none;
    border-radius: 8px;
    padding: 9px 24px;
    font-size: 0.82rem;
    letter-spacing: 0.02em;
    transition: all 0.2s;
    box-shadow: 0 4px 12px rgba(242,201,76,0.2);
}}
.stButton > button:hover {{
    opacity: 0.9;
    transform: translateY(-2px);
    box-shadow: 0 6px 18px rgba(242,201,76,0.35);
}}
.stButton > button:active {{ transform: translateY(0); }}
.stDownloadButton > button {{
    background: transparent;
    color: {GOLD};
    border: 1px solid {GOLD};
    border-radius: 8px;
    padding: 8px 20px;
    font-size: 0.8rem;
    font-weight: 600;
    transition: all 0.2s;
}}
.stDownloadButton > button:hover {{
    background: rgba(242,201,76,0.1);
    box-shadow: 0 0 12px rgba(242,201,76,0.2);
}}

/* ─── File uploader ─── */
[data-testid="stFileUploader"] {{
    background: #141428;
    border: 2px dashed {BORDER};
    border-radius: 12px;
    padding: 8px;
    transition: border-color 0.2s;
}}
[data-testid="stFileUploader"]:hover {{ border-color: {GOLD}; }}

/* ─── Progress / slider ─── */
.stProgress > div > div > div {{ background: linear-gradient(90deg, {GOLD}, {ORANGE}); }}
[data-testid="stSlider"] > div > div > div > div {{
    background: linear-gradient(90deg, {GOLD}, {ORANGE}) !important;
}}

/* ─── Alert / info boxes ─── */
.stAlert {{ border-radius: 10px; font-size: 0.83rem; border: none !important; }}

/* ─── Quality classes ─── */
.qual-good {{ color: {GREEN}; font-weight: 700; }}
.qual-warn {{ color: {ORANGE}; font-weight: 700; }}
.qual-bad  {{ color: {RED}; font-weight: 700; }}

/* ─── Quality banner ─── */
.quality-banner {{
    background: linear-gradient(135deg, {CARD}, {CARD2});
    border: 1px solid {BORDER};
    border-radius: 14px;
    padding: 20px 24px;
    display: flex;
    align-items: center;
    gap: 24px;
    margin-bottom: 20px;
    position: relative;
    overflow: hidden;
}}
.quality-banner::after {{
    content: '';
    position: absolute;
    right: 0; top: 0; bottom: 0;
    width: 200px;
    background: linear-gradient(to left, rgba(111,207,151,0.04), transparent);
}}
.quality-score-ring {{
    width: 70px; height: 70px;
    border-radius: 50%;
    border: 3px solid var(--qc, {GREEN});
    display: flex; align-items: center; justify-content: center;
    font-size: 1.15rem; font-weight: 800; color: var(--qc, {GREEN});
    flex-shrink: 0;
    background: radial-gradient(circle, rgba(111,207,151,0.08), transparent);
}}
.quality-details {{ flex: 1; }}
.quality-details h3 {{ color: {TEXT}; margin: 0 0 4px; font-size: 0.95rem; font-weight: 600; }}
.quality-details p  {{ color: {MUTED}; margin: 0; font-size: 0.78rem; }}
.quality-pills {{ display: flex; gap: 8px; margin-top: 8px; flex-wrap: wrap; }}
.quality-pill {{
    background: {CARD2};
    border: 1px solid {BORDER};
    border-radius: 20px;
    padding: 3px 10px;
    font-size: 0.68rem;
    color: {MUTED};
}}

/* ─── Welcome / empty state ─── */
.welcome-card {{
    background: linear-gradient(145deg, {CARD}, {CARD2});
    border: 1px solid {BORDER};
    border-radius: 16px;
    padding: 32px 24px;
    text-align: center;
    transition: all 0.2s;
    position: relative;
    overflow: hidden;
}}
.welcome-card::before {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, {GOLD}, transparent);
}}
.welcome-card:hover {{
    border-color: {GOLD};
    box-shadow: 0 8px 28px rgba(242,201,76,0.1);
    transform: translateY(-3px);
}}
.welcome-icon  {{ font-size: 2.6rem; margin-bottom: 12px; }}
.welcome-title {{ color: {GOLD}; font-weight: 700; font-size: 1rem; margin-bottom: 6px; }}
.welcome-desc  {{ color: {MUTED}; font-size: 0.8rem; line-height: 1.5; }}

/* ─── Chart container ─── */
.chart-wrap {{
    background: {CARD};
    border: 1px solid {BORDER};
    border-radius: 12px;
    padding: 4px;
    margin-bottom: 14px;
}}

/* ─── Data table header ─── */
.tbl-header {{
    background: {CARD2};
    border: 1px solid {BORDER};
    border-radius: 10px;
    padding: 10px 16px;
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 8px;
    font-size: 0.8rem;
    color: {MUTED};
}}
.tbl-header b {{ color: {TEXT}; }}

/* ─── Chat UI — improved ─── */
.chat-container {{ display: flex; flex-direction: column; gap: 14px; margin-bottom: 20px; }}
.chat-msg {{ display: flex; align-items: flex-end; gap: 10px; }}
.chat-msg.user {{ flex-direction: row-reverse; }}
.bubble {{
    max-width: 78%;
    padding: 13px 18px;
    border-radius: 18px;
    font-size: 0.87rem;
    line-height: 1.65;
}}
.bubble.user {{
    background: linear-gradient(135deg, {GOLD}, {ORANGE});
    color: #0f0f1a;
    font-weight: 500;
    border-radius: 18px 18px 4px 18px;
    box-shadow: 0 4px 14px rgba(242,201,76,0.25);
}}
.bubble.ai {{
    background: {CARD2};
    color: {TEXT};
    border: 1px solid {BORDER};
    border-radius: 18px 18px 18px 4px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.25);
}}
.bubble.ai b {{ color: {GOLD}; }}
.chat-avatar {{
    width: 30px; height: 30px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 13px;
    flex-shrink: 0;
}}
.chat-avatar.ai   {{ background: {CARD2}; border: 1.5px solid {GOLD}; }}
.chat-avatar.user {{ background: linear-gradient(135deg, {GOLD}, {ORANGE}); color: #0f0f1a; }}
.chat-empty {{
    text-align: center;
    padding: 50px 20px;
    color: {MUTED};
}}
.chat-empty .icon {{ font-size: 3.5rem; margin-bottom: 12px; }}
.chat-empty h3 {{ color: {GOLD}; font-size: 1.05rem; margin: 0 0 8px; }}
.chat-empty p  {{ font-size: 0.83rem; line-height: 1.6; }}

/* ─── Suggestion chips ─── */
.chip-row {{ display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 16px; }}

/* ─── Footer ─── */
.app-footer {{
    text-align: center;
    padding: 20px 0 8px;
    color: #2d2d50;
    font-size: 0.72rem;
    border-top: 1px solid {BORDER};
    margin-top: 24px;
}}

/* ─── Expander ─── */
.streamlit-expanderHeader {{
    background: {CARD} !important;
    border-radius: 8px !important;
    color: {TEXT} !important;
    font-size: 0.82rem !important;
}}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  UTILITY FUNCTIONS (all crash-proof)
# ══════════════════════════════════════════════════════════════
def fmt(n, prefix="", suffix=""):
    try:
        if pd.isna(n): return "—"
    except Exception:
        return str(n)
    try:
        n = float(n)
        if not np.isfinite(n): return str(n)
        if abs(n) >= 1_000_000_000: s = f"{n/1e9:.2f}B"
        elif abs(n) >= 1_000_000:   s = f"{n/1e6:.2f}M"
        elif abs(n) >= 1_000:       s = f"{n/1e3:.1f}K"
        else:
            try:
                s = f"{int(n):,}" if n == int(n) else f"{n:,.2f}"
            except (OverflowError, ValueError):
                s = f"{n:.4g}"
        return f"{prefix}{s}{suffix}"
    except Exception:
        return str(n)

def pct_change(new, old):
    """Return formatted pct change string with arrow."""
    try:
        if old == 0 or pd.isna(old) or pd.isna(new): return ""
        p = (new - old) / abs(old) * 100
        arrow = "▲" if p >= 0 else "▼"
        cls   = "up" if p >= 0 else "down"
        return f'<span class="{cls}">{arrow} {abs(p):.1f}%</span>'
    except Exception:
        return ""

def hex_to_rgba(h, a=0.15):
    h = h.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{a})"

def apply_theme(fig, height=None):
    layout = dict(PBI_LAYOUT)
    if height: layout["height"] = height
    fig.update_layout(**layout)
    return fig

def get_num_cols(df):  return df.select_dtypes(include=np.number).columns.tolist()
def get_cat_cols(df):  return df.select_dtypes(include=["object","category"]).columns.tolist()
def get_date_cols(df):
    return [c for c in df.columns if "datetime" in str(df[c].dtype).lower()]

def detect_and_parse_dates(df):
    for col in df.select_dtypes(include="object").columns:
        if df[col].nunique() > 0.95 * max(len(df), 1): continue
        sample = df[col].dropna().head(200)
        if len(sample) == 0: continue
        try:
            converted = pd.to_datetime(sample, errors="coerce")
            if converted.notna().sum() / max(len(sample), 1) > 0.75:
                df[col] = pd.to_datetime(df[col], errors="coerce")
        except Exception:
            pass
    return df

def safe_read(f):
    name = f.name.lower()
    if name.endswith(".csv"):
        for enc in ["utf-8","utf-8-sig","latin-1","cp1252"]:
            try:
                f.seek(0)
                return {"Sheet1": pd.read_csv(f, encoding=enc, low_memory=False)}
            except Exception:
                continue
        raise ValueError("Cannot decode CSV — try saving as UTF-8.")
    else:
        xls = pd.ExcelFile(f)
        return {s: xls.parse(s) for s in xls.sheet_names}

def safe_groupby(df, group_cols, val_col, agg="sum"):
    group_cols = [c for c in group_cols if c and c in df.columns and c != val_col]
    if not group_cols or val_col not in df.columns:
        return pd.DataFrame(columns=(group_cols or []) + [val_col])
    try:
        tmp = df[group_cols + [val_col]].dropna(subset=group_cols).copy()
        for c in group_cols:
            tmp[c] = tmp[c].astype(str).str.strip()
            tmp = tmp[~tmp[c].isin(["nan", "None", "NaN", ""])]
        if tmp.empty:
            return pd.DataFrame(columns=group_cols + [val_col])
        return tmp.groupby(group_cols, as_index=False, sort=False)[val_col].agg(agg)
    except Exception:
        return pd.DataFrame(columns=group_cols + [val_col])

def detect_outliers_iqr(series):
    q1, q3 = series.quantile(0.25), series.quantile(0.75)
    iqr = q3 - q1
    return (series < q1 - 1.5*iqr) | (series > q3 + 1.5*iqr)

def data_quality_score(df):
    total = df.size
    if total == 0: return 0
    missing_pct = df.isnull().sum().sum() / total
    dup_pct     = df.duplicated().sum() / max(len(df), 1)
    score = 100 - (missing_pct * 60) - (dup_pct * 40)
    return max(0, min(100, score))

def auto_insights(df, num_cols, cat_cols, date_cols):
    insights = []
    try:
        miss = df.isnull().mean()
        bad  = miss[miss > 0.2]
        if len(bad):
            cols_str = ", ".join(f"**{c}** ({miss[c]:.0%})" for c in bad.index[:3])
            insights.append(("⚠️", RED, f"High missing values in: {cols_str}"))
    except Exception: pass
    try:
        dups = int(df.duplicated().sum())
        if dups:
            insights.append(("🔁", ORANGE, f"**{dups:,} duplicate rows** detected ({dups/max(len(df),1):.1%} of data)"))
    except Exception: pass
    for col in num_cols[:4]:
        try:
            s = df[col].dropna()
            if len(s) < 4: continue
            mask  = detect_outliers_iqr(s)
            n_out = int(mask.sum())
            if n_out > 0 and n_out / max(len(df), 1) > 0.02:
                insights.append(("📍", PURPLE, f"**{n_out:,} outliers** in **{col}** (range {fmt(s.min())} → {fmt(s.max())})"))
        except Exception: pass
    for col in num_cols[:4]:
        try:
            sk = float(df[col].skew())
            if pd.isna(sk): continue
            if abs(sk) > 2:
                direction = "right (positive)" if sk > 0 else "left (negative)"
                insights.append(("📈", CYAN, f"**{col}** is heavily skewed {direction} (skew={sk:.1f}) — consider log transform"))
        except Exception: pass
    for col in cat_cols[:2]:
        try:
            vc = df[col].value_counts(normalize=True)
            if len(vc) and vc.iloc[0] > 0.5:
                insights.append(("🏆", GREEN, f"**{str(vc.index[0])}** dominates **{col}** ({vc.iloc[0]:.0%} of rows)"))
        except Exception: pass
    try:
        if len(num_cols) >= 2:
            corr    = df[num_cols].corr()
            arr     = corr.to_numpy().copy()
            np.fill_diagonal(arr, np.nan)
            corr_m  = pd.DataFrame(arr, index=corr.index, columns=corr.columns)
            stacked = corr_m.abs().stack().dropna()
            if len(stacked):
                idx     = stacked.idxmax()
                max_val = float(corr_m.loc[idx])
                if abs(max_val) > 0.7:
                    insights.append(("🔗", BLUE, f"Strong correlation ({max_val:.2f}) between **{idx[0]}** and **{idx[1]}**"))
    except Exception: pass
    if date_cols and num_cols:
        try:
            ts = df[[date_cols[0], num_cols[0]]].dropna().sort_values(date_cols[0])
            if len(ts) > 5:
                first = float(ts[num_cols[0]].iloc[0])
                last  = float(ts[num_cols[0]].iloc[-1])
                pct   = (last - first) / abs(first) * 100 if first != 0 else 0
                arrow = "📈" if pct > 0 else "📉"
                color = GREEN if pct > 0 else RED
                insights.append((arrow, color, f"**{num_cols[0]}** changed **{pct:+.1f}%** from first to last record"))
        except Exception: pass
    if not insights:
        insights.append(("✅", GREEN, "Data looks clean — no major issues detected."))
    return insights


# ══════════════════════════════════════════════════════════════
#  CHART BUILDERS
# ══════════════════════════════════════════════════════════════
def bar(df, x, y, color=None, title="", orientation="v", top_n=None):
    d = df.copy()
    if top_n:
        d = d.nlargest(top_n, y)
    if orientation == "h":
        d = d.sort_values(y)
        fig = px.bar(d, x=y, y=x, color=color, orientation="h",
                     title=title, color_discrete_sequence=PALETTE)
    else:
        fig = px.bar(d, x=x, y=y, color=color, title=title,
                     color_discrete_sequence=PALETTE, barmode="group")
    fig.update_traces(marker_line_width=0)
    return apply_theme(fig)

def line(df, x, y, color=None, title=""):
    fig = px.line(df, x=x, y=y, color=color, title=title,
                  color_discrete_sequence=PALETTE, markers=True)
    fig.update_traces(line_width=2.5, marker_size=5)
    return apply_theme(fig)

def area(df, x, y, color=None, title=""):
    fig = px.area(df, x=x, y=y, color=color, title=title,
                  color_discrete_sequence=PALETTE)
    fig.update_traces(line_width=2)
    return apply_theme(fig)

def donut(df, names, values, title="", hole=0.6):
    top = df.nlargest(10, values) if len(df) > 10 else df
    fig = px.pie(top, names=names, values=values, title=title,
                 hole=hole, color_discrete_sequence=PALETTE)
    fig.update_traces(textinfo="percent+label", textfont_size=11,
                      pull=[0.04] + [0] * (len(top) - 1))
    return apply_theme(fig)

def scatter(df, x, y, color=None, size=None, title="", trendline=False):
    safe_size = None
    if size and size in df.columns:
        if pd.api.types.is_numeric_dtype(df[size]) and df[size].dropna().min() >= 0:
            safe_size = size
    use_trendline = False
    if trendline:
        try:
            import statsmodels  # noqa
            use_trendline = True
        except ImportError:
            pass
    kw = dict(trendline="ols") if use_trendline else {}
    try:
        fig = px.scatter(df, x=x, y=y, color=color, size=safe_size, title=title,
                         color_discrete_sequence=PALETTE, opacity=0.72, **kw)
        if use_trendline:
            fig.update_traces(selector=dict(mode="lines"),
                              line=dict(color=GOLD, width=2, dash="dot"))
    except Exception:
        fig = px.scatter(df, x=x, y=y, color=color, title=title,
                         color_discrete_sequence=PALETTE, opacity=0.72)
    return apply_theme(fig)

def histogram(df, col, bins=30, color_col=None, title=""):
    fig = px.histogram(df, x=col, nbins=bins, color=color_col,
                       title=title, color_discrete_sequence=PALETTE,
                       marginal="box")
    fig.update_traces(marker_line_color=BG, marker_line_width=0.5)
    return apply_theme(fig)

def box_plot(df, y, x=None, title=""):
    fig = px.box(df, x=x, y=y, title=title,
                 color_discrete_sequence=PALETTE, points="outliers")
    fig.update_traces(marker_color=GOLD)
    return apply_theme(fig)

def heatmap_corr(df, num_cols):
    if len(num_cols) < 2: return None
    try:
        corr = df[num_cols].corr().round(2)
        arr  = corr.to_numpy().copy()
        fig  = go.Figure(go.Heatmap(
            z=arr, x=corr.columns.tolist(), y=corr.index.tolist(),
            colorscale=[[0, RED], [0.5, CARD], [1, GREEN]],
            zmin=-1, zmax=1,
            text=arr, texttemplate="%{text:.2f}",
            hoverongaps=False,
        ))
        fig.update_layout(title="Correlation Matrix")
        return apply_theme(fig)
    except Exception:
        return None

def waterfall(df, x_col, y_col, title=""):
    try:
        tmp = df[[x_col, y_col]].dropna().copy()
        tmp[x_col] = tmp[x_col].astype(str)
        d = tmp.groupby(x_col, as_index=False)[y_col].sum()
        d = d.sort_values(y_col, ascending=False).head(12)
        fig = go.Figure(go.Waterfall(
            x=d[x_col], y=d[y_col],
            connector={"line": {"color": BORDER}},
            increasing={"marker": {"color": GREEN}},
            decreasing={"marker": {"color": RED}},
            totals={"marker": {"color": GOLD}},
        ))
        fig.update_layout(title=title)
        return apply_theme(fig)
    except Exception as e:
        return go.Figure().update_layout(title=f"Error: {e}")

def funnel(df, cat_col, val_col, title=""):
    try:
        tmp = df[[cat_col, val_col]].dropna().copy()
        tmp[cat_col] = tmp[cat_col].astype(str)
        d = tmp.groupby(cat_col, as_index=False)[val_col].sum()
        d = d.sort_values(val_col, ascending=False).head(8)
        fig = go.Figure(go.Funnel(
            y=d[cat_col], x=d[val_col],
            marker={"color": PALETTE[:len(d)]},
            textinfo="value+percent total",
        ))
        fig.update_layout(title=title)
        return apply_theme(fig)
    except Exception as e:
        return go.Figure().update_layout(title=f"Error: {e}")

def treemap(df, path_cols, val_col, title=""):
    try:
        tmp = df[path_cols + [val_col]].dropna().copy()
        for c in path_cols:
            tmp[c] = tmp[c].astype(str)
        d   = tmp.groupby(path_cols, as_index=False)[val_col].sum()
        fig = px.treemap(d, path=path_cols, values=val_col, title=title,
                         color_discrete_sequence=PALETTE)
        fig.update_traces(textinfo="label+value+percent parent", root_color=BG)
        return apply_theme(fig)
    except Exception as e:
        return go.Figure().update_layout(title=f"Error: {e}")

def gauge(value, title, max_v=None):
    if pd.isna(value) or value == 0: value = 0
    if max_v is None or max_v == 0: max_v = max(abs(value) * 2, 1)
    pct   = value / max_v
    color = GREEN if pct > 0.66 else (ORANGE if pct > 0.33 else RED)
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        number={"font": {"color": "#fff", "size": 22}, "valueformat": ".2s"},
        gauge=dict(
            axis=dict(range=[0, max_v], tickfont={"color": MUTED},
                      tickformat=".2s", nticks=5),
            bar=dict(color=color, thickness=0.25),
            bgcolor=BG,
            borderwidth=0,
            steps=[
                dict(range=[0, max_v*0.33],  color="#1e1010"),
                dict(range=[max_v*0.33, max_v*0.66], color="#1e1a0e"),
                dict(range=[max_v*0.66, max_v],  color="#0e1e14"),
            ],
        ),
        title=dict(text=title, font=dict(color=MUTED, size=11)),
    ))
    fig.update_layout(height=220, margin=dict(l=20, r=20, t=50, b=10),
                      paper_bgcolor="rgba(0,0,0,0)")
    return fig

def multi_axis_line(df, date_col, metrics):
    n = len(metrics)
    if n == 0: return go.Figure()
    try:
        fig = make_subplots(rows=n, cols=1, shared_xaxes=True,
                            vertical_spacing=0.04,
                            subplot_titles=[f"▸ {m}" for m in metrics])
        for i, m in enumerate(metrics):
            try:
                tmp = df[[date_col, m]].dropna().copy()
                tmp = tmp.sort_values(date_col).groupby(date_col, as_index=False)[m].sum()
                c   = PALETTE[i % len(PALETTE)]
                fig.add_trace(go.Scatter(
                    x=tmp[date_col], y=tmp[m], name=m,
                    line=dict(color=c, width=2.2),
                    fill="tozeroy", fillcolor=hex_to_rgba(c, 0.08),
                    hovertemplate=f"<b>%{{x}}</b><br>{m}: %{{y:,.2f}}<extra></extra>",
                ), row=i+1, col=1)
                if len(tmp) > 6:
                    win  = min(7, max(2, len(tmp)//3))
                    roll = tmp[m].rolling(win, min_periods=1).mean()
                    fig.add_trace(go.Scatter(
                        x=tmp[date_col], y=roll, name=f"{m} ({win}-avg)",
                        line=dict(color=c, width=1, dash="dot"),
                        showlegend=False,
                    ), row=i+1, col=1)
            except Exception:
                continue
        layout = {k: v for k, v in PBI_LAYOUT.items() if k not in ("xaxis","yaxis")}
        fig.update_layout(height=max(200, 220*n), showlegend=True, **layout)
        fig.update_annotations(font=dict(color=GOLD, size=11))
        return fig
    except Exception as e:
        return go.Figure().update_layout(title=f"Time series error: {e}")

def pareto_chart(df, cat_col, val_col, title="Pareto Analysis"):
    try:
        tmp = df[[cat_col, val_col]].dropna().copy()
        tmp[cat_col] = tmp[cat_col].astype(str).str.strip()
        tmp = tmp[~tmp[cat_col].isin(["nan","None",""])]
        d = tmp.groupby(cat_col, as_index=False)[val_col].sum()
        d = d.sort_values(val_col, ascending=False).head(15)
        total = d[val_col].sum()
        if total == 0: return go.Figure().update_layout(title="No data")
        d["cumpct"] = d[val_col].cumsum() / total * 100
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Bar(x=d[cat_col], y=d[val_col], name=val_col,
                             marker_color=BLUE, marker_line_width=0), secondary_y=False)
        fig.add_trace(go.Scatter(x=d[cat_col], y=d["cumpct"], name="Cumulative %",
                                 line=dict(color=GOLD, width=2.5),
                                 mode="lines+markers", marker_size=6), secondary_y=True)
        fig.add_shape(type="line", x0=-0.5, x1=len(d)-0.5, y0=80, y1=80,
                      line=dict(color=RED, width=1.5, dash="dot"),
                      xref="x", yref="y2")
        fig.update_yaxes(title_text=val_col, secondary_y=False,
                         gridcolor="#1e1e38", tickfont=dict(color=MUTED))
        fig.update_yaxes(title_text="Cumulative %", secondary_y=True,
                         range=[0, 108], tickfont=dict(color=GOLD),
                         gridcolor="rgba(0,0,0,0)", ticksuffix="%")
        fig.update_layout(title=title)
        return apply_theme(fig)
    except Exception as e:
        return go.Figure().update_layout(title=f"Pareto Error: {e}")

def missing_heatmap(df):
    miss = df.isnull().astype(int)
    if miss.sum().sum() == 0: return None
    fig = px.imshow(miss.T, title="Missing Value Map",
                    color_continuous_scale=[[0, CARD], [1, RED]],
                    labels=dict(color="Missing"), aspect="auto")
    fig.update_layout(coloraxis_showscale=False)
    return apply_theme(fig, height=max(200, len(df.columns) * 22))

def outlier_scatter(df, col):
    s    = df[col].dropna()
    mask = detect_outliers_iqr(s)
    fig  = go.Figure()
    fig.add_trace(go.Scatter(x=s[~mask].index, y=s[~mask], mode="markers",
                             name="Normal", marker=dict(color=BLUE, size=5, opacity=0.6)))
    fig.add_trace(go.Scatter(x=s[mask].index, y=s[mask], mode="markers",
                             name="Outlier", marker=dict(color=RED, size=8, symbol="x")))
    q1, q3 = s.quantile(0.25), s.quantile(0.75)
    iqr = q3 - q1
    for bound, label, c in [(q1-1.5*iqr,"Lower fence",ORANGE),(q3+1.5*iqr,"Upper fence",ORANGE)]:
        fig.add_hline(y=bound, line_dash="dash", line_color=c,
                      annotation_text=label, annotation_font_color=c)
    fig.update_layout(title=f"Outlier Detection — {col}")
    return apply_theme(fig)

def pivot_heatmap(df, row_col, col_col, val_col):
    try:
        piv = df.pivot_table(values=val_col, index=row_col,
                             columns=col_col, aggfunc="sum", fill_value=0)
        if piv.shape[0] > 30: piv = piv.iloc[:30]
        if piv.shape[1] > 20: piv = piv.iloc[:, :20]
        fig = px.imshow(piv, title=f"{val_col} — {row_col} × {col_col}",
                        color_continuous_scale=[[0, BG], [0.5, BLUE], [1, GOLD]],
                        text_auto=".2s", aspect="auto")
        return apply_theme(fig)
    except Exception as e:
        return go.Figure().update_layout(title=f"Error: {e}")

# ══════════════════════════════════════════════════════════════
#  EXPORT HELPERS
# ══════════════════════════════════════════════════════════════
def to_excel(df):
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as w:
        df.to_excel(w, index=False, sheet_name="Data")
        df.describe().T.to_excel(w, sheet_name="Stats")
    return buf.getvalue()

def to_csv(df):
    return df.to_csv(index=False).encode("utf-8")

def chart_download_btn(fig, filename="chart"):
    html_str = fig.to_html(include_plotlyjs="cdn", full_html=True,
                           config={"displayModeBar": True})
    b64  = base64.b64encode(html_str.encode()).decode()
    href = (f'<a href="data:text/html;base64,{b64}" download="{filename}.html" '
            f'style="color:{GOLD};font-size:0.75rem;text-decoration:none;'
            f'background:{CARD2};padding:5px 14px;border-radius:6px;border:1px solid {BORDER};">'
            f'⬇ Download Chart</a>')
    st.markdown(href, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  SAMPLE DATA
# ══════════════════════════════════════════════════════════════
def generate_sample_data():
    np.random.seed(42)
    n = 300
    regions    = ["North", "South", "East", "West", "Central"]
    products   = ["Laptop", "Phone", "Tablet", "Monitor", "Headphones", "Keyboard"]
    categories = ["Electronics", "Accessories", "Computing"]
    reps       = ["Ahmed", "Sara", "Mohamed", "Fatima", "Omar", "Layla", "Karim"]
    channels   = ["Online", "Retail", "Partner", "Direct"]

    dates = pd.date_range("2023-01-01", periods=n, freq="D")
    np.random.shuffle(dates := dates.tolist())

    df = pd.DataFrame({
        "Date":       dates,
        "Region":     np.random.choice(regions, n),
        "Product":    np.random.choice(products, n),
        "Category":   np.random.choice(categories, n),
        "Sales Rep":  np.random.choice(reps, n),
        "Channel":    np.random.choice(channels, n),
        "Units Sold": np.random.randint(1, 50, n),
        "Unit Price": np.random.choice([299, 599, 999, 149, 79, 49], n),
        "Discount %": np.random.choice([0, 5, 10, 15, 20], n),
        "Revenue":    None,
        "Cost":       None,
        "Profit":     None,
        "Customer Rating": np.round(np.random.uniform(3.0, 5.0, n), 1),
    })
    df["Revenue"] = df["Units Sold"] * df["Unit Price"] * (1 - df["Discount %"] / 100)
    df["Cost"]    = df["Revenue"] * np.random.uniform(0.5, 0.7, n)
    df["Profit"]  = df["Revenue"] - df["Cost"]
    df.loc[np.random.choice(n, 10, replace=False), "Customer Rating"] = np.nan
    df.loc[np.random.choice(n, 5,  replace=False), "Discount %"]      = np.nan
    return df


# ══════════════════════════════════════════════════════════════
#  FORECASTING
# ══════════════════════════════════════════════════════════════
def forecast_series(df, date_col, val_col, periods=30):
    try:
        tmp = df[[date_col, val_col]].dropna().copy()
        tmp = tmp.sort_values(date_col).groupby(date_col, as_index=False)[val_col].sum()
        if len(tmp) < 6:
            return None, "Need at least 6 data points for forecasting.", 0
        t0      = tmp[date_col].min()
        tmp["_t"] = (tmp[date_col] - t0).dt.days.astype(float)
        x, y    = tmp["_t"].values, tmp[val_col].values
        try:
            coeffs = np.polyfit(x, y, deg=min(2, len(x)-1))
            poly   = np.poly1d(coeffs)
        except Exception:
            coeffs = np.polyfit(x, y, deg=1)
            poly   = np.poly1d(coeffs)
        diffs        = tmp[date_col].diff().dropna().dt.days
        freq_days    = max(1, int(diffs.median()))
        last_date    = tmp[date_col].max()
        future_dates = [last_date + timedelta(days=i*freq_days) for i in range(1, periods+1)]
        future_t     = np.array([(d - t0).days for d in future_dates], dtype=float)
        forecast_y   = poly(future_t)
        residuals    = y - poly(x)
        std          = residuals.std()
        hist_df = pd.DataFrame({date_col: tmp[date_col], val_col: y, "type": "Historical"})
        fc_df   = pd.DataFrame({
            date_col: future_dates, val_col: forecast_y,
            "upper": forecast_y + 1.5*std, "lower": forecast_y - 1.5*std,
            "type": "Forecast",
        })
        return hist_df, fc_df, std
    except Exception as e:
        return None, f"Forecast error: {e}", 0

def forecast_chart(hist_df, fc_df, date_col, val_col):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=hist_df[date_col], y=hist_df[val_col],
                             name="Historical", line=dict(color=BLUE, width=2.5),
                             mode="lines"))
    fig.add_trace(go.Scatter(x=fc_df[date_col], y=fc_df[val_col],
                             name="Forecast", line=dict(color=GOLD, width=2.5, dash="dash"),
                             mode="lines+markers", marker_size=5))
    fig.add_trace(go.Scatter(
        x=pd.concat([fc_df[date_col], fc_df[date_col].iloc[::-1]]),
        y=pd.concat([fc_df["upper"], fc_df["lower"].iloc[::-1]]),
        fill="toself", fillcolor=hex_to_rgba(GOLD, 0.1),
        line=dict(color="rgba(0,0,0,0)"), name="95% CI", hoverinfo="skip",
    ))
    split = hist_df[date_col].max()
    fig.add_vline(x=str(split), line_dash="dot", line_color="#4b5563",
                  annotation_text="Forecast Start", annotation_font_color=MUTED)
    fig.update_layout(title=f"📅 {val_col} Forecast — next {len(fc_df)} periods")
    return apply_theme(fig, height=400)


# ══════════════════════════════════════════════════════════════
#  HTML REPORT GENERATOR
# ══════════════════════════════════════════════════════════════
def build_html_report(df, num_cols, cat_cols, date_cols, filename, sheet):
    qs  = data_quality_score(df)
    ins = auto_insights(df, num_cols, cat_cols, date_cols)
    kpi_html, insight_html = "", ""
    for col in num_cols[:6]:
        kpi_html += f"""
        <div class="kpi">
            <div class="kpi-label">{col}</div>
            <div class="kpi-val">{fmt(df[col].sum())}</div>
            <div class="kpi-sub">Avg {fmt(df[col].mean())} · Max {fmt(df[col].max())}</div>
        </div>"""
    for icon, color, text in ins:
        clean = text.replace("**","<b>",1)
        while "**" in clean:
            clean = clean.replace("**","</b>",1).replace("**","<b>",1)
        insight_html += f'<div class="insight" style="border-left:3px solid {color}">{icon} {clean}</div>'
    stats_html = ""
    if num_cols:
        stats = df[num_cols].describe().T.round(2)
        stats["skew"] = df[num_cols].skew().round(2)
        stats_html = stats.to_html(classes="tbl", border=0)
    qcolor = GREEN if qs >= 80 else (ORANGE if qs >= 50 else RED)
    html = f"""<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8">
<title>DataVision Pro Report — {filename}</title>
<style>
  body{{font-family:'Segoe UI',sans-serif;background:#0f0f1a;color:#e2e8f0;margin:0;padding:24px}}
  h1{{color:#f2c94c;border-bottom:2px solid #f2c94c;padding-bottom:10px;font-size:1.5rem}}
  h2{{color:#f2c94c;font-size:0.85rem;text-transform:uppercase;letter-spacing:1.5px;
      border-left:3px solid #f2c94c;padding-left:10px;margin:28px 0 12px}}
  .meta{{color:#94a3b8;font-size:0.78rem;margin-bottom:20px;background:#1e1e35;
         padding:10px 16px;border-radius:8px;border:1px solid #2a2a48}}
  .kpis{{display:flex;flex-wrap:wrap;gap:14px;margin-bottom:20px}}
  .kpi{{background:#1e1e35;border-radius:12px;padding:16px 20px;
        border-top:3px solid #f2c94c;min-width:150px;flex:1;border:1px solid #2a2a48}}
  .kpi-label{{color:#94a3b8;font-size:0.68rem;text-transform:uppercase;letter-spacing:1px}}
  .kpi-val{{color:#fff;font-size:1.7rem;font-weight:800}}
  .kpi-sub{{color:#6b7280;font-size:0.7rem;margin-top:4px}}
  .insight{{background:#1e1e35;border-radius:8px;padding:12px 14px;
            margin-bottom:8px;font-size:0.83rem;color:#cbd5e1;border:1px solid #2a2a48}}
  .insight b{{color:#f2c94c}}
  .badge{{background:#f2c94c;color:#0f0f1a;font-size:0.6rem;font-weight:800;
           padding:2px 8px;border-radius:20px;letter-spacing:1.5px}}
  .qs{{font-size:1.5rem;font-weight:800;color:{qcolor}}}
  .tbl{{width:100%;border-collapse:collapse;font-size:0.8rem;margin-top:8px}}
  .tbl th{{background:#1e1e35;color:#f2c94c;padding:9px 10px;text-align:left;
           border-bottom:1px solid #2a2a48;font-size:0.72rem;text-transform:uppercase;letter-spacing:0.8px}}
  .tbl td{{padding:8px 10px;border-bottom:1px solid #1a1a2e;color:#cbd5e1}}
  .tbl tr:hover td{{background:#1e1e35}}
  footer{{color:#374151;font-size:0.72rem;text-align:center;
          margin-top:40px;border-top:1px solid #2a2a48;padding-top:16px}}
</style></head><body>
<h1>🔷 DataVision Pro <span class="badge">REPORT</span></h1>
<div class="meta">
  File: <b>{filename}</b> · Sheet: <b>{sheet}</b> ·
  {len(df):,} rows · {len(df.columns)} columns ·
  Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}
</div>
<h2>Data Quality</h2>
<div class="qs">{qs:.0f}/100</div>
<div style="color:#94a3b8;font-size:0.8rem;margin-top:4px">
  Missing: {df.isnull().mean().mean()*100:.1f}% · Duplicates: {df.duplicated().sum()} ·
  Numeric cols: {len(num_cols)} · Categorical: {len(cat_cols)}
</div>
<h2>KPI Summary</h2>
<div class="kpis">{kpi_html}</div>
<h2>Auto Insights</h2>{insight_html}
<h2>Statistical Summary</h2>{stats_html}
<footer>DataVision Pro · Expert Edition · {datetime.now().year}</footer>
</body></html>"""
    return html.encode("utf-8")


# ══════════════════════════════════════════════════════════════
#  HELPER: section header
# ══════════════════════════════════════════════════════════════
def sec(icon, title, count=None):
    count_html = f'<span class="count">{count}</span>' if count else ""
    st.markdown(f"""
    <div class="sec-header">
        <span class="icon">{icon}</span>
        <span class="title">{title}</span>
        {count_html}
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown(f"""
    <div class="sidebar-logo">
        <h2>🔷 DataVision Pro</h2>
        <span>Enterprise Analytics Platform</span>
    </div>
    """, unsafe_allow_html=True)

    # Plan selector
    st.markdown("##### 💎 Your Plan")
    plan = st.radio("", ["🆓 Free", "⭐ Pro", "🏢 Business"],
                    index=1, label_visibility="collapsed", key="plan_sel")
    PLAN      = plan.split()[-1]
    ROW_LIMIT = {"Free": 300, "Pro": 10_000, "Business": 9_999_999}[PLAN]

    plan_details = {
        "Free": ("plan-free", "300 rows · Basic charts", "Upgrade for AI Chat & Forecasting"),
        "Pro":  ("plan-pro",  "10K rows · AI Chat · Forecasting", "Most popular for analysts"),
        "Business": ("plan-biz", "Unlimited rows · All features", "Full enterprise access"),
    }
    pcls, plimit, pdesc = plan_details[PLAN]
    st.markdown(f"""
    <div class="plan-card {pcls}">
        <div class="plan-name">{PLAN} Plan</div>
        <div class="plan-detail">{plimit}</div>
        <div class="plan-detail" style="color:#6b7280;margin-top:2px">{pdesc}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    uploaded = st.file_uploader("📁 Upload Dataset", type=["csv", "xlsx"],
                                help="CSV or Excel — multi-sheet supported")

    use_sample = False
    if uploaded is None:
        if st.button("🎯 Load Demo Dataset", use_container_width=True, key="sample_btn"):
            use_sample = True
        st.caption("No file? Load a demo sales dataset to explore features.")

    st.markdown("---")
    st.markdown("##### ⚙️ Display Settings")
    top_n_global = st.slider("Max categories shown", 5, 30, 12)
    show_raw     = st.checkbox("Show values on bar charts", False)

    st.markdown("---")
    st.caption("DataVision Pro v2.0 · Expert Edition")


# ══════════════════════════════════════════════════════════════
#  HEADER
# ══════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="app-header">
    <div class="app-header-logo">🔷</div>
    <div>
        <h1>DataVision Pro <span style="font-size:0.6rem;background:linear-gradient(135deg,{GOLD},{ORANGE});
            color:#0f0f1a;padding:2px 8px;border-radius:20px;vertical-align:middle;
            font-weight:800;letter-spacing:1.5px;text-transform:uppercase">EXPERT</span></h1>
        <p>Power BI-Style Analytics &nbsp;·&nbsp; Upload CSV / Excel to begin</p>
    </div>
    <div class="app-header-meta">
        <div class="date-str">{datetime.now().strftime("%A, %d %B %Y")}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  EMPTY STATE
# ══════════════════════════════════════════════════════════════
if uploaded is None and not use_sample:
    features = [
        ("📂", "Upload Any File", "CSV or Excel with single or multiple sheets"),
        ("🤖", "AI-Powered Analysis", "Instant KPIs, trends, and intelligent insights"),
        ("📊", "15+ Chart Types", "Bars, lines, scatter, treemaps, forecasting & more"),
        ("🧹", "Data Cleaning", "Remove duplicates, fill missing values, rename columns"),
        ("🔮", "Forecasting", "Polynomial time-series forecasting with confidence bands"),
        ("📤", "Export Everything", "CSV, Excel, HTML report, and interactive charts"),
    ]
    r1, r2, r3 = st.columns(3)
    r4, r5, r6 = st.columns(3)
    cols = [r1, r2, r3, r4, r5, r6]
    for i, (icon, title, desc) in enumerate(features):
        with cols[i]:
            st.markdown(f"""
            <div class="welcome-card">
                <div class="welcome-icon">{icon}</div>
                <div class="welcome-title">{title}</div>
                <div class="welcome-desc">{desc}</div>
            </div>""", unsafe_allow_html=True)
    st.markdown(f"""
    <div style='text-align:center;padding:32px;color:{MUTED};font-size:0.85rem;'>
        ← Upload a file in the sidebar or click
        <b style='color:{GOLD}'>Load Demo Dataset</b> to explore
    </div>""", unsafe_allow_html=True)
    st.stop()


# ══════════════════════════════════════════════════════════════
#  LOAD DATA
# ══════════════════════════════════════════════════════════════
@st.cache_data(show_spinner="📊 Loading data…", ttl=3600)
def load_data(file_bytes: bytes, file_name: str):
    import io as _io
    buf      = _io.BytesIO(file_bytes)
    buf.name = file_name
    sheets   = safe_read(buf)
    for k in sheets:
        sheets[k] = detect_and_parse_dates(sheets[k])
    return sheets

if use_sample:
    df_raw     = generate_sample_data()
    df_raw     = detect_and_parse_dates(df_raw)
    sheet_name = "Sample Sales Data"
    sheets     = {sheet_name: df_raw}
    st.info("📊 **Demo mode** — 300-row sales dataset loaded. Upload your own CSV/Excel to analyze real data.")
else:
    try:
        file_bytes = uploaded.read()
        sheets = load_data(file_bytes, uploaded.name)
    except Exception as e:
        st.error(f"❌ **File read error:** {e}")
        st.info("Try re-saving as CSV UTF-8, or check for empty sheets.")
        st.stop()

sheet_names = list(sheets.keys())
sheet_name  = sheet_names[0] if not use_sample else sheet_name
if len(sheet_names) > 1:
    with st.sidebar:
        st.markdown("##### 📑 Sheet")
        sheet_name = st.selectbox("Select sheet", sheet_names)

df_raw = sheets[sheet_name].copy()
df_raw = df_raw.dropna(how="all").dropna(axis=1, how="all")
df_raw.columns = [str(c).strip() for c in df_raw.columns]

if len(df_raw) > ROW_LIMIT:
    st.warning(f"⚠️ **{PLAN} plan limit:** Your file has **{len(df_raw):,} rows** but plan allows **{ROW_LIMIT:,}**. Showing first {ROW_LIMIT:,} rows.")
    df_raw = df_raw.head(ROW_LIMIT)

num_cols  = get_num_cols(df_raw)
cat_cols  = get_cat_cols(df_raw)
date_cols = get_date_cols(df_raw)

# ══════════════════════════════════════════════════════════════
#  SIDEBAR FILTERS
# ══════════════════════════════════════════════════════════════
df = df_raw.copy()
with st.sidebar:
    st.markdown("---")
    st.markdown("##### 🔍 Filters")
    active_filters = 0
    for col in cat_cols[:5]:
        opts = sorted(df_raw[col].dropna().astype(str).unique().tolist())
        if 2 <= len(opts) <= 40:
            sel = st.multiselect(col, opts, default=opts, key=f"f_{col}")
            if sel and len(sel) < len(opts):
                df = df[df[col].astype(str).isin(sel)]
                active_filters += 1
    if date_cols:
        dc = date_cols[0]
        try:
            mn = df_raw[dc].min().date()
            mx = df_raw[dc].max().date()
            dr = st.date_input("Date range", value=[mn, mx], key="daterange")
            if len(dr) == 2 and (dr[0] != mn or dr[1] != mx):
                df = df[(df[dc] >= pd.Timestamp(dr[0])) & (df[dc] <= pd.Timestamp(dr[1]))]
                active_filters += 1
        except Exception:
            pass
    for nc in num_cols[:2]:
        try:
            mn_v, mx_v = float(df_raw[nc].min()), float(df_raw[nc].max())
            if mn_v < mx_v:
                rng = st.slider(f"{nc} range", mn_v, mx_v, (mn_v, mx_v), key=f"nr_{nc}")
                if rng != (mn_v, mx_v):
                    df = df[(df[nc] >= rng[0]) & (df[nc] <= rng[1])]
                    active_filters += 1
        except Exception:
            pass
    if active_filters:
        st.success(f"✅ {active_filters} filter(s) active · {len(df):,} rows")
    else:
        st.caption(f"{len(df):,} rows · {len(df.columns)} columns")

if len(df) == 0:
    st.warning("⚠️ No data matches your current filters. Please adjust.")
    st.stop()

# ══════════════════════════════════════════════════════════════
#  TABS
# ══════════════════════════════════════════════════════════════
tabs = st.tabs(["📈 Overview", "📊 Charts", "🔬 Analysis", "🔍 Deep Dive",
                "🧹 Clean", "🗃️ Data", "💾 Export", "🤖 AI Chat"])
tab_overview, tab_charts, tab_analysis, tab_deep, tab_clean, tab_data, tab_export, tab_chat = tabs


# ══════════════════════════════════════════════════════════════
#  TAB 1 — OVERVIEW
# ══════════════════════════════════════════════════════════════
with tab_overview:
    # Quality banner
    qs = data_quality_score(df_raw)
    qc = GREEN if qs >= 80 else (ORANGE if qs >= 50 else RED)
    ql = "Excellent" if qs >= 80 else ("Needs Attention" if qs >= 50 else "Poor")
    qe = "✅" if qs >= 80 else ("⚠️" if qs >= 50 else "❌")
    st.markdown(f"""
    <div class="quality-banner">
        <div class="quality-score-ring" style="--qc:{qc}">{qs:.0f}</div>
        <div class="quality-details">
            <h3>{qe} Data Quality: {ql}</h3>
            <p>Your dataset has been analyzed across {len(df_raw.columns)} columns</p>
            <div class="quality-pills">
                <span class="quality-pill">📋 {len(df_raw):,} rows</span>
                <span class="quality-pill">📑 {len(df_raw.columns)} columns</span>
                <span class="quality-pill">❓ {df_raw.isnull().mean().mean()*100:.1f}% missing</span>
                <span class="quality-pill">🔁 {df_raw.duplicated().sum()} duplicates</span>
                <span class="quality-pill">📊 {len(num_cols)} numeric cols</span>
                <span class="quality-pill">🏷️ {len(cat_cols)} text cols</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # KPI Cards
    if num_cols:
        sec("📌", "Key Metrics", f"{len(num_cols)} columns")
        accents = PALETTE
        icons   = ["💰","📦","📊","🎯","⚡","🔥","💡","📐"]
        cards_html = '<div class="kpi-grid">'
        for i, col in enumerate(num_cols[:8]):
            total = df[col].sum()
            mean_ = df[col].mean()
            mn_v  = df[col].min()
            mx_v  = df[col].max()
            acc   = accents[i % len(accents)]
            cards_html += f"""
            <div class="kpi-card" style="--accent:{acc};--accent-glow:{hex_to_rgba(acc,0.06)}">
                <div class="kpi-icon">{icons[i%len(icons)]}</div>
                <div class="kpi-label">{col}</div>
                <div class="kpi-value">{fmt(total)}</div>
                <div class="kpi-sub">
                    <span>Avg {fmt(mean_)}</span>
                    <span>·</span>
                    <span>↓{fmt(mn_v)}</span>
                    <span>·</span>
                    <span>↑{fmt(mx_v)}</span>
                </div>
            </div>"""
        cards_html += "</div>"
        st.markdown(cards_html, unsafe_allow_html=True)

    # Gauges
    sec("🎯", "Performance Gauges", f"{min(4,len(num_cols))} metrics")
    gcols = st.columns(min(4, len(num_cols)) or 1)
    for i, nc in enumerate(num_cols[:4]):
        with gcols[i]:
            st.plotly_chart(gauge(df[nc].sum(), nc, df_raw[nc].sum() * 1.2),
                            use_container_width=True)

    # Smart charts
    sec("📊", "Smart Visuals")
    if cat_cols and num_cols:
        c1, c2 = st.columns(2)
        with c1:
            try:
                d = safe_groupby(df, [cat_cols[0]], num_cols[0])
                d = d.nlargest(top_n_global, num_cols[0])
                fig = bar(d, cat_cols[0], num_cols[0],
                          title=f"Top {top_n_global}: {num_cols[0]} by {cat_cols[0]}",
                          orientation="h")
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.warning(f"Chart error: {e}")
        with c2:
            try:
                d   = safe_groupby(df, [cat_cols[0]], num_cols[0])
                fig = donut(d, cat_cols[0], num_cols[0],
                            title=f"{num_cols[0]} Share")
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.warning(f"Chart error: {e}")

    if date_cols and num_cols:
        try:
            d   = safe_groupby(df, [date_cols[0]], num_cols[0]).sort_values(date_cols[0])
            fig = area(d, date_cols[0], num_cols[0], title=f"{num_cols[0]} Over Time")
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.warning(f"Time series error: {e}")

    # Auto insights
    sec("🤖", "Auto Insights")
    insights = auto_insights(df, num_cols, cat_cols, date_cols)
    for icon, color, text in insights:
        clean = text.replace("**","<b>",1)
        while "**" in clean:
            clean = clean.replace("**","</b>",1).replace("**","<b>",1)
        st.markdown(f"""
        <div class="insight-card" style="--c:{color}">
            <div class="i-icon">{icon}</div>
            <div class="i-text">{clean}</div>
        </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  TAB 2 — CHART BUILDER
# ══════════════════════════════════════════════════════════════
with tab_charts:
    sec("🛠️", "Interactive Chart Builder")

    chart_type = st.selectbox("Chart Type", [
        "Horizontal Bar", "Vertical Bar", "Grouped Bar",
        "Line Chart", "Area Chart", "Scatter Plot",
        "Donut Chart", "Pie Chart", "Histogram", "Box Plot",
        "Waterfall", "Funnel", "Pareto Analysis",
    ], key="cht_type")

    cfg1, cfg2, cfg3 = st.columns(3)

    try:
        if chart_type in ["Horizontal Bar","Vertical Bar","Grouped Bar",
                           "Line Chart","Area Chart","Waterfall","Funnel","Pareto Analysis"]:
            all_x = cat_cols + date_cols + num_cols
            with cfg1: x_col = st.selectbox("X / Category", all_x, key="cx")
            with cfg2: y_col = st.selectbox("Y / Value", num_cols or all_x, key="cy")
            with cfg3: color_col = st.selectbox("Color group", ["None"] + cat_cols, key="cc")
            color_col = None if color_col == "None" else color_col

            if chart_type in ["Horizontal Bar","Vertical Bar","Grouped Bar"]:
                d   = safe_groupby(df, [x_col]+([color_col] if color_col else []), y_col)
                fig = bar(d, x_col, y_col, color_col,
                          title=f"{y_col} by {x_col}",
                          orientation="h" if chart_type=="Horizontal Bar" else "v",
                          top_n=top_n_global if not color_col else None)
            elif chart_type == "Line Chart":
                d   = safe_groupby(df, [x_col]+([color_col] if color_col else []), y_col)
                fig = line(d.sort_values(x_col), x_col, y_col, color_col, f"{y_col} over {x_col}")
            elif chart_type == "Area Chart":
                d   = safe_groupby(df, [x_col]+([color_col] if color_col else []), y_col)
                fig = area(d.sort_values(x_col), x_col, y_col, color_col, f"{y_col} Area")
            elif chart_type == "Waterfall":
                fig = waterfall(df, x_col, y_col, f"{y_col} Waterfall")
            elif chart_type == "Funnel":
                fig = funnel(df, x_col, y_col, f"{y_col} Funnel")
            elif chart_type == "Pareto Analysis":
                fig = pareto_chart(df, x_col, y_col)
            st.plotly_chart(fig, use_container_width=True)
            chart_download_btn(fig, f"chart_{chart_type.lower().replace(' ','_')}")

        elif chart_type in ["Donut Chart","Pie Chart"]:
            with cfg1: names_c = st.selectbox("Category", cat_cols or df.columns.tolist(), key="pn")
            with cfg2: vals_c  = st.selectbox("Values",   num_cols or df.columns.tolist(), key="pv")
            d    = safe_groupby(df, [names_c], vals_c)
            hole = 0.6 if chart_type == "Donut Chart" else 0
            fig  = donut(d, names_c, vals_c, chart_type, hole)
            st.plotly_chart(fig, use_container_width=True)
            chart_download_btn(fig)

        elif chart_type == "Scatter Plot":
            with cfg1: x_c = st.selectbox("X (numeric)", num_cols, key="sx")
            with cfg2: y_c = st.selectbox("Y (numeric)", num_cols, key="sy")
            with cfg3:
                col_c  = st.selectbox("Color", ["None"] + cat_cols, key="scc")
                size_c = st.selectbox("Size",  ["None"] + num_cols, key="ssc")
                trend  = st.checkbox("Trendline", True, key="str")
            col_c  = None if col_c  == "None" else col_c
            size_c = None if size_c == "None" else size_c
            sample = df.sample(min(2000, len(df)), random_state=42)
            fig    = scatter(sample, x_c, y_c, col_c, size_c, f"{y_c} vs {x_c}", trendline=trend)
            st.plotly_chart(fig, use_container_width=True)
            chart_download_btn(fig)

        elif chart_type == "Histogram":
            with cfg1: col_h  = st.selectbox("Column", num_cols, key="hc")
            with cfg2: bins_h = st.slider("Bins", 5, 100, 30, key="hb")
            with cfg3: col_c  = st.selectbox("Color", ["None"] + cat_cols, key="hcc")
            col_c = None if col_c == "None" else col_c
            fig   = histogram(df, col_h, bins_h, col_c, f"{col_h} Distribution")
            st.plotly_chart(fig, use_container_width=True)
            chart_download_btn(fig)

        elif chart_type == "Box Plot":
            with cfg1: y_c = st.selectbox("Value",    num_cols, key="bxy")
            with cfg2: x_c = st.selectbox("Group by", ["None"] + cat_cols, key="bxx")
            x_c = None if x_c == "None" else x_c
            fig = box_plot(df, y_c, x_c, f"{y_c} Distribution")
            st.plotly_chart(fig, use_container_width=True)
            chart_download_btn(fig)

    except Exception as e:
        st.error(f"❌ Chart error: **{e}** — try different columns.")


# ══════════════════════════════════════════════════════════════
#  TAB 3 — ANALYSIS
# ══════════════════════════════════════════════════════════════
with tab_analysis:
    # Correlation
    sec("🔗", "Correlation Matrix")
    if len(num_cols) >= 2:
        fig_corr = heatmap_corr(df, num_cols)
        if fig_corr:
            st.plotly_chart(fig_corr, use_container_width=True)
    else:
        st.info("Need at least 2 numeric columns.")

    c1, c2 = st.columns(2)
    with c1:
        sec("🗺️", "Treemap")
        if cat_cols and num_cols:
            path_sel = st.multiselect("Hierarchy", cat_cols,
                                       default=cat_cols[:min(2, len(cat_cols))], key="tpath")
            val_sel  = st.selectbox("Values", num_cols, key="tval")
            if path_sel:
                try:
                    st.plotly_chart(treemap(df, path_sel, val_sel), use_container_width=True)
                except Exception as e:
                    st.warning(f"Treemap error: {e}")
        else:
            st.info("Need categorical + numeric columns.")

    with c2:
        sec("🔥", "Pivot Heatmap")
        if len(cat_cols) >= 2 and num_cols:
            r_col = st.selectbox("Rows",    cat_cols, key="pr")
            c_col = st.selectbox("Columns", cat_cols, index=min(1, len(cat_cols)-1), key="pc")
            v_col = st.selectbox("Values",  num_cols, key="pv2")
            if r_col != c_col:
                try:
                    st.plotly_chart(pivot_heatmap(df, r_col, c_col, v_col), use_container_width=True)
                except Exception as e:
                    st.warning(f"Pivot error: {e}")
            else:
                st.info("Row and column must be different.")
        else:
            st.info("Need at least 2 categorical columns.")

    if date_cols and num_cols:
        sec("📅", "Multi-Metric Time Series")
        dc_sel  = st.selectbox("Date column", date_cols, key="tsdc")
        met_sel = st.multiselect("Metrics", num_cols, default=num_cols[:min(3, len(num_cols))], key="tsm")
        if met_sel:
            try:
                st.plotly_chart(multi_axis_line(df, dc_sel, met_sel), use_container_width=True)
            except Exception as e:
                st.warning(f"Time series error: {e}")

    # Statistical summary
    sec("📐", "Statistical Summary")
    if num_cols:
        try:
            stats = df[num_cols].describe().T.round(2)
            stats["skewness"] = df[num_cols].skew().round(2)
            stats["kurtosis"] = df[num_cols].kurt().round(2)
            stats["missing%"] = (df[num_cols].isnull().mean() * 100).round(1)
            stats["outliers"] = [detect_outliers_iqr(df[c].dropna()).sum() for c in num_cols]
            st.dataframe(stats, use_container_width=True, height=300)
        except Exception as e:
            st.warning(f"Stats error: {e}")

    # Forecasting
    sec("🔮", "Time Series Forecast")
    if PLAN == "Free":
        st.markdown(f"""<div class="insight-card" style="--c:{ORANGE}">
            <div class="i-icon">🔒</div>
            <div class="i-text">Forecasting is a <b>Pro feature</b>. Upgrade your plan in the sidebar to unlock.</div>
        </div>""", unsafe_allow_html=True)
    elif date_cols and num_cols:
        fc1, fc2, fc3 = st.columns(3)
        with fc1: fc_date = st.selectbox("Date column",     date_cols, key="fc_date")
        with fc2: fc_val  = st.selectbox("Metric",          num_cols,  key="fc_val")
        with fc3: fc_per  = st.slider("Forecast periods", 7, 90, 30, key="fc_per")
        if st.button("🔮 Run Forecast", key="run_fc"):
            with st.spinner("Running forecast model…"):
                try:
                    result = forecast_series(df, fc_date, fc_val, periods=fc_per)
                    if result[0] is None:
                        st.warning(result[1])
                    else:
                        hist_df, fc_df, std = result
                        fig_fc = forecast_chart(hist_df, fc_df, fc_date, fc_val)
                        st.plotly_chart(fig_fc, use_container_width=True)
                        chart_download_btn(fig_fc, f"forecast_{fc_val}")
                        fc_sum = fc_df[fc_val]
                        c1f, c2f, c3f, c4f = st.columns(4)
                        c1f.metric("Forecast periods",   fc_per)
                        c2f.metric("Avg forecast value", fmt(fc_sum.mean()))
                        c3f.metric("Peak forecast",      fmt(fc_sum.max()))
                        direction = "📈 Upward" if fc_sum.iloc[-1] > fc_sum.iloc[0] else "📉 Downward"
                        c4f.metric("Trend direction",    direction)
                        with st.expander("📋 Forecast data table"):
                            st.dataframe(fc_df[[fc_date, fc_val, "upper", "lower"]].round(2),
                                         use_container_width=True)
                            st.download_button("⬇️ Forecast CSV",
                                               fc_df.to_csv(index=False).encode(),
                                               "forecast.csv", "text/csv")
                except Exception as e:
                    st.error(f"Forecast error: {e}")
    else:
        st.info("Need a date column and at least one numeric column for forecasting.")


# ══════════════════════════════════════════════════════════════
#  TAB 4 — DEEP DIVE
# ══════════════════════════════════════════════════════════════
with tab_deep:
    sec("🔎", "Outlier Detection")
    if num_cols:
        out_col = st.selectbox("Select column", num_cols, key="outcol")
        try:
            c1, c2 = st.columns([2, 1])
            with c1:
                st.plotly_chart(outlier_scatter(df, out_col), use_container_width=True)
            with c2:
                s     = df[out_col].dropna()
                mask  = detect_outliers_iqr(s)
                n_out = mask.sum()
                q1, q3 = s.quantile(0.25), s.quantile(0.75)
                st.markdown(f"""
                <div class="kpi-card" style="--accent:{RED};margin-top:10px">
                    <div class="kpi-label">Outliers detected</div>
                    <div class="kpi-value" style="color:{RED}">{n_out}</div>
                    <div class="kpi-sub">{n_out/len(s)*100:.1f}% of non-null rows</div>
                </div>
                <div class="kpi-card" style="--accent:{BLUE};margin-top:10px">
                    <div class="kpi-label">IQR Bounds</div>
                    <div class="kpi-value" style="font-size:1rem">{fmt(q1-1.5*(q3-q1))} → {fmt(q3+1.5*(q3-q1))}</div>
                    <div class="kpi-sub">Q1={fmt(q1)} · Q3={fmt(q3)}</div>
                </div>""", unsafe_allow_html=True)
                if n_out:
                    st.dataframe(df[mask].head(20), use_container_width=True)
        except Exception as e:
            st.warning(f"Outlier error: {e}")

    sec("❓", "Missing Value Analysis")
    miss_summary = df.isnull().sum()
    miss_pct     = (df.isnull().mean() * 100).round(1)
    miss_df      = pd.DataFrame({"Column": df.columns, "Missing": miss_summary, "Pct": miss_pct})
    miss_df      = miss_df[miss_df["Missing"] > 0].sort_values("Missing", ascending=False)
    if len(miss_df):
        c1, c2 = st.columns([1, 2])
        with c1:
            st.dataframe(miss_df, use_container_width=True)
        with c2:
            try:
                fig_m = missing_heatmap(df.sample(min(200, len(df)), random_state=1))
                if fig_m:
                    st.plotly_chart(fig_m, use_container_width=True)
            except Exception as e:
                st.warning(f"Missing map error: {e}")
    else:
        st.success("✅ No missing values!")

    sec("📊", "Distribution Analysis")
    if num_cols:
        dist_cols = st.multiselect("Columns to compare", num_cols,
                                    default=num_cols[:min(3, len(num_cols))], key="distcols")
        if dist_cols:
            try:
                n = len(dist_cols)
                fig_dist = make_subplots(rows=1, cols=n,
                                          subplot_titles=[f"▸ {c}" for c in dist_cols])
                for i, col in enumerate(dist_cols):
                    vals = df[col].dropna()
                    c_color = PALETTE[i % len(PALETTE)]
                    fig_dist.add_trace(
                        go.Histogram(x=vals, name=col, nbinsx=30,
                                     marker_color=c_color, opacity=0.8,
                                     marker_line_width=0), row=1, col=i+1)
                layout_d = {k: v for k, v in PBI_LAYOUT.items() if k not in ("xaxis","yaxis")}
                fig_dist.update_layout(height=320, showlegend=False, **layout_d)
                st.plotly_chart(fig_dist, use_container_width=True)
            except Exception as e:
                st.warning(f"Distribution error: {e}")

    if cat_cols and num_cols:
        sec("📊", "Pareto Analysis (80/20 Rule)")
        p_cat = st.selectbox("Category", cat_cols, key="pcat")
        p_val = st.selectbox("Value",    num_cols, key="pval")
        try:
            st.plotly_chart(pareto_chart(df, p_cat, p_val, f"Pareto: {p_val} by {p_cat}"),
                            use_container_width=True)
        except Exception as e:
            st.warning(f"Pareto error: {e}")


# ══════════════════════════════════════════════════════════════
#  TAB 5 — DATA CLEANING
# ══════════════════════════════════════════════════════════════
with tab_clean:
    sec("🧹", "Data Cleaning Toolkit")

    if "clean_df" not in st.session_state or st.button("↺ Reset to original", key="reset_clean"):
        st.session_state.clean_df = df_raw.copy()
    cdf = st.session_state.clean_df

    # Stats row
    bef1, bef2, bef3, bef4 = st.columns(4)
    bef1.metric("Rows",          f"{len(cdf):,}",      f"{len(cdf)-len(df_raw):,}")
    bef2.metric("Duplicates",    f"{cdf.duplicated().sum():,}")
    bef3.metric("Missing cells", f"{cdf.isnull().sum().sum():,}")
    bef4.metric("Quality score", f"{data_quality_score(cdf):.0f}/100")

    st.markdown("---")
    cl1, cl2 = st.columns(2)

    with cl1:
        st.markdown(f"#### ✂️ Remove Operations")
        if st.button("🗑️ Remove duplicate rows", use_container_width=True, key="rm_dup"):
            before = len(cdf)
            cdf    = cdf.drop_duplicates()
            st.session_state.clean_df = cdf
            st.success(f"Removed {before - len(cdf):,} duplicate rows")
        drop_cols = st.multiselect("Drop columns", cdf.columns.tolist(), key="drop_cols")
        if st.button("🗑️ Drop selected columns", use_container_width=True, key="do_drop_cols"):
            if drop_cols:
                cdf = cdf.drop(columns=drop_cols)
                st.session_state.clean_df = cdf
                st.success(f"Dropped: {drop_cols}")
        if st.button("🗑️ Drop rows with ANY missing value", use_container_width=True, key="drop_any"):
            before = len(cdf)
            cdf    = cdf.dropna()
            st.session_state.clean_df = cdf
            st.success(f"Removed {before - len(cdf):,} rows")
        thresh_pct = st.slider("Drop columns with >X% missing", 0, 100, 50, key="col_thresh")
        if st.button(f"🗑️ Drop columns >{thresh_pct}% missing", use_container_width=True, key="do_col_thresh"):
            before_cols = len(cdf.columns)
            thresh = int(len(cdf) * thresh_pct / 100)
            cdf    = cdf.dropna(axis=1, thresh=thresh)
            st.session_state.clean_df = cdf
            st.success(f"Dropped {before_cols - len(cdf.columns)} columns")
        if num_cols:
            if st.button("🗑️ Remove numeric outliers (IQR)", use_container_width=True, key="rm_out"):
                before = len(cdf)
                num_c  = get_num_cols(cdf)
                mask   = pd.Series([True] * len(cdf), index=cdf.index)
                for col in num_c:
                    mask &= ~detect_outliers_iqr(cdf[col].fillna(cdf[col].median()))
                cdf = cdf[mask]
                st.session_state.clean_df = cdf
                st.success(f"Removed {before - len(cdf):,} outlier rows")

    with cl2:
        st.markdown(f"#### 🔧 Fill & Transform")
        fill_strategy = st.selectbox("Fill missing values with",
            ["— choose —", "Mean (numeric only)", "Median (numeric only)",
             "Mode (all columns)", "Zero (numeric only)", "Custom value"],
            key="fill_strat")
        if fill_strategy != "— choose —":
            custom_val = ""
            if fill_strategy == "Custom value":
                custom_val = st.text_input("Custom fill value", "0", key="fill_custom")
            if st.button(f"✅ Apply: {fill_strategy}", use_container_width=True, key="do_fill"):
                try:
                    num_c = get_num_cols(cdf)
                    if fill_strategy == "Mean (numeric only)":
                        cdf[num_c] = cdf[num_c].fillna(cdf[num_c].mean())
                    elif fill_strategy == "Median (numeric only)":
                        cdf[num_c] = cdf[num_c].fillna(cdf[num_c].median())
                    elif fill_strategy == "Mode (all columns)":
                        for col in cdf.columns:
                            mode_val = cdf[col].mode()
                            if len(mode_val): cdf[col] = cdf[col].fillna(mode_val[0])
                    elif fill_strategy == "Zero (numeric only)":
                        cdf[num_c] = cdf[num_c].fillna(0)
                    elif fill_strategy == "Custom value":
                        try:    cdf = cdf.fillna(float(custom_val))
                        except: cdf = cdf.fillna(str(custom_val))
                    st.session_state.clean_df = cdf
                    st.success(f"Applied: {fill_strategy}")
                except Exception as e:
                    st.error(f"Fill error: {e}")

        st.markdown("---")
        st.markdown("**Rename column**")
        rc1, rc2 = st.columns(2)
        with rc1: old_name = st.selectbox("Column to rename", cdf.columns.tolist(), key="rn_old")
        with rc2: new_name = st.text_input("New name", key="rn_new")
        if st.button("✅ Rename", use_container_width=True, key="do_rename"):
            if new_name and new_name != old_name and new_name not in cdf.columns:
                cdf = cdf.rename(columns={old_name: new_name})
                st.session_state.clean_df = cdf
                st.success(f"Renamed '{old_name}' → '{new_name}'")
            else:
                st.warning("Invalid or duplicate name")

        st.markdown("---")
        st.markdown("**Convert column type**")
        dt1, dt2 = st.columns(2)
        with dt1: type_col = st.selectbox("Column", cdf.columns.tolist(), key="tc")
        with dt2: new_type = st.selectbox("Convert to", ["numeric","text","datetime","integer"], key="nt")
        if st.button("✅ Convert type", use_container_width=True, key="do_type"):
            try:
                if new_type == "numeric":
                    cdf[type_col] = pd.to_numeric(cdf[type_col], errors="coerce")
                elif new_type == "integer":
                    cdf[type_col] = pd.to_numeric(cdf[type_col], errors="coerce").astype("Int64")
                elif new_type == "text":
                    cdf[type_col] = cdf[type_col].astype(str)
                elif new_type == "datetime":
                    cdf[type_col] = pd.to_datetime(cdf[type_col], errors="coerce")
                st.session_state.clean_df = cdf
                st.success(f"Converted '{type_col}' to {new_type}")
            except Exception as e:
                st.error(f"Conversion error: {e}")

    st.markdown("---")
    sec("👁️", "Cleaned Data Preview")
    st.caption(f"Shape: {cdf.shape[0]:,} rows × {cdf.shape[1]} columns — Quality: {data_quality_score(cdf):.0f}/100")
    st.dataframe(cdf.head(50), use_container_width=True, height=320)
    cc1, cc2 = st.columns(2)
    with cc1:
        st.download_button("⬇️ Download Cleaned CSV",
                           cdf.to_csv(index=False).encode("utf-8"),
                           "cleaned_data.csv", "text/csv", use_container_width=True)
    with cc2:
        buf = io.BytesIO()
        with pd.ExcelWriter(buf, engine="openpyxl") as w:
            cdf.to_excel(w, index=False)
        st.download_button("⬇️ Download Cleaned Excel", buf.getvalue(),
                           "cleaned_data.xlsx",
                           "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                           use_container_width=True)


# ══════════════════════════════════════════════════════════════
#  TAB 6 — DATA EXPLORER
# ══════════════════════════════════════════════════════════════
with tab_data:
    sec("🗃️", "Data Explorer")
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Rows",        f"{len(df):,}")
    m2.metric("Columns",     f"{len(df.columns)}")
    m3.metric("Numeric",     f"{len(num_cols)}")
    m4.metric("Categorical", f"{len(cat_cols)}")
    m5.metric("Missing %",   f"{df.isnull().mean().mean()*100:.1f}%")

    search = st.text_input("🔍 Search rows", placeholder="Type to filter rows across all columns…", key="search")
    display_df = df.copy()
    if search.strip():
        try:
            mask = display_df.apply(lambda c: c.astype(str).str.contains(search.strip(), case=False, na=False))
            display_df = display_df[mask.any(axis=1)]
            st.caption(f"Found {len(display_df):,} matching rows")
        except Exception:
            pass

    n_show = st.slider("Rows to display", 10, min(1000, max(10, len(display_df))), 50)
    st.dataframe(display_df.head(n_show), use_container_width=True, height=400)

    sec("📋", "Column Info")
    col_info = pd.DataFrame({
        "Column":  df.columns,
        "Type":    df.dtypes.astype(str).values,
        "Non-Null": df.count().values,
        "Null %":  (df.isnull().mean() * 100).round(1).astype(str) + "%",
        "Unique":  df.nunique().values,
        "Sample":  [str(df[c].dropna().iloc[0]) if df[c].dropna().shape[0] > 0 else "—"
                    for c in df.columns],
    })
    st.dataframe(col_info, use_container_width=True)


# ══════════════════════════════════════════════════════════════
#  TAB 7 — EXPORT
# ══════════════════════════════════════════════════════════════
with tab_export:
    sec("💾", "Export Options")
    e1, e2, e3, e4 = st.columns(4)

    with e1:
        st.markdown(f"""<div class="kpi-card" style="--accent:{GOLD}">
        <div class="kpi-icon">📥</div><div class="kpi-label">Filtered CSV</div>
        <div class="kpi-value" style="font-size:1.1rem">{len(df):,} rows</div>
        <div class="kpi-sub">Filtered dataset</div></div>""", unsafe_allow_html=True)
        st.download_button("⬇️ Download CSV", to_csv(df), "filtered_data.csv",
                            "text/csv", use_container_width=True)

    with e2:
        st.markdown(f"""<div class="kpi-card" style="--accent:{BLUE}">
        <div class="kpi-icon">📊</div><div class="kpi-label">Excel Report</div>
        <div class="kpi-value" style="font-size:1.1rem">Data + Stats</div>
        <div class="kpi-sub">Two-sheet workbook</div></div>""", unsafe_allow_html=True)
        st.download_button("⬇️ Download Excel", to_excel(df), "bi_report.xlsx",
                            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            use_container_width=True)

    with e3:
        st.markdown(f"""<div class="kpi-card" style="--accent:{GREEN}">
        <div class="kpi-icon">📐</div><div class="kpi-label">Stats CSV</div>
        <div class="kpi-value" style="font-size:1.1rem">Descriptive</div>
        <div class="kpi-sub">Mean, std, skew…</div></div>""", unsafe_allow_html=True)
        if num_cols:
            stats_exp = df[num_cols].describe().T.copy()
            stats_exp["skew"]     = df[num_cols].skew()
            stats_exp["kurtosis"] = df[num_cols].kurt()
            st.download_button("⬇️ Download Stats", to_csv(stats_exp),
                                "stats_summary.csv", "text/csv", use_container_width=True)

    with e4:
        st.markdown(f"""<div class="kpi-card" style="--accent:{PURPLE}">
        <div class="kpi-icon">📄</div><div class="kpi-label">HTML Report</div>
        <div class="kpi-value" style="font-size:1.1rem">Full Report</div>
        <div class="kpi-sub">KPIs · Insights · Stats</div></div>""", unsafe_allow_html=True)
        try:
            fname = uploaded.name if not use_sample else "sample_data"
            report_bytes = build_html_report(df, num_cols, cat_cols, date_cols,
                                             fname, sheet_name)
            st.download_button("⬇️ Download Report", report_bytes,
                                "bi_report.html", "text/html", use_container_width=True)
        except Exception as e:
            st.warning(f"Report error: {e}")

    st.markdown("---")
    sec("🗂️", "Dataset Metadata")
    fname_meta = uploaded.name if uploaded else "sample_data.csv"
    st.json({
        "filename":           fname_meta,
        "sheet":              sheet_name,
        "plan":               PLAN,
        "row_limit":          ROW_LIMIT,
        "rows_total":         len(df_raw),
        "rows_filtered":      len(df),
        "columns":            len(df.columns),
        "numeric_columns":    num_cols,
        "categorical_cols":   cat_cols,
        "date_columns":       [str(c) for c in date_cols],
        "data_quality_score": f"{data_quality_score(df_raw):.0f}/100",
        "missing_pct":        f"{df_raw.isnull().mean().mean()*100:.2f}%",
        "duplicates":         int(df_raw.duplicated().sum()),
        "generated_at":       datetime.now().isoformat(),
    })


# ══════════════════════════════════════════════════════════════
#  TAB 8 — AI CHAT
# ══════════════════════════════════════════════════════════════
with tab_chat:
    # Additional chat CSS
    st.markdown("""<style>
    .stTextInput input { font-size:0.9rem !important; }
    </style>""", unsafe_allow_html=True)

    def build_data_context(df, num_cols, cat_cols, date_cols, max_rows=6):
        lines = []
        fname = uploaded.name if not use_sample else "sample_data.csv"
        lines.append(f"DATASET: '{fname}' — Sheet: '{sheet_name}'")
        lines.append(f"Shape: {len(df):,} rows × {len(df.columns)} columns")
        lines.append(f"Numeric columns ({len(num_cols)}): {', '.join(num_cols)}")
        lines.append(f"Categorical columns ({len(cat_cols)}): {', '.join(cat_cols)}")
        if date_cols:
            lines.append(f"Date columns: {', '.join(str(c) for c in date_cols)}")
        lines.append(f"Missing: {df.isnull().mean().mean()*100:.1f}% overall")
        lines.append(f"Duplicates: {df.duplicated().sum()}")
        lines.append(f"Data quality score: {data_quality_score(df):.0f}/100")
        lines.append("")
        if num_cols:
            lines.append("NUMERIC SUMMARY:")
            for c in num_cols[:8]:
                s = df[c].dropna()
                if len(s):
                    lines.append(
                        f"  {c}: sum={s.sum():,.2f}, mean={s.mean():,.2f}, "
                        f"min={s.min():,.2f}, max={s.max():,.2f}, nulls={df[c].isnull().sum()}"
                    )
        if cat_cols:
            lines.append("")
            lines.append("TOP CATEGORIES:")
            for c in cat_cols[:4]:
                vc = df[c].value_counts().head(5)
                lines.append(f"  {c}: {dict(vc)}")
        lines.append("")
        lines.append(f"SAMPLE DATA (first {max_rows} rows):")
        lines.append(df.head(max_rows).to_string(index=False, max_cols=10))
        return "\n".join(lines)

    # API key handling
    api_key = None
    try:
        api_key = st.secrets.get("ANTHROPIC_API_KEY", None)
    except Exception:
        pass

    if not api_key:
        sec("🔑", "API Key Setup")
        st.markdown(f"""
        <div class="insight-card" style="--c:{GOLD}">
            <div class="i-icon">💡</div>
            <div class="i-text">
                To use AI Chat, you need a free Anthropic API key.<br>
                Get one at <b>console.anthropic.com</b> → API Keys → Create Key.<br>
                Then paste it below (session only) or save in Streamlit secrets for persistence.
            </div>
        </div>""", unsafe_allow_html=True)
        api_input = st.text_input("Paste your Anthropic API key",
                                   type="password", key="api_key_input",
                                   placeholder="sk-ant-…")
        if api_input.strip().startswith("sk-ant-"):
            api_key = api_input.strip()
            st.success("✅ API key set for this session!")
        elif api_input:
            st.error("❌ Key should start with 'sk-ant-'")

    sec("🤖", "Chat With Your Data")

    # Suggestions
    data_ctx   = build_data_context(df, num_cols, cat_cols, date_cols)
    suggestions = []
    if num_cols:
        suggestions.append("What are the key insights from this data?")
        suggestions.append(f"Which {cat_cols[0] if cat_cols else 'category'} has the highest {num_cols[0]}?")
        suggestions.append("Are there any anomalies or outliers I should know about?")
        suggestions.append("Give me an executive summary of this dataset")
    if date_cols:
        suggestions.append(f"What is the trend over time for {num_cols[0] if num_cols else 'the data'}?")
    suggestions.append("What data cleaning steps do you recommend?")
    suggestions.append("ما هي أبرز النتائج في هذه البيانات؟")

    cols_sg = st.columns(min(3, len(suggestions)))
    clicked_suggestion = None
    for i, sg in enumerate(suggestions[:6]):
        with cols_sg[i % 3]:
            if st.button(sg[:52] + ("…" if len(sg) > 52 else ""),
                         key=f"sg_{i}", use_container_width=True):
                clicked_suggestion = sg

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Render chat
    if st.session_state.chat_history:
        chat_html = '<div class="chat-container">'
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                chat_html += f"""
                <div class="chat-msg user">
                    <div class="bubble user">{msg["content"]}</div>
                    <div class="chat-avatar user">👤</div>
                </div>"""
            else:
                content = msg["content"]
                content = content.replace("**", "<b>", 1)
                while "**" in content:
                    content = content.replace("**", "</b>", 1).replace("**", "<b>", 1)
                content = content.replace("\n- ", "<br>• ").replace("\n• ", "<br>• ")
                content = content.replace("\n\n", "<br><br>").replace("\n", "<br>")
                chat_html += f"""
                <div class="chat-msg">
                    <div class="chat-avatar ai">🤖</div>
                    <div class="bubble ai">{content}</div>
                </div>"""
        chat_html += "</div>"
        st.markdown(chat_html, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-empty">
            <div class="icon">🤖</div>
            <h3>AI Data Analyst</h3>
            <p>Ask anything about your data in English or Arabic.<br>
               Click a suggestion above or type your question below.</p>
        </div>""", unsafe_allow_html=True)

    # Input row
    col_input, col_btn, col_clear = st.columns([7, 1, 1])
    with col_input:
        user_input = st.text_input(
            "Ask about your data",
            value=clicked_suggestion or "",
            placeholder="e.g. What are the top 3 insights? / ما هي أبرز النتائج؟",
            key="chat_input", label_visibility="collapsed"
        )
    with col_btn:
        send = st.button("Send ➤", use_container_width=True, key="send_btn")
    with col_clear:
        if st.button("🗑️ Clear", use_container_width=True, key="clear_btn"):
            st.session_state.chat_history = []
            st.rerun()

    question = (user_input.strip() if send and user_input.strip()
                else (clicked_suggestion if clicked_suggestion else None))

    if question:
        if not api_key:
            st.error("❌ Please enter your Anthropic API key above to use AI Chat.")
        else:
            st.session_state.chat_history.append({"role": "user", "content": question})
            with st.spinner("🤖 Analyzing your data…"):
                try:
                    import urllib.request, json as _json
                    system_prompt = f"""You are an expert data analyst and business intelligence consultant.
You have been given a dataset to analyze. Answer questions clearly, professionally, and concisely.
If the user writes in Arabic, respond fully in Arabic. If in English, respond in English.
Use bullet points for lists. Use **bold** for key numbers and findings.
Keep answers focused and actionable — like a senior analyst presenting to executives.

Here is the dataset context:
{data_ctx}"""
                    history_for_api = st.session_state.chat_history[-10:]
                    messages_payload = [{"role": m["role"], "content": m["content"]}
                                        for m in history_for_api]
                    payload = _json.dumps({
                        "model":    "claude-sonnet-4-20250514",
                        "max_tokens": 1024,
                        "system":   system_prompt,
                        "messages": messages_payload,
                    }).encode("utf-8")
                    req = urllib.request.Request(
                        "https://api.anthropic.com/v1/messages",
                        data=payload,
                        headers={"Content-Type": "application/json",
                                 "x-api-key": api_key,
                                 "anthropic-version": "2023-06-01"},
                        method="POST"
                    )
                    with urllib.request.urlopen(req, timeout=30) as resp:
                        result   = _json.loads(resp.read().decode("utf-8"))
                        ai_reply = result["content"][0]["text"]
                    st.session_state.chat_history.append({"role": "assistant", "content": ai_reply})
                    st.rerun()
                except Exception as e:
                    err_msg = str(e)
                    if "401" in err_msg:
                        st.error("❌ Invalid API key. Check at console.anthropic.com")
                    elif "429" in err_msg:
                        st.error("⏳ Rate limit reached. Wait a moment and try again.")
                    elif "timeout" in err_msg.lower():
                        st.error("⏱️ Request timed out. Try a shorter question.")
                    else:
                        st.error(f"❌ AI error: {e}")

    with st.expander("📖 How to save your API key permanently"):
        st.markdown("""
**Option A — Streamlit Cloud Secrets (recommended):**
1. Go to your app on [share.streamlit.io](https://share.streamlit.io)
2. Click **⋮ → Settings → Secrets**
3. Add: `ANTHROPIC_API_KEY = "sk-ant-your-key-here"`
4. Save — the app restarts automatically.

**Option B — Local `.streamlit/secrets.toml` file:**
```toml
ANTHROPIC_API_KEY = "sk-ant-your-key-here"
```
Get your free API key at **[console.anthropic.com](https://console.anthropic.com)** → API Keys.
        """)


# ══════════════════════════════════════════════════════════════
#  FOOTER
# ══════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="app-footer">
    DataVision Pro · Expert Edition · Powered by Streamlit · Plotly · Claude AI &nbsp;·&nbsp; {datetime.now().year}
</div>""", unsafe_allow_html=True)
