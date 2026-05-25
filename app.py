import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import io
from datetime import datetime

# ─────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────
st.set_page_config(
    page_title="BI Studio Pro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────
#  POWER BI DARK THEME CSS
# ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Segoe+UI:wght@300;400;600;700&display=swap');

/* ── Global ── */
html, body, [class*="css"] { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
.main        { background: #1b1b2f; color: #e0e0e0; }
.block-container { padding: 1.5rem 2rem; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #13131f;
    border-right: 1px solid #2a2a40;
}
[data-testid="stSidebar"] .stMarkdown h1,
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown h3 { color: #f2c94c; }

/* ── Top banner ── */
.pbi-header {
    background: linear-gradient(135deg, #0f0f23 0%, #1b1b3a 50%, #252547 100%);
    border-bottom: 2px solid #f2c94c;
    padding: 18px 28px;
    border-radius: 10px;
    margin-bottom: 22px;
    display: flex;
    align-items: center;
    gap: 16px;
}
.pbi-header h1 { color: #f2c94c; font-size: 1.8rem; margin: 0; font-weight: 700; }
.pbi-header p  { color: #9ca3af; margin: 0; font-size: 0.85rem; }
.pbi-logo { font-size: 2.4rem; }

/* ── KPI Cards ── */
.kpi-row { display: flex; gap: 16px; margin-bottom: 22px; flex-wrap: wrap; }
.kpi-card {
    flex: 1;
    min-width: 160px;
    background: #252540;
    border-radius: 10px;
    padding: 18px 20px;
    border-top: 4px solid var(--accent);
    box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    transition: transform 0.2s;
}
.kpi-card:hover { transform: translateY(-3px); }
.kpi-label { color: #9ca3af; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 6px; }
.kpi-value { color: #ffffff; font-size: 1.9rem; font-weight: 700; line-height: 1; }
.kpi-delta { font-size: 0.78rem; margin-top: 6px; }
.kpi-delta.up   { color: #4ade80; }
.kpi-delta.down { color: #f87171; }

/* ── Chart containers ── */
.chart-card {
    background: #252540;
    border-radius: 10px;
    padding: 16px;
    margin-bottom: 18px;
    border: 1px solid #2e2e50;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
}
.chart-title {
    color: #f2c94c;
    font-size: 0.95rem;
    font-weight: 600;
    margin-bottom: 10px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* ── Section dividers ── */
.section-header {
    color: #f2c94c;
    font-size: 1rem;
    font-weight: 600;
    border-left: 4px solid #f2c94c;
    padding-left: 10px;
    margin: 18px 0 12px 0;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* ── Streamlit widgets ── */
.stSelectbox label, .stMultiSelect label, .stSlider label { color: #d1d5db !important; }
div[data-baseweb="select"] > div { background: #1f1f38 !important; border-color: #3a3a5c !important; color: #e0e0e0 !important; }
.stDataFrame { border: 1px solid #2e2e50; border-radius: 8px; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] { background: #1b1b2f; border-bottom: 2px solid #f2c94c; }
.stTabs [data-baseweb="tab"]      { color: #9ca3af; font-weight: 500; }
.stTabs [aria-selected="true"]    { color: #f2c94c !important; border-bottom: 2px solid #f2c94c !important; }

/* ── Metric overrides ── */
[data-testid="stMetric"]          { background: #252540; padding: 14px; border-radius: 10px; border-left: 4px solid #f2c94c; }
[data-testid="stMetricLabel"]     { color: #9ca3af !important; font-size: 0.75rem !important; }
[data-testid="stMetricValue"]     { color: #ffffff !important; font-size: 1.8rem !important; }
[data-testid="stMetricDelta"]     { font-size: 0.8rem !important; }

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #f2c94c, #f59e0b);
    color: #1b1b2f;
    font-weight: 700;
    border: none;
    border-radius: 6px;
    padding: 8px 20px;
}
.stButton > button:hover { background: linear-gradient(135deg, #f59e0b, #d97706); color: #fff; }

/* ── Upload zone ── */
[data-testid="stFileUploader"] {
    background: #1f1f38;
    border: 2px dashed #3a3a5c;
    border-radius: 10px;
    padding: 12px;
}
[data-testid="stFileUploader"]:hover { border-color: #f2c94c; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #1b1b2f; }
::-webkit-scrollbar-thumb { background: #3a3a5c; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
#  POWER BI PLOTLY THEME
# ─────────────────────────────────────────
PBI_COLORS = [
    "#f2c94c", "#4e9af1", "#6fcf97", "#eb5757",
    "#9b59b6", "#f97316", "#06b6d4", "#ec4899",
]

PBI_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#d1d5db", family="Segoe UI, Tahoma, sans-serif", size=12),
    title_font=dict(color="#f2c94c", size=14),
    legend=dict(bgcolor="rgba(37,37,64,0.8)", bordercolor="#3a3a5c", borderwidth=1, font=dict(color="#d1d5db")),
    margin=dict(l=40, r=20, t=40, b=40),
    colorway=PBI_COLORS,
    xaxis=dict(gridcolor="#2e2e50", linecolor="#3a3a5c", tickcolor="#9ca3af", tickfont=dict(color="#9ca3af")),
    yaxis=dict(gridcolor="#2e2e50", linecolor="#3a3a5c", tickcolor="#9ca3af", tickfont=dict(color="#9ca3af")),
)

def apply_pbi_theme(fig):
    fig.update_layout(**PBI_LAYOUT)
    return fig

# ─────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────
def fmt_number(n):
    if pd.isna(n): return "—"
    if abs(n) >= 1_000_000: return f"{n/1_000_000:.1f}M"
    if abs(n) >= 1_000:     return f"{n/1_000:.1f}K"
    return f"{n:,.1f}"

def get_numeric_cols(df):
    return df.select_dtypes(include=np.number).columns.tolist()

def get_cat_cols(df):
    return df.select_dtypes(include=["object", "category"]).columns.tolist()

def get_date_cols(df):
    return df.select_dtypes(include=["datetime64"]).columns.tolist()

def safe_groupby(df, group_cols, value_col, agg="sum"):
    """Groupby that handles NaN, duplicate cols, and non-numeric value columns."""
    group_cols = [c for c in group_cols if c and c != value_col]
    if not group_cols:
        return df[[value_col]].copy()
    try:
        clean = df.dropna(subset=group_cols)
        # convert group cols to string to avoid multi-index issues
        clean = clean.copy()
        for c in group_cols:
            clean[c] = clean[c].astype(str)
        result = clean.groupby(group_cols, as_index=False)[value_col].agg(agg)
        return result
    except Exception:
        return pd.DataFrame(columns=group_cols + [value_col])

def detect_dates(df):
    for col in df.select_dtypes(include="object").columns:
        try:
            converted = pd.to_datetime(df[col], infer_datetime_format=True, errors="coerce")
            if converted.notna().sum() / len(df) > 0.6:
                df[col] = converted
        except Exception:
            pass
    return df

def read_file(f):
    if f.name.endswith(".csv"):
        try:
            return {"Sheet1": pd.read_csv(f, encoding="utf-8")}
        except UnicodeDecodeError:
            return {"Sheet1": pd.read_csv(f, encoding="latin-1")}
    else:
        xls = pd.ExcelFile(f)
        return {sheet: xls.parse(sheet) for sheet in xls.sheet_names}

# ─────────────────────────────────────────
#  KPI CARDS (custom HTML)
# ─────────────────────────────────────────
def render_kpi_cards(df):
    num_cols = get_numeric_cols(df)[:6]
    accents = ["#f2c94c", "#4e9af1", "#6fcf97", "#eb5757", "#9b59b6", "#f97316"]
    cols = st.columns(len(num_cols) if num_cols else 1)
    for i, col in enumerate(num_cols):
        val = df[col].sum()
        mean_val = df[col].mean()
        with cols[i]:
            st.markdown(f"""
            <div class="kpi-card" style="--accent:{accents[i % len(accents)]}">
                <div class="kpi-label">{col}</div>
                <div class="kpi-value">{fmt_number(val)}</div>
                <div class="kpi-delta up">⌀ Avg: {fmt_number(mean_val)}</div>
            </div>
            """, unsafe_allow_html=True)

# ─────────────────────────────────────────
#  CHART BUILDERS
# ─────────────────────────────────────────
def bar_chart(df, x, y, color=None, title="Bar Chart"):
    fig = px.bar(df, x=x, y=y, color=color, title=title,
                 color_discrete_sequence=PBI_COLORS, barmode="group")
    fig.update_traces(marker_line_width=0)
    return apply_pbi_theme(fig)

def line_chart(df, x, y, color=None, title="Line Chart"):
    fig = px.line(df, x=x, y=y, color=color, title=title,
                  color_discrete_sequence=PBI_COLORS, markers=True)
    fig.update_traces(line_width=2.5)
    return apply_pbi_theme(fig)

def area_chart(df, x, y, title="Area Chart"):
    fig = px.area(df, x=x, y=y, title=title,
                  color_discrete_sequence=PBI_COLORS)
    return apply_pbi_theme(fig)

def pie_donut(df, names, values, title="Donut Chart", hole=0.55):
    fig = px.pie(df, names=names, values=values, title=title, hole=hole,
                 color_discrete_sequence=PBI_COLORS)
    fig.update_traces(textinfo="percent+label", pull=[0.03]*len(df[names].unique()))
    return apply_pbi_theme(fig)

def scatter_chart(df, x, y, color=None, size=None, title="Scatter Chart"):
    fig = px.scatter(df, x=x, y=y, color=color, size=size, title=title,
                     color_discrete_sequence=PBI_COLORS, opacity=0.75)
    return apply_pbi_theme(fig)

def histogram_chart(df, col, bins=30, title="Distribution"):
    fig = px.histogram(df, x=col, nbins=bins, title=title,
                       color_discrete_sequence=["#f2c94c"])
    fig.update_traces(marker_line_color="#1b1b2f", marker_line_width=0.5)
    return apply_pbi_theme(fig)

def heatmap_chart(df, title="Correlation Heatmap"):
    num = df.select_dtypes(include=np.number)
    if num.shape[1] < 2:
        return None
    corr = num.corr()
    fig = go.Figure(go.Heatmap(
        z=corr.values, x=corr.columns, y=corr.index,
        colorscale=[[0,"#eb5757"],[0.5,"#252540"],[1,"#6fcf97"]],
        zmin=-1, zmax=1,
        text=np.round(corr.values, 2), texttemplate="%{text}",
    ))
    fig.update_layout(title=title)
    return apply_pbi_theme(fig)

def treemap_chart(df, path_cols, values_col, title="Treemap"):
    fig = px.treemap(df, path=path_cols, values=values_col, title=title,
                     color_discrete_sequence=PBI_COLORS)
    fig.update_traces(textinfo="label+percent parent+value")
    return apply_pbi_theme(fig)

def waterfall_chart(df, x_col, y_col, title="Waterfall"):
    try:
        clean = df[[x_col, y_col]].dropna()
        clean[x_col] = clean[x_col].astype(str)
        d = clean.groupby(x_col, as_index=False)[y_col].sum().head(15)
    except Exception:
        return go.Figure()
    fig = go.Figure(go.Waterfall(
        x=d[x_col].astype(str), y=d[y_col],
        connector={"line": {"color": "#3a3a5c"}},
        increasing={"marker": {"color": "#6fcf97"}},
        decreasing={"marker": {"color": "#eb5757"}},
    ))
    fig.update_layout(title=title)
    return apply_pbi_theme(fig)

def funnel_chart(df, x_col, y_col, title="Funnel"):
    try:
        clean = df[[x_col, y_col]].dropna()
        clean[x_col] = clean[x_col].astype(str)
        d = clean.groupby(x_col, as_index=False)[y_col].sum().sort_values(y_col, ascending=False).head(8)
    except Exception:
        return go.Figure()
    fig = go.Figure(go.Funnel(
        y=d[x_col].astype(str), x=d[y_col],
        marker={"color": PBI_COLORS[:len(d)]},
    ))
    fig.update_layout(title=title)
    return apply_pbi_theme(fig)

def gauge_chart(value, title, min_v=0, max_v=None):
    if max_v is None: max_v = value * 2 if value else 100
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        delta={"reference": max_v * 0.6},
        gauge=dict(
            axis=dict(range=[min_v, max_v], tickcolor="#9ca3af"),
            bar=dict(color="#f2c94c"),
            bgcolor="#1b1b2f",
            steps=[
                dict(range=[min_v, max_v*0.33], color="#eb5757"),
                dict(range=[max_v*0.33, max_v*0.66], color="#f97316"),
                dict(range=[max_v*0.66, max_v], color="#6fcf97"),
            ],
            threshold=dict(line=dict(color="#ffffff", width=3), value=max_v*0.8),
        ),
        title=dict(text=title, font=dict(color="#f2c94c")),
        number=dict(font=dict(color="#ffffff")),
    ))
    return apply_pbi_theme(fig)

def box_plot(df, y_col, x_col=None, title="Box Plot"):
    fig = px.box(df, x=x_col, y=y_col, title=title,
                 color_discrete_sequence=PBI_COLORS)
    return apply_pbi_theme(fig)

# ─────────────────────────────────────────
#  EXPORT HELPERS
# ─────────────────────────────────────────
def to_excel_bytes(df):
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as w:
        df.to_excel(w, index=False)
    return buf.getvalue()

# ─────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📊 BI Studio Pro")
    st.markdown("---")
    uploaded = st.file_uploader("Upload Data File", type=["csv", "xlsx"],
                                 help="Supports CSV and Excel (.xlsx)")
    st.markdown("---")
    st.markdown("### 🎨 Theme Accent")
    accent = st.color_picker("Accent Color", "#f2c94c")
    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.caption("Power BI-style analytics dashboard built with Streamlit + Plotly.")

# ─────────────────────────────────────────
#  HEADER
# ─────────────────────────────────────────
st.markdown(f"""
<div class="pbi-header">
    <span class="pbi-logo">📊</span>
    <div>
        <h1>BI Studio Pro</h1>
        <p>Power BI-style Analytics · {datetime.now().strftime("%A, %d %B %Y")}</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
#  NO FILE STATE
# ─────────────────────────────────────────
if uploaded is None:
    st.markdown("""
    <div style="text-align:center; padding:80px 20px; color:#6b7280;">
        <div style="font-size:5rem;">📂</div>
        <h2 style="color:#f2c94c; margin-top:16px;">Upload your data to get started</h2>
        <p style="font-size:1rem;">Supports CSV and Excel files · Auto-detects columns · 15+ chart types</p>
        <p style="font-size:0.85rem; margin-top:10px; color:#4b5563;">← Use the sidebar to upload your file</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ─────────────────────────────────────────
#  LOAD DATA
# ─────────────────────────────────────────
try:
    sheets = read_file(uploaded)
except Exception as e:
    st.error(f"❌ Failed to read file: {e}")
    st.stop()

sheet_name = list(sheets.keys())[0]
if len(sheets) > 1:
    with st.sidebar:
        st.markdown("### 📑 Sheet")
        sheet_name = st.selectbox("Select Sheet", list(sheets.keys()))

df_raw = sheets[sheet_name].copy()
df_raw = detect_dates(df_raw)

# Column type buckets
num_cols  = get_numeric_cols(df_raw)
cat_cols  = get_cat_cols(df_raw)
date_cols = get_date_cols(df_raw)

# ─────────────────────────────────────────
#  SIDEBAR FILTERS
# ─────────────────────────────────────────
df = df_raw.copy()
with st.sidebar:
    st.markdown("---")
    st.markdown("### 🔍 Filters")
    for col in cat_cols[:4]:
        opts = sorted(df_raw[col].dropna().unique().tolist())
        if len(opts) <= 30:
            sel = st.multiselect(f"{col}", opts, default=opts,
                                  key=f"filter_{col}")
            if sel:
                df = df[df[col].isin(sel)]
    if date_cols:
        dc = date_cols[0]
        mn, mx = df_raw[dc].min(), df_raw[dc].max()
        if pd.notna(mn) and pd.notna(mx):
            dr = st.date_input("Date Range", [mn, mx], key="date_filter")
            if len(dr) == 2:
                df = df[(df[dc] >= pd.Timestamp(dr[0])) & (df[dc] <= pd.Timestamp(dr[1]))]

# ─────────────────────────────────────────
#  TABS
# ─────────────────────────────────────────
tab_overview, tab_charts, tab_advanced, tab_data, tab_export = st.tabs([
    "📈 Overview", "📊 Charts", "🔬 Advanced", "🗃️ Data", "💾 Export"
])

# ══════════════════════════════════════
#  TAB 1 — OVERVIEW
# ══════════════════════════════════════
with tab_overview:
    st.markdown('<div class="section-header">KPI Summary</div>', unsafe_allow_html=True)
    render_kpi_cards(df)

    # Gauges for top 3 numeric cols
    if num_cols:
        st.markdown('<div class="section-header">Performance Gauges</div>', unsafe_allow_html=True)
        gcols = st.columns(min(3, len(num_cols)))
        for i, nc in enumerate(num_cols[:3]):
            with gcols[i]:
                fig = gauge_chart(df[nc].sum(), nc, max_v=df_raw[nc].sum()*1.2)
                fig.update_layout(height=260)
                st.plotly_chart(fig, use_container_width=True)

    # Auto smart charts
    st.markdown('<div class="section-header">Smart Visuals</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    if cat_cols and num_cols:
        with c1:
            try:
                agg = safe_groupby(df, [cat_cols[0]], num_cols[0])
                agg = agg.sort_values(num_cols[0], ascending=False).head(12)
                fig = bar_chart(agg, cat_cols[0], num_cols[0],
                                title=f"{num_cols[0]} by {cat_cols[0]}")
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.warning(f"Bar chart error: {e}")
        with c2:
            try:
                agg = safe_groupby(df, [cat_cols[0]], num_cols[0]).head(8)
                fig = pie_donut(agg, cat_cols[0], num_cols[0],
                                title=f"{num_cols[0]} Share")
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.warning(f"Donut chart error: {e}")

    if date_cols and num_cols:
        try:
            agg = safe_groupby(df, [date_cols[0]], num_cols[0])
            fig = area_chart(agg, date_cols[0], num_cols[0],
                             title=f"{num_cols[0]} Over Time")
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.warning(f"Time series error: {e}")

# ══════════════════════════════════════
#  TAB 2 — CHARTS BUILDER
# ══════════════════════════════════════
with tab_charts:
    st.markdown('<div class="section-header">Chart Builder</div>', unsafe_allow_html=True)

    chart_type = st.selectbox("Chart Type", [
        "Bar Chart", "Grouped Bar", "Line Chart", "Area Chart",
        "Scatter Plot", "Donut Chart", "Pie Chart",
        "Box Plot", "Histogram", "Waterfall", "Funnel"
    ])

    cfg1, cfg2, cfg3 = st.columns(3)

    if chart_type in ["Bar Chart", "Grouped Bar", "Line Chart", "Area Chart",
                       "Waterfall", "Funnel"]:
        all_cols = cat_cols + date_cols + num_cols
        with cfg1:
            x_col = st.selectbox("X Axis", all_cols, key="cb_x")
        with cfg2:
            y_col = st.selectbox("Y Axis", num_cols, key="cb_y") if num_cols else st.selectbox("Y Axis", all_cols, key="cb_y2")
        with cfg3:
            color_col = st.selectbox("Color / Group", ["None"] + cat_cols, key="cb_color")
        color_col = None if color_col == "None" else color_col

        try:
            group_cols = [x_col] + ([color_col] if color_col else [])
            agg_df = safe_groupby(df, group_cols, y_col)

            if chart_type in ["Bar Chart", "Grouped Bar"]:
                fig = bar_chart(agg_df, x_col, y_col, color_col, f"{y_col} by {x_col}")
            elif chart_type == "Line Chart":
                fig = line_chart(agg_df, x_col, y_col, color_col, f"{y_col} over {x_col}")
            elif chart_type == "Area Chart":
                fig = area_chart(agg_df, x_col, y_col, f"{y_col} Area")
            elif chart_type == "Waterfall":
                fig = waterfall_chart(df, x_col, y_col, f"{y_col} Waterfall")
            elif chart_type == "Funnel":
                fig = funnel_chart(df, x_col, y_col, f"{y_col} Funnel")
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"❌ Chart error: {e}. Try different columns.")

    elif chart_type in ["Donut Chart", "Pie Chart"]:
        with cfg1:
            names_col = st.selectbox("Category", cat_cols or num_cols, key="pie_name")
        with cfg2:
            vals_col = st.selectbox("Values", num_cols, key="pie_val") if num_cols else st.selectbox("Values", cat_cols, key="pie_val2")
        hole = 0.55 if chart_type == "Donut Chart" else 0
        try:
            agg_df = safe_groupby(df, [names_col], vals_col)
            agg_df = agg_df.head(12)
            fig = pie_donut(agg_df, names_col, vals_col, chart_type, hole)
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"❌ Chart error: {e}")

    elif chart_type == "Scatter Plot":
        with cfg1:
            x_col = st.selectbox("X Axis", num_cols, key="sc_x")
        with cfg2:
            y_col = st.selectbox("Y Axis", num_cols, key="sc_y")
        with cfg3:
            color_col = st.selectbox("Color", ["None"] + cat_cols, key="sc_color")
            size_col = st.selectbox("Size", ["None"] + num_cols, key="sc_size")
        color_col = None if color_col == "None" else color_col
        size_col  = None if size_col  == "None" else size_col
        fig = scatter_chart(df, x_col, y_col, color_col, size_col, f"{y_col} vs {x_col}")
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Box Plot":
        with cfg1:
            y_col = st.selectbox("Value Column", num_cols, key="box_y")
        with cfg2:
            x_col = st.selectbox("Group By", ["None"] + cat_cols, key="box_x")
        x_col = None if x_col == "None" else x_col
        fig = box_plot(df, y_col, x_col, f"{y_col} Distribution")
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Histogram":
        with cfg1:
            col = st.selectbox("Column", num_cols, key="hist_col")
        with cfg2:
            bins = st.slider("Bins", 5, 100, 30, key="hist_bins")
        fig = histogram_chart(df, col, bins, f"{col} Distribution")
        st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════
#  TAB 3 — ADVANCED
# ══════════════════════════════════════
with tab_advanced:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="section-header">Correlation Heatmap</div>', unsafe_allow_html=True)
        fig = heatmap_chart(df)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Need at least 2 numeric columns for correlation heatmap.")

    with c2:
        st.markdown('<div class="section-header">Treemap</div>', unsafe_allow_html=True)
        if cat_cols and num_cols:
            path_sel = st.multiselect("Path (hierarchy)", cat_cols, default=cat_cols[:min(2,len(cat_cols))], key="tm_path")
            val_sel  = st.selectbox("Values", num_cols, key="tm_val")
            if path_sel:
                try:
                    agg_tm = safe_groupby(df, path_sel, val_sel)
                    fig = treemap_chart(agg_tm, path_sel, val_sel, "Treemap")
                    st.plotly_chart(fig, use_container_width=True)
                except Exception as e:
                    st.warning(f"Treemap error: {e}")
        else:
            st.info("Need categorical and numeric columns for treemap.")

    # Multi-metric line
    if date_cols and len(num_cols) > 1:
        st.markdown('<div class="section-header">Multi-Metric Time Series</div>', unsafe_allow_html=True)
        dc = st.selectbox("Date Column", date_cols, key="ts_date")
        metrics = st.multiselect("Metrics", num_cols, default=num_cols[:2], key="ts_metrics")
        if metrics:
            ts_df = df.groupby(dc)[metrics].sum().reset_index()
            fig = make_subplots(rows=len(metrics), cols=1, shared_xaxes=True,
                                vertical_spacing=0.05)
            for i, m in enumerate(metrics):
                fig.add_trace(
                    go.Scatter(x=ts_df[dc], y=ts_df[m], name=m,
                               line=dict(color=PBI_COLORS[i], width=2),
                               fill="tozeroy", fillcolor=f"rgba({','.join(str(int(PBI_COLORS[i].lstrip('#')[j:j+2], 16)) for j in (0,2,4))},0.1)"),
                    row=i+1, col=1
                )
            fig.update_layout(height=280*len(metrics), title="Multi-Metric Time Series",
                               showlegend=True, **{k: v for k, v in PBI_LAYOUT.items()
                                                    if k not in ("xaxis","yaxis")})
            st.plotly_chart(fig, use_container_width=True)

    # Statistical summary
    st.markdown('<div class="section-header">Statistical Summary</div>', unsafe_allow_html=True)
    if num_cols:
        stats = df[num_cols].describe().T
        stats["skewness"] = df[num_cols].skew()
        stats["kurtosis"] = df[num_cols].kurt()
        st.dataframe(stats.style.format("{:.2f}").background_gradient(
            cmap="YlOrRd", subset=["mean", "std"]), use_container_width=True)

# ══════════════════════════════════════
#  TAB 4 — DATA
# ══════════════════════════════════════
with tab_data:
    st.markdown('<div class="section-header">Dataset Preview</div>', unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Rows",    f"{len(df):,}")
    m2.metric("Columns", f"{len(df.columns):,}")
    m3.metric("Numeric", f"{len(num_cols)}")
    m4.metric("Missing", f"{df.isnull().sum().sum():,}")

    search = st.text_input("🔍 Search in data", placeholder="Type to filter rows…")
    display_df = df
    if search:
        mask = df.apply(lambda col: col.astype(str).str.contains(search, case=False, na=False))
        display_df = df[mask.any(axis=1)]

    n_rows = st.slider("Rows to display", 10, min(500, len(display_df)), 50)
    st.dataframe(display_df.head(n_rows), use_container_width=True, height=420)

    st.markdown('<div class="section-header">Column Info</div>', unsafe_allow_html=True)
    col_info = pd.DataFrame({
        "Column": df.columns,
        "Type": df.dtypes.astype(str).values,
        "Non-Null": df.count().values,
        "Null %": (df.isnull().mean() * 100).round(1).values,
        "Unique": df.nunique().values,
    })
    st.dataframe(col_info, use_container_width=True)

# ══════════════════════════════════════
#  TAB 5 — EXPORT
# ══════════════════════════════════════
with tab_export:
    st.markdown('<div class="section-header">Export Options</div>', unsafe_allow_html=True)
    ec1, ec2, ec3 = st.columns(3)

    with ec1:
        st.markdown("#### 📥 Filtered Data (CSV)")
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("Download CSV", csv, "filtered_data.csv", "text/csv")

    with ec2:
        st.markdown("#### 📊 Filtered Data (Excel)")
        excel_bytes = to_excel_bytes(df)
        st.download_button("Download Excel", excel_bytes,
                            "filtered_data.xlsx",
                            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    with ec3:
        st.markdown("#### 📋 Summary Stats (CSV)")
        if num_cols:
            stats_csv = df[num_cols].describe().to_csv().encode("utf-8")
            st.download_button("Download Stats", stats_csv, "stats_summary.csv", "text/csv")

    st.markdown("---")
    st.markdown("#### 🗂️ Full Data Info")
    st.json({
        "filename": uploaded.name,
        "sheet": sheet_name,
        "rows": len(df),
        "columns": list(df.columns),
        "numeric_columns": num_cols,
        "categorical_columns": cat_cols,
        "date_columns": [str(c) for c in date_cols],
    })

# ─────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding:30px 0 10px; color:#4b5563; font-size:0.78rem;">
    BI Studio Pro · Powered by Streamlit + Plotly · Built for professional analytics
</div>
""", unsafe_allow_html=True)
