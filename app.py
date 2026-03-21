import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="PitSight — BMW Intelligence", page_icon="🏎️", layout="wide", initial_sidebar_state="expanded")

# ═══════════════════════════════════════════
# CSS — BMW iDRIVE PREMIUM DARK THEME
# ═══════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700;800&display=swap');

:root {
    --bg-deep: #060B18;
    --bg-card: rgba(12,20,40,0.85);
    --bg-card-hover: rgba(18,30,55,0.95);
    --border: rgba(50,80,140,0.25);
    --glow: rgba(30,136,229,0.15);
    --accent: #1E88E5;
    --cyan: #00E5FF;
    --text: #E8ECF1;
    --text2: #8899B0;
    --text3: #4A5F7A;
    --green: #00E676;
    --red: #FF5252;
    --amber: #FFAB00;
    --m-blue: #0066B1;
    --m-red: #E2001A;
    --m-purple: #7B3FE4;
}

.stApp {
    background: linear-gradient(165deg, #060B18 0%, #0A1628 40%, #0D1B30 100%);
    font-family: 'DM Sans', sans-serif;
}
.main .block-container { padding: 1rem 1.5rem; max-width: 100%; }

/* Hide defaults */
#MainMenu, footer, header { visibility: hidden; }

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #080E1E 0%, #0A1225 100%);
    border-right: 1px solid var(--border);
}

/* Glass card */
.glass {
    background: var(--bg-card);
    backdrop-filter: blur(20px);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 12px;
    box-shadow: 0 4px 30px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.03);
}
.glass:hover {
    border-color: rgba(30,136,229,0.4);
    box-shadow: 0 4px 40px var(--glow);
}

/* M-stripe */
.m-line {
    height: 2px;
    background: linear-gradient(90deg, var(--m-blue), var(--m-purple), var(--m-red));
    border-radius: 1px;
    margin: 8px 0 20px;
}

/* KPI */
.kpi {
    background: linear-gradient(135deg, rgba(30,136,229,0.12) 0%, rgba(0,229,255,0.06) 100%);
    border: 1px solid rgba(30,136,229,0.2);
    border-radius: 14px;
    padding: 22px 16px;
    text-align: center;
    box-shadow: 0 0 20px rgba(30,136,229,0.05);
}
.kpi-val { font-size: 1.9rem; font-weight: 800; line-height: 1.1; }
.kpi-lab { font-size: 0.72rem; color: var(--text2); text-transform: uppercase; letter-spacing: 1.5px; margin-top: 6px; }

/* Section label */
.sec { font-size: 0.78rem; font-weight: 600; color: var(--text3); text-transform: uppercase; letter-spacing: 2px; margin: 20px 0 12px; padding-bottom: 8px; border-bottom: 1px solid var(--border); }

/* Badges */
.badge-g { background: rgba(0,230,118,0.12); color: var(--green); padding: 3px 10px; border-radius: 20px; font-size: 0.78rem; font-weight: 600; }
.badge-r { background: rgba(255,82,82,0.12); color: var(--red); padding: 3px 10px; border-radius: 20px; font-size: 0.78rem; font-weight: 600; }

/* Model cards */
.mcard {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 14px 8px;
    text-align: center;
    transition: all 0.2s;
}
.mcard:hover { border-color: var(--accent); transform: translateY(-2px); box-shadow: 0 8px 25px var(--glow); }
.mcard-active { border-color: var(--cyan); box-shadow: 0 0 15px rgba(0,229,255,0.15); }

/* Insight card */
.insight {
    background: linear-gradient(135deg, var(--bg-card) 0%, rgba(10,22,40,0.9) 100%);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 28px;
}

/* Review card */
.rev-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 10px;
}

/* Scrollbar */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }

