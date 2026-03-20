import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="PitSight — BMW Intelligence",
    page_icon="🏎️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# BMW M-INSPIRED COLOR PALETTE
# ============================================================
BMW_COLORS = {
    'bg_primary': '#0A0E17',
    'bg_secondary': '#111827',
    'bg_card': '#1A2332',
    'bg_card_hover': '#1F2D3F',
    'text_primary': '#F0F4F8',
    'text_secondary': '#8B99A8',
    'text_muted': '#5A6B7D',
    'accent_blue': '#1A73E8',
    'accent_m_blue': '#0066B1',
    'accent_m_red': '#E2001A',
    'accent_m_purple': '#6E3ECC',
    'accent_cyan': '#00D4FF',
    'accent_green': '#00C853',
    'accent_amber': '#FFB300',
    'border': '#1E2D3D',
    'chart_blue': '#4A90D9',
    'chart_light': '#7CB5EC',
    'chart_bar': '#2B5EA7',
    'positive': '#00C853',
    'negative': '#FF5252',
    'neutral': '#FFB300',
}

# ============================================================
# CUSTOM CSS — BMW PREMIUM DARK THEME
# ============================================================
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    /* Global */
    .stApp {{
        background: linear-gradient(180deg, {BMW_COLORS['bg_primary']} 0%, #0D1520 100%);
        font-family: 'DM Sans', sans-serif;
    }}
    .main .block-container {{
        padding-top: 1.5rem;
        max-width: 100%;
    }}

    /* Sidebar */
    section[data-testid="stSidebar"] {{
        background: {BMW_COLORS['bg_secondary']};
        border-right: 1px solid {BMW_COLORS['border']};
    }}
    section[data-testid="stSidebar"] .stMarkdown h1 {{
        color: {BMW_COLORS['text_primary']};
        font-size: 1.1rem;
        font-weight: 700;
        letter-spacing: 2px;
    }}

    /* Hide Streamlit defaults */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}

    /* Cards */
    .bmw-card {{
        background: {BMW_COLORS['bg_card']};
        border: 1px solid {BMW_COLORS['border']};
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 12px;
        transition: all 0.2s ease;
    }}
    .bmw-card:hover {{
        border-color: {BMW_COLORS['accent_blue']};
        box-shadow: 0 4px 20px rgba(26,115,232,0.1);
    }}

    /* KPI Card */
    .kpi-card {{
        background: linear-gradient(135deg, {BMW_COLORS['accent_m_blue']} 0%, {BMW_COLORS['accent_blue']} 100%);
        border-radius: 14px;
        padding: 24px;
        color: white;
    }}
    .kpi-card .kpi-value {{
        font-size: 2.4rem;
        font-weight: 800;
        line-height: 1.1;
        margin-bottom: 4px;
    }}
    .kpi-card .kpi-label {{
        font-size: 0.85rem;
        opacity: 0.8;
        letter-spacing: 0.5px;
    }}
    .kpi-card .kpi-change {{
        font-size: 1.1rem;
        font-weight: 600;
    }}
    .kpi-card .kpi-prev {{
        font-size: 0.9rem;
        opacity: 0.7;
        margin-top: 8px;
    }}

    /* Section headers */
    .section-header {{
        font-size: 1rem;
        font-weight: 600;
        color: {BMW_COLORS['text_secondary']};
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 16px;
        padding-bottom: 8px;
        border-bottom: 1px solid {BMW_COLORS['border']};
    }}

    /* M Stripe accent */
    .m-stripe {{
        height: 3px;
        background: linear-gradient(90deg, {BMW_COLORS['accent_m_blue']} 0%, {BMW_COLORS['accent_m_purple']} 50%, {BMW_COLORS['accent_m_red']} 100%);
        border-radius: 2px;
        margin-bottom: 20px;
    }}

    /* Metric boxes */
    .metric-box {{
        background: {BMW_COLORS['bg_card']};
        border: 1px solid {BMW_COLORS['border']};
        border-radius: 10px;
        padding: 16px;
        text-align: center;
    }}
    .metric-box .metric-value {{
        font-size: 1.8rem;
        font-weight: 700;
        color: {BMW_COLORS['text_primary']};
    }}
    .metric-box .metric-label {{
        font-size: 0.78rem;
        color: {BMW_COLORS['text_muted']};
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 4px;
    }}

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 0px;
        background: {BMW_COLORS['bg_card']};
        border-radius: 10px;
        padding: 4px;
    }}
    .stTabs [data-baseweb="tab"] {{
        border-radius: 8px;
        font-weight: 500;
        font-size: 0.88rem;
        padding: 8px 24px;
    }}
    .stTabs [aria-selected="true"] {{
        background: {BMW_COLORS['accent_blue']};
        color: white;
    }}

    /* Plotly chart backgrounds */
    .js-plotly-plot .plotly .modebar {{
        display: none !important;
    }}

    /* Sentiment badges */
    .badge-satisfied {{
        background: rgba(0,200,83,0.15);
        color: {BMW_COLORS['positive']};
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 600;
    }}
    .badge-dissatisfied {{
        background: rgba(255,82,82,0.15);
        color: {BMW_COLORS['negative']};
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 600;
    }}

    /* Scrollbar */
    ::-webkit-scrollbar {{
        width: 6px;
    }}
    ::-webkit-scrollbar-track {{
        background: {BMW_COLORS['bg_primary']};
    }}
    ::-webkit-scrollbar-thumb {{
        background: {BMW_COLORS['border']};
        border-radius: 3px;
    }}
