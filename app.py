"""
Honda US Market Analysis — Interactive Dashboard
================================================
Redesigned: Dark Neutral + Honda Red Accent
Minimalist, no emoji icons, high readability.

Run: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Honda US Market Analysis",
    page_icon="assets/favicon.ico" if False else None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# DESIGN TOKENS
# ============================================================
# Dark neutral palette with Honda red accent
# BG_BASE      — deep charcoal canvas
# BG_SURFACE   — slightly lighter card surface
# BG_ELEVATED  — hover/active surface
# BORDER       — subtle rule color
# TEXT_PRIMARY — near-white
# TEXT_MUTED   — secondary labels
# RED          — Honda red accent (classic #CC0000 Honda brand)
# RED_DIM      — muted red for fills / backgrounds

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* ── Tokens ──────────────────────────────── */
:root {
    --bg-base:       #111214;
    --bg-surface:    #1A1C1F;
    --bg-elevated:   #222529;
    --border:        #2C2F34;
    --border-strong: #3A3D42;
    --text-primary:  #F0F1F3;
    --text-secondary:#9DA3AE;
    --text-muted:    #5C6370;
    --red:           #CC0000;
    --red-dim:       rgba(204,0,0,0.12);
    --red-hover:     #E60000;
    --radius:        8px;
    --radius-lg:     12px;
}

/* ── Reset & Base ─────────────────────────── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: var(--bg-base) !important;
    color: var(--text-primary) !important;
}

/* Main content area */
.main .block-container {
    padding: 1.5rem 2rem 3rem 2rem;
    max-width: 1400px;
}

/* ── Sidebar ──────────────────────────────── */
[data-testid="stSidebar"] {
    background-color: var(--bg-surface) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * {
    color: var(--text-primary) !important;
}
[data-testid="stSidebar"] .stRadio label,
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label,
[data-testid="stSidebar"] .stSlider label {
    color: var(--text-secondary) !important;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-weight: 600;
}
[data-testid="stSidebar"] hr {
    border-color: var(--border) !important;
}

/* Sidebar radio — nav items */
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
    padding: 0.45rem 0.75rem;
    border-radius: var(--radius);
    transition: background 0.15s;
    font-size: 0.875rem !important;
    font-weight: 500 !important;
    text-transform: none !important;
    letter-spacing: 0 !important;
    color: var(--text-secondary) !important;
    cursor: pointer;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {
    background: var(--bg-elevated) !important;
    color: var(--text-primary) !important;
}

/* Sidebar meta labels */
.sidebar-meta {
    font-size: 0.75rem;
    color: var(--text-muted);
    line-height: 2;
}
.sidebar-meta span {
    color: var(--text-secondary);
    font-weight: 500;
}

/* ── Page Header ──────────────────────────── */
.page-header {
    border-left: 3px solid var(--red);
    padding: 0.5rem 0 0.5rem 1rem;
    margin-bottom: 1.75rem;
}
.page-header h1 {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--text-primary);
    margin: 0 0 0.2rem 0;
    letter-spacing: -0.02em;
    line-height: 1.3;
}
.page-header p {
    font-size: 0.875rem;
    color: var(--text-secondary);
    margin: 0;
    font-weight: 400;
}

/* ── KPI Cards ────────────────────────────── */
.kpi-card {
    background: var(--bg-surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 1.25rem 1.25rem 1rem 1.25rem;
}
.kpi-label {
    font-size: 0.7rem;
    font-weight: 600;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 0.4rem;
}
.kpi-value {
    font-size: 1.75rem;
    font-weight: 700;
    color: var(--text-primary);
    line-height: 1.1;
    letter-spacing: -0.03em;
}
.kpi-value.accent {
    color: var(--red);
}

/* ── Section Labels ───────────────────────── */
.section-label {
    font-size: 0.7rem;
    font-weight: 700;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin: 0 0 0.75rem 0;
}

/* ── Chart Wrapper ────────────────────────── */
.chart-card {
    background: var(--bg-surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 1.25rem 1.25rem 0.5rem 1.25rem;
    margin-bottom: 0.25rem;
}
.chart-card .section-label {
    margin-bottom: 0.5rem;
}

/* ── Tabs ─────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    gap: 0;
    border-bottom: 1px solid var(--border) !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--text-muted) !important;
    border-radius: 0 !important;
    font-size: 0.8rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    padding: 0.6rem 1rem !important;
    border-bottom: 2px solid transparent !important;
}
.stTabs [aria-selected="true"] {
    color: var(--text-primary) !important;
    border-bottom: 2px solid var(--red) !important;
}

/* ── Dataframe ────────────────────────────── */
[data-testid="stDataFrame"] {
    border-radius: var(--radius) !important;
}

/* ── Divider ──────────────────────────────── */
hr {
    border-color: var(--border) !important;
}

/* ── Info / Caption ───────────────────────── */
.stCaption, .caption-note {
    font-size: 0.75rem;
    color: var(--text-muted) !important;
}

/* ── Footer ───────────────────────────────── */
.dashboard-footer {
    margin-top: 3rem;
    padding-top: 1.25rem;
    border-top: 1px solid var(--border);
    font-size: 0.75rem;
    color: var(--text-muted);
    display: flex;
    justify-content: space-between;
    align-items: center;
}

/* ── Scrollbar ────────────────────────────── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg-base); }
::-webkit-scrollbar-thumb { background: var(--border-strong); border-radius: 3px; }

/* Hide Streamlit chrome */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }

/* Streamlit selectbox / multiselect dark fix */
[data-baseweb="select"] {
    background-color: var(--bg-elevated) !important;
}
[data-baseweb="select"] * {
    background-color: var(--bg-elevated) !important;
    color: var(--text-primary) !important;
}
[data-baseweb="popover"] * {
    background-color: var(--bg-elevated) !important;
    color: var(--text-primary) !important;
}
</style>
"""

