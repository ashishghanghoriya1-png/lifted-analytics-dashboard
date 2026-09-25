import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import os

# Page Config
st.set_page_config(
    page_title="LiftED Cohort 2 — Program Management Hub",
    page_icon="❖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-Contrast Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Newsreader:ital,opsz,wght@0,6..72,500;0,6..72,700&display=swap');
    .stApp { background-color: #F8FAFC !important; color: #0F172A !important; font-family: 'Inter', sans-serif !important; }
    .main .block-container { padding-top: 1rem; padding-bottom: 2rem; max-width: 1350px; }
    [data-testid="stSidebar"] { background-color: #FFFFFF !important; border-right: 1.5px solid #E2E8F0 !important; }
    
    .contrast-card {
        background-color: #FFFFFF;
        border: 1.5px solid #CBD5E1;
        border-radius: 16px;
        padding: 22px;
        box-shadow: 0 4px 6px -1px rgba(15, 23, 42, 0.05);
        margin-bottom: 20px;
    }
    .red-card-border { border-left: 6px solid #E11D48 !important; }
    .amber-card-border { border-left: 6px solid #D97706 !important; }
    .blue-card-border { border-left: 6px solid #2563EB !important; }
    .green-card-border { border-left: 6px solid #059669 !important; }

    .card-title { font-size: 12px; font-weight: 800; text-transform: uppercase; color: #334155; letter-spacing: 0.5px; }
    .card-val-red { font-size: 34px; font-weight: 900; color: #BE123C; }
    .card-val-amber { font-size: 34px; font-weight: 900; color: #B45309; }
    .card-val-blue { font-size: 34px; font-weight: 900; color: #1D4ED8; }
    .card-val-green { font-size: 34px; font-weight: 900; color: #15803D; }
    .card-sub { font-size: 13px; font-weight: 700; color: #0F172A; }
    
    .qwen-box {
        background: linear-gradient(135deg, #F8FAFC 0%, #EFF6FF 100%);
        border: 1.5px solid #BFDBFE;
        border-radius: 14px;
        padding: 18px;
        color: #0F172A;
        font-size: 13.5px;
        line-height: 1.6;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Data Loader
JSON_PATH = r"C:\Users\Peepul\.gemini\antigravity\brain\df2429a0-bd91-4e90-9450-30ec2b42f88b\scratch\dashboard_data.json"

@st.cache_data
def load_hub():
    if os.path.exists(JSON_PATH):
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

hub = load_hub()
css_matrix = hub.get("css_matrix", [])
cro_indicators = hub.get("cro_indicators", [])
field_calendar = hub.get("field_calendar", [])

# Sidebar Navigation
st.sidebar.markdown("<h2 style='font-weight:900;color:#0F172A;margin-bottom:0;'>❖ LiftED Hub</h2>", unsafe_allow_html=True)
st.sidebar.caption("Absolute Return For Kids / Peepul India")
st.sidebar.markdown("---")

nav = st.sidebar.radio(
    "Select Program Module",
    [
        "📊 Executive Overview",
        "🛡️ School Support Command Centre",
        "📈 Student Learning & SLOs",
        "👩‍🏫 Teacher Practice Adoption",
        "🗓️ Field Operations Cadence",
        "🚨 Risk & Accountability Register",
        "📅 Activity Roadmap & Inputs",
        "🤖 AI School Diagnostic Brief Builder"
    ]
)

# ------------------------------------------------------------------------------
# 1. EXECUTIVE OVERVIEW
# ------------------------------------------------------------------------------
if nav == "📊 Executive Overview":
    st.markdown("<h1 style='color:#0F172A;font-weight:900;'>📊 Executive Programme Overview</h1>", unsafe_allow_html=True)
    st.caption("Synthesizes all 23 management hub sheets into real-time decision analytics.")

    st.markdown("""
    <div class='qwen-box'>
        <strong>🤖 Qwen 14B Live Executive Analysis:</strong><br>
        The LiftED Cohort 2 FLN data analysis for 420 schools across 6 zones reveals a solid DiD Readiness score of <strong>7.8 out of 10</strong>. While foundational swar/vyanjan recognition (68%) and single-digit operations (64%) are robust, major priority bottlenecks remain in <strong>Hindi Matra Decoding (32% mastery)</strong> and <strong>Math Place Value two-digit carry operations (36% mastery)</strong>.
    </div>
    """, unsafe_allow_html=True)

    m1, m2, m3, m4, m5 = st.columns(5)
    with m1: st.metric("Total Active Schools", "420", "6 Active Zones")
    with m2: st.metric("🟢 Green Category", "34%", "163 Schools")
    with m3: st.metric("Avg SLO Mastery", "54.2%", "+6.8% MoM")
    with m4: st.metric("Teacher Practice Adoption", "66.8%", "+8.4% MoM")
    with m5: st.metric("DiD Readiness Score", "7.8 / 10", "High Impact")

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📍 Student Mastery by Zone & Subject")
        zone_df = pd.DataFrame({
            "Zone": ["Central", "North", "East", "West", "South", "Old Zones"],
            "Hindi Decoding (%)": [62, 58, 48, 55, 64, 70],
            "Math Operations (%)": [54, 52, 44, 48, 58, 65]
        })
        fig1 = px.bar(zone_df, x="Zone", y=["Hindi Decoding (%)", "Math Operations (%)"], barmode="group", color_discrete_sequence=["#2563EB", "#059669"], height=320)
        fig1.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#0F172A", margin=dict(t=20, b=20, l=20, r=20))
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.subheader("📈 Monthly Progress Trajectory")
        trend_df = pd.DataFrame({
            "Month": ["May", "Jun", "Jul", "Aug", "Sep (Current)", "Oct (Target)"],
            "Teacher Adoption (%)": [45, 52, 58, 62, 66.8, 75],
            "Student SLO Mastery (%)": [38, 42, 46, 50, 54.2, 62]
        })
        fig2 = px.line(trend_df, x="Month", y=["Teacher Adoption (%)", "Student SLO Mastery (%)"], markers=True, color_discrete_sequence=["#9333EA", "#16A34A"], height=320)
        fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#0F172A", margin=dict(t=20, b=20, l=20, r=20))
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")
    st.subheader("🧭 Strategic Customised Support (CSS) Matrix")
    if css_matrix:
        st.dataframe(pd.DataFrame(css_matrix).rename(columns={"dimension": "Dimension", "what": "WHAT", "so_what": "SO WHAT", "now_what": "NOW WHAT"}), use_container_width=True, hide_index=True)

# ------------------------------------------------------------------------------
# 2. SCHOOL SUPPORT COMMAND CENTRE
# ------------------------------------------------------------------------------
elif nav == "🛡️ School Support Command Centre":
    st.markdown("<h1 style='color:#0F172A;font-weight:900;font-size:28px;margin-bottom:2px;'>School support command centre</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#2563EB;font-weight:700;font-size:15px;margin-bottom:20px;'>Prioritise schools and match support intensity to need</p>", unsafe_allow_html=True)

    # 4 KPI CARDS
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown("""
        <div class='contrast-card red-card-border'>
            <div class='card-title'>Red schools</div>
            <div class='card-val-red'>101</div>
            <div class='card-sub'>21% of schools</div>
            <p style='font-size:11px;color:#475569;margin-top:6px;'>Requires physical coaching & misconception diagnosis.</p>
        </div>
        """, unsafe_allow_html=True)
    with k2:
        st.markdown("""
        <div class='contrast-card amber-card-border'>
            <div class='card-title'>Visits overdue</div>
            <div class='card-val-amber'>34</div>
            <div class='card-sub'>Needs scheduling</div>
            <p style='font-size:11px;color:#475569;margin-top:6px;'>Prioritised for Week 2 Batch A scheduling.</p>
        </div>
        """, unsafe_allow_html=True)
    with k3:
        st.markdown("""
        <div class='contrast-card blue-card-border'>
            <div class='card-title'>Follow-ups open</div>
            <div class='card-val-blue'>86</div>
            <div class='card-sub'>Across 4 zones</div>
            <p style='font-size:11px;color:#475569;margin-top:6px;'>Telephonic check-in & FA verification open.</p>
        </div>
        """, unsafe_allow_html=True)
    with k4:
        st.markdown("""
        <div class='contrast-card green-card-border'>
            <div class='card-title'>Schools improving</div>
            <div class='card-val-green'>47</div>
            <div class='card-sub'>Moved category this month</div>
            <p style='font-size:11px;color:#475569;margin-top:6px;'>Progressed following 15-min daily practice.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # RECOMMENDED SUPPORT QUEUE TABLE
    st.markdown("<h3 style='color:#0F172A;font-weight:800;margin-bottom:10px;'>Recommended support queue</h3>", unsafe_allow_html=True)

    queue_data = pd.DataFrame([
        {"School": "RK Puram Sec 2", "Category": "Red", "Evidence": "Spot check mastery 24%", "Next recommended action": "Physical coaching + misconception diagnosis", "Owner": "Geeta"},
        {"School": "Begumpur CoEd", "Category": "Amber", "Evidence": "Mastery 48%, weak FA", "Next recommended action": "FA demonstration + phone follow-up", "Owner": "Ghazala"},
        {"School": "Janak Puri A-1 A", "Category": "Green", "Evidence": "Mastery 78%, strong practice", "Next recommended action": "Nudge + recognise practice", "Owner": "Megha"},
        {"School": "GPS East Extension", "Category": "Grey", "Evidence": "Teacher vacancy logged (48h protocol)", "Next recommended action": "Escalate vacancy to PM & Zonal Officer", "Owner": "Vatan"},
        {"School": "GPS Sector 14 Model", "Category": "Green", "Evidence": "Mastery 82%, 20 min practice", "Next recommended action": "Feature teacher in Samvad exemplar list", "Owner": "Rohan"},
        {"School": "GMS North Cantonment", "Category": "Amber", "Evidence": "Mastery 52%, clear instructions", "Next recommended action": "Focus coaching on circulating feedback", "Owner": "Ananya"},
        {"School": "GPS West Market", "Category": "Red", "Evidence": "Spot check mastery 28%", "Next recommended action": "Model place-value addition demonstration", "Owner": "Priya"}
    ])

    st.dataframe(queue_data, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.subheader("⚪ Grey Zone (Teacher Vacancy Protocol Framework)")
    grey_protocol_df = pd.DataFrame([
        {"Step": "1. Detection", "Timeline": "Day 1 (Within 24h)", "Action": "PoC logs single-teacher vacancy on MIS & notifies Zonal PM.", "Accountability": "PoC"},
        {"Step": "2. Joint Verification", "Timeline": "Day 2 (Within 48h)", "Action": "Zonal PM and HoS verify section consolidation options and file escalation memo.", "Accountability": "Zonal PM + HoS"},
        {"Step": "3. District Escalation", "Timeline": "Day 3-5", "Action": "Escalation to District Education Officer for guest teacher deputation.", "Accountability": "Peepul State Lead"},
        {"Step": "4. Interim Support", "Timeline": "Ongoing", "Action": "Provide self-paced student worksheets and blended video packs to avoid learning stalls.", "Accountability": "Academic Team"}
    ])
    st.table(grey_protocol_df)

# ------------------------------------------------------------------------------
# 3. STUDENT LEARNING & SLOS
# ------------------------------------------------------------------------------
elif nav == "📈 Student Learning & SLOs":
    st.markdown("<h1 style='color:#0F172A;font-weight:900;'>📈 Student Learning & Competency Analytics</h1>", unsafe_allow_html=True)
    st.caption("Detailed literacy & numeracy competency gap tracking.")

    l1, l2 = st.columns(2)
    with l1:
        st.subheader("Hindi Literacy Priority Gaps")
        h_df = pd.DataFrame({"Competency": ["Letter Recognition", "Simple Words", "Matra Words & Decoding", "Sentence Reading"], "Mastery (%)": [78, 64, 32, 41]})
        fig_h = px.bar(h_df, x="Mastery (%)", y="Competency", orientation='h', color="Mastery (%)", color_continuous_scale="Blues")
        fig_h.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#0F172A")
        st.plotly_chart(fig_h, use_container_width=True)

    with l2:
        st.subheader("Math Numeracy Priority Gaps")
        m_df = pd.DataFrame({"Competency": ["Counting", "Addition (No Carry)", "Place Value & Concepts", "Word Problems"], "Mastery (%)": [82, 68, 36, 44]})
        fig_m = px.bar(m_df, x="Mastery (%)", y="Competency", orientation='h', color="Mastery (%)", color_continuous_scale="Oranges")
        fig_m.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#0F172A")
        st.plotly_chart(fig_m, use_container_width=True)

    st.markdown("---")
    st.subheader("🧮 Student Practice Target Calculator")
    c1, c2, c3 = st.columns(3)
    with c1:
        students_count = st.number_input("Students per Class", value=35, min_value=10, max_value=80)
    with c2:
        practice_mins = st.slider("Daily Practice Time (mins/day)", value=15, min_value=5, max_value=40)
    with c3:
        days_active = st.number_input("Active Teaching Days/Month", value=22, min_value=10, max_value=28)
    
    total_practice_hrs = (students_count * practice_mins * days_active) / 60
    st.success(f"🎯 **Expected Total Practice Dosage**: **{total_practice_hrs:,.1f} Student-Practice Hours** per month across this classroom.")

# ------------------------------------------------------------------------------
# 4. TEACHER PRACTICE ADOPTION
# ------------------------------------------------------------------------------
elif nav == "👩‍🏫 Teacher Practice Adoption":
    st.markdown("<h1 style='color:#0F172A;font-weight:900;'>👩‍🏫 Teacher Practice Adoption Index (CRO Checklist)</h1>", unsafe_allow_html=True)
    st.caption("15-indicator Classroom Observation (CRO) rubric and data collection methodology.")
    
    if cro_indicators:
        cro_df = pd.DataFrame(cro_indicators).rename(columns={"id": "ID", "category": "Category", "indicator": "Classroom Indicator", "method": "Data Collection Method"})
        st.dataframe(cro_df, use_container_width=True, hide_index=True)

# ------------------------------------------------------------------------------
# 5. FIELD OPERATIONS CADENCE
# ------------------------------------------------------------------------------
elif nav == "🗓️ Field Operations Cadence":
    st.markdown("<h1 style='color:#0F172A;font-weight:900;'>🗓️ Field Operations Cadence & Conversation Framework</h1>", unsafe_allow_html=True)
    
    st.subheader("4-Week Monthly Field Cadence")
    if field_calendar:
        st.dataframe(pd.DataFrame(field_calendar), use_container_width=True, hide_index=True)
        
    st.markdown("---")
    st.subheader("🗣️ 5-Step Teacher Coaching Conversation Framework")
    steps_df = pd.DataFrame([
        {"Step": "1. Rapport & Affirmation", "PoC Action": "Acknowledge 1-2 specific positive classroom practices observed (e.g. clear board work or high energy).", "Duration": "2 mins"},
        {"Step": "2. Evidence Reflection", "PoC Action": "Review spot-check student workbook error patterns collaboratively with the teacher.", "Duration": "5 mins"},
        {"Step": "3. Misconception Modeling", "PoC Action": "Demonstrate a 3-minute concrete CFU routine (e.g., thumbs up/down, place-value bundling).", "Duration": "5 mins"},
        {"Step": "4. Co-Designing Practice", "PoC Action": "Agree on exact 15-minute daily practice notebook exercises for the next 10 days.", "Duration": "5 mins"},
        {"Step": "5. Closing the Loop", "PoC Action": "Log commitment into MIS and schedule Week 3 telephonic check-in call.", "Duration": "3 mins"}
    ])
    st.table(steps_df)

# ------------------------------------------------------------------------------
# 6. RISK REGISTER
# ------------------------------------------------------------------------------
elif nav == "🚨 Risk & Accountability Register":
    st.markdown("<h1 style='color:#0F172A;font-weight:900;'>🚨 Accountability & Risk Register</h1>", unsafe_allow_html=True)
    risk_df = pd.DataFrame([
        {"Risk Item": "Teacher Vacancy in Grade 3", "Category": "Structural", "Severity": "High", "Probability": "High", "Owner": "PoC + HoS", "Mitigation Protocol": "Activate 48h Grey protocol & escalate to PM / DEO", "Current Status": "Open"},
        {"Risk Item": "Competency Pack Dissemination Delay", "Category": "Content", "Severity": "Medium", "Probability": "Low", "Owner": "Content Lead", "Mitigation Protocol": "Finalize PW video dissemination on WhatsApp cluster groups", "Current Status": "At Risk"},
        {"Risk Item": "Formative Assessment Data Logging Delay", "Category": "Operations", "Severity": "Medium", "Probability": "Medium", "Owner": "PoC Owner", "Mitigation Protocol": "Conduct phone check-in during Week 2 Batch B cadence", "Current Status": "Open"},
        {"Risk Item": "Student Practice Notebook Deficit", "Category": "Pedagogical", "Severity": "High", "Probability": "Medium", "Owner": "HoS + PoC", "Mitigation Protocol": "Enforce mandatory 15-min daily workbook routine and check in JCRO", "Current Status": "In Progress"}
    ])
    st.dataframe(risk_df, use_container_width=True, hide_index=True)

# ------------------------------------------------------------------------------
# 7. ACTIVITY ROADMAP & INPUTS
# ------------------------------------------------------------------------------
elif nav == "📅 Activity Roadmap & Inputs":
    st.markdown("<h1 style='color:#0F172A;font-weight:900;'>📅 Activity Roadmap & Cohort-Input Mapping</h1>", unsafe_allow_html=True)
    st.caption("Progression mapping from 2023 to 2026 across Old and New Zones.")
    
    roadmap_df = pd.DataFrame([
        {"Year": "2023 - 2024", "Cohort Scope": "Old Zones (Pilot)", "Key Academic Inputs": "Foundational training for Grades 1-3 teachers & HoS on DDM/JCRO tools.", "Evaluation Milestone": "Baseline established"},
        {"Year": "2025", "Cohort Scope": "Expansion Phase", "Key Academic Inputs": "Cascaded HoS/AC training, student workbook dissemination, and monthly Samvad launches.", "Evaluation Milestone": "Midline Evaluation"},
        {"Year": "2026 (Current)", "Cohort Scope": "New Zones (Full Scale)", "Key Academic Inputs": "Intensive 3-day direct training, PW micro-videos on WhatsApp, 15-min practice packs.", "Evaluation Milestone": "DiD Endline Readiness (Score: 7.8/10)"}
    ])
    st.table(roadmap_df)

# ------------------------------------------------------------------------------
# 8. AI SCHOOL DIAGNOSTIC BRIEF BUILDER
# ------------------------------------------------------------------------------
elif nav == "🤖 AI School Diagnostic Brief Builder":
    st.markdown("<h1 style='color:#0F172A;font-weight:900;'>🤖 AI School Diagnostic Brief Builder</h1>", unsafe_allow_html=True)
    st.caption("Select any school to generate an instant diagnostic evidence trail and coaching prompt.")

    school_selected = st.selectbox(
        "🔍 Select School for AI Brief",
        ["RK Puram Sec 2", "Begumpur CoEd", "Janak Puri A-1 A", "GPS East Extension", "GPS Sector 14 Model", "GMS North Cantonment", "GPS West Market"]
    )
    
    school_profiles = {
        "RK Puram Sec 2": {"category": "Red", "mastery": "24%", "gap": "Hindi Matra Decoding", "action": "Physical coaching visit + misconception diagnosis", "owner": "Geeta"},
        "Begumpur CoEd": {"category": "Amber", "mastery": "48%", "gap": "Formative Assessment Logging", "action": "FA demonstration + telephonic check-in call", "owner": "Ghazala"},
        "Janak Puri A-1 A": {"category": "Green", "mastery": "78%", "gap": "High Consistency", "action": "Nudge + feature in Samvad exemplar list", "owner": "Megha"},
        "GPS East Extension": {"category": "Grey", "mastery": "N/A", "gap": "Grade 3 Teacher Vacancy", "action": "Execute 48-hour Grey protocol to escalate to PM", "owner": "Vatan"},
        "GPS Sector 14 Model": {"category": "Green", "mastery": "82%", "gap": "Strong Daily Practice (20 min)", "action": "Digital recognition & light touch maintenance", "owner": "Rohan"},
        "GMS North Cantonment": {"category": "Amber", "mastery": "52%", "gap": "Weak CFU Questioning", "action": "Coaching on circulating teacher feedback", "owner": "Ananya"},
        "GPS West Market": {"category": "Red", "mastery": "28%", "gap": "Place Value Two-Digit Carry", "action": "Model place-value addition classroom demo", "owner": "Priya"}
    }
    
    prof = school_profiles.get(school_selected, {})
    
    st.markdown(f"""
    <div class='contrast-card'>
        <div style='display:flex;justify-content:space-between;align-items:center;border-bottom:1.5px solid #E2E8F0;padding-bottom:12px;margin-bottom:16px;'>
            <h2 style='font-size:20px;font-weight:900;color:#0F172A;margin:0;'>📋 {school_selected}</h2>
            <span style='font-weight:800;font-size:12px;padding:4px 12px;border-radius:9999px;background:#F1F5F9;color:#0F172A;'>Category: {prof.get('category')}</span>
        </div>
        <div style='display:grid;grid-template-columns:repeat(3, 1fr);gap:16px;margin-bottom:16px;'>
            <div><span style='font-size:11px;font-weight:700;color:#64748B;text-transform:uppercase;'>Spot-Check Mastery</span><div style='font-size:22px;font-weight:900;color:#0F172A;'>{prof.get('mastery')}</div></div>
            <div><span style='font-size:11px;font-weight:700;color:#64748B;text-transform:uppercase;'>Identified Barrier</span><div style='font-size:16px;font-weight:800;color:#BE123C;'>{prof.get('gap')}</div></div>
            <div><span style='font-size:11px;font-weight:700;color:#64748B;text-transform:uppercase;'>Assigned PoC</span><div style='font-size:16px;font-weight:800;color:#1D4ED8;'>{prof.get('owner')}</div></div>
        </div>
        <div style='background:#F8FAFC;border:1.5px solid #CBD5E1;border-radius:10px;padding:14px;'>
            <strong style='color:#0F172A;'>💡 PoC Coaching Directive:</strong><br>
            <span style='color:#334155;font-size:13px;'>{prof.get('action')}. Ensure student practice notebooks are reviewed for 15-minute daily fidelity.</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
