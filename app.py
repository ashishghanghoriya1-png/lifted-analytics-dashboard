import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import os
from lifted_digest import load_briefs, render_digest

# 1. PAGE CONFIGURATION
st.set_page_config(
    page_title="LIFTed Analytics Dashboard",
    page_icon="❖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. FIGMA-GRADE ULTRA-SLEEK GLASSMORPHISM STYLING (WCAG AAA HIGH CONTRAST)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,600;1,6..72,400&display=swap');

    .stApp {
        background-color: #F8FAFC !important;
        font-family: 'Inter', sans-serif !important;
    }
    .main .block-container {
        padding-top: 1.2rem;
        padding-bottom: 3rem;
        max-width: 1350px;
    }
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1.5px solid #E2E8F0 !important;
    }

    /* EMIL KOWALSKI TACTILE GLASSMORPHISM + UI/UX PRO MAX CARDS */
    .figma-card {
        background: #FFFFFF;
        border: 1.5px solid #E2E8F0;
        border-radius: 18px;
        padding: 22px 24px;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04), 0 6px 16px -2px rgba(15, 23, 42, 0.05), inset 0 1px 0 rgba(255, 255, 255, 0.9);
        transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
        margin-bottom: 22px;
        position: relative;
        overflow: hidden;
    }
    .figma-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 28px -4px rgba(15, 23, 42, 0.08), 0 4px 8px -2px rgba(15, 23, 42, 0.04);
        border-color: #CBD5E1;
    }

    /* CARD STATUS BORDERS & GLOWS */
    .border-red { border-left: 6px solid #E11D48 !important; }
    .border-amber { border-left: 6px solid #D97706 !important; }
    .border-blue { border-left: 6px solid #2563EB !important; }
    .border-green { border-left: 6px solid #059669 !important; }
    .border-purple { border-left: 6px solid #7C3AED !important; }
    .border-navy { border-left: 6px solid #1E3A8A !important; }

    /* PILL BADGES */
    .badge-red { background: #FFE4E6; color: #9F1239; font-weight: 800; font-size: 11px; padding: 4px 10px; border-radius: 9999px; border: 1px solid #FECDD3; text-transform: uppercase; }
    .badge-amber { background: #FEF3C7; color: #92400E; font-weight: 800; font-size: 11px; padding: 4px 10px; border-radius: 9999px; border: 1px solid #FDE68A; text-transform: uppercase; }
    .badge-green { background: #D1FAE5; color: #065F46; font-weight: 800; font-size: 11px; padding: 4px 10px; border-radius: 9999px; border: 1px solid #A7F3D0; text-transform: uppercase; }
    .badge-blue { background: #DBEAFE; color: #1E40AF; font-weight: 800; font-size: 11px; padding: 4px 10px; border-radius: 9999px; border: 1px solid #BFDBFE; text-transform: uppercase; }
    .badge-grey { background: #F1F5F9; color: #475569; font-weight: 800; font-size: 11px; padding: 4px 10px; border-radius: 9999px; border: 1px solid #E2E8F0; text-transform: uppercase; }

    /* TYPOGRAPHY */
    .figma-h1 {
        font-family: 'Newsreader', serif;
        font-size: 36px;
        font-weight: 600;
        color: #0F172A;
        letter-spacing: -0.5px;
        margin-bottom: 4px;
    }
    .figma-sub {
        color: #475569;
        font-size: 15px;
        font-weight: 500;
        margin-bottom: 24px;
    }
    .card-val-huge {
        font-size: 40px;
        font-weight: 900;
        line-height: 1;
        margin: 10px 0 6px 0;
        color: #0F172A;
    }

    /* QWEN DEEP ANALYSIS CONTAINER */
    .qwen-exec-container {
        background: linear-gradient(135deg, #F8FAFC 0%, #EFF6FF 100%);
        border: 1.5px solid #BFDBFE;
        border-radius: 16px;
        padding: 24px;
        color: #0F172A;
        font-size: 14px;
        line-height: 1.7;
        margin-bottom: 28px;
    }
    /* The custom dashboard uses light surfaces. Pair their native labels with
       dark text even when Streamlit's System setting resolves to dark mode.
       Input fields, menus, dialogs and buttons retain their native theme pairs. */
    [data-testid="stWidgetLabel"],
    [data-testid="stWidgetLabel"] p,
    [data-testid="stCaptionContainer"],
    [data-testid="stCaptionContainer"] p,
    [data-testid="stHeading"],
    [data-testid="stHeading"] h1,
    [data-testid="stHeading"] h2,
    [data-testid="stHeading"] h3,
    [data-testid="stMetricLabel"],
    [data-testid="stMetricValue"],
    [data-testid="stTabs"] [role="tab"],
    [data-testid="stTabs"] [role="tab"] p {
        color: #0F172A !important;
    }
    [data-testid="stTabs"] [role="tablist"] {
        background-color: #F8FAFC;
    }
    [data-testid="stTabs"] [role="tab"][aria-selected="true"] {
        color: #1D4ED8 !important;
    }
    [data-testid="stTabs"] [role="tab"][aria-selected="true"] p {
        color: inherit !important;
    }
    [data-testid="stSliderTickBarMin"],
    [data-testid="stSliderTickBarMax"],
    [data-testid="stSliderThumbValue"] {
        color: #334155 !important;
    }
    [data-testid="stMarkdownContainer"] {
        color: #0F172A;
    }
    /* Keep native dark notifications, buttons and expandable panels coherent. */
    [data-testid="stAlert"] [data-testid="stMarkdownContainer"],
    button [data-testid="stMarkdownContainer"],
    [data-testid="stExpander"] [data-testid="stMarkdownContainer"] {
        color: inherit;
    }
    [data-testid="stPlotlyChart"] {
        background-color: #FFFFFF;
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)

# 3. PORTABLE ZONE INTELLIGENCE
def render_html(html_str: str):
    """Clean all leading whitespace from every line so Streamlit markdown never interprets HTML as a code block."""
    cleaned = "\n".join(line.strip() for line in html_str.strip().split("\n"))
    st.markdown(cleaned, unsafe_allow_html=True)

zone_briefs = load_briefs()
# 4. SIDEBAR MULTI-LEVEL SLICERS & EXCEL DATA MODEL
EXCEL_PATH = r"c:\Users\Ashish\OneDrive - Absolute Return For Kids\LIFTed\LiftED Cohort 2_Program Management Hub.xlsx"

# GROUND-TRUTH ZONE & FLN DATA MODEL (DERIVED FROM EXCEL PROGRAM HUB)
ZONE_FLN_DATA = {
    "West": {
        "schools": 127, "hos_att": 117, "hos_target": 127, "hos_pct": "92.1%",
        "teacher_batches": "4/5 (80%)", "teacher_done": 4, "teacher_total": 5, "red_schools": 24, "amber_schools": 52, "green_schools": 45, "grey_schools": 6,
        "lit_prof": 61, "num_prof": 53, "risk_pct": 16, "remedial_pct": 68, "assessed": 22500,
        "tp_adoption_index": 68, "tp_adoption_change": 11, "tp_targeted_inst": 74, "tp_dedicated_practice": 62, "tp_fa_remediation": 53, "tp_engagement": 74,
        "field_visits_done": 114, "field_calls_done": 242, "vacancies_logged": 6, "samvad_pct": 91.2,
        "tp_indicators": [
            {"category": "Targeted instruction", "name": "LO aligned to focused competency", "observed": 75, "target": 75},
            {"category": "Targeted instruction", "name": "Clear competency-linked instruction", "observed": 72, "target": 80},
            {"category": "Targeted instruction", "name": "Two LO-linked questions", "observed": 58, "target": 70},
            {"category": "Dedicated practice time", "name": "Students receive feedback", "observed": 65, "target": 80},
            {"category": "Dedicated practice time", "name": "Students spend at least 15 min on practice", "observed": 63, "target": 70},
            {"category": "Dedicated practice time", "name": "Worksheets filled for previous LO", "observed": 69, "target": 90},
            {"category": "FA and remediation", "name": "Teachers shared FA data prior/during call", "observed": 57, "target": 90},
            {"category": "FA and remediation", "name": "Observed remedial strategy for focused LO", "observed": 51, "target": 60},
            {"category": "Classroom engagement", "name": "Active student engagement in questioning", "observed": 76, "target": 70},
        ],
        "competencies": [
            {"name": "Number sense", "subject": "Math", "mastery": 75, "change": 13, "priority": "Stable"},
            {"name": "Addition and subtraction", "subject": "Math", "mastery": 54, "change": 6, "priority": "Focus"},
            {"name": "ORF", "subject": "Hindi", "mastery": 49, "change": 4, "priority": "Priority"},
            {"name": "Reading comprehension", "subject": "Hindi", "mastery": 45, "change": 3, "priority": "Priority"},
            {"name": "Place value", "subject": "Math", "mastery": 39, "change": 3, "priority": "Priority"},
            {"name": "Multiplication & division", "subject": "Math", "mastery": 50, "change": 4, "priority": "Focus"},
            {"name": "Hindi Matra decoding", "subject": "Hindi", "mastery": 35, "change": 2, "priority": "Priority"},
            {"name": "Word reading", "subject": "Hindi", "mastery": 71, "change": 9, "priority": "Stable"},
        ]
    },
    "Central": {
        "schools": 128, "hos_att": 105, "hos_target": 128, "hos_pct": "82.0%",
        "teacher_batches": "1/4 (25%)", "teacher_done": 1, "teacher_total": 4, "red_schools": 31, "amber_schools": 54, "green_schools": 35, "grey_schools": 8,
        "lit_prof": 54, "num_prof": 48, "risk_pct": 22, "remedial_pct": 58, "assessed": 23000,
        "tp_adoption_index": 59, "tp_adoption_change": 6, "tp_targeted_inst": 66, "tp_dedicated_practice": 53, "tp_fa_remediation": 44, "tp_engagement": 66,
        "field_visits_done": 86, "field_calls_done": 198, "vacancies_logged": 8, "samvad_pct": 79.4,
        "tp_indicators": [
            {"category": "Targeted instruction", "name": "LO aligned to focused competency", "observed": 67, "target": 75},
            {"category": "Targeted instruction", "name": "Clear competency-linked instruction", "observed": 63, "target": 80},
            {"category": "Targeted instruction", "name": "Two LO-linked questions", "observed": 49, "target": 70},
            {"category": "Dedicated practice time", "name": "Students receive feedback", "observed": 56, "target": 80},
            {"category": "Dedicated practice time", "name": "Students spend at least 15 min on practice", "observed": 52, "target": 70},
            {"category": "Dedicated practice time", "name": "Worksheets filled for previous LO", "observed": 58, "target": 90},
            {"category": "FA and remediation", "name": "Teachers shared FA data prior/during call", "observed": 46, "target": 90},
            {"category": "FA and remediation", "name": "Observed remedial strategy for focused LO", "observed": 41, "target": 60},
            {"category": "Classroom engagement", "name": "Active student engagement in questioning", "observed": 67, "target": 70},
        ],
        "competencies": [
            {"name": "Number sense", "subject": "Math", "mastery": 68, "change": 8, "priority": "Focus"},
            {"name": "Addition and subtraction", "subject": "Math", "mastery": 47, "change": 3, "priority": "Priority"},
            {"name": "ORF", "subject": "Hindi", "mastery": 42, "change": 2, "priority": "Priority"},
            {"name": "Reading comprehension", "subject": "Hindi", "mastery": 39, "change": 1, "priority": "Priority"},
            {"name": "Place value", "subject": "Math", "mastery": 32, "change": 1, "priority": "Priority"},
            {"name": "Multiplication & division", "subject": "Math", "mastery": 44, "change": 2, "priority": "Priority"},
            {"name": "Hindi Matra decoding", "subject": "Hindi", "mastery": 28, "change": 1, "priority": "Priority"},
            {"name": "Word reading", "subject": "Hindi", "mastery": 63, "change": 6, "priority": "Focus"},
        ]
    },
    "Civil": {
        "schools": 94, "hos_att": 76, "hos_target": 94, "hos_pct": "80.9%",
        "teacher_batches": "5/5 (100%)", "teacher_done": 5, "teacher_total": 5, "red_schools": 19, "amber_schools": 38, "green_schools": 32, "grey_schools": 5,
        "lit_prof": 59, "num_prof": 52, "risk_pct": 17, "remedial_pct": 65, "assessed": 16500,
        "tp_adoption_index": 67, "tp_adoption_change": 10, "tp_targeted_inst": 73, "tp_dedicated_practice": 61, "tp_fa_remediation": 51, "tp_engagement": 73,
        "field_visits_done": 90, "field_calls_done": 186, "vacancies_logged": 5, "samvad_pct": 89.1,
        "tp_indicators": [
            {"category": "Targeted instruction", "name": "LO aligned to focused competency", "observed": 74, "target": 75},
            {"category": "Targeted instruction", "name": "Clear competency-linked instruction", "observed": 71, "target": 80},
            {"category": "Targeted instruction", "name": "Two LO-linked questions", "observed": 56, "target": 70},
            {"category": "Dedicated practice time", "name": "Students receive feedback", "observed": 64, "target": 80},
            {"category": "Dedicated practice time", "name": "Students spend at least 15 min on practice", "observed": 62, "target": 70},
            {"category": "Dedicated practice time", "name": "Worksheets filled for previous LO", "observed": 68, "target": 90},
            {"category": "FA and remediation", "name": "Teachers shared FA data prior/during call", "observed": 56, "target": 90},
            {"category": "FA and remediation", "name": "Observed remedial strategy for focused LO", "observed": 49, "target": 60},
            {"category": "Classroom engagement", "name": "Active student engagement in questioning", "observed": 75, "target": 70},
        ],
        "competencies": [
            {"name": "Number sense", "subject": "Math", "mastery": 73, "change": 12, "priority": "Stable"},
            {"name": "Addition and subtraction", "subject": "Math", "mastery": 52, "change": 5, "priority": "Focus"},
            {"name": "ORF", "subject": "Hindi", "mastery": 47, "change": 3, "priority": "Priority"},
            {"name": "Reading comprehension", "subject": "Hindi", "mastery": 43, "change": 2, "priority": "Priority"},
            {"name": "Place value", "subject": "Math", "mastery": 37, "change": 2, "priority": "Priority"},
            {"name": "Multiplication & division", "subject": "Math", "mastery": 49, "change": 3, "priority": "Focus"},
            {"name": "Hindi Matra decoding", "subject": "Hindi", "mastery": 33, "change": 2, "priority": "Priority"},
            {"name": "Word reading", "subject": "Hindi", "mastery": 69, "change": 8, "priority": "Stable"},
        ]
    },
    "South": {
        "schools": 130, "hos_att": 110, "hos_target": 130, "hos_pct": "84.6%",
        "teacher_batches": "6/6 (100%)", "teacher_done": 6, "teacher_total": 6, "red_schools": 27, "amber_schools": 57, "green_schools": 51, "grey_schools": 10,
        "lit_prof": 58, "num_prof": 51, "risk_pct": 18, "remedial_pct": 62, "assessed": 23000,
        "tp_adoption_index": 63, "tp_adoption_change": 8, "tp_targeted_inst": 70, "tp_dedicated_practice": 57, "tp_fa_remediation": 48, "tp_engagement": 70,
        "field_visits_done": 104, "field_calls_done": 234, "vacancies_logged": 10, "samvad_pct": 84.3,
        "tp_indicators": [
            {"category": "Targeted instruction", "name": "LO aligned to focused competency", "observed": 70, "target": 75},
            {"category": "Targeted instruction", "name": "Clear competency-linked instruction", "observed": 67, "target": 80},
            {"category": "Targeted instruction", "name": "Two LO-linked questions", "observed": 53, "target": 70},
            {"category": "Dedicated practice time", "name": "Students receive feedback", "observed": 60, "target": 80},
            {"category": "Dedicated practice time", "name": "Students spend at least 15 min on practice", "observed": 57, "target": 70},
            {"category": "Dedicated practice time", "name": "Worksheets filled for previous LO", "observed": 63, "target": 90},
            {"category": "FA and remediation", "name": "Teachers shared FA data prior/during call", "observed": 50, "target": 90},
            {"category": "FA and remediation", "name": "Observed remedial strategy for focused LO", "observed": 45, "target": 60},
            {"category": "Classroom engagement", "name": "Active student engagement in questioning", "observed": 71, "target": 70},
        ],
        "competencies": [
            {"name": "Number sense", "subject": "Math", "mastery": 71, "change": 10, "priority": "Stable"},
            {"name": "Addition and subtraction", "subject": "Math", "mastery": 50, "change": 4, "priority": "Focus"},
            {"name": "ORF", "subject": "Hindi", "mastery": 45, "change": 3, "priority": "Priority"},
            {"name": "Reading comprehension", "subject": "Hindi", "mastery": 41, "change": 2, "priority": "Priority"},
            {"name": "Place value", "subject": "Math", "mastery": 35, "change": 2, "priority": "Priority"},
            {"name": "Multiplication & division", "subject": "Math", "mastery": 47, "change": 3, "priority": "Focus"},
            {"name": "Hindi Matra decoding", "subject": "Hindi", "mastery": 31, "change": 1, "priority": "Priority"},
            {"name": "Word reading", "subject": "Hindi", "mastery": 68, "change": 7, "priority": "Stable"},
        ]
    }
}

ALL_PACK_DATA = {
    "September · Number Operations + ORF": {
        "title": "September · Number Operations + ORF",
        "description": "Foundational multi-digit addition, subtraction and oral reading fluency (ORF)",
        "zones": {
            "West": {"schools": 127, "received": 127, "engaged": 112, "implemented": 91, "mastery": 70, "adoption_pct": 59},
            "Central": {"schools": 128, "received": 128, "engaged": 106, "implemented": 83, "mastery": 61, "adoption_pct": 53},
            "Civil": {"schools": 94, "received": 94, "engaged": 82, "implemented": 67, "mastery": 51, "adoption_pct": 58},
            "South": {"schools": 130, "received": 130, "engaged": 111, "implemented": 89, "mastery": 65, "adoption_pct": 58},
        },
        "competencies": [
            {"name": "Number sense & addition", "subject": "Math", "reach": "88%", "practice": "58%", "mastery": "51%", "status": "Active cycle", "status_bg": "#DEF7EC", "status_color": "#03543F"},
            {"name": "Oral Reading Fluency (ORF)", "subject": "Hindi", "reach": "84%", "practice": "54%", "mastery": "46%", "status": "Active cycle", "status_bg": "#DEF7EC", "status_color": "#03543F"}
        ]
    },
    "August · Word Reading & Place Value": {
        "title": "August · Word Reading & Place Value",
        "description": "Baseline decoding of Hindi alphabets and foundational single-digit place value",
        "zones": {
            "West": {"schools": 127, "received": 127, "engaged": 119, "implemented": 104, "mastery": 83, "adoption_pct": 70},
            "Central": {"schools": 128, "received": 128, "engaged": 118, "implemented": 101, "mastery": 78, "adoption_pct": 65},
            "Civil": {"schools": 94, "received": 94, "engaged": 88, "implemented": 78, "mastery": 61, "adoption_pct": 69},
            "South": {"schools": 130, "received": 130, "engaged": 120, "implemented": 105, "mastery": 80, "adoption_pct": 67},
        },
        "competencies": [
            {"name": "Word reading & Swar/Vyanjan", "subject": "Hindi", "reach": "95%", "practice": "74%", "mastery": "68%", "status": "Completed cycle", "status_bg": "#E0E7FF", "status_color": "#3730A3"},
            {"name": "Place value (Tens & Units)", "subject": "Math", "reach": "91%", "practice": "62%", "mastery": "58%", "status": "Completed cycle", "status_bg": "#E0E7FF", "status_color": "#3730A3"}
        ]
    },
    "October · Reading Comprehension & Multi-digit Operations": {
        "title": "October · Reading Comprehension & Multi-digit Operations",
        "description": "Advanced passage comprehension, inference, and multi-digit multiplication/division",
        "zones": {
            "West": {"schools": 127, "received": 127, "engaged": 89, "implemented": 60, "mastery": 42, "adoption_pct": 41},
            "Central": {"schools": 128, "received": 128, "engaged": 83, "implemented": 52, "mastery": 35, "adoption_pct": 34},
            "Civil": {"schools": 94, "received": 94, "engaged": 66, "implemented": 43, "mastery": 30, "adoption_pct": 39},
            "South": {"schools": 130, "received": 130, "engaged": 88, "implemented": 56, "mastery": 37, "adoption_pct": 37},
        },
        "competencies": [
            {"name": "Reading comprehension & inference", "subject": "Hindi", "reach": "70%", "practice": "40%", "mastery": "31%", "status": "Early rollout", "status_bg": "#FEF3C7", "status_color": "#92400E"},
            {"name": "Multiplication & division operations", "subject": "Math", "reach": "66%", "practice": "36%", "mastery": "29%", "status": "Early rollout", "status_bg": "#FEF3C7", "status_color": "#92400E"}
        ]
    }
}

ALL_IMPACT_DATA = {
    "Baseline to current": {
        "title": "Baseline to Current Cycle",
        "scope_desc": "Cumulative outcomes measured against pre-intervention baseline diagnostics",
        "zones": {
            "West": {"schools": 127, "learning_gain": 6.8, "school_imp": 14, "adoption_gain": 10, "confidence": 75, "support_rate": 88, "practice_rate": 68, "student_prac_rate": 62, "mastery_rate": 55},
            "Central": {"schools": 128, "learning_gain": 5.4, "school_imp": 11, "adoption_gain": 8, "confidence": 69, "support_rate": 83, "practice_rate": 59, "student_prac_rate": 54, "mastery_rate": 48},
            "Civil": {"schools": 94, "learning_gain": 6.5, "school_imp": 9, "adoption_gain": 10, "confidence": 74, "support_rate": 87, "practice_rate": 67, "student_prac_rate": 60, "mastery_rate": 54},
            "South": {"schools": 130, "learning_gain": 5.9, "school_imp": 13, "adoption_gain": 8, "confidence": 71, "support_rate": 85, "practice_rate": 63, "student_prac_rate": 57, "mastery_rate": 50},
        },
        "pathway_changes": {
            "support": "+12 pts",
            "practice": "+9 pts",
            "student": "+6 pts",
            "mastery": "+6 pts"
        },
        "equity": {
            "low_baseline": "+7.4 pts",
            "low_baseline_width": 74,
            "vacancies": "+2.1 pts",
            "vacancies_width": 21,
            "red_schools": "+8.2 pts",
            "red_schools_width": 82
        }
    },
    "Cycle 1 to Cycle 2": {
        "title": "Cycle 1 to Cycle 2 (Inter-cycle)",
        "scope_desc": "Incremental velocity gains comparing August closeout with September cycle",
        "zones": {
            "West": {"schools": 127, "learning_gain": 4.6, "school_imp": 9, "adoption_gain": 7, "confidence": 83, "support_rate": 92, "practice_rate": 74, "student_prac_rate": 68, "mastery_rate": 61},
            "Central": {"schools": 128, "learning_gain": 3.8, "school_imp": 8, "adoption_gain": 5, "confidence": 79, "support_rate": 88, "practice_rate": 67, "student_prac_rate": 61, "mastery_rate": 53},
            "Civil": {"schools": 94, "learning_gain": 4.5, "school_imp": 7, "adoption_gain": 6, "confidence": 84, "support_rate": 93, "practice_rate": 73, "student_prac_rate": 66, "mastery_rate": 60},
            "South": {"schools": 130, "learning_gain": 4.1, "school_imp": 8, "adoption_gain": 6, "confidence": 81, "support_rate": 90, "practice_rate": 70, "student_prac_rate": 64, "mastery_rate": 56},
        },
        "pathway_changes": {
            "support": "+6 pts",
            "practice": "+7 pts",
            "student": "+5 pts",
            "mastery": "+5 pts"
        },
        "equity": {
            "low_baseline": "+5.8 pts",
            "low_baseline_width": 58,
            "vacancies": "+1.6 pts",
            "vacancies_width": 16,
            "red_schools": "+6.4 pts",
            "red_schools_width": 64
        }
    },
    "Projected endline": {
        "title": "Projected Endline Trajectory",
        "scope_desc": "Forecasted impact modeled on sustained 15-minute daily practice and coaching intensity",
        "zones": {
            "West": {"schools": 127, "learning_gain": 12.8, "school_imp": 26, "adoption_gain": 20, "confidence": 67, "support_rate": 96, "practice_rate": 85, "student_prac_rate": 80, "mastery_rate": 74},
            "Central": {"schools": 128, "learning_gain": 10.3, "school_imp": 22, "adoption_gain": 16, "confidence": 61, "support_rate": 93, "practice_rate": 78, "student_prac_rate": 72, "mastery_rate": 65},
            "Civil": {"schools": 94, "learning_gain": 12.2, "school_imp": 19, "adoption_gain": 19, "confidence": 66, "support_rate": 97, "practice_rate": 84, "student_prac_rate": 78, "mastery_rate": 73},
            "South": {"schools": 130, "learning_gain": 11.2, "school_imp": 22, "adoption_gain": 18, "confidence": 64, "support_rate": 95, "practice_rate": 81, "student_prac_rate": 75, "mastery_rate": 68},
        },
        "pathway_changes": {
            "support": "+18 pts",
            "practice": "+18 pts",
            "student": "+15 pts",
            "mastery": "+14 pts"
        },
        "equity": {
            "low_baseline": "+13.2 pts",
            "low_baseline_width": 92,
            "vacancies": "+4.5 pts",
            "vacancies_width": 45,
            "red_schools": "+15.1 pts",
            "red_schools_width": 98
        }
    }
}
ZONE_IMPACT_DATA = ALL_IMPACT_DATA["Baseline to current"]["zones"]

st.sidebar.markdown("<h2 style='font-family:Newsreader;font-size:24px;font-weight:600;color:#0F172A;'>❖ LIFTed Analytics Dashboard</h2>", unsafe_allow_html=True)
st.sidebar.caption("Figma-Grade Ollama Qwen Analytics Engine")
st.sidebar.markdown("---")

st.sidebar.markdown("<h4 style='font-weight:800;color:#334155;font-size:12px;text-transform:uppercase;'>🎛️ Interactive Program Slicers</h4>", unsafe_allow_html=True)

zone_filter = st.sidebar.multiselect(
    "📍 Select Zone(s)",
    ["All Zones", "West", "Central", "Civil", "South"],
    default=["All Zones"]
)

category_filter = st.sidebar.multiselect(
    "🎯 Select Category",
    ["All Categories", "Green (163)", "Amber (201)", "Red (101)", "Grey (29)"],
    default=["All Categories"]
)

poc_filter = st.sidebar.selectbox(
    "👤 Select PoC Owner",
    ["All Owners", "Geeta", "Megha", "Sakshi", "Swagata", "Harshita", "Anshika", "Malya", "Sheetal", "Riya", "Anchal", "Veena", "Manish", "Shalini", "Aditya", "Kavya", "Keerthi"]
)

subject_filter = st.sidebar.selectbox(
    "📚 Select Competency Subject",
    ["All Subjects", "Numeracy (Math FLN)", "Literacy (Hindi FLN)"]
)

mastery_slider = st.sidebar.slider(
    "🎚️ Mastery Threshold Filter (%)",
    min_value=0, max_value=100, value=(0, 100)
)

st.sidebar.markdown("---")

# DYNAMIC AGGREGATION BASED ON ACTIVE SLICERS
if not zone_filter or "All Zones" in zone_filter:
    active_zones = list(ZONE_FLN_DATA.keys())
    zone_label = "All Zones (West, Central, Civil, South)"
    zone_badge_text = "All Zones"
else:
    active_zones = [z for z in zone_filter if z in ZONE_FLN_DATA]
    if not active_zones:
        active_zones = list(ZONE_FLN_DATA.keys())
    zone_label = ", ".join(active_zones) + " Zone" + ("s" if len(active_zones) > 1 else "")
    zone_badge_text = ", ".join(active_zones)

total_active_schools = sum(ZONE_FLN_DATA[z]["schools"] for z in active_zones)
total_hos_att = sum(ZONE_FLN_DATA[z]["hos_att"] for z in active_zones)
total_hos_target = sum(ZONE_FLN_DATA[z]["hos_target"] for z in active_zones)
hos_attendance_pct = round((total_hos_att / total_hos_target) * 100, 1) if total_hos_target > 0 else 85.2

teacher_batches_done = sum(ZONE_FLN_DATA[z]["teacher_done"] for z in active_zones)
teacher_batches_total = sum(ZONE_FLN_DATA[z]["teacher_total"] for z in active_zones)
teacher_batch_pct = round((teacher_batches_done / teacher_batches_total) * 100, 1) if teacher_batches_total > 0 else 80.0

total_red_schools = sum(ZONE_FLN_DATA[z]["red_schools"] for z in active_zones)
total_amber_schools = sum(ZONE_FLN_DATA[z]["amber_schools"] for z in active_zones)
total_green_schools = sum(ZONE_FLN_DATA[z]["green_schools"] for z in active_zones)
total_grey_schools = sum(ZONE_FLN_DATA[z]["grey_schools"] for z in active_zones)

# Weighted student learning metrics
dyn_lit_prof = round(sum(ZONE_FLN_DATA[z]["schools"] * ZONE_FLN_DATA[z]["lit_prof"] for z in active_zones) / total_active_schools)
dyn_num_prof = round(sum(ZONE_FLN_DATA[z]["schools"] * ZONE_FLN_DATA[z]["num_prof"] for z in active_zones) / total_active_schools)
dyn_risk_pct = round(sum(ZONE_FLN_DATA[z]["schools"] * ZONE_FLN_DATA[z]["risk_pct"] for z in active_zones) / total_active_schools)
dyn_remedial_pct = round(sum(ZONE_FLN_DATA[z]["schools"] * ZONE_FLN_DATA[z]["remedial_pct"] for z in active_zones) / total_active_schools)
dyn_assessed = sum(ZONE_FLN_DATA[z]["assessed"] for z in active_zones)

# Aggregate competencies dynamically across active zones
comp_names = ["Number sense", "Addition and subtraction", "ORF", "Reading comprehension", "Place value", "Multiplication & division", "Hindi Matra decoding", "Word reading"]
aggregated_comps = []
for c_name in comp_names:
    c_subj = "Math" if c_name in ["Number sense", "Addition and subtraction", "Place value", "Multiplication & division"] else "Hindi"
    c_mastery = round(sum(ZONE_FLN_DATA[z]["schools"] * next(item["mastery"] for item in ZONE_FLN_DATA[z]["competencies"] if item["name"] == c_name) for z in active_zones) / total_active_schools)
    c_change = round(sum(ZONE_FLN_DATA[z]["schools"] * next(item["change"] for item in ZONE_FLN_DATA[z]["competencies"] if item["name"] == c_name) for z in active_zones) / total_active_schools)
    
    if c_mastery >= 65:
        p_label, p_bg, p_color = "Stable", "#DEF7EC", "#03543F"
    elif c_mastery >= 50:
        p_label, p_bg, p_color = "Focus", "#FEF3C7", "#92400E"
    else:
        p_label, p_bg, p_color = "Priority", "#FEE2E2", "#991B1B"
        
    aggregated_comps.append({
        "name": c_name,
        "subject": c_subj,
        "mastery": c_mastery,
        "change": c_change,
        "priority": p_label,
        "bg": p_bg,
        "color": p_color
    })

# Filter competencies by Subject Slicer
if subject_filter == "Numeracy (Math FLN)":
    filtered_comps = [c for c in aggregated_comps if c["subject"] == "Math"]
elif subject_filter == "Literacy (Hindi FLN)":
    filtered_comps = [c for c in aggregated_comps if c["subject"] == "Hindi"]
else:
    # All subjects: Core 4 as displayed in reference mockup
    filtered_comps = [c for c in aggregated_comps if c["name"] in ["Number sense", "Addition and subtraction", "ORF", "Reading comprehension"]]

# Filter competencies by Mastery Slider
min_m, max_m = mastery_slider
filtered_comps = [c for c in filtered_comps if min_m <= c["mastery"] <= max_m]

# Weighted Teacher Practice adoption metrics (Dynamically derived from active zones)
dyn_tp_weight = total_active_schools
if dyn_tp_weight > 0:
    dyn_tp_index = round(sum(ZONE_FLN_DATA[z]["schools"] * ZONE_FLN_DATA[z]["tp_adoption_index"] for z in active_zones) / dyn_tp_weight)
    dyn_tp_change = round(sum(ZONE_FLN_DATA[z]["schools"] * ZONE_FLN_DATA[z]["tp_adoption_change"] for z in active_zones) / dyn_tp_weight)
    dyn_tp_ti = round(sum(ZONE_FLN_DATA[z]["schools"] * ZONE_FLN_DATA[z]["tp_targeted_inst"] for z in active_zones) / dyn_tp_weight)
    dyn_tp_dp = round(sum(ZONE_FLN_DATA[z]["schools"] * ZONE_FLN_DATA[z]["tp_dedicated_practice"] for z in active_zones) / dyn_tp_weight)
    dyn_tp_fa = round(sum(ZONE_FLN_DATA[z]["schools"] * ZONE_FLN_DATA[z]["tp_fa_remediation"] for z in active_zones) / dyn_tp_weight)
    dyn_tp_engagement = round(sum(ZONE_FLN_DATA[z]["schools"] * ZONE_FLN_DATA[z]["tp_engagement"] for z in active_zones) / dyn_tp_weight)
    
    # Field operations metrics
    dyn_field_visits_done = sum(ZONE_FLN_DATA[z]["field_visits_done"] for z in active_zones)
    dyn_field_visits_target = total_active_schools
    dyn_field_calls_done = sum(ZONE_FLN_DATA[z]["field_calls_done"] for z in active_zones)
    dyn_field_calls_target = total_active_schools * 2
    dyn_vacancies_logged = sum(ZONE_FLN_DATA[z]["vacancies_logged"] for z in active_zones)
    dyn_samvad_pct = round(sum(ZONE_FLN_DATA[z]["schools"] * ZONE_FLN_DATA[z]["samvad_pct"] for z in active_zones) / dyn_tp_weight, 1)
else:
    dyn_tp_index, dyn_tp_change, dyn_tp_ti, dyn_tp_dp, dyn_tp_fa, dyn_tp_engagement = 64, 9, 71, 58, 49, 72
    dyn_field_visits_done, dyn_field_visits_target, dyn_field_calls_done, dyn_field_calls_target, dyn_vacancies_logged, dyn_samvad_pct = 394, 479, 860, 958, 29, 85.6

# Teacher Practice Indicator dynamic aggregation across active zones
tp_indicator_definitions = [
    {"category": "Targeted instruction", "name": "LO aligned to focused competency", "target": 75},
    {"category": "Targeted instruction", "name": "Clear competency-linked instruction", "target": 80},
    {"category": "Targeted instruction", "name": "Two LO-linked questions", "target": 70},
    {"category": "Dedicated practice time", "name": "Students receive feedback", "target": 80},
    {"category": "Dedicated practice time", "name": "Students spend at least 15 min on practice", "target": 70},
    {"category": "Dedicated practice time", "name": "Worksheets filled for previous LO", "target": 90},
    {"category": "FA and remediation", "name": "Teachers shared FA data prior/during call", "target": 90},
    {"category": "FA and remediation", "name": "Observed remedial strategy for focused LO", "target": 60},
    {"category": "Classroom engagement", "name": "Active student engagement in questioning", "target": 70},
]

aggregated_tp_indicators = []
for ind_def in tp_indicator_definitions:
    ind_name = ind_def["name"]
    ind_target = ind_def["target"]
    ind_cat = ind_def["category"]
    
    ind_obs = round(sum(ZONE_FLN_DATA[z]["schools"] * next(item["observed"] for item in ZONE_FLN_DATA[z]["tp_indicators"] if item["name"] == ind_name) for z in active_zones) / total_active_schools)
    gap = ind_obs - ind_target
    
    if gap >= 0:
        interp, bg, color = "On track", "#DEF7EC", "#03543F"
    elif gap >= -10:
        interp, bg, color = "Near target", "#FEF3C7", "#B45309"
    elif gap >= -15:
        interp, bg, color = "Coach", "#FEF3C7", "#B45309"
    else:
        interp, bg, color = "Priority", "#FEE2E2", "#BE123C"
        
    aggregated_tp_indicators.append({
        "category": ind_cat,
        "name": ind_name,
        "observed": ind_obs,
        "target": ind_target,
        "gap": gap,
        "interpretation": interp,
        "bg": bg,
        "color": color
    })

# Active Filters Indicator Summary
active_filters = []
if "All Zones" not in zone_filter and zone_filter:
    active_filters.append(f"Zone: **{', '.join(zone_filter)}**")
if "All Categories" not in category_filter and category_filter:
    active_filters.append(f"Category: **{', '.join(category_filter)}**")
if poc_filter != "All Owners":
    active_filters.append(f"PoC: **{poc_filter}**")
if subject_filter != "All Subjects":
    active_filters.append(f"Subject: **{subject_filter}**")
if mastery_slider != (0, 100):
    active_filters.append(f"Mastery: **{min_m}%–{max_m}%**")

# HORIZONTAL TOP NAVIGATION BAR
tabs = st.tabs([
    "📊 Executive Summary",
    "🛡️ School support command centre",
    "📈 Student Learning & SLOs",
    "👩‍🏫 Teacher Practice Adoption",
    "🗓️ Field Operations Cadence",
    "📦 Competency pack analytics",
    "🎯 Impact and evaluation",
    "⚠️ Risks and Decisions",
    "🤖 School AI Brief"
])

# ------------------------------------------------------------------------------
# TAB 1: EXECUTIVE SUMMARY (DYNAMIC KPIS & CHARTS CONNECTED TO SLICERS)
# ------------------------------------------------------------------------------
with tabs[0]:
    # HEADER
    st.markdown(f"""
    <div style='display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:18px;'>
        <div>
            <h2 style='font-size:24px;font-weight:700;color:#0F172A;margin:0 0 4px 0;'>Programme Overview</h2>
            <div style='font-size:13px;color:#64748B;font-weight:400;'>A consolidated view of school reach, leadership engagement and teacher training progress across {zone_label} — Week ending 11 Sep 2026</div>
        </div>
        <div style='background:#FFFFFF;border:1px solid #E2E8F0;border-radius:8px;padding:5px 14px;font-size:12px;color:#475569;font-weight:500;box-shadow:0 1px 2px rgba(0,0,0,0.04);'>
            Cohort 2 &nbsp;·&nbsp; {zone_badge_text} &nbsp;·&nbsp; Sep 2026
        </div>
    </div>
    """, unsafe_allow_html=True)

    if active_filters:
        st.info("🔍 **Filters active:** " + " | ".join(active_filters))

    # PROGRAMME PROGRESS FLOW STRIP
    st.markdown(f"""
    <div style='display:flex;align-items:center;justify-content:space-between;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:10px;padding:10px 20px;margin-bottom:24px;font-size:12px;'>
        <div style='display:flex;flex-direction:column;align-items:center;gap:2px;'>
            <span style='font-weight:800;color:#0F172A;font-size:18px;'>{total_active_schools}</span>
            <span style='color:#64748B;font-weight:500;'>Schools in scope</span>
        </div>
        <span style='color:#CBD5E1;font-size:18px;font-weight:300;'>›</span>
        <div style='display:flex;flex-direction:column;align-items:center;gap:2px;'>
            <span style='font-weight:800;color:#0F766E;font-size:18px;'>{hos_attendance_pct}%</span>
            <span style='color:#64748B;font-weight:500;'>Head of School attendance</span>
        </div>
        <span style='color:#CBD5E1;font-size:18px;font-weight:300;'>›</span>
        <div style='display:flex;flex-direction:column;align-items:center;gap:2px;'>
            <span style='font-weight:800;color:#0F766E;font-size:18px;'>{teacher_batch_pct}%</span>
            <span style='color:#64748B;font-weight:500;'>Teacher batches completed</span>
        </div>
        <span style='color:#CBD5E1;font-size:18px;font-weight:300;'>›</span>
        <div style='display:flex;flex-direction:column;align-items:center;gap:2px;'>
            <span style='font-weight:800;color:#047857;font-size:18px;'>47</span>
            <span style='color:#64748B;font-weight:500;'>Schools improved category</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 4 KPI CARDS
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_html(f"""
        <div class='figma-card' style='padding:18px 20px;'>
            <div style='font-size:12px;color:#64748B;font-weight:500;margin-bottom:6px;letter-spacing:0.02em;'>Schools in scope</div>
            <div style='font-size:34px;font-weight:700;color:#0F172A;line-height:1.1;margin-bottom:6px;'>{total_active_schools}</div>
            <div style='font-size:12px;color:#059669;font-weight:500;'>Grade 3 FLN &nbsp;·&nbsp; {zone_badge_text}</div>
        </div>
        """)
    with c2:
        render_html(f"""
        <div class='figma-card' style='padding:18px 20px;'>
            <div style='font-size:12px;color:#64748B;font-weight:500;margin-bottom:6px;letter-spacing:0.02em;'>Head of School attendance</div>
            <div style='font-size:34px;font-weight:700;color:#0F172A;line-height:1.1;margin-bottom:6px;'>{hos_attendance_pct}%</div>
            <div style='font-size:12px;color:#059669;font-weight:500;'>{total_hos_att} of {total_hos_target} leaders attended</div>
        </div>
        """)
    with c3:
        render_html(f"""
        <div class='figma-card' style='padding:18px 20px;'>
            <div style='font-size:12px;color:#64748B;font-weight:500;margin-bottom:6px;letter-spacing:0.02em;'>Teacher batch completion</div>
            <div style='font-size:34px;font-weight:700;color:#0F172A;line-height:1.1;margin-bottom:6px;'>{teacher_batch_pct}%</div>
            <div style='font-size:12px;color:#059669;font-weight:500;'>{teacher_batches_done} of {teacher_batches_total} batches delivered</div>
        </div>
        """)
    with c4:
        render_html(f"""
        <div class='figma-card' style='padding:18px 20px;'>
            <div style='font-size:12px;color:#64748B;font-weight:500;margin-bottom:6px;letter-spacing:0.02em;'>Schools needing intensive support</div>
            <div style='font-size:34px;font-weight:700;color:#BE123C;line-height:1.1;margin-bottom:6px;'>{total_red_schools}</div>
            <div style='font-size:12px;color:#BE123C;font-weight:600;'>{round(total_red_schools/total_active_schools*100)}% of all schools in programme</div>
        </div>
        """)

    st.markdown("<br>", unsafe_allow_html=True)

    # CHARTS ROW
    col_chart1, col_chart2 = st.columns([1.35, 1.0])

    with col_chart1:
        render_html("""
<div style='margin-bottom:4px;'>
<div style='font-size:15px;font-weight:700;color:#0F172A;'>Reach and Leadership Engagement by Zone</div>
<div style='font-size:12px;color:#94A3B8;margin-top:2px;'>Number of target schools per zone against Head of School attendance in the September session</div>
</div>
""")
        zone_df = pd.DataFrame([
            {
                "Zone": z,
                "Target Schools": ZONE_FLN_DATA[z]["schools"],
                "HoS Attended": ZONE_FLN_DATA[z]["hos_att"],
                "HoS Attendance %": ZONE_FLN_DATA[z]["hos_pct"],
                "Teacher Batches": ZONE_FLN_DATA[z]["teacher_batches"],
                "Active": "Active" if z in active_zones else "Filtered Out"
            }
            for z in ["West", "Central", "Civil", "South"]
        ])

        fig_zone_col = go.Figure()

        # Target schools bars — deep navy
        fig_zone_col.add_trace(go.Bar(
            x=zone_df["Zone"],
            y=zone_df["Target Schools"],
            name="Target Schools",
            marker=dict(
                color=[
                    "rgba(30,58,138,0.90)" if z in active_zones else "rgba(203,213,225,0.5)"
                    for z in zone_df["Zone"]
                ],
                cornerradius=5,
                line=dict(width=0)
            ),
            text=[f"{v}" for v in zone_df["Target Schools"]],
            textposition="outside",
            textfont=dict(size=12, family="Inter", color="#1E3A8A", weight=700),
            customdata=zone_df[["HoS Attendance %", "Teacher Batches"]],
            hovertemplate="<b>%{x} Zone</b><br>Target Schools: <b>%{y}</b><br>HoS Attendance: <b>%{customdata[0]}%</b><extra></extra>",
            width=0.32,
        ))

        # HoS attended bars — teal
        fig_zone_col.add_trace(go.Bar(
            x=zone_df["Zone"],
            y=zone_df["HoS Attended"],
            name="HoS Attended",
            marker=dict(
                color=[
                    "rgba(5,150,105,0.85)" if z in active_zones else "rgba(167,243,208,0.5)"
                    for z in zone_df["Zone"]
                ],
                cornerradius=5,
                line=dict(width=0)
            ),
            text=[f"{v}" for v in zone_df["HoS Attended"]],
            textposition="outside",
            textfont=dict(size=12, family="Inter", color="#047857", weight=700),
            customdata=zone_df[["HoS Attendance %", "Teacher Batches"]],
            hovertemplate="<b>%{x} Zone</b><br>HoS Attended: <b>%{y}</b> (%{customdata[0]}%)<extra></extra>",
            width=0.32,
        ))

        fig_zone_col.update_layout(
            barmode="group",
            bargap=0.30,
            bargroupgap=0.08,
            height=320,
            margin=dict(t=40, b=60, l=10, r=10),
            legend=dict(
                orientation="h",
                yanchor="top",
                y=-0.22,
                xanchor="center",
                x=0.5,
                font=dict(size=12, family="Inter", color="#475569"),
                bgcolor="rgba(0,0,0,0)",
                borderwidth=0,
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", color="#0F172A"),
            yaxis=dict(
                gridcolor="#F1F5F9",
                gridwidth=1,
                zeroline=False,
                showline=False,
                tickfont=dict(color="#94A3B8", size=11, family="Inter"),
                range=[0, max(zone_df["Target Schools"].max(), 180) * 1.22],
            ),
            xaxis=dict(
                tickfont=dict(color="#0F172A", size=13, family="Inter", weight=600),
                linecolor="#E2E8F0",
                showgrid=False,
            ),
        )
        st.plotly_chart(fig_zone_col, use_container_width=True, theme=None)

    with col_chart2:
        render_html("""
<div style='margin-bottom:4px;'>
<div style='font-size:15px;font-weight:700;color:#0F172A;'>Support Pathway Distribution</div>
<div style='font-size:12px;color:#94A3B8;margin-top:2px;'>Classification of active schools by intensity of support required this cycle</div>
</div>
""")
        # Premium donut — muted premium palette, thick ring, clean inner label
        rag_values = [total_green_schools, total_amber_schools, total_red_schools, total_grey_schools]
        rag_labels = ["Sustaining (Green)", "Developing (Amber)", "Intensive (Red)", "Paused (Grey)"]
        rag_colors = ["#0D9488", "#D97706", "#DC2626", "#94A3B8"]

        fig_rag_donut = go.Figure(data=[go.Pie(
            labels=rag_labels,
            values=rag_values,
            hole=0.68,
            rotation=90,
            marker=dict(
                colors=rag_colors,
                line=dict(color="#FFFFFF", width=4)
            ),
            textinfo="none",
            hovertemplate="<b>%{label}</b><br>%{value} schools&nbsp; (%{percent})<extra></extra>",
            direction="clockwise",
        )])

        # Custom legend as annotation rows — cleaner than Plotly legend
        fig_rag_donut.update_layout(
            height=320,
            margin=dict(t=20, b=10, l=10, r=10),
            showlegend=True,
            legend=dict(
                orientation="v",
                yanchor="middle",
                y=0.5,
                xanchor="left",
                x=1.02,
                font=dict(size=12, family="Inter", color="#475569"),
                bgcolor="rgba(0,0,0,0)",
                borderwidth=0,
                itemsizing="constant",
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", color="#0F172A"),
            annotations=[
                dict(
                    text=f"<b><span style='font-size:28px;font-weight:800;color:#0F172A;'>{total_active_schools}</span></b><br><span style='font-size:11px;color:#94A3B8;font-weight:600;letter-spacing:0.06em;'>ACTIVE</span>",
                    showarrow=False,
                    x=0.5, y=0.5,
                    xanchor="center", yanchor="middle",
                    font=dict(family="Inter", size=13, color="#0F172A"),
                )
            ]
        )
        st.plotly_chart(fig_rag_donut, use_container_width=True, theme=None)

        # Inline legend pills below chart
        render_html(f"""
<div style='display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin-top:-8px;margin-bottom:8px;'>
    <span style='display:inline-flex;align-items:center;gap:5px;font-size:11px;font-weight:600;color:#0F172A;'>
        <span style='width:10px;height:10px;border-radius:50%;background:#0D9488;display:inline-block;'></span>Sustaining&nbsp;<span style='color:#64748B;font-weight:400;'>{total_green_schools}</span>
    </span>
    <span style='display:inline-flex;align-items:center;gap:5px;font-size:11px;font-weight:600;color:#0F172A;'>
        <span style='width:10px;height:10px;border-radius:50%;background:#D97706;display:inline-block;'></span>Developing&nbsp;<span style='color:#64748B;font-weight:400;'>{total_amber_schools}</span>
    </span>
    <span style='display:inline-flex;align-items:center;gap:5px;font-size:11px;font-weight:600;color:#0F172A;'>
        <span style='width:10px;height:10px;border-radius:50%;background:#DC2626;display:inline-block;'></span>Intensive&nbsp;<span style='color:#64748B;font-weight:400;'>{total_red_schools}</span>
    </span>
    <span style='display:inline-flex;align-items:center;gap:5px;font-size:11px;font-weight:600;color:#0F172A;'>
        <span style='width:10px;height:10px;border-radius:50%;background:#94A3B8;display:inline-block;'></span>Paused&nbsp;<span style='color:#64748B;font-weight:400;'>{total_grey_schools}</span>
    </span>
</div>
""")

    st.markdown("<br>", unsafe_allow_html=True)

    # Zone selection applies immediately; persisted Qwen briefs also work on hosting.
    render_html(f"""
<div class='qwen-exec-container'>
<div style='font-weight:700;font-size:15px;color:#1E3A8A;'>📊 Programme Intelligence Digest</div>
<p style='font-size:12px;color:#475569;'>Scope: {zone_badge_text} · Programme snapshot: week ending 11 Sep 2026. Zone-level analysis; other slicers do not change this brief. Recommendations require programme review.</p>
{render_digest(active_zones, ZONE_FLN_DATA, zone_briefs)}
</div>
""")

# ------------------------------------------------------------------------------
# TAB 2: SCHOOL SUPPORT COMMAND CENTRE (SLICER REACTIVE)
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# TAB 2: SCHOOL SUPPORT COMMAND CENTRE (SLICER REACTIVE)
# ------------------------------------------------------------------------------
with tabs[1]:
    # HEADER SECTION (DEFAULT FIGMA DESIGN MATCHING TAB 6)
    st.markdown(f"""
    <div style='display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:18px;'>
        <div>
            <h2 style='font-size:24px;font-weight:700;color:#0F172A;margin:0 0 4px 0;'>School support command centre</h2>
            <div style='font-size:13px;color:#64748B;font-weight:400;'>Prioritise schools and match support intensity to need across active zones</div>
        </div>
        <div style='background:#FFFFFF;border:1px solid #E2E8F0;border-radius:8px;padding:5px 14px;font-size:12px;color:#475569;font-weight:500;box-shadow:0 1px 2px rgba(0,0,0,0.04);'>
            September · Cohort 2 · {zone_badge_text}
        </div>
    </div>
    """, unsafe_allow_html=True)

    if active_filters:
        st.info("🔍 **Active Slicers Applied:** " + " | ".join(active_filters))

    # STEPPED SUPPORT TRIAGE STRIP (MATCHING TAB 6)
    st.markdown(f"""
    <div style='display:flex;align-items:center;justify-content:space-between;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:10px;padding:8px 16px;margin-bottom:24px;font-size:12px;'>
        <div style='display:flex;align-items:center;gap:6px;'>
            <span style='font-weight:700;color:#0F172A;'>{total_active_schools}</span>
            <span style='color:#64748B;'>Active Schools</span>
        </div>
        <span style='color:#94A3B8;font-weight:600;'>&rarr;</span>
        <div style='display:flex;align-items:center;gap:6px;'>
            <span style='font-weight:700;color:#BE123C;'>{total_red_schools} Red</span>
            <span style='color:#64748B;'>Intensive Coaching</span>
        </div>
        <span style='color:#94A3B8;font-weight:600;'>&rarr;</span>
        <div style='display:flex;align-items:center;gap:6px;'>
            <span style='font-weight:700;color:#B45309;'>{total_amber_schools} Amber</span>
            <span style='color:#64748B;'>Targeted Coaching</span>
        </div>
        <span style='color:#94A3B8;font-weight:600;'>&rarr;</span>
        <div style='display:flex;align-items:center;gap:6px;'>
            <span style='font-weight:700;color:#047857;'>{total_green_schools} Green</span>
            <span style='color:#64748B;'>Light Touch</span>
        </div>
        <span style='color:#94A3B8;font-weight:600;'>&rarr;</span>
        <div style='display:flex;align-items:center;gap:6px;'>
            <span style='font-weight:700;color:#475569;'>{total_grey_schools} Grey</span>
            <span style='color:#64748B;'>Vacancy Protocol</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 4 DYNAMIC MINIMALIST FIGMA-GRADE KPI CARDS (MATCHING TAB 6)
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        render_html(f"""
        <div class='figma-card' style='padding:18px 20px;'>
            <div style='font-size:12px;color:#64748B;font-weight:500;margin-bottom:6px;'>Category Red</div>
            <div style='font-size:34px;font-weight:700;color:#BE123C;line-height:1.1;margin-bottom:6px;'>{total_red_schools}</div>
            <div style='font-size:12px;color:#BE123C;font-weight:600;'>{round(total_red_schools/total_active_schools*100)}% of schools</div>
        </div>
        """)
    with k2:
        render_html(f"""
        <div class='figma-card' style='padding:18px 20px;'>
            <div style='font-size:12px;color:#64748B;font-weight:500;margin-bottom:6px;'>Visits overdue</div>
            <div style='font-size:34px;font-weight:700;color:#0F172A;line-height:1.1;margin-bottom:6px;'>34</div>
            <div style='font-size:12px;color:#B45309;font-weight:500;'>Scheduled for Week 2</div>
        </div>
        """)
    with k3:
        render_html(f"""
        <div class='figma-card' style='padding:18px 20px;'>
            <div style='font-size:12px;color:#64748B;font-weight:500;margin-bottom:6px;'>Follow-ups open</div>
            <div style='font-size:34px;font-weight:700;color:#0F172A;line-height:1.1;margin-bottom:6px;'>86</div>
            <div style='font-size:12px;color:#059669;font-weight:500;'>Across active zones</div>
        </div>
        """)
    with k4:
        render_html(f"""
        <div class='figma-card' style='padding:18px 20px;'>
            <div style='font-size:12px;color:#64748B;font-weight:500;margin-bottom:6px;'>Schools improving</div>
            <div style='font-size:34px;font-weight:700;color:#0F172A;line-height:1.1;margin-bottom:6px;'>47</div>
            <div style='font-size:12px;color:#059669;font-weight:600;'>Moved category this cycle</div>
        </div>
        """)

    st.markdown("<br>", unsafe_allow_html=True)

    # RECOMMENDED SUPPORT QUEUE TABLE (EXECUTIVE AGENCY DESIGN MATCHING TAB 6)
    queue_data_raw = [
        {"School": "RK Puram Sec 2", "Zone": "Central", "Category": "Red", "cat_bg": "#FEE2E2", "cat_col": "#991B1B", "Evidence": "Spot check mastery 24%", "Next recommended action": "Physical coaching + misconception diagnosis", "Owner": "Geeta", "Qwen Diagnostic": "Critical decoding bottleneck. PoC Geeta conducts in-person classroom demonstration on matra combinations."},
        {"School": "Begumpur CoEd", "Zone": "West", "Category": "Amber", "cat_bg": "#FEF3C7", "cat_col": "#92400E", "Evidence": "Mastery 48%, weak FA", "Next recommended action": "FA demonstration + phone follow-up", "Owner": "Ghazala", "Qwen Diagnostic": "Emerging student mastery but weak formative assessment logging. PoC Ghazala demonstrates FA logging."},
        {"School": "Janak Puri A-1 A", "Zone": "West", "Category": "Green", "cat_bg": "#DEF7EC", "cat_col": "#03543F", "Evidence": "Mastery 78%, strong practice", "Next recommended action": "Nudge + recognise practice", "Owner": "Megha", "Qwen Diagnostic": "High mastery (>75%) and consistent practice routines. PoC Megha features teacher in Samvad exemplar list."},
        {"School": "GPS Civil Lines East", "Zone": "Civil", "Category": "Grey", "cat_bg": "#F1F5F9", "cat_col": "#475569", "Evidence": "Teacher vacancy logged (48h protocol)", "Next recommended action": "Escalate vacancy to PM & Zonal Officer", "Owner": "Vatan", "Qwen Diagnostic": "Structural Grade 3 teacher vacancy. PoC Vatan executes 48-hour Grey protocol to identify interim teaching."},
        {"School": "GPS Sector 14 Model", "Zone": "South", "Category": "Green", "cat_bg": "#DEF7EC", "cat_col": "#03543F", "Evidence": "Mastery 82%, 20 min practice", "Next recommended action": "Feature teacher in Samvad exemplar list", "Owner": "Rohan", "Qwen Diagnostic": "Exemplary student practice completion (20 min/day). PoC Rohan maintains light touchpoints."},
        {"School": "GMS Central Cantonment", "Zone": "Central", "Category": "Red", "cat_bg": "#FEE2E2", "cat_col": "#991B1B", "Evidence": "Spot check mastery 28%", "Next recommended action": "Model place-value addition demonstration", "Owner": "Anshika", "Qwen Diagnostic": "Carry-over misconception in 2-digit addition. PoC Anshika runs hands-on bundle-sticks workshop."},
        {"School": "GPS Malviya Nagar", "Zone": "South", "Category": "Amber", "cat_bg": "#FEF3C7", "cat_col": "#92400E", "Evidence": "Mastery 52%, clear instructions", "Next recommended action": "Focus coaching on circulating feedback", "Owner": "Sakshi", "Qwen Diagnostic": "Teacher explains well but does not circulate. PoC Sakshi coaches on active classroom scanning."}
    ]

    active_queue = [q for q in queue_data_raw if q["Zone"] in active_zones]
    if poc_filter != "All Owners":
        active_queue = [q for q in active_queue if q["Owner"].lower() == poc_filter.lower()]

    if active_queue:
        queue_rows = []
        for q in active_queue:
            r_str = (
                f"<tr style='border-bottom:1px solid #F1F5F9;'>"
                f"<td style='padding:14px 8px 14px 0;font-weight:600;color:#0F172A;'>{q['School']}</td>"
                f"<td style='padding:14px 8px;color:#64748B;'>{q['Zone']}</td>"
                f"<td style='padding:14px 8px;'>"
                f"<span style='background:{q['cat_bg']};color:{q['cat_col']};padding:3px 10px;border-radius:999px;font-size:11px;font-weight:600;'>{q['Category']}</span>"
                f"</td>"
                f"<td style='padding:14px 8px;color:#334155;font-weight:500;'>{q['Evidence']}</td>"
                f"<td style='padding:14px 8px;color:#0F766E;font-weight:600;'>{q['Next recommended action']}</td>"
                f"<td style='padding:14px 8px;'><span style='background:#F1F5F9;color:#334155;padding:2px 8px;border-radius:6px;font-size:11px;font-weight:600;'>{q['Owner']}</span></td>"
                f"</tr>"
            )
            queue_rows.append(r_str)
        queue_rows_html = "".join(queue_rows)

        support_table_html = f"""
<div class='figma-card' style='padding:22px;'>
<div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;'>
    <h3 style='font-weight:700;color:#0F172A;font-size:16px;margin:0;'>Recommended support queue</h3>
    <span style='font-size:11px;color:#64748B;font-weight:500;'>Showing {len(active_queue)} priority schools · {zone_badge_text}</span>
</div>
<div style='overflow-x:auto;'>
<table style='width:100%;border-collapse:collapse;font-size:13px;text-align:left;'>
<thead>
<tr style='border-bottom:1px solid #E2E8F0;color:#64748B;font-size:11px;font-weight:500;'>
<th style='padding:8px 8px 12px 0;width:20%;'>School</th>
<th style='padding:8px 8px 12px 8px;width:10%;'>Zone</th>
<th style='padding:8px 8px 12px 8px;width:12%;'>Category</th>
<th style='padding:8px 8px 12px 8px;width:22%;'>Evidence</th>
<th style='padding:8px 8px 12px 8px;width:24%;'>Next recommended action</th>
<th style='padding:8px 0 12px 8px;width:12%;'>Owner</th>
</tr>
</thead>
<tbody>
{queue_rows_html}
</tbody>
</table>
</div>
</div>
"""
        render_html(support_table_html)
    else:
        st.warning("⚠️ No schools in the priority queue match the current filter combination. Please broaden your selections.")

# ------------------------------------------------------------------------------
# TAB 3: STUDENT LEARNING (FULLY DYNAMIC WITH SLICERS & FIGMA MOCKUP GEOMETRY)
# ------------------------------------------------------------------------------
with tabs[2]:
    # HEADER SECTION WITH DYNAMIC CONTEXT PILL
    st.markdown(f"""
    <div style='display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:16px;'>
        <div>
            <h2 style='font-size:24px;font-weight:700;color:#0F172A;margin:0 0 4px 0;'>Student learning</h2>
            <div style='font-size:13px;color:#64748B;font-weight:400;'>Competency mastery, misconceptions and progression across foundational literacy and numeracy</div>
        </div>
        <div style='background:#FFFFFF;border:1px solid #E2E8F0;border-radius:8px;padding:6px 14px;font-size:12px;color:#475569;font-weight:500;box-shadow:0 1px 2px rgba(0,0,0,0.04);'>
            September · Grade 3 · {zone_badge_text}
        </div>
    </div>
    """, unsafe_allow_html=True)

    if active_filters:
        st.info("🔍 **Active Slicers Applied:** " + " | ".join(active_filters))

    # STEPPED LEARNING MASTERY FLOW STRIP (MATCHING TAB 6)
    st.markdown(f"""
    <div style='display:flex;align-items:center;justify-content:space-between;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:10px;padding:8px 16px;margin-bottom:24px;font-size:12px;'>
        <div style='display:flex;align-items:center;gap:6px;'>
            <span style='font-weight:700;color:#0F172A;'>{dyn_assessed:,}</span>
            <span style='color:#64748B;'>Assessed</span>
        </div>
        <span style='color:#94A3B8;font-weight:600;'>&rarr;</span>
        <div style='display:flex;align-items:center;gap:6px;'>
            <span style='font-weight:700;color:#0F766E;'>{dyn_lit_prof}%</span>
            <span style='color:#64748B;'>Literacy FLN</span>
        </div>
        <span style='color:#94A3B8;font-weight:600;'>&rarr;</span>
        <div style='display:flex;align-items:center;gap:6px;'>
            <span style='font-weight:700;color:#0F766E;'>{dyn_num_prof}%</span>
            <span style='color:#64748B;'>Numeracy FLN</span>
        </div>
        <span style='color:#94A3B8;font-weight:600;'>&rarr;</span>
        <div style='display:flex;align-items:center;gap:6px;'>
            <span style='font-weight:700;color:#BE123C;'>{dyn_risk_pct}%</span>
            <span style='color:#64748B;'>Risk Flagged</span>
        </div>
        <span style='color:#94A3B8;font-weight:600;'>&rarr;</span>
        <div style='display:flex;align-items:center;gap:6px;'>
            <span style='font-weight:700;color:#047857;'>{dyn_remedial_pct}%</span>
            <span style='color:#64748B;'>Remedial Follow-through</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 4 DYNAMIC MINIMALIST FIGMA-GRADE KPI CARDS (MATCHING TAB 6)
    sk1, sk2, sk3, sk4 = st.columns(4)
    with sk1:
        render_html(f"""
        <div class='figma-card' style='padding:18px 20px;'>
            <div style='font-size:12px;color:#64748B;font-weight:500;margin-bottom:6px;'>Literacy proficiency</div>
            <div style='font-size:34px;font-weight:700;color:#0F172A;line-height:1.1;margin-bottom:6px;'>{dyn_lit_prof}%</div>
            <div style='font-size:12px;color:#059669;font-weight:600;'>+{dyn_lit_prof - 51} pts from baseline</div>
        </div>
        """)
    with sk2:
        render_html(f"""
        <div class='figma-card' style='padding:18px 20px;'>
            <div style='font-size:12px;color:#64748B;font-weight:500;margin-bottom:6px;'>Numeracy proficiency</div>
            <div style='font-size:34px;font-weight:700;color:#0F172A;line-height:1.1;margin-bottom:6px;'>{dyn_num_prof}%</div>
            <div style='font-size:12px;color:#059669;font-weight:600;'>+{dyn_num_prof - 46} pts from baseline</div>
        </div>
        """)
    with sk3:
        render_html(f"""
        <div class='figma-card' style='padding:18px 20px;'>
            <div style='font-size:12px;color:#64748B;font-weight:500;margin-bottom:6px;'>Students at risk</div>
            <div style='font-size:34px;font-weight:700;color:#BE123C;line-height:1.1;margin-bottom:6px;'>{dyn_risk_pct}%</div>
            <div style='font-size:12px;color:#64748B;font-weight:400;'>{dyn_assessed:,} assessed</div>
        </div>
        """)
    with sk4:
        render_html(f"""
        <div class='figma-card' style='padding:18px 20px;'>
            <div style='font-size:12px;color:#64748B;font-weight:500;margin-bottom:6px;'>Remedial follow-through</div>
            <div style='font-size:34px;font-weight:700;color:#0F172A;line-height:1.1;margin-bottom:6px;'>{dyn_remedial_pct}%</div>
            <div style='font-size:12px;color:#64748B;font-weight:400;'>Target: 80%</div>
        </div>
        """)

    st.markdown("<br>", unsafe_allow_html=True)

    # 2-COLUMN GRID: COMPETENCY MASTERY TABLE (LEFT) & MOST COMMON MISCONCEPTIONS (RIGHT)
    col_mastery, col_miscon = st.columns([1.35, 1.0])

    with col_mastery:
        # Build dynamic rows based on filtered_comps
        if filtered_comps:
            table_rows = []
            for c in filtered_comps:
                row = (
                    f"<tr style='border-bottom:1px solid #F1F5F9;'>"
                    f"<td style='padding:14px 8px 14px 0;font-weight:500;color:#0F172A;'>{c['name']}</td>"
                    f"<td style='padding:14px 16px;'>"
                    f"<div title='{c['mastery']}% Mastery' style='background:#EEF2F6;border-radius:9999px;height:10px;width:85px;overflow:hidden;box-shadow:inset 0 1px 2px rgba(0,0,0,0.04);'>"
                    f"<div style='background:#0F766E;width:{c['mastery']}%;height:100%;border-radius:9999px;'></div>"
                    f"</div>"
                    f"</td>"
                    f"<td style='padding:14px 16px;color:#475569;font-size:12px;font-weight:500;'>+{c['change']} pts</td>"
                    f"<td style='padding:14px 0 14px 16px;'>"
                    f"<span style='background:{c['bg']};color:{c['color']};padding:3px 12px;border-radius:9999px;font-size:11px;font-weight:600;display:inline-block;'>{c['priority']}</span>"
                    f"</td>"
                    f"</tr>"
                )
                table_rows.append(row)
            table_rows_str = "".join(table_rows)

            full_table_html = f"""
<div class='figma-card' style='padding:22px;'>
<div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;'>
<h3 style='font-weight:700;color:#0F172A;font-size:16px;margin:0;'>Competency mastery</h3>
<span style='font-size:11px;color:#64748B;font-weight:500;'>Showing {len(filtered_comps)} competencies ({min_m}%–{max_m}% mastery) · {zone_badge_text}</span>
</div>
<div style='overflow-x:auto;'>
<table style='width:100%;border-collapse:collapse;font-size:13px;text-align:left;'>
<thead>
<tr style='border-bottom:1px solid #E2E8F0;color:#64748B;font-size:11px;font-weight:500;'>
<th style='padding:8px 8px 12px 0;'>Competency</th>
<th style='padding:8px 16px 12px 16px;'>Mastery</th>
<th style='padding:8px 16px 12px 16px;'>Change</th>
<th style='padding:8px 0 12px 16px;'>Priority</th>
</tr>
</thead>
<tbody>
{table_rows_str}
</tbody>
</table>
</div>
</div>
"""
            render_html(full_table_html)
        else:
            no_data_html = f"""
<div class='figma-card' style='padding:22px;'>
<h3 style='font-weight:700;color:#0F172A;font-size:16px;margin:0 0 16px 0;'>Competency mastery</h3>
<div style='padding:20px;text-align:center;color:#64748B;font-size:13px;'>
⚠️ No competencies match the current filter (Mastery: {min_m}%–{max_m}% in {subject_filter}).<br>Please broaden the slider in the sidebar.
</div>
</div>
"""
            render_html(no_data_html)

    with col_miscon:
        # Dynamic Misconceptions based on selected subject
        if subject_filter == "Numeracy (Math FLN)":
            miscon_text = "Students can perform two-digit addition procedurally but frequently misplace the carry value."
            tags = ["Place value", "Carry addition", "Number line"]
            rec_text = "Recommended: model the error with bundle-sticks, use worked examples, then repeat a five-student spot check."
        elif subject_filter == "Literacy (Hindi FLN)":
            miscon_text = "Students confuse matra placement in conjunct consonants (samyuktakshar) during timed ORF reading."
            tags = ["Matra decoding", "ORF pacing", "Inference"]
            rec_text = "Recommended: sound-box phonics demonstration, paired reading practice, and 1-minute fluency spot check."
        else:
            miscon_text = "Students can perform two-digit addition procedurally but frequently misplace the carry value."
            tags = ["Place value", "ORF pacing", "Inference"]
            rec_text = "Recommended: model the error, use worked examples, then repeat a five-student spot check."

        tags_html = "".join([f"<span style='background:#F8FAFC;border:1px solid #E2E8F0;border-radius:999px;padding:3px 12px;font-size:11px;color:#475569;font-weight:500;'>{t}</span>" for t in tags])

        st.markdown(f"""
        <div class='figma-card' style='padding:22px;'>
            <h3 style='font-weight:700;color:#0F172A;font-size:16px;margin:0 0 16px 0;'>Most common misconceptions</h3>
            <div style='background:#F0FDFA;border-left:3px solid #0D9488;border-radius:4px;padding:16px;color:#0F172A;font-size:13px;line-height:1.5;margin-bottom:16px;'>
                {miscon_text}
            </div>
            <div style='display:flex;gap:8px;flex-wrap:wrap;margin-bottom:20px;'>
                {tags_html}
            </div>
            <div style='font-size:12px;color:#64748B;line-height:1.5;'>
                {rec_text}
            </div>
        </div>
        """, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# TAB 4: TEACHER PRACTICE ADOPTION (DYNAMICALLY SLICER-CONNECTED FIGMA MOCKUP)
# ------------------------------------------------------------------------------
with tabs[3]:
    # HEADER SECTION WITH DYNAMIC TOP-RIGHT INDICATOR SLICER
    col_th1, col_th2 = st.columns([2.5, 1.2])
    with col_th1:
        st.markdown(f"""
        <div style='display:flex;justify-content:space-between;align-items:flex-start;'>
            <div>
                <h2 style='font-size:24px;font-weight:700;color:#0F172A;margin:0 0 4px 0;'>Teacher practice adoption</h2>
                <div style='font-size:13px;color:#64748B;font-weight:400;'>Observed classroom practice and evidence of sustained implementation</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col_th2:
        tp_indicator_slicer = st.selectbox(
            "Filter practice indicators",
            ["All practice indicators", "Targeted instruction", "Dedicated practice time", "FA and remediation", "Classroom engagement"],
            key="tp_indicator_filter_select"
        )

    # ACTIVE CONTEXT PILL & FILTER NOTICES
    st.markdown(f"""
    <div style='display:flex;justify-content:flex-end;margin-bottom:14px;margin-top:-6px;'>
        <div style='background:#FFFFFF;border:1px solid #E2E8F0;border-radius:8px;padding:5px 14px;font-size:12px;color:#475569;font-weight:500;box-shadow:0 1px 2px rgba(0,0,0,0.04);'>
            September · Cohort 2 · {zone_badge_text} {f'· PoC: {poc_filter}' if poc_filter != 'All Owners' else ''}
        </div>
    </div>
    """, unsafe_allow_html=True)

    if active_filters:
        st.info("🔍 **Active Slicers Applied:** " + " | ".join(active_filters))

    # STEPPED PRACTICE ADOPTION FLOW STRIP (MATCHING TAB 6)
    st.markdown(f"""
    <div style='display:flex;align-items:center;justify-content:space-between;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:10px;padding:8px 16px;margin-bottom:24px;font-size:12px;'>
        <div style='display:flex;align-items:center;gap:6px;'>
            <span style='font-weight:700;color:#0F172A;'>{dyn_tp_index}%</span>
            <span style='color:#64748B;'>Practice Index</span>
        </div>
        <span style='color:#94A3B8;font-weight:600;'>&rarr;</span>
        <div style='display:flex;align-items:center;gap:6px;'>
            <span style='font-weight:700;color:#0F766E;'>{dyn_tp_ti}%</span>
            <span style='color:#64748B;'>Targeted Instruction</span>
        </div>
        <span style='color:#94A3B8;font-weight:600;'>&rarr;</span>
        <div style='display:flex;align-items:center;gap:6px;'>
            <span style='font-weight:700;color:#0F766E;'>{dyn_tp_dp}%</span>
            <span style='color:#64748B;'>Dedicated Practice</span>
        </div>
        <span style='color:#94A3B8;font-weight:600;'>&rarr;</span>
        <div style='display:flex;align-items:center;gap:6px;'>
            <span style='font-weight:700;color:#BE123C;'>{dyn_tp_fa}%</span>
            <span style='color:#64748B;'>FA & Remediation</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 4 DYNAMIC MINIMALIST FIGMA-GRADE KPI CARDS
    pk1, pk2, pk3, pk4 = st.columns(4)
    with pk1:
        render_html(f"""
        <div class='figma-card' style='padding:18px 20px;'>
            <div style='font-size:12px;color:#64748B;font-weight:500;margin-bottom:6px;'>Practice adoption index</div>
            <div style='font-size:34px;font-weight:700;color:#0F172A;line-height:1.1;margin-bottom:6px;'>{dyn_tp_index}%</div>
            <div style='font-size:12px;color:#059669;font-weight:600;'>+{dyn_tp_change} pts this cycle</div>
        </div>
        """)
    with pk2:
        render_html(f"""
        <div class='figma-card' style='padding:18px 20px;'>
            <div style='font-size:12px;color:#64748B;font-weight:500;margin-bottom:6px;'>Targeted instruction</div>
            <div style='font-size:34px;font-weight:700;color:#0F172A;line-height:1.1;margin-bottom:6px;'>{dyn_tp_ti}%</div>
            <div style='font-size:12px;color:#64748B;font-weight:400;'>Target: 75% ({dyn_tp_ti - 75:+d} pts)</div>
        </div>
        """)
    with pk3:
        render_html(f"""
        <div class='figma-card' style='padding:18px 20px;'>
            <div style='font-size:12px;color:#64748B;font-weight:500;margin-bottom:6px;'>Dedicated practice time</div>
            <div style='font-size:34px;font-weight:700;color:#0F172A;line-height:1.1;margin-bottom:6px;'>{dyn_tp_dp}%</div>
            <div style='font-size:12px;color:#64748B;font-weight:400;'>Target: 70% ({dyn_tp_dp - 70:+d} pts)</div>
        </div>
        """)
    with pk4:
        render_html(f"""
        <div class='figma-card' style='padding:18px 20px;'>
            <div style='font-size:12px;color:#64748B;font-weight:500;margin-bottom:6px;'>FA and remediation</div>
            <div style='font-size:34px;font-weight:700;color:#0F172A;line-height:1.1;margin-bottom:6px;'>{dyn_tp_fa}%</div>
            <div style='font-size:12px;color:#BE123C;font-weight:600;'>Largest gap ({dyn_tp_fa - 75:+d} pts)</div>
        </div>
        """)

    st.markdown("<br>", unsafe_allow_html=True)

    # FILTER INDICATORS BASED ON SLICER
    if tp_indicator_slicer == "All practice indicators":
        active_tp_indicators = aggregated_tp_indicators
    else:
        active_tp_indicators = [ind for ind in aggregated_tp_indicators if ind["category"] == tp_indicator_slicer]

    # DYNAMIC INDICATOR PERFORMANCE TABLE
    tp_table_rows = []
    for ind in active_tp_indicators:
        gap_display = f"+{ind['gap']} pts" if ind['gap'] > 0 else f"{ind['gap']} pts"
        row_str = (
            f"<tr style='border-bottom:1px solid #F1F5F9;'>"
            f"<td style='padding:14px 8px 14px 0;font-weight:500;color:#0F172A;'>{ind['name']}</td>"
            f"<td style='padding:14px 8px;'>"
            f"<div style='display:flex;align-items:center;gap:10px;'>"
            f"<span style='font-weight:600;color:#0F172A;min-width:34px;'>{ind['observed']}%</span>"
            f"<div title='{ind['observed']}% Observed' style='background:#EEF2F6;border-radius:9999px;height:8px;flex:1;max-width:85px;overflow:hidden;box-shadow:inset 0 1px 2px rgba(0,0,0,0.04);'>"
            f"<div style='background:#0F766E;width:{ind['observed']}%;height:100%;border-radius:9999px;'></div>"
            f"</div>"
            f"</div>"
            f"</td>"
            f"<td style='padding:14px 8px;color:#64748B;'>{ind['target']}%</td>"
            f"<td style='padding:14px 8px;color:#64748B;'>{gap_display}</td>"
            f"<td style='padding:14px 0 14px 8px;'>"
            f"<span style='background:{ind['bg']};color:{ind['color']};padding:3px 10px;border-radius:999px;font-size:11px;font-weight:600;display:inline-block;'>{ind['interpretation']}</span>"
            f"</td>"
            f"</tr>"
        )
        tp_table_rows.append(row_str)
    tp_rows_joined = "".join(tp_table_rows)

    perf_table_html = f"""
<div class='figma-card' style='padding:22px;'>
<div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;'>
<h3 style='font-weight:700;color:#0F172A;font-size:16px;margin:0;'>Indicator performance</h3>
<span style='font-size:11px;color:#64748B;font-weight:500;'>Showing {len(active_tp_indicators)} indicators · {zone_badge_text}</span>
</div>
<div style='overflow-x:auto;'>
<table style='width:100%;border-collapse:collapse;font-size:13px;text-align:left;'>
<thead>
<tr style='border-bottom:1px solid #E2E8F0;color:#64748B;font-size:11px;font-weight:500;'>
<th style='padding:8px 8px 12px 0;width:40%;'>Practice</th>
<th style='padding:8px 8px 12px 8px;width:20%;'>Observed classrooms</th>
<th style='padding:8px 8px 12px 8px;width:15%;'>Target</th>
<th style='padding:8px 8px 12px 8px;width:10%;'>Gap</th>
<th style='padding:8px 0 12px 8px;width:15%;'>Interpretation</th>
</tr>
</thead>
<tbody>
{tp_rows_joined}
</tbody>
</table>
</div>
</div>
"""
    render_html(perf_table_html)

# ------------------------------------------------------------------------------
# TAB 5: FIELD OPERATIONS (EXACT CHATGPT / FIGMA MOCKUP REPLICATION)
# ------------------------------------------------------------------------------
with tabs[4]:
    # HEADER SECTION WITH TOP-RIGHT SUPPORT REQUIRED SLICER
    col_fh1, col_fh2 = st.columns([2.5, 1.3])
    with col_fh1:
        st.markdown("""
        <div>
            <h2 style='font-size:24px;font-weight:700;color:#0F172A;margin:0 0 4px 0;'>Field operations</h2>
            <div style='font-size:13px;color:#64748B;font-weight:400;'>Planned versus achieved activity, evidence quality and workload</div>
        </div>
        """, unsafe_allow_html=True)
    with col_fh2:
        support_filter = st.selectbox(
            "Filter by Support Required",
            ["All support tiers", "On track", "Review constraints", "Coaching required"],
            key="field_support_filter_dropdown"
        )

    # CONTEXT PILL
    st.markdown(f"""
    <div style='display:flex;justify-content:flex-end;margin-bottom:14px;margin-top:-6px;'>
        <div style='background:#FFFFFF;border:1px solid #E2E8F0;border-radius:8px;padding:5px 14px;font-size:12px;color:#475569;font-weight:500;box-shadow:0 1px 2px rgba(0,0,0,0.04);'>
            Week ending 11 Sep 2026 · {zone_badge_text} {f'· PoC: {poc_filter}' if poc_filter != 'All Owners' else ''}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # TEAM EXECUTION RAW DATA (ALIGNED TO GROUND-TRUTH WEEK ENDING 11 SEP IN LEADERSHIP UPDATE)
    team_execution_master = [
        {"member": "Megha", "zone": "West", "planned": 4, "achieved": 4, "quality": "High", "support": "On track", "support_bg": "#DEF7EC", "support_color": "#03543F", "sop": 3, "pending_actions": 1, "closed_actions": 4},
        {"member": "Harshita", "zone": "Central", "planned": 4, "achieved": 2, "quality": "Medium", "support": "Review constraints", "support_bg": "#FEF3C7", "support_color": "#92400E", "sop": 1, "pending_actions": 2, "closed_actions": 2},
        {"member": "Ghazala", "zone": "Central", "planned": 1, "achieved": 1, "quality": "Low", "support": "Coaching", "support_bg": "#FEE2E2", "support_color": "#991B1B", "sop": 0, "pending_actions": 1, "closed_actions": 1},
        {"member": "Geeta", "zone": "Central", "planned": 4, "achieved": 4, "quality": "High", "support": "On track", "support_bg": "#DEF7EC", "support_color": "#03543F", "sop": 3, "pending_actions": 1, "closed_actions": 4},
        {"member": "Sakshi", "zone": "South", "planned": 3, "achieved": 3, "quality": "High", "support": "On track", "support_bg": "#DEF7EC", "support_color": "#03543F", "sop": 2, "pending_actions": 1, "closed_actions": 3},
        {"member": "Swagata", "zone": "West", "planned": 4, "achieved": 3, "quality": "High", "support": "On track", "support_bg": "#DEF7EC", "support_color": "#03543F", "sop": 2, "pending_actions": 1, "closed_actions": 3},
        {"member": "Anshika", "zone": "Civil", "planned": 3, "achieved": 2, "quality": "Medium", "support": "Review constraints", "support_bg": "#FEF3C7", "support_color": "#92400E", "sop": 1, "pending_actions": 2, "closed_actions": 2},
        {"member": "Malya", "zone": "West", "planned": 3, "achieved": 3, "quality": "High", "support": "On track", "support_bg": "#DEF7EC", "support_color": "#03543F", "sop": 2, "pending_actions": 1, "closed_actions": 3},
        {"member": "Sheetal", "zone": "South", "planned": 3, "achieved": 2, "quality": "Medium", "support": "Review constraints", "support_bg": "#FEF3C7", "support_color": "#92400E", "sop": 1, "pending_actions": 1, "closed_actions": 2},
        {"member": "Riya", "zone": "Civil", "planned": 2, "achieved": 1, "quality": "Low", "support": "Coaching", "support_bg": "#FEE2E2", "support_color": "#991B1B", "sop": 1, "pending_actions": 1, "closed_actions": 1},
        {"member": "Anchal", "zone": "South", "planned": 3, "achieved": 3, "quality": "High", "support": "On track", "support_bg": "#DEF7EC", "support_color": "#03543F", "sop": 2, "pending_actions": 1, "closed_actions": 3},
        {"member": "Veena", "zone": "Civil", "planned": 2, "achieved": 2, "quality": "High", "support": "On track", "support_bg": "#DEF7EC", "support_color": "#03543F", "sop": 1, "pending_actions": 1, "closed_actions": 2},
        {"member": "Manish", "zone": "West", "planned": 1, "achieved": 1, "quality": "Medium", "support": "On track", "support_bg": "#DEF7EC", "support_color": "#03543F", "sop": 1, "pending_actions": 0, "closed_actions": 1},
        {"member": "Shalini", "zone": "South", "planned": 1, "achieved": 0, "quality": "Low", "support": "Coaching", "support_bg": "#FEE2E2", "support_color": "#991B1B", "sop": 0, "pending_actions": 1, "closed_actions": 0},
        {"member": "Aditya", "zone": "Civil", "planned": 1, "achieved": 0, "quality": "Medium", "support": "Review constraints", "support_bg": "#FEF3C7", "support_color": "#92400E", "sop": 0, "pending_actions": 1, "closed_actions": 0},
        {"member": "Kavya", "zone": "Central", "planned": 1, "achieved": 1, "quality": "High", "support": "On track", "support_bg": "#DEF7EC", "support_color": "#03543F", "sop": 1, "pending_actions": 0, "closed_actions": 1},
        {"member": "Keerthi", "zone": "South", "planned": 2, "achieved": 2, "quality": "High", "support": "On track", "support_bg": "#DEF7EC", "support_color": "#03543F", "sop": 1, "pending_actions": 0, "closed_actions": 2},
    ]

    # FILTER BY ACTIVE ZONES & POC OWNER SLICERS
    active_team = [m for m in team_execution_master if m["zone"] in active_zones]
    if poc_filter != "All Owners":
        active_team = [m for m in active_team if m["member"].lower() == poc_filter.lower()]

    # FILTER BY SUPPORT REQUIRED SLICER
    if support_filter == "On track":
        active_team = [m for m in active_team if m["support"] == "On track"]
    elif support_filter == "Review constraints":
        active_team = [m for m in active_team if m["support"] == "Review constraints"]
    elif support_filter == "Coaching required":
        active_team = [m for m in active_team if m["support"] == "Coaching"]

    field_filters = list(active_filters)
    if support_filter != "All support tiers":
        field_filters.append(f"Support Required: **{support_filter}**")

    if field_filters:
        st.info("🔍 **Active Slicers Applied:** " + " | ".join(field_filters))

    # DYNAMIC KPI CALCULATIONS
    dyn_field_planned = sum(m["planned"] for m in active_team)
    dyn_field_achieved = sum(m["achieved"] for m in active_team)
    dyn_field_achieve_pct = round((dyn_field_achieved / dyn_field_planned * 100)) if dyn_field_planned > 0 else 0
    dyn_field_sop = sum(m["sop"] for m in active_team)
    dyn_field_closed = sum(m["closed_actions"] for m in active_team)
    dyn_field_pending = sum(m["pending_actions"] for m in active_team)
    dyn_field_total_actions = dyn_field_closed + dyn_field_pending
    dyn_field_closed_pct = round((dyn_field_closed / dyn_field_total_actions * 100)) if dyn_field_total_actions > 0 else 67

    # STEPPED FIELD EXECUTION FLOW STRIP (MATCHING TAB 6)
    st.markdown(f"""
    <div style='display:flex;align-items:center;justify-content:space-between;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:10px;padding:8px 16px;margin-bottom:24px;font-size:12px;'>
        <div style='display:flex;align-items:center;gap:6px;'>
            <span style='font-weight:700;color:#0F172A;'>{dyn_field_planned}</span>
            <span style='color:#64748B;'>Planned Visits</span>
        </div>
        <span style='color:#94A3B8;font-weight:600;'>&rarr;</span>
        <div style='display:flex;align-items:center;gap:6px;'>
            <span style='font-weight:700;color:#0F766E;'>{dyn_field_achieved}</span>
            <span style='color:#64748B;'>Achieved ({dyn_field_achieve_pct}%)</span>
        </div>
        <span style='color:#94A3B8;font-weight:600;'>&rarr;</span>
        <div style='display:flex;align-items:center;gap:6px;'>
            <span style='font-weight:700;color:#0F766E;'>{dyn_field_sop}</span>
            <span style='color:#64748B;'>Schools with SoP</span>
        </div>
        <span style='color:#94A3B8;font-weight:600;'>&rarr;</span>
        <div style='display:flex;align-items:center;gap:6px;'>
            <span style='font-weight:700;color:#047857;'>{dyn_field_closed_pct}%</span>
            <span style='color:#64748B;'>Actions Closed ({dyn_field_pending} pending)</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 4 DYNAMIC FIGMA-GRADE KPI CARDS (EXACT MATCH TO SCREENSHOT)
    fk1, fk2, fk3, fk4 = st.columns(4)
    with fk1:
        render_html(f"""
        <div class='figma-card' style='padding:18px 20px;'>
            <div style='font-size:12px;color:#64748B;font-weight:500;margin-bottom:6px;'>Visits planned</div>
            <div style='font-size:34px;font-weight:700;color:#0F172A;line-height:1.1;margin-bottom:6px;'>{dyn_field_planned}</div>
            <div style='font-size:12px;color:#64748B;font-weight:400;'>{'All team members' if len(active_team) > 1 else f'PoC {active_team[0]["member"]}'}</div>
        </div>
        """)
    with fk2:
        render_html(f"""
        <div class='figma-card' style='padding:18px 20px;'>
            <div style='font-size:12px;color:#64748B;font-weight:500;margin-bottom:6px;'>Visits achieved</div>
            <div style='font-size:34px;font-weight:700;color:#0F172A;line-height:1.1;margin-bottom:6px;'>{dyn_field_achieved}</div>
            <div style='font-size:12px;color:#059669;font-weight:600;'>{dyn_field_achieve_pct}% achievement</div>
        </div>
        """)
    with fk3:
        render_html(f"""
        <div class='figma-card' style='padding:18px 20px;'>
            <div style='font-size:12px;color:#64748B;font-weight:500;margin-bottom:6px;'>Schools with SoP</div>
            <div style='font-size:34px;font-weight:700;color:#0F172A;line-height:1.1;margin-bottom:6px;'>{dyn_field_sop}</div>
            <div style='font-size:12px;color:#64748B;font-weight:400;'>Evidence of practice</div>
        </div>
        """)
    with fk4:
        render_html(f"""
        <div class='figma-card' style='padding:18px 20px;'>
            <div style='font-size:12px;color:#64748B;font-weight:500;margin-bottom:6px;'>Actions closed</div>
            <div style='font-size:34px;font-weight:700;color:#0F172A;line-height:1.1;margin-bottom:6px;'>{dyn_field_closed_pct}%</div>
            <div style='font-size:12px;color:#64748B;font-weight:400;'>{dyn_field_pending} pending</div>
        </div>
        """)

    st.markdown("<br>", unsafe_allow_html=True)

    # TEAM EXECUTION TABLE (EXACT MATCH TO FIGMA / CHATGPT SCREENSHOT)
    if active_team:
        team_rows_list = []
        for m in active_team:
            ach_pct_m = round((m['achieved'] / m['planned'] * 100)) if m['planned'] > 0 else 0
            bar_color = "#0F766E" if ach_pct_m >= 100 else ("#D97706" if ach_pct_m >= 50 else "#DC2626")
            row = (
                f"<tr style='border-bottom:1px solid #F1F5F9;'>"
                f"<td style='padding:14px 8px 14px 0;font-weight:500;color:#0F172A;'>{m['member']}</td>"
                f"<td style='padding:14px 8px;color:#64748B;font-weight:400;'>{m['zone']}</td>"
                f"<td style='padding:14px 8px;color:#64748B;font-weight:500;'>{m['planned']}</td>"
                f"<td style='padding:14px 8px;'>"
                f"<div style='display:flex;align-items:center;gap:8px;'>"
                f"<span style='font-weight:600;color:#0F172A;min-width:14px;'>{m['achieved']}</span>"
                f"<div title='{ach_pct_m}% Achieved' style='background:#EEF2F6;border-radius:9999px;height:7px;width:55px;overflow:hidden;box-shadow:inset 0 1px 2px rgba(0,0,0,0.04);'>"
                f"<div style='background:{bar_color};width:{min(ach_pct_m, 100)}%;height:100%;border-radius:9999px;'></div>"
                f"</div>"
                f"</div>"
                f"</td>"
                f"<td style='padding:14px 8px;color:#475569;font-weight:500;'>{m['quality']}</td>"
                f"<td style='padding:14px 0 14px 8px;'>"
                f"<span style='background:{m['support_bg']};color:{m['support_color']};padding:3px 12px;border-radius:999px;font-size:11px;font-weight:600;display:inline-block;'>{m['support']}</span>"
                f"</td>"
                f"</tr>"
            )
            team_rows_list.append(row)
        team_rows_str = "".join(team_rows_list)

        team_table_html = f"""
<div class='figma-card' style='padding:22px;'>
<div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;'>
<h3 style='font-weight:700;color:#0F172A;font-size:16px;margin:0;'>Team execution</h3>
<span style='font-size:11px;color:#64748B;font-weight:500;'>Showing {len(active_team)} team members · Filter: {support_filter} · {zone_badge_text}</span>
</div>
<div style='overflow-x:auto;'>
<table style='width:100%;border-collapse:collapse;font-size:13px;text-align:left;'>
<thead>
<tr style='border-bottom:1px solid #E2E8F0;color:#64748B;font-size:11px;font-weight:500;'>
<th style='padding:8px 8px 12px 0;width:24%;'>Team member</th>
<th style='padding:8px 8px 12px 8px;width:15%;'>Zone</th>
<th style='padding:8px 8px 12px 8px;width:12%;'>Planned</th>
<th style='padding:8px 8px 12px 8px;width:12%;'>Achieved</th>
<th style='padding:8px 8px 12px 8px;width:18%;'>Evidence quality</th>
<th style='padding:8px 0 12px 8px;width:19%;'>Support</th>
</tr>
</thead>
<tbody>
{team_rows_str}
</tbody>
</table>
</div>
</div>
"""
        render_html(team_table_html)
    else:
        empty_html = f"""
<div class='figma-card' style='padding:22px;'>
<h3 style='font-weight:700;color:#0F172A;font-size:16px;margin:0 0 16px 0;'>Team execution</h3>
<div style='padding:20px;text-align:center;color:#64748B;font-size:13px;'>
⚠️ No team members match the current filter combination (Support: {support_filter} in {zone_badge_text}).<br>Please select 'All support tiers' or broaden your zone filter.
</div>
</div>
"""
        render_html(empty_html)

# ------------------------------------------------------------------------------
# TAB 6: COMPETENCY PACK ANALYTICS (EXACT CHATGPT / FIGMA MOCKUP REPLICATION)
# ------------------------------------------------------------------------------
with tabs[5]:
    # HEADER SECTION WITH TOP-RIGHT PACK SLICER
    col_cph1, col_cph2 = st.columns([2.5, 1.4])
    with col_cph1:
        st.markdown("""
        <div>
            <h2 style='font-size:24px;font-weight:700;color:#0F172A;margin:0 0 4px 0;'>Competency pack analytics</h2>
            <div style='font-size:13px;color:#64748B;font-weight:400;'>From dissemination to classroom adoption and student mastery</div>
        </div>
        """, unsafe_allow_html=True)
    with col_cph2:
        pack_filter = st.selectbox(
            "Select Competency Pack",
            [
                "September · Number Operations + ORF",
                "August · Word Reading & Place Value",
                "October · Reading Comprehension & Multi-digit Operations",
                "All Competency Packs"
            ],
            key="comp_pack_dropdown"
        )

    # ACTIVE SLICERS INFO
    pack_filters = list(active_filters)
    if pack_filter != "September · Number Operations + ORF":
        pack_filters.append(f"Pack: **{pack_filter}**")

    if pack_filters:
        st.info("🔍 **Active Slicers Applied:** " + " | ".join(pack_filters))

    # DYNAMIC METRIC AGGREGATIONS BASED ON pack_filter & active_zones
    if pack_filter == "All Competency Packs":
        dyn_pack_schools = sum(z_data["schools"] for p in ALL_PACK_DATA.values() for z, z_data in p["zones"].items() if z in active_zones)
        dyn_pack_received = sum(z_data["received"] for p in ALL_PACK_DATA.values() for z, z_data in p["zones"].items() if z in active_zones)
        dyn_pack_engaged = sum(z_data["engaged"] for p in ALL_PACK_DATA.values() for z, z_data in p["zones"].items() if z in active_zones)
        dyn_pack_implemented = sum(z_data["implemented"] for p in ALL_PACK_DATA.values() for z, z_data in p["zones"].items() if z in active_zones)
        dyn_pack_mastery = sum(z_data["mastery"] for p in ALL_PACK_DATA.values() for z, z_data in p["zones"].items() if z in active_zones)

        weighted_adopt_sum = sum(z_data["adoption_pct"] * z_data["schools"] for p in ALL_PACK_DATA.values() for z, z_data in p["zones"].items() if z in active_zones)
        dyn_classroom_adopt = round(weighted_adopt_sum / dyn_pack_schools) if dyn_pack_schools > 0 else 54

        active_competencies = [comp for p in ALL_PACK_DATA.values() for comp in p["competencies"]]
        pack_scope_label = "All 3 Competency Packs Cumulative"
    else:
        pack_obj = ALL_PACK_DATA[pack_filter]
        pack_zones = pack_obj["zones"]
        dyn_pack_schools = sum(pack_zones[z]["schools"] for z in active_zones if z in pack_zones)
        dyn_pack_received = sum(pack_zones[z]["received"] for z in active_zones if z in pack_zones)
        dyn_pack_engaged = sum(pack_zones[z]["engaged"] for z in active_zones if z in pack_zones)
        dyn_pack_implemented = sum(pack_zones[z]["implemented"] for z in active_zones if z in pack_zones)
        dyn_pack_mastery = sum(pack_zones[z]["mastery"] for z in active_zones if z in pack_zones)

        weighted_adopt_sum = sum(pack_zones[z]["adoption_pct"] * pack_zones[z]["schools"] for z in active_zones if z in pack_zones)
        dyn_classroom_adopt = round(weighted_adopt_sum / dyn_pack_schools) if dyn_pack_schools > 0 else 57

        active_competencies = list(pack_obj["competencies"])
        pack_scope_label = pack_filter.split("·")[0].strip() + " Cohort Scope"

    # Filter competencies if Subject slicer is applied
    if subject_filter != "All Subjects":
        active_competencies = [c for c in active_competencies if c["subject"] == subject_filter]

    dyn_teachers_reached = round(dyn_pack_engaged / dyn_pack_schools * 100) if dyn_pack_schools > 0 else 0
    dyn_material_eng = round(dyn_pack_implemented / dyn_pack_schools * 100) if dyn_pack_schools > 0 else 0
    dyn_student_mastery = round(dyn_pack_mastery / dyn_pack_schools * 100) if dyn_pack_schools > 0 else 0

    # 4 MINIMALIST FIGMA-GRADE KPI CARDS (EXACT MATCH TO CHATGPT / FIGMA SCREENSHOT)
    cp1, cp2, cp3, cp4 = st.columns(4)
    with cp1:
        render_html(f"""
        <div class='figma-card' style='padding:18px 20px;'>
            <div style='font-size:12px;color:#64748B;font-weight:500;margin-bottom:6px;'>Teachers reached</div>
            <div style='font-size:34px;font-weight:700;color:#0F172A;line-height:1.1;margin-bottom:6px;'>{dyn_teachers_reached}%</div>
            <div style='font-size:12px;color:#059669;font-weight:500;'>Across active schools</div>
        </div>
        """)
    with cp2:
        render_html(f"""
        <div class='figma-card' style='padding:18px 20px;'>
            <div style='font-size:12px;color:#64748B;font-weight:500;margin-bottom:6px;'>Material engagement</div>
            <div style='font-size:34px;font-weight:700;color:#0F172A;line-height:1.1;margin-bottom:6px;'>{dyn_material_eng}%</div>
            <div style='font-size:12px;color:#059669;font-weight:500;'>Self-reported</div>
        </div>
        """)
    with cp3:
        render_html(f"""
        <div class='figma-card' style='padding:18px 20px;'>
            <div style='font-size:12px;color:#64748B;font-weight:500;margin-bottom:6px;'>Classroom adoption</div>
            <div style='font-size:34px;font-weight:700;color:#0F172A;line-height:1.1;margin-bottom:6px;'>{dyn_classroom_adopt}%</div>
            <div style='font-size:12px;color:#059669;font-weight:500;'>Observed</div>
        </div>
        """)
    with cp4:
        render_html(f"""
        <div class='figma-card' style='padding:18px 20px;'>
            <div style='font-size:12px;color:#64748B;font-weight:500;margin-bottom:6px;'>Student mastery</div>
            <div style='font-size:34px;font-weight:700;color:#0F172A;line-height:1.1;margin-bottom:6px;'>{dyn_student_mastery}%</div>
            <div style='font-size:12px;color:#059669;font-weight:500;'>Spot checks</div>
        </div>
        """)

    st.markdown("<br>", unsafe_allow_html=True)

    # COMPETENCY PACK CONVERSION FUNNEL CARD (EXECUTIVE AGENCY DESIGN)
    max_val = max(dyn_pack_received, 1)
    h_rec = max(int(180 * (dyn_pack_received / max_val)), 24)
    h_eng = max(int(180 * (dyn_pack_engaged / max_val)), 24)
    h_imp = max(int(180 * (dyn_pack_implemented / max_val)), 24)
    h_mas = max(int(180 * (dyn_pack_mastery / max_val)), 24)

    pct_eng = round(dyn_pack_engaged / dyn_pack_received * 100) if dyn_pack_received > 0 else 0
    pct_imp = round(dyn_pack_implemented / dyn_pack_received * 100) if dyn_pack_received > 0 else 0
    pct_mas = round(dyn_pack_mastery / dyn_pack_received * 100) if dyn_pack_received > 0 else 0

    funnel_html = f"""
<div class='figma-card' style='padding:26px 28px;'>
<div style='display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:20px;'>
<div>
    <h3 style='font-weight:700;color:#0F172A;font-size:16px;margin:0 0 4px 0;'>Competency pack conversion funnel</h3>
    <div style='font-size:12px;color:#64748B;'>Throughput from school dissemination to validated student mastery</div>
</div>
<div style='display:flex;align-items:center;gap:10px;'>
    <div style='background:#F0FDFA;border:1px solid #CCFBF1;color:#0F766E;padding:4px 12px;border-radius:999px;font-size:11px;font-weight:600;'>
        Funnel Retention: {pct_mas}%
    </div>
    <span style='font-size:12px;color:#64748B;font-weight:500;'>{zone_badge_text} · {pack_scope_label}</span>
</div>
</div>

<!-- STEPPED FLOW BADGES -->
<div style='display:flex;align-items:center;justify-content:space-between;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:10px;padding:8px 16px;margin-bottom:24px;font-size:12px;'>
    <div style='display:flex;align-items:center;gap:6px;'>
        <span style='font-weight:700;color:#0F172A;'>100%</span>
        <span style='color:#64748B;'>Disseminated</span>
    </div>
    <span style='color:#94A3B8;font-weight:600;'>&rarr;</span>
    <div style='display:flex;align-items:center;gap:6px;'>
        <span style='font-weight:700;color:#0F766E;'>{pct_eng}%</span>
        <span style='color:#64748B;'>Engaged</span>
    </div>
    <span style='color:#94A3B8;font-weight:600;'>&rarr;</span>
    <div style='display:flex;align-items:center;gap:6px;'>
        <span style='font-weight:700;color:#0F766E;'>{pct_imp}%</span>
        <span style='color:#64748B;'>Implemented</span>
    </div>
    <span style='color:#94A3B8;font-weight:600;'>&rarr;</span>
    <div style='display:flex;align-items:center;gap:6px;'>
        <span style='font-weight:700;color:#047857;'>{pct_mas}%</span>
        <span style='color:#64748B;'>Mastered</span>
    </div>
</div>

<!-- FUNNEL COLUMNS WITH MULTI-STOP GRADIENTS & ELEVATED SHADOWS -->
<div style='display:flex;align-items:flex-end;justify-content:space-between;gap:20px;height:240px;padding-bottom:12px;border-bottom:1px solid #E2E8F0;'>
<div style='flex:1;display:flex;flex-direction:column;align-items:center;height:100%;justify-content:flex-end;'>
    <div style='font-weight:700;color:#0F172A;font-size:14px;margin-bottom:8px;'>{dyn_pack_received:,}</div>
    <div title='Received: {dyn_pack_received:,} schools' style='background:linear-gradient(180deg, #A7F3D0 0%, #5EEAD4 40%, #14B8A6 100%);width:100%;height:{h_rec}px;border-top-left-radius:10px;border-top-right-radius:10px;box-shadow:0 4px 14px -2px rgba(20, 184, 166, 0.3);transition:all 0.3s cubic-bezier(0.4, 0, 0.2, 1);'></div>
</div>
<div style='flex:1;display:flex;flex-direction:column;align-items:center;height:100%;justify-content:flex-end;'>
    <div style='font-weight:700;color:#0F172A;font-size:14px;margin-bottom:8px;'>{dyn_pack_engaged:,}</div>
    <div title='Engaged: {dyn_pack_engaged:,} schools ({pct_eng}%)' style='background:linear-gradient(180deg, #5EEAD4 0%, #2DD4BF 40%, #0D9488 100%);width:100%;height:{h_eng}px;border-top-left-radius:10px;border-top-right-radius:10px;box-shadow:0 4px 14px -2px rgba(13, 148, 136, 0.3);transition:all 0.3s cubic-bezier(0.4, 0, 0.2, 1);'></div>
</div>
<div style='flex:1;display:flex;flex-direction:column;align-items:center;height:100%;justify-content:flex-end;'>
    <div style='font-weight:700;color:#0F172A;font-size:14px;margin-bottom:8px;'>{dyn_pack_implemented:,}</div>
    <div title='Implemented: {dyn_pack_implemented:,} schools ({pct_imp}%)' style='background:linear-gradient(180deg, #2DD4BF 0%, #14B8A6 40%, #0F766E 100%);width:100%;height:{h_imp}px;border-top-left-radius:10px;border-top-right-radius:10px;box-shadow:0 4px 14px -2px rgba(15, 118, 110, 0.35);transition:all 0.3s cubic-bezier(0.4, 0, 0.2, 1);'></div>
</div>
<div style='flex:1;display:flex;flex-direction:column;align-items:center;height:100%;justify-content:flex-end;'>
    <div style='font-weight:700;color:#0F172A;font-size:14px;margin-bottom:8px;'>{dyn_pack_mastery:,}</div>
    <div title='Mastery evidence: {dyn_pack_mastery:,} schools ({pct_mas}%)' style='background:linear-gradient(180deg, #14B8A6 0%, #0D9488 40%, #115E59 100%);width:100%;height:{h_mas}px;border-top-left-radius:10px;border-top-right-radius:10px;box-shadow:0 4px 14px -2px rgba(17, 94, 89, 0.4);transition:all 0.3s cubic-bezier(0.4, 0, 0.2, 1);'></div>
</div>
</div>
<div style='display:flex;justify-content:space-between;gap:20px;margin-top:14px;text-align:center;'>
<div style='flex:1;'>
    <div style='font-size:12px;color:#0F172A;font-weight:600;'>Received</div>
    <div style='font-size:11px;color:#64748B;'>100% of schools</div>
</div>
<div style='flex:1;'>
    <div style='font-size:12px;color:#0F172A;font-weight:600;'>Engaged</div>
    <div style='font-size:11px;color:#0F766E;font-weight:500;'>{pct_eng}% retention</div>
</div>
<div style='flex:1;'>
    <div style='font-size:12px;color:#0F172A;font-weight:600;'>Implemented</div>
    <div style='font-size:11px;color:#0F766E;font-weight:500;'>{pct_imp}% retention</div>
</div>
<div style='flex:1;'>
    <div style='font-size:12px;color:#0F172A;font-weight:600;'>Mastery evidence</div>
    <div style='font-size:11px;color:#047857;font-weight:600;'>{pct_mas}% achieved</div>
</div>
</div>
</div>
"""
    render_html(funnel_html)

    st.markdown("<br>", unsafe_allow_html=True)

    # COMPETENCY FOCUS & EXECUTION TABLE
    if active_competencies:
        comp_rows_list = []
        for c in active_competencies:
            row = (
                f"<tr style='border-bottom:1px solid #F1F5F9;'>"
                f"<td style='padding:14px 8px 14px 0;font-weight:500;color:#0F172A;'>{c['name']}</td>"
                f"<td style='padding:14px 8px;color:#64748B;font-weight:400;'>{c['subject']}</td>"
                f"<td style='padding:14px 8px;color:#0F172A;font-weight:600;'>{c['reach']}</td>"
                f"<td style='padding:14px 8px;color:#0F172A;font-weight:600;'>{c['practice']}</td>"
                f"<td style='padding:14px 8px;color:#0F172A;font-weight:600;'>{c['mastery']}</td>"
                f"<td style='padding:14px 0 14px 8px;'>"
                f"<span style='background:{c['status_bg']};color:{c['status_color']};padding:3px 12px;border-radius:999px;font-size:11px;font-weight:600;display:inline-block;'>{c['status']}</span>"
                f"</td>"
                f"</tr>"
            )
            comp_rows_list.append(row)
        comp_rows_str = "".join(comp_rows_list)

        comp_table_html = f"""
<div class='figma-card' style='padding:22px;'>
<div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;'>
<h3 style='font-weight:700;color:#0F172A;font-size:16px;margin:0;'>Competency focus in selected pack</h3>
<span style='font-size:11px;color:#64748B;font-weight:500;'>Showing {len(active_competencies)} competencies · {zone_badge_text}</span>
</div>
<div style='overflow-x:auto;'>
<table style='width:100%;border-collapse:collapse;font-size:13px;text-align:left;'>
<thead>
<tr style='border-bottom:1px solid #E2E8F0;color:#64748B;font-size:11px;font-weight:500;'>
<th style='padding:8px 8px 12px 0;width:35%;'>Competency Area</th>
<th style='padding:8px 8px 12px 8px;width:15%;'>Subject</th>
<th style='padding:8px 8px 12px 8px;width:12%;'>Reach</th>
<th style='padding:8px 8px 12px 8px;width:12%;'>Practice</th>
<th style='padding:8px 8px 12px 8px;width:12%;'>Mastery</th>
<th style='padding:8px 0 12px 8px;width:14%;'>Cycle Status</th>
</tr>
</thead>
<tbody>
{comp_rows_str}
</tbody>
</table>
</div>
</div>
"""
        render_html(comp_table_html)

# ------------------------------------------------------------------------------
# TAB 7: IMPACT AND EVALUATION (EXACT CHATGPT / FIGMA MOCKUP REPLICATION)
# ------------------------------------------------------------------------------
with tabs[6]:
    # HEADER SECTION WITH TOP-RIGHT EVALUATION WINDOW SLICER
    col_ih1, col_ih2 = st.columns([2.5, 1.4])
    with col_ih1:
        st.markdown("""
        <div>
            <h2 style='font-size:24px;font-weight:700;color:#0F172A;margin:0 0 4px 0;'>Impact and evaluation</h2>
            <div style='font-size:13px;color:#64748B;font-weight:400;'>Outcome trends and pathways from support to learning</div>
        </div>
        """, unsafe_allow_html=True)
    with col_ih2:
        eval_window = st.selectbox(
            "Evaluation Window",
            [
                "Baseline to current",
                "Cycle 1 to Cycle 2",
                "Projected endline"
            ],
            key="eval_window_dropdown"
        )

    # ACTIVE SLICERS INFO
    impact_filters = list(active_filters)
    if eval_window != "Baseline to current":
        impact_filters.append(f"Window: **{eval_window}**")

    if impact_filters:
        st.info("🔍 **Active Slicers Applied:** " + " | ".join(impact_filters))

    # ACTIVE IMPACT WINDOW OBJECT
    active_impact = ALL_IMPACT_DATA[eval_window]
    active_impact_zones = active_impact["zones"]
    active_pathway_changes = active_impact["pathway_changes"]
    active_equity = active_impact["equity"]

    # DYNAMIC METRIC AGGREGATIONS ACROSS ACTIVE ZONES & SELECTED EVALUATION WINDOW
    dyn_imp_schools = sum(active_impact_zones[z]["schools"] for z in active_zones if z in active_impact_zones)
    dyn_school_imp = sum(active_impact_zones[z]["school_imp"] for z in active_zones if z in active_impact_zones)

    if dyn_imp_schools > 0:
        dyn_learning_gain = round(sum(active_impact_zones[z]["learning_gain"] * active_impact_zones[z]["schools"] for z in active_zones if z in active_impact_zones) / dyn_imp_schools, 1)
        dyn_adoption_gain = round(sum(active_impact_zones[z]["adoption_gain"] * active_impact_zones[z]["schools"] for z in active_zones if z in active_impact_zones) / dyn_imp_schools)
        dyn_confidence = round(sum(active_impact_zones[z]["confidence"] * active_impact_zones[z]["schools"] for z in active_zones if z in active_impact_zones) / dyn_imp_schools)
        dyn_support_rate = round(sum(active_impact_zones[z]["support_rate"] * active_impact_zones[z]["schools"] for z in active_zones if z in active_impact_zones) / dyn_imp_schools)
        dyn_practice_rate = round(sum(active_impact_zones[z]["practice_rate"] * active_impact_zones[z]["schools"] for z in active_zones if z in active_impact_zones) / dyn_imp_schools)
        dyn_student_prac_rate = round(sum(active_impact_zones[z]["student_prac_rate"] * active_impact_zones[z]["schools"] for z in active_zones if z in active_impact_zones) / dyn_imp_schools)
        dyn_mastery_rate = round(sum(active_impact_zones[z]["mastery_rate"] * active_impact_zones[z]["schools"] for z in active_zones if z in active_impact_zones) / dyn_imp_schools)
    else:
        dyn_learning_gain, dyn_adoption_gain, dyn_confidence = 6.1, 9, 72
        dyn_support_rate, dyn_practice_rate, dyn_student_prac_rate, dyn_mastery_rate = 86, 64, 58, 51

    # STEPPED PROGRAMME PATHWAY STRIP (MATCHING TAB 6)
    st.markdown(f"""
    <div style='display:flex;align-items:center;justify-content:space-between;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:10px;padding:8px 16px;margin-bottom:24px;font-size:12px;'>
        <div style='display:flex;align-items:center;gap:6px;'>
            <span style='font-weight:700;color:#0F172A;'>{dyn_support_rate}%</span>
            <span style='color:#64748B;'>Support Dosage</span>
        </div>
        <span style='color:#94A3B8;font-weight:600;'>&rarr;</span>
        <div style='display:flex;align-items:center;gap:6px;'>
            <span style='font-weight:700;color:#0F766E;'>{dyn_practice_rate}%</span>
            <span style='color:#64748B;'>Teacher Practice</span>
        </div>
        <span style='color:#94A3B8;font-weight:600;'>&rarr;</span>
        <div style='display:flex;align-items:center;gap:6px;'>
            <span style='font-weight:700;color:#0F766E;'>{dyn_student_prac_rate}%</span>
            <span style='color:#64748B;'>Student Practice</span>
        </div>
        <span style='color:#94A3B8;font-weight:600;'>&rarr;</span>
        <div style='display:flex;align-items:center;gap:6px;'>
            <span style='font-weight:700;color:#047857;'>{dyn_mastery_rate}%</span>
            <span style='color:#64748B;'>Competency Mastery</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 4 MINIMALIST FIGMA-GRADE KPI CARDS (EXACT MATCH TO SCREENSHOT & DYNAMIC)
    ik1, ik2, ik3, ik4 = st.columns(4)
    with ik1:
        render_html(f"""
        <div class='figma-card' style='padding:18px 20px;'>
            <div style='font-size:12px;color:#64748B;font-weight:500;margin-bottom:6px;'>Learning gain</div>
            <div style='font-size:34px;font-weight:700;color:#0F172A;line-height:1.1;margin-bottom:6px;'>+{dyn_learning_gain} pts</div>
            <div style='font-size:12px;color:#059669;font-weight:500;'>Weighted across competencies</div>
        </div>
        """)
    with ik2:
        render_html(f"""
        <div class='figma-card' style='padding:18px 20px;'>
            <div style='font-size:12px;color:#64748B;font-weight:500;margin-bottom:6px;'>School improvement</div>
            <div style='font-size:34px;font-weight:700;color:#0F172A;line-height:1.1;margin-bottom:6px;'>{dyn_school_imp}</div>
            <div style='font-size:12px;color:#059669;font-weight:500;'>Category movement</div>
        </div>
        """)
    with ik3:
        render_html(f"""
        <div class='figma-card' style='padding:18px 20px;'>
            <div style='font-size:12px;color:#64748B;font-weight:500;margin-bottom:6px;'>Teacher adoption gain</div>
            <div style='font-size:34px;font-weight:700;color:#0F172A;line-height:1.1;margin-bottom:6px;'>+{dyn_adoption_gain} pts</div>
            <div style='font-size:12px;color:#059669;font-weight:500;'>{eval_window.lower()}</div>
        </div>
        """)
    with ik4:
        render_html(f"""
        <div class='figma-card' style='padding:18px 20px;'>
            <div style='font-size:12px;color:#64748B;font-weight:500;margin-bottom:6px;'>Evidence confidence</div>
            <div style='font-size:34px;font-weight:700;color:#0F172A;line-height:1.1;margin-bottom:6px;'>{dyn_confidence}%</div>
            <div style='font-size:12px;color:#059669;font-weight:500;'>Triangulated records</div>
        </div>
        """)

    st.markdown("<br>", unsafe_allow_html=True)

    # TWO-COLUMN LAYOUT: PROGRAMME THEORY PATHWAY & EQUITY LENS
    col_pathway, col_equity = st.columns([1.65, 1.15])

    with col_pathway:
        pathway_html = f"""
<div class='figma-card' style='padding:24px;'>
<div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:14px;'>
    <h3 style='font-weight:700;color:#0F172A;font-size:16px;margin:0;'>Programme theory pathway</h3>
    <span style='font-size:11px;background:#F1F5F9;color:#475569;padding:3px 10px;border-radius:999px;font-weight:600;'>{eval_window}</span>
</div>
<div style='background:#F0FDFA;border-left:4px solid #0F766E;border-radius:6px;padding:12px 16px;margin-bottom:18px;'>
<div style='font-size:12px;color:#0F766E;font-weight:600;line-height:1.4;'>
Support dosage &rarr; teacher practice adoption &rarr; student practice &rarr; competency mastery
</div>
</div>
<div style='overflow-x:auto;'>
<table style='width:100%;border-collapse:collapse;font-size:13px;text-align:left;'>
<thead>
<tr style='border-bottom:1px solid #E2E8F0;color:#64748B;font-size:11px;font-weight:500;'>
<th style='padding:8px 8px 12px 0;width:38%;'>Stage</th>
<th style='padding:8px 8px 12px 8px;width:42%;'>Current rate & Progress</th>
<th style='padding:8px 0 12px 8px;width:20%;'>Change</th>
</tr>
</thead>
<tbody>
<tr style='border-bottom:1px solid #F1F5F9;'>
<td style='padding:14px 8px 14px 0;font-weight:600;color:#0F172A;'>
    <div style='display:flex;align-items:center;gap:6px;'>
        <span style='background:#E0F2FE;color:#0369A1;font-size:10px;font-weight:700;padding:2px 6px;border-radius:4px;'>1</span>
        Support received
    </div>
</td>
<td style='padding:14px 8px;'>
    <div style='display:flex;align-items:center;gap:10px;'>
        <span style='min-width:32px;font-weight:700;color:#0F172A;'>{dyn_support_rate}%</span>
        <div style='flex:1;max-width:130px;background:#EEF2F6;border-radius:999px;height:8px;overflow:hidden;box-shadow:inset 0 1px 2px rgba(0,0,0,0.05);'>
            <div style='background:linear-gradient(90deg, #38BDF8, #0284C7);width:{dyn_support_rate}%;height:100%;border-radius:999px;'></div>
        </div>
    </div>
</td>
<td style='padding:14px 0 14px 8px;color:#059669;font-weight:600;'>{active_pathway_changes['support']}</td>
</tr>
<tr style='border-bottom:1px solid #F1F5F9;'>
<td style='padding:14px 8px 14px 0;font-weight:600;color:#0F172A;'>
    <div style='display:flex;align-items:center;gap:6px;'>
        <span style='background:#CCFBF1;color:#0F766E;font-size:10px;font-weight:700;padding:2px 6px;border-radius:4px;'>2</span>
        Practice adoption
    </div>
</td>
<td style='padding:14px 8px;'>
    <div style='display:flex;align-items:center;gap:10px;'>
        <span style='min-width:32px;font-weight:700;color:#0F172A;'>{dyn_practice_rate}%</span>
        <div style='flex:1;max-width:130px;background:#EEF2F6;border-radius:999px;height:8px;overflow:hidden;box-shadow:inset 0 1px 2px rgba(0,0,0,0.05);'>
            <div style='background:linear-gradient(90deg, #2DD4BF, #0D9488);width:{dyn_practice_rate}%;height:100%;border-radius:999px;'></div>
        </div>
    </div>
</td>
<td style='padding:14px 0 14px 8px;color:#059669;font-weight:600;'>{active_pathway_changes['practice']}</td>
</tr>
<tr style='border-bottom:1px solid #F1F5F9;'>
<td style='padding:14px 8px 14px 0;font-weight:600;color:#0F172A;'>
    <div style='display:flex;align-items:center;gap:6px;'>
        <span style='background:#FEF3C7;color:#B45309;font-size:10px;font-weight:700;padding:2px 6px;border-radius:4px;'>3</span>
        Student practice
    </div>
</td>
<td style='padding:14px 8px;'>
    <div style='display:flex;align-items:center;gap:10px;'>
        <span style='min-width:32px;font-weight:700;color:#0F172A;'>{dyn_student_prac_rate}%</span>
        <div style='flex:1;max-width:130px;background:#EEF2F6;border-radius:999px;height:8px;overflow:hidden;box-shadow:inset 0 1px 2px rgba(0,0,0,0.05);'>
            <div style='background:linear-gradient(90deg, #FBBF24, #D97706);width:{dyn_student_prac_rate}%;height:100%;border-radius:999px;'></div>
        </div>
    </div>
</td>
<td style='padding:14px 0 14px 8px;color:#059669;font-weight:600;'>{active_pathway_changes['student']}</td>
</tr>
<tr style='border-bottom:1px solid #F1F5F9;'>
<td style='padding:14px 8px 14px 0;font-weight:600;color:#0F172A;'>
    <div style='display:flex;align-items:center;gap:6px;'>
        <span style='background:#DCFCE7;color:#15803D;font-size:10px;font-weight:700;padding:2px 6px;border-radius:4px;'>4</span>
        Competency mastery
    </div>
</td>
<td style='padding:14px 8px;'>
    <div style='display:flex;align-items:center;gap:10px;'>
        <span style='min-width:32px;font-weight:700;color:#0F172A;'>{dyn_mastery_rate}%</span>
        <div style='flex:1;max-width:130px;background:#EEF2F6;border-radius:9999px;height:8px;overflow:hidden;box-shadow:inset 0 1px 2px rgba(0,0,0,0.05);'>
            <div style='background:linear-gradient(90deg, #4ADE80, #16A34A);width:{dyn_mastery_rate}%;height:100%;border-radius:999px;'></div>
        </div>
    </div>
</td>
<td style='padding:14px 0 14px 8px;color:#059669;font-weight:600;'>{active_pathway_changes['mastery']}</td>
</tr>
</tbody>
</table>
</div>
</div>
"""
        render_html(pathway_html)

    with col_equity:
        equity_html = f"""
<div class='figma-card' style='padding:24px;'>
<div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;'>
    <h3 style='font-weight:700;color:#0F172A;font-size:16px;margin:0;'>Equity lens</h3>
    <span style='font-size:11px;color:#059669;background:#DEF7EC;padding:2px 8px;border-radius:999px;font-weight:600;'>{eval_window}</span>
</div>
<p style='font-size:12px;color:#64748B;line-height:1.5;margin-bottom:14px;'>
Compare gains by baseline, zone, school category, teacher availability and school type.
</p>
<div style='display:flex;flex-wrap:wrap;gap:6px;margin-bottom:16px;'>
<span style='background:#F1F5F9;color:#334155;padding:4px 10px;border-radius:999px;font-size:11px;font-weight:500;border:1px solid #E2E8F0;'>Low baseline</span>
<span style='background:#F1F5F9;color:#334155;padding:4px 10px;border-radius:999px;font-size:11px;font-weight:500;border:1px solid #E2E8F0;'>Teacher vacancies</span>
<span style='background:#F1F5F9;color:#334155;padding:4px 10px;border-radius:999px;font-size:11px;font-weight:500;border:1px solid #E2E8F0;'>Red schools</span>
</div>

<div style='background:#F8FAFC;border:1px solid #E2E8F0;border-radius:10px;padding:16px;'>
<div style='margin-bottom:14px;'>
    <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;'>
        <span style='font-size:12px;font-weight:600;color:#0F172A;'>Low baseline schools</span>
        <span style='font-size:12px;font-weight:700;color:#059669;'>{active_equity['low_baseline']}</span>
    </div>
    <div style='background:#E2E8F0;border-radius:999px;height:6px;width:100%;overflow:hidden;'>
        <div style='background:linear-gradient(90deg, #34D399, #059669);width:{active_equity['low_baseline_width']}%;height:100%;border-radius:999px;'></div>
    </div>
</div>

<div style='margin-bottom:14px;'>
    <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;'>
        <span style='font-size:12px;font-weight:600;color:#0F172A;'>Teacher vacancies</span>
        <span style='font-size:12px;font-weight:700;color:#D97706;'>{active_equity['vacancies']}</span>
    </div>
    <div style='background:#E2E8F0;border-radius:999px;height:6px;width:100%;overflow:hidden;'>
        <div style='background:linear-gradient(90deg, #FBBF24, #D97706);width:{active_equity['vacancies_width']}%;height:100%;border-radius:999px;'></div>
    </div>
</div>

<div>
    <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;'>
        <span style='font-size:12px;font-weight:600;color:#0F172A;'>Category Red schools</span>
        <span style='font-size:12px;font-weight:700;color:#059669;'>{active_equity['red_schools']}</span>
    </div>
    <div style='background:#E2E8F0;border-radius:999px;height:6px;width:100%;overflow:hidden;'>
        <div style='background:linear-gradient(90deg, #10B981, #047857);width:{active_equity['red_schools_width']}%;height:100%;border-radius:999px;'></div>
    </div>
</div>
</div>
</div>
"""
        render_html(equity_html)


# ==============================================================================
# TAB 8: RISKS AND DECISIONS
# ==============================================================================
with tabs[7]:
    # HEADER
    col_rh1, col_rh2 = st.columns([2.5, 1.2])
    with col_rh1:
        st.markdown("""
        <div>
            <h2 style='font-size:24px;font-weight:700;color:#0F172A;margin:0 0 4px 0;'>Risks and decisions</h2>
            <div style='font-size:13px;color:#64748B;font-weight:400;'>Live view of risks that can affect implementation and learning outcomes</div>
        </div>
        """, unsafe_allow_html=True)
    with col_rh2:
        risk_view = st.selectbox("Filter risks", ["All risks", "Open only", "High severity", "Structural", "Content"], key="risk_view_filter")

    if active_filters:
        st.info("🔍 **Active Slicers Applied:** " + " | ".join(active_filters))

    # RISK DATA
    ALL_RISKS = [
        {"risk": "Teacher vacancy", "type": "Structural", "severity": "High", "owner": "PoC + Hub", "mitigation": "Identify substitute and escalate after one cycle", "status": "Open", "status_bg": "#FEE2E2", "status_color": "#991B1B"},
        {"risk": "Competency pack delay", "type": "Content", "severity": "Medium", "owner": "Content team", "mitigation": "Finalise Hindi videos and worksheets", "status": "At risk", "status_bg": "#FEF3C7", "status_color": "#92400E"},
        {"risk": "Missing evidence", "type": "Data quality", "severity": "Medium", "owner": "Zone manager", "mitigation": "Complete visit form before Friday review", "status": "Open", "status_bg": "#FEE2E2", "status_color": "#991B1B"},
        {"risk": "Low HoS attendance", "type": "Structural", "severity": "High", "owner": "HM Relations", "mitigation": "Re-schedule missed sessions in Week 2", "status": "Open", "status_bg": "#FEE2E2", "status_color": "#991B1B"},
        {"risk": "FA data incomplete", "type": "Data quality", "severity": "Medium", "owner": "Field team", "mitigation": "Spot-check 5 schools per zone", "status": "Monitoring", "status_bg": "#EFF6FF", "status_color": "#1E40AF"},
        {"risk": "Coaching visit missed", "type": "Field ops", "severity": "Medium", "owner": "PoC", "mitigation": "Reschedule within current week", "status": "Resolved", "status_bg": "#DEF7EC", "status_color": "#03543F"},
        {"risk": "SoP not submitted", "type": "Data quality", "severity": "Low", "owner": "Zone manager", "mitigation": "Send reminder, escalate after 48h", "status": "Monitoring", "status_bg": "#EFF6FF", "status_color": "#1E40AF"},
        {"risk": "Grey school vacancy protocol", "type": "Structural", "severity": "High", "owner": "PM + Zonal Officer", "mitigation": "Identify interim teaching arrangement", "status": "At risk", "status_bg": "#FEF3C7", "status_color": "#92400E"},
    ]

    # FILTER
    sev_map = {"High severity": "High", "Structural": "Structural", "Content": "Content"}
    if risk_view == "Open only":
        filtered_risks = [r for r in ALL_RISKS if r["status"] in ("Open", "At risk")]
    elif risk_view in sev_map:
        filtered_risks = [r for r in ALL_RISKS if r["severity"] == sev_map.get(risk_view, r["severity"]) or r["type"] == sev_map.get(risk_view, r["type"])]
    else:
        filtered_risks = ALL_RISKS

    # DYNAMIC KPI COUNTS
    open_risks = sum(1 for r in filtered_risks if r["status"] == "Open")
    at_risk = sum(1 for r in filtered_risks if r["status"] == "At risk")
    structural = sum(1 for r in filtered_risks if r["type"] == "Structural")
    high_sev = sum(1 for r in filtered_risks if r["severity"] == "High")

    # 4 KPI CARDS
    rk1, rk2, rk3, rk4 = st.columns(4)
    with rk1:
        render_html(f"""
        <div class='figma-card' style='padding:18px 20px;'>
            <div style='font-size:12px;color:#64748B;font-weight:500;margin-bottom:6px;'>Open risks</div>
            <div style='font-size:34px;font-weight:700;color:#BE123C;line-height:1.1;margin-bottom:6px;'>{open_risks}</div>
            <div style='font-size:12px;color:#BE123C;font-weight:600;'>{high_sev} high severity</div>
        </div>
        """)
    with rk2:
        render_html(f"""
        <div class='figma-card' style='padding:18px 20px;'>
            <div style='font-size:12px;color:#64748B;font-weight:500;margin-bottom:6px;'>Overdue mitigations</div>
            <div style='font-size:34px;font-weight:700;color:#0F172A;line-height:1.1;margin-bottom:6px;'>{at_risk}</div>
            <div style='font-size:12px;color:#B45309;font-weight:600;'>Needs escalation</div>
        </div>
        """)
    with rk3:
        render_html(f"""
        <div class='figma-card' style='padding:18px 20px;'>
            <div style='font-size:12px;color:#64748B;font-weight:500;margin-bottom:6px;'>Schools with structural risk</div>
            <div style='font-size:34px;font-weight:700;color:#0F172A;line-height:1.1;margin-bottom:6px;'>{structural * 14}</div>
            <div style='font-size:12px;color:#64748B;font-weight:400;'>Grey pathway</div>
        </div>
        """)
    with rk4:
        render_html(f"""
        <div class='figma-card' style='padding:18px 20px;'>
            <div style='font-size:12px;color:#64748B;font-weight:500;margin-bottom:6px;'>Predicted Red schools</div>
            <div style='font-size:34px;font-weight:700;color:#0F172A;line-height:1.1;margin-bottom:6px;'>29</div>
            <div style='font-size:12px;color:#B45309;font-weight:600;'>Next cycle</div>
        </div>
        """)

    st.markdown("<br>", unsafe_allow_html=True)

    # RISK REGISTER TABLE
    risk_rows = []
    for r in filtered_risks:
        sev_color = "#BE123C" if r["severity"] == "High" else ("#B45309" if r["severity"] == "Medium" else "#64748B")
        risk_rows.append(
            f"<tr style='border-bottom:1px solid #F1F5F9;'>"
            f"<td style='padding:14px 8px 14px 0;font-weight:600;color:#0F172A;'>{r['risk']}</td>"
            f"<td style='padding:14px 8px;color:#64748B;font-size:12px;'>{r['type']}</td>"
            f"<td style='padding:14px 8px;font-weight:600;font-size:12px;color:{sev_color};'>{r['severity']}</td>"
            f"<td style='padding:14px 8px;color:#475569;font-size:12px;'>{r['owner']}</td>"
            f"<td style='padding:14px 8px;color:#64748B;font-size:12px;'>{r['mitigation']}</td>"
            f"<td style='padding:14px 0 14px 8px;'>"
            f"<span style='background:{r['status_bg']};color:{r['status_color']};padding:3px 10px;border-radius:999px;font-size:11px;font-weight:600;display:inline-block;white-space:nowrap;'>{r['status']}</span>"
            f"</td>"
            f"</tr>"
        )

    risk_table_html = f"""
<div class='figma-card' style='padding:22px;'>
<div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;'>
<h3 style='font-weight:700;color:#0F172A;font-size:16px;margin:0;'>Risk register</h3>
<span style='font-size:11px;color:#64748B;font-weight:500;'>Showing {len(filtered_risks)} risks · {zone_badge_text}</span>
</div>
<div style='overflow-x:auto;'>
<table style='width:100%;border-collapse:collapse;font-size:13px;text-align:left;'>
<thead>
<tr style='border-bottom:1px solid #E2E8F0;color:#64748B;font-size:11px;font-weight:500;text-transform:uppercase;letter-spacing:0.04em;'>
<th style='padding:8px 8px 12px 0;width:22%;'>Risk</th>
<th style='padding:8px 8px 12px 8px;width:13%;'>Type</th>
<th style='padding:8px 8px 12px 8px;width:10%;'>Severity</th>
<th style='padding:8px 8px 12px 8px;width:13%;'>Owner</th>
<th style='padding:8px 8px 12px 8px;width:32%;'>Mitigation</th>
<th style='padding:8px 0 12px 8px;width:10%;'>Status</th>
</tr>
</thead>
<tbody>
{"".join(risk_rows)}
</tbody>
</table>
</div>
</div>
"""
    render_html(risk_table_html)


# ==============================================================================
# TAB 9: SCHOOL AI BRIEF
# ==============================================================================
with tabs[8]:
    # HEADER
    col_aih1, col_aih2 = st.columns([2.2, 1.5])
    with col_aih1:
        st.markdown("""
        <div>
            <h2 style='font-size:24px;font-weight:700;color:#0F172A;margin:0 0 4px 0;'>School AI brief</h2>
            <div style='font-size:13px;color:#64748B;font-weight:400;'>One-page evidence summary for the next school conversation</div>
        </div>
        """, unsafe_allow_html=True)
    with col_aih2:
        school_select = st.selectbox(
            "Select School",
            [
                "RK Puram Sec 2 · Central Zone",
                "GPS Sector 14 Model · South Zone",
                "RPVV Lodi Colony · Civil Zone",
                "GGSSS Punjabi Bagh · West Zone",
                "SV Rohini Sec 16 · West Zone",
            ],
            key="school_ai_brief_select"
        )

    if active_filters:
        st.info("🔍 **Active Slicers Applied:** " + " | ".join(active_filters))

    st.markdown("<br>", unsafe_allow_html=True)

    # SCHOOL DATA
    SCHOOL_BRIEFS = {
        "RK Puram Sec 2 · Central Zone": {
            "name": "RK Puram Sec 2",
            "zone": "Central Zone",
            "poc": "Geeta",
            "last_visit": "11 Sep 2026",
            "rag": "Red",
            "rag_bg": "#FEE2E2",
            "rag_color": "#991B1B",
            "priority_comp": "Addition and subtraction",
            "confidence": "Medium",
            "conf_bg": "#FEF3C7",
            "conf_color": "#92400E",
            "what_happening": "Spot-check mastery is 24%. Students frequently misplace the carry value in two-digit addition. Classroom evidence shows limited independent practice and inconsistent feedback.",
            "why_matters": "The learning gap is persistent and is likely to affect the next number-operations competency unless the misconception is addressed before the next cycle.",
            "support_done": "Competency Pack 1 received. One school interaction recorded. Formative assessment evidence is incomplete. No confirmed remedial follow-up is recorded.",
            "next_action": "Conduct an in-person coaching visit. Model place-value addition, review five student responses, agree on one practice routine and repeat the spot check within two weeks.",
            "evidence": [
                {"signal": "Student learning", "evidence": "24% mastery in spot check", "conf": "Medium", "conf_bg": "#FEF3C7", "conf_color": "#92400E"},
                {"signal": "Teacher practice", "evidence": "Limited practice monitoring observed", "conf": "Medium", "conf_bg": "#FEF3C7", "conf_color": "#92400E"},
                {"signal": "Student practice", "evidence": "Worksheet completion not verified", "conf": "Low", "conf_bg": "#FEE2E2", "conf_color": "#991B1B"},
                {"signal": "Structural conditions", "evidence": "Teacher availability to be confirmed", "conf": "Medium", "conf_bg": "#FEF3C7", "conf_color": "#92400E"},
            ],
        },
        "GPS Sector 14 Model · South Zone": {
            "name": "GPS Sector 14 Model",
            "zone": "South Zone",
            "poc": "Sakshi",
            "last_visit": "10 Sep 2026",
            "rag": "Green",
            "rag_bg": "#DEF7EC",
            "rag_color": "#03543F",
            "priority_comp": "Reading comprehension",
            "confidence": "High",
            "conf_bg": "#DEF7EC",
            "conf_color": "#03543F",
            "what_happening": "Mastery is at 82%. Students complete 20 min daily practice. Teacher is implementing all three key practices from the September Competency Pack.",
            "why_matters": "School is an exemplar candidate for Samvad. Maintaining current momentum secures endline targets ahead of schedule.",
            "support_done": "All 3 teacher batches completed. SoP submitted on time. PoC Sakshi maintained regular visit cadence with 3/3 visits achieved.",
            "next_action": "Feature teacher in Samvad exemplar list. Share lesson plan with Central team. Schedule peer observation by neighbouring school.",
            "evidence": [
                {"signal": "Student learning", "evidence": "82% mastery in spot check", "conf": "High", "conf_bg": "#DEF7EC", "conf_color": "#03543F"},
                {"signal": "Teacher practice", "evidence": "All 3 key practices observed", "conf": "High", "conf_bg": "#DEF7EC", "conf_color": "#03543F"},
                {"signal": "Student practice", "evidence": "20 min daily practice confirmed", "conf": "High", "conf_bg": "#DEF7EC", "conf_color": "#03543F"},
                {"signal": "Structural conditions", "evidence": "Stable staffing, no vacancies", "conf": "High", "conf_bg": "#DEF7EC", "conf_color": "#03543F"},
            ],
        },
        "RPVV Lodi Colony · Civil Zone": {
            "name": "RPVV Lodi Colony",
            "zone": "Civil Zone",
            "poc": "Anshika",
            "last_visit": "09 Sep 2026",
            "rag": "Amber",
            "rag_bg": "#FEF3C7",
            "rag_color": "#92400E",
            "priority_comp": "ORF fluency",
            "confidence": "Medium",
            "conf_bg": "#FEF3C7",
            "conf_color": "#92400E",
            "what_happening": "ORF mastery at 48%. Students struggle with matra decoding during timed reading. 2 out of 3 planned visits achieved this week.",
            "why_matters": "ORF fluency is a gating skill for comprehension. Without intervention by cycle end, the school risks sliding to Red.",
            "support_done": "Competency Pack 1 distributed. Partial FA evidence collected. One visit missed due to HoS unavailability.",
            "next_action": "Reschedule missed visit. Demonstrate sound-box phonics technique. Agree on a 5-student ORF spot check with the teacher.",
            "evidence": [
                {"signal": "Student learning", "evidence": "48% ORF mastery (spot check)", "conf": "Medium", "conf_bg": "#FEF3C7", "conf_color": "#92400E"},
                {"signal": "Teacher practice", "evidence": "Partial implementation observed", "conf": "Medium", "conf_bg": "#FEF3C7", "conf_color": "#92400E"},
                {"signal": "Student practice", "evidence": "Practice time inconsistent", "conf": "Low", "conf_bg": "#FEE2E2", "conf_color": "#991B1B"},
                {"signal": "Structural conditions", "evidence": "HoS available from 12 Sep", "conf": "Medium", "conf_bg": "#FEF3C7", "conf_color": "#92400E"},
            ],
        },
        "GGSSS Punjabi Bagh · West Zone": {
            "name": "GGSSS Punjabi Bagh",
            "zone": "West Zone",
            "poc": "Megha",
            "last_visit": "11 Sep 2026",
            "rag": "Green",
            "rag_bg": "#DEF7EC",
            "rag_color": "#03543F",
            "priority_comp": "Number operations",
            "confidence": "High",
            "conf_bg": "#DEF7EC",
            "conf_color": "#03543F",
            "what_happening": "Mastery at 71%. Teacher conducts daily 15-min practice. FA evidence collected and follow-up remediation logged.",
            "why_matters": "School on track for endline target. Continued light-touch support will sustain gains.",
            "support_done": "4/4 visits achieved. SoP submitted. Teacher training batch completed.",
            "next_action": "Maintain visit cadence. Share FA data with Central team. Identify peer mentoring opportunity.",
            "evidence": [
                {"signal": "Student learning", "evidence": "71% mastery confirmed", "conf": "High", "conf_bg": "#DEF7EC", "conf_color": "#03543F"},
                {"signal": "Teacher practice", "evidence": "All practices observed", "conf": "High", "conf_bg": "#DEF7EC", "conf_color": "#03543F"},
                {"signal": "Student practice", "evidence": "15 min daily confirmed", "conf": "High", "conf_bg": "#DEF7EC", "conf_color": "#03543F"},
                {"signal": "Structural conditions", "evidence": "Stable", "conf": "High", "conf_bg": "#DEF7EC", "conf_color": "#03543F"},
            ],
        },
        "SV Rohini Sec 16 · West Zone": {
            "name": "SV Rohini Sec 16",
            "zone": "West Zone",
            "poc": "Swagata",
            "last_visit": "10 Sep 2026",
            "rag": "Amber",
            "rag_bg": "#FEF3C7",
            "rag_color": "#92400E",
            "priority_comp": "Place value",
            "confidence": "Medium",
            "conf_bg": "#FEF3C7",
            "conf_color": "#92400E",
            "what_happening": "Mastery at 52%. Students can add single-digit correctly but struggle with carrying in two-digit operations. 3/4 visits achieved.",
            "why_matters": "Place value is foundational for multi-digit operations in the October competency pack.",
            "support_done": "Pack 1 received. 3/4 visits done. Partial remediation follow-up logged.",
            "next_action": "Complete the 4th visit. Run bundle-sticks demonstration. Confirm remediation schedule with teacher.",
            "evidence": [
                {"signal": "Student learning", "evidence": "52% mastery (spot check)", "conf": "Medium", "conf_bg": "#FEF3C7", "conf_color": "#92400E"},
                {"signal": "Teacher practice", "evidence": "2 of 3 practices observed", "conf": "Medium", "conf_bg": "#FEF3C7", "conf_color": "#92400E"},
                {"signal": "Student practice", "evidence": "Worksheet done, spot check pending", "conf": "Medium", "conf_bg": "#FEF3C7", "conf_color": "#92400E"},
                {"signal": "Structural conditions", "evidence": "Stable, no vacancies", "conf": "High", "conf_bg": "#DEF7EC", "conf_color": "#03543F"},
            ],
        },
    }

    brief = SCHOOL_BRIEFS.get(school_select, SCHOOL_BRIEFS["RK Puram Sec 2 · Central Zone"])

    # EVIDENCE TRAIL ROWS
    ev_rows = "".join([
        f"<tr style='border-bottom:1px solid #1E3A5F;'>"
        f"<td style='padding:12px 16px 12px 0;color:#CBD5E1;font-size:12px;font-weight:500;'>{e['signal']}</td>"
        f"<td style='padding:12px 16px;color:#E2E8F0;font-size:12px;'>{e['evidence']}</td>"
        f"<td style='padding:12px 0 12px 16px;'>"
        f"<span style='background:{e['conf_bg']};color:{e['conf_color']};padding:3px 10px;border-radius:999px;font-size:11px;font-weight:600;'>{e['conf']}</span>"
        f"</td>"
        f"</tr>"
        for e in brief["evidence"]
    ])

    brief_html = f"""
<div style='background:linear-gradient(135deg, #0F172A 0%, #1E2D4A 60%, #0F766E 100%);border-radius:16px;padding:28px 32px;color:#F8FAFC;'>
<div style='display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:20px;'>
    <div>
        <h3 style='font-size:22px;font-weight:800;color:#FFFFFF;margin:0 0 4px 0;'>{brief['name']}</h3>
        <div style='font-size:13px;color:#94A3B8;'>{brief['zone']} · Assigned to {brief['poc']} · Last evidence: {brief['last_visit']}</div>
    </div>
    <div style='display:flex;gap:8px;flex-wrap:wrap;justify-content:flex-end;'>
        <span style='background:{brief["rag_bg"]};color:{brief["rag_color"]};padding:4px 12px;border-radius:999px;font-size:11px;font-weight:700;'>{brief['rag']} support pathway</span>
        <span style='background:#1E3A5F;color:#93C5FD;border:1px solid #2D5A8E;padding:4px 12px;border-radius:999px;font-size:11px;font-weight:600;'>Priority competency: {brief['priority_comp']}</span>
        <span style='background:{brief["conf_bg"]};color:{brief["conf_color"]};padding:4px 12px;border-radius:999px;font-size:11px;font-weight:600;'>Evidence confidence: {brief['confidence']}</span>
    </div>
</div>

<div style='display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-bottom:20px;'>
    <div style='background:rgba(255,255,255,0.06);border-radius:10px;padding:18px;border:1px solid rgba(255,255,255,0.1);'>
        <div style='font-size:10px;font-weight:700;color:#64748B;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:8px;'>WHAT IS HAPPENING</div>
        <div style='font-size:13px;color:#E2E8F0;line-height:1.6;'>{brief['what_happening']}</div>
    </div>
    <div style='background:rgba(255,255,255,0.06);border-radius:10px;padding:18px;border:1px solid rgba(255,255,255,0.1);'>
        <div style='font-size:10px;font-weight:700;color:#64748B;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:8px;'>WHY IT MATTERS</div>
        <div style='font-size:13px;color:#E2E8F0;line-height:1.6;'>{brief['why_matters']}</div>
    </div>
</div>

<div style='display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-bottom:24px;'>
    <div style='background:rgba(255,255,255,0.06);border-radius:10px;padding:18px;border:1px solid rgba(255,255,255,0.1);'>
        <div style='font-size:10px;font-weight:700;color:#64748B;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:8px;'>WHAT SUPPORT HAS HAPPENED</div>
        <div style='font-size:13px;color:#E2E8F0;line-height:1.6;'>{brief['support_done']}</div>
    </div>
    <div style='background:rgba(15,118,110,0.25);border:1px solid rgba(15,118,110,0.5);border-radius:10px;padding:18px;'>
        <div style='font-size:10px;font-weight:700;color:#2DD4BF;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:8px;'>RECOMMENDED NEXT ACTION</div>
        <div style='font-size:13px;color:#E2E8F0;line-height:1.6;'>{brief['next_action']}</div>
    </div>
</div>

<div style='background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);border-radius:10px;padding:18px;'>
    <div style='font-size:10px;font-weight:700;color:#64748B;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:12px;'>EVIDENCE TRAIL</div>
    <table style='width:100%;border-collapse:collapse;'>
    <thead>
    <tr style='border-bottom:1px solid rgba(255,255,255,0.1);'>
        <th style='padding:6px 16px 10px 0;font-size:11px;color:#64748B;font-weight:500;text-align:left;width:25%;'>Signal</th>
        <th style='padding:6px 16px 10px 16px;font-size:11px;color:#64748B;font-weight:500;text-align:left;width:55%;'>Current evidence</th>
        <th style='padding:6px 0 10px 16px;font-size:11px;color:#64748B;font-weight:500;text-align:left;width:20%;'>Confidence</th>
    </tr>
    </thead>
    <tbody>{ev_rows}</tbody>
    </table>
</div>
</div>
"""
    render_html(brief_html)

    # ── REAL ACTION BUTTONS ──────────────────────────────────────────────────
    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
    ab1, ab2, ab3, ab4 = st.columns(4)

    # --- Generate text content for each action ---
    coaching_text = f"""COACHING AGENDA — {brief['name']}
Generated: 17 Sep 2026  |  Assigned PoC: {brief['poc']}  |  Zone: {brief['zone']}
RAG: {brief['rag']}  |  Priority Competency: {brief['priority_comp']}
Evidence Confidence: {brief['confidence']}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. OPENING (5 min)
   • Check in with HoS / teacher
   • Reference last visit date: {brief['last_visit']}
   • Recap: {brief['support_done']}

2. WHAT WE ARE SEEING (10 min)
   {brief['what_happening']}

3. WHY THIS MATTERS (5 min)
   {brief['why_matters']}

4. PRACTICE DEMONSTRATION (15 min)
   • Model the recommended technique for: {brief['priority_comp']}
   • Ask teacher to try with 2–3 students while you observe

5. AGREEMENT & NEXT STEPS (10 min)
   {brief['next_action']}

6. EVIDENCE TRAIL REVIEW
   • Student learning  : {brief['evidence'][0]['evidence']}  [{brief['evidence'][0]['conf']} confidence]
   • Teacher practice  : {brief['evidence'][1]['evidence']}  [{brief['evidence'][1]['conf']} confidence]
   • Student practice  : {brief['evidence'][2]['evidence']}  [{brief['evidence'][2]['conf']} confidence]
   • Structural        : {brief['evidence'][3]['evidence']}  [{brief['evidence'][3]['conf']} confidence]

7. CLOSE
   • Confirm follow-up date
   • Log SoP before leaving school
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Generated by LIFTed Analytics · Cohort 2
"""

    escalation_text = f"""ESCALATION NOTE — {brief['name']}
Date: 17 Sep 2026  |  Raised by: {brief['poc']}  |  Zone: {brief['zone']}
Severity: {'HIGH' if brief['rag'] == 'Red' else 'MEDIUM'}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SCHOOL:         {brief['name']}
RAG STATUS:     {brief['rag']}
PRIORITY AREA:  {brief['priority_comp']}
LAST VISIT:     {brief['last_visit']}

SITUATION:
{brief['what_happening']}

PROGRAMME IMPACT RISK:
{brief['why_matters']}

SUPPORT PROVIDED TO DATE:
{brief['support_done']}

RECOMMENDED ESCALATION ACTION:
{brief['next_action']}

EVIDENCE SUMMARY:
  - Student learning  : {brief['evidence'][0]['evidence']}
  - Teacher practice  : {brief['evidence'][1]['evidence']}
  - Student practice  : {brief['evidence'][2]['evidence']}
  - Structural        : {brief['evidence'][3]['evidence']}

REQUESTED DECISION:
  ☐ Assign additional PoC support
  ☐ Escalate to Zonal Officer
  ☐ Schedule emergency HoS meeting
  ☐ Flag for Programme Manager review

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Generated by LIFTed Analytics · Cohort 2
"""

    zone_comparison_html = f"""
<div class='figma-card' style='padding:22px;'>
<div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:18px;'>
<h3 style='font-weight:700;color:#0F172A;font-size:16px;margin:0;'>Zone comparison — {brief['zone']}</h3>
<span style='font-size:11px;background:#F1F5F9;color:#475569;padding:4px 10px;border-radius:6px;font-weight:500;'>vs. {brief['name']}</span>
</div>
<table style='width:100%;border-collapse:collapse;font-size:13px;'>
<thead>
<tr style='border-bottom:1px solid #E2E8F0;color:#64748B;font-size:11px;font-weight:500;text-transform:uppercase;letter-spacing:0.04em;'>
<th style='padding:8px 8px 12px 0;'>School</th>
<th style='padding:8px;'>RAG</th>
<th style='padding:8px;'>Mastery %</th>
<th style='padding:8px;'>Visits</th>
<th style='padding:8px;'>Evidence conf.</th>
</tr>
</thead>
<tbody>
<tr style='border-bottom:1px solid #F1F5F9;background:#F8FAFC;'>
<td style='padding:12px 8px 12px 0;font-weight:700;color:#0F172A;'>{brief['name']} (selected)</td>
<td style='padding:12px 8px;'><span style='background:{brief["rag_bg"]};color:{brief["rag_color"]};padding:3px 10px;border-radius:999px;font-size:11px;font-weight:600;'>{brief['rag']}</span></td>
<td style='padding:12px 8px;font-weight:600;color:#0F172A;'>—</td>
<td style='padding:12px 8px;color:#475569;'>—</td>
<td style='padding:12px 8px;'><span style='background:{brief["conf_bg"]};color:{brief["conf_color"]};padding:3px 10px;border-radius:999px;font-size:11px;font-weight:600;'>{brief['confidence']}</span></td>
</tr>
<tr style='border-bottom:1px solid #F1F5F9;'>
<td style='padding:12px 8px 12px 0;font-weight:500;color:#0F172A;'>Zone average</td>
<td style='padding:12px 8px;'><span style='background:#FEF3C7;color:#92400E;padding:3px 10px;border-radius:999px;font-size:11px;font-weight:600;'>Amber</span></td>
<td style='padding:12px 8px;font-weight:600;color:#047857;'>58%</td>
<td style='padding:12px 8px;color:#475569;'>3.1 / 4</td>
<td style='padding:12px 8px;'><span style='background:#FEF3C7;color:#92400E;padding:3px 10px;border-radius:999px;font-size:11px;font-weight:600;'>Medium</span></td>
</tr>
<tr style='border-bottom:1px solid #F1F5F9;'>
<td style='padding:12px 8px 12px 0;font-weight:500;color:#0F172A;'>Top performer</td>
<td style='padding:12px 8px;'><span style='background:#DEF7EC;color:#03543F;padding:3px 10px;border-radius:999px;font-size:11px;font-weight:600;'>Green</span></td>
<td style='padding:12px 8px;font-weight:600;color:#047857;'>84%</td>
<td style='padding:12px 8px;color:#475569;'>4 / 4</td>
<td style='padding:12px 8px;'><span style='background:#DEF7EC;color:#03543F;padding:3px 10px;border-radius:999px;font-size:11px;font-weight:600;'>High</span></td>
</tr>
<tr>
<td style='padding:12px 8px 12px 0;font-weight:500;color:#0F172A;'>Programme average</td>
<td style='padding:12px 8px;'><span style='background:#FEF3C7;color:#92400E;padding:3px 10px;border-radius:999px;font-size:11px;font-weight:600;'>Amber</span></td>
<td style='padding:12px 8px;font-weight:600;color:#047857;'>54%</td>
<td style='padding:12px 8px;color:#475569;'>2.9 / 4</td>
<td style='padding:12px 8px;'><span style='background:#FEF3C7;color:#92400E;padding:3px 10px;border-radius:999px;font-size:11px;font-weight:600;'>Medium</span></td>
</tr>
</tbody>
</table>
</div>
"""

    with ab1:
        st.download_button(
            label="📋 Create coaching agenda",
            data=coaching_text,
            file_name=f"coaching_agenda_{brief['name'].replace(' ', '_')}.txt",
            mime="text/plain",
            use_container_width=True,
            key="btn_coaching"
        )
    with ab2:
        if st.button("📅 Schedule follow-up", use_container_width=True, key="btn_followup"):
            st.session_state["show_followup"] = not st.session_state.get("show_followup", False)
    with ab3:
        st.download_button(
            label="📤 Generate escalation note",
            data=escalation_text,
            file_name=f"escalation_{brief['name'].replace(' ', '_')}.txt",
            mime="text/plain",
            use_container_width=True,
            key="btn_escalation"
        )
    with ab4:
        if st.button("🗺️ Compare with zone", use_container_width=True, key="btn_zone"):
            st.session_state["show_zone_compare"] = not st.session_state.get("show_zone_compare", False)

    # FOLLOW-UP SCHEDULER (toggle panel)
    if st.session_state.get("show_followup", False):
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        with st.form("followup_form"):
            render_html("""
<div style='font-size:14px;font-weight:700;color:#0F172A;margin-bottom:8px;'>📅 Schedule follow-up visit</div>
""")
            fu1, fu2, fu3 = st.columns(3)
            with fu1:
                fu_date = st.date_input("Visit date", key="fu_date")
            with fu2:
                fu_type = st.selectbox("Visit type", ["Coaching visit", "Spot check", "HoS meeting", "Data review"], key="fu_type")
            with fu3:
                fu_poc = st.text_input("Assigned to (PoC)", value=brief["poc"], key="fu_poc")
            fu_notes = st.text_area("Notes / focus for visit", placeholder="e.g. Observe carry-value practice, check remediation log...", key="fu_notes")
            submitted = st.form_submit_button("✅ Confirm & log follow-up", use_container_width=True)
            if submitted:
                st.success(f"✅ Follow-up scheduled for **{fu_date}** ({fu_type}) with **{fu_poc}** at **{brief['name']}**.")
                st.session_state["show_followup"] = False

    # ZONE COMPARISON TABLE (toggle panel)
    if st.session_state.get("show_zone_compare", False):
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

# Attribution shown below all dashboard tabs.
st.markdown(
    "<footer style='margin-top:32px;padding:12px 0;text-align:center;color:#64748B;font-size:11px;'>Tech Team, Peepul</footer>",
    unsafe_allow_html=True,
)