st.markdown(CSS, unsafe_allow_html=True)

# ============================================================
# PLOTLY THEME (dark, matches dashboard)
# ============================================================
PLOT_BG    = "#1A1C1F"
GRID_COLOR = "#2C2F34"
TEXT_COLOR = "#9DA3AE"
FONT_FAM   = "Inter"

def dark_layout(fig, height=400, **kwargs):
    """Apply the dashboard dark theme to any Plotly figure."""
    fig.update_layout(
        height=height,
        paper_bgcolor=PLOT_BG,
        plot_bgcolor=PLOT_BG,
        font=dict(family=FONT_FAM, color=TEXT_COLOR, size=12),
        margin=dict(l=8, r=8, t=24, b=8),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            bordercolor=GRID_COLOR,
            borderwidth=1,
            font=dict(size=11)
        ),
        **kwargs
    )
    fig.update_xaxes(
        gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR,
        tickfont=dict(size=11), title_font=dict(size=11)
    )
    fig.update_yaxes(
        gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR,
        tickfont=dict(size=11), title_font=dict(size=11)
    )
    return fig

# Minimal color palette red anchor + muted neutrals
PALETTE = [
    "#CC0000",   # honda red
    "#E8E8E8",   # near-white
    "#7A8394",   # mid-grey
    "#4A5568",   # dark-grey
    "#A0C4FF",   # soft blue
    "#FFD166",   # muted gold
    "#6FFFE9",   # teal
    "#BFA2DB",   # lavender
    "#F4A261",   # amber
    "#52B788",   # green
]

RED   = "#CC0000"
WHITE = "#E8E8E8"
GREY  = "#7A8394"

# ============================================================
# DATA
# ============================================================
@st.cache_data
def load_data():
    df = pd.read_csv('honda_cleaned.csv')
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("`honda_cleaned.csv` not found. Please ensure the file is in the same directory.")
    st.stop()