/* Radio pills */
div[data-testid="stRadio"] > div { gap: 0; }
div[data-testid="stRadio"] label { font-size: 0.85rem; }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════
# LOAD DATA
# ═══════════════════════════════════════════
@st.cache_data
def load_data():
    from pathlib import Path
    d = Path(__file__).parent.resolve()
    t1 = pd.read_csv(d / 'table1.csv')
    p2 = d / 'table2.csv.gz'
    if not p2.exists():
        p2 = d / 'table2.csv'
    if not p2.exists():
        st.error(f"table2 not found. Files in dir: {[f.name for f in d.iterdir()]}")
        st.stop()
    t2 = pd.read_csv(p2)
    t1['Date'] = pd.to_datetime(t1['Date'], format='%d/%m/%Y')
    t1['Month'] = t1['Date'].dt.month
    t1['Weekday'] = t1['Date'].dt.day_name()
    t2['Date'] = pd.to_datetime(t2['Date'], format='%d/%m/%Y')
    return t1, t2

df1, df2 = load_data()

# Chart theme
def dark_layout(h=340):
    return dict(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='DM Sans', color='#8899B0', size=11),
        margin=dict(l=40, r=20, t=30, b=40), height=h,
        xaxis=dict(gridcolor='rgba(40,60,100,0.2)', zeroline=False),
        yaxis=dict(gridcolor='rgba(40,60,100,0.2)', zeroline=False),
        legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(size=10)),
        hoverlabel=dict(bgcolor='#0D1B30', font_size=11, font_family='DM Sans'),
    )

