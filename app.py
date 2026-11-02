from datetime import date, timedelta

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Creator Studio · Analytics", page_icon="◉", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');
:root{--bg:#0f1012;--panel:#181a1d;--line:#2c2e33;--muted:#969ba4;--ink:#f5f6f7;--red:#ff5263;--blue:#74a7ff;--green:#a2e6b6}
html,body,[class*="css"]{font-family:'DM Sans',sans-serif;color:var(--ink)}
.stApp{background:radial-gradient(ellipse at 76% 0%,#24252a 0%,#0f1012 47%);color:var(--ink)}
#MainMenu,footer,header{visibility:hidden}.block-container{max-width:1440px;padding-top:1.35rem;padding-bottom:3rem}
h1,h2,h3{font-family:'Space Grotesk',sans-serif;letter-spacing:-.04em}h1{font-size:2.4rem!important;margin:.15rem 0 .4rem!important}h2{font-size:1.35rem!important}
.topline{display:flex;justify-content:space-between;align-items:center;padding-bottom:1.15rem;border-bottom:1px solid var(--line);margin-bottom:1.6rem}
.logo{font-family:'Space Grotesk';font-weight:700;font-size:1.15rem;letter-spacing:-.04em}.logo em{font-style:normal;color:var(--red)}
.small{color:var(--muted);font-size:.86rem}.eyebrow{color:#acb1ba;font-size:.73rem;font-weight:700;letter-spacing:.14em;text-transform:uppercase}
.pill{display:inline-block;background:#25272c;border:1px solid #383a40;border-radius:100px;padding:6px 11px;color:#d7d9de;font-size:.78rem}
.panel{background:linear-gradient(145deg,#1b1d20,#17181b);border:1px solid #2b2d32;border-radius:17px;padding:18px 20px}
.metric-label{color:#a5a9b1;font-size:.83rem}.metric-value{font-family:'Space Grotesk';font-size:1.95rem;font-weight:700;letter-spacing:-.045em;margin-top:7px}.positive{font-size:.78rem;color:var(--green);margin-top:2px}
.video-thumb{height:82px;width:132px;border-radius:11px;display:grid;place-items:center;font-size:1.7rem;background:linear-gradient(145deg,#bd6c50,#563654)}
.stButton>button{border-radius:100px;border:1px solid #393b41;background:#1c1e21;color:#f5f6f7;font-weight:600}.stButton>button:hover{border-color:#ff5263;color:#ff8994}
div[data-testid="stSelectbox"]>div,div[data-testid="stDateInput"]>div>div,div[data-testid="stTextInput"]>div>div{background:#191a1e;border-color:#34363c;color:#f5f6f7}
div[data-testid="stDataFrame"]{border:1px solid #2b2d32;border-radius:12px;overflow:hidden}
div[data-testid="stSidebar"]{background:#141518;border-right:1px solid #2b2d32}
@media(max-width:760px){h1{font-size:1.9rem!important}.video-thumb{width:82px}.metric-value{font-size:1.55rem}}
</style>
""", unsafe_allow_html=True)

if "section" not in st.session_state:
    st.session_state.section = "Overview"

st.sidebar.markdown('<div class="logo">◉ Creator <em>Studio</em></div><p class="small">Your channel, made clearer.</p>', unsafe_allow_html=True)
st.sidebar.markdown("---")
section = st.sidebar.radio("Studio navigation", ["Overview", "Content", "Audience"], label_visibility="collapsed", key="section")
st.sidebar.markdown("---")
st.sidebar.markdown("**Channel** 　<span class='pill'>Demo data</span>", unsafe_allow_html=True)
st.sidebar.markdown("<span class='small'>These example metrics are synthetic and do not represent a real YouTube channel.</span>", unsafe_allow_html=True)

top_left, top_right = st.columns([3, 1])
with top_left:
    st.markdown('<div class="topline"><div><div class="logo">◉ Creator <em>Studio</em></div><div class="small">Analytics that make sense at a glance</div></div></div>', unsafe_allow_html=True)
with top_right:
    date_range = st.selectbox("Date range", ["Last 28 days", "Last 7 days", "Last 90 days"], label_visibility="collapsed")

days = {"Last 7 days": 7, "Last 28 days": 28, "Last 90 days": 90}[date_range]
end = date.today()
dates = pd.date_range(end=end, periods=days, freq="D")
base = pd.Series(range(days), dtype=float)
views = (14800 + 1100 * (base / max(days, 1)) + 5200 * ((base % 9 == 2).astype(int)) + 2700 * ((base % 13 == 7).astype(int))).astype(int)
trend = pd.DataFrame({"Date": dates, "Views": views, "Watch time (hours)": (views * 0.0068).round(1)})
total_views = int(trend["Views"].sum())
hours = int(trend["Watch time (hours)"].sum())
subs = int(total_views * 0.0018)
impressions = int(total_views * 2.73)

if section == "Overview":
    st.markdown(f'<div class="eyebrow">CHANNEL OVERVIEW · {date_range.upper()}</div><h1>Your channel at a glance.</h1><p class="small">A clearer picture of what’s working and where to go next.</p>', unsafe_allow_html=True)
    m1,m2,m3,m4=st.columns(4)
    metrics=[("Views",f"{total_views/1000:.1f}K","↑ 12.8% vs previous period"),("Watch time",f"{hours:,} hrs","↑ 8.4% vs previous period"),("Subscribers",f"+{subs:,}","↑ 6.2% vs previous period"),("Impressions",f"{impressions/1000:.1f}K","↑ 10.1% vs previous period")]
    for col,(label,value,delta) in zip([m1,m2,m3,m4],metrics):
        with col:
            st.markdown(f'<div class="panel"><div class="metric-label">{label}</div><div class="metric-value">{value}</div><div class="positive">{delta}</div></div>',unsafe_allow_html=True)
    st.write("")
    left,right=st.columns([1.8,1],gap="large")
    with left:
        st.markdown('<div class="panel">',unsafe_allow_html=True)
        st.markdown("### Views over time")
        st.markdown('<div class="small">Daily views · hover to explore individual days</div>',unsafe_allow_html=True)
        chart=trend.set_index("Date")[["Views"]]
        st.area_chart(chart, color="#ff5263", height=280)
        st.markdown('</div>',unsafe_allow_html=True)
    with right:
        st.markdown('<div class="panel">',unsafe_allow_html=True)
        st.markdown("### Where views came from")
        sources=pd.DataFrame({"Traffic source":["Shorts feed","YouTube search","Browse features","Suggested videos","Other"],"Share":[58,17,12,8,5]})
        st.bar_chart(sources.set_index("Traffic source"), color="#74a7ff", height=245)
        st.markdown('<div class="small">Shorts feed is your biggest discovery source.</div></div>',unsafe_allow_html=True)
    st.write("")
    st.markdown("### Top videos")
    st.markdown('<div class="small">Ranked by views in this period</div>',unsafe_allow_html=True)
    videos=pd.DataFrame([
        {"Video":"5-minute desk stretch","Format":"Short","Views":"42.8K","Avg. view duration":"0:38","Likes":"96.4%","Change":"↑ 18%"},
        {"Video":"My quiet Sunday reset","Format":"Short","Views":"31.2K","Avg. view duration":"0:42","Likes":"98.1%","Change":"↑ 11%"},
        {"Video":"3 things I wish I knew sooner","Format":"Short","Views":"24.6K","Avg. view duration":"0:29","Likes":"94.8%","Change":"↑ 7%"},
        {"Video":"A week of simple lunches","Format":"Video","Views":"18.3K","Avg. view duration":"4:12","Likes":"97.2%","Change":"↑ 3%"},
    ])
    st.dataframe(videos,hide_index=True,use_container_width=True)
    st.markdown('<div class="panel"><div class="eyebrow">A useful takeaway</div><h3>Shorts are bringing new people in.</h3><div class="small">The Shorts feed accounts for 58% of your views. Try following up your best-performing Short with a related video to give new viewers a next step.</div></div>',unsafe_allow_html=True)

elif section == "Content":
    st.markdown('<div class="eyebrow">CONTENT PERFORMANCE</div><h1>See what’s resonating.</h1><p class="small">Compare videos using the metrics that matter to you.</p>',unsafe_allow_html=True)
    sort_by=st.selectbox("Compare by",["Views","Watch time","Average view duration","Likes"])
    left,right=st.columns([1.25,1],gap="large")
    with left:
        chart_data=pd.DataFrame({"Video":["Desk stretch","Sunday reset","Wish I knew","Simple lunches"],"Views":[42.8,31.2,24.6,18.3],"Watch time":[25.4,20.1,12.7,40.6],"Likes":[96,98,95,97]})
        st.markdown("### Compare videos")
        st.bar_chart(chart_data.set_index("Video")[["Views"]],color="#ff5263",height=300)
    with right:
        st.markdown("### Keep an eye on")
        for title,copy in [("Strong opening","Your top Short keeps viewers for 38 seconds on average."),("Room to grow","Search brings 17% of views. Try using the phrase viewers search for in titles."),("Healthy engagement","Likes stay above 94% across your top videos.")]:
            st.markdown(f'<div class="panel" style="margin-bottom:10px"><b>{title}</b><div class="small" style="margin-top:6px">{copy}</div></div>',unsafe_allow_html=True)
    st.markdown("### Recent uploads")
    st.dataframe(pd.DataFrame([
        {"Title":"5-minute desk stretch","Published":"2 days ago","Views":"42.8K","Avg. view duration":"0:38","Likes":"96.4%"},
        {"Title":"My quiet Sunday reset","Published":"5 days ago","Views":"31.2K","Avg. view duration":"0:42","Likes":"98.1%"},
        {"Title":"3 things I wish I knew sooner","Published":"9 days ago","Views":"24.6K","Avg. view duration":"0:29","Likes":"94.8%"},
        {"Title":"A week of simple lunches","Published":"12 days ago","Views":"18.3K","Avg. view duration":"4:12","Likes":"97.2%"},
    ]),hide_index=True,use_container_width=True)

else:
    st.markdown('<div class="eyebrow">YOUR AUDIENCE</div><h1>Know who’s watching.</h1><p class="small">Simple signals to help you make more of what your audience loves.</p>',unsafe_allow_html=True)
    c1,c2,c3=st.columns(3)
    for col,label,value,delta in [(c1,"Returning viewers","38.2%","↑ 4.1 pts"),(c2,"Average view duration","0:36","↑ 0:04"),(c3,"Subscribers gained","+1,284","↑ 6.2%")]:
        with col: st.markdown(f'<div class="panel"><div class="metric-label">{label}</div><div class="metric-value">{value}</div><div class="positive">{delta} vs previous period</div></div>',unsafe_allow_html=True)
    st.write("")
    left,right=st.columns(2,gap="large")
    with left:
        st.markdown("### Subscriber growth")
        subs_line=pd.DataFrame({"Date":dates,"Subscribers":(base*6+250+((base%10==4)*48)).astype(int)}).set_index("Date")
        st.line_chart(subs_line,color="#a2e6b6",height=280)
    with right:
        st.markdown("### Who’s watching")
        age=pd.DataFrame({"Age group":["18–24","25–34","35–44","45–54","55+"],"Share of viewers":[19,38,24,12,7]}).set_index("Age group")
        st.bar_chart(age,color="#74a7ff",height=280)
    st.markdown('<div class="panel"><div class="eyebrow">AUDIENCE TIP</div><h3>Your 25–34 audience is growing.</h3><div class="small">That group now makes up 38% of viewers. Compare the topics and formats they watch most before planning your next upload.</div></div>',unsafe_allow_html=True)

st.markdown('<div style="border-top:1px solid #2c2e33;margin-top:28px;padding-top:16px" class="small">Creator Studio analytics concept · Sample data for demonstration · Not affiliated with YouTube</div>',unsafe_allow_html=True)