# ============================================================
# HELPERS
# ============================================================
def kpi(label, value, accent=False):
    accent_class = " accent" if accent else ""
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value{accent_class}">{value}</div>
    </div>
    """, unsafe_allow_html=True)

def section(text):
    st.markdown(f'<div class="section-label">{text}</div>', unsafe_allow_html=True)

def header(title, subtitle=""):
    sub = f"<p>{subtitle}</p>" if subtitle else ""
    st.markdown(f"""
    <div class="page-header">
        <h1>{title}</h1>
        {sub}
    </div>
    """, unsafe_allow_html=True)

def fmt_price(v):
    return f"${v:,.0f}"

def spacer(h="0.75rem"):
    st.markdown(f"<div style='height:{h}'></div>", unsafe_allow_html=True)

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("""
    <div style='padding:1rem 0 0.5rem 0'>
        <div style='font-size:0.65rem;font-weight:700;color:#5C6370;
                    text-transform:uppercase;letter-spacing:0.12em;
                    margin-bottom:0.25rem'>Dashboard</div>
        <div style='font-size:1.05rem;font-weight:700;color:#F0F1F3;
                    letter-spacing:-0.01em'>Honda US Market</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    page = st.radio(
        "Navigate",
        ["Executive Overview",
         "Pricing & Depreciation",
         "Consumer Satisfaction",
         "Hybrid vs Gasoline",
         "Market Geography"],
        label_visibility="collapsed"
    )

    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="sidebar-meta">
        <div>Listings &nbsp;<span>{len(df):,}</span></div>
        <div>Years &nbsp;<span>{int(df['Year'].min())}–{int(df['Year'].max())}</span></div>
        <div>Models &nbsp;<span>{df['Model_Family'].nunique()}</span></div>
        <div>States &nbsp;<span>{df['State'].nunique()}</span></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size:0.7rem;color:#5C6370;line-height:1.6'>
        Portfolio Project<br>Built with Streamlit & Plotly
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# PAGE 1: EXECUTIVE OVERVIEW
# ============================================================
if page == "Executive Overview":
    header(
        "Executive Overview",
        "Honda vehicle listings across the United States"
    )

    # KPIs
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: kpi("Total Listings", f"{len(df):,}")
    with c2: kpi("Median Price", fmt_price(df['Price'].median()), accent=True)
    with c3: kpi("Avg Rating", f"{df['Consumer_Rating'].mean():.2f}")
    with c4: kpi("Hybrid Share", f"{df['Is_Hybrid'].sum()/len(df)*100:.1f}%")
    with c5:
        new_pct = df['Condition'].value_counts().get('New', 0) / len(df) * 100
        kpi("New Vehicles", f"{new_pct:.1f}%")

    spacer("1.25rem")

    # Row 1
    col_l, col_r = st.columns([3, 2], gap="medium")

    with col_l:
        section("Top Model Families by Volume")
        mc = df['Model_Family'].value_counts().head(10).reset_index()
        mc.columns = ['Model Family', 'Count']
        fig = px.bar(
            mc, x='Count', y='Model Family', orientation='h',
            color_discrete_sequence=[RED]
        )
        fig.update_traces(marker_line_width=0)
        fig.update_layout(
            yaxis={'categoryorder': 'total ascending'},
            xaxis_title="Listings", yaxis_title=""
        )
        dark_layout(fig, height=380)
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        section("Condition Breakdown")
        cc = df['Condition'].value_counts().reset_index()
        cc.columns = ['Condition', 'Count']
        fig = px.pie(
            cc, values='Count', names='Condition',
            color_discrete_sequence=[RED, WHITE, GREY],
            hole=0.62
        )
        fig.update_traces(
            textinfo='label+percent',
            textfont_size=11,
            marker=dict(line=dict(color=PLOT_BG, width=2))
        )
        fig.update_layout(
            showlegend=False,
            annotations=[dict(
                text=f"<b>{len(df):,}</b>",
                x=0.5, y=0.5,
                font=dict(size=18, color="#F0F1F3", family=FONT_FAM),
                showarrow=False
            )]
        )
        dark_layout(fig, height=380)
        st.plotly_chart(fig, use_container_width=True)

    spacer()

    # Row 2
    col_l2, col_r2 = st.columns(2, gap="medium")

    with col_l2:
        section("Price Distribution by Condition")
        fig = px.box(
            df, x='Condition', y='Price', color='Condition',
            color_discrete_sequence=[RED, WHITE, GREY],
            category_orders={'Condition': ['New', 'Honda Certified', 'Used']}
        )
        fig.update_traces(
            line_color=GRID_COLOR,
            marker=dict(opacity=0.4, size=3)
        )
        fig.update_layout(showlegend=False, yaxis_title="Price (USD)", xaxis_title="")
        dark_layout(fig, height=380)
        st.plotly_chart(fig, use_container_width=True)

    with col_r2:
        section("Listings by Model Year")
        yc = df[df['Year'] >= 2010].groupby('Year').size().reset_index(name='Count')
        fig = px.area(
            yc, x='Year', y='Count',
            color_discrete_sequence=[RED]
        )
        fig.update_traces(
            fill='tozeroy',
            fillcolor='rgba(204,0,0,0.1)',
            line=dict(color=RED, width=1.5)
        )
        fig.update_layout(yaxis_title="Listings", xaxis_title="")
        dark_layout(fig, height=380)
        st.plotly_chart(fig, use_container_width=True)