# ═══════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:8px 0 16px;">
        <div style="font-size:1.6rem;font-weight:800;letter-spacing:3px;color:#E8ECF1;">PIT<span style="color:#00E5FF;">SIGHT</span></div>
        <div style="font-size:0.62rem;color:#4A5F7A;letter-spacing:2px;">BMW INTELLIGENCE PLATFORM</div>
        <div style="height:2px;background:linear-gradient(90deg,#0066B1,#7B3FE4,#E2001A);border-radius:1px;margin-top:10px;"></div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio("NAV", ["📊 Dashboard", "🏎️ All Models", "🔍 Sentiment Intelligence"], label_visibility="collapsed")

    st.markdown('<div style="margin-top:16px;"></div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.68rem;color:#4A5F7A;letter-spacing:1.5px;font-weight:600;">FILTERS</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        sel_y = st.multiselect("Year", sorted(df1['Year'].unique()), default=sorted(df1['Year'].unique()), key='fy')
    with c2:
        sel_ch = st.multiselect("Channel", sorted(df1['Channel'].unique()), default=sorted(df1['Channel'].unique()), key='fch')

    sel_r = st.multiselect("Region", sorted(df1['Region'].unique()), default=sorted(df1['Region'].unique()), key='fr')
    sel_co = st.multiselect("Country", sorted(df1['Country'].unique()), default=sorted(df1['Country'].unique()), key='fco')
    sel_m = st.multiselect("Model", sorted(df1['Model'].unique()), default=[], key='fm')

    st.markdown("""
    <div style="text-align:center;padding:30px 0 10px;">
        <div style="font-size:2rem;font-weight:900;color:#E8ECF1;letter-spacing:5px;">BMW</div>
        <div style="font-size:0.58rem;color:#4A5F7A;letter-spacing:1px;">SHEER DRIVING PLEASURE</div>
    </div>
    """, unsafe_allow_html=True)

# Apply filters
f1 = df1[(df1['Year'].isin(sel_y)) & (df1['Region'].isin(sel_r)) & (df1['Country'].isin(sel_co)) & (df1['Channel'].isin(sel_ch))]
if sel_m: f1 = f1[f1['Model'].isin(sel_m)]
f2 = df2[(df2['Year'].isin(sel_y)) & (df2['Country'].isin(sel_co))]
if sel_m: f2 = f2[f2['Model'].isin(sel_m)]

# ═══════════════════════════════════════════
# PAGE 1: DASHBOARD
# ═══════════════════════════════════════════
if page == "📊 Dashboard":
    st.markdown('<div class="m-line"></div>', unsafe_allow_html=True)
    tg = st.radio("", ["Year", "Month", "Weekday"], horizontal=True, label_visibility="collapsed")

    cL, cR = st.columns([3.2, 1])
    with cL:
        st.markdown('<div class="sec">Global Sales</div>', unsafe_allow_html=True)
        mn = {1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'Jun',7:'Jul',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec'}
        if tg == "Year":
            a = f1.groupby('Year').agg(Rev=('Revenue','sum'), Qty=('Quantity Sold','sum')).reset_index()
            a['PY'] = a['Rev'].shift(1)
            xc = 'Year'
        elif tg == "Month":
            a = f1.groupby('Month').agg(Rev=('Revenue','sum'), Qty=('Quantity Sold','sum')).reset_index()
            a['Label'] = a['Month'].map(mn)
            a['PY'] = a['Rev'].shift(1).fillna(a['Rev'].mean())
            xc = 'Label'
        else:
            do = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
            a = f1.groupby('Weekday').agg(Rev=('Revenue','sum'), Qty=('Quantity Sold','sum')).reset_index()
            a['Weekday'] = pd.Categorical(a['Weekday'], categories=do, ordered=True)
            a = a.sort_values('Weekday')
            a['PY'] = a['Rev'].mean()
            xc = 'Weekday'

        fig = go.Figure()
        fig.add_bar(x=a[xc], y=a['Rev'], name='Revenue', marker=dict(color='#1A5BA8', line=dict(width=0)), opacity=0.85)
        if 'PY' in a.columns:
            fig.add_scatter(x=a[xc], y=a['PY'], name='PY Revenue', mode='lines+markers',
                           line=dict(color='#5DB8FE', width=2.5, dash='dot'), marker=dict(size=5, color='#5DB8FE'))
        fig.update_layout(**dark_layout(320), yaxis_tickformat='$,.0s',
                         legend=dict(orientation='h', y=-0.18, x=0.5, xanchor='center'))
        st.plotly_chart(fig, use_container_width=True, key='gs')

    with cR:
        tr = f1['Revenue'].sum()
        tq = int(f1['Quantity Sold'].sum())
        mx = int(f1['Year'].max()) if len(f1) else 2025
        cy = f1[f1['Year']==mx]['Revenue'].sum()
        py = f1[f1['Year']==mx-1]['Revenue'].sum()
        pc = ((cy-py)/py*100) if py>0 else 0
        arr = '↑' if pc>=0 else '↓'
        col = '#00E676' if pc>=0 else '#FF5252'

        st.markdown(f"""
        <div class="glass" style="background:linear-gradient(135deg,rgba(30,136,229,0.15),rgba(0,229,255,0.05));padding:24px;">
            <div style="font-size:0.72rem;color:#4A5F7A;letter-spacing:1px;">PERIOD TOTAL</div>
            <div style="font-size:2.2rem;font-weight:800;color:#E8ECF1;margin:6px 0 2px;">${tr/1e9:.2f}bn</div>
            <div style="font-size:1rem;font-weight:600;color:{col};">{arr} {abs(pc):.1f}%</div>
            <div style="font-size:0.82rem;color:#4A5F7A;margin-top:4px;">PY ${py/1e9:.2f}bn</div>
            <div style="margin-top:18px;padding-top:14px;border-top:1px solid rgba(50,80,140,0.25);">
                <div style="font-size:0.72rem;color:#4A5F7A;letter-spacing:1px;">UNITS SOLD</div>
                <div style="font-size:1.6rem;font-weight:700;color:#00E5FF;">{tq:,}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Top Models
    st.markdown('<div class="sec">Top Selling Models</div>', unsafe_allow_html=True)
    tm = f1.groupby('Model')['Quantity Sold'].sum().sort_values(ascending=False).head(8).reset_index()
    cols = st.columns(min(len(tm), 8))
    for i, (_, r) in enumerate(tm.iterrows()):
        if i < len(cols):
            with cols[i]:
                st.markdown(f"""<div class="mcard">
                    <div style="font-size:0.82rem;font-weight:600;color:#E8ECF1;">{r['Model'].replace('BMW ','')}</div>
                    <div style="font-size:1.15rem;font-weight:700;color:#00E5FF;">{int(r['Quantity Sold']):,}</div>
                </div>""", unsafe_allow_html=True)

    # Bottom row
    c1, c2, c3 = st.columns([2, 1.2, 1.2])
    with c1:
        st.markdown('<div class="sec">Country-wise Sales</div>', unsafe_allow_html=True)
        cd = f1.groupby('Country').agg(Qty=('Quantity Sold','sum'), Rev=('Revenue','sum')).sort_values('Qty', ascending=False).head(12).reset_index()
        cd['Rev_fmt'] = cd['Rev'].apply(lambda x: f"${x/1e6:.0f}M")
        cd['Qty_fmt'] = cd['Qty'].apply(lambda x: f"{x:,}")
        st.dataframe(cd[['Country','Qty_fmt','Rev_fmt']].rename(columns={'Qty_fmt':'Units','Rev_fmt':'Revenue'}),
                     hide_index=True, use_container_width=True, height=360)

    with c2:
        st.markdown('<div class="sec">Channel Split</div>', unsafe_allow_html=True)
        ch = f1.groupby('Channel')['Quantity Sold'].sum().reset_index()
        fig_d = go.Figure(go.Pie(
            labels=ch['Channel'], values=ch['Quantity Sold'], hole=0.7,
            marker=dict(colors=['#1A5BA8','#00E5FF','#7B3FE4']),
            textinfo='label+percent', textfont=dict(size=10, color='#8899B0'),
        ))
        fig_d.update_layout(**dark_layout(320), showlegend=False,
                          annotations=[dict(text=f"<b>{tq/1e3:.0f}K</b>", x=0.5, y=0.5, font_size=20, font_color='#E8ECF1', showarrow=False)])
        st.plotly_chart(fig_d, use_container_width=True, key='ch')

    with c3:
        st.markdown('<div class="sec">Yearly Volume</div>', unsafe_allow_html=True)
        yq = f1.groupby('Year')['Quantity Sold'].sum().reset_index()
        fig_y = go.Figure(go.Bar(x=yq['Year'], y=yq['Quantity Sold'], marker=dict(color='#1A5BA8', line=dict(width=0))))
        fig_y.update_layout(**dark_layout(320), yaxis_tickformat=',', showlegend=False)
        st.plotly_chart(fig_y, use_container_width=True, key='yv')


# ═══════════════════════════════════════════
# PAGE 2: ALL MODELS
# ═══════════════════════════════════════════
elif page == "🏎️ All Models":
    st.markdown('<div class="m-line"></div>', unsafe_allow_html=True)
    sm = st.selectbox("Search Model", sorted(f1['Model'].unique()), index=0, label_visibility="collapsed")
    st.markdown(f'<div style="font-size:2rem;font-weight:800;color:#E8ECF1;margin:12px 0 6px;">{sm}</div>', unsafe_allow_html=True)

    md = f1[f1['Model']==sm]
    cL, cR = st.columns([1, 1.5])

    with cL:
        st.markdown('<div class="sec">Yearly Performance</div>', unsafe_allow_html=True)
        ym = md.groupby('Year').agg(Qty=('Quantity Sold','sum'), Rev=('Revenue','sum')).reset_index()
        for _, r in ym.iterrows():
            st.markdown(f"""<div style="display:flex;justify-content:space-between;padding:8px 12px;border-bottom:1px solid rgba(50,80,140,0.2);font-size:0.9rem;">
                <span style="color:#8899B0;">{int(r['Year'])}</span>
                <span style="color:#00E5FF;font-weight:600;">{int(r['Qty']):,}</span>
                <span style="color:#E8ECF1;font-weight:600;">${r['Rev']/1e6:.0f}M</span>
            </div>""", unsafe_allow_html=True)

        tq = int(ym['Qty'].sum())
        tr = ym['Rev'].sum()
        st.markdown(f"""<div style="display:flex;justify-content:space-between;padding:10px 12px;background:rgba(30,136,229,0.08);border-radius:8px;margin-top:8px;font-size:0.92rem;">
            <span style="color:#1E88E5;font-weight:700;">Total</span>
            <span style="color:#00E5FF;font-weight:700;">{tq:,}</span>
            <span style="color:#E8ECF1;font-weight:700;">${tr/1e6:.0f}M</span>
        </div>""", unsafe_allow_html=True)

        ap = md['Revenue'].sum() / max(md['Quantity Sold'].sum(), 1)
        st.markdown(f"""<div style="margin-top:24px;">
            <div style="font-size:2.2rem;font-weight:800;color:#E8ECF1;">${ap/1e3:.1f}K</div>
            <div style="font-size:0.78rem;color:#4A5F7A;text-transform:uppercase;letter-spacing:1px;">Average Price</div>
        </div>""", unsafe_allow_html=True)

    with cR:
        fig_m = go.Figure()
        fig_m.add_bar(x=ym['Year'], y=ym['Rev'], name='Revenue', marker=dict(color='#1A5BA8'))
        fig_m.add_scatter(x=ym['Year'], y=ym['Qty'], name='Units', mode='lines+markers',
                         line=dict(color='#00E5FF', width=3), marker=dict(size=7, color='#00E5FF'), yaxis='y2')
        fig_m.update_layout(**dark_layout(380),
            yaxis=dict(title='Revenue', tickformat='$,.0s', gridcolor='rgba(40,60,100,0.2)'),
            yaxis2=dict(title='Units', overlaying='y', side='right', showgrid=False),
            legend=dict(orientation='h', y=-0.15, x=0.5, xanchor='center'))
        st.plotly_chart(fig_m, use_container_width=True, key='mp')

    # Model carousel
    st.markdown('<div class="sec">Browse Models</div>', unsafe_allow_html=True)
    ta = f1.groupby('Model')['Quantity Sold'].sum().sort_values(ascending=False).head(8).reset_index()
    cols = st.columns(min(len(ta), 8))
    for i, (_, r) in enumerate(ta.iterrows()):
        if i < len(cols):
            with cols[i]:
                ac = "mcard mcard-active" if r['Model']==sm else "mcard"
                st.markdown(f"""<div class="{ac}">
                    <div style="font-size:0.8rem;font-weight:{'700' if r['Model']==sm else '500'};color:#E8ECF1;">{r['Model'].replace('BMW ','')}</div>
                    <div style="font-size:1rem;font-weight:600;color:#00E5FF;">{int(r['Quantity Sold']):,}</div>
                </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════
# PAGE 3: SENTIMENT INTELLIGENCE
# ═══════════════════════════════════════════
elif page == "🔍 Sentiment Intelligence":
    st.markdown('<div class="m-line"></div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div style="font-size:1.5rem;font-weight:800;color:#E8ECF1;margin-bottom:4px;">Sentiment Intelligence</div>
    <div style="font-size:0.85rem;color:#4A5F7A;margin-bottom:20px;">Understanding the WHY behind sales trends — {len(f2):,} customer reviews analyzed</div>
    """, unsafe_allow_html=True)

    # KPIs
    nr = len(f2)
    ps = (f2['Sentiment_Label']=='Satisfied').mean()*100 if len(f2)>0 else 0
    as_ = f2['Service_History'].mean() if len(f2)>0 else 0
    ad = f2['Delivery_Days'].mean() if len(f2)>0 else 0

    k1,k2,k3,k4 = st.columns(4)
    for c, v, l, co in [(k1,f"{nr:,}","Total Reviews","#1E88E5"),(k2,f"{ps:.1f}%","Satisfied","#00E676"),
                        (k3,f"{as_:.1f}","Avg Service Visits","#FFAB00"),(k4,f"{ad:.0f} days","Avg Delivery","#00E5FF")]:
        with c:
            st.markdown(f'<div class="kpi"><div class="kpi-val" style="color:{co};">{v}</div><div class="kpi-lab">{l}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Satisfaction by Model + Trend
    cL, cR = st.columns([1.2, 1])
    with cL:
        st.markdown('<div class="sec">Satisfaction Rate by Model</div>', unsafe_allow_html=True)
        ms = f2.groupby('Model').apply(lambda x: (x['Sentiment_Label']=='Satisfied').mean()*100).reset_index(name='Sat')
        ms = ms.sort_values('Sat')
        colors = ['#FF5252' if v < 50 else '#FFAB00' if v < 80 else '#00E676' for v in ms['Sat']]
        fig_ms = go.Figure(go.Bar(
            y=ms['Model'].str.replace('BMW ',''), x=ms['Sat'], orientation='h',
            marker=dict(color=colors), text=ms['Sat'].apply(lambda x: f'{x:.0f}%'), textposition='outside', textfont=dict(size=9)))
        fig_ms.update_layout(**dark_layout(520), xaxis=dict(title='% Satisfied', range=[0,110], gridcolor='rgba(40,60,100,0.2)'))
        st.plotly_chart(fig_ms, use_container_width=True, key='msat')

    with cR:
        st.markdown('<div class="sec">Satisfaction Trend</div>', unsafe_allow_html=True)
        ys = f2.groupby('Year').apply(lambda x: pd.Series({
            'Sat': (x['Sentiment_Label']=='Satisfied').mean()*100,
            'Svc': x['Service_History'].mean()
        })).reset_index()
        fig_t = go.Figure()
        fig_t.add_scatter(x=ys['Year'], y=ys['Sat'], name='% Satisfied', mode='lines+markers',
                         line=dict(color='#00E676', width=3), marker=dict(size=7), fill='tozeroy', fillcolor='rgba(0,230,118,0.05)')
        fig_t.add_scatter(x=ys['Year'], y=ys['Svc']*30, name='Svc Visits (scaled)', mode='lines+markers',
                         line=dict(color='#FF5252', width=2, dash='dot'), marker=dict(size=5))
        fig_t.update_layout(**dark_layout(340), yaxis=dict(title='% Satisfied', gridcolor='rgba(40,60,100,0.2)'),
                          legend=dict(orientation='h', y=-0.2, x=0.5, xanchor='center'))
        st.plotly_chart(fig_t, use_container_width=True, key='trend')

    # Heatmap + Spotlight
    cL2, cR2 = st.columns([1.2, 1])
    with cL2:
        st.markdown('<div class="sec">Aspect Scores by Category</div>', unsafe_allow_html=True)
        def cat(m):
            if m.startswith('BMW i') or m=='BMW iX': return 'EV'
            elif m.startswith('BMW M'): return 'M-Series'
            elif m.startswith('BMW X'): return 'X-Series'
            else: return 'Sedan'
        f2c = f2.copy(); f2c['Cat'] = f2c['Model'].apply(cat)
        hm = []
        for ct in ['Sedan','X-Series','M-Series','EV']:
            s = f2c[f2c['Cat']==ct]
            row = {'Cat': ct}
            for asp in ['maintenance_score','comfort_score','technology_score','service_experience_score','fuel_or_range_score']:
                v = s[s[asp]>0][asp]
                row[asp.replace('_score','').replace('_',' ').title()] = round(v.mean(),1) if len(v)>0 else 0
            hm.append(row)
        hdf = pd.DataFrame(hm).set_index('Cat')
        fig_h = go.Figure(go.Heatmap(
            z=hdf.values, x=hdf.columns, y=hdf.index,
            colorscale=[[0,'#FF5252'],[0.5,'#FFAB00'],[1,'#00E676']], zmin=1, zmax=5,
            text=hdf.values, texttemplate='%{text}', textfont=dict(size=12, color='white')))
        fig_h.update_layout(**dark_layout(260))
        st.plotly_chart(fig_h, use_container_width=True, key='hm')

    with cR2:
        st.markdown('<div class="sec">Spotlight: X6 vs X5</div>', unsafe_allow_html=True)
        sp = []
        for m in ['BMW X6','BMW X5']:
            s = f2[f2['Model']==m]
            for y in sorted(s['Year'].unique()):
                sy = s[s['Year']==y]
                sp.append({'Model':m.replace('BMW ',''),'Year':y,'Sat':(sy['Sentiment_Label']=='Satisfied').mean()*100})
        spd = pd.DataFrame(sp)
        fig_sp = go.Figure()
        for m, co in [('X6','#FF5252'),('X5','#00E676')]:
            d = spd[spd['Model']==m]
            fig_sp.add_scatter(x=d['Year'], y=d['Sat'], name=m, mode='lines+markers', line=dict(color=co, width=3), marker=dict(size=7))
        fig_sp.update_layout(**dark_layout(260), yaxis=dict(title='% Satisfied', range=[0,105], gridcolor='rgba(40,60,100,0.2)'),
                           legend=dict(orientation='h', y=-0.2, x=0.5, xanchor='center'))
        st.plotly_chart(fig_sp, use_container_width=True, key='sp')

    # Feature Importance + Reviews
    cL3, cR3 = st.columns([1, 1.2])
    with cL3:
        st.markdown('<div class="sec">ML Feature Importance</div>', unsafe_allow_html=True)
        fi = pd.DataFrame({'F':['Service History','Delivery Days','Customer Age','Warranty Years','Is EV'],
                          'I':[46.3,41.2,9.4,2.4,0.8]}).sort_values('I')
        fig_fi = go.Figure(go.Bar(y=fi['F'], x=fi['I'], orientation='h',
                                  marker=dict(color=['#4A5F7A','#4A5F7A','#1E88E5','#1E88E5','#1E88E5']),
                                  text=fi['I'].apply(lambda x: f'{x:.1f}%'), textposition='outside', textfont=dict(size=10)))
        fig_fi.update_layout(**dark_layout(240), xaxis=dict(title='Importance %', gridcolor='rgba(40,60,100,0.2)'))
        st.plotly_chart(fig_fi, use_container_width=True, key='fi')

        st.markdown("""<div class="glass" style="border-left:2px solid #1E88E5;">
            <div style="font-size:0.85rem;color:#E8ECF1;font-weight:600;">Random Forest — 91.5% Accuracy</div>
            <div style="font-size:0.78rem;color:#4A5F7A;margin-top:4px;">Service History + Delivery Days = 87.5% of prediction power.</div>
        </div>""", unsafe_allow_html=True)

    with cR3:
        st.markdown('<div class="sec">Review Explorer</div>', unsafe_allow_html=True)
        rm = st.selectbox("Model", sorted(f2['Model'].unique()), key='rm2')
        rs = st.selectbox("Sentiment", ['All','Satisfied','Dissatisfied'], key='rs2')
        rf = f2[f2['Model']==rm]
        if rs != 'All': rf = rf[rf['Sentiment_Label']==rs]
        samp = rf.sample(min(4, len(rf)), random_state=42) if len(rf)>0 else rf
        for _, r in samp.iterrows():
            bc = "badge-g" if r['Sentiment_Label']=='Satisfied' else "badge-r"
            st.markdown(f"""<div class="rev-card">
                <div style="display:flex;justify-content:space-between;margin-bottom:6px;">
                    <span style="font-size:0.72rem;color:#4A5F7A;">{r['Customer_ID']} · {int(r['Year'])} · Svc={int(r['Service_History'])}</span>
                    <span class="{bc}">{r['Sentiment_Label']}</span>
                </div>
                <div style="font-size:0.84rem;color:#C0CAD8;line-height:1.5;">"{str(r['Customer_Review'])[:180]}..."</div>
                <div style="display:flex;gap:10px;margin-top:6px;">
                    <span style="font-size:0.7rem;color:#4A5F7A;">Maint:{r['maintenance_score']}</span>
                    <span style="font-size:0.7rem;color:#4A5F7A;">Tech:{r['technology_score']}</span>
                    <span style="font-size:0.7rem;color:#4A5F7A;">Svc:{r['service_experience_score']}</span>
                    <span style="font-size:0.7rem;color:#4A5F7A;">Score:{r['Sentiment_Score']}</span>
                </div>
            </div>""", unsafe_allow_html=True)

    # Key findings
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""<div class="insight">
        <div style="font-size:1.05rem;font-weight:700;color:#E8ECF1;margin-bottom:14px;">Key Findings</div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;font-size:0.84rem;color:#8899B0;">
            <div><span style="color:#FF5252;font-weight:600;">🔴 BMW X6</span> — Service visits: 1.5→6.6. Satisfaction: 97%→0%. Reliability crisis.</div>
            <div><span style="color:#00E676;font-weight:600;">🟢 BMW X5</span> — 2022 dip fixed. Satisfaction recovered from 21% to 99%.</div>
            <div><span style="color:#00E5FF;font-weight:600;">🔵 EVs</span> — Service visits dropped 2.9→1.0. Most satisfied segment by 2025.</div>
            <div><span style="color:#7B3FE4;font-weight:600;">🟣 M-Series</span> — Buyer age 47→33. Youth marketing working. Sales doubled.</div>
        </div>
    </div>""", unsafe_allow_html=True)
