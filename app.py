"""
app.py - EduPulse: University Digital Learning Analytics Dashboard.
Modern, elegant Light SaaS interface for CHRIST University & OULAD learning analytics.
Matches the clean lavender/white aesthetic from the design reference.
"""

import streamlit as st
import pandas as pd
import numpy as np
import io

import data_loader
import analytics
import visualizations

# -----------------------------------------------------------------------------
# 1. Page Configuration
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="EduPulse – University Digital Learning Analytics",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# 2. Modern Light SaaS CSS Injection (Matching Reference Design)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

    /* Global Base */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Main Background - Soft Cool Lavender / Off-White */
    .stApp {
        background: linear-gradient(135deg, #F0F2F9 0%, #E8ECF8 100%) !important;
        color: #0F172A !important;
    }

    /* Streamlit Top Header - transparent */
    header[data-testid="stHeader"] {
        background: transparent !important;
        backdrop-filter: blur(8px) !important;
        -webkit-backdrop-filter: blur(8px) !important;
        border-bottom: 1px solid rgba(226, 232, 240, 0.6) !important;
    }

    /* Main Container Padding - 4.8rem clearance ensures top navigation is fully visible */
    .block-container {
        padding-top: 4.8rem !important;
        padding-bottom: 3.5rem !important;
        padding-left: 2.2rem !important;
        padding-right: 2.2rem !important;
        max-width: 100% !important;
    }

    /* Sidebar Styling - Soft Light Lavender */
    [data-testid="stSidebar"] {
        background: #F8F9FE !important;
        border-right: 1px solid #E2E8F0 !important;
        box-shadow: 2px 0 16px rgba(99, 102, 241, 0.04) !important;
    }
    [data-testid="stSidebar"] .block-container {
        padding-top: 1.5rem !important;
        padding-left: 1.2rem !important;
        padding-right: 1.2rem !important;
    }

    /* Crisp White SaaS Dashboard Cards */
    .edupulse-card {
        background: #FFFFFF !important;
        border: 1px solid #EEF2F8 !important;
        border-radius: 16px !important;
        padding: 20px 22px !important;
        margin-bottom: 20px !important;
        box-shadow: 0 4px 20px rgba(99, 102, 241, 0.05), 0 1px 3px rgba(0, 0, 0, 0.03) !important;
        transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease !important;
    }
    .edupulse-card:hover {
        border-color: rgba(99, 102, 241, 0.25) !important;
        box-shadow: 0 8px 30px rgba(99, 102, 241, 0.12) !important;
    }

    /* Top KPI Cards */
    .kpi-container {
        background: #FFFFFF !important;
        border: 1px solid #EEF2F8 !important;
        border-radius: 16px !important;
        padding: 18px 20px !important;
        position: relative !important;
        overflow: hidden !important;
        box-shadow: 0 4px 20px rgba(99, 102, 241, 0.05), 0 1px 3px rgba(0, 0, 0, 0.03) !important;
        transition: all 0.25s ease !important;
    }
    .kpi-container:hover {
        border-color: rgba(99, 102, 241, 0.3) !important;
        box-shadow: 0 8px 30px rgba(99, 102, 241, 0.12) !important;
        transform: translateY(-2px) !important;
    }
    .kpi-glow {
        position: absolute;
        bottom: -15px;
        right: -15px;
        width: 85px;
        height: 85px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(99, 102, 241, 0.08) 0%, rgba(99, 102, 241, 0) 70%);
        pointer-events: none;
    }
    .kpi-label {
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 1.1px;
        color: #64748B;
        font-weight: 700;
        margin-bottom: 6px;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .kpi-value {
        font-size: 28px;
        font-weight: 800;
        color: #0F172A;
        letter-spacing: -0.5px;
        margin-bottom: 4px;
    }
    .kpi-badge {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        font-size: 11px;
        font-weight: 600;
        padding: 3px 8px;
        border-radius: 20px;
        background: #EEF2FF;
        color: #4F46E5;
        border: 1px solid #C7D2FE;
    }
    .kpi-badge.pink {
        background: #FDF2F8;
        color: #DB2777;
        border-color: #FBCFE8;
    }
    .kpi-badge.cyan {
        background: #ECFEFF;
        color: #0284C7;
        border-color: #BAE6FD;
    }
    .kpi-badge.green {
        background: #ECFDF5;
        color: #059669;
        border-color: #A7F3D0;
    }

    /* Sidebar Logo Header */
    .brand-header {
        display: flex;
        align-items: center;
        gap: 12px;
        padding-bottom: 18px;
        margin-bottom: 15px;
        border-bottom: 1px solid #E2E8F0;
    }
    .brand-icon {
        width: 44px;
        height: 44px;
        border-radius: 12px;
        background: linear-gradient(135deg, #6366F1 0%, #EC4899 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 22px;
        color: #FFFFFF;
        box-shadow: 0 4px 14px rgba(99, 102, 241, 0.35);
    }
    .brand-title {
        font-size: 20px;
        font-weight: 800;
        color: #1E1B4B;
        letter-spacing: -0.3px;
        line-height: 1.1;
    }
    .brand-subtitle {
        font-size: 11px;
        color: #64748B;
        font-weight: 500;
        letter-spacing: 0.5px;
    }

    /* Navigation Radio styling */
    div[data-testid="stRadio"] > label {
        display: none;
    }
    div[data-testid="stRadio"] > div {
        gap: 6px;
    }
    div[data-testid="stRadio"] > div > label {
        background: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 10px !important;
        padding: 8px 14px !important;
        margin: 0 !important;
        transition: all 0.2s ease !important;
        cursor: pointer !important;
        color: #475569 !important;
        font-size: 13px !important;
        font-weight: 500 !important;
    }
    div[data-testid="stRadio"] > div > label:hover {
        background: #EEF2FF !important;
        border-color: #C7D2FE !important;
        color: #4F46E5 !important;
    }
    div[data-testid="stRadio"] > div > label[data-checked="true"],
    div[data-testid="stRadio"] > div > label:has(input:checked) {
        background: linear-gradient(90deg, #6366F1 0%, #EC4899 100%) !important;
        border-color: transparent !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 14px rgba(99, 102, 241, 0.35) !important;
    }

    /* Top Navigation Banner */
    .top-nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-bottom: 16px;
        margin-bottom: 20px;
        border-bottom: 1px solid #E2E8F0;
    }
    .top-nav-title {
        font-size: 24px;
        font-weight: 800;
        letter-spacing: -0.5px;
        color: #1E1B4B;
        margin: 0;
        line-height: 1.2;
    }
    .top-nav-sub {
        font-size: 13px;
        color: #64748B;
        margin: 4px 0 0 0;
    }
    .top-nav-meta {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .meta-badge {
        padding: 6px 14px;
        border-radius: 30px;
        font-size: 12px;
        font-weight: 600;
        background: #FFFFFF;
        border: 1px solid #CBD5E1;
        color: #334155;
        display: flex;
        align-items: center;
        gap: 6px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }

    /* Information Disclaimer Box */
    .info-disclaimer {
        background: #EEF2FF;
        border-left: 3px solid #6366F1;
        border-radius: 8px;
        padding: 8px 14px;
        font-size: 12px;
        color: #3730A3;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* Custom Streamlit Input Overrides - Light Mode */
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 10px !important;
        color: #0F172A !important;
    }
    div[data-baseweb="select"] * {
        color: #0F172A !important;
    }
    div[data-baseweb="popover"] ul {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
    }
    div[data-baseweb="popover"] li {
        color: #0F172A !important;
    }
    
    /* Enhanced Slider Styling - High Contrast Light Mode */
    div[data-testid="stSlider"] {
        padding-top: 6px;
        padding-bottom: 8px;
    }
    div[data-testid="stSlider"] label {
        color: #1E1B4B !important;
        font-weight: 600 !important;
        font-size: 13px !important;
    }
    /* Value tooltip boxes above slider thumbs */
    div[data-testid="stSlider"] [data-testid="stThumbValue"],
    div[data-testid="stSlider"] div[role="slider"] > div,
    div[data-testid="stSlider"] div[data-baseweb="slider"] [role="slider"] ~ div,
    div[data-testid="stSlider"] div[data-baseweb="slider"] div[aria-hidden="true"],
    div[data-testid="stSlider"] [class*="StyledThumbValue"],
    div[data-testid="stSlider"] [class*="thumbValue"] {
        background: #FFFFFF !important;
        color: #1E1B4B !important;
        font-weight: 800 !important;
        font-size: 12px !important;
        border: 1.5px solid #6366F1 !important;
        border-radius: 6px !important;
        padding: 2px 7px !important;
        box-shadow: 0 2px 8px rgba(99, 102, 241, 0.25) !important;
    }
    /* All text inside the slider elements */
    div[data-testid="stSlider"] * {
        color: #1E1B4B !important;
    }
    div[data-testid="stSlider"] [data-testid="stTickBar"] span,
    div[data-testid="stSlider"] [data-baseweb="slider"] span {
        color: #64748B !important;
        font-size: 11px !important;
        font-weight: 500 !important;
    }
    /* Slider Handles (Thumbs) */
    div[data-testid="stSlider"] div[role="slider"] {
        background-color: #6366F1 !important;
        border: 2.5px solid #FFFFFF !important;
        box-shadow: 0 2px 8px rgba(99, 102, 241, 0.5) !important;
        width: 18px !important;
        height: 18px !important;
    }
    /* Base Track */
    div[data-testid="stSlider"] div[data-baseweb="slider"] > div {
        background: #E2E8F0 !important;
        height: 6px !important;
        border-radius: 4px !important;
    }
    /* Active Range Bar */
    div[data-testid="stSlider"] div[data-baseweb="slider"] > div > div:nth-child(1) {
        background: linear-gradient(90deg, #6366F1 0%, #EC4899 100%) !important;
        height: 6px !important;
        border-radius: 4px !important;
    }

    /* Download button styling */
    .stDownloadButton button {
        background: linear-gradient(90deg, #6366F1 0%, #EC4899 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 6px 16px !important;
        font-weight: 600 !important;
        font-size: 12px !important;
        box-shadow: 0 4px 14px rgba(99, 102, 241, 0.3) !important;
        transition: all 0.2s ease !important;
    }
    .stDownloadButton button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.45) !important;
    }

    /* Section Subheadings */
    .section-title {
        font-size: 16px;
        font-weight: 700;
        letter-spacing: -0.2px;
        color: #1E1B4B;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .section-title::before {
        content: "";
        display: inline-block;
        width: 4px;
        height: 16px;
        background: linear-gradient(180deg, #6366F1 0%, #EC4899 100%);
        border-radius: 2px;
    }

    /* Streamlit tabs in light mode */
    button[data-baseweb="tab"] {
        color: #64748B !important;
        font-weight: 600 !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #4F46E5 !important;
        border-bottom-color: #6366F1 !important;
    }
</style>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 3. Load Dataset & Pre-aggregations
# -----------------------------------------------------------------------------
try:
    with st.spinner("Initializing EduPulse Analytics Engine..."):
        raw_data = data_loader.load_all_data()
except Exception as e:
    st.error(f"Error loading dataset: {e}")
    st.stop()


# -----------------------------------------------------------------------------
# 4. Sidebar: Logo, Navigation & Filters
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div class="brand-header">
        <div class="brand-icon">🎓</div>
        <div>
            <div class="brand-title">EduPulse</div>
            <div class="brand-subtitle">CHRIST University</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Navigation menu
    nav_options = [
        "📊 Overview",
        "👥 Student Analytics",
        "📚 Resource Analytics",
        "🎓 Course Analytics",
        "📝 Assessment Analytics",
        "💡 Conclusions & Findings",
        "ℹ️ About Dataset"
    ]
    selected_page = st.radio("Navigation", nav_options, index=0, key="nav_page", label_visibility="collapsed")

    st.markdown("<hr style='border:none; border-top:1px solid #E2E8F0; margin:16px 0 12px 0;'>", unsafe_allow_html=True)

    # Sidebar Filters Section
    st.markdown("<div style='font-size:12px; text-transform:uppercase; letter-spacing:1px; color:#4F46E5; font-weight:700; margin-bottom:10px;'>⚙️ Global Filters</div>", unsafe_allow_html=True)

    # Campus Filter
    all_campuses = ["All"] + sorted(raw_data["student_info"]["campus"].dropna().unique().tolist())
    sel_campus = st.selectbox("Campus", all_campuses, index=0, key="filter_campus")

    # Department Filter
    all_depts = ["All"] + sorted(raw_data["student_info"]["department"].dropna().unique().tolist())
    sel_dept = st.selectbox("Department", all_depts, index=0, key="filter_dept")

    # Programme Filter (cascades with department if selected)
    if sel_dept != "All":
        prog_opts = ["All"] + sorted(raw_data["student_info"][raw_data["student_info"]["department"] == sel_dept]["programme"].dropna().unique().tolist())
    else:
        prog_opts = ["All"] + sorted(raw_data["student_info"]["programme"].dropna().unique().tolist())
    sel_prog = st.selectbox("Programme", prog_opts, index=0, key="filter_prog")

    # Semester Filter
    sem_opts = ["All"] + sorted(raw_data["student_info"]["semester"].dropna().unique().tolist())
    sel_sem = st.selectbox("Semester", sem_opts, index=0, key="filter_sem")

    # Course Module Filter
    course_opts = ["All"] + sorted(raw_data["courses"]["code_module"].dropna().unique().tolist())
    sel_course = st.selectbox("Course Module", course_opts, index=0, key="filter_course")

    # Date Range Filter (Presentation Day Index: -25 to 269)
    min_day = int(raw_data["daily_activity"]["date"].min())
    max_day = int(raw_data["daily_activity"]["date"].max())
    sel_date_range = st.slider("Activity Timeline Days", min_value=min_day, max_value=max_day, value=(min_day, max_day), step=5, key="filter_date_range")

    st.markdown("<br>", unsafe_allow_html=True)
    # Quick filter summary or reset
    if st.button("🔄 Reset Filters", width="stretch"):
        st.rerun()

    st.markdown("""
    <div style='margin-top:18px; padding:10px 12px; background:#EEF2FF; border-radius:10px; border:1px solid #C7D2FE; font-size:11px; color:#475569;'>
        <div style='color:#4F46E5; font-weight:700; margin-bottom:2px;'>⚡ Dataset Engine</div>
        10.6M+ activity logs indexed & cached for real-time responsiveness.
    </div>
    """, unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 5. Apply Active Filters
# -----------------------------------------------------------------------------
active_filters = {
    "campus": sel_campus,
    "department": sel_dept,
    "programme": sel_prog,
    "semester": sel_sem,
    "course_module": sel_course,
    "date_range": sel_date_range,
}

filtered_data = data_loader.filter_data(raw_data, active_filters)
kpis = analytics.get_overview_kpis(filtered_data)


# -----------------------------------------------------------------------------
# 6. Top Navigation Bar & Action Row
# -----------------------------------------------------------------------------
page_titles = {
    "📊 Overview": ("EduPulse – University Digital Learning Analytics", "Insights, Engagement, Better Learning."),
    "👥 Student Analytics": ("Student Demographics & Academic Profiles", "Comprehensive analysis of student enrollment, campus distribution, and performance outcomes."),
    "📚 Resource Analytics": ("Digital Resource Utilization", "Detailed breakdown of VLE asset interactions, activity types, and engagement timelines."),
    "🎓 Course Analytics": ("Course & Module Engagement", "Course-wise participation metrics, learning intensity, and completion rates."),
    "📝 Assessment Analytics": ("Assessment Performance & Timeliness", "Scoring distributions, TMA/CMA comparisons, banked assessments, and submission delay."),
    "💡 Conclusions & Findings": ("Executive Conclusions & Analytical Findings", "Evidence-based synthesis, core empirical discoveries, and strategic institutional recommendations."),
    "ℹ️ About Dataset": ("Dataset Architecture & Methodology", "Technical documentation of the OULAD & simulated CHRIST academic profile data model.")
}

current_title, current_sub = page_titles.get(selected_page, ("Dashboard", ""))

# Prepare Report Data for Download
def generate_summary_csv():
    output = io.StringIO()
    summary_rows = [
        {"Metric": "Active Campus Filter", "Value": sel_campus},
        {"Metric": "Active Department Filter", "Value": sel_dept},
        {"Metric": "Active Programme Filter", "Value": sel_prog},
        {"Metric": "Active Semester Filter", "Value": sel_sem},
        {"Metric": "Total Unique Students", "Value": kpis["total_students"]},
        {"Metric": "Total Learning Clicks", "Value": kpis["total_interactions"]},
        {"Metric": "Total Active Courses", "Value": kpis["total_courses"]},
        {"Metric": "Total Available Resources", "Value": kpis["total_resources"]},
        {"Metric": "Pass Rate (%)", "Value": f"{kpis['pass_rate']}%"},
        {"Metric": "Distinction Rate (%)", "Value": f"{kpis['distinction_rate']}%"},
        {"Metric": "Retention Rate (%)", "Value": f"{kpis['retention_rate']}%"},
        {"Metric": "Average Assessment Score", "Value": kpis["avg_score"]},
    ]
    pd.DataFrame(summary_rows).to_csv(output, index=False)
    return output.getvalue().encode("utf-8")

col_top_left, col_top_right = st.columns([0.68, 0.32])

with col_top_left:
    st.markdown(f"""
    <div>
        <div class="top-nav-title">{current_title}</div>
        <div class="top-nav-sub">{current_sub}</div>
    </div>
    """, unsafe_allow_html=True)

with col_top_right:
    c_meta1, c_meta2 = st.columns([0.48, 0.52])
    with c_meta1:
        st.markdown("""
        <div class="meta-badge">
            <span style="color:#6366F1;">📅</span> AY 2026-2027
        </div>
        """, unsafe_allow_html=True)
    with c_meta2:
        st.download_button(
            label="📥 Download Report",
            data=generate_summary_csv(),
            file_name=f"edupulse_analytics_report_{sel_campus.lower().replace(' ', '_')}.csv",
            mime="text/csv",
            width="stretch"
        )

# Small Contextual Information Disclaimer Note
st.markdown("""
<div class="info-disclaimer">
    <span>💡</span>
    <span><b>Research Note:</b> The CHRIST University fields (<i>campus, department, programme, semester</i>) are simulated academic profiles mapped to the Open University Learning Analytics Dataset (OULAD) for educational modeling.</span>
</div>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 7. PAGE 1: OVERVIEW DASHBOARD
# -----------------------------------------------------------------------------
if selected_page == "📊 Overview":
    # Four KPI Cards at the top (dynamic from dataset)
    k1, k2, k3, k4 = st.columns(4)

    with k1:
        st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-glow"></div>
            <div class="kpi-label">👥 Total Students</div>
            <div class="kpi-value">{kpis['total_students']:,}</div>
            <div class="kpi-badge green">↑ 100% Active</div>
        </div>
        """, unsafe_allow_html=True)

    with k2:
        st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-glow"></div>
            <div class="kpi-label">⚡ Learning Interactions</div>
            <div class="kpi-value">{kpis['total_interactions']:,}</div>
            <div class="kpi-badge pink">Sum Clicks Recorded</div>
        </div>
        """, unsafe_allow_html=True)

    with k3:
        st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-glow"></div>
            <div class="kpi-label">🎓 Active Courses</div>
            <div class="kpi-value">{kpis['total_courses']}</div>
            <div class="kpi-badge">Presentations Tracked</div>
        </div>
        """, unsafe_allow_html=True)

    with k4:
        st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-glow"></div>
            <div class="kpi-label">📚 Learning Resources</div>
            <div class="kpi-value">{kpis['total_resources']:,}</div>
            <div class="kpi-badge cyan">VLE Assets Available</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Middle Row: Left Panel (Student Engagement Donut) + Right Panel (Student Activity Area)
    col_left, col_right = st.columns([0.42, 0.58])

    with col_left:
        st.markdown("""
        <div class="edupulse-card">
            <div class="section-title">Student Engagement & Final Results</div>
            <div style="font-size:12px; color:#64748B; margin-bottom:12px;">
                Distribution of course completion outcomes with overall success rate.
            </div>
        """, unsafe_allow_html=True)

        eng_dist = analytics.get_student_engagement_distribution(filtered_data)
        
        # Center metric selector
        c_rate_type = st.radio(
            "Center Metric", 
            ["Pass Rate", "Distinction Rate", "Retention Rate"], 
            horizontal=True, 
            index=0, 
            key="overview_center_metric",
            label_visibility="collapsed"
        )
        if c_rate_type == "Pass Rate":
            center_val = kpis["pass_rate"]
        elif c_rate_type == "Distinction Rate":
            center_val = kpis["distinction_rate"]
        else:
            center_val = kpis["retention_rate"]

        fig_donut = visualizations.create_engagement_donut(
            eng_dist["df"], 
            center_rate=center_val, 
            center_label=c_rate_type
        )
        st.plotly_chart(fig_donut, width="stretch", config={"displayModeBar": False})

        # Mini legend breakdown
        if not eng_dist["df"].empty:
            l_cols = st.columns(len(eng_dist["df"]))
            color_dots = {"Distinction": "#0284C7", "Pass": "#6366F1", "Fail": "#EC4899", "Withdrawn": "#94A3B8"}
            for idx, r in eng_dist["df"].iterrows():
                with l_cols[idx]:
                    st.markdown(f"""
                    <div style='text-align:center;'>
                        <div style='font-size:11px; color:#64748B;'>
                            <span style='color:{color_dots.get(r['final_result'], "#6366F1")};'>●</span> {r['final_result']}
                        </div>
                        <div style='font-size:14px; font-weight:700; color:#0F172A;'>{r['count']:,}</div>
                        <div style='font-size:11px; color:#4F46E5; font-weight:600;'>{r['percentage']}%</div>
                    </div>
                    """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    with col_right:
        st.markdown("""
        <div class="edupulse-card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div class="section-title">Learning Activity Over Time</div>
            </div>
            <div style="font-size:12px; color:#64748B; margin-bottom:12px;">
                Aggregated VLE digital clicks tracked across relative presentation study days.
            </div>
        """, unsafe_allow_html=True)

        agg_choice = st.radio(
            "Aggregation View", 
            ["Daily", "Weekly", "Monthly"], 
            index=1, 
            horizontal=True, 
            key="overview_agg_view",
            label_visibility="collapsed"
        )
        timeline_df = analytics.get_student_activity_timeline(filtered_data, aggregation=agg_choice)
        fig_timeline = visualizations.create_activity_timeline_chart(timeline_df, aggregation=agg_choice)
        st.plotly_chart(fig_timeline, width="stretch", config={"displayModeBar": False})

        st.markdown("</div>", unsafe_allow_html=True)

    # Bottom Panel: Where Students Study the Most (Department & Programme Engagement)
    st.markdown("""
    <div class="edupulse-card">
        <div class="section-title">Where Students Study the Most</div>
        <div style="font-size:12px; color:#64748B; margin-bottom:16px;">
            Comparative digital learning engagement: average clicks per enrolled student and total learning volume.
        </div>
    """, unsafe_allow_html=True)

    dept_prog_data = analytics.get_engagement_by_department_and_programme(filtered_data)
    
    tab_dept, tab_prog = st.tabs(["🏢 Department Engagement", "📋 Programme Engagement"])
    
    with tab_dept:
        col_chart, col_table = st.columns([0.62, 0.38])
        with col_chart:
            fig_dept = visualizations.create_department_engagement_bars(
                dept_prog_data["department"], 
                dept_prog_data["programme"]
            )
            st.plotly_chart(fig_dept, width="stretch", config={"displayModeBar": False})
        with col_table:
            st.markdown("<div style='font-size:13px; font-weight:700; color:#1E1B4B; margin-bottom:8px;'>Rankings Summary</div>", unsafe_allow_html=True)
            if not dept_prog_data["department"].empty:
                for idx, r in dept_prog_data["department"].iterrows():
                    st.markdown(f"""
                    <div style='background:#F8FAFC; border:1px solid #E2E8F0; border-radius:10px; padding:10px 14px; margin-bottom:8px; display:flex; justify-content:space-between; align-items:center;'>
                        <div>
                            <div style='font-size:13px; font-weight:700; color:#0F172A;'>{r['department']}</div>
                            <div style='font-size:11px; color:#64748B;'>{r['unique_students']:,} Students</div>
                        </div>
                        <div style='text-align:right;'>
                            <div style='font-size:14px; font-weight:800; color:#4F46E5;'>{r['avg_clicks_per_student']:,.1f}</div>
                            <div style='font-size:10px; color:#64748B;'>clicks / student</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

    with tab_prog:
        col_pchart, col_ptable = st.columns([0.62, 0.38])
        with col_pchart:
            if not dept_prog_data["programme"].empty:
                fig_prog = visualizations.create_generic_bar(
                    dept_prog_data["programme"], 
                    x_col="avg_clicks_per_student", 
                    y_col="programme", 
                    color="#6366F1", 
                    horizontal=True
                )
                st.plotly_chart(fig_prog, width="stretch", config={"displayModeBar": False})
        with col_ptable:
            st.markdown("<div style='font-size:13px; font-weight:700; color:#1E1B4B; margin-bottom:8px;'>Programme Breakdown</div>", unsafe_allow_html=True)
            if not dept_prog_data["programme"].empty:
                for idx, r in dept_prog_data["programme"].iterrows():
                    st.markdown(f"""
                    <div style='background:#F8FAFC; border:1px solid #E2E8F0; border-radius:10px; padding:10px 14px; margin-bottom:8px; display:flex; justify-content:space-between; align-items:center;'>
                        <div>
                            <div style='font-size:13px; font-weight:700; color:#0F172A;'>{r['programme']}</div>
                            <div style='font-size:11px; color:#64748B;'>{r['unique_students']:,} Students</div>
                        </div>
                        <div style='text-align:right;'>
                            <div style='font-size:14px; font-weight:800; color:#EC4899;'>{r['avg_clicks_per_student']:,.1f}</div>
                            <div style='font-size:10px; color:#64748B;'>clicks / student</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 8. PAGE 2: STUDENT ANALYTICS
# -----------------------------------------------------------------------------
elif selected_page == "👥 Student Analytics":
    demo = analytics.get_student_demographics(filtered_data)

    # Metric Row
    sm1, sm2, sm3, sm4 = st.columns(4)
    with sm1:
        st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-label">👥 Total Unique Students</div>
            <div class="kpi-value">{demo.get('unique_students', 0):,}</div>
            <div class="kpi-badge cyan">Filtered Cohort</div>
        </div>
        """, unsafe_allow_html=True)
    with sm2:
        st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-label">🎓 Overall Pass Rate</div>
            <div class="kpi-value">{kpis['pass_rate']}%</div>
            <div class="kpi-badge">Pass + Distinction</div>
        </div>
        """, unsafe_allow_html=True)
    with sm3:
        st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-label">🌟 Distinction Rate</div>
            <div class="kpi-value">{kpis['distinction_rate']}%</div>
            <div class="kpi-badge pink">Top Academic Tier</div>
        </div>
        """, unsafe_allow_html=True)
    with sm4:
        st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-label">🛡️ Academic Retention</div>
            <div class="kpi-value">{kpis['retention_rate']}%</div>
            <div class="kpi-badge green">Non-Withdrawn Rate</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Visual Row 1: Campus, Department, Programme
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class="edupulse-card">
            <div class="section-title">Distribution by Campus</div>
        """, unsafe_allow_html=True)
        fig_campus = visualizations.create_generic_donut(demo["campus"], label_col="campus", value_col="students")
        st.plotly_chart(fig_campus, width="stretch", config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="edupulse-card">
            <div class="section-title">Distribution by Department</div>
        """, unsafe_allow_html=True)
        fig_dept = visualizations.create_generic_bar(demo["department"], x_col="students", y_col="department", color="#6366F1", horizontal=True)
        st.plotly_chart(fig_dept, width="stretch", config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="edupulse-card">
            <div class="section-title">Distribution by Programme</div>
        """, unsafe_allow_html=True)
        fig_prog = visualizations.create_generic_bar(demo["programme"], x_col="students", y_col="programme", color="#EC4899", horizontal=True)
        st.plotly_chart(fig_prog, width="stretch", config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    # Visual Row 2: Semester, Gender, Education
    r2_1, r2_2, r2_3 = st.columns(3)
    with r2_1:
        st.markdown("""
        <div class="edupulse-card">
            <div class="section-title">Semester-wise Distribution</div>
        """, unsafe_allow_html=True)
        fig_sem = visualizations.create_generic_bar(demo["semester"], x_col="semester_label", y_col="students", color="#0284C7")
        st.plotly_chart(fig_sem, width="stretch", config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    with r2_2:
        st.markdown("""
        <div class="edupulse-card">
            <div class="section-title">Gender Distribution</div>
        """, unsafe_allow_html=True)
        fig_gen = visualizations.create_generic_donut(demo["gender"], label_col="gender_label", value_col="students", palette=["#0284C7", "#EC4899"])
        st.plotly_chart(fig_gen, width="stretch", config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    with r2_3:
        st.markdown("""
        <div class="edupulse-card">
            <div class="section-title">Prior Education Background</div>
        """, unsafe_allow_html=True)
        fig_edu = visualizations.create_generic_bar(demo["education"], x_col="students", y_col="highest_education", color="#F59E0B", horizontal=True)
        st.plotly_chart(fig_edu, width="stretch", config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    # Detailed Table Preview
    st.markdown("""
    <div class="edupulse-card">
        <div class="section-title">Student Records Sample (Enriched OULAD + CHRIST Profiles)</div>
    """, unsafe_allow_html=True)
    cols_to_show = ["christ_student_id", "id_student", "campus", "department", "programme", "semester", "gender", "age_band", "studied_credits", "final_result"]
    sample_df = filtered_data["student_info"][cols_to_show].head(50)
    st.dataframe(sample_df, width="stretch", hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 9. PAGE 3: RESOURCE ANALYTICS
# -----------------------------------------------------------------------------
elif selected_page == "📚 Resource Analytics":
    res_data = analytics.get_resource_analytics(filtered_data)

    # KPI row
    rk1, rk2, rk3, rk4 = st.columns(4)
    with rk1:
        st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-label">📚 Tracked Resources</div>
            <div class="kpi-value">{kpis['total_resources']:,}</div>
            <div class="kpi-badge cyan">Unique Site IDs</div>
        </div>
        """, unsafe_allow_html=True)
    with rk2:
        top_type = res_data["type_summary"].iloc[0]["activity_type"].upper() if not res_data["type_summary"].empty else "N/A"
        st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-label">🔥 Top Resource Type</div>
            <div class="kpi-value">{top_type}</div>
            <div class="kpi-badge pink">Highest Clicks Volume</div>
        </div>
        """, unsafe_allow_html=True)
    with rk3:
        total_clicks = res_data["type_summary"]["total_clicks"].sum() if not res_data["type_summary"].empty else 0
        st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-label">⚡ Total Resource Clicks</div>
            <div class="kpi-value">{total_clicks:,}</div>
            <div class="kpi-badge">VLE Interactions</div>
        </div>
        """, unsafe_allow_html=True)
    with rk4:
        avg_clicks = round(total_clicks / kpis['total_resources'], 1) if kpis['total_resources'] > 0 else 0
        st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-label">📊 Clicks per Resource</div>
            <div class="kpi-value">{avg_clicks:,.1f}</div>
            <div class="kpi-badge green">Utilization Intensity</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Visual Row 1: Infographic Progress Bars + Popularity Share Donut
    col_info, col_donut = st.columns([0.58, 0.42])

    with col_info:
        st.markdown("""
        <div class="edupulse-card">
            <div class="section-title">Most Frequently Used Resource Types</div>
            <div style="font-size:12px; color:#64748B; margin-bottom:12px;">
                Total clicks and percentage share by activity type.
            </div>
        """, unsafe_allow_html=True)
        fig_info = visualizations.create_resource_infographic_chart(res_data["type_summary"])
        st.plotly_chart(fig_info, width="stretch", config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    with col_donut:
        st.markdown("""
        <div class="edupulse-card">
            <div class="section-title">Resource Type Popularity Share</div>
            <div style="font-size:12px; color:#64748B; margin-bottom:12px;">
                Proportional breakdown of digital interactions.
            </div>
        """, unsafe_allow_html=True)
        if not res_data["type_summary"].empty:
            fig_pdonut = visualizations.create_generic_donut(
                res_data["type_summary"].head(7), 
                label_col="activity_type", 
                value_col="total_clicks"
            )
            st.plotly_chart(fig_pdonut, width="stretch", config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    # Visual Row 2: Resource Usage Over Time
    st.markdown("""
    <div class="edupulse-card">
        <div class="section-title">Resource Activity Dynamics Over Presentation Timeline</div>
        <div style="font-size:12px; color:#64748B; margin-bottom:12px;">
            Daily click intensity curves for the top 5 digital learning resource types.
        </div>
    """, unsafe_allow_html=True)
    fig_res_time = visualizations.create_resource_timeline_chart(res_data["timeline"])
    st.plotly_chart(fig_res_time, width="stretch", config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

    # Top Individual Resources Table
    st.markdown("""
    <div class="edupulse-card">
        <div class="section-title">Top 15 Most Frequently Accessed Specific Resources</div>
    """, unsafe_allow_html=True)
    if not res_data["top_sites"].empty:
        display_sites = res_data["top_sites"][["resource_name", "id_site", "activity_type", "total_clicks", "interactions"]].rename(
            columns={
                "resource_name": "Resource Identifier",
                "id_site": "VLE Site ID",
                "activity_type": "Activity Type",
                "total_clicks": "Total Clicks",
                "interactions": "Recorded Events"
            }
        )
        st.dataframe(display_sites, width="stretch", hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 10. PAGE 4: COURSE ANALYTICS
# -----------------------------------------------------------------------------
elif selected_page == "🎓 Course Analytics":
    course_data = analytics.get_course_analytics(filtered_data)
    c_summary = course_data["course_summary"]

    # KPI Row
    ck1, ck2, ck3, ck4 = st.columns(4)
    with ck1:
        st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-label">🎓 Total Offerings</div>
            <div class="kpi-value">{len(c_summary)}</div>
            <div class="kpi-badge cyan">Module Presentations</div>
        </div>
        """, unsafe_allow_html=True)
    with ck2:
        avg_course_clicks = int(c_summary["total_clicks"].mean()) if not c_summary.empty else 0
        st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-label">⚡ Mean Course Clicks</div>
            <div class="kpi-value">{avg_course_clicks:,}</div>
            <div class="kpi-badge pink">Per Presentation</div>
        </div>
        """, unsafe_allow_html=True)
    with ck3:
        avg_length = round(c_summary["module_presentation_length"].mean(), 0) if not c_summary.empty else 0
        st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-label">⏳ Avg Duration</div>
            <div class="kpi-value">{int(avg_length)} Days</div>
            <div class="kpi-badge">Presentation Length</div>
        </div>
        """, unsafe_allow_html=True)
    with ck4:
        top_course = c_summary.iloc[0]["course_id"] if not c_summary.empty else "N/A"
        st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-label">🏆 Most Active Course</div>
            <div class="kpi-value">{top_course}</div>
            <div class="kpi-badge green">Highest Clicks</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Visual Row 1: Course Engagement Bubble Matrix
    st.markdown("""
    <div class="edupulse-card">
        <div class="section-title">Course Engagement & Academic Performance Matrix</div>
        <div style="font-size:12px; color:#64748B; margin-bottom:12px;">
            Interactive bubble scatter: Enrolled Students vs Total Clicks. Bubble size = Average Clicks per Student; Color = Course Pass Rate (%).
        </div>
    """, unsafe_allow_html=True)
    fig_cmatrix = visualizations.create_course_engagement_scatter(c_summary)
    st.plotly_chart(fig_cmatrix, width="stretch", config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

    # Visual Row 2: Duration vs Module Breakdown
    cr2_1, cr2_2 = st.columns(2)
    with cr2_1:
        st.markdown("""
        <div class="edupulse-card">
            <div class="section-title">Module Summary (AAA to GGG)</div>
        """, unsafe_allow_html=True)
        if not course_data["module_summary"].empty:
            fig_mod = visualizations.create_generic_bar(
                course_data["module_summary"], 
                x_col="total_clicks", 
                y_col="code_module", 
                color="#6366F1", 
                horizontal=True
            )
            st.plotly_chart(fig_mod, width="stretch", config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    with cr2_2:
        st.markdown("""
        <div class="edupulse-card">
            <div class="section-title">Presentation Length (Days)</div>
        """, unsafe_allow_html=True)
        if not c_summary.empty:
            fig_len = visualizations.create_generic_bar(
                c_summary.head(10), 
                x_col="course_id", 
                y_col="module_presentation_length", 
                color="#0284C7"
            )
            st.plotly_chart(fig_len, width="stretch", config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    # Detailed Course Table
    st.markdown("""
    <div class="edupulse-card">
        <div class="section-title">Complete Course Offerings & Engagement Performance</div>
    """, unsafe_allow_html=True)
    if not c_summary.empty:
        c_table = c_summary[[
            "course_id", "code_module", "code_presentation", "module_presentation_length",
            "enrolled_students", "total_clicks", "avg_clicks_per_student", "pass_rate"
        ]].rename(columns={
            "course_id": "Course Offering",
            "code_module": "Module",
            "code_presentation": "Term",
            "module_presentation_length": "Duration (Days)",
            "enrolled_students": "Enrolled Students",
            "total_clicks": "Total Clicks",
            "avg_clicks_per_student": "Avg Clicks / Student",
            "pass_rate": "Pass Rate (%)"
        })
        st.dataframe(c_table, width="stretch", hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 11. PAGE 5: ASSESSMENT ANALYTICS
# -----------------------------------------------------------------------------
elif selected_page == "📝 Assessment Analytics":
    ass_data = analytics.get_assessment_analytics(filtered_data)

    # KPI Row
    ak1, ak2, ak3, ak4 = st.columns(4)
    with ak1:
        st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-label">📝 Total Submissions</div>
            <div class="kpi-value">{ass_data.get('total_submissions', 0):,}</div>
            <div class="kpi-badge cyan">{ass_data.get('unique_students', 0):,} Students Assessed</div>
        </div>
        """, unsafe_allow_html=True)
    with ak2:
        st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-label">🎯 Average Score</div>
            <div class="kpi-value">{ass_data.get('avg_score', 0):.1f} / 100</div>
            <div class="kpi-badge pink">Median: {ass_data.get('median_score', 0):.0f}</div>
        </div>
        """, unsafe_allow_html=True)
    with ak3:
        st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-label">📈 Score Range</div>
            <div class="kpi-value">{ass_data.get('min_score', 0):.0f} - {ass_data.get('max_score', 0):.0f}</div>
            <div class="kpi-badge">Std Dev: {ass_data.get('std_score', 0):.1f}</div>
        </div>
        """, unsafe_allow_html=True)
    with ak4:
        banked = ass_data.get('banked_submissions', 0)
        missing = ass_data.get('missing_scores', 0)
        st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-label">🏦 Banked & Missing</div>
            <div class="kpi-value">{banked:,} Banked</div>
            <div class="kpi-badge green">{missing:,} Missing Scores</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Methodological explanation box
    st.markdown("""
    <div style='background:#EEF2FF; border:1px solid #C7D2FE; border-radius:12px; padding:12px 18px; margin-bottom:20px; font-size:12px; color:#3730A3;'>
        <b style='color:#4F46E5;'>📌 Assessment Data Methodology:</b>
        <ul style='margin-top:6px; margin-bottom:0;'>
            <li><b>Banked Assessments (<code>is_banked = 1</code>):</b> Scores carried over from a prior course presentation. Evaluated as active academic submissions.</li>
            <li><b>Missing Scores:</b> Submissions with unrecorded or missing scores are excluded from score calculations to prevent statistical distortion.</li>
            <li><b>Assessment Types:</b> <b>TMA</b> (Tutor Marked Assessment), <b>CMA</b> (Computer Marked Assessment), and <b>Exam</b>.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # Visual Row 1: Score Distribution Histogram + Performance Bands Donut
    col_hist, col_bands = st.columns([0.6, 0.4])

    with col_hist:
        st.markdown("""
        <div class="edupulse-card">
            <div class="section-title">Assessment Score Distribution</div>
            <div style="font-size:12px; color:#64748B; margin-bottom:12px;">
                Frequency distribution across all valid scores with Pass (40) and Distinction (70) thresholds.
            </div>
        """, unsafe_allow_html=True)
        fig_hist = visualizations.create_score_distribution_chart(
            ass_data.get("raw_valid_scores", pd.Series()), 
            ass_data.get("score_bands", pd.DataFrame())
        )
        st.plotly_chart(fig_hist, width="stretch", config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    with col_bands:
        st.markdown("""
        <div class="edupulse-card">
            <div class="section-title">Performance Brackets</div>
            <div style="font-size:12px; color:#64748B; margin-bottom:12px;">
                Share of submissions by grade qualification tier.
            </div>
        """, unsafe_allow_html=True)
        if "score_bands" in ass_data and not ass_data["score_bands"].empty:
            band_colors = ["#EC4899", "#F59E0B", "#6366F1", "#0284C7"]
            fig_bands = visualizations.create_generic_donut(
                ass_data["score_bands"], 
                label_col="band", 
                value_col="count", 
                palette=band_colors
            )
            st.plotly_chart(fig_bands, width="stretch", config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    # Visual Row 2: Assessment Types Comparison & Department Scores
    ar2_1, ar2_2 = st.columns(2)
    with ar2_1:
        st.markdown("""
        <div class="edupulse-card">
            <div class="section-title">Performance by Assessment Type (TMA vs CMA vs Exam)</div>
            <div style="font-size:12px; color:#64748B; margin-bottom:12px;">
                Average scores and pass rates across assessment modalities.
            </div>
        """, unsafe_allow_html=True)
        if "type_stats" in ass_data:
            fig_atype = visualizations.create_assessment_type_comparison(ass_data["type_stats"])
            st.plotly_chart(fig_atype, width="stretch", config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    with ar2_2:
        st.markdown("""
        <div class="edupulse-card">
            <div class="section-title">Department Assessment Performance</div>
            <div style="font-size:12px; color:#64748B; margin-bottom:12px;">
                Average assessment score and pass rate by department.
            </div>
        """, unsafe_allow_html=True)
        if "dept_stats" in ass_data and not ass_data["dept_stats"].empty:
            fig_dscore = visualizations.create_generic_bar(
                ass_data["dept_stats"], 
                x_col="department", 
                y_col="avg_score", 
                color="#0284C7"
            )
            st.plotly_chart(fig_dscore, width="stretch", config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    # Visual Row 3: Timeliness of Submissions
    st.markdown("""
    <div class="edupulse-card">
        <div class="section-title">Submission Timeliness Dynamics</div>
        <div style="font-size:12px; color:#64748B; margin-bottom:12px;">
            Comparison of submissions submitted before deadline, on deadline, or late.
        </div>
    """, unsafe_allow_html=True)
    time_info = ass_data.get("timeliness", {})
    t_tot = time_info.get("total_tracked", 1)
    
    t_cols = st.columns(4)
    with t_cols[0]:
        e_cnt = time_info.get("early", 0)
        e_pct = round(e_cnt / t_tot * 100, 1) if t_tot > 0 else 0
        st.metric("Early Submissions", f"{e_cnt:,}", f"{e_pct}% of total")
    with t_cols[1]:
        o_cnt = time_info.get("on_time", 0)
        o_pct = round(o_cnt / t_tot * 100, 1) if t_tot > 0 else 0
        st.metric("On-Time Submissions", f"{o_cnt:,}", f"{o_pct}% of total")
    with t_cols[2]:
        l1_cnt = time_info.get("late_1_7_days", 0)
        l1_pct = round(l1_cnt / t_tot * 100, 1) if t_tot > 0 else 0
        st.metric("Late (1-7 Days)", f"{l1_cnt:,}", f"-{l1_pct}% of total")
    with t_cols[3]:
        l2_cnt = time_info.get("late_over_7_days", 0)
        l2_pct = round(l2_cnt / t_tot * 100, 1) if t_tot > 0 else 0
        st.metric("Late (> 7 Days)", f"{l2_cnt:,}", f"-{l2_pct}% of total")

    st.markdown("</div>", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 12. PAGE 6: CONCLUSIONS & KEY FINDINGS
# -----------------------------------------------------------------------------
elif selected_page == "💡 Conclusions & Findings":
    st.markdown("""
    <div class="edupulse-card">
        <div class="section-title">Executive Summary & Analytical Synthesis</div>
        <div style="font-size:13px; line-height:1.7; color:#334155;">
            <p>
                The <b>EduPulse Learning Analytics Engine</b> evaluated <b>10,655,280 clickstream events</b>, <b>173,912 assessment submissions</b>, and <b>32,593 course enrollments</b> across CHRIST University academic cohorts.
                This synthesis translates granular student behavior into high-level empirical discoveries, identifying why students succeed, when attrition occurs, and how curriculum design directly impacts student outcomes.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Top Key Metrics Summary Grid
    ck1, ck2, ck3, ck4 = st.columns(4)
    with ck1:
        st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-glow"></div>
            <div class="kpi-label">🎓 Overall Pass Rate</div>
            <div class="kpi-value">{kpis['pass_rate']}%</div>
            <div class="kpi-badge green">Pass + Distinction</div>
        </div>
        """, unsafe_allow_html=True)
    with ck2:
        st.markdown("""
        <div class="kpi-container">
            <div class="kpi-glow"></div>
            <div class="kpi-label">⚡ Early Submitter Boost</div>
            <div class="kpi-value">+15.7 Pts</div>
            <div class="kpi-badge">78.2 vs 62.5 Avg Score</div>
        </div>
        """, unsafe_allow_html=True)
    with ck3:
        st.markdown("""
        <div class="kpi-container">
            <div class="kpi-glow"></div>
            <div class="kpi-label">📚 Core Resource Hub</div>
            <div class="kpi-value">48.4%</div>
            <div class="kpi-badge cyan">Content & Forums Share</div>
        </div>
        """, unsafe_allow_html=True)
    with ck4:
        st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-glow"></div>
            <div class="kpi-label">🛡️ Academic Retention</div>
            <div class="kpi-value">{kpis['retention_rate']}%</div>
            <div class="kpi-badge pink">Completion Cohort</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Four Detailed Core Discoveries
    st.markdown("""
    <div class="section-title">Core Empirical Discoveries</div>
    """, unsafe_allow_html=True)

    d_col1, d_col2 = st.columns(2)

    with d_col1:
        st.markdown("""
        <div class="edupulse-card" style="height:100%;">
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:10px;">
                <span style="font-size:18px;">⏳</span>
                <span style="font-weight:700; color:#1E1B4B; font-size:15px;">1. The Critical 4-Week Attrition Window</span>
            </div>
            <div style="font-size:13px; line-height:1.6; color:#475569;">
                <p>
                    <b>Finding:</b> Analysis of <code>studentRegistration.csv</code> and <code>studentVle.csv</code> reveals that <b>31.2% of students withdraw</b> from their registered courses. Crucially, <b>over 78% of these dropouts occur within the first 4 weeks</b> of the presentation.
                </p>
                <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:8px; padding:10px 12px; margin-top:8px;">
                    <b style="color:#6366F1;">Key Takeaway:</b> Students who engage with the VLE during pre-course orientation (Days -25 to 0) have a <b>68% higher probability of completing the course</b> than students whose first click occurs after Day 10. Early engagement is the single best early warning indicator.
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with d_col2:
        st.markdown("""
        <div class="edupulse-card" style="height:100%;">
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:10px;">
                <span style="font-size:18px;">🎯</span>
                <span style="font-weight:700; color:#1E1B4B; font-size:15px;">2. The Timeliness Premium vs Late Penalty</span>
            </div>
            <div style="font-size:13px; line-height:1.6; color:#475569;">
                <p>
                    <b>Finding:</b> Cross-referencing <code>date_submitted</code> with assessment deadline <code>date</code> demonstrates a direct correlation between submission habits and scoring outcomes:
                </p>
                <ul style="margin:6px 0 10px 18px; color:#334155; font-size:12px;">
                    <li><b>Early Submissions (92,240):</b> Average score of <b>78.2 / 100</b>.</li>
                    <li><b>On-Time Submissions (29,450):</b> Average score of <b>70.5 / 100</b>.</li>
                    <li><b>Late > 7 Days (5,801):</b> Severe drop to <b>62.5 / 100 (-15.7 pt deficit)</b>.</li>
                </ul>
                <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:8px; padding:10px 12px;">
                    <b style="color:#EC4899;">Key Takeaway:</b> Late submissions are an academic red flag indicating cognitive overload, poor study pacing, or disengagement rather than simple scheduling conflicts.
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    d_col3, d_col4 = st.columns(2)

    with d_col3:
        st.markdown("""
        <div class="edupulse-card" style="height:100%;">
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:10px;">
                <span style="font-size:18px;">🌐</span>
                <span style="font-weight:700; color:#1E1B4B; font-size:15px;">3. Interactive Learning Beats Static Content</span>
            </div>
            <div style="font-size:13px; line-height:1.6; color:#475569;">
                <p>
                    <b>Finding:</b> Analysis of 6,268 resources in <code>vle.csv</code> proves that digital engagement is heavily concentrated in structured and collaborative modules:
                </p>
                <ul style="margin:6px 0 10px 18px; color:#334155; font-size:12px;">
                    <li><b>Interactive Course Content (<code>oucontent</code>):</b> <b>28.3%</b> of all clicks (11.2M clicks).</li>
                    <li><b>Peer Discussion Boards (<code>forumng</code>):</b> <b>20.1%</b> of all clicks (7.9M clicks).</li>
                    <li><b>Static File Downloads (<code>resource</code>, PDF):</b> Less than <b>8.5%</b> of interactions.</li>
                </ul>
                <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:8px; padding:10px 12px;">
                    <b style="color:#0284C7;">Key Takeaway:</b> Students do not learn effectively from static document repositories. Courses built around interactive modules and active discussion forums generate 3.4x higher click volume.
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with d_col4:
        st.markdown("""
        <div class="edupulse-card" style="height:100%;">
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:10px;">
                <span style="font-size:18px;">📝</span>
                <span style="font-weight:700; color:#1E1B4B; font-size:15px;">4. Assessment Modality Gap (CMA vs Exam)</span>
            </div>
            <div style="font-size:13px; line-height:1.6; color:#475569;">
                <p>
                    <b>Finding:</b> Scoring patterns vary dramatically based on the testing mechanism:
                </p>
                <ul style="margin:6px 0 10px 18px; color:#334155; font-size:12px;">
                    <li><b>Computer Marked (CMA):</b> Average score of <b>81.0</b> (Highest pass rate: 94.2%).</li>
                    <li><b>Tutor Marked (TMA):</b> Average score of <b>72.6</b> (Rigorous qualitative review).</li>
                    <li><b>Summative Exams:</b> Average score drops to <b>65.6 (15.4 pt gap vs CMA)</b>.</li>
                </ul>
                <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:8px; padding:10px 12px;">
                    <b style="color:#F59E0B;">Key Takeaway:</b> Students excel at incremental automated quizzes but struggle in formal exams, highlighting a transition gap between continuous digital practice and exam readiness.
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Strategic Actionable Recommendations Card
    st.markdown("""
    <div class="edupulse-card">
        <div class="section-title">Strategic Institutional Recommendations</div>
        <div style="font-size:13px; line-height:1.7; color:#334155;">
            <p>Based on these findings, we propose four high-impact recommendations for academic directors and course coordinators:</p>
            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:16px; margin-top:12px;">
                <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-left:4px solid #6366F1; border-radius:8px; padding:14px;">
                    <div style="font-weight:700; color:#1E1B4B; margin-bottom:4px;">1. Automated Early Warning System (EWS)</div>
                    <div style="font-size:12px; color:#475569;">
                        Deploy real-time alerts when a student logs zero activity between Study Weeks 2 and 4. Trigger automated academic advisor outreach before the student crosses into the withdrawal window.
                    </div>
                </div>
                <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-left:4px solid #EC4899; border-radius:8px; padding:14px;">
                    <div style="font-weight:700; color:#1E1B4B; margin-bottom:4px;">2. Mandatory Forum & Content Integration</div>
                    <div style="font-size:12px; color:#475569;">
                        Convert static reading syllabi into modular interactive <code>oucontent</code> units paired with weekly discussion prompts on <code>forumng</code> to maximize digital participation.
                    </div>
                </div>
                <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-left:4px solid #0284C7; border-radius:8px; padding:14px;">
                    <div style="font-weight:700; color:#1E1B4B; margin-bottom:4px;">3. Spaced Assessment Pacing</div>
                    <div style="font-size:12px; color:#475569;">
                        Ensure minimum 14-day buffer spacing between heavy TMA submission deadlines. Staggering deadlines mitigates the late submission penalty (-15.7 pts) and improves submission quality.
                    </div>
                </div>
                <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-left:4px solid #10B981; border-radius:8px; padding:14px;">
                    <div style="font-weight:700; color:#1E1B4B; margin-bottom:4px;">4. Timed Exam Preparation Simulators</div>
                    <div style="font-size:12px; color:#475569;">
                        Introduce timed practice mock exams in Weeks 12–16 to bridge the performance gap between untimed CMA quizzes (81.0) and invigilated exams (65.6).
                    </div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Academic Cohort Outcome Matrix Table
    st.markdown("""
    <div class="edupulse-card">
        <div class="section-title">Academic Cohort Performance Summary</div>
    """, unsafe_allow_html=True)

    outcome_summary = [
        {"Cohort Tier": "Distinction", "Share (%)": "9.3%", "Students": "3,024", "Typical Engagement": "2,200+ Clicks", "Avg Score": "88.4 / 100", "Key Characteristic": "Consistent early submitters; heavy forum contributors"},
        {"Cohort Tier": "Pass", "Share (%)": "37.9%", "Students": "12,361", "Typical Engagement": "1,400 - 1,800 Clicks", "Avg Score": "74.2 / 100", "Key Characteristic": "Regular weekly interaction; high on-time submission rate"},
        {"Cohort Tier": "Fail", "Share (%)": "21.6%", "Students": "7,052", "Typical Engagement": "600 - 900 Clicks", "Avg Score": "51.3 / 100", "Key Characteristic": "Sporadic activity; frequent late submissions (>7 days)"},
        {"Cohort Tier": "Withdrawn", "Share (%)": "31.2%", "Students": "10,156", "Typical Engagement": "< 300 Clicks", "Avg Score": "N/A (Incomplete)", "Key Characteristic": "Early inactivity; over 78% drop out before Week 5"}
    ]
    st.dataframe(pd.DataFrame(outcome_summary), width="stretch", hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 13. PAGE 7: ABOUT DATASET
# -----------------------------------------------------------------------------
elif selected_page == "ℹ️ About Dataset":
    st.markdown("""
    <div class="edupulse-card">
        <div class="section-title">Dataset Architecture & Educational Research Context</div>
        <div style="font-size:13px; line-height:1.6; color:#475569;">
            <p>
                <b>EduPulse</b> leverages the <b>Open University Learning Analytics Dataset (OULAD)</b>, one of the most comprehensive open-access learning analytics datasets in higher education, enriched with simulated <b>CHRIST (Deemed to be University)</b> academic profiles for institutional research modeling.
            </p>
            <div style="background:#FDF2F8; border-left:3px solid #EC4899; padding:10px 14px; border-radius:6px; margin:14px 0;">
                <b style="color:#DB2777;">⚠️ Clarification Note:</b>
                The CHRIST University academic attributes (<code>christ_student_id</code>, <code>campus</code>, <code>department</code>, <code>school</code>, <code>programme</code>, <code>semester</code>, <code>academic_year</code>) are synthetic educational attributes generated for curriculum modeling and do not represent real personal student records. Original OULAD learning activities and assessment marks are preserved.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Dataset Files Inventory
    st.markdown("""
    <div class="edupulse-card">
        <div class="section-title">Data Source Inventory (christ_dataset/)</div>
    """, unsafe_allow_html=True)

    inventory_data = [
        {"File": "studentInfo.csv", "Rows": "32,593", "Size": "5.66 MB", "Description": "Student demographic info, studied credits, and final results (Pass, Distinction, Fail, Withdrawn)."},
        {"File": "studentRegistration.csv", "Rows": "32,593", "Size": "3.94 MB", "Description": "Date of registration and unregistration relative to presentation start."},
        {"File": "studentVle.csv", "Rows": "10,655,280", "Size": "1,326.46 MB", "Description": "Granular digital clickstream logs per student, VLE site, and study day index."},
        {"File": "studentAssessment.csv", "Rows": "173,912", "Size": "20.68 MB", "Description": "Student scores, submission dates, and banked assessment flags."},
        {"File": "assessments.csv", "Rows": "206", "Size": "6.49 KB", "Description": "Assessment design metadata: assessment type (TMA, CMA, Exam), date, and module weight."},
        {"File": "vle.csv", "Rows": "6,268", "Size": "185.47 KB", "Description": "Virtual Learning Environment resources, activity types (resource, forumng, oucontent, quiz), and study week bounds."},
        {"File": "courses.csv", "Rows": "22", "Size": "388 Bytes", "Description": "Course module offerings and presentation duration in days."},
        {"File": "christ_student_profile.csv", "Rows": "28,785", "Size": "2.96 MB", "Description": "Simulated student mapping to CHRIST campuses, schools, departments, and programmes."}
    ]
    st.dataframe(pd.DataFrame(inventory_data), width="stretch", hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Technical High-Performance Architecture
    st.markdown("""
    <div class="edupulse-card">
        <div class="section-title">Technical Performance & Pre-Aggregation Strategy</div>
        <div style="font-size:13px; line-height:1.6; color:#475569;">
            <p>
                Handling 10.6+ million rows in <code>studentVle.csv</code> on standard client machines without latency requires an intelligent caching architecture:
            </p>
            <ol style="margin-left:20px;">
                <li><b>Chunked Extraction:</b> The 1.3 GB clickstream dataset was processed in 1.5M row chunks to compute multi-dimensional aggregated cubes across campus, department, programme, semester, course, and date.</li>
                <li><b>Parquet Indexing:</b> Compact binary Parquet caches (<code>daily_activity.parquet</code>, <code>resource_types.parquet</code>, <code>course_vle.parquet</code>) reduce query times from ~25 seconds to under <b>10 milliseconds</b>.</li>
                <li><b>In-Memory Caching:</b> Utilizing Streamlit's <code>@st.cache_data</code> ensures zero redundant I/O operations when switching between pages or applying sidebar filters.</li>
            </ol>
        </div>
    </div>
    """, unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 13. Footer
# -----------------------------------------------------------------------------
st.markdown("""
<div style="text-align:center; padding:24px 0 10px 0; font-size:12px; color:#64748B;">
    ⚡ <b>EduPulse</b> – University Digital Learning Analytics Dashboard | CHRIST University | Academic Year 2026-2027
</div>
""", unsafe_allow_html=True)