# ============================================================
# PAGE 2: PRICING & DEPRECIATION
# ============================================================
elif page == "Pricing & Depreciation":
    header(
        "Pricing & Depreciation",
        "How Honda vehicles are priced and how value changes over time"
    )

    with st.sidebar:
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('<div style="font-size:0.7rem;font-weight:700;color:#5C6370;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.5rem">Filters</div>', unsafe_allow_html=True)
        sel_cond = st.multiselect(
            "Condition", df['Condition'].unique().tolist(),
            default=df['Condition'].unique().tolist(), key="p2_cond"
        )
        sel_models = st.multiselect(
            "Model Family", sorted(df['Model_Family'].unique().tolist()),
            default=sorted(df['Model_Family'].value_counts().head(6).index.tolist()), key="p2_model"
        )
        yr_range = st.slider(
            "Year Range", int(df['Year'].min()), int(df['Year'].max()),
            (2015, int(df['Year'].max())), key="p2_yr"
        )

    dff = df[
        df['Condition'].isin(sel_cond) &
        df['Model_Family'].isin(sel_models) &
        df['Year'].between(yr_range[0], yr_range[1])
    ]

    c1, c2, c3, c4 = st.columns(4)
    with c1: kpi("Filtered Listings", f"{len(dff):,}")
    with c2: kpi("Average Price", fmt_price(dff['Price'].mean()), accent=True)
    with c3: kpi("Median Price", fmt_price(dff['Price'].median()))
    with c4: kpi("Std Deviation", f"${dff['Price'].std():,.0f}")

    spacer("1.25rem")

    col_l, col_r = st.columns(2, gap="medium")

    with col_l:
        section("Average Price by Model Family")
        mp = (dff.groupby('Model_Family')['Price']
              .agg(['mean', 'median', 'count'])
              .sort_values('mean', ascending=True)
              .reset_index())
        mp.columns = ['Model Family', 'Mean', 'Median', 'Count']
        fig = px.bar(
            mp, x='Mean', y='Model Family', orientation='h',
            color_discrete_sequence=[RED],
            hover_data={'Median': ':$,.0f', 'Count': ':,'}
        )
        fig.update_traces(marker_line_width=0)
        fig.update_layout(xaxis_title="Average Price (USD)", yaxis_title="")
        dark_layout(fig, height=420)
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        section("Price Distribution by Condition")
        fig = px.violin(
            dff, x='Condition', y='Price', color='Condition',
            box=True, points=False,
            color_discrete_sequence=[RED, WHITE, GREY],
            category_orders={'Condition': ['New', 'Honda Certified', 'Used']}
        )
        fig.update_layout(showlegend=False, yaxis_title="Price (USD)", xaxis_title="")
        dark_layout(fig, height=420)
        st.plotly_chart(fig, use_container_width=True)

    spacer()
    section("Price vs Vehicle Age Depreciation Curve")
    df_dep = dff[dff['Vehicle_Age'] >= 0].copy()
    fig = px.scatter(
        df_dep, x='Vehicle_Age', y='Price', color='Model_Family',
        opacity=0.45, trendline="lowess",
        color_discrete_sequence=PALETTE,
        labels={'Vehicle_Age': 'Vehicle Age (years)', 'Price': 'Price (USD)'}
    )
    fig.update_traces(marker=dict(size=4), selector=dict(mode='markers'))
    fig.update_layout(legend_title="")
    dark_layout(fig, height=460)
    st.plotly_chart(fig, use_container_width=True)

    spacer()
    section("Price vs Mileage Used & Certified")
    df_mil = dff[
        dff['Condition'].isin(['Used', 'Honda Certified']) &
        dff['Mileage'].notna() &
        (dff['Mileage'] > 0) &
        (dff['Mileage'] < 300000)
    ]
    if len(df_mil) > 0:
        fig = px.scatter(
            df_mil, x='Mileage', y='Price', color='Model_Family',
            opacity=0.45, trendline="lowess",
            color_discrete_sequence=PALETTE,
            labels={'Mileage': 'Mileage (mi)', 'Price': 'Price (USD)'}
        )
        fig.update_traces(marker=dict(size=4), selector=dict(mode='markers'))
        fig.update_layout(legend_title="")
        dark_layout(fig, height=460)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No used/certified vehicles with mileage data match the current filters.")


