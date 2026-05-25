import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import io
import warnings
from datetime import datetime, timedelta

warnings.filterwarnings("ignore")

# ══════════════════════════════════════════════════════════════
#  PAGE CONFIG
# ══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="BI Studio Pro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════
#  THEME
# ══════════════════════════════════════════════════════════════
GOLD   = "#f2c94c"
BLUE   = "#4e9af1"
GREEN  = "#6fcf97"
RED    = "#eb5757"
PURPLE = "#9b59b6"
ORANGE = "#f97316"
CYAN   = "#06b6d4"
PINK   = "#ec4899"
BG     = "#1b1b2f"
CARD   = "#252540"
BORDER = "#2e2e50"

PBI_COLORS = [GOLD, BLUE, GREEN, RED, PURPLE, ORANGE, CYAN, PINK,
              "#a78bfa", "#34d399", "#fb923c", "#60a5fa"]

PBI_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#d1d5db", family="Segoe UI, sans-serif", size=12),
    title_font=dict(color=GOLD, size=14, family="Segoe UI, sans-serif"),
    legend=dict(bgcolor="rgba(37,37,64,0.85)", bordercolor=BORDER,
                borderwidth=1, font=dict(color="#d1d5db", size=11)),
    margin=dict(l=45, r=20, t=45, b=45),
    colorway=PBI_COLORS,
    xaxis=dict(gridcolor="#2a2a45", linecolor="#3a3a5c",
               tickfont=dict(color="#9ca3af"), zerolinecolor="#3a3a5c"),
    yaxis=dict(gridcolor="#2a2a45", linecolor="#3a3a5c",
               tickfont=dict(color="#9ca3af"), zerolinecolor="#3a3a5c"),
    hoverlabel=dict(bgcolor="#1f1f3a", bordercolor=BORDER,
                    font=dict(color="#e0e0e0", size=12)),
)

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
html, body, [class*="css"] {{
    font-family: 'Inter', 'Segoe UI', Tahoma, sans-serif;
}}
.main {{ background:{BG}; color:#e0e0e0; }}
.block-container {{ padding:1.2rem 1.8rem; max-width:100%; }}

/* Sidebar */
[data-testid="stSidebar"] {{
    background:#13131f;
    border-right:1px solid {BORDER};
}}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {{ color:{GOLD}; }}

/* Header */
.pbi-header {{
    background:linear-gradient(135deg,#0a0a1a 0%,#1a1a35 60%,#252547 100%);
    border-bottom:2px solid {GOLD};
    padding:16px 24px;
    border-radius:10px;
    margin-bottom:18px;
    display:flex; align-items:center; gap:16px;
}}
.pbi-header h1 {{ color:{GOLD}; font-size:1.7rem; margin:0; font-weight:700; }}
.pbi-header p  {{ color:#9ca3af; margin:2px 0 0; font-size:0.82rem; }}
.pbi-badge {{
    background:{GOLD}; color:#1b1b2f; font-size:0.65rem;
    font-weight:700; padding:2px 8px; border-radius:20px;
    letter-spacing:1px; margin-left:8px; vertical-align:middle;
}}

/* KPI Cards */
.kpi-grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(160px,1fr)); gap:14px; margin-bottom:20px; }}
.kpi-card {{
    background:{CARD}; border-radius:10px; padding:16px 18px;
    border-top:3px solid var(--accent);
    box-shadow:0 4px 18px rgba(0,0,0,0.4);
    transition:transform 0.18s, box-shadow 0.18s;
}}
.kpi-card:hover {{ transform:translateY(-3px); box-shadow:0 8px 26px rgba(0,0,0,0.55); }}
.kpi-icon  {{ font-size:1.4rem; margin-bottom:6px; }}
.kpi-label {{ color:#9ca3af; font-size:0.7rem; text-transform:uppercase; letter-spacing:1.2px; }}
.kpi-value {{ color:#fff; font-size:1.75rem; font-weight:700; line-height:1.1; }}
.kpi-sub   {{ color:#6b7280; font-size:0.72rem; margin-top:4px; }}

/* Section headers */
.sec {{ color:{GOLD}; font-size:0.88rem; font-weight:600;
        border-left:3px solid {GOLD}; padding-left:10px;
        margin:20px 0 12px; text-transform:uppercase; letter-spacing:1px; }}

/* Insight cards */
.insight-card {{
    background:{CARD}; border-radius:8px; padding:14px 16px;
    border-left:3px solid var(--c,{GOLD});
    margin-bottom:10px; font-size:0.85rem; color:#d1d5db;
}}
.insight-card b {{ color:var(--c,{GOLD}); }}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {{ background:{BG}; border-bottom:2px solid {GOLD}; gap:4px; }}
.stTabs [data-baseweb="tab"] {{ color:#9ca3af; font-weight:500; font-size:0.85rem; padding:8px 16px; }}
.stTabs [aria-selected="true"] {{ color:{GOLD}!important; background:{CARD}!important; border-radius:6px 6px 0 0; }}

/* Metrics */
[data-testid="stMetric"] {{ background:{CARD}; padding:14px; border-radius:10px; border-left:3px solid {GOLD}; }}
[data-testid="stMetricLabel"] {{ color:#9ca3af!important; font-size:0.72rem!important; text-transform:uppercase; letter-spacing:0.8px; }}
[data-testid="stMetricValue"] {{ color:#fff!important; font-size:1.7rem!important; font-weight:700!important; }}
[data-testid="stMetricDelta"] {{ font-size:0.78rem!important; }}

/* Widgets */
.stSelectbox label, .stMultiSelect label,
.stSlider label, .stRadio label {{ color:#d1d5db!important; font-size:0.82rem!important; }}
div[data-baseweb="select"] > div {{ background:#1f1f38!important; border-color:#3a3a5c!important; color:#e0e0e0!important; }}
.stDataFrame {{ border:1px solid {BORDER}; border-radius:8px; }}

/* Buttons */
.stButton > button {{
    background:linear-gradient(135deg,{GOLD},{ORANGE});
    color:#1b1b2f; font-weight:700; border:none;
    border-radius:7px; padding:8px 22px; font-size:0.85rem;
    transition:all 0.2s;
}}
.stButton > button:hover {{ opacity:0.88; transform:translateY(-1px); }}
.stDownloadButton > button {{
    background:transparent; color:{GOLD}; border:1px solid {GOLD};
    border-radius:7px; padding:7px 18px; font-size:0.82rem;
}}
.stDownloadButton > button:hover {{ background:{GOLD}22; }}

/* Upload */
[data-testid="stFileUploader"] {{
    background:#1f1f38; border:2px dashed #3a3a5c; border-radius:10px; padding:10px;
}}

/* Scrollbar */
::-webkit-scrollbar {{ width:5px; height:5px; }}
::-webkit-scrollbar-track {{ background:{BG}; }}
::-webkit-scrollbar-thumb {{ background:#3a3a5c; border-radius:3px; }}

/* Alert overrides */
.stAlert {{ border-radius:8px; font-size:0.83rem; }}

/* Quality badge */
.qual-good  {{ color:{GREEN}; font-weight:600; }}
.qual-warn  {{ color:{ORANGE}; font-weight:600; }}
.qual-bad   {{ color:{RED}; font-weight:600; }}

/* Progress bar */
.stProgress > div > div > div {{ background:{GOLD}; }}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  UTILITY FUNCTIONS
# ══════════════════════════════════════════════════════════════

def fmt(n, prefix="", suffix=""):
    """Smart number formatter."""
    if pd.isna(n): return "—"
    try:
        n = float(n)
        if abs(n) >= 1_000_000_000: s = f"{n/1e9:.2f}B"
        elif abs(n) >= 1_000_000:   s = f"{n/1e6:.2f}M"
        elif abs(n) >= 1_000:       s = f"{n/1e3:.1f}K"
        elif n == int(n):            s = f"{int(n):,}"
        else:                        s = f"{n:,.2f}"
        return f"{prefix}{s}{suffix}"
    except Exception:
        return str(n)

def hex_to_rgba(h, a=0.15):
    h = h.lstrip("#")
    r,g,b = int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)
    return f"rgba({r},{g},{b},{a})"

def apply_theme(fig, height=None):
    layout = dict(PBI_LAYOUT)
    if height: layout["height"] = height
    fig.update_layout(**layout)
    return fig

def get_num_cols(df):
    return df.select_dtypes(include=np.number).columns.tolist()

def get_cat_cols(df):
    return df.select_dtypes(include=["object","category"]).columns.tolist()

def get_date_cols(df):
    return df.select_dtypes(include=["datetime64","datetimetz"]).columns.tolist()

def detect_and_parse_dates(df):
    """Try to detect and convert date-like string columns."""
    for col in df.select_dtypes(include="object").columns:
        if df[col].nunique() > 0.95 * len(df): continue  # skip high-cardinality
        sample = df[col].dropna().head(200)
        try:
            converted = pd.to_datetime(sample, infer_datetime_format=True, errors="coerce")
            if converted.notna().sum() / max(len(sample),1) > 0.75:
                df[col] = pd.to_datetime(df[col], infer_datetime_format=True, errors="coerce")
        except Exception:
            pass
    return df

def safe_read(f):
    """Read CSV or Excel robustly."""
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
    """Crash-proof groupby."""
    group_cols = [c for c in group_cols if c and c in df.columns and c != val_col]
    if not group_cols or val_col not in df.columns:
        return pd.DataFrame(columns=(group_cols or []) + [val_col])
    try:
        tmp = df[group_cols + [val_col]].dropna(subset=group_cols).copy()
        for c in group_cols:
            tmp[c] = tmp[c].astype(str).str.strip()
        tmp = tmp[tmp[c] != "nan"]  # remove stringified NaN
        return tmp.groupby(group_cols, as_index=False, sort=False)[val_col].agg(agg)
    except Exception:
        return pd.DataFrame(columns=group_cols + [val_col])

def detect_outliers_iqr(series):
    """Return boolean mask of outliers via IQR."""
    q1, q3 = series.quantile(0.25), series.quantile(0.75)
    iqr = q3 - q1
    return (series < q1 - 1.5*iqr) | (series > q3 + 1.5*iqr)

def data_quality_score(df):
    """0-100 quality score."""
    total = df.size
    if total == 0: return 0
    missing_pct  = df.isnull().sum().sum() / total
    dup_pct      = df.duplicated().sum() / max(len(df),1)
    score = 100 - (missing_pct * 60) - (dup_pct * 40)
    return max(0, min(100, score))

def auto_insights(df, num_cols, cat_cols, date_cols):
    """Generate plain-language insights from the data."""
    insights = []
    # Missing data
    miss = df.isnull().mean()
    bad = miss[miss > 0.2]
    if len(bad):
        cols_str = ", ".join(f"**{c}** ({miss[c]:.0%})" for c in bad.index[:3])
        insights.append(("⚠️", RED, f"High missing values in: {cols_str}"))
    # Duplicates
    dups = df.duplicated().sum()
    if dups:
        insights.append(("🔁", ORANGE, f"**{dups:,} duplicate rows** detected ({dups/len(df):.1%} of data)"))
    # Outliers
    for col in num_cols[:4]:
        out_mask = detect_outliers_iqr(df[col].dropna())
        n_out = out_mask.sum()
        if n_out > 0 and n_out / len(df) > 0.02:
            insights.append(("📍", PURPLE,
                f"**{n_out:,} outliers** in **{col}** "
                f"(min {fmt(df[col].min())}, max {fmt(df[col].max())})"))
    # Skewness
    for col in num_cols[:4]:
        sk = df[col].skew()
        if abs(sk) > 2:
            direction = "right (positive)" if sk > 0 else "left (negative)"
            insights.append(("📈", CYAN,
                f"**{col}** is heavily skewed {direction} (skew={sk:.1f}) — consider log transform"))
    # Dominant category
    for col in cat_cols[:2]:
        vc = df[col].value_counts(normalize=True)
        if len(vc) and vc.iloc[0] > 0.5:
            insights.append(("🏆", GREEN,
                f"**{vc.index[0]}** dominates **{col}** "
                f"({vc.iloc[0]:.0%} of rows)"))
    # Correlation
    if len(num_cols) >= 2:
        corr = df[num_cols].corr()
        np.fill_diagonal(corr.values, np.nan)
        max_corr = corr.abs().stack().idxmax()
        max_val  = corr.loc[max_corr]
        if abs(max_val) > 0.7:
            insights.append(("🔗", BLUE,
                f"Strong correlation ({max_val:.2f}) between "
                f"**{max_corr[0]}** and **{max_corr[1]}**"))
    # Trend in numeric (if date present)
    if date_cols and num_cols:
        try:
            ts = df.set_index(date_cols[0])[num_cols[0]].dropna().sort_index()
            if len(ts) > 5:
                pct_chg = (ts.iloc[-1] - ts.iloc[0]) / abs(ts.iloc[0]) * 100 if ts.iloc[0] != 0 else 0
                arrow = "📈" if pct_chg > 0 else "📉"
                color = GREEN if pct_chg > 0 else RED
                insights.append((arrow, color,
                    f"**{num_cols[0]}** changed by **{pct_chg:+.1f}%** "
                    f"from start to end of period"))
        except Exception:
            pass
    if not insights:
        insights.append(("✅", GREEN, "Data looks clean — no major issues detected"))
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
                     title=title, color_discrete_sequence=PBI_COLORS)
    else:
        fig = px.bar(d, x=x, y=y, color=color, title=title,
                     color_discrete_sequence=PBI_COLORS, barmode="group")
    fig.update_traces(marker_line_width=0, marker_line_color="rgba(0,0,0,0)")
    return apply_theme(fig)

def line(df, x, y, color=None, title=""):
    fig = px.line(df, x=x, y=y, color=color, title=title,
                  color_discrete_sequence=PBI_COLORS, markers=True)
    fig.update_traces(line_width=2.5, marker_size=5)
    return apply_theme(fig)

def area(df, x, y, color=None, title=""):
    fig = px.area(df, x=x, y=y, color=color, title=title,
                  color_discrete_sequence=PBI_COLORS)
    fig.update_traces(line_width=2)
    return apply_theme(fig)

def donut(df, names, values, title="", hole=0.55):
    top = df.nlargest(10, values) if len(df) > 10 else df
    fig = px.pie(top, names=names, values=values, title=title,
                 hole=hole, color_discrete_sequence=PBI_COLORS)
    fig.update_traces(textinfo="percent+label", textfont_size=11,
                      pull=[0.04] + [0]*(len(top)-1))
    return apply_theme(fig)

def scatter(df, x, y, color=None, size=None, title="", trendline=False):
    kw = dict(trendline="ols") if trendline else {}
    fig = px.scatter(df, x=x, y=y, color=color, size=size, title=title,
                     color_discrete_sequence=PBI_COLORS, opacity=0.7, **kw)
    if trendline:
        fig.update_traces(selector=dict(mode="lines"),
                          line=dict(color=GOLD, width=2, dash="dot"))
    return apply_theme(fig)

def histogram(df, col, bins=30, color_col=None, title=""):
    fig = px.histogram(df, x=col, nbins=bins, color=color_col,
                       title=title, color_discrete_sequence=PBI_COLORS,
                       marginal="box")
    fig.update_traces(marker_line_color=BG, marker_line_width=0.5)
    return apply_theme(fig)

def box_plot(df, y, x=None, title=""):
    fig = px.box(df, x=x, y=y, title=title,
                 color_discrete_sequence=PBI_COLORS, points="outliers")
    fig.update_traces(marker_color=GOLD)
    return apply_theme(fig)

def heatmap_corr(df, num_cols):
    if len(num_cols) < 2: return None
    corr = df[num_cols].corr().round(2)
    fig = go.Figure(go.Heatmap(
        z=corr.values, x=corr.columns.tolist(), y=corr.index.tolist(),
        colorscale=[[0,RED],[0.5,CARD],[1,GREEN]],
        zmin=-1, zmax=1,
        text=corr.values, texttemplate="%{text:.2f}",
        hoverongaps=False,
    ))
    fig.update_layout(title="Correlation Matrix")
    return apply_theme(fig)

def waterfall(df, x_col, y_col, title=""):
    try:
        tmp = df[[x_col,y_col]].dropna().copy()
        tmp[x_col] = tmp[x_col].astype(str)
        d = tmp.groupby(x_col, as_index=False)[y_col].sum()
        d = d.sort_values(y_col, ascending=False).head(12)
        fig = go.Figure(go.Waterfall(
            x=d[x_col], y=d[y_col],
            connector={"line":{"color":BORDER}},
            increasing={"marker":{"color":GREEN}},
            decreasing={"marker":{"color":RED}},
            totals={"marker":{"color":GOLD}},
        ))
        fig.update_layout(title=title)
        return apply_theme(fig)
    except Exception as e:
        return go.Figure().update_layout(title=f"Error: {e}")

def funnel(df, cat_col, val_col, title=""):
    try:
        tmp = df[[cat_col,val_col]].dropna().copy()
        tmp[cat_col] = tmp[cat_col].astype(str)
        d = tmp.groupby(cat_col, as_index=False)[val_col].sum()
        d = d.sort_values(val_col, ascending=False).head(8)
        fig = go.Figure(go.Funnel(
            y=d[cat_col], x=d[val_col],
            marker={"color": PBI_COLORS[:len(d)]},
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
        d = tmp.groupby(path_cols, as_index=False)[val_col].sum()
        fig = px.treemap(d, path=path_cols, values=val_col, title=title,
                         color_discrete_sequence=PBI_COLORS)
        fig.update_traces(textinfo="label+value+percent parent", root_color=BG)
        return apply_theme(fig)
    except Exception as e:
        return go.Figure().update_layout(title=f"Error: {e}")

def gauge(value, title, max_v=None):
    if pd.isna(value) or value == 0: value = 0
    if max_v is None or max_v == 0: max_v = max(abs(value)*2, 1)
    pct = value / max_v
    color = GREEN if pct > 0.66 else (ORANGE if pct > 0.33 else RED)
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        number={"font":{"color":"#fff","size":22}, "valueformat":".2s"},
        gauge=dict(
            axis=dict(range=[0, max_v], tickfont={"color":"#9ca3af"},
                      tickformat=".2s", nticks=5),
            bar=dict(color=color, thickness=0.25),
            bgcolor=BG,
            borderwidth=0,
            steps=[
                dict(range=[0, max_v*0.33], color="#2a1a1a"),
                dict(range=[max_v*0.33, max_v*0.66], color="#2a1f12"),
                dict(range=[max_v*0.66, max_v], color="#122a1a"),
            ],
        ),
        title=dict(text=title, font=dict(color="#9ca3af", size=11)),
    ))
    fig.update_layout(height=220, margin=dict(l=20,r=20,t=50,b=10),
                      paper_bgcolor="rgba(0,0,0,0)")
    return fig

def multi_axis_line(df, date_col, metrics):
    """Multi-metric time series with shared x-axis."""
    n = len(metrics)
    if n == 0: return go.Figure()
    fig = make_subplots(rows=n, cols=1, shared_xaxes=True,
                        vertical_spacing=0.04,
                        subplot_titles=[f"▸ {m}" for m in metrics])
    for i, m in enumerate(metrics):
        tmp = df[[date_col, m]].dropna().groupby(date_col, as_index=False)[m].sum()
        c = PBI_COLORS[i % len(PBI_COLORS)]
        fig.add_trace(go.Scatter(
            x=tmp[date_col], y=tmp[m], name=m,
            line=dict(color=c, width=2.2),
            fill="tozeroy", fillcolor=hex_to_rgba(c, 0.08),
            hovertemplate=f"<b>%{{x}}</b><br>{m}: %{{y:,.2f}}<extra></extra>",
        ), row=i+1, col=1)
        # Rolling avg overlay
        if len(tmp) > 6:
            roll = tmp[m].rolling(min(7, len(tmp)//3), min_periods=1).mean()
            fig.add_trace(go.Scatter(
                x=tmp[date_col], y=roll, name=f"{m} (7-avg)",
                line=dict(color=c, width=1, dash="dot"),
                showlegend=False,
            ), row=i+1, col=1)
    layout = {k:v for k,v in PBI_LAYOUT.items() if k not in ("xaxis","yaxis")}
    fig.update_layout(height=220*n, showlegend=True, **layout)
    fig.update_annotations(font=dict(color=GOLD, size=11))
    return fig

def pareto_chart(df, cat_col, val_col, title="Pareto Analysis"):
    try:
        tmp = df[[cat_col, val_col]].dropna().copy()
        tmp[cat_col] = tmp[cat_col].astype(str)
        d = tmp.groupby(cat_col, as_index=False)[val_col].sum()
        d = d.sort_values(val_col, ascending=False).head(15)
        d["cumpct"] = d[val_col].cumsum() / d[val_col].sum() * 100
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Bar(x=d[cat_col], y=d[val_col], name=val_col,
                             marker_color=BLUE, marker_line_width=0), secondary_y=False)
        fig.add_trace(go.Scatter(x=d[cat_col], y=d["cumpct"], name="Cumulative %",
                                 line=dict(color=GOLD, width=2.5),
                                 mode="lines+markers", marker_size=6), secondary_y=True)
        fig.add_hline(y=80, line_dash="dot", line_color=RED, annotation_text="80%",
                      secondary_y=True)
        fig.update_layout(title=title)
        fig.update_yaxes(title_text=val_col, secondary_y=False,
                         gridcolor="#2a2a45", tickfont=dict(color="#9ca3af"))
        fig.update_yaxes(title_text="Cumulative %", secondary_y=True,
                         range=[0,105], tickfont=dict(color=GOLD),
                         gridcolor="rgba(0,0,0,0)")
        return apply_theme(fig)
    except Exception as e:
        return go.Figure().update_layout(title=f"Error: {e}")

def missing_heatmap(df):
    miss = df.isnull().astype(int)
    if miss.sum().sum() == 0: return None
    fig = px.imshow(miss.T, title="Missing Value Map",
                    color_continuous_scale=[[0,CARD],[1,RED]],
                    labels=dict(color="Missing"),
                    aspect="auto")
    fig.update_layout(coloraxis_showscale=False)
    return apply_theme(fig, height=max(200, len(df.columns)*22))

def outlier_scatter(df, col):
    s = df[col].dropna()
    mask = detect_outliers_iqr(s)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=s[~mask].index, y=s[~mask], mode="markers",
        name="Normal", marker=dict(color=BLUE, size=5, opacity=0.6)))
    fig.add_trace(go.Scatter(
        x=s[mask].index, y=s[mask], mode="markers",
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
        if piv.shape[1] > 20: piv = piv.iloc[:,:20]
        fig = px.imshow(piv, title=f"{val_col} — {row_col} × {col_col}",
                        color_continuous_scale=[[0,BG],[0.5,BLUE],[1,GOLD]],
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

# ══════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown(f"## 📊 BI Studio Pro <span class='pbi-badge'>EXPERT</span>", unsafe_allow_html=True)
    st.markdown("---")
    uploaded = st.file_uploader("📁 Upload File", type=["csv","xlsx"],
                                help="CSV or Excel — multiple sheets supported")
    st.markdown("---")
    st.markdown("### ⚙️ Settings")
    top_n_global = st.slider("Max categories in charts", 5, 30, 12)
    show_raw     = st.checkbox("Show raw values on charts", False)
    st.markdown("---")
    st.caption("BI Studio Pro · Data Analysis Expert Edition")

# ══════════════════════════════════════════════════════════════
#  HEADER
# ══════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="pbi-header">
    <span style="font-size:2.2rem">📊</span>
    <div>
        <h1>BI Studio Pro <span class="pbi-badge">EXPERT</span></h1>
        <p>Power BI-style Analytics Dashboard &nbsp;·&nbsp; {datetime.now().strftime("%A %d %B %Y")}</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  EMPTY STATE
# ══════════════════════════════════════════════════════════════
if uploaded is None:
    c1,c2,c3 = st.columns(3)
    for col, icon, title, desc in [
        (c1,"📂","Upload Any File","CSV or Excel, single or multi-sheet"),
        (c2,"🤖","Auto Analysis","Instant KPIs, insights & chart recommendations"),
        (c3,"📤","Export Results","Download filtered data, stats & reports"),
    ]:
        with col:
            st.markdown(f"""
            <div class="kpi-card" style="--accent:{GOLD}; text-align:center; padding:28px 20px;">
                <div style="font-size:2.5rem">{icon}</div>
                <div style="color:{GOLD};font-weight:600;margin:10px 0 6px;">{title}</div>
                <div style="color:#6b7280;font-size:0.82rem">{desc}</div>
            </div>""", unsafe_allow_html=True)
    st.markdown(f"<div style='text-align:center;padding:40px;color:#4b5563;'>← Upload a file in the sidebar to get started</div>", unsafe_allow_html=True)
    st.stop()

# ══════════════════════════════════════════════════════════════
#  LOAD DATA
# ══════════════════════════════════════════════════════════════
@st.cache_data(show_spinner="Loading data…")
def load_data(file_bytes, file_name):
    import io as _io
    f = _io.BytesIO(file_bytes)
    f.name = file_name
    sheets = safe_read(f)
    for k in sheets:
        sheets[k] = detect_and_parse_dates(sheets[k])
    return sheets

try:
    file_bytes = uploaded.read()
    sheets = load_data(file_bytes, uploaded.name)
except Exception as e:
    st.error(f"❌ **File read error:** {e}")
    st.info("Try: re-saving as CSV UTF-8, or check Excel sheet names.")
    st.stop()

# Sheet selector
sheet_names = list(sheets.keys())
sheet_name  = sheet_names[0]
if len(sheet_names) > 1:
    with st.sidebar:
        st.markdown("### 📑 Sheet")
        sheet_name = st.selectbox("Select sheet", sheet_names)

df_raw = sheets[sheet_name].copy()

# Drop fully-empty rows/cols
df_raw = df_raw.dropna(how="all").dropna(axis=1, how="all")
df_raw.columns = [str(c).strip() for c in df_raw.columns]

num_cols  = get_num_cols(df_raw)
cat_cols  = get_cat_cols(df_raw)
date_cols = get_date_cols(df_raw)
all_cols  = df_raw.columns.tolist()

# ══════════════════════════════════════════════════════════════
#  SIDEBAR FILTERS
# ══════════════════════════════════════════════════════════════
df = df_raw.copy()
with st.sidebar:
    st.markdown("---")
    st.markdown("### 🔍 Filters")
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
            if len(dr) == 2 and dr[0] != mn or (len(dr)==2 and dr[1] != mx):
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
tabs = st.tabs(["📈 Overview","📊 Charts","🔬 Analysis","🔍 Deep Dive","🗃️ Data","💾 Export"])
tab_overview, tab_charts, tab_analysis, tab_deep, tab_data, tab_export = tabs

# ══════════════════════════════════════════════════════════════
#  TAB 1 — OVERVIEW
# ══════════════════════════════════════════════════════════════
with tab_overview:
    # Data quality banner
    qs = data_quality_score(df_raw)
    qc = GREEN if qs>=80 else (ORANGE if qs>=50 else RED)
    ql = "Excellent" if qs>=80 else ("Needs Attention" if qs>=50 else "Poor")
    st.markdown(f"""
    <div class="kpi-card" style="--accent:{qc}; display:flex; align-items:center; gap:20px; margin-bottom:16px;">
        <div style="font-size:2rem">{"✅" if qs>=80 else ("⚠️" if qs>=50 else "❌")}</div>
        <div>
            <div class="kpi-label">Data Quality Score</div>
            <div class="kpi-value" style="color:{qc}">{qs:.0f} / 100 &nbsp;<span style="font-size:1rem;color:#9ca3af">— {ql}</span></div>
            <div class="kpi-sub">{len(df_raw):,} rows · {len(df_raw.columns)} cols · 
                {df_raw.isnull().mean().mean()*100:.1f}% missing · 
                {df_raw.duplicated().sum()} duplicates
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # KPI Cards
    if num_cols:
        st.markdown('<div class="sec">📌 Key Metrics</div>', unsafe_allow_html=True)
        accents = PBI_COLORS
        icons   = ["💰","📦","📊","🎯","⚡","🔥","💡","📐"]
        cards_html = '<div class="kpi-grid">'
        for i, col in enumerate(num_cols[:8]):
            total = df[col].sum()
            mean  = df[col].mean()
            cards_html += f"""
            <div class="kpi-card" style="--accent:{accents[i%len(accents)]}">
                <div class="kpi-icon">{icons[i%len(icons)]}</div>
                <div class="kpi-label">{col}</div>
                <div class="kpi-value">{fmt(total)}</div>
                <div class="kpi-sub">Avg {fmt(mean)} · Min {fmt(df[col].min())} · Max {fmt(df[col].max())}</div>
            </div>"""
        cards_html += "</div>"
        st.markdown(cards_html, unsafe_allow_html=True)

    # Gauges
    st.markdown('<div class="sec">🎯 Gauges</div>', unsafe_allow_html=True)
    gcols = st.columns(min(4, len(num_cols)))
    for i, nc in enumerate(num_cols[:4]):
        with gcols[i]:
            st.plotly_chart(gauge(df[nc].sum(), nc, df_raw[nc].sum()*1.2),
                            use_container_width=True)

    # Auto Smart Charts
    st.markdown('<div class="sec">📊 Smart Visuals</div>', unsafe_allow_html=True)
    if cat_cols and num_cols:
        c1, c2 = st.columns(2)
        with c1:
            try:
                d = safe_groupby(df, [cat_cols[0]], num_cols[0])
                d = d.nlargest(top_n_global, num_cols[0])
                st.plotly_chart(bar(d, cat_cols[0], num_cols[0],
                    title=f"Top {top_n_global}: {num_cols[0]} by {cat_cols[0]}",
                    orientation="h"), use_container_width=True)
            except Exception as e:
                st.warning(f"Chart error: {e}")
        with c2:
            try:
                d = safe_groupby(df, [cat_cols[0]], num_cols[0])
                st.plotly_chart(donut(d, cat_cols[0], num_cols[0],
                    title=f"{num_cols[0]} Share"), use_container_width=True)
            except Exception as e:
                st.warning(f"Chart error: {e}")

    if date_cols and num_cols:
        try:
            d = safe_groupby(df, [date_cols[0]], num_cols[0])
            d = d.sort_values(date_cols[0])
            st.plotly_chart(area(d, date_cols[0], num_cols[0],
                title=f"{num_cols[0]} Over Time"), use_container_width=True)
        except Exception as e:
            st.warning(f"Time series error: {e}")

    # Auto Insights
    st.markdown('<div class="sec">🤖 Auto Insights</div>', unsafe_allow_html=True)
    insights = auto_insights(df, num_cols, cat_cols, date_cols)
    for icon, color, text in insights:
        st.markdown(f"""
        <div class="insight-card" style="--c:{color}">
            {icon} &nbsp; {text}
        </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  TAB 2 — CHART BUILDER
# ══════════════════════════════════════════════════════════════
with tab_charts:
    st.markdown('<div class="sec">🛠️ Chart Builder</div>', unsafe_allow_html=True)

    chart_type = st.selectbox("Chart Type", [
        "Horizontal Bar","Vertical Bar","Grouped Bar",
        "Line Chart","Area Chart","Scatter Plot",
        "Donut Chart","Pie Chart","Histogram","Box Plot",
        "Waterfall","Funnel","Pareto Analysis",
    ], key="cht_type")

    cfg1, cfg2, cfg3 = st.columns(3)

    try:
        # ── Bar / Line / Area / Waterfall / Funnel ──
        if chart_type in ["Horizontal Bar","Vertical Bar","Grouped Bar",
                           "Line Chart","Area Chart","Waterfall","Funnel","Pareto Analysis"]:
            all_x = cat_cols + date_cols + num_cols
            with cfg1: x_col = st.selectbox("X / Category", all_x, key="cx")
            with cfg2: y_col = st.selectbox("Y / Value", num_cols or all_x, key="cy")
            with cfg3: color_col = st.selectbox("Color group", ["None"]+cat_cols, key="cc")
            color_col = None if color_col == "None" else color_col

            if chart_type in ["Horizontal Bar","Vertical Bar","Grouped Bar"]:
                d = safe_groupby(df, [x_col]+([color_col] if color_col else []), y_col)
                fig = bar(d, x_col, y_col, color_col,
                          title=f"{y_col} by {x_col}",
                          orientation="h" if chart_type=="Horizontal Bar" else "v",
                          top_n=top_n_global if not color_col else None)
            elif chart_type == "Line Chart":
                d = safe_groupby(df, [x_col]+([color_col] if color_col else []), y_col)
                d = d.sort_values(x_col)
                fig = line(d, x_col, y_col, color_col, f"{y_col} over {x_col}")
            elif chart_type == "Area Chart":
                d = safe_groupby(df, [x_col]+([color_col] if color_col else []), y_col)
                d = d.sort_values(x_col)
                fig = area(d, x_col, y_col, color_col, f"{y_col} Area")
            elif chart_type == "Waterfall":
                fig = waterfall(df, x_col, y_col, f"{y_col} Waterfall")
            elif chart_type == "Funnel":
                fig = funnel(df, x_col, y_col, f"{y_col} Funnel")
            elif chart_type == "Pareto Analysis":
                fig = pareto_chart(df, x_col, y_col)
            st.plotly_chart(fig, use_container_width=True)

        # ── Donut / Pie ──
        elif chart_type in ["Donut Chart","Pie Chart"]:
            with cfg1: names_c = st.selectbox("Category", cat_cols or all_cols, key="pn")
            with cfg2: vals_c  = st.selectbox("Values", num_cols or all_cols, key="pv")
            d = safe_groupby(df, [names_c], vals_c)
            hole = 0.55 if chart_type=="Donut Chart" else 0
            st.plotly_chart(donut(d, names_c, vals_c, chart_type, hole), use_container_width=True)

        # ── Scatter ──
        elif chart_type == "Scatter Plot":
            with cfg1: x_c = st.selectbox("X (numeric)", num_cols, key="sx")
            with cfg2: y_c = st.selectbox("Y (numeric)", num_cols, key="sy")
            with cfg3:
                col_c  = st.selectbox("Color", ["None"]+cat_cols, key="scc")
                size_c = st.selectbox("Size",  ["None"]+num_cols, key="ssc")
                trend  = st.checkbox("Trendline", True, key="str")
            col_c  = None if col_c  == "None" else col_c
            size_c = None if size_c == "None" else size_c
            # limit size for performance
            sample = df.sample(min(2000, len(df)), random_state=42)
            st.plotly_chart(scatter(sample, x_c, y_c, col_c, size_c,
                                    f"{y_c} vs {x_c}", trendline=trend),
                            use_container_width=True)

        # ── Histogram ──
        elif chart_type == "Histogram":
            with cfg1: col_h  = st.selectbox("Column", num_cols, key="hc")
            with cfg2: bins_h = st.slider("Bins", 5, 100, 30, key="hb")
            with cfg3: col_c  = st.selectbox("Color", ["None"]+cat_cols, key="hcc")
            col_c = None if col_c == "None" else col_c
            st.plotly_chart(histogram(df, col_h, bins_h, col_c, f"{col_h} Distribution"),
                            use_container_width=True)

        # ── Box Plot ──
        elif chart_type == "Box Plot":
            with cfg1: y_c = st.selectbox("Value", num_cols, key="bxy")
            with cfg2: x_c = st.selectbox("Group by", ["None"]+cat_cols, key="bxx")
            x_c = None if x_c == "None" else x_c
            st.plotly_chart(box_plot(df, y_c, x_c, f"{y_c} Distribution"),
                            use_container_width=True)

    except Exception as e:
        st.error(f"❌ Chart error: **{e}** — try different columns.")

# ══════════════════════════════════════════════════════════════
#  TAB 3 — ANALYSIS
# ══════════════════════════════════════════════════════════════
with tab_analysis:
    # Correlation heatmap
    st.markdown('<div class="sec">🔗 Correlation Matrix</div>', unsafe_allow_html=True)
    if len(num_cols) >= 2:
        fig_corr = heatmap_corr(df, num_cols)
        if fig_corr:
            st.plotly_chart(fig_corr, use_container_width=True)
    else:
        st.info("Need at least 2 numeric columns.")

    c1, c2 = st.columns(2)

    # Treemap
    with c1:
        st.markdown('<div class="sec">🗺️ Treemap</div>', unsafe_allow_html=True)
        if cat_cols and num_cols:
            path_sel = st.multiselect("Hierarchy", cat_cols,
                                       default=cat_cols[:min(2,len(cat_cols))], key="tpath")
            val_sel  = st.selectbox("Values", num_cols, key="tval")
            if path_sel:
                try:
                    st.plotly_chart(treemap(df, path_sel, val_sel), use_container_width=True)
                except Exception as e:
                    st.warning(f"Treemap error: {e}")
        else:
            st.info("Need categorical + numeric columns.")

    # Pivot heatmap
    with c2:
        st.markdown('<div class="sec">🔥 Pivot Heatmap</div>', unsafe_allow_html=True)
        if len(cat_cols) >= 2 and num_cols:
            r_col = st.selectbox("Rows",    cat_cols, key="pr")
            c_col = st.selectbox("Columns", cat_cols, index=min(1,len(cat_cols)-1), key="pc")
            v_col = st.selectbox("Values",  num_cols, key="pv2")
            if r_col != c_col:
                try:
                    st.plotly_chart(pivot_heatmap(df, r_col, c_col, v_col),
                                    use_container_width=True)
                except Exception as e:
                    st.warning(f"Pivot error: {e}")
            else:
                st.info("Row and column must be different.")
        else:
            st.info("Need at least 2 categorical columns.")

    # Multi-metric time series
    if date_cols and len(num_cols) >= 1:
        st.markdown('<div class="sec">📅 Multi-Metric Time Series</div>', unsafe_allow_html=True)
        dc_sel   = st.selectbox("Date column", date_cols, key="tsdc")
        met_sel  = st.multiselect("Metrics", num_cols, default=num_cols[:min(3,len(num_cols))], key="tsm")
        if met_sel:
            try:
                st.plotly_chart(multi_axis_line(df, dc_sel, met_sel), use_container_width=True)
            except Exception as e:
                st.warning(f"Time series error: {e}")

    # Statistical summary
    st.markdown('<div class="sec">📐 Statistical Summary</div>', unsafe_allow_html=True)
    if num_cols:
        try:
            stats = df[num_cols].describe().T.round(2)
            stats["skewness"] = df[num_cols].skew().round(2)
            stats["kurtosis"] = df[num_cols].kurt().round(2)
            stats["missing%"] = (df[num_cols].isnull().mean()*100).round(1)
            stats["outliers"] = [detect_outliers_iqr(df[c].dropna()).sum() for c in num_cols]
            # Style
            def style_stats(v):
                if pd.api.types.is_numeric_dtype(v):
                    return [f"color:{RED}" if (isinstance(x,float) and abs(x)>2) else "" for x in v]
                return [""]*len(v)
            st.dataframe(stats, use_container_width=True, height=300)
        except Exception as e:
            st.warning(f"Stats error: {e}")

# ══════════════════════════════════════════════════════════════
#  TAB 4 — DEEP DIVE
# ══════════════════════════════════════════════════════════════
with tab_deep:
    # Outlier analysis
    st.markdown('<div class="sec">🔎 Outlier Detection</div>', unsafe_allow_html=True)
    if num_cols:
        out_col = st.selectbox("Select column", num_cols, key="outcol")
        try:
            c1, c2 = st.columns([2,1])
            with c1:
                st.plotly_chart(outlier_scatter(df, out_col), use_container_width=True)
            with c2:
                s = df[out_col].dropna()
                mask = detect_outliers_iqr(s)
                n_out = mask.sum()
                q1, q3 = s.quantile(0.25), s.quantile(0.75)
                st.markdown(f"""
                <div class="kpi-card" style="--accent:{RED}; margin-top:10px;">
                    <div class="kpi-label">Outliers detected</div>
                    <div class="kpi-value" style="color:{RED}">{n_out}</div>
                    <div class="kpi-sub">{n_out/len(s)*100:.1f}% of non-null rows</div>
                </div>
                <div class="kpi-card" style="--accent:{BLUE}; margin-top:10px;">
                    <div class="kpi-label">IQR Bounds</div>
                    <div class="kpi-value" style="font-size:1.1rem">{fmt(q1-1.5*(q3-q1))} → {fmt(q3+1.5*(q3-q1))}</div>
                    <div class="kpi-sub">Q1={fmt(q1)} · Q3={fmt(q3)}</div>
                </div>
                """, unsafe_allow_html=True)
                if n_out:
                    st.dataframe(df[mask].head(20), use_container_width=True)
        except Exception as e:
            st.warning(f"Outlier error: {e}")

    # Missing value map
    st.markdown('<div class="sec">❓ Missing Value Analysis</div>', unsafe_allow_html=True)
    miss_summary = df.isnull().sum()
    miss_pct     = (df.isnull().mean()*100).round(1)
    miss_df      = pd.DataFrame({"Column":df.columns,"Missing":miss_summary,"Pct":miss_pct})
    miss_df      = miss_df[miss_df["Missing"]>0].sort_values("Missing",ascending=False)

    if len(miss_df):
        c1, c2 = st.columns([1,2])
        with c1:
            st.dataframe(miss_df, use_container_width=True)
        with c2:
            try:
                fig_m = missing_heatmap(df.sample(min(200,len(df)), random_state=1))
                if fig_m:
                    st.plotly_chart(fig_m, use_container_width=True)
            except Exception as e:
                st.warning(f"Missing map error: {e}")
    else:
        st.success("✅ No missing values!")

    # Distribution comparison
    st.markdown('<div class="sec">📊 Distribution Analysis</div>', unsafe_allow_html=True)
    if num_cols:
        dist_cols = st.multiselect("Columns to compare", num_cols,
                                    default=num_cols[:min(3,len(num_cols))], key="distcols")
        if dist_cols:
            try:
                n = len(dist_cols)
                fig_dist = make_subplots(rows=1, cols=n,
                                          subplot_titles=[f"▸ {c}" for c in dist_cols])
                for i, col in enumerate(dist_cols):
                    vals = df[col].dropna()
                    c_color = PBI_COLORS[i % len(PBI_COLORS)]
                    fig_dist.add_trace(
                        go.Histogram(x=vals, name=col, nbinsx=30,
                                     marker_color=c_color, opacity=0.8,
                                     marker_line_width=0),
                        row=1, col=i+1
                    )
                layout_d = {k:v for k,v in PBI_LAYOUT.items() if k not in ("xaxis","yaxis")}
                fig_dist.update_layout(height=320, showlegend=False, **layout_d)
                st.plotly_chart(fig_dist, use_container_width=True)
            except Exception as e:
                st.warning(f"Distribution error: {e}")

    # Pareto analysis
    if cat_cols and num_cols:
        st.markdown('<div class="sec">📊 Pareto Analysis (80/20 Rule)</div>', unsafe_allow_html=True)
        p_cat = st.selectbox("Category", cat_cols, key="pcat")
        p_val = st.selectbox("Value",    num_cols, key="pval")
        try:
            st.plotly_chart(pareto_chart(df, p_cat, p_val,
                            f"Pareto: {p_val} by {p_cat}"), use_container_width=True)
        except Exception as e:
            st.warning(f"Pareto error: {e}")

# ══════════════════════════════════════════════════════════════
#  TAB 5 — DATA
# ══════════════════════════════════════════════════════════════
with tab_data:
    st.markdown('<div class="sec">🗃️ Dataset</div>', unsafe_allow_html=True)

    # Metrics row
    m1,m2,m3,m4,m5 = st.columns(5)
    m1.metric("Rows",        f"{len(df):,}")
    m2.metric("Columns",     f"{len(df.columns)}")
    m3.metric("Numeric",     f"{len(num_cols)}")
    m4.metric("Categorical", f"{len(cat_cols)}")
    m5.metric("Missing %",   f"{df.isnull().mean().mean()*100:.1f}%")

    # Search
    search = st.text_input("🔍 Search rows", placeholder="Type anything…", key="search")
    display_df = df.copy()
    if search.strip():
        try:
            mask = display_df.apply(
                lambda c: c.astype(str).str.contains(search.strip(), case=False, na=False)
            )
            display_df = display_df[mask.any(axis=1)]
            st.caption(f"Found {len(display_df):,} matching rows")
        except Exception:
            pass

    n_show = st.slider("Rows to display", 10, min(1000, len(display_df)), 50)
    st.dataframe(display_df.head(n_show), use_container_width=True, height=400)

    # Column info
    st.markdown('<div class="sec">📋 Column Info</div>', unsafe_allow_html=True)
    col_info = pd.DataFrame({
        "Column":    df.columns,
        "Type":      df.dtypes.astype(str).values,
        "Non-Null":  df.count().values,
        "Null %":    (df.isnull().mean()*100).round(1).astype(str)+"%",
        "Unique":    df.nunique().values,
        "Sample":    [str(df[c].dropna().iloc[0]) if df[c].dropna().shape[0]>0 else "—"
                      for c in df.columns],
    })
    st.dataframe(col_info, use_container_width=True)

# ══════════════════════════════════════════════════════════════
#  TAB 6 — EXPORT
# ══════════════════════════════════════════════════════════════
with tab_export:
    st.markdown('<div class="sec">💾 Export Options</div>', unsafe_allow_html=True)
    e1,e2,e3 = st.columns(3)
    with e1:
        st.markdown(f"""<div class="kpi-card" style="--accent:{GOLD}">
        <div class="kpi-icon">📥</div><div class="kpi-label">Filtered Data</div>
        <div class="kpi-value" style="font-size:1.2rem">{len(df):,} rows</div></div>""",
        unsafe_allow_html=True)
        st.download_button("⬇️ Download CSV", to_csv(df),
                            "filtered_data.csv", "text/csv")
    with e2:
        st.markdown(f"""<div class="kpi-card" style="--accent:{BLUE}">
        <div class="kpi-icon">📊</div><div class="kpi-label">Excel Report</div>
        <div class="kpi-value" style="font-size:1.2rem">Data + Stats</div></div>""",
        unsafe_allow_html=True)
        st.download_button("⬇️ Download Excel", to_excel(df),
                            "bi_report.xlsx",
                            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    with e3:
        st.markdown(f"""<div class="kpi-card" style="--accent:{GREEN}">
        <div class="kpi-icon">📐</div><div class="kpi-label">Stats Summary</div>
        <div class="kpi-value" style="font-size:1.2rem">CSV</div></div>""",
        unsafe_allow_html=True)
        if num_cols:
            stats_exp = df[num_cols].describe().T
            stats_exp["skew"]     = df[num_cols].skew()
            stats_exp["kurtosis"] = df[num_cols].kurt()
            st.download_button("⬇️ Download Stats", to_csv(stats_exp),
                                "stats_summary.csv","text/csv")

    st.markdown("---")
    st.markdown('<div class="sec">🗂️ Dataset Metadata</div>', unsafe_allow_html=True)
    st.json({
        "filename":         uploaded.name,
        "sheet":            sheet_name,
        "rows_total":       len(df_raw),
        "rows_filtered":    len(df),
        "columns":          len(df.columns),
        "numeric_columns":  num_cols,
        "categorical_cols": cat_cols,
        "date_columns":     [str(c) for c in date_cols],
        "data_quality_score": f"{data_quality_score(df_raw):.0f}/100",
        "missing_pct":      f"{df_raw.isnull().mean().mean()*100:.2f}%",
        "duplicates":       int(df_raw.duplicated().sum()),
        "generated_at":     datetime.now().isoformat(),
    })

# Footer
st.markdown(f"""
<div style="text-align:center;padding:24px 0 8px;color:#374151;font-size:0.75rem;border-top:1px solid {BORDER};margin-top:20px;">
    BI Studio Pro · Expert Edition · Powered by Streamlit + Plotly + Pandas
</div>""", unsafe_allow_html=True)