</style>
""", unsafe_allow_html=True)


# ============================================================
# LOAD DATA
# ============================================================
@st.cache_data
def load_data():
    import os
    base_dir = os.path.dirname(os.path.abspath(__file__))
    t1 = pd.read_csv(os.path.join(base_dir, 'table1.csv'))
    # table2 is gzipped to fit GitHub's 25MB limit
    t2_gz = os.path.join(base_dir, 'table2.csv.gz')
    t2_csv = os.path.join(base_dir, 'table2.csv')
    if os.path.exists(t2_gz):
        t2 = pd.read_csv(t2_gz, compression='gzip')
    else:
        t2 = pd.read_csv(t2_csv)
    t1['Date'] = pd.to_datetime(t1['Date'], format='%d/%m/%Y')
    t1['Month'] = t1['Date'].dt.month
    t1['MonthName'] = t1['Date'].dt.strftime('%b')
    t1['Weekday'] = t1['Date'].dt.day_name()
    t2['Date'] = pd.to_datetime(t2['Date'], format='%d/%m/%Y')
    return t1, t2

df1, df2 = load_data()

# Chart layout template
CHART_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='DM Sans', color=BMW_COLORS['text_secondary'], size=12),
    margin=dict(l=40, r=20, t=40, b=40),
    xaxis=dict(gridcolor='rgba(30,45,61,0.5)', zeroline=False),
    yaxis=dict(gridcolor='rgba(30,45,61,0.5)', zeroline=False),
    legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(size=11)),
    hoverlabel=dict(bgcolor=BMW_COLORS['bg_card'], font_size=12, font_family='DM Sans'),
)

# ============================================================
# SIDEBAR — Navigation + Filters
# ============================================================
with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:10px 0 20px;">
        <div style="font-size:1.8rem;font-weight:800;letter-spacing:3px;color:#F0F4F8;">PIT<span style="color:#1A73E8;">SIGHT</span></div>
        <div style="font-size:0.7rem;color:#5A6B7D;letter-spacing:2px;margin-top:2px;">BMW INTELLIGENCE PLATFORM</div>
        <div style="height:3px;background:linear-gradient(90deg,#0066B1,#6E3ECC,#E2001A);border-radius:2px;margin-top:12px;"></div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio("", ["📊 Dashboard", "🏎️ All Models", "🔍 Sentiment Intelligence"],
                    label_visibility="collapsed")

    st.markdown("---")
    st.markdown('<div style="font-size:0.78rem;color:#5A6B7D;letter-spacing:1.5px;font-weight:600;">FILTERS</div>', unsafe_allow_html=True)

    sel_years = st.multiselect("Year", sorted(df1['Year'].unique()), default=sorted(df1['Year'].unique()))
    sel_regions = st.multiselect("Region", sorted(df1['Region'].unique()), default=sorted(df1['Region'].unique()))
    sel_countries = st.multiselect("Country", sorted(df1['Country'].unique()), default=sorted(df1['Country'].unique()))
    sel_channels = st.multiselect("Channel", sorted(df1['Channel'].unique()), default=sorted(df1['Channel'].unique()))
    sel_models = st.multiselect("Model", sorted(df1['Model'].unique()), default=[])

    st.markdown("---")
    st.markdown("""
    <div style="text-align:center;padding:20px 0;">
        <div style="font-size:2.5rem;font-weight:900;color:#F0F4F8;letter-spacing:4px;">BMW</div>
        <div style="font-size:0.65rem;color:#5A6B7D;letter-spacing:1px;margin-top:4px;">SHEER DRIVING PLEASURE</div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# APPLY FILTERS