# ============================================================
# PAGE 3: CONSUMER SATISFACTION
# ============================================================
elif page == "Consumer Satisfaction":
    header(
        "Consumer Satisfaction",
        "Six rating dimensions across Honda model families"
    )

    df_rated = df[df['Has_Ratings'] == True].copy()
    rating_cols = [
        'Comfort_Rating', 'Interior_Design_Rating', 'Performance_Rating',
        'Value_For_Money_Rating', 'Exterior_Styling_Rating', 'Reliability_Rating'
    ]
    short_names = ['Comfort', 'Interior Design', 'Performance', 'Value for Money', 'Exterior Styling', 'Reliability']

    with st.sidebar:
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('<div style="font-size:0.7rem;font-weight:700;color:#5C6370;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.5rem">Compare Models</div>', unsafe_allow_html=True)
        models_radar = st.multiselect(
            "Model Families",
            sorted(df_rated['Model_Family'].unique().tolist()),
            default=sorted(df_rated['Model_Family'].value_counts().head(4).index.tolist()),
            key="p3_models"
        )

    c1, c2, c3, c4 = st.columns(4)
    with c1: kpi("Rated Listings", f"{len(df_rated):,}")
    with c2:
        best_dim = pd.Series(df_rated[rating_cols].mean().values, index=short_names).idxmax()
        kpi("Highest Dimension", best_dim)
    with c3: kpi("Overall Rating", f"{df_rated['Consumer_Rating'].mean():.2f}", accent=True)
    with c4: kpi("Avg Reliability", f"{df_rated['Reliability_Rating'].mean():.2f}")

    spacer("1.25rem")

    col_l, col_r = st.columns([3, 2], gap="medium")

    with col_l:
        section("Rating Radar Model Comparison")
        if models_radar:
            fig = go.Figure()
            for i, model in enumerate(models_radar):
                sub = df_rated[df_rated['Model_Family'] == model]
                vals = sub[rating_cols].mean().values.tolist()
                vals += vals[:1]
                lbls = short_names + [short_names[0]]
                fig.add_trace(go.Scatterpolar(
                    r=vals, theta=lbls, fill='toself',
                    name=f"{model} (n={len(sub)})",
                    line_color=PALETTE[i % len(PALETTE)],
                    fillcolor=f"rgba({int(PALETTE[i%len(PALETTE)][1:3],16)}, {int(PALETTE[i%len(PALETTE)][3:5],16)}, {int(PALETTE[i%len(PALETTE)][5:7],16)}, 0.08)",
                    opacity=0.9
                ))
            fig.update_layout(
                polar=dict(
                    bgcolor=PLOT_BG,
                    radialaxis=dict(
                        visible=True, range=[3.0, 5.2],
                        gridcolor=GRID_COLOR,
                        tickfont=dict(size=10, color=TEXT_COLOR),
                        linecolor=GRID_COLOR
                    ),
                    angularaxis=dict(
                        gridcolor=GRID_COLOR,
                        tickfont=dict(size=11, color=TEXT_COLOR),
                        linecolor=GRID_COLOR
                    )
                ),
                paper_bgcolor=PLOT_BG,
                font=dict(family=FONT_FAM, color=TEXT_COLOR),
                legend=dict(
                    bgcolor="rgba(0,0,0,0)",
                    bordercolor=GRID_COLOR,
                    borderwidth=1,
                    orientation="h",
                    yanchor="bottom", y=-0.18,
                    xanchor="center", x=0.5,
                    font=dict(size=11)
                ),
                margin=dict(l=40, r=40, t=30, b=40),
                height=460
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Select at least one model family to compare.")

    with col_r:
        section("Rating Correlation")
        corr = df_rated[rating_cols].corr()
        corr.columns = short_names
        corr.index = short_names
        fig = px.imshow(
            corr, text_auto='.2f', aspect='auto',
            color_continuous_scale=["#2C2F34", RED],
            zmin=0, zmax=1
        )
        fig.update_traces(textfont=dict(size=10, color="#F0F1F3"))
        fig.update_layout(coloraxis_showscale=False)
        dark_layout(fig, height=460)
        st.plotly_chart(fig, use_container_width=True)

    spacer()
    section("Value Map Rating vs Average Price")
    mv = (df_rated.groupby('Model_Family')
          .agg(Avg_Price=('Price', 'mean'),
               Avg_Rating=('Consumer_Rating', 'mean'),
               Count=('Price', 'count'))
          .reset_index())
    mv = mv[mv['Count'] >= 10]
    fig = px.scatter(
        mv, x='Avg_Price', y='Avg_Rating',
        size='Count', text='Model_Family',
        size_max=44,
        color_discrete_sequence=[RED],
        labels={'Avg_Price': 'Average Price (USD)', 'Avg_Rating': 'Average Rating'}
    )
    fig.update_traces(
        textposition='top center',
        textfont=dict(size=11, color=TEXT_COLOR),
        marker=dict(color=RED, opacity=0.7, line=dict(color=PLOT_BG, width=1))
    )
    fig.update_layout(showlegend=False)
    dark_layout(fig, height=460)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('<div class="caption-note">Models top-left (high rating, lower price) represent the strongest value proposition. Bubble size = listing volume.</div>', unsafe_allow_html=True)


# ============================================================
# PAGE 4: HYBRID VS GASOLINE
# ============================================================
elif page == "Hybrid vs Gasoline":
    header(
        "Hybrid vs Gasoline",
        "Evaluating Honda's electrification strategy through data"
    )

    df_fuel = df[df['Fuel_Type'].isin(['Gasoline', 'Hybrid'])].copy()
    df_gas  = df_fuel[df_fuel['Fuel_Type'] == 'Gasoline']
    df_hyb  = df_fuel[df_fuel['Fuel_Type'] == 'Hybrid']

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    with c1: kpi("Gasoline", f"{len(df_gas):,}")
    with c2: kpi("Hybrid", f"{len(df_hyb):,}", accent=True)
    with c3: kpi("Gas Median Price", fmt_price(df_gas['Price'].median()))
    with c4: kpi("Hybrid Median Price", fmt_price(df_hyb['Price'].median()), accent=True)
    with c5: kpi("Gas Rating", f"{df_gas['Consumer_Rating'].mean():.2f}")
    with c6: kpi("Hybrid Rating", f"{df_hyb['Consumer_Rating'].mean():.2f}")

    spacer("1.25rem")

    col_l, col_r = st.columns(2, gap="medium")

    with col_l:
        section("Price Distribution")
        fig = px.violin(
            df_fuel, x='Fuel_Type', y='Price', color='Fuel_Type',
            box=True, points=False,
            color_discrete_map={'Gasoline': GREY, 'Hybrid': RED}
        )
        fig.update_layout(showlegend=False, yaxis_title="Price (USD)", xaxis_title="")
        dark_layout(fig, height=400)
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        section("Fuel Economy City vs Highway MPG")
        df_mpg = df_fuel[df_fuel['MPG_Combined'].notna()].copy()
        if len(df_mpg) > 0:
            mpg_s = (df_mpg.groupby('Fuel_Type')
                     .agg(City=('MPG_City', 'mean'), Highway=('MPG_Highway', 'mean'))
                     .round(1).reset_index())
            mpg_m = mpg_s.melt(id_vars='Fuel_Type', var_name='Type', value_name='MPG')
            fig = px.bar(
                mpg_m, x='Fuel_Type', y='MPG', color='Type',
                barmode='group', text='MPG',
                color_discrete_sequence=[RED, WHITE]
            )
            fig.update_traces(textposition='outside', texttemplate='%{text:.1f}', marker_line_width=0)
            fig.update_layout(yaxis_title="Average MPG", xaxis_title="", legend_title="")
            dark_layout(fig, height=400)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No MPG data available.")

    spacer()

    col_l2, col_r2 = st.columns(2, gap="medium")

    with col_l2:
        section("Rating Comparison by Dimension")
        rc = ['Comfort_Rating', 'Interior_Design_Rating', 'Performance_Rating',
              'Value_For_Money_Rating', 'Exterior_Styling_Rating', 'Reliability_Rating']
        rn = ['Comfort', 'Interior', 'Performance', 'Value', 'Styling', 'Reliability']
        df_fr = df_fuel[df_fuel['Has_Ratings'] == True]
        fr = df_fr.groupby('Fuel_Type')[rc].mean().reset_index()
        fm = pd.melt(fr, id_vars='Fuel_Type', value_vars=rc, var_name='Dim', value_name='Score')
        fm['Dim'] = fm['Dim'].map(dict(zip(rc, rn)))
        fig = px.bar(
            fm, x='Dim', y='Score', color='Fuel_Type',
            barmode='group', text=fm['Score'].round(2),
            color_discrete_map={'Gasoline': GREY, 'Hybrid': RED}
        )
        fig.update_traces(textposition='outside', marker_line_width=0)
        fig.update_layout(yaxis_range=[3.5, 5.4], yaxis_title="Avg Rating",
                          xaxis_title="", legend_title="")
        dark_layout(fig, height=400)
        st.plotly_chart(fig, use_container_width=True)

    with col_r2:
        section("Hybrid Adoption Trend New Cars")
        df_nf = df_fuel[df_fuel['Condition'] == 'New'].copy()
        yr = (df_nf.groupby(['Year', 'Fuel_Type']).size()
              .unstack(fill_value=0).reset_index())
        if 'Hybrid' in yr.columns and 'Gasoline' in yr.columns:
            yr = yr[yr['Year'] >= 2018]
            yr['Hybrid_Pct'] = (yr['Hybrid'] / (yr['Hybrid'] + yr['Gasoline']) * 100).round(1)
            fig = go.Figure()
            fig.add_trace(go.Bar(x=yr['Year'], y=yr['Gasoline'], name='Gasoline', marker_color=GREY, marker_line_width=0))
            fig.add_trace(go.Bar(x=yr['Year'], y=yr['Hybrid'], name='Hybrid', marker_color=RED, marker_line_width=0))
            fig.add_trace(go.Scatter(
                x=yr['Year'],
                y=yr['Hybrid_Pct'] * (yr['Gasoline'].max() / 100),
                name='Hybrid %',
                yaxis='y2',
                line=dict(color=WHITE, width=2),
                mode='lines+markers',
                marker=dict(size=5)
            ))
            fig.update_layout(
                barmode='stack',
                yaxis_title="Listings",
                yaxis2=dict(
                    title="Hybrid %", overlaying='y', side='right',
                    range=[0, 100], showgrid=False,
                    tickfont=dict(size=10, color=TEXT_COLOR)
                ),
                legend=dict(
                    orientation="h", yanchor="bottom", y=-0.22,
                    xanchor="center", x=0.5,
                    bgcolor="rgba(0,0,0,0)", font=dict(size=11)
                ),
                margin=dict(l=8, r=40, t=24, b=8)
            )
            dark_layout(fig, height=400)
            st.plotly_chart(fig, use_container_width=True)

    spacer()
    section("Hybrid Model Breakdown Top 10 by Volume")
    hm = (df_hyb.groupby('Model')
          .agg(Count=('Price', 'count'),
               Avg_Price=('Price', 'mean'),
               Avg_Rating=('Consumer_Rating', 'mean'))
          .sort_values('Count', ascending=False)
          .head(10).reset_index())
    hm['Avg_Price'] = hm['Avg_Price'].apply(lambda x: f"${x:,.0f}")
    hm['Avg_Rating'] = hm['Avg_Rating'].round(2)
    st.dataframe(
        hm, use_container_width=True, hide_index=True,
        column_config={
            "Model": st.column_config.TextColumn("Model", width="large"),
            "Count": st.column_config.NumberColumn("Listings", format="%d"),
            "Avg_Price": st.column_config.TextColumn("Avg Price"),
            "Avg_Rating": st.column_config.NumberColumn("Avg Rating", format="%.2f")
        }
    )


# ============================================================
# PAGE 5: MARKET GEOGRAPHY
# ============================================================
elif page == "Market Geography":
    header(
        "Market Geography",
        "Honda's market distribution across US states and regions"
    )

    df_geo = df[df['State'].notna()].copy()

    with st.sidebar:
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('<div style="font-size:0.7rem;font-weight:700;color:#5C6370;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.5rem">Filters</div>', unsafe_allow_html=True)
        geo_metric = st.selectbox(
            "Map Metric",
            ["Average Price", "Listing Count", "Average Rating", "Hybrid Share (%)"],
            key="geo_metric"
        )
        geo_cond = st.multiselect(
            "Condition", df_geo['Condition'].unique().tolist(),
            default=df_geo['Condition'].unique().tolist(), key="geo_cond"
        )

    df_geo = df_geo[df_geo['Condition'].isin(geo_cond)]
    sm = df_geo.groupby('State').agg(
        Avg_Price=('Price', 'mean'),
        Count=('Price', 'count'),
        Avg_Rating=('Consumer_Rating', 'mean'),
        Hybrid_Count=('Is_Hybrid', 'sum'),
        Total=('Is_Hybrid', 'count')
    ).reset_index()
    sm['Hybrid_Pct'] = (sm['Hybrid_Count'] / sm['Total'] * 100).round(1)

    c1, c2, c3, c4 = st.columns(4)
    with c1: kpi("States Covered", f"{df_geo['State'].nunique()}")
    with c2: kpi("Filtered Listings", f"{len(df_geo):,}")
    with c3:
        top_state = sm.sort_values('Count', ascending=False).iloc[0]['State']
        kpi("Top State by Volume", top_state, accent=True)
    with c4: kpi("Regions", f"{df_geo['Region'].nunique()}")

    spacer("1.25rem")

    metric_map = {
        "Average Price":    ("Avg_Price",  "Avg Price (USD)",  [[0, "#1A1C1F"], [1, RED]]),
        "Listing Count":    ("Count",      "Listings",         [[0, "#1A1C1F"], [1, WHITE]]),
        "Average Rating":   ("Avg_Rating", "Avg Rating",       [[0, "#1A1C1F"], [1, RED]]),
        "Hybrid Share (%)": ("Hybrid_Pct", "Hybrid %",         [[0, "#1A1C1F"], [1, RED]])
    }
    m_col, m_title, m_scale = metric_map[geo_metric]

    section(f"US Map {geo_metric}")
    fig = px.choropleth(
        sm, locations='State', locationmode='USA-states',
        color=m_col, scope='usa',
        color_continuous_scale=m_scale,
        hover_data={'Avg_Price': ':$,.0f', 'Count': ':,', 'Avg_Rating': ':.2f', 'Hybrid_Pct': ':.1f'},
        labels={m_col: m_title}
    )
    fig.update_layout(
        height=480,
        geo=dict(bgcolor=PLOT_BG, lakecolor=PLOT_BG, landcolor="#222529", showlakes=True),
        coloraxis_colorbar=dict(
            title=m_title, thickness=12,
            tickfont=dict(size=10, color=TEXT_COLOR),
            title_font=dict(size=10, color=TEXT_COLOR)
        ),
        margin=dict(l=0, r=0, t=8, b=0),
        paper_bgcolor=PLOT_BG,
        font=dict(family=FONT_FAM, color=TEXT_COLOR)
    )
    st.plotly_chart(fig, use_container_width=True)

    spacer()

    col_l, col_r = st.columns(2, gap="medium")

    rs = (df_geo.groupby('Region')
          .agg(Avg_Price=('Price', 'mean'), Count=('Price', 'count'))
          .sort_values('Avg_Price', ascending=False)
          .reset_index())

    with col_l:
        section("Average Price by Region")
        fig = px.bar(
            rs, x='Region', y='Avg_Price',
            text=rs['Avg_Price'].apply(lambda x: f"${x:,.0f}"),
            color_discrete_sequence=[RED]
        )
        fig.update_traces(textposition='outside', marker_line_width=0)
        fig.update_layout(showlegend=False, yaxis_title="Avg Price (USD)", xaxis_title="")
        dark_layout(fig, height=360)
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        section("Listing Volume by Region")
        fig = px.pie(
            rs, values='Count', names='Region',
            color_discrete_sequence=[RED, WHITE, GREY, "#4A5568"],
            hole=0.55
        )
        fig.update_traces(
            textinfo='label+percent', textfont_size=11,
            marker=dict(line=dict(color=PLOT_BG, width=2))
        )
        fig.update_layout(showlegend=False)
        dark_layout(fig, height=360)
        st.plotly_chart(fig, use_container_width=True)

    spacer()
    section("Top Model Families by Region")
    rm = (df_geo.groupby(['Region', 'Model_Family']).size()
          .reset_index(name='Count')
          .sort_values(['Region', 'Count'], ascending=[True, False]))
    rt = rm.groupby('Region').head(5)
    fig = px.bar(
        rt, x='Model_Family', y='Count', color='Region',
        barmode='group',
        color_discrete_sequence=[RED, WHITE, GREY, "#4A5568"]
    )
    fig.update_traces(marker_line_width=0)
    fig.update_layout(xaxis_title="", yaxis_title="Listings", legend_title="Region")
    dark_layout(fig, height=400)
    st.plotly_chart(fig, use_container_width=True)

    spacer()
    section("State-Level Detail")
    sd = sm.sort_values('Count', ascending=False).copy()
    sd['Avg_Price'] = sd['Avg_Price'].apply(lambda x: f"${x:,.0f}")
    sd['Avg_Rating'] = sd['Avg_Rating'].round(2)
    sd = sd[['State', 'Count', 'Avg_Price', 'Avg_Rating', 'Hybrid_Pct']]
    sd.columns = ['State', 'Listings', 'Avg Price', 'Avg Rating', 'Hybrid %']
    st.dataframe(sd, use_container_width=True, hide_index=True, height=380)


# ============================================================
# FOOTER
# ============================================================
st.markdown("""
<div class="dashboard-footer">
    <span>Honda US Market Analysis</span>
    <span>Built with Streamlit & Plotly &nbsp;·&nbsp; Portfolio Project</span>
</div>
""", unsafe_allow_html=True)