# ============================================================
f1 = df1[
    (df1['Year'].isin(sel_years)) &
    (df1['Region'].isin(sel_regions)) &
    (df1['Country'].isin(sel_countries)) &
    (df1['Channel'].isin(sel_channels))
]
if sel_models:
    f1 = f1[f1['Model'].isin(sel_models)]

f2 = df2[
    (df2['Year'].isin(sel_years)) &
    (df2['Country'].isin(sel_countries))
]
if sel_models:
    f2 = f2[f2['Model'].isin(sel_models)]


# ============================================================
# PAGE 1: DASHBOARD
# ============================================================
if page == "📊 Dashboard":

    # M Stripe
    st.markdown('<div class="m-stripe"></div>', unsafe_allow_html=True)

    # Time granularity toggle
    time_gran = st.radio("", ["Year", "Month", "Weekday"], horizontal=True, label_visibility="collapsed")

    # Top row: Global Sales Chart + KPI
    col_chart, col_kpi = st.columns([3, 1])

    with col_chart:
        st.markdown('<div class="section-header">Global Sales</div>', unsafe_allow_html=True)

        if time_gran == "Year":
            agg = f1.groupby('Year').agg({'Revenue': 'sum', 'Quantity Sold': 'sum'}).reset_index()
            agg['PY_Revenue'] = agg['Revenue'].shift(1)
            x_col = 'Year'
        elif time_gran == "Month":
            agg = f1.groupby('Month').agg({'Revenue': 'sum', 'Quantity Sold': 'sum'}).reset_index()
            month_names = {1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'Jun',7:'Jul',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec'}
            agg['MonthName'] = agg['Month'].map(month_names)
            agg['PY_Revenue'] = agg['Revenue'].shift(1).fillna(agg['Revenue'].mean())
            x_col = 'MonthName'
        else:
            day_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
            agg = f1.groupby('Weekday').agg({'Revenue': 'sum', 'Quantity Sold': 'sum'}).reset_index()
            agg['Weekday'] = pd.Categorical(agg['Weekday'], categories=day_order, ordered=True)
            agg = agg.sort_values('Weekday')
            agg['PY_Revenue'] = agg['Revenue'].mean()
            x_col = 'Weekday'

        fig_sales = go.Figure()
        fig_sales.add_trace(go.Bar(
            x=agg[x_col], y=agg['Revenue'],
            name='Revenue', marker_color=BMW_COLORS['chart_bar'],
            marker_line_width=0, opacity=0.9
        ))
        if 'PY_Revenue' in agg.columns:
            fig_sales.add_trace(go.Scatter(
                x=agg[x_col], y=agg['PY_Revenue'],
                name='Revenue PY', mode='lines+markers',
                line=dict(color=BMW_COLORS['chart_light'], width=2.5),
                marker=dict(size=6)
            ))
        fig_sales.update_layout(
            **CHART_LAYOUT,
            height=320,
            yaxis_title='',
            xaxis_title='',
            legend=dict(orientation='h', y=-0.15, x=0.5, xanchor='center'),
            yaxis=dict(gridcolor='rgba(30,45,61,0.3)', tickformat='$,.0s'),
        )
        st.plotly_chart(fig_sales, use_container_width=True)

    with col_kpi:
        total_rev = f1['Revenue'].sum()
        total_qty = int(f1['Quantity Sold'].sum())

        # Calculate PY
        max_year = f1['Year'].max() if len(f1) > 0 else 2025
        cy_rev = f1[f1['Year'] == max_year]['Revenue'].sum()
        py_rev = f1[f1['Year'] == max_year - 1]['Revenue'].sum()
        pct_change = ((cy_rev - py_rev) / py_rev * 100) if py_rev > 0 else 0

        min_date = f1['Date'].min().strftime('%b %d, %Y') if len(f1) > 0 else ''
        max_date = f1['Date'].max().strftime('%b %d, %Y') if len(f1) > 0 else ''

        change_color = BMW_COLORS['positive'] if pct_change >= 0 else BMW_COLORS['negative']
        arrow = '↑' if pct_change >= 0 else '↓'

        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Period: {min_date} – {max_date}</div>
            <div class="kpi-value">${total_rev/1e9:.2f}bn</div>
            <div class="kpi-change" style="color:{change_color};">{arrow} {abs(pct_change):.1f}%</div>
            <div class="kpi-prev">PY ${py_rev/1e9:.2f}bn</div>
            <div style="margin-top:16px;padding-top:12px;border-top:1px solid rgba(255,255,255,0.2);">
                <div class="kpi-label">Total Units</div>
                <div style="font-size:1.5rem;font-weight:700;">{total_qty:,}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Top Selling Models
    st.markdown('<div class="section-header">Top Selling Models</div>', unsafe_allow_html=True)
    top_models = f1.groupby('Model')['Quantity Sold'].sum().sort_values(ascending=False).head(8).reset_index()

    cols = st.columns(min(len(top_models), 8))
    for i, (idx, row) in enumerate(top_models.iterrows()):
        if i < len(cols):
            with cols[i]:
                st.markdown(f"""
                <div class="bmw-card" style="text-align:center;padding:16px 8px;">
                    <div style="font-size:0.88rem;font-weight:600;color:{BMW_COLORS['text_primary']};margin-bottom:4px;">
                        {row['Model'].replace('BMW ', '')}
                    </div>
                    <div style="font-size:1.2rem;font-weight:700;color:{BMW_COLORS['accent_cyan']};">
                        {int(row['Quantity Sold']):,}
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # Bottom row: Country table + Channel donut + Cars sold yearly
    col_table, col_donut, col_yearly = st.columns([2, 1.2, 1.2])

    with col_table:
        st.markdown('<div class="section-header">Cars Sold Country-wise</div>', unsafe_allow_html=True)
        country_data = f1.groupby('Country').agg({
            'Quantity Sold': 'sum',
            'Revenue': 'sum'
        }).sort_values('Quantity Sold', ascending=False).reset_index()
        country_data['Revenue_fmt'] = country_data['Revenue'].apply(lambda x: f"${x/1e6:.0f}M")
        country_data['Qty'] = country_data['Quantity Sold'].apply(lambda x: f"{x:,}")

        display_df = country_data[['Country', 'Qty', 'Revenue_fmt']].rename(
            columns={'Revenue_fmt': 'Revenue'}).head(10)
        st.dataframe(display_df, hide_index=True, use_container_width=True, height=350)

    with col_donut:
        st.markdown('<div class="section-header">Channel Contribution</div>', unsafe_allow_html=True)
        channel_data = f1.groupby('Channel')['Quantity Sold'].sum().reset_index()

        fig_donut = go.Figure(go.Pie(
            labels=channel_data['Channel'],
            values=channel_data['Quantity Sold'],
            hole=0.65,
            marker=dict(colors=[BMW_COLORS['chart_bar'], BMW_COLORS['accent_cyan'], BMW_COLORS['accent_m_purple']]),
            textinfo='label+percent',
            textfont=dict(size=11, color=BMW_COLORS['text_primary']),
        ))
        fig_donut.update_layout(
            **CHART_LAYOUT, height=320, showlegend=False,
            annotations=[dict(text=f"<b>{total_qty/1e3:.0f}K</b>", x=0.5, y=0.5,
                             font_size=22, font_color=BMW_COLORS['text_primary'],
                             showarrow=False)]
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    with col_yearly:
        st.markdown('<div class="section-header">Cars Sold Year-wise</div>', unsafe_allow_html=True)
        yearly_qty = f1.groupby('Year')['Quantity Sold'].sum().reset_index()

        fig_yearly = go.Figure()
        fig_yearly.add_trace(go.Bar(
            x=yearly_qty['Year'], y=yearly_qty['Quantity Sold'],
            marker_color=BMW_COLORS['chart_bar'], name='Qty'
        ))
        fig_yearly.update_layout(
            **CHART_LAYOUT, height=320,
            yaxis=dict(gridcolor='rgba(30,45,61,0.3)', tickformat=','),
            showlegend=False
        )
        st.plotly_chart(fig_yearly, use_container_width=True)


# ============================================================
# PAGE 2: ALL MODELS
# ============================================================
elif page == "🏎️ All Models":

    st.markdown('<div class="m-stripe"></div>', unsafe_allow_html=True)

    # Model search
    all_models = sorted(f1['Model'].unique())
    selected_model = st.selectbox("Search Model", all_models, index=0, label_visibility="collapsed",
                                   placeholder="Search BMW models...")

    st.markdown(f"""
    <div style="font-size:2.2rem;font-weight:800;color:{BMW_COLORS['text_primary']};margin:16px 0 8px;">
        {selected_model}
    </div>
    """, unsafe_allow_html=True)

    model_data = f1[f1['Model'] == selected_model]

    # Yearly summary + hero area
    col_summary, col_hero = st.columns([1, 1.5])

    with col_summary:
        yearly_model = model_data.groupby('Year').agg({
            'Quantity Sold': 'sum', 'Revenue': 'sum'
        }).reset_index()

        # Styled table
        st.markdown('<div class="section-header">Yearly Performance</div>', unsafe_allow_html=True)

        for _, row in yearly_model.iterrows():
            rev_fmt = f"${row['Revenue']/1e6:.0f}M"
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;padding:8px 12px;
                        border-bottom:1px solid {BMW_COLORS['border']};font-size:0.92rem;">
                <span style="color:{BMW_COLORS['text_secondary']};font-weight:500;">{int(row['Year'])}</span>
                <span style="color:{BMW_COLORS['accent_cyan']};font-weight:600;">{int(row['Quantity Sold']):,}</span>
                <span style="color:{BMW_COLORS['text_primary']};font-weight:600;">{rev_fmt}</span>
            </div>
            """, unsafe_allow_html=True)

        # Total row
        total_q = int(yearly_model['Quantity Sold'].sum())
        total_r = yearly_model['Revenue'].sum()
        st.markdown(f"""
        <div style="display:flex;justify-content:space-between;padding:10px 12px;
                    background:{BMW_COLORS['bg_card']};border-radius:8px;margin-top:8px;font-size:0.95rem;">
            <span style="color:{BMW_COLORS['accent_blue']};font-weight:700;">Total</span>
            <span style="color:{BMW_COLORS['accent_cyan']};font-weight:700;">{total_q:,}</span>
            <span style="color:{BMW_COLORS['text_primary']};font-weight:700;">${total_r/1e6:.0f}M</span>
        </div>
        """, unsafe_allow_html=True)

        # Average price KPI
        avg_price = model_data['Revenue'].sum() / max(model_data['Quantity Sold'].sum(), 1)
        st.markdown(f"""
        <div style="margin-top:24px;">
            <div style="font-size:2.5rem;font-weight:800;color:{BMW_COLORS['text_primary']};">${avg_price/1e3:.1f}K</div>
            <div style="font-size:0.85rem;color:{BMW_COLORS['text_muted']};text-transform:uppercase;letter-spacing:1px;">Average Price</div>
        </div>
        """, unsafe_allow_html=True)

    with col_hero:
        # Revenue trend chart for this model
        fig_model = make_subplots(specs=[[{"secondary_y": True}]])
        fig_model.add_trace(go.Bar(
            x=yearly_model['Year'], y=yearly_model['Revenue'],
            name='Revenue', marker_color=BMW_COLORS['chart_bar'], opacity=0.8
        ), secondary_y=False)
        fig_model.add_trace(go.Scatter(
            x=yearly_model['Year'], y=yearly_model['Quantity Sold'],
            name='Units', mode='lines+markers',
            line=dict(color=BMW_COLORS['accent_cyan'], width=3),
            marker=dict(size=8)
        ), secondary_y=True)
        fig_model.update_layout(
            **CHART_LAYOUT, height=350,
            title=dict(text=f'{selected_model} — Revenue & Units', font=dict(size=14)),
            legend=dict(orientation='h', y=-0.15, x=0.5, xanchor='center'),
        )
        fig_model.update_yaxes(title_text='Revenue', tickformat='$,.0s', secondary_y=False,
                               gridcolor='rgba(30,45,61,0.3)')
        fig_model.update_yaxes(title_text='Units', secondary_y=True, showgrid=False)
        st.plotly_chart(fig_model, use_container_width=True)

    # Model carousel at bottom
    st.markdown('<div class="section-header">Browse Models</div>', unsafe_allow_html=True)
    top_all = f1.groupby('Model')['Quantity Sold'].sum().sort_values(ascending=False).reset_index()
    cols = st.columns(min(len(top_all), 8))
    for i, (_, row) in enumerate(top_all.head(8).iterrows()):
        with cols[i]:
            is_selected = row['Model'] == selected_model
            border_color = BMW_COLORS['accent_blue'] if is_selected else BMW_COLORS['border']
            bg = BMW_COLORS['bg_card_hover'] if is_selected else BMW_COLORS['bg_card']
            st.markdown(f"""
            <div style="background:{bg};border:2px solid {border_color};border-radius:10px;
                        padding:12px 6px;text-align:center;">
                <div style="font-size:0.82rem;font-weight:{'700' if is_selected else '500'};
                     color:{BMW_COLORS['text_primary']};margin-bottom:2px;">
                    {row['Model'].replace('BMW ', '')}
                </div>
                <div style="font-size:1rem;font-weight:600;color:{BMW_COLORS['accent_cyan']};">
                    {int(row['Quantity Sold']):,}
                </div>
            </div>
            """, unsafe_allow_html=True)


# ============================================================
# PAGE 3: SENTIMENT INTELLIGENCE
# ============================================================
elif page == "🔍 Sentiment Intelligence":

    st.markdown('<div class="m-stripe"></div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div style="font-size:1.6rem;font-weight:800;color:{BMW_COLORS['text_primary']};margin-bottom:4px;">
        Sentiment Intelligence
    </div>
    <div style="font-size:0.88rem;color:{BMW_COLORS['text_muted']};margin-bottom:24px;">
        Understanding the WHY behind sales trends — powered by NLP analysis of {len(f2):,} customer reviews
    </div>
    """, unsafe_allow_html=True)

    # KPI Row
    total_reviews = len(f2)
    pct_satisfied = (f2['Sentiment_Label'] == 'Satisfied').mean() * 100
    avg_svc = f2['Service_History'].mean()
    avg_delivery = f2['Delivery_Days'].mean()

    k1, k2, k3, k4 = st.columns(4)
    for col, val, label, color in [
        (k1, f"{total_reviews:,}", "Total Reviews", BMW_COLORS['accent_blue']),
        (k2, f"{pct_satisfied:.1f}%", "Satisfied", BMW_COLORS['positive']),
        (k3, f"{avg_svc:.1f}", "Avg Service Visits", BMW_COLORS['accent_amber']),
        (k4, f"{avg_delivery:.0f} days", "Avg Delivery", BMW_COLORS['accent_cyan']),
    ]:
        with col:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-value" style="color:{color};">{val}</div>
                <div class="metric-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Row 2: Satisfaction by Model + Satisfaction Over Time
    col_model_sat, col_time_sat = st.columns([1.2, 1])

    with col_model_sat:
        st.markdown('<div class="section-header">Satisfaction Rate by Model</div>', unsafe_allow_html=True)

        model_sat = f2.groupby('Model').agg(
            satisfied=('Sentiment_Label', lambda x: (x == 'Satisfied').mean() * 100),
            count=('Sentiment_Label', 'count'),
            avg_svc=('Service_History', 'mean')
        ).sort_values('satisfied', ascending=True).reset_index()

        fig_msat = go.Figure()
        fig_msat.add_trace(go.Bar(
            y=model_sat['Model'].str.replace('BMW ', ''),
            x=model_sat['satisfied'],
            orientation='h',
            marker=dict(
                color=model_sat['satisfied'],
                colorscale=[[0, BMW_COLORS['negative']], [0.5, BMW_COLORS['neutral']], [1, BMW_COLORS['positive']]],
                cmin=0, cmax=100
            ),
            text=model_sat['satisfied'].apply(lambda x: f'{x:.0f}%'),
            textposition='outside',
            textfont=dict(size=10),
        ))
        fig_msat.update_layout(
            **CHART_LAYOUT, height=550,
            xaxis=dict(title='% Satisfied', range=[0, 110], gridcolor='rgba(30,45,61,0.3)'),
            yaxis=dict(gridcolor='rgba(30,45,61,0.3)'),
        )
        st.plotly_chart(fig_msat, use_container_width=True)

    with col_time_sat:
        st.markdown('<div class="section-header">Satisfaction Trend Over Time</div>', unsafe_allow_html=True)

        yearly_sat = f2.groupby('Year').agg(
            satisfied=('Sentiment_Label', lambda x: (x == 'Satisfied').mean() * 100),
            avg_svc=('Service_History', 'mean'),
            avg_delivery=('Delivery_Days', 'mean')
        ).reset_index()

        fig_trend = make_subplots(specs=[[{"secondary_y": True}]])
        fig_trend.add_trace(go.Scatter(
            x=yearly_sat['Year'], y=yearly_sat['satisfied'],
            name='% Satisfied', mode='lines+markers',
            line=dict(color=BMW_COLORS['positive'], width=3),
            marker=dict(size=8), fill='tozeroy',
            fillcolor='rgba(0,200,83,0.08)'
        ), secondary_y=False)
        fig_trend.add_trace(go.Scatter(
            x=yearly_sat['Year'], y=yearly_sat['avg_svc'],
            name='Avg Service Visits', mode='lines+markers',
            line=dict(color=BMW_COLORS['negative'], width=2, dash='dot'),
            marker=dict(size=6)
        ), secondary_y=True)
        fig_trend.update_layout(**CHART_LAYOUT, height=350,
                               legend=dict(orientation='h', y=-0.2, x=0.5, xanchor='center'))
        fig_trend.update_yaxes(title_text='% Satisfied', secondary_y=False,
                               gridcolor='rgba(30,45,61,0.3)')
        fig_trend.update_yaxes(title_text='Avg Service Visits', secondary_y=True, showgrid=False)
        st.plotly_chart(fig_trend, use_container_width=True)

    # Row 3: Aspect Scores Heatmap + Model Deep Dive
    col_heatmap, col_deep = st.columns([1.2, 1])

    with col_heatmap:
        st.markdown('<div class="section-header">Aspect Scores by Model Category</div>', unsafe_allow_html=True)

        def categorize(model):
            if model.startswith('BMW i') or model == 'BMW iX': return 'EV'
            elif model.startswith('BMW M'): return 'M-Series'
            elif model.startswith('BMW X'): return 'X-Series'
            elif model == 'BMW Z4': return 'Z-Series'
            else: return 'Sedan'

        f2_cat = f2.copy()
        f2_cat['Category'] = f2_cat['Model'].apply(categorize)

        aspect_means = []
        for cat in ['Sedan', 'X-Series', 'M-Series', 'EV']:
            sub = f2_cat[f2_cat['Category'] == cat]
            row = {'Category': cat}
            for asp in ['maintenance_score', 'comfort_score', 'technology_score',
                        'service_experience_score', 'fuel_or_range_score']:
                vals = sub[sub[asp] > 0][asp]
                row[asp.replace('_score', '').replace('_', ' ').title()] = vals.mean() if len(vals) > 0 else 0
            aspect_means.append(row)

        hm_df = pd.DataFrame(aspect_means).set_index('Category')

        fig_hm = go.Figure(go.Heatmap(
            z=hm_df.values,
            x=hm_df.columns,
            y=hm_df.index,
            colorscale=[[0, BMW_COLORS['negative']], [0.5, BMW_COLORS['neutral']], [1, BMW_COLORS['positive']]],
            zmin=1, zmax=5,
            text=np.round(hm_df.values, 1),
            texttemplate='%{text}',
            textfont=dict(size=13, color='white'),
            hovertemplate='%{y} — %{x}: %{z:.2f}<extra></extra>'
        ))
        fig_hm.update_layout(**CHART_LAYOUT, height=300)
        st.plotly_chart(fig_hm, use_container_width=True)

    with col_deep:
        st.markdown('<div class="section-header">Spotlight: BMW X6 vs X5</div>', unsafe_allow_html=True)

        spotlight_data = []
        for model_name, color in [('BMW X6', BMW_COLORS['negative']), ('BMW X5', BMW_COLORS['positive'])]:
            sub = f2[f2['Model'] == model_name]
            for yr in sorted(sub['Year'].unique()):
                s = sub[sub['Year'] == yr]
                spotlight_data.append({
                    'Model': model_name.replace('BMW ', ''),
                    'Year': yr,
                    'Satisfied': (s['Sentiment_Label'] == 'Satisfied').mean() * 100,
                    'Avg_Svc': s['Service_History'].mean()
                })

        sp_df = pd.DataFrame(spotlight_data)
        fig_spot = go.Figure()
        for model_name, color in [('X6', BMW_COLORS['negative']), ('X5', BMW_COLORS['positive'])]:
            sub = sp_df[sp_df['Model'] == model_name]
            fig_spot.add_trace(go.Scatter(
                x=sub['Year'], y=sub['Satisfied'], name=model_name,
                mode='lines+markers', line=dict(color=color, width=3),
                marker=dict(size=8)
            ))
        fig_spot.update_layout(
            **CHART_LAYOUT, height=300,
            yaxis=dict(title='% Satisfied', range=[0, 105], gridcolor='rgba(30,45,61,0.3)'),
            legend=dict(orientation='h', y=-0.2, x=0.5, xanchor='center'),
        )
        st.plotly_chart(fig_spot, use_container_width=True)

    # Row 4: Feature Importance + Review Explorer
    col_fi, col_reviews = st.columns([1, 1.2])

    with col_fi:
        st.markdown('<div class="section-header">What Drives Satisfaction? (ML Feature Importance)</div>', unsafe_allow_html=True)

        fi_data = pd.DataFrame({
            'Feature': ['Service History', 'Delivery Days', 'Customer Age', 'Warranty Years', 'Is EV'],
            'Importance': [46.3, 41.2, 9.4, 2.4, 0.8]
        }).sort_values('Importance')

        fig_fi = go.Figure(go.Bar(
            y=fi_data['Feature'], x=fi_data['Importance'],
            orientation='h',
            marker_color=[BMW_COLORS['accent_blue']] * 3 + [BMW_COLORS['text_muted']] * 2,
            text=fi_data['Importance'].apply(lambda x: f'{x:.1f}%'),
            textposition='outside'
        ))
        fig_fi.update_layout(
            **CHART_LAYOUT, height=280,
            xaxis=dict(title='Importance %', gridcolor='rgba(30,45,61,0.3)'),
        )
        st.plotly_chart(fig_fi, use_container_width=True)

        st.markdown(f"""
        <div class="bmw-card" style="border-left:3px solid {BMW_COLORS['accent_blue']};">
            <div style="font-size:0.88rem;color:{BMW_COLORS['text_primary']};font-weight:600;margin-bottom:6px;">
                ML Model: Random Forest — 91.5% Accuracy
            </div>
            <div style="font-size:0.82rem;color:{BMW_COLORS['text_muted']};">
                Service History + Delivery Days account for 87.5% of prediction power.
                Fix these two operational metrics → customer satisfaction improves.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_reviews:
        st.markdown('<div class="section-header">Review Explorer</div>', unsafe_allow_html=True)

        rev_model = st.selectbox("Select Model", sorted(f2['Model'].unique()), key='rev_model')
        rev_sentiment = st.selectbox("Sentiment", ['All', 'Satisfied', 'Dissatisfied'], key='rev_sent')

        rev_filtered = f2[f2['Model'] == rev_model]
        if rev_sentiment != 'All':
            rev_filtered = rev_filtered[rev_filtered['Sentiment_Label'] == rev_sentiment]

        rev_sample = rev_filtered.sample(min(5, len(rev_filtered)), random_state=42) if len(rev_filtered) > 0 else rev_filtered

        for _, r in rev_sample.iterrows():
            badge_class = 'badge-satisfied' if r['Sentiment_Label'] == 'Satisfied' else 'badge-dissatisfied'
            st.markdown(f"""
            <div class="bmw-card" style="padding:14px 18px;">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
                    <span style="font-size:0.78rem;color:{BMW_COLORS['text_muted']};">
                        {r['Customer_ID']} · {int(r['Year'])} · Svc={int(r['Service_History'])}
                    </span>
                    <span class="{badge_class}">{r['Sentiment_Label']}</span>
                </div>
                <div style="font-size:0.88rem;color:{BMW_COLORS['text_primary']};line-height:1.5;">
                    "{r['Customer_Review'][:200]}{'...' if len(str(r['Customer_Review'])) > 200 else ''}"
                </div>
                <div style="display:flex;gap:12px;margin-top:8px;">
                    <span style="font-size:0.75rem;color:{BMW_COLORS['text_muted']};">Maint: {r['maintenance_score']}</span>
                    <span style="font-size:0.75rem;color:{BMW_COLORS['text_muted']};">Tech: {r['technology_score']}</span>
                    <span style="font-size:0.75rem;color:{BMW_COLORS['text_muted']};">Svc: {r['service_experience_score']}</span>
                    <span style="font-size:0.75rem;color:{BMW_COLORS['text_muted']};">Score: {r['Sentiment_Score']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Bottom: Insight narrative
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,{BMW_COLORS['bg_card']} 0%,{BMW_COLORS['bg_secondary']} 100%);
                border:1px solid {BMW_COLORS['border']};border-radius:14px;padding:28px;">
        <div style="font-size:1.1rem;font-weight:700;color:{BMW_COLORS['text_primary']};margin-bottom:12px;">
            Key Findings — PitSight NLP Analysis
        </div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;font-size:0.88rem;color:{BMW_COLORS['text_secondary']};">
            <div>
                <div style="color:{BMW_COLORS['negative']};font-weight:600;margin-bottom:4px;">🔴 BMW X6 — Reliability Crisis</div>
                Service visits rose from 1.5 (2019) to 6.6 (2025). Satisfaction collapsed from 97% to 0%.
                Transmission and electronics issues are the primary drivers.
            </div>
            <div>
                <div style="color:{BMW_COLORS['positive']};font-weight:600;margin-bottom:4px;">🟢 BMW X5 — Full Recovery</div>
                Temporary quality dip in 2022 (service visits spiked to 4.0). Fixed by 2023 —
                satisfaction recovered to 99%. Facelift and quality improvements worked.
            </div>
            <div>
                <div style="color:{BMW_COLORS['accent_cyan']};font-weight:600;margin-bottom:4px;">🔵 EV Models — Maturing Fast</div>
                Service visits dropped from 2.9 to 1.0. Range satisfaction improved dramatically.
                EV customers are now among the most satisfied BMW buyers.
            </div>
            <div>
                <div style="color:{BMW_COLORS['accent_m_purple']};font-weight:600;margin-bottom:4px;">🟣 M-Series — Youth Pivot Working</div>
                Average buyer age dropped from 47 to 33. Social media-driven marketing
                is attracting younger buyers who rate performance highly.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
