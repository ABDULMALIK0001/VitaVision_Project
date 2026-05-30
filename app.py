import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import html
import json
import hashlib
import joblib
from io import BytesIO
from pathlib import Path
from datetime import datetime, date, timedelta

import dashboard_v2

# =========================================
# Page configuration
# =========================================
st.set_page_config(
    page_title="VitaVision Health Analyzer",
    page_icon="IconVitaVision.png",
    layout="wide"
)

DISCLAIMER_QUERY_KEY = "vv_disclaimer"
HISTORY_ARCHIVE_SCHEMA_VERSION = 1
HISTORY_ARCHIVE_APP = "VitaVision"
HISTORY_ARCHIVE_ATTACHMENT_NAME = "vitavision_history.json"


def query_param_value(key):
    value = st.query_params.get(key)
    if isinstance(value, list):
        return value[0] if value else None
    return value


if "language" not in st.session_state:
    st.session_state["language"] = "English"

disclaimer_agreed_from_url = query_param_value(DISCLAIMER_QUERY_KEY) == "accepted"

if "disclaimer_agreed" not in st.session_state:
    st.session_state["disclaimer_agreed"] = disclaimer_agreed_from_url
elif disclaimer_agreed_from_url:
    st.session_state["disclaimer_agreed"] = True

if "theme_mode" not in st.session_state:
    st.session_state["theme_mode"] = "Dark"

# =========================================
# Disclaimer dialog
# =========================================
@st.dialog("\u00A0", dismissible=False)
def show_disclaimer():
    lang_c1, lang_c2, lang_c3 = st.columns([1, 2, 1])
    with lang_c2:
        disclaimer_lang = st.selectbox(
            "Language / اللغة",
            ["English", "العربية"],
            index=0 if st.session_state["language"] == "English" else 1,
            key="disclaimer_language"
        )

    is_ar = disclaimer_lang == "العربية"

    if not is_ar:
        title = "Medical Disclaimer"
        text = (
            "VitaVision is an educational awareness tool that interprets vitamin and mineral lab values using reference ranges "
            "and a machine-learning model.\n\n"
            "It does not replace medical diagnosis, consultation, or treatment. The app does not know your full medical history, "
            "medications, symptoms, or clinical context.\n\n"
            "Use the results as guidance only. If you have symptoms, abnormal values, or concerns, consult a qualified healthcare professional."
        )
        button_text = "I Agree and Continue"
    else:
        title = "تنبيه طبي"
        text = (
            "VitaVision أداة تعليمية وتوعوية تفسر قيم الفيتامينات والمعادن باستخدام نطاقات مرجعية ونموذج ذكاء اصطناعي.\n\n"
            "لا يغني التطبيق عن التشخيص الطبي أو الاستشارة أو العلاج، ولا يعرف تاريخك الطبي الكامل أو الأدوية أو الأعراض أو السياق السريري.\n\n"
            "استخدم النتائج كإرشاد عام فقط. إذا كانت لديك أعراض أو قيم غير طبيعية أو أي قلق صحي، فاستشر مختصًا صحيًا مؤهلًا."
        )
        button_text = "أوافق وأتابع"

    dir_val = "rtl" if is_ar else "ltr"
    align_val = "right" if is_ar else "left"

    formatted_text = text.replace("\n\n", "<br><br>").replace("\n", "<br>")

    st.html(f"""
<div style="
    border: 1px solid rgba(0,191,255,0.4);
    border-radius: 18px;
    padding: 22px 24px;
    background: linear-gradient(145deg, rgba(0,15,30,0.98), rgba(0,25,45,0.95));
    box-shadow: 0 8px 40px rgba(0,191,255,0.08), inset 0 1px 0 rgba(255,255,255,0.04);
">
    <div style="
        text-align: center;
        color: #00BFFF;
        font-size: 21px;
        font-weight: 800;
        margin-bottom: 16px;
        letter-spacing: 0.3px;
        font-family: 'Segoe UI', sans-serif;
    ">
        ⚠️ {title}
    </div>
    <div style="
        width: 60px;
        height: 2px;
        margin: 0 auto 16px;
        border-radius: 2px;
    "></div>
    <div style="
        color: #D8E8F0;
        font-size: 14.5px;
        line-height: 1.75;
        direction: {dir_val};
        text-align: {align_val};
        font-family: 'Segoe UI', 'Helvetica Neue', sans-serif;
        background: rgba(0,191,255,0.03);
        border-radius: 12px;
        padding: 16px 18px;
        border: 1px solid rgba(0,191,255,0.1);
        max-height: min(46vh, 360px);
        overflow-y: auto;
    ">
        {formatted_text}
    </div>
</div>
""")

    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

    if st.button(button_text, use_container_width=True, type="primary"):
        st.session_state["language"] = disclaimer_lang
        st.session_state["main_language"] = disclaimer_lang
        st.session_state["disclaimer_agreed"] = True
        st.query_params[DISCLAIMER_QUERY_KEY] = "accepted"
        st.rerun()


# =========================================
# Google Fonts
# =========================================
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# =========================================
# Global UI Styles
# =========================================
st.markdown("""
<style>

/* ── Base & Fonts ─────────────────────────── */
:root {
    --blue:        #00BFFF;
    --blue-dim:    rgba(0,191,255,0.18);
    --blue-border: rgba(0,191,255,0.30);
    --bg-card:     rgba(255,255,255,0.032);
    --bg-card-hover: rgba(0,191,255,0.06);
    --text-main:   #F0F4F8;
    --text-muted:  #8A9BAD;
    --text-sub:    #B8C8D8;
    --red:    #FF4B4B;
    --green:  #1DB954;
    --orange: #FFA500;
    --radius-lg: 18px;
    --radius-md: 12px;
    --radius-sm: 8px;
    --shadow-blue: 0 4px 24px rgba(0,191,255,0.10);
}

html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Plus Jakarta Sans', 'Cairo', sans-serif !important;
    background: #060d14 !important;
    color: var(--text-main) !important;
    width: 100% !important;
    min-height: 100% !important;
}
* {
    box-sizing: border-box !important;
}

.block-container {
    max-width: 1080px !important;
    margin: 0 auto !important;
    padding: 1.2rem 1.5rem 3rem !important;
}

/* ── Remove Streamlit chrome ─────────────── */
#MainMenu, footer, header { visibility: hidden; }

/* ── Dialog cleanup ──────────────────────── */
div[role="dialog"] header { display: none !important; }
div[role="dialog"] > div { padding-top: 0 !important; }
div[role="dialog"] { margin-top: -20px !important; }
.stTabs [data-baseweb="tab-highlight"],
.stTabs [data-baseweb="tab-border"] { display: none !important; }

/* ── Navigation Tabs ─────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    justify-content: center;
    gap: 0;
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 5px;
    margin-bottom: 30px;
    width: fit-content;
    margin-left: auto;
    margin-right: auto;
}

.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border: none !important;
    border-radius: 10px !important;
    color: var(--text-muted) !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    padding: 9px 26px !important;
    transition: all 0.2s ease !important;
    letter-spacing: 0.2px;
}

.stTabs [data-baseweb="tab"]:hover {
    color: var(--blue) !important;
    background: rgba(0,191,255,0.06) !important;
}

.stTabs [aria-selected="true"] {
    color: var(--blue) !important;
    background: rgba(0,191,255,0.12) !important;
    box-shadow: 0 0 0 1px rgba(0,191,255,0.25) !important;
}

/* ── Buttons ─────────────────────────────── */
div.stButton > button {
    border-radius: var(--radius-md) !important;
    height: 46px !important;
    font-weight: 700 !important;
    font-size: 14px !important;
    border: 1px solid var(--blue-border) !important;
    color: var(--text-main) !important;
    background: rgba(0,191,255,0.06) !important;
    transition: all 0.2s ease !important;
    letter-spacing: 0.3px !important;
}

div.stButton > button:hover {
    border-color: var(--blue) !important;
    background: rgba(0,191,255,0.16) !important;
    box-shadow: 0 0 16px rgba(0,191,255,0.20) !important;
    transform: translateY(-1px) !important;
}

div.stButton > button[kind="primary"],
div.stButton > button.primary {
    background: linear-gradient(135deg, #163845, #0e6081) !important;
    color: #fff !important;
    border: none !important;
    box-shadow: 0 4px 16px rgba(0,191,255,0.30) !important;
}

div.stDownloadButton > button {
    border-radius: var(--radius-md) !important;
    height: 46px !important;
    font-weight: 700 !important;
    font-size: 14px !important;
    background: linear-gradient(135deg, rgba(0,128,179,0.25), rgba(0,191,255,0.15)) !important;
    border: 1px solid var(--blue-border) !important;
    color: var(--blue) !important;
    transition: all 0.2s ease !important;
}

div.stDownloadButton > button:hover {
    background: linear-gradient(135deg, rgba(0,128,179,0.40), rgba(0,191,255,0.30)) !important;
    box-shadow: 0 0 20px rgba(0,191,255,0.25) !important;
}

/* ── Inputs ──────────────────────────────── */
input, textarea,
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.10) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-main) !important;
    font-family: 'Plus Jakarta Sans', 'Cairo', sans-serif !important;
    transition: border-color 0.2s !important;
}

input:focus, textarea:focus {
    border-color: var(--blue) !important;
    box-shadow: 0 0 0 2px rgba(0,191,255,0.15) !important;
    outline: none !important;
}

[data-testid="stNumberInput"] button {
    border-color: var(--blue-border) !important;
    color: var(--blue) !important;
}

/* ── Selectbox ───────────────────────────── */
div[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.04) !important;
    border-color: rgba(255,255,255,0.10) !important;
    border-radius: var(--radius-sm) !important;
    transition: border-color 0.2s !important;
}

div[data-baseweb="select"] > div:focus-within {
    border-color: var(--blue) !important;
    box-shadow: 0 0 0 2px rgba(0,191,255,0.15) !important;
}

/* ── Radio ───────────────────────────────── */
[data-testid="stRadio"] input[type="radio"] { accent-color: var(--blue) !important; }
[data-testid="stRadio"] label { gap: 10px !important; }

/* ── DataFrames / Tables ─────────────────── */
[data-testid="stDataFrame"] {
    border-radius: var(--radius-lg) !important;
    overflow: hidden !important;
    border: 1px solid rgba(0,191,255,0.18) !important;
}

/* ── Divider ─────────────────────────────── */
hr { border-color: rgba(255,255,255,0.07) !important; margin: 32px 0 !important; }

/* ── Scrollbar ───────────────────────────── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: rgba(255,255,255,0.03); }
::-webkit-scrollbar-thumb { background: rgba(0,191,255,0.30); border-radius: 3px; }

/* ── Cards ───────────────────────────────── */
.vv-card {
    background: linear-gradient(145deg, rgba(255,255,255,0.038), rgba(255,255,255,0.018));
    border: 1px solid var(--blue-border);
    border-radius: var(--radius-lg);
    padding: 26px 30px;
    margin-bottom: 20px;
    transition: border-color 0.25s, box-shadow 0.25s, transform 0.2s;
    position: relative;
    overflow: hidden;
}

.vv-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(0,191,255,0.4), transparent);
}

.vv-card:hover {
    border-color: rgba(0,191,255,0.55);
    box-shadow: 0 6px 28px rgba(0,191,255,0.10);
    transform: translateY(-1px);
}

.vv-card-title {
    font-size: 18px;
    font-weight: 800;
    color: var(--blue);
    margin-bottom: 12px;
    letter-spacing: 0.2px;
    font-family: 'Plus Jakarta Sans', 'Cairo', sans-serif;
}

.vv-card-text {
    font-size: 15px;
    color: var(--text-sub);
    line-height: 1.75;
    font-family: 'Plus Jakarta Sans', 'Cairo', sans-serif;
}

.vv-card-list {
    margin-top: 14px;
    padding-left: 20px;
    list-style: none;
    padding-left: 0;
}

.vv-card-list li {
    position: relative;
    padding-left: 20px;
    margin-bottom: 8px;
    color: #B8C8D8;
    font-size: 14.5px;
    line-height: 1.6;
}

.vv-card-list li::before {
    content: '›';
    position: absolute;
    left: 0;
    color: var(--blue);
    font-weight: 700;
    font-size: 16px;
}

/* RTL list arrows */
[dir="rtl"] .vv-card-list li { padding-left: 0; padding-right: 20px; }
[dir="rtl"] .vv-card-list li::before { left: auto; right: 0; }

/* ── Result card ─────────────────────────── */
.result-card {
    border-radius: var(--radius-lg);
    padding: 22px 26px;
    margin-bottom: 16px;
    background: linear-gradient(145deg, rgba(255,255,255,0.035), rgba(255,255,255,0.015));
    transition: box-shadow 0.2s, transform 0.2s;
    position: relative;
    overflow: hidden;
}

.result-card:hover {
    box-shadow: 0 6px 24px rgba(0,0,0,0.20);
    transform: translateY(-1px);
}

/* ── Section title ───────────────────────── */
.vv-section-title {
    font-family: 'Plus Jakarta Sans', 'Cairo', sans-serif;
    font-weight: 800;
    color: #F0F4F8;
    margin-top: 34px;
    margin-bottom: 16px;
    letter-spacing: -0.3px;
    position: relative;
    display: flex;
    align-items: center;
    gap: 10px;
}

.vv-section-title::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, rgba(0,191,255,0.25), transparent);
}

/* ── Misc helpers ────────────────────────── */
.small-muted { color: var(--text-muted); font-size: 13px; }
.badge {
    display: inline-flex;
    align-items: center;
    padding: 4px 14px;
    border-radius: 999px;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.3px;
}

/* ── Stats mini-card ─────────────────────── */
.stat-mini {
    min-width: 0 !important;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: var(--radius-md);
    padding: 14px 18px;
    text-align: center;
    transition: border-color 0.2s;
}

.stat-mini:hover { border-color: var(--blue-border); }
.stat-number { font-size: 28px; font-weight: 800; line-height: 1.1; }
.stat-label  { font-size: 12px; color: var(--text-muted); margin-top: 4px; letter-spacing: 0.4px; text-transform: uppercase; }

/* ── Disclaimer banner ───────────────────── */
.disclaimer-banner {
    background: linear-gradient(135deg, rgba(255,193,7,0.08), rgba(255,152,0,0.05));
    border: 1px solid rgba(255,193,7,0.30);
    border-radius: var(--radius-md);
    padding: 16px 20px;
    margin-top: 24px;
    display: flex;
    align-items: flex-start;
    gap: 12px;
}

.disclaimer-icon { font-size: 20px; flex-shrink: 0; margin-top: 1px; }
.disclaimer-title { font-size: 14px; font-weight: 700; color: #FFD54F; margin-bottom: 4px; }
.disclaimer-text  { font-size: 13.5px; color: #D4C5A0; line-height: 1.6; }

/* ── Responsive ──────────────────────────── */
@media (max-width: 768px) {
    .block-container {
        max-width: 100% !important;
        width: 100% !important;
        padding-left: 0.75rem !important;
        padding-right: 0.75rem !important;
    }

    .stat-mini {
        min-width: 0 !important;
        padding: 10px 6px !important;
    }

    .stat-label {
        font-size: 10px !important;
        white-space: normal !important;
        word-break: break-word !important;
    }
}

</style>
""", unsafe_allow_html=True)

# =========================================
# Display settings
# =========================================
settings_left, lang_center, theme_center = st.columns([3.55, 0.8, 1.45])

old_language = st.session_state.get("language", "English")

if st.session_state.get("language_segment") not in ["English", "العربية"]:
    st.session_state["language_segment"] = old_language

with lang_center:
    language = st.segmented_control(
        "Language / اللغة",
        ["English", "العربية"],
        format_func=lambda value: "EN" if value == "English" else "AR",
        label_visibility="collapsed",
        key="language_segment",
        width="content",
    )

if language is None:
    language = old_language

if language != old_language:
    st.session_state["language"] = language
    st.session_state["language_changed"] = True
else:
    st.session_state["language"] = language

theme_labels = {
    "Dark": "Dark",
    "Light": "Light",
}

if st.session_state.get("theme_segment") not in ["Dark", "Light"]:
    st.session_state["theme_segment"] = st.session_state["theme_mode"]

with theme_center:
    theme_mode = st.segmented_control(
        "Theme / المظهر",
        ["Dark", "Light"],
        format_func=lambda value: theme_labels[value],
        label_visibility="collapsed",
        key="theme_segment",
        width="content",
    )

if theme_mode is None:
    theme_mode = st.session_state["theme_mode"]

st.session_state["theme_mode"] = theme_mode

is_light_theme = theme_mode == "Light"
is_arabic = language == "العربية"

if is_light_theme:
    app_bg = "#F6FAFC"
    surface_bg = "#FFFFFF"
    card_bg = "linear-gradient(145deg, rgba(255,255,255,0.98), rgba(238,247,251,0.92))"
    inner_bg = "rgba(7, 51, 73, 0.045)"
    control_bg = "rgba(255,255,255,0.88)"
    text_main = "#132938"
    text_sub = "#365468"
    text_muted = "#647C8D"
    border_soft = "rgba(10, 88, 120, 0.16)"
    tab_bg = "rgba(255,255,255,0.72)"
    settings_bg = "rgba(255,255,255,0.68)"
    shadow_soft = "0 8px 28px rgba(12, 62, 85, 0.08)"
    divider_bg = "rgba(10, 88, 120, 0.12)"
else:
    app_bg = "#060d14"
    surface_bg = "rgba(255,255,255,0.032)"
    card_bg = "linear-gradient(145deg, rgba(255,255,255,0.038), rgba(255,255,255,0.018))"
    inner_bg = "rgba(255,255,255,0.03)"
    control_bg = "rgba(255,255,255,0.04)"
    text_main = "#F0F4F8"
    text_sub = "#B8C8D8"
    text_muted = "#8A9BAD"
    border_soft = "rgba(255,255,255,0.10)"
    tab_bg = "rgba(255,255,255,0.025)"
    settings_bg = "rgba(255,255,255,0.035)"
    shadow_soft = "0 6px 24px rgba(0,0,0,0.20)"
    divider_bg = "rgba(255,255,255,0.07)"

# Direction and theme styles
st.markdown(f"""
<style>
:root {{
    --bg-app: {app_bg};
    --bg-surface: {surface_bg};
    --bg-card: {card_bg};
    --bg-inner: {inner_bg};
    --bg-control: {control_bg};
    --text-main: {text_main};
    --text-sub: {text_sub};
    --text-muted: {text_muted};
    --border-soft: {border_soft};
    --tab-bg: {tab_bg};
    --settings-bg: {settings_bg};
    --shadow-soft: {shadow_soft};
    --divider-soft: {divider_bg};
}}

html, body, [data-testid="stAppViewContainer"] {{
    direction: {"rtl" if is_arabic else "ltr"};
    text-align: {"right" if is_arabic else "left"};
    background: var(--bg-app) !important;
    color: var(--text-main) !important;
}}

[data-testid="stAppViewContainer"] > .main,
[data-testid="stHeader"],
[data-testid="stToolbar"],
.block-container {{
    background: transparent !important;
    color: var(--text-main) !important;
}}

.stTabs [data-baseweb="tab-list"] {{
    background: var(--tab-bg) !important;
    border-color: var(--border-soft) !important;
    box-shadow: var(--shadow-soft) !important;
}}

.stTabs [data-baseweb="tab"] {{
    color: var(--text-muted) !important;
}}

[data-testid="stSegmentedControl"] {{
    width: fit-content !important;
    max-width: 100% !important;
    margin-left: auto !important;
    margin-right: auto !important;
}}

[data-testid="stSegmentedControl"] div[role="group"] {{
    width: fit-content !important;
    max-width: 100% !important;
    display: inline-flex !important;
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    align-items: center !important;
    justify-content: center !important;
    overflow-x: auto !important;
    background: var(--settings-bg) !important;
    border: 1px solid var(--border-soft) !important;
    border-radius: 999px !important;
    padding: 3px !important;
    box-shadow: 0 6px 18px rgba(12, 62, 85, 0.06) !important;
    backdrop-filter: blur(12px) !important;
}}

[data-testid="stSegmentedControl"] button {{
    flex: 0 0 auto !important;
    min-width: 44px !important;
    min-height: 30px !important;
    white-space: nowrap !important;
    border-radius: 999px !important;
    border: 0 !important;
    background: transparent !important;
    color: var(--text-main) !important;
    font-size: 12px !important;
    font-weight: 700 !important;
    letter-spacing: 0 !important;
    padding: 0 12px !important;
}}

[data-testid="stSegmentedControl"] button[aria-pressed="true"] {{
    background: rgba(0,191,255,0.16) !important;
    color: var(--blue) !important;
    box-shadow: inset 0 0 0 1px rgba(0,191,255,0.24) !important;
}}

.st-key-main_nav_container {{
    width: 100% !important;
    display: flex !important;
    justify-content: center !important;
}}

.st-key-main_nav_container [data-testid="stSegmentedControl"] {{
    margin-left: auto !important;
    margin-right: auto !important;
}}

div[role="radiogroup"][aria-label="button group"] {{
    width: fit-content !important;
    max-width: 100% !important;
    display: inline-flex !important;
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    align-items: center !important;
    margin-left: auto !important;
    margin-right: auto !important;
    overflow-x: auto !important;
    background: var(--settings-bg) !important;
    border: 1px solid var(--border-soft) !important;
    border-radius: 999px !important;
    padding: 3px !important;
    box-shadow: 0 6px 18px rgba(12, 62, 85, 0.06) !important;
    backdrop-filter: blur(12px) !important;
}}

div[role="radiogroup"][aria-label="button group"] button {{
    flex: 0 0 auto !important;
    min-width: 44px !important;
    min-height: 30px !important;
    white-space: nowrap !important;
    border-radius: 999px !important;
    border: 1px solid transparent !important;
    background: transparent !important;
    color: var(--text-main) !important;
    font-size: 12px !important;
    font-weight: 700 !important;
    letter-spacing: 0 !important;
    padding: 0 12px !important;
}}

div[role="radiogroup"][aria-label="button group"] button[class*="e7msn5c13"] {{
    background: rgba(0,191,255,0.16) !important;
    border-color: rgba(0,191,255,0.24) !important;
    color: var(--blue) !important;
    box-shadow: none !important;
}}

[data-testid="stRadio"] {{
    max-width: 760px !important;
    margin-top: -2px !important;
    margin-bottom: 26px !important;
}}

[data-testid="stRadio"] div[role="radiogroup"] {{
    display: grid !important;
    grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
    gap: 10px !important;
    padding: 6px !important;
    border: 1px solid var(--border-soft) !important;
    border-radius: 16px !important;
    background: var(--settings-bg) !important;
    box-shadow: var(--shadow-soft) !important;
}}

[data-testid="stRadio"] label {{
    position: relative !important;
    min-height: 58px !important;
    padding: 14px 18px !important;
    border-radius: 12px !important;
    border: 1px solid transparent !important;
    background: transparent !important;
    transition: all 0.18s ease !important;
    cursor: pointer !important;
}}

[data-testid="stRadio"] label:hover {{
    border-color: rgba(0,191,255,0.22) !important;
    background: var(--bg-inner) !important;
}}

[data-testid="stRadio"] input[type="radio"] {{
    position: absolute !important;
    opacity: 0 !important;
    pointer-events: none !important;
}}

[data-testid="stRadio"] label > div:first-child {{
    display: none !important;
}}

[data-testid="stRadio"] label:has(input[type="radio"]:checked) {{
    border-color: rgba(0,191,255,0.32) !important;
    background: linear-gradient(135deg, rgba(0,191,255,0.16), rgba(0,191,255,0.07)) !important;
    box-shadow: inset 0 0 0 1px rgba(0,191,255,0.08) !important;
}}

[data-testid="stRadio"] label p {{
    color: var(--text-sub) !important;
    font-size: 15px !important;
    font-weight: 700 !important;
    letter-spacing: 0 !important;
}}

[data-testid="stRadio"] label:has(input[type="radio"]:checked) p {{
    color: var(--blue) !important;
}}

@media (max-width: 640px) {{
    [data-testid="stSegmentedControl"],
    [data-testid="stSegmentedControl"] div[role="group"],
    div[role="radiogroup"][aria-label="button group"] {{
        width: 100% !important;
    }}

    [data-testid="stSegmentedControl"] button,
    div[role="radiogroup"][aria-label="button group"] button {{
        flex: 1 1 0 !important;
        min-width: 0 !important;
        padding-left: 8px !important;
        padding-right: 8px !important;
    }}

    [data-testid="stRadio"] div[role="radiogroup"] {{
        grid-template-columns: 1fr !important;
    }}
}}


input, textarea,
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
div[data-baseweb="select"] > div {{
    background: var(--bg-control) !important;
    border-color: var(--border-soft) !important;
    color: var(--text-main) !important;
}}

div[data-baseweb="input"],
div[data-baseweb="input"] > div {{
    background: var(--bg-control) !important;
    border-color: var(--border-soft) !important;
    color: var(--text-main) !important;
}}

div[data-baseweb="input"] input,
div[data-baseweb="select"] input {{
    background: transparent !important;
    color: var(--text-main) !important;
    caret-color: var(--blue) !important;
}}

div[data-baseweb="select"] span,
div[data-baseweb="select"] svg {{
    color: var(--text-main) !important;
    fill: var(--text-main) !important;
}}

div[data-baseweb="popover"],
div[data-baseweb="popover"] > div,
div[data-baseweb="popover"] [data-baseweb="menu"],
div[data-baseweb="popover"] [role="listbox"] {{
    background: var(--bg-surface) !important;
    color: var(--text-main) !important;
    border: 1px solid var(--border-soft) !important;
    box-shadow: var(--shadow-soft) !important;
}}

div[data-baseweb="popover"] * {{
    color: var(--text-main) !important;
}}

div[data-baseweb="popover"] [role="option"],
div[data-baseweb="popover"] li {{
    background: var(--bg-surface) !important;
    color: var(--text-main) !important;
}}

div[data-baseweb="popover"] [role="option"]:hover,
div[data-baseweb="popover"] [role="option"][aria-selected="true"],
div[data-baseweb="popover"] li:hover {{
    background: var(--bg-inner) !important;
    background-color: var(--bg-inner) !important;
}}

div[data-baseweb="popover"] [role="option"] > div,
div[data-baseweb="popover"] [role="option"] span {{
    background: transparent !important;
    background-color: transparent !important;
    color: var(--text-main) !important;
}}

div[data-baseweb="popover"] [role="option"][aria-selected="true"],
div[data-baseweb="popover"] [role="option"][aria-selected="true"] > div {{
    background: rgba(0,191,255,0.12) !important;
    background-color: rgba(0,191,255,0.12) !important;
    color: var(--text-main) !important;
}}

html body div[data-baseweb="popover"] div[role="option"],
html body div[data-baseweb="popover"] div[role="option"] * {{
    color: var(--text-main) !important;
}}

html body div[data-baseweb="popover"] div[role="option"][aria-selected="true"],
html body div[data-baseweb="popover"] div[role="option"][aria-selected="true"] * {{
    background: rgba(0,191,255,0.12) !important;
    background-color: rgba(0,191,255,0.12) !important;
    color: #FFFFFF !important;
}}

div.stButton > button {{
    background: var(--bg-control) !important;
    color: var(--text-main) !important;
    border-color: var(--blue-border) !important;
    min-height: 50px !important;
    border-radius: 14px !important;
    box-shadow: 0 8px 22px rgba(0,0,0,0.08) !important;
}}

div.stButton > button:hover {{
    background: rgba(0,191,255,0.12) !important;
    border-color: rgba(0,191,255,0.42) !important;
    transform: translateY(-1px) !important;
}}

div.stButton > button p {{
    font-size: 14px !important;
    font-weight: 750 !important;
    letter-spacing: 0 !important;
}}

div.stButton > button[kind="primary"] {{
    background: linear-gradient(135deg, #0088B8, #00BFFF) !important;
    color: #FFFFFF !important;
    border-color: transparent !important;
    box-shadow: 0 10px 24px rgba(0,191,255,0.24) !important;
}}

[data-testid="stNumberInput"] button {{
    background: var(--bg-control) !important;
    border-color: var(--border-soft) !important;
    color: var(--blue) !important;
}}

.vv-card,
.result-card,
.stat-mini {{
    background: var(--bg-card) !important;
    border-color: var(--border-soft) !important;
    box-shadow: var(--shadow-soft) !important;
    color: var(--text-main) !important;
}}

.vv-section-title,
.stat-number {{
    color: var(--text-main) !important;
}}

.vv-card-text,
.vv-card-list li,
.small-muted,
.stat-label,
.disclaimer-text,
label,
p {{
    color: var(--text-sub) !important;
}}

hr {{
    border-color: var(--divider-soft) !important;
}}

[data-testid="stDataFrame"] {{
    background: var(--bg-surface) !important;
    border-color: var(--border-soft) !important;
}}

.result-card [style*="background:rgba(255,255,255"],
.vv-card [style*="background:rgba(255,255,255"],
.stat-mini [style*="background:rgba(255,255,255"] {{
    background: var(--bg-inner) !important;
    border-color: var(--border-soft) !important;
}}

.result-card [style*="color:#F0F4F8"],
.vv-card [style*="color:#F0F4F8"],
.stat-mini [style*="color:#F0F4F8"],
table [style*="color:#F0F4F8"] {{
    color: var(--text-main) !important;
}}

.result-card [style*="color:#B8C8D8"],
.result-card [style*="color:#7A9BB5"],
.result-card [style*="color:#9AAAB8"],
.vv-card [style*="color:#B8C8D8"],
.vv-card [style*="color:#7A9BB5"],
.vv-card [style*="color:#9AAAB8"],
table [style*="color:#B8C8D8"],
table [style*="color:#7A9BB5"],
table [style*="color:#9AAAB8"] {{
    color: var(--text-sub) !important;
}}

[style*="color:#F0F4F8"] {{
    color: var(--text-main) !important;
}}

[style*="color:#B8C8D8"],
[style*="color:#7A9BB5"],
[style*="color:#9AAAB8"] {{
    color: var(--text-sub) !important;
}}

[style*="background:rgba(255,255,255"] {{
    background: var(--bg-inner) !important;
}}

[style*="border:1px solid rgba(255,255,255"],
[style*="border: 1px solid rgba(255,255,255"] {{
    border-color: var(--border-soft) !important;
}}

[style*="border-bottom:1px solid rgba(255,255,255"],
[style*="border-bottom: 1px solid rgba(255,255,255"] {{
    border-bottom-color: var(--border-soft) !important;
}}

.js-plotly-plot .plotly .gtitle,
.js-plotly-plot .plotly .xtick text,
.js-plotly-plot .plotly .ytick text,
.js-plotly-plot .plotly .legendtext {{
    fill: var(--text-sub) !important;
}}

.vv-card-text, .vv-card-list, .small-muted,
.disclaimer-text, .result-explanation,
li, p, label {{
    direction: {"rtl" if is_arabic else "ltr"};
    text-align: {"right" if is_arabic else "left"};
    font-family: {"'Cairo', sans-serif" if is_arabic else "'Plus Jakarta Sans', sans-serif"} !important;
}}

.vv-card-list {{
    padding-right: {"20px" if is_arabic else "0"} !important;
    padding-left: {"0" if is_arabic else "20px"} !important;
}}

.vv-card-list li {{
    padding-left: {"0" if is_arabic else "20px"} !important;
    padding-right: {"20px" if is_arabic else "0"} !important;
    text-align: {"right" if is_arabic else "left"} !important;
}}

.vv-card-list li::before {{
    left: {"auto" if is_arabic else "0"} !important;
    right: {"0" if is_arabic else "auto"} !important;
}}

[data-testid="stRadio"] label > div:last-child {{
    margin-right: {"8px" if is_arabic else "0"} !important;
    margin-left: {"0" if is_arabic else "8px"} !important;
}}

.vv-section-title::after {{
    background: linear-gradient({"270deg" if is_arabic else "90deg"}, rgba(0,191,255,0.25), transparent) !important;
}}
</style>
""", unsafe_allow_html=True)

# =========================================
# Helpers
# =========================================
def tr(en, ar):
    return en if language == "English" else ar

def section_title(text_value, size=26, icon=""):
    icon_html = f'<span style="font-size:{size-4}px">{icon}</span>' if icon else ""
    st.html(f"""
    <div class="vv-section-title" style="font-size:{size}px;">
        {icon_html}{text_value}
    </div>
    """)

# =========================================
# Header
# =========================================
def render_header():
    subtitle = tr("Smart Insight for Vitamin Health", "رؤية ذكية لصحة الفيتامينات")
    vision_shadow = (
        "0 2px 8px rgba(0,191,255,0.25)"
        if is_light_theme
        else "0 0 4px rgba(0,191,255,0.60), 0 0 12px rgba(0,191,255,0.35), 0 0 24px rgba(0,191,255,0.15)"
    )
    st.html(f"""
<div style="text-align:center; padding: 20px 0 12px; position: relative;">
    <div style="
        position: absolute; top: 0; left: 50%; transform: translateX(-50%);
        width: 300px; height: 80px;
        background: radial-gradient(ellipse, rgba(0,191,255,0.07) 0%, transparent 70%);
        pointer-events: none;
    "></div>
    <h1 style="
        font-size: 52px;
        font-weight: 800;
        letter-spacing: -1.5px;
        margin: 0 0 8px;
        font-family: 'Plus Jakarta Sans', 'Cairo', sans-serif;
        line-height: 1;
    ">
        <span style="color:var(--text-main);">Vita</span><span style="
            color:var(--blue);
            text-shadow:{vision_shadow};
        ">Vision</span>
    </h1>
    <div style="
        font-size: 16px;
        color: var(--text-muted);
        letter-spacing: 0.5px;
        font-family: 'Plus Jakarta Sans', 'Cairo', sans-serif;
    ">{subtitle}</div>
    <div style="
        width: 50px; height: 2px;
        background: linear-gradient(90deg, transparent, #00BFFF, transparent);
        margin: 14px auto 0;
        border-radius: 2px;
    "></div>
</div>
""")

# =========================================
# Navigation tabs
# =========================================
render_header()

nav_options = ["home", "dashboard", "about"]
if st.session_state.get("active_nav") not in nav_options:
    st.session_state["active_nav"] = "home"

nav_labels = {
    "home": tr("Home", "الرئيسية"),
    "dashboard": tr("Dashboard", "لوحة التحكم"),
    "about": tr("About", "حول"),
}

with st.container(
    key="main_nav_container",
    horizontal=True,
    horizontal_alignment="center",
    vertical_alignment="center",
):
    active_tab = st.segmented_control(
        tr("Navigation", "التنقل"),
        nav_options,
        format_func=lambda value: nav_labels[value],
        label_visibility="collapsed",
        key="active_nav",
        width="content",
    )

if active_tab is None:
    active_tab = "home"

# =========================================
# Reference ranges (unchanged)
# =========================================
REFERENCE_RANGES = {
    "Zinc":      {"low": 66,   "high": 106,  "unit": "µg/dL",  "max_reasonable": 300},
    "Vitamin_E": {"low": 500,  "high": 2000, "unit": "µg/dL",  "max_reasonable": 5000},
    "Vitamin_A": {"low": 28,   "high": 86,   "unit": "µg/dL",  "max_reasonable": 250},
    "Vitamin_D": {"low": 20,   "high": 50,   "unit": "ng/mL",  "max_reasonable": 200},
    "Vitamin_C": {"low": 0.4,  "high": 2.0,  "unit": "mg/dL",  "max_reasonable": 5},
    "Magnesium": {"low": 1.7,  "high": 2.2,  "unit": "mg/dL",  "max_reasonable": 5},
    "Folate":    {"low": 3,    "high": 20,   "unit": "ng/mL",  "max_reasonable": 60},
    "Vitamin_K": {"low": 0.10, "high": 2.20, "unit": "ng/mL",  "max_reasonable": 8},
    "B12":       {"low": 200,  "high": 900,  "unit": "pg/mL",  "max_reasonable": 3000},
    "B6":        {"low": 20,   "high": 100,  "unit": "nmol/L", "max_reasonable": 400},
    "Calcium":   {"low": 8.6,  "high": 10.2, "unit": "mg/dL",  "max_reasonable": 16},
}

NUTRIENT_ALIASES = {
    "zinc": "Zinc",
    "vitamin e": "Vitamin_E",
    "vitamin_e": "Vitamin_E",
    "vitamin a": "Vitamin_A",
    "vitamin_a": "Vitamin_A",
    "vitamin d": "Vitamin_D",
    "vitamin_d": "Vitamin_D",
    "vitamin c": "Vitamin_C",
    "vitamin_c": "Vitamin_C",
    "magnesium": "Magnesium",
    "folate": "Folate",
    "vitamin k": "Vitamin_K",
    "vitamin_k": "Vitamin_K",
    "vitamin b12": "B12",
    "vitamin_b12": "B12",
    "b12": "B12",
    "vitamin b6": "B6",
    "vitamin_b6": "B6",
    "b6": "B6",
    "calcium": "Calcium",
    "ferritin": "Ferritin",
}

def normalize_nutrient_name(nutrient):
    raw_name = str(nutrient or "").strip()
    if not raw_name:
        return ""
    simplified = " ".join(raw_name.replace("-", " ").replace("_", " ").split()).lower()
    return NUTRIENT_ALIASES.get(simplified, raw_name)

# =========================================
# Nutrient display names
# =========================================
def nutrient_display_name(nutrient):
    nutrient = normalize_nutrient_name(nutrient)
    names = {
        "Zinc":      tr("Zinc",       "الزنك"),
        "Vitamin_E": tr("Vitamin E",  "فيتامين E"),
        "Vitamin_A": tr("Vitamin A",  "فيتامين A"),
        "Vitamin_D": tr("Vitamin D",  "فيتامين D"),
        "Vitamin_C": tr("Vitamin C",  "فيتامين C"),
        "Magnesium": tr("Magnesium",  "المغنيسيوم"),
        "Folate":    tr("Folate",     "الفولات"),
        "Vitamin_K": tr("Vitamin K",  "فيتامين K"),
        "B12":       tr("Vitamin B12","فيتامين B12"),
        "B6":        tr("Vitamin B6", "فيتامين B6"),
        "Calcium":   tr("Calcium",    "الكالسيوم"),
        "Ferritin":  tr("Ferritin",   "الفيريتين"),
    }
    return names.get(nutrient, nutrient)

def nutrient_display_name_en(nutrient):
    nutrient = normalize_nutrient_name(nutrient)
    names = {
        "Zinc": "Zinc",
        "Vitamin_E": "Vitamin E",
        "Vitamin_A": "Vitamin A",
        "Vitamin_D": "Vitamin D",
        "Vitamin_C": "Vitamin C",
        "Magnesium": "Magnesium",
        "Folate": "Folate",
        "Vitamin_K": "Vitamin K",
        "B12": "Vitamin B12",
        "B6": "Vitamin B6",
        "Calcium": "Calcium",
        "Ferritin": "Ferritin",
    }
    return names.get(nutrient, nutrient)

# =========================================
# Ferritin range & helpers (unchanged logic)
# =========================================
def get_ferritin_range(gender):
    if gender in [1, "1", "Male", "male", "M", "m", "ذكر"]:
        return {"low": 30,  "high": 400, "unit": "ng/mL", "max_reasonable": 1200}
    return     {"low": 13,  "high": 150, "unit": "ng/mL", "max_reasonable": 800}

def normalize_gender(gender):
    if gender in [1, "1", "Male", "male", "M", "m", "ذكر"]:   return "Male"
    if gender in [2, "2", "Female", "female", "F", "f", "أنثى"]: return "Female"
    return "Male"

def get_range(nutrient, gender):
    nutrient = normalize_nutrient_name(nutrient)
    if nutrient == "Ferritin":
        return get_ferritin_range(gender)
    return REFERENCE_RANGES.get(nutrient)

# =========================================
# Machine learning model helpers
# =========================================
MODEL_PATH = Path(__file__).resolve().parent / "models" / "vitavision_unified_model.pkl"
MODEL_UNAVAILABLE = "Unavailable"
MODEL_RESULT_COLUMNS = ["ML Prediction", "ML Confidence", "Model Agreement"]
MODEL_VALID_STATUSES = ["Deficient", "Normal", "Excessive"]
MODEL_NUTRIENT_NAME_MAP = {
    "Vitamin_D": "Vitamin D",
    "Vitamin D": "Vitamin D",
    "Vitamin_C": "Vitamin C",
    "Vitamin C": "Vitamin C",
    "Vitamin_A": "Vitamin A",
    "Vitamin A": "Vitamin A",
    "Vitamin_E": "Vitamin E",
    "Vitamin E": "Vitamin E",
    "Vitamin_K": "Vitamin K",
    "Vitamin K": "Vitamin K",
    "B12": "Vitamin B12",
    "Vitamin_B12": "Vitamin B12",
    "Vitamin B12": "Vitamin B12",
    "B6": "Vitamin B6",
    "Vitamin_B6": "Vitamin B6",
    "Vitamin B6": "Vitamin B6",
}

def unavailable_model_fields():
    return {
        "ML Prediction": MODEL_UNAVAILABLE,
        "ML Confidence": MODEL_UNAVAILABLE,
        "Model Agreement": MODEL_UNAVAILABLE,
    }

@st.cache_resource(show_spinner=False)
def load_vitavision_model():
    if not MODEL_PATH.exists():
        return None
    try:
        return joblib.load(MODEL_PATH)
    except Exception:
        return None

def nutrient_model_name(nutrient):
    nutrient = normalize_nutrient_name(nutrient)
    return MODEL_NUTRIENT_NAME_MAP.get(nutrient, nutrient)

def build_model_input(age, gender, nutrient, value):
    numeric_age = pd.to_numeric(age, errors="coerce")
    numeric_value = pd.to_numeric(value, errors="coerce")
    if pd.isna(numeric_age) or pd.isna(numeric_value):
        return None

    gender_value = 1 if normalize_gender(gender) == "Male" else 2
    return pd.DataFrame([{
        "Age": float(numeric_age),
        "Gender": gender_value,
        "Nutrient": nutrient_model_name(nutrient),
        "Value": float(numeric_value),
    }])

def model_confidence(model, model_input):
    if not hasattr(model, "predict_proba"):
        return MODEL_UNAVAILABLE
    try:
        probabilities = model.predict_proba(model_input)[0]
        confidence = max(float(probability) for probability in probabilities)
    except Exception:
        return MODEL_UNAVAILABLE
    return f"{confidence * 100:.1f}%"

def predict_model_fields(age, gender, nutrient, value, status):
    if status not in MODEL_VALID_STATUSES:
        return unavailable_model_fields()

    model = load_vitavision_model()
    model_input = build_model_input(age, gender, nutrient, value)
    if model is None or model_input is None:
        return unavailable_model_fields()

    try:
        prediction = str(model.predict(model_input)[0])
    except Exception:
        return unavailable_model_fields()

    return {
        "ML Prediction": prediction,
        "ML Confidence": model_confidence(model, model_input),
        "Model Agreement": "Agree" if prediction == status else "Different",
    }

def ml_prediction_text(prediction):
    prediction = str(prediction or MODEL_UNAVAILABLE)
    if prediction in MODEL_VALID_STATUSES:
        return status_text(prediction)
    return tr("Unavailable", "غير متوفر")

def model_agreement_text(agreement):
    return {
        "Agree": tr("Agree", "متطابق"),
        "Different": tr("Different", "مختلف"),
        MODEL_UNAVAILABLE: tr("Unavailable", "غير متوفر"),
    }.get(str(agreement or MODEL_UNAVAILABLE), str(agreement or MODEL_UNAVAILABLE))

def model_agreement_color(agreement):
    return {
        "Agree": "#1DB954",
        "Different": "#FFA500",
        MODEL_UNAVAILABLE: "#7A9BB5",
    }.get(str(agreement or MODEL_UNAVAILABLE), "#7A9BB5")

def validate_value(value, range_info):
    if value is None:
        return False, tr("Missing or non-numeric value.", "القيمة مفقودة أو غير رقمية.")
    if pd.isna(value):
        return False, tr("Missing or non-numeric value.", "القيمة مفقودة أو غير رقمية.")
    if value <= 0:
        return False, tr("Value must be greater than zero.", "القيمة يجب أن تكون أكبر من صفر.")
    if value > range_info["max_reasonable"]:
        return False, tr(
            "Please check the input value. It looks unusually high.",
            "تأكد من المدخلات، القيمة تبدو مرتفعة بشكل غير منطقي."
        )
    return True, ""

def classify_value(value, low, high):
    if value < low:  return "Deficient"
    if value <= high: return "Normal"
    return "Excessive"

def status_text(status):
    mapping = {
        "Deficient": tr("Deficient",     "ناقص"),
        "Normal":    tr("Normal",         "طبيعي"),
        "Excessive": tr("Excessive",      "مرتفع"),
        "Invalid":   tr("Invalid Input",  "مدخل غير منطقي"),
        "Unknown":   tr("Unknown",        "غير معروف"),
        "Error":     tr("Error",          "خطأ"),
    }
    return mapping.get(status, status)

def status_color(status):
    colors = {
        "Deficient": "#FF4B4B",
        "Normal":    "#1DB954",
        "Excessive": "#FFA500",
        "Invalid":   "#00BFFF",
        "Unknown":   "#888888",
        "Error":     "#888888",
    }
    return colors.get(status, "#888888")

def status_icon(status):
    icons = {
        "Deficient": "",
        "Normal":    "",
        "Excessive": "",
        "Invalid":   "",
        "Unknown":   "—",
        "Error":     "",
    }
    return icons.get(status, "—")

def get_explanation(nutrient, value, unit, status, low, high):
    name = nutrient_display_name(nutrient)
    if status == "Deficient":
        return tr(
            f"Your {name} level is below the normal range ({low}–{high} {unit}).",
            f"مستوى {name} أقل من النطاق الطبيعي ({low}–{high} {unit})."
        )
    if status == "Normal":
        return tr(
            f"Your {name} level is within the normal range ({low}–{high} {unit}).",
            f"مستوى {name} ضمن النطاق الطبيعي ({low}–{high} {unit})."
        )
    return tr(
        f"Your {name} level is above the normal range ({low}–{high} {unit}).",
        f"مستوى {name} أعلى من النطاق الطبيعي ({low}–{high} {unit})."
    )

def get_possible_causes(nutrient, status):
    causes_en = {
        "Deficient": {
            "Vitamin_D": ["Low sunlight exposure", "Low dietary intake"],
            "Vitamin_C": ["Low fruit intake", "Poor nutrition"],
            "Vitamin_A": ["Low intake", "Absorption issues"],
            "Vitamin_E": ["Poor fat absorption"],
            "Vitamin_K": ["Low leafy greens intake"],
            "B12": ["Low animal products", "Absorption problems"],
            "B6": ["Poor diet"],
            "Folate": ["Low vegetables intake"],
            "Ferritin": ["Low iron intake", "Blood loss"],
            "Zinc": ["Poor nutrition"],
            "Magnesium": ["Low intake", "Digestive loss"],
            "Calcium": ["Low intake", "Vitamin D deficiency"],
        },
        "Normal": {"default": ["Balanced nutrition"]},
        "Excessive": {
            "Vitamin_D": ["High supplement intake"],
            "Vitamin_C": ["Excess supplements"],
            "Vitamin_A": ["Over supplementation"],
            "Vitamin_E": ["Supplement overuse"],
            "Vitamin_K": ["High intake"],
            "B12": ["Supplement use"],
            "B6": ["Over supplementation"],
            "Folate": ["Excess supplements"],
            "Ferritin": ["Inflammation", "Iron overload"],
            "Zinc": ["High supplements"],
            "Magnesium": ["Supplement overuse"],
            "Calcium": ["High intake"],
        },
    }
    causes_ar = {
        "Deficient": {
            "Vitamin_D": ["قلة التعرض للشمس", "انخفاض المدخول الغذائي"],
            "Vitamin_C": ["قلة تناول الفواكه", "ضعف التغذية"],
            "Vitamin_A": ["انخفاض المدخول", "مشاكل امتصاص"],
            "Vitamin_E": ["ضعف امتصاص الدهون"],
            "Vitamin_K": ["قلة تناول الخضار الورقية"],
            "B12": ["قلة تناول المنتجات الحيوانية", "مشاكل امتصاص"],
            "B6": ["ضعف النظام الغذائي"],
            "Folate": ["قلة تناول الخضار"],
            "Ferritin": ["قلة تناول الحديد", "فقدان الدم"],
            "Zinc": ["ضعف التغذية"],
            "Magnesium": ["قلة المدخول", "فقدان عبر الجهاز الهضمي"],
            "Calcium": ["قلة المدخول", "نقص فيتامين D"],
        },
        "Normal": {"default": ["تغذية متوازنة"]},
        "Excessive": {
            "Vitamin_D": ["زيادة استخدام المكملات"],
            "Vitamin_C": ["زيادة المكملات"],
            "Vitamin_A": ["زيادة استخدام المكملات"],
            "Vitamin_E": ["الإفراط في المكملات"],
            "Vitamin_K": ["ارتفاع المدخول"],
            "B12": ["استخدام مكملات"],
            "B6": ["الإفراط في المكملات"],
            "Folate": ["زيادة المكملات"],
            "Ferritin": ["التهاب", "زيادة الحديد"],
            "Zinc": ["زيادة المكملات"],
            "Magnesium": ["الإفراط في المكملات"],
            "Calcium": ["ارتفاع المدخول"],
        },
    }
    causes = causes_en if language == "English" else causes_ar
    if status == "Normal":
        return causes["Normal"]["default"]
    return causes.get(status, {}).get(
        nutrient,
        [tr("Diet or absorption related", "مرتبط بالغذاء أو الامتصاص")]
    )

def get_recommendations(status):
    if language == "English":
        recs = {
            "Deficient": ["Improve dietary intake.", "Consult a doctor before supplements."],
            "Normal":    ["Maintain healthy lifestyle."],
            "Excessive": ["Avoid unnecessary supplements.", "Consult a healthcare professional."],
            "Invalid":   ["Check the entered value.", "Make sure the unit matches the nutrient."],
        }
    else:
        recs = {
            "Deficient": ["حسّن المدخول الغذائي.", "استشر الطبيب قبل استخدام المكملات."],
            "Normal":    ["حافظ على نمط حياة صحي."],
            "Excessive": ["تجنب المكملات غير الضرورية.", "استشر مختصًا صحيًا."],
            "Invalid":   ["تأكد من القيمة المدخلة.", "تأكد أن الوحدة مناسبة للعنصر."],
        }
    return recs.get(status, [tr("Consult a healthcare professional.", "استشر مختصًا صحيًا.")])

# =========================================
# Analyze row
# =========================================
def analyze_row(row):
    nutrient = normalize_nutrient_name(row.get("Nutrient", ""))
    value    = pd.to_numeric(row.get("Value", None), errors="coerce")
    value    = None if pd.isna(value) else float(value)
    gender   = normalize_gender(row.get("Gender", "Male"))
    age      = row.get("Age", None)
    range_info = get_range(nutrient, gender)

    if range_info is None:
        return {
            "Age": age, "Gender": gender, "Nutrient": nutrient, "Value": value,
            "Unit": "Unknown", "Low": None, "High": None, "Status": "Unknown",
            "Explanation": tr("Unknown nutrient.", "عنصر غير معروف"),
            "Possible Causes": "", "Recommendations": "",
            **unavailable_model_fields(),
        }

    valid, msg = validate_value(value, range_info)

    if not valid:
        return {
            "Age": age, "Gender": gender, "Nutrient": nutrient, "Value": value,
            "Unit": range_info["unit"], "Low": range_info["low"], "High": range_info["high"],
            "Status": "Invalid", "Explanation": msg,
            "Possible Causes": tr(
                "Possible wrong unit or typing error.",
                "قد تكون الوحدة غير صحيحة أو يوجد خطأ في الإدخال."
            ),
            "Recommendations": "; ".join(get_recommendations("Invalid")),
            **unavailable_model_fields(),
        }

    low, high, unit = range_info["low"], range_info["high"], range_info["unit"]
    status = classify_value(value, low, high)
    model_fields = predict_model_fields(age, gender, nutrient, value, status)

    return {
        "Age": age, "Gender": gender, "Nutrient": nutrient, "Value": value,
        "Unit": unit, "Low": low, "High": high, "Status": status,
        "Explanation": get_explanation(nutrient, value, unit, status, low, high),
        "Possible Causes": "; ".join(get_possible_causes(nutrient, status)),
        "Recommendations": "; ".join(get_recommendations(status)),
        **model_fields,
    }

# =========================================
# Reference range chart
# =========================================
def create_reference_chart(row):
    if row.get("Low") is None or row.get("High") is None:
        return None
    value, low, high = row["Value"], row["Low"], row["High"]
    nutrient, unit  = row["Nutrient"], row["Unit"]
    if pd.isna(low) or pd.isna(high):
        return None

    max_axis = max(value, high) * 1.35
    fig = go.Figure()

    fig.add_trace(go.Bar(x=[low],          y=[nutrient], orientation="h",
                         marker_color="rgba(255,75,75,0.75)",  name=tr("Below normal", "أقل من الطبيعي"), base=0))
    fig.add_trace(go.Bar(x=[high - low],   y=[nutrient], orientation="h",
                         marker_color="rgba(29,185,84,0.75)",  name=tr("Normal range", "النطاق الطبيعي"), base=low))
    fig.add_trace(go.Bar(x=[max_axis - high], y=[nutrient], orientation="h",
                         marker_color="rgba(255,165,0,0.60)", name=tr("Above normal", "أعلى من الطبيعي"), base=high))
    fig.add_trace(go.Scatter(
        x=[value], y=[nutrient], mode="markers+text",
        text=[f"  {value} {unit}"], textposition="middle right",
        textfont=dict(color="white", size=12, family="Plus Jakarta Sans, Cairo"),
        marker=dict(size=16, color="white", line=dict(color="#00BFFF", width=2.5),
                    symbol="diamond"),
        name=tr("Your value", "قيمتك"),
    ))

    fig.update_layout(
    title=dict(
        text=tr(
            f"{nutrient_display_name(nutrient)}: Value vs Normal Range",
            f"{nutrient_display_name(nutrient)}: القيمة مقارنة بالنطاق الطبيعي"
        ),
        font=dict(size=14, color="#B8C8D8", family="Plus Jakarta Sans, Cairo"),
    ),
    height=230 if is_arabic else 220,
    barmode="overlay",
    xaxis=dict(
        range=[0, max_axis],
        title=unit,
        gridcolor="rgba(255,255,255,0.05)",
        tickfont=dict(color="#7A9BB5", size=11)
    ),
    yaxis=dict(
        title="",
        tickfont=dict(color="#7A9BB5")
    ),
    margin=dict(l=10, r=10, t=40, b=20),
    legend=dict(
        orientation="h",
        y=-0.5,
        font=dict(color="#9AAAB8", size=11),
        bgcolor="rgba(0,0,0,0)"
    ),
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Plus Jakarta Sans, Cairo"),

    
        dragmode=False,
        hovermode=False
    )

    
    fig.update_xaxes(fixedrange=True)
    fig.update_yaxes(fixedrange=True)

    return fig 

# =========================================
# Result card (enhanced)
# =========================================
def render_result_card(row):
    status   = row["Status"]
    color    = status_color(status)
    icon     = status_icon(status)
    nutrient = nutrient_display_name(row["Nutrient"])
    value    = row["Value"]
    unit     = row.get("Unit", "")
    ml_prediction = str(row.get("ML Prediction", MODEL_UNAVAILABLE))
    ml_confidence = str(row.get("ML Confidence", MODEL_UNAVAILABLE))
    agreement = str(row.get("Model Agreement", MODEL_UNAVAILABLE))
    ml_color = status_color(ml_prediction) if ml_prediction in MODEL_VALID_STATUSES else "#7A9BB5"
    agreement_color = model_agreement_color(agreement)
    dir_val  = "rtl" if is_arabic else "ltr"
    align    = "right" if is_arabic else "left"

    causes_html = "".join(
        f'<li>{c.strip()}</li>'
        for c in str(row.get("Possible Causes", "")).split(";") if c.strip()
    )
    recs_html = "".join(
        f'<li>{r.strip()}</li>'
        for r in str(row.get("Recommendations", "")).split(";") if r.strip()
    )

    explanation = row.get("Explanation", "")

    padding_side = "padding-right: 20px" if is_arabic else "padding-left: 20px"
    arrow_side   = "right: 0" if is_arabic else "left: 0"

    st.html(f"""
<div class="result-card" style="border: 1px solid {color}30; border-left: 4px solid {color}; direction:{dir_val};">
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px; flex-wrap:wrap; gap:10px;">
        <div>
            <div style="font-size:19px; font-weight:800; color:#F0F4F8;
                        font-family:'Plus Jakarta Sans','Cairo',sans-serif; margin-bottom:3px;">
                {nutrient}
            </div>
            <div style="font-size:12px; color:#7A9BB5; letter-spacing:0.4px; text-transform:uppercase;">
                {tr("Lab Result", "نتيجة التحليل")}
            </div>
        </div>
        <span class="badge" style="color:{color}; background:{'rgba'+color[3:]+'22)' if color.startswith('#') else color+'22'};
                                   border: 1px solid {color}55; font-size:13px;">
            {icon} {status_text(status)}
        </span>
    </div>

    <div style="font-size:34px; font-weight:800; color:{color};
                font-family:'Plus Jakarta Sans','Cairo',sans-serif; margin-bottom:16px; line-height:1;">
        {value}
        <span style="font-size:16px; color:#7A9BB5; font-weight:500; margin-left:6px;">{unit}</span>
    </div>

    <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(160px, 1fr)); gap:10px; margin-bottom:14px;">
        <div style="background:rgba(0,191,255,0.045); border:1px solid {ml_color}35; border-radius:8px; padding:10px 12px;">
            <div style="font-size:11px; font-weight:700; color:#7A9BB5; letter-spacing:0.5px;
                        text-transform:uppercase; margin-bottom:4px;">
                {tr("ML Prediction", "تنبؤ الموديل")}
            </div>
            <div style="font-size:14px; font-weight:800; color:{ml_color};">
                {ml_prediction_text(ml_prediction)}
                <span style="font-size:12px; font-weight:600; color:#7A9BB5;">
                    {"" if ml_confidence == MODEL_UNAVAILABLE else f"({ml_confidence})"}
                </span>
            </div>
        </div>
        <div style="background:rgba(255,255,255,0.025); border:1px solid {agreement_color}35; border-radius:8px; padding:10px 12px;">
            <div style="font-size:11px; font-weight:700; color:#7A9BB5; letter-spacing:0.5px;
                        text-transform:uppercase; margin-bottom:4px;">
                {tr("Model Agreement", "توافق الموديل")}
            </div>
            <div style="font-size:14px; font-weight:800; color:{agreement_color};">
                {model_agreement_text(agreement)}
            </div>
        </div>
    </div>

    <div style="font-size:14px; color:#B8C8D8; line-height:1.7; margin-bottom:14px;
                background:rgba(255,255,255,0.03); border-radius:8px; padding:12px 14px;
                border-left:2px solid {color}55; text-align:{align}; direction:{dir_val};">
        {explanation}
    </div>

    <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px;">
        <div style="background:rgba(255,255,255,0.025); border-radius:10px; padding:12px 14px;
                    border:1px solid rgba(255,255,255,0.06);">
            <div style="font-size:11px; font-weight:700; color:#7A9BB5; letter-spacing:0.5px;
                        text-transform:uppercase; margin-bottom:8px;">
                🔍 {tr("Possible Causes", "الأسباب المحتملة")}
            </div>
            <ul style="margin:0; padding:0; list-style:none; direction:{dir_val}; text-align:{align};">
                {causes_html.replace('<li>', f'<li style="font-size:13px; color:#B8C8D8; margin-bottom:5px; {padding_side}; position:relative;"><span style="position:absolute; {arrow_side}; color:{color};">›</span>')}
            </ul>
        </div>
        <div style="background:rgba(255,255,255,0.025); border-radius:10px; padding:12px 14px;
                    border:1px solid rgba(255,255,255,0.06);">
            <div style="font-size:11px; font-weight:700; color:#7A9BB5; letter-spacing:0.5px;
                        text-transform:uppercase; margin-bottom:8px;">
                💡 {tr("Recommendations", "التوصيات")}
            </div>
            <ul style="margin:0; padding:0; list-style:none; direction:{dir_val}; text-align:{align};">
                {recs_html.replace('<li>', f'<li style="font-size:13px; color:#B8C8D8; margin-bottom:5px; {padding_side}; position:relative;"><span style="position:absolute; {arrow_side}; color:{color};">›</span>')}
            </ul>
        </div>
    </div>

    <div style="margin-top:14px; padding:10px 14px; border-radius:8px;
                background:rgba(255,193,7,0.06); border:1px solid rgba(255,193,7,0.20);
                display:flex; align-items:flex-start; gap:8px; direction:{dir_val};">
        <span style="font-size:14px; flex-shrink:0;"></span>
        <span style="font-size:13px; color:#C8B87A; line-height:1.5; text-align:{align};">
            {tr(
                "Medical note: This result is not a medical diagnosis. Please consult a healthcare professional.",
                "ملاحظة طبية: هذه النتيجة ليست تشخيصًا طبيًا. يرجى استشارة مختص صحي."
            )}
        </span>
    </div>
</div>
<div style="height:8px;"></div>
""")

# =========================================
# Summary stats bar
# =========================================
def render_summary_stats(df):
    total      = len(df)
    normal     = len(df[df["Status"] == "Normal"])
    deficient  = len(df[df["Status"] == "Deficient"])
    excessive  = len(df[df["Status"] == "Excessive"])

    st.html(f"""
<div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(115px, 1fr)); gap:12px; margin:18px 0; width:100%;">
    <div class="stat-mini">
        <div class="stat-number" style="color:#F0F4F8;">{total}</div>
        <div class="stat-label">{tr("Total", "الإجمالي")}</div>
    </div>
    <div class="stat-mini">
        <div class="stat-number" style="color:#1DB954;">{normal}</div>
        <div class="stat-label">{tr("Normal", "طبيعي")}</div>
    </div>
    <div class="stat-mini">
        <div class="stat-number" style="color:#FF4B4B;">{deficient}</div>
        <div class="stat-label">{tr("Deficient", "ناقص")}</div>
    </div>
    <div class="stat-mini">
        <div class="stat-number" style="color:#FFA500;">{excessive}</div>
        <div class="stat-label">{tr("Excessive", "مرتفع")}</div>
    </div>
</div>
""")

# =========================================
# Dashboard helpers
# =========================================
DASHBOARD_VALID_STATUSES = ["Normal", "Deficient", "Excessive"]
DASHBOARD_STATUS_ORDER = ["Normal", "Deficient", "Excessive", "Invalid", "Unknown", "Error"]
REPORT_RESULT_COLUMNS = [
    "Age", "Gender", "Nutrient", "Value", "Unit", "Low", "High",
    "Status", "ML Prediction", "ML Confidence", "Model Agreement",
    "Explanation", "Possible Causes", "Recommendations",
]

def safe_html(value):
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except (TypeError, ValueError):
        pass
    return html.escape(str(value))

def report_json_value(value):
    if value is None:
        return None
    try:
        if pd.isna(value):
            return None
    except (TypeError, ValueError):
        pass
    if isinstance(value, (pd.Timestamp,)):
        return value.isoformat()
    if isinstance(value, (int, float, str, bool)):
        return value
    return str(value)

def report_records_from_df(df):
    if df.empty:
        return []

    ordered_cols = [col for col in REPORT_RESULT_COLUMNS if col in df.columns]
    extra_cols = [col for col in df.columns if col not in ordered_cols]
    records = []
    for _, row in df[ordered_cols + extra_cols].iterrows():
        records.append({
            col: report_json_value(row.get(col))
            for col in ordered_cols + extra_cols
        })
    return records

def report_signature_from_records(records):
    signature_fields = [
        "Age", "Gender", "Nutrient", "Value", "Unit", "Low", "High",
        "Status", "ML Prediction", "ML Confidence", "Model Agreement",
    ]
    stable_records = sorted(
        [
            {field: record.get(field) for field in signature_fields}
            for record in records
        ],
        key=lambda record: (
            str(record.get("Nutrient", "")),
            str(record.get("Value", "")),
            str(record.get("Status", "")),
        ),
    )
    payload = json.dumps(stable_records, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()

def report_counts(records):
    statuses = [str(record.get("Status", "Unknown")) for record in records]
    return {
        "total": len(records),
        "normal": statuses.count("Normal"),
        "deficient": statuses.count("Deficient"),
        "excessive": statuses.count("Excessive"),
        "invalid": sum(status in ["Invalid", "Unknown", "Error"] for status in statuses),
    }

def report_overall_status(counts):
    if counts["invalid"]:
        return "Needs Review"
    if counts["deficient"] or counts["excessive"]:
        return "Needs Attention"
    if counts["total"]:
        return "Normal"
    return "Empty"

def report_overall_status_text(status):
    return {
        "Needs Review": tr("Needs Review", "يحتاج مراجعة"),
        "Needs Attention": tr("Needs Attention", "يحتاج متابعة"),
        "Normal": tr("Normal", "طبيعي"),
        "Empty": tr("Empty", "فارغ"),
    }.get(status, status)

def load_report_history():
    reports = st.session_state.get("report_history", [])
    if not isinstance(reports, list):
        return []

    return sorted(
        [report for report in reports if isinstance(report, dict)],
        key=lambda report: str(report.get("created_at", "")),
    )

def save_report_history(reports):
    st.session_state["report_history"] = sorted(
        [report for report in reports if isinstance(report, dict)],
        key=lambda report: str(report.get("created_at", "")),
    )

def load_reminder():
    reminder = st.session_state.get("reminder")
    return reminder if isinstance(reminder, dict) else None

def save_reminder(next_date, interval_months):
    st.session_state["reminder"] = {
        "next_test_date": next_date.isoformat(),
        "interval_months": interval_months,
        "created_at": datetime.now().isoformat(),
    }

def delete_reminder():
    st.session_state.pop("reminder", None)

def days_until_next_test():
    reminder = load_reminder()
    if not reminder:
        return None, None
    try:
        next_date = date.fromisoformat(reminder["next_test_date"])
        delta = (next_date - date.today()).days
        return delta, next_date
    except Exception:
        return None, None

def refresh_report_history_state():
    if "report_history" not in st.session_state:
        st.session_state["report_history"] = []
    else:
        st.session_state["report_history"] = load_report_history()

def get_report_history():
    if "report_history" not in st.session_state:
        refresh_report_history_state()
    return st.session_state["report_history"]

def report_to_df(report):
    df = pd.DataFrame(report.get("results", []))
    for column in MODEL_RESULT_COLUMNS:
        if column not in df.columns:
            df[column] = MODEL_UNAVAILABLE
    return df

def build_report(df, source):
    records = report_records_from_df(df)
    signature = report_signature_from_records(records)
    created_at = pd.Timestamp.now()
    counts = report_counts(records)
    report_id = f"RPT-{created_at.strftime('%Y%m%d-%H%M%S')}-{signature[:6].upper()}"
    return {
        "report_id": report_id,
        "created_at": created_at.isoformat(),
        "source": source,
        "signature": signature,
        "summary": counts,
        "overall_status": report_overall_status(counts),
        "results": records,
    }

def save_analysis_report(df, source):
    if df.empty:
        return None

    report = build_report(df, source)
    reports = list(get_report_history())
    if any(existing.get("signature") == report["signature"] for existing in reports):
        return None

    reports.append(report)
    save_report_history(reports)
    reports = get_report_history()
    st.session_state["selected_report_id"] = report["report_id"]
    return report

def delete_analysis_report(report_id):
    reports = [
        report for report in get_report_history()
        if report.get("report_id") != report_id
    ]
    save_report_history(reports)
    st.session_state["report_history"] = reports
    if reports:
        st.session_state["selected_report_id"] = reports[-1]["report_id"]
    else:
        st.session_state.pop("selected_report_id", None)

def report_display_date(report):
    created_at = pd.to_datetime(report.get("created_at"), errors="coerce")
    if pd.isna(created_at):
        return tr("Unknown date", "تاريخ غير معروف")
    return tr(
        created_at.strftime("%b %d, %Y"),
        created_at.strftime("%Y/%m/%d"),
    )

def report_display_date_en(report):
    created_at = pd.to_datetime(report.get("created_at"), errors="coerce")
    if pd.isna(created_at):
        return "Unknown date"
    return created_at.strftime("%Y-%m-%d")

def clean_imported_result(record):
    if not isinstance(record, dict):
        return None

    cleaned = {
        str(key): report_json_value(value)
        for key, value in record.items()
    }
    nutrient = normalize_nutrient_name(cleaned.get("Nutrient"))
    if not nutrient or "Value" not in cleaned:
        return None

    cleaned["Nutrient"] = nutrient
    cleaned["Status"] = str(cleaned.get("Status") or "Unknown")

    if not str(cleaned.get("Unit", "")).strip():
        nutrient_range = get_range(nutrient, cleaned.get("Gender", 1))
        if nutrient_range:
            cleaned["Unit"] = nutrient_range.get("unit", "")

    for column in MODEL_RESULT_COLUMNS:
        cleaned.setdefault(column, MODEL_UNAVAILABLE)

    return cleaned

def clean_report_summary(summary, results):
    counts = report_counts(results)
    if not isinstance(summary, dict):
        return counts

    for key in counts:
        try:
            counts[key] = max(int(summary.get(key, counts[key])), 0)
        except (TypeError, ValueError):
            pass
    return counts

def normalize_imported_report(report):
    if not isinstance(report, dict):
        return None

    created_at = str(report.get("created_at", "")).strip()
    parsed_date = pd.to_datetime(created_at, errors="coerce")
    if not created_at or pd.isna(parsed_date):
        return None

    raw_results = report.get("results", [])
    if not isinstance(raw_results, list):
        return None

    results = []
    for result in raw_results:
        cleaned = clean_imported_result(result)
        if cleaned is None:
            return None
        results.append(cleaned)

    if not results:
        return None

    signature = str(report.get("signature") or report_signature_from_records(results)).strip()
    if not signature:
        signature = report_signature_from_records(results)

    report_id = str(report.get("report_id") or f"RPT-IMPORTED-{signature[:10].upper()}").strip()
    summary = clean_report_summary(report.get("summary"), results)
    overall_status = str(report.get("overall_status") or report_overall_status(summary))
    source = str(report.get("source") or "Imported History").strip() or "Imported History"

    return {
        "report_id": report_id,
        "created_at": parsed_date.isoformat(),
        "source": source,
        "signature": signature,
        "summary": summary,
        "overall_status": overall_status,
        "results": results,
    }

def parse_history_archive_bytes(raw_bytes):
    try:
        archive = json.loads(raw_bytes.decode("utf-8-sig"))
    except UnicodeDecodeError:
        return [], tr(
            "This VitaVision backup data is not readable.",
            "بيانات نسخة VitaVision الاحتياطية غير قابلة للقراءة."
        )
    except json.JSONDecodeError:
        return [], tr(
            "This VitaVision backup data is not valid.",
            "بيانات نسخة VitaVision الاحتياطية غير صالحة."
        )

    if not isinstance(archive, dict):
        return [], tr(
            "This is not a VitaVision history backup.",
            "هذا الملف ليس نسخة احتياطية لسجل VitaVision."
        )

    if (
        archive.get("schema_version") != HISTORY_ARCHIVE_SCHEMA_VERSION
        or archive.get("app") != HISTORY_ARCHIVE_APP
        or "exported_at" not in archive
        or "reports" not in archive
    ):
        return [], tr(
            "This file does not contain valid VitaVision history data.",
            "هذا الملف لا يحتوي على بيانات سجل VitaVision صالحة."
        )

    reports = archive.get("reports")
    if not isinstance(reports, list):
        return [], tr(
            "The backup file is missing a valid reports list.",
            "ملف النسخة الاحتياطية لا يحتوي على قائمة تقارير صالحة."
        )

    normalized_reports = []
    for report in reports:
        normalized_report = normalize_imported_report(report)
        if normalized_report is None:
            return [], tr(
                "The backup contains unsupported report data and was not imported.",
                "تحتوي النسخة الاحتياطية على بيانات تقارير غير مدعومة ولم يتم استيرادها."
            )
        normalized_reports.append(normalized_report)

    return normalized_reports, None

def embedded_pdf_attachment_bytes(reader):
    attachments = getattr(reader, "attachments", None) or {}
    if not attachments:
        return None

    preferred_names = [HISTORY_ARCHIVE_ATTACHMENT_NAME]
    preferred_names.extend(
        name for name in attachments.keys()
        if str(name).lower().endswith(".json") and name not in preferred_names
    )

    for name in preferred_names:
        payload = attachments.get(name)
        candidates = payload if isinstance(payload, list) else [payload]
        for candidate in candidates:
            if isinstance(candidate, bytes):
                return candidate
            if isinstance(candidate, str):
                return candidate.encode("utf-8")

    return None

def parse_history_pdf_bytes(raw_bytes):
    try:
        from pypdf import PdfReader
    except ImportError:
        return [], tr(
            "PDF restore needs pypdf. Install the app requirements, then restart VitaVision.",
            "استرجاع PDF يحتاج مكتبة pypdf. ثبّت متطلبات التطبيق ثم أعد تشغيل VitaVision."
        )

    try:
        reader = PdfReader(BytesIO(raw_bytes))
    except Exception:
        return [], tr(
            "This is not a readable PDF file.",
            "هذا الملف ليس PDF قابلًا للقراءة."
        )

    archive_bytes = embedded_pdf_attachment_bytes(reader)
    if archive_bytes is None:
        return [], tr(
            "This PDF was not exported from VitaVision, or it does not contain restorable history data.",
            "هذا الملف لم يتم تصديره من VitaVision، أو لا يحتوي على بيانات سجل قابلة للاسترجاع."
        )

    return parse_history_archive_bytes(archive_bytes)

def merge_report_history(imported_reports):
    reports = list(get_report_history())
    existing_signatures = {
        str(report.get("signature", "")).strip()
        for report in reports
        if str(report.get("signature", "")).strip()
    }
    existing_report_ids = {
        str(report.get("report_id", "")).strip()
        for report in reports
        if str(report.get("report_id", "")).strip()
    }

    added = 0
    duplicates = 0
    for report in imported_reports:
        signature = str(report.get("signature", "")).strip()
        report_id = str(report.get("report_id", "")).strip()

        if signature and signature in existing_signatures:
            duplicates += 1
            continue
        if report_id and report_id in existing_report_ids:
            duplicates += 1
            continue

        reports.append(report)
        if signature:
            existing_signatures.add(signature)
        if report_id:
            existing_report_ids.add(report_id)
        added += 1

    if added:
        save_report_history(reports)
        saved_reports = get_report_history()
        if saved_reports:
            st.session_state["selected_report_id"] = saved_reports[-1].get("report_id")

    return added, duplicates

def build_history_archive(reports):
    safe_reports = json.loads(json.dumps(reports, ensure_ascii=False, default=str))
    return {
        "schema_version": HISTORY_ARCHIVE_SCHEMA_VERSION,
        "app": HISTORY_ARCHIVE_APP,
        "exported_at": datetime.now().isoformat(),
        "reports": safe_reports,
    }

def build_history_archive_bytes(reports):
    return json.dumps(
        build_history_archive(reports),
        ensure_ascii=False,
        indent=2,
        default=str,
    ).encode("utf-8")

def history_status_summary(reports):
    summary = {
        "Normal": 0,
        "Deficient": 0,
        "Excessive": 0,
        "Invalid": 0,
    }
    for report in reports:
        for result in report.get("results", []):
            status = str(result.get("Status", "Invalid"))
            if status in ["Normal", "Deficient", "Excessive"]:
                summary[status] += 1
            else:
                summary["Invalid"] += 1
    return summary

def report_source_en(source):
    source_text = str(source or "").strip()
    lowered = source_text.lower()
    if "csv" in lowered:
        return "CSV Upload"
    if "manual" in lowered:
        return "Manual Input"
    if "current" in lowered and "session" in lowered:
        return "Current Session"
    if "import" in lowered:
        return "Imported History"
    if not source_text:
        return "Unknown"
    return source_text if source_text.isascii() else "Imported History"

def display_cell_value(value):
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except (TypeError, ValueError):
        pass
    return str(value)

def history_display_dataframe(reports):
    columns = [
        tr("Date", "التاريخ"),
        tr("Source", "المصدر"),
        tr("Nutrient", "العنصر"),
        tr("Value", "القيمة"),
        tr("Unit", "الوحدة"),
        tr("Status", "الحالة"),
    ]
    rows = []
    for report in sorted(reports, key=report_sort_value, reverse=True):
        for result in report.get("results", []):
            rows.append({
                columns[0]: report_display_date(report),
                columns[1]: report.get("source", ""),
                columns[2]: nutrient_display_name(result.get("Nutrient", "")),
                columns[3]: display_cell_value(result.get("Value", "")),
                columns[4]: display_cell_value(result.get("Unit", "")),
                columns[5]: status_text(str(result.get("Status", "Unknown"))),
            })
    return pd.DataFrame(rows, columns=columns)

def history_pdf_rows(reports):
    rows = []
    for report in sorted(reports, key=report_sort_value, reverse=True):
        for result in report.get("results", []):
            status = str(result.get("Status", "Invalid"))
            rows.append({
                "Date": report_display_date_en(report),
                "Source": report_source_en(report.get("source", "")),
                "Nutrient": nutrient_display_name_en(result.get("Nutrient", "")),
                "Value": display_cell_value(result.get("Value", "")),
                "Unit": display_cell_value(result.get("Unit", "")),
                "Status": status if status in ["Normal", "Deficient", "Excessive"] else "Invalid",
            })
    return rows

def attach_history_archive_to_pdf(pdf_bytes, archive_bytes):
    try:
        from pypdf import PdfReader, PdfWriter
    except ImportError:
        return None

    try:
        reader = PdfReader(BytesIO(pdf_bytes))
        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)
        writer.add_metadata({
            "/Title": "VitaVision Report History",
            "/Subject": "Readable and restorable VitaVision report history",
            "/Creator": "VitaVision",
            "/Producer": "VitaVision",
            "/Keywords": "VitaVision,report history,restorable backup",
        })
        writer.add_attachment(HISTORY_ARCHIVE_ATTACHMENT_NAME, archive_bytes)
        output = BytesIO()
        writer.write(output)
        return output.getvalue()
    except Exception:
        return None

def build_history_pdf(reports):
    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import A4, landscape
        from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
        from reportlab.lib.units import mm
        from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
    except ImportError:
        return None

    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A4),
        rightMargin=12 * mm,
        leftMargin=12 * mm,
        topMargin=12 * mm,
        bottomMargin=12 * mm,
        title="VitaVision Report History",
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "VitaVisionTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#0E6081"),
        spaceAfter=8,
    )
    body_style = ParagraphStyle(
        "VitaVisionBody",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#263238"),
    )
    cell_style = ParagraphStyle(
        "VitaVisionCell",
        parent=body_style,
        fontSize=8,
        leading=10,
    )
    header_style = ParagraphStyle(
        "VitaVisionHeader",
        parent=cell_style,
        fontName="Helvetica-Bold",
        textColor=colors.white,
    )
    footer_style = ParagraphStyle(
        "VitaVisionFooter",
        parent=body_style,
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#546E7A"),
    )

    summary = history_status_summary(reports)
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M")
    status_line = (
        f"Normal: {summary['Normal']} | "
        f"Deficient: {summary['Deficient']} | "
        f"Excessive: {summary['Excessive']} | "
        f"Invalid: {summary['Invalid']}"
    )

    story = [
        Paragraph("VitaVision Report History", title_style),
        Paragraph(f"Generated at: {generated_at}", body_style),
        Paragraph(f"Report count: {len(reports)}", body_style),
        Paragraph(f"Status summary: {status_line}", body_style),
        Spacer(1, 8),
    ]

    headers = ["Date", "Source", "Nutrient", "Value", "Unit", "Status"]
    table_data = [[Paragraph(header, header_style) for header in headers]]
    for row in history_pdf_rows(reports):
        table_data.append([
            Paragraph(html.escape(display_cell_value(row.get(header, ""))), cell_style)
            for header in headers
        ])

    if len(table_data) == 1:
        table_data.append([
            Paragraph("No report rows available.", cell_style),
            Paragraph("", cell_style),
            Paragraph("", cell_style),
            Paragraph("", cell_style),
            Paragraph("", cell_style),
            Paragraph("", cell_style),
        ])

    table = Table(
        table_data,
        colWidths=[30 * mm, 44 * mm, 56 * mm, 30 * mm, 30 * mm, 36 * mm],
        repeatRows=1,
    )
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0E6081")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#B0BEC5")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F4F8FB")]),
    ]))
    story.append(table)
    story.extend([
        Spacer(1, 10),
        Paragraph(
            "Medical note: VitaVision is an educational awareness tool only and does not replace medical diagnosis, treatment, or consultation with a qualified healthcare professional.",
            footer_style,
        ),
    ])

    doc.build(story)
    return attach_history_archive_to_pdf(
        buffer.getvalue(),
        build_history_archive_bytes(reports),
    )

def render_history_restore_panel():
    section_title(tr("Restore Previous History", "استرجاع سجل سابق"), 22, "")
    st.info(tr(
        "Upload the VitaVision history PDF you downloaded earlier. The same PDF is readable and can restore your history.",
        "ارفع ملف سجل VitaVision بصيغة PDF الذي حمّلته سابقًا. نفس ملف PDF قابل للقراءة ويمكنه استرجاع السجل."
    ))

    uploaded_history = st.file_uploader(
        tr("Upload VitaVision History PDF", "رفع ملف سجل VitaVision PDF"),
        type=["pdf"],
        key="history_restore_upload",
    )

    if uploaded_history is None:
        return

    raw_bytes = uploaded_history.getvalue()
    file_digest = hashlib.sha256(raw_bytes).hexdigest()

    if st.session_state.get("last_history_import_hash") == file_digest:
        st.info(tr(
            "This file was already processed in this session. Your history was not duplicated.",
            "تمت معالجة هذا الملف مسبقًا في هذه الجلسة، ولم يتم تكرار السجل."
        ))
        return

    imported_reports, error_message = parse_history_pdf_bytes(raw_bytes)
    if error_message:
        st.error(error_message)
        return

    added, duplicates = merge_report_history(imported_reports)
    st.session_state["last_history_import_hash"] = file_digest
    st.session_state["last_history_import_result"] = {
        "added": added,
        "duplicates": duplicates,
    }

    if added:
        st.success(tr(
            f"Restored {added} report(s). Skipped {duplicates} duplicate(s). Open Dashboard to view the history.",
            f"تم استرجاع {added} تقرير. تم تجاهل {duplicates} تقرير مكرر. افتح لوحة التحكم لعرض السجل."
        ))
    else:
        st.info(tr(
            f"No new reports were added. Skipped {duplicates} duplicate report(s).",
            f"لم تتم إضافة تقارير جديدة. تم تجاهل {duplicates} تقرير مكرر."
        ))

def render_history_backup_panel(reports):
    with st.expander(tr("Report History & Backup", "سجل التقارير والنسخ الاحتياطي"), expanded=False):
        if not reports:
            st.info(tr(
                "Backup export becomes available after you analyze results or restore a VitaVision PDF history file from Home.",
                "سيصبح التصدير متاحًا بعد تحليل نتائج أو استرجاع ملف سجل VitaVision PDF من الصفحة الرئيسية."
            ))
            return

        history_df = history_display_dataframe(reports)
        if history_df.empty:
            st.info(tr(
                "No report rows are available for export yet.",
                "لا توجد صفوف تقارير متاحة للتصدير حتى الآن."
            ))
        else:
            st.dataframe(history_df, use_container_width=True, hide_index=True)

        st.caption(tr(
            "This single PDF is readable by you and restorable by VitaVision later.",
            "هذا ملف PDF واحد يمكنك قراءته، ويمكن لـ VitaVision استرجاع السجل منه لاحقًا."
        ))

        pdf_data = build_history_pdf(reports)
        if pdf_data is None:
            st.warning(tr(
                "Smart PDF export needs ReportLab and pypdf. They are listed in requirements.txt; install dependencies and restart the app.",
                "تصدير PDF الذكي يحتاج ReportLab و pypdf. تمت إضافتهما في requirements.txt؛ ثبّت المتطلبات ثم أعد تشغيل التطبيق."
            ))
        else:
            st.download_button(
                label=tr("Download History PDF", "تحميل ملف السجل PDF"),
                data=pdf_data,
                file_name="vitavision_report_history.pdf",
                mime="application/pdf",
                use_container_width=True,
                key="history_backup_pdf_download",
            )

def latest_report():
    reports = get_report_history()
    return reports[-1] if reports else None

def dashboard_days_since_last():
    reports = get_report_history()
    if not reports:
        return 0
    last_date = reports[-1].get("created_at", pd.Timestamp.now())
    try:
        delta = pd.Timestamp.now() - pd.Timestamp(last_date)
        return max(int(delta.days), 0)
    except Exception:
        return 0

def render_dashboard_styles():
    st.markdown("""
.vv-dashboard-header { margin: 10px 0 20px; }
.vv-dashboard-title {
    font-family: 'Plus Jakarta Sans','Cairo',sans-serif;
    font-size: 28px; font-weight: 800; line-height: 1.15;
    color: var(--text-main); margin: 0 0 4px;
}
.vv-dashboard-subtitle { color: var(--text-muted); font-size: 13px; font-weight: 500; }

/* ── Overall health banner ── */
.vv-health-banner {
    border-radius: 14px;
    padding: 20px 24px;
    margin: 0 0 22px;
    display: flex; align-items: center; gap: 16px;
    border: 1px solid;
}
.vv-health-banner-icon { font-size: 32px; flex-shrink: 0; }
.vv-health-banner-title {
    font-size: 18px; font-weight: 800;
    font-family: 'Plus Jakarta Sans','Cairo',sans-serif;
    margin-bottom: 4px;
}
.vv-health-banner-text { font-size: 13px; line-height: 1.6; opacity: 0.85; }

/* ── KPI cards ── */
.vv-dashboard-metrics {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 12px; margin: 0 0 22px;
}
.vv-dashboard-card {
    border-radius: 12px;
    padding: 18px 20px;
    border: 1px solid rgba(0,191,255,0.15);
    background: rgba(0,191,255,0.04);
    display: flex; flex-direction: column; gap: 10px;
}
.vv-dashboard-card.soft-green {
    background: rgba(29,185,84,0.08);
    border-color: rgba(29,185,84,0.25);
}
.vv-dashboard-card.soft-amber {
    background: rgba(255,165,0,0.08);
    border-color: rgba(255,165,0,0.25);
}
.vv-dashboard-card.soft-red {
    background: rgba(255,75,75,0.08);
    border-color: rgba(255,75,75,0.25);
}
.vv-dashboard-card.soft-blue {
    background: rgba(0,191,255,0.08);
    border-color: rgba(0,191,255,0.25);
}
.vv-dashboard-card-label {
    color: #7A9BB5; font-size: 12px; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.5px;
}
.vv-dashboard-card-value {
    color: #F0F4F8; font-size: 26px; font-weight: 800; line-height: 1;
}
.vv-dashboard-panel-subtitle { color: #7A9BB5; font-size: 13px; }
.vv-dashboard-status-pill {
    width: fit-content; border-radius: 999px; padding: 4px 10px;
    background: rgba(255,255,255,0.1); color: #F0F4F8;
    font-size: 11px; font-weight: 800;
}

/* ── Tracking cards ── */
.vv-tracking-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 12px; margin: 12px 0 24px;
}
.vv-tracking-card {
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.08);
    border-left: 5px solid #9ca3af;
    background: rgba(255,255,255,0.04);
    padding: 16px 17px;
    display: flex; flex-direction: column; justify-content: space-between;
}
.vv-tracking-card.normal  { border-left-color: #1DB954; background: rgba(29,185,84,0.05); }
.vv-tracking-card.deficient { border-left-color: #FF4B4B; background: rgba(255,75,75,0.05); }
.vv-tracking-card.excessive { border-left-color: #FFA500; background: rgba(255,165,0,0.05); }
.vv-tracking-card.invalid,
.vv-tracking-card.unknown,
.vv-tracking-card.error { border-left-color: #6b7280; }
.vv-tracking-name { color: #F0F4F8; font-size: 16px; font-weight: 800; }
.vv-tracking-value {
    color: #00BFFF; font-size: 26px; font-weight: 800;
    line-height: 1.1; margin-top: 6px;
}
.vv-tracking-meta { color: #7A9BB5; font-size: 12px; font-weight: 600; margin-top: 6px; line-height: 1.5; }
.vv-tracking-delta {
    width: fit-content; margin-top: 8px; border-radius: 999px;
    padding: 4px 10px; background: rgba(0,191,255,0.10);
    color: #00BFFF; font-size: 12px; font-weight: 800;
}
.vv-tracking-warning {
    margin-top: 8px; border-radius: 8px; padding: 7px 10px;
    background: rgba(255,165,0,0.10); color: #FFA500;
    font-size: 12px; font-weight: 700;
}

/* ── Sparkline ── */
.vv-sparkline { width: 100%; height: 48px; margin-top: 12px; }
.vv-sparkline-empty {
    height: 48px; margin-top: 12px; border-radius: 8px;
    background: rgba(255,255,255,0.04); color: #7A9BB5;
    display: flex; align-items: center; justify-content: center;
    font-size: 12px; font-weight: 700;
}

/* ── Reminder card ── */
.vv-reminder-card {
    border-radius: 14px;
    padding: 20px 24px;
    margin: 0 0 22px;
    border: 1px solid;
    display: flex; align-items: center; gap: 16px;
}
.vv-reminder-icon { font-size: 32px; flex-shrink: 0; }
.vv-reminder-title {
    font-size: 16px; font-weight: 800;
    font-family: 'Plus Jakarta Sans','Cairo',sans-serif;
    margin-bottom: 4px;
}
.vv-reminder-text { font-size: 13px; line-height: 1.6; opacity: 0.85; }
.vv-reminder-countdown {
    font-size: 28px; font-weight: 800;
    font-family: 'Plus Jakarta Sans','Cairo',sans-serif;
    line-height: 1;
}

/* ── Quick stats ── */
.vv-quick-stats {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 12px; margin: 0 0 22px;
}
@media (max-width: 900px) { .vv-quick-stats { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 560px) { .vv-quick-stats { grid-template-columns: 1fr; } }

/* ── Empty state ── */
.vv-dashboard-empty {
    background: rgba(255,255,255,0.03);
    border: 1px dashed rgba(0,191,255,0.20);
    border-radius: 14px; padding: 36px; color: #7A9BB5;
    text-align: center;
}

@media (max-width: 900px) { .vv-dashboard-metrics { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 560px) { .vv-dashboard-metrics { grid-template-columns: 1fr; } }
</style>
""", unsafe_allow_html=True)

def render_dashboard_header():
    days = dashboard_days_since_last()
    subtitle = tr(
        f"Last check {days} day(s) ago",
        f"آخر فحص قبل {days} يوم"
    )
    align = "right" if is_arabic else "left"

    st.html(f"""
<div class="vv-dashboard-header" style="text-align:{align};">
    <div class="vv-dashboard-title">{safe_html(tr("Dashboard", "لوحة التحكم"))}</div>
    <div class="vv-dashboard-subtitle">{safe_html(subtitle)}</div>
</div>
""")

def dashboard_status_class(status):
    status_value = str(status)
    return status_value.lower() if status_value in DASHBOARD_STATUS_ORDER else "unknown"

def dashboard_number(value):
    numeric_value = pd.to_numeric(value, errors="coerce")
    if pd.isna(numeric_value):
        return safe_html(value)
    return f"{float(numeric_value):g}"



def render_reminder_card():
    reminder = load_reminder()
    days_left, next_date = days_until_next_test()

    if reminder and days_left is not None:
        interval = reminder.get("interval_months", 3)
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            new_interval = st.selectbox(
                tr("Repeat interval", "فترة التكرار"),
                options=[3, 6, 12],
                index=[3, 6, 12].index(interval) if interval in [3, 6, 12] else 0,
                format_func=lambda m: tr(f"Every {m} months", f"كل {m} أشهر"),
                key="reminder_interval_select",
            )
        with col2:
            if st.button(tr("Reschedule", "إعادة جدولة"), use_container_width=True, key="reminder_reschedule"):
                new_date = date.today() + timedelta(days=new_interval * 30)
                save_reminder(new_date, new_interval)
                st.rerun()
        with col3:
            if st.button(tr("Delete", "حذف"), use_container_width=True, key="reminder_delete"):
                delete_reminder()
                st.rerun()
    else:
        col1, col2 = st.columns([3, 2])
        with col1:
            interval = st.selectbox(
                tr("Test interval", "فترة التحليل"),
                options=[3, 6, 12],
                format_func=lambda m: tr(f"Every {m} months", f"كل {m} أشهر"),
                key="reminder_new_interval",
            )
        with col2:
            if st.button(tr("Set Reminder", "تعيين التذكير"), use_container_width=True, type="primary", key="reminder_set"):
                new_date = date.today() + timedelta(days=interval * 30)
                save_reminder(new_date, interval)
                st.rerun()

def render_report_history_table(reports):
    rows = []
    for report in reversed(reports):
        counts = report.get("summary", {})
        rows.append({
            tr("Date", "التاريخ"): report_display_date(report),
            tr("Source", "المصدر"): report.get("source", ""),
            tr("Items", "العناصر"): counts.get("total", 0),
            tr("Deficient", "ناقص"): counts.get("deficient", 0),
            tr("Excessive", "مرتفع"): counts.get("excessive", 0),
            tr("Status", "الحالة"): report_overall_status_text(report.get("overall_status", "")),
        })

    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

def render_report_actions(report, report_df, key_prefix="report"):
    download_col, delete_col = st.columns([2, 1])
    with download_col:
        st.download_button(
            label=tr("Download Selected Report CSV", "تحميل التقرير المحدد CSV"),
            data=report_df.to_csv(index=False),
            file_name=f"{report.get('report_id', 'vitavision_report')}.csv",
            mime="text/csv",
            use_container_width=True,
            key=f"{key_prefix}_download_{report.get('report_id')}",
        )
    with delete_col:
        if st.button(
            tr("Delete Report", "حذف التقرير"),
            use_container_width=True,
            key=f"{key_prefix}_delete_{report.get('report_id')}",
        ):
            delete_analysis_report(report.get("report_id"))
            st.rerun()

def is_valid_trend_reading(status, value):
    return str(status) not in ["Invalid", "Unknown", "Error"] and not pd.isna(pd.to_numeric(value, errors="coerce"))

def report_sort_value(report):
    created_at = pd.to_datetime(report.get("created_at"), errors="coerce")
    if pd.isna(created_at):
        return pd.Timestamp.min
    return created_at

def nutrient_names_from_reports(reports):
    names = {
        str(result.get("Nutrient", ""))
        for report in reports
        for result in report.get("results", [])
        if result.get("Nutrient")
    }
    return sorted(names, key=nutrient_display_name)

def nutrient_readings_from_reports(reports, nutrient):
    readings = []
    for report in sorted(reports, key=report_sort_value):
        for result in report.get("results", []):
            if str(result.get("Nutrient", "")) != str(nutrient):
                continue

            status = str(result.get("Status", "Unknown"))
            value = pd.to_numeric(result.get("Value"), errors="coerce")
            readings.append({
                "report_id": report.get("report_id", ""),
                "date": report_display_date(report),
                "created_at": report_sort_value(report),
                "value": float(value) if not pd.isna(value) else None,
                "raw_value": result.get("Value"),
                "unit": result.get("Unit", ""),
                "low": pd.to_numeric(result.get("Low"), errors="coerce"),
                "high": pd.to_numeric(result.get("High"), errors="coerce"),
                "status": status,
                "valid": is_valid_trend_reading(status, value),
            })
    return readings

def latest_nutrient_reading(readings):
    if not readings:
        return None
    return sorted(readings, key=lambda reading: reading["created_at"])[-1]

def valid_nutrient_readings(readings):
    return [reading for reading in readings if reading.get("valid")]

def nutrient_delta_text(valid_readings):
    if len(valid_readings) < 2:
        return tr("No previous valid reading", "لا توجد قراءة صالحة سابقة")

    latest = valid_readings[-1]
    previous = valid_readings[-2]
    delta = latest["value"] - previous["value"]
    if abs(delta) < 0.000001:
        return tr("No change", "لا يوجد تغير")

    sign = "+" if delta > 0 else ""
    return tr(
        f"{sign}{delta:g} {latest.get('unit', '')} since previous",
        f"{sign}{delta:g} {latest.get('unit', '')} منذ القراءة السابقة",
    )

def nutrient_range_label(reading):
    if reading is None:
        return tr("Reference range unavailable", "النطاق المرجعي غير متاح")
    low = reading.get("low")
    high = reading.get("high")
    unit = reading.get("unit", "")
    if pd.isna(low) or pd.isna(high):
        return tr("Reference range unavailable", "النطاق المرجعي غير متاح")
    return tr(
        f"Normal range: {float(low):g}-{float(high):g} {unit}",
        f"النطاق الطبيعي: {float(low):g}-{float(high):g} {unit}",
    )

def sparkline_svg(valid_readings, color):
    if len(valid_readings) < 2:
        return f"""
        <div class="vv-sparkline-empty">
            {safe_html(tr("Need two valid readings", "تحتاج قراءتين صالحتين"))}
        </div>
        """

    values = [reading["value"] for reading in valid_readings]
    min_value = min(values)
    max_value = max(values)
    span = max(max_value - min_value, 1)
    width = 220
    height = 46
    points = []
    circles = []
    for index, value in enumerate(values):
        x = 8 + (index / (len(values) - 1)) * (width - 16)
        y = height - 8 - ((value - min_value) / span) * (height - 16)
        points.append(f"{x:.1f},{y:.1f}")
        circles.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.2" fill="{color}" />')

    return f"""
    <svg class="vv-sparkline" viewBox="0 0 {width} {height}" preserveAspectRatio="none" role="img">
        <line x1="8" y1="{height - 8}" x2="{width - 8}" y2="{height - 8}" stroke="rgba(255,255,255,0.12)" stroke-width="1" />
        <polyline fill="none" stroke="{color}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" points="{' '.join(points)}" />
        {''.join(circles)}
    </svg>
    """


def render_selected_nutrient_timeline(reports, nutrient):
    if not nutrient:
        return

    readings = nutrient_readings_from_reports(reports, nutrient)
    valid_readings = valid_nutrient_readings(readings)
    invalid_count = len([reading for reading in readings if not reading.get("valid")])

    section_title(
        tr(
            f"{nutrient_display_name(nutrient)} Timeline",
            f"تطور {nutrient_display_name(nutrient)} عبر الزمن",
        ),
        22,
        "",
    )

    if invalid_count:
        st.warning(tr(
            f"{invalid_count} invalid reading(s) were excluded from this timeline.",
            f"تم استبعاد {invalid_count} قراءة غير صالحة من هذا الخط الزمني."
        ))

    if not valid_readings:
        st.info(tr(
            "No valid readings to display.",
            "لا توجد قراءات صالحة للعرض."
        ))
        return

    trend_df = pd.DataFrame(valid_readings)
    marker_colors = [status_color(status) for status in trend_df["status"]]
    draw_mode = "lines+markers+text" if len(valid_readings) >= 2 else "markers+text"
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=trend_df["date"],
        y=trend_df["value"],
        mode=draw_mode,
        text=[f"{value:g}" for value in trend_df["value"]],
        textposition="top center",
        line=dict(color="#00BFFF", width=3),
        marker=dict(size=14 if len(valid_readings) == 1 else 12, color=marker_colors, line=dict(color="#ffffff", width=2)),
        customdata=[
            [status_text(row["status"]), f"{row['value']:g} {row.get('unit', '')}"]
            for _, row in trend_df.iterrows()
        ],
        hovertemplate="%{x}<br>%{customdata[1]}<br>%{customdata[0]}<extra></extra>",
    ))

    low_values = trend_df["low"].dropna()
    high_values = trend_df["high"].dropna()
    if not low_values.empty and not high_values.empty:
        low = float(low_values.iloc[-1])
        high = float(high_values.iloc[-1])
        fig.add_hrect(y0=low, y1=high, fillcolor="rgba(29,185,84,0.10)", line_width=0, layer="below")
        fig.add_hline(y=low, line_color="#1DB954", line_dash="dot")
        fig.add_hline(y=high, line_color="#1DB954", line_dash="dot")

    grid_color = "rgba(0,0,0,0.06)" if is_light_theme else "rgba(255,255,255,0.06)"
    axis_color = "#5a6a7a" if is_light_theme else "#7A9BB5"
    font_color = "#5a6a7a" if is_light_theme else "#9AAAB8"
    fig.update_layout(
        height=400,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color=font_color, family="Plus Jakarta Sans, Cairo"),
        margin=dict(l=24, r=24, t=24, b=48),
        xaxis=dict(showgrid=False, color=axis_color),
        yaxis=dict(gridcolor=grid_color, title=trend_df["unit"].iloc[-1], color=axis_color),
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

def build_dashboard_html(reports):
    latest = reports[-1]
    counts = latest.get("summary", {})
    normal_count = counts.get("normal", 0)
    deficient_count = counts.get("deficient", 0)
    excessive_count = counts.get("excessive", 0)
    follow_up = deficient_count + excessive_count + counts.get("invalid", 0)
    total = counts.get("total", 0)
    days_since = dashboard_days_since_last()
    last_date = report_display_date(latest)
    dir_val = "rtl" if is_arabic else "ltr"
    align = "right" if is_arabic else "left"
    light = is_light_theme
    t_sub = "#5a6a7a" if light else "#B8C8D8"

    # Banner
    if follow_up == 0 and total > 0:
        b_color, b_bg, b_icon = "#1DB954", "rgba(29,185,84,0.12)", "✅"
        b_title = tr("All Results Normal", "جميع النتائج طبيعية")
        b_text = tr(f"All {total} nutrient(s) within healthy range.", f"جميع الـ {total} عناصر ضمن النطاق الطبيعي.")
    elif follow_up > 0:
        b_color = "#FFA500" if follow_up < total else "#FF4B4B"
        b_bg = "rgba(255,165,0,0.12)" if follow_up < total else "rgba(255,75,75,0.12)"
        b_icon = "⚠️"
        b_title = tr("Needs Attention", "يحتاج متابعة")
        b_text = tr(f"{follow_up}/{total} result(s) need attention.", f"{follow_up} من {total} تحتاج متابعة.")
    else:
        b_color, b_bg, b_icon = "#7A9BB5", "rgba(255,255,255,0.04)", "📊"
        b_title = tr("No Data", "لا بيانات")
        b_text = ""

    # Reminder
    days_left, next_date = days_until_next_test()
    if days_left is not None:
        if days_left > 30:
            r_color, r_bg, r_icon = "#1DB954", "rgba(29,185,84,0.10)", "🟢"
        elif days_left > 7:
            r_color, r_bg, r_icon = "#FFA500", "rgba(255,165,0,0.10)", "🟡"
        elif days_left > 0:
            r_color, r_bg, r_icon = "#FF4B4B", "rgba(255,75,75,0.10)", "🔴"
        else:
            r_color, r_bg, r_icon = "#FF4B4B", "rgba(255,75,75,0.15)", "⏰"

        if days_left > 0:
            r_main = tr(f"{days_left} days remaining", f"{days_left} يوم متبقي")
            r_sub = tr(f"Next: {next_date.strftime('%b %d, %Y')}", f"القادم: {next_date.strftime('%Y/%m/%d')}")
        elif days_left == 0:
            r_main = tr("Today!", "اليوم!")
            r_sub = tr("Your test is today.", "تحليلك اليوم.")
        else:
            r_main = tr(f"{abs(days_left)} days overdue", f"متأخر {abs(days_left)} يوم")
            r_sub = tr(f"Was due: {next_date.strftime('%b %d, %Y')}", f"كان: {next_date.strftime('%Y/%m/%d')}")
        reminder_html = f"""
        <div class="db-reminder" style="background:{r_bg}; border-color:{r_color}40;">
            <div class="db-reminder-icon">{r_icon}</div>
            <div class="db-reminder-content">
                <div class="db-reminder-countdown" style="color:{r_color};">{safe_html(r_main)}</div>
                <div class="db-reminder-sub">{safe_html(r_sub)}</div>
            </div>
        </div>
        """
    else:
        no_rem_color = "#0070CC" if light else "#00BFFF"
        reminder_html = f"""
        <div class="db-reminder" style="background:rgba(0,140,255,0.06); border-color:rgba(0,140,255,0.25);">
            <div class="db-reminder-icon">📅</div>
            <div class="db-reminder-content">
                <div class="db-reminder-countdown" style="color:{no_rem_color};">{safe_html(tr("No Reminder Set", "لا يوجد تذكير"))}</div>
                <div class="db-reminder-sub">{safe_html(tr("Set one below to track your next test.", "حدد تذكير أدناه لمتابعة تحليلك القادم."))}</div>
            </div>
        </div>
        """

    # Nutrient cards data
    nutrient_names = nutrient_names_from_reports(reports)
    tracking_cards = ""
    for nutrient in nutrient_names:
        readings = nutrient_readings_from_reports(reports, nutrient)
        latest_r = latest_nutrient_reading(readings)
        valid_r = valid_nutrient_readings(readings)
        status = latest_r.get("status", "Unknown") if latest_r else "Unknown"
        color = status_color(status)
        value = latest_r.get("value") if latest_r else None
        raw_value = latest_r.get("raw_value", "") if latest_r else ""
        unit = latest_r.get("unit", "") if latest_r else ""
        val_display = f"{dashboard_number(value if value is not None else raw_value)} {safe_html(unit)}".strip()
        delta = nutrient_delta_text(valid_r)
        range_label = nutrient_range_label(latest_r)
        spark = sparkline_svg(valid_r, color)

        status_label = status_text(status)
        tracking_cards += f"""
        <div class="db-track-card" style="border-left-color:{color};">
            <div class="db-track-pill" style="background:{color}20; color:{color};">{safe_html(status_label)}</div>
            <div class="db-track-name">{safe_html(nutrient_display_name(nutrient))}</div>
            <div class="db-track-value" style="color:{color};">{val_display}</div>
            <div class="db-track-range">{safe_html(range_label)}</div>
            <div class="db-track-delta">{safe_html(delta)}</div>
            {spark}
        </div>
        """

    # Stats cards (3 cards)
    stats_html = f"""
    <div class="db-stats">
        <div class="db-stat-card">
            <div class="db-stat-icon">📅</div>
            <div class="db-stat-value">{safe_html(last_date)}</div>
            <div class="db-stat-label">{safe_html(tr("Last Test", "آخر تحليل"))}</div>
        </div>
        <div class="db-stat-card">
            <div class="db-stat-icon">🧪</div>
            <div class="db-stat-value">{total}</div>
            <div class="db-stat-label">{safe_html(tr("Nutrients", "عناصر"))}</div>
        </div>
        <div class="db-stat-card" style="{'border-color:#FF4B4B40;' if follow_up else ''}">
            <div class="db-stat-icon">{'⚠️' if follow_up else '✅'}</div>
            <div class="db-stat-value" style="color:{'#FF4B4B' if follow_up else '#1DB954'};">{follow_up}</div>
            <div class="db-stat-label">{safe_html(tr("Need Attention", "تحتاج متابعة"))}</div>
        </div>
    </div>
    """

    return f"""
<div class="db-root" style="direction:{dir_val}; text-align:{align};">

    <!-- Health Banner -->
    <div class="db-banner" style="background:{b_bg}; border-color:{b_color}40;">
        <span class="db-banner-icon">{b_icon}</span>
        <div class="db-banner-body">
            <div class="db-banner-title" style="color:{b_color};">{safe_html(b_title)}</div>
            <div class="db-banner-text">{safe_html(b_text)}</div>
        </div>
    </div>

    <!-- Quick Stats -->
    {stats_html}

    <!-- Reminder -->
    {reminder_html}

    <!-- Tracking Section Title -->
    <div class="db-section-title">{safe_html(tr("Vitamin Tracking", "متابعة الفيتامينات"))}</div>

    <!-- Tracking Cards -->
    <div class="db-track-grid">
        {tracking_cards if tracking_cards else f'<div class="db-empty">{safe_html(tr("No nutrients to track yet.", "لا عناصر للمتابعة بعد."))}</div>'}
    </div>

</div>
"""

def get_dashboard_css():
    light = is_light_theme
    text_main = "#1a2332" if light else "#F0F4F8"
    text_muted = "#5a6a7a" if light else "#7A9BB5"
    text_sub = "#6b7b8b" if light else "#9AAAB8"
    card_bg = "rgba(0,0,0,0.03)" if light else "rgba(255,255,255,0.03)"
    card_border = "rgba(0,0,0,0.08)" if light else "rgba(255,255,255,0.08)"
    card_hover_shadow = "0 8px 24px rgba(0,0,0,0.08)" if light else "0 8px 24px rgba(0,0,0,0.2)"
    section_border = "rgba(0,0,0,0.08)" if light else "rgba(255,255,255,0.06)"
    sparkline_bg = "rgba(0,0,0,0.03)" if light else "rgba(255,255,255,0.03)"
    delta_bg = "rgba(0,140,255,0.08)" if light else "rgba(0,191,255,0.08)"
    delta_color = "#0070CC" if light else "#00BFFF"

    return f"""
<style>
.db-root {{
    font-family: 'Plus Jakarta Sans', 'Cairo', -apple-system, sans-serif;
    padding: 0; margin: 0;
}}

/* Banner */
.db-banner {{
    border-radius: 16px; padding: 20px 24px; margin-bottom: 20px;
    display: flex; align-items: center; gap: 16px;
    border: 1px solid; backdrop-filter: blur(8px);
}}
.db-banner-icon {{ font-size: 34px; flex-shrink: 0; }}
.db-banner-title {{ font-size: 18px; font-weight: 800; margin-bottom: 4px; }}
.db-banner-text {{ font-size: 13px; color: {text_sub}; line-height: 1.5; }}

/* Stats Grid */
.db-stats {{
    display: grid; grid-template-columns: repeat(3, 1fr);
    gap: 12px; margin-bottom: 20px;
}}
.db-stat-card {{
    background: {card_bg}; border: 1px solid {card_border};
    border-radius: 14px; padding: 18px 16px; text-align: center;
    transition: transform 0.2s, border-color 0.2s, box-shadow 0.2s;
}}
.db-stat-card:hover {{ transform: translateY(-2px); border-color: rgba(0,140,255,0.3); box-shadow: {card_hover_shadow}; }}
.db-stat-icon {{ font-size: 24px; margin-bottom: 8px; }}
.db-stat-value {{
    font-size: 20px; font-weight: 800; color: {text_main};
    line-height: 1.2; margin-bottom: 4px;
    word-break: break-word;
}}
.db-stat-label {{ font-size: 11px; color: {text_muted}; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; }}

/* Reminder */
.db-reminder {{
    border-radius: 14px; padding: 20px 24px; margin-bottom: 20px;
    display: flex; align-items: center; gap: 16px;
    border: 1px solid; transition: transform 0.2s;
}}
.db-reminder:hover {{ transform: translateY(-1px); }}
.db-reminder-icon {{ font-size: 32px; flex-shrink: 0; }}
.db-reminder-content {{ flex: 1; }}
.db-reminder-countdown {{ font-size: 26px; font-weight: 800; line-height: 1.2; }}
.db-reminder-sub {{ font-size: 13px; color: {text_sub}; margin-top: 4px; }}

/* Section Title */
.db-section-title {{
    font-size: 20px; font-weight: 800; color: {text_main};
    margin: 24px 0 14px; padding-bottom: 8px;
    border-bottom: 1px solid {section_border};
}}

/* Tracking Grid */
.db-track-grid {{
    display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
    gap: 14px; margin-bottom: 20px;
}}
.db-track-card {{
    background: {card_bg}; border: 1px solid {card_border};
    border-left: 5px solid #6b7280; border-radius: 14px;
    padding: 18px 20px; transition: transform 0.2s, box-shadow 0.2s;
}}
.db-track-card:hover {{ transform: translateY(-2px); box-shadow: {card_hover_shadow}; }}
.db-track-pill {{
    display: inline-block; border-radius: 999px; padding: 3px 10px;
    font-size: 11px; font-weight: 800; margin-bottom: 8px;
}}
.db-track-name {{ font-size: 16px; font-weight: 800; color: {text_main}; margin-bottom: 4px; }}
.db-track-value {{ font-size: 28px; font-weight: 800; line-height: 1.1; margin: 6px 0; }}
.db-track-range {{ font-size: 12px; color: {text_muted}; margin-bottom: 4px; }}
.db-track-delta {{
    display: inline-block; background: {delta_bg}; color: {delta_color};
    border-radius: 999px; padding: 3px 10px; font-size: 11px; font-weight: 700; margin-top: 6px;
}}

/* Sparkline */
.vv-sparkline {{ width: 100%; height: 48px; margin-top: 12px; }}
.vv-sparkline-empty {{
    height: 48px; margin-top: 12px; border-radius: 8px;
    background: {sparkline_bg}; color: {text_muted};
    display: flex; align-items: center; justify-content: center;
    font-size: 11px; font-weight: 700;
}}

/* Empty state */
.db-empty {{
    grid-column: 1 / -1; text-align: center; padding: 32px;
    color: {text_muted}; font-size: 14px;
    border: 1px dashed rgba(0,140,255,0.2); border-radius: 14px;
}}

/* Responsive */
@media (max-width: 900px) {{ .db-stats {{ grid-template-columns: repeat(2, 1fr); }} }}
@media (max-width: 560px) {{
    .db-stats {{ grid-template-columns: 1fr; }}
    .db-track-grid {{ grid-template-columns: 1fr; }}
}}
</style>
"""

def render_report_dashboard(reports):
    latest = reports[-1]
    latest_df = report_to_df(latest)

    # Render full custom HTML dashboard
    st.html(get_dashboard_css() + build_dashboard_html(reports))

    # Interactive: Reminder controls (Streamlit widgets)
    render_reminder_card()

    # Interactive: Timeline chart for selected nutrient
    nutrient_names = nutrient_names_from_reports(reports)
    if nutrient_names:
        selected_nutrient = st.selectbox(
            tr("Choose nutrient for timeline", "اختر العنصر لعرض الخط الزمني"),
            options=nutrient_names,
            index=0,
            format_func=nutrient_display_name,
            key="tracking_selected_nutrient",
        )
        render_selected_nutrient_timeline(reports, selected_nutrient)

    # Report History (collapsed)
    with st.expander(tr("Report History", "سجل التقارير"), expanded=False):
        render_report_history_table(reports)
        render_report_actions(latest, latest_df, key_prefix="latest")

# =========================================
# Session state
# =========================================
if "manual_items" not in st.session_state:
    st.session_state["manual_items"] = []

if "results_df" not in st.session_state:
    st.session_state["results_df"] = pd.DataFrame()

if "csv_input_df" not in st.session_state:
    st.session_state["csv_input_df"] = None

if st.session_state.get("language_changed", False):
    if st.session_state["csv_input_df"] is not None:
        analyzed = [analyze_row(row) for _, row in st.session_state["csv_input_df"].iterrows()]
        st.session_state["results_df"] = pd.DataFrame(analyzed)
    elif len(st.session_state["manual_items"]) > 0:
        input_df = pd.DataFrame(st.session_state["manual_items"])
        analyzed = [analyze_row(row) for _, row in input_df.iterrows()]
        st.session_state["results_df"] = pd.DataFrame(analyzed)
    st.session_state["language_changed"] = False

# =========================================
# HOME TAB
# =========================================
if active_tab == "home":
    section_title(tr("Input Method", "طريقة الإدخال"), icon="")

    manual_label = tr("Manual Input", "إدخال يدوي")
    csv_label = tr("Upload CSV", "رفع CSV")
    history_pdf_label = tr("Restore PDF", "استرجاع PDF")

    input_mode = st.radio(
        tr("Input Method", "طريقة الإدخال"),
        [manual_label, csv_label, history_pdf_label],
        label_visibility="collapsed",
        horizontal=True,
    )

    # ── Manual input ──────────────────────────
    if input_mode == manual_label:
        section_title(tr("Enter Lab Values", "أدخل قيم التحليل"), 22, "")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            age = st.number_input(tr("Age", "العمر"), min_value=0, max_value=120, value=25, step=1)
        with col2:
            gender_text = st.selectbox(tr("Gender", "الجنس"), [tr("Male", "ذكر"), tr("Female", "أنثى")])
        with col3:
            nutrient = st.selectbox(
                tr("Nutrient", "العنصر"),
                list(REFERENCE_RANGES.keys()) + ["Ferritin"],
                format_func=nutrient_display_name,
            )
        with col4:
            value = st.number_input(tr("Value", "القيمة"), min_value=0.0, value=0.0, step=0.1)

        add_col, analyze_col, clear_col = st.columns(3)
        with add_col:
            if st.button(f"➕  {tr('Add Nutrient', 'إضافة العنصر')}", use_container_width=True):
                if value <= 0:
                    st.warning(tr(
                        "Enter a lab value greater than zero before adding it.",
                        "أدخل قيمة تحليل أكبر من صفر قبل إضافة العنصر."
                    ))
                else:
                    gender_value = 1 if gender_text in ["Male", "ذكر"] else 2
                    st.session_state["manual_items"].append({
                        "Age": age, "Gender": gender_value,
                        "Nutrient": normalize_nutrient_name(nutrient), "Value": value,
                    })
        with analyze_col:
            analyze_manual_clicked = st.button(
                f"🔬  {tr('Analyze', 'تحليل')}",
                use_container_width=True,
                type="primary",
            )
        with clear_col:
            if st.button(f"🗑️  {tr('Clear All', 'مسح الكل')}", use_container_width=True):
                st.session_state["manual_items"] = []
                st.session_state["csv_input_df"] = None
                st.session_state["results_df"] = pd.DataFrame()
                st.rerun()

        # Added nutrients table
        section_title(tr("Added Nutrients", "العناصر المضافة"), 20, "")

        if len(st.session_state["manual_items"]) == 0:
            st.html(f"""
<div style="text-align:center; padding:28px; border:1px dashed rgba(0,191,255,0.20);
            border-radius:14px; color:#5A7A8A; font-size:14px;">
    {tr("No nutrients added yet. Use the form above to add lab values.",
        "لم تتم إضافة أي عنصر حتى الآن. استخدم النموذج أعلاه لإضافة قيم التحاليل.")}
</div>
""")
        else:
            dir_val = "rtl" if is_arabic else "ltr"
            align   = "right" if is_arabic else "left"
            header_cells = "".join(
                f'<th style="padding:10px 14px; font-size:12px; font-weight:700; color:#7A9BB5; '
                f'text-transform:uppercase; letter-spacing:0.4px; text-align:{align}; '
                f'background:rgba(0,191,255,0.04);">{h}</th>'
                for h in [tr("Age","العمر"), tr("Gender","الجنس"),
                          tr("Nutrient","العنصر"), tr("Value","القيمة")]
            )
            rows_html = ""
            for i, item in enumerate(st.session_state["manual_items"]):
                shown_gender = tr("Male","ذكر") if item["Gender"] == 1 else tr("Female","أنثى")
                rows_html += f"""
<tr style="border-bottom:1px solid rgba(255,255,255,0.04);">
    <td style="padding:10px 14px; font-size:14px; color:#B8C8D8; text-align:{align};">{item['Age']}</td>
    <td style="padding:10px 14px; font-size:14px; color:#B8C8D8; text-align:{align};">{shown_gender}</td>
    <td style="padding:10px 14px; font-size:14px; font-weight:600; color:#F0F4F8; text-align:{align};">{nutrient_display_name(item['Nutrient'])}</td>
    <td style="padding:10px 14px; font-size:14px; font-weight:700; color:#00BFFF; text-align:{align};">{item['Value']}</td>
</tr>"""

            st.html(f"""
<div style="overflow-x:auto; border-radius:14px; border:1px solid rgba(255,255,255,0.07); direction:{dir_val};">
    <table style="width:100%; border-collapse:collapse; font-family:'Plus Jakarta Sans','Cairo',sans-serif;">
        <thead><tr>{header_cells}</tr></thead>
        <tbody>{rows_html}</tbody>
    </table>
</div>""")

            remove_options = list(range(len(st.session_state["manual_items"])))
            remove_index = st.selectbox(
                tr("Select nutrient to remove", "اختر العنصر المراد حذفه"),
                options=remove_options,
                format_func=lambda idx: (
                    f"{idx + 1}. {nutrient_display_name(st.session_state['manual_items'][idx]['Nutrient'])} - "
                    f"{st.session_state['manual_items'][idx]['Value']}"
                ),
                key="manual_remove_index",
            )
            if st.button(tr("Remove Selected Nutrient", "حذف العنصر المحدد"), use_container_width=True):
                st.session_state["manual_items"].pop(remove_index)
                st.rerun()

        if analyze_manual_clicked:
            if len(st.session_state["manual_items"]) == 0:
                st.warning(tr("Please add at least one nutrient.", "يرجى إضافة عنصر واحد على الأقل."))
            else:
                with st.spinner(tr("Analyzing...", "جاري التحليل...")):
                    input_df = pd.DataFrame(st.session_state["manual_items"])
                    analyzed = [analyze_row(r) for _, r in input_df.iterrows()]
                    st.session_state["results_df"] = pd.DataFrame(analyzed)
                    save_analysis_report(
                        st.session_state["results_df"],
                        tr("Manual Input", "إدخال يدوي"),
                    )

    # ── CSV input ──────────────────────────────
    elif input_mode == csv_label:
        section_title(tr("Upload CSV File", "رفع ملف CSV"), 22, "")

        st.html(f"""
<div style="background:rgba(0,191,255,0.04); border:1px dashed rgba(0,191,255,0.25);
            border-radius:14px; padding:16px 20px; margin-bottom:16px; font-size:13.5px; color:#7A9BB5;
            direction:{'rtl' if is_arabic else 'ltr'}; text-align:{'right' if is_arabic else 'left'};">
    <strong style="color:#00BFFF;">  {tr("Required columns:", "الأعمدة المطلوبة:")}</strong>
    &nbsp;Nutrient, Value &nbsp;|&nbsp;
    <strong style="color:#9AAAB8;">{tr("Optional:", "اختياري:")}</strong> Age, Gender
</div>
""")

        uploaded_file = st.file_uploader(
            tr("Upload CSV file", "ارفع ملف CSV"),
            type=["csv"]
        )

        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            st.markdown(f"**{tr('Preview:', 'معاينة:')}**")
            st.dataframe(df, use_container_width=True)

            required_columns = ["Nutrient", "Value"]
            missing_columns  = [col for col in required_columns if col not in df.columns]

            if missing_columns:
                st.error(tr(
                    f"Missing required columns: {missing_columns}",
                    f"الأعمدة الناقصة: {missing_columns}"
                ))
                st.info(tr(
                    "Required columns: Nutrient, Value. Optional: Age, Gender.",
                    "الأعمدة المطلوبة: Nutrient و Value. الاختيارية: Age و Gender."
                ))
            else:
                if "Age"    not in df.columns: df["Age"]    = None
                if "Gender" not in df.columns: df["Gender"] = 1

                if st.button(f"🔬  {tr('Analyze CSV', 'تحليل ملف CSV')}", use_container_width=True, type="primary"):
                    analyzed = []
                    with st.spinner(tr("Analyzing CSV...", "جاري تحليل الملف...")):
                        for _, row in df.iterrows():
                            try:
                                analyzed.append(analyze_row(row))
                            except Exception as e:
                                analyzed.append({
                                    "Age": row.get("Age", None),
                                    "Gender": row.get("Gender", None),
                                    "Nutrient": row.get("Nutrient", "Unknown"),
                                    "Value": row.get("Value", None),
                                    "Unit": "Unknown", "Low": None, "High": None,
                                    "Status": "Error",
                                    "Explanation": tr(f"Could not analyze: {e}", f"تعذر التحليل: {e}"),
                                    "Possible Causes": tr("Not available", "غير متوفر"),
                                    "Recommendations": tr("Check data format.", "تأكد من صيغة البيانات."),
                                    **unavailable_model_fields(),
                                })
                    st.session_state["results_df"]  = pd.DataFrame(analyzed)
                    st.session_state["csv_input_df"] = df.copy()
                    save_analysis_report(
                        st.session_state["results_df"],
                        tr("CSV Upload", "رفع CSV"),
                    )

    else:
        render_history_restore_panel()

    # ── Results ────────────────────────────────
    results_df = st.session_state["results_df"]

    if not results_df.empty:
        # ── Step 1: Summary stats ─────────────
        section_title(tr("Results Summary", "ملخص النتائج"), 26, "")
        render_summary_stats(results_df)

        # ── Step 2: Status Distribution chart ─
        valid_results = results_df[
            results_df["Status"].isin(["Deficient", "Normal", "Excessive"])
        ].copy()

        if not valid_results.empty:
            if is_arabic:
                valid_results["Status_Display"] = valid_results["Status"].map({
                    "Deficient": "ناقص",
                    "Normal": "طبيعي",
                    "Excessive": "مرتفع"
                })
                label_col = "Status_Display"
                color_map = {
                    "ناقص": "#FF4B4B",
                    "طبيعي": "#1DB954",
                    "مرتفع": "#FFA500"
                }
            else:
                label_col = "Status"
                color_map = {
                    "Deficient": "#FF4B4B",
                    "Normal": "#1DB954",
                    "Excessive": "#FFA500"
                }

            fig_summary = px.pie(
                valid_results.groupby(label_col).size().reset_index(name="Count"),
                names=label_col,
                values="Count",
                color=label_col,
                color_discrete_map=color_map,
                hole=0.55,
                title=tr("Status Distribution", "توزيع الحالات"),
            )
            fig_summary.update_traces(
                textfont=dict(color="white", size=13, family="Plus Jakarta Sans, Cairo"),
                marker=dict(line=dict(color="rgba(0,0,0,0.3)", width=2)),
            )
            fig_summary.update_layout(
                height=380,
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#9AAAB8", family="Plus Jakarta Sans, Cairo"),
                legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#B8C8D8")),
                title=dict(font=dict(color="#B8C8D8", size=15)),
            )
            st.plotly_chart(fig_summary, use_container_width=True, config={"displayModeBar": False})

        # ── Step 3: Smart Result Cards ────────
        section_title(tr("Detailed Results", "تفاصيل النتائج"), 22, "")
        for _, row in results_df.iterrows():
            render_result_card(row)

        # ── Invalid warnings ──────────────────
        invalid_results = results_df[results_df["Status"] == "Invalid"].copy()
        if not invalid_results.empty:
            section_title(tr("Input Warnings", "تنبيهات الإدخال"), 22, "⚠️")
            for _, row in invalid_results.iterrows():
                st.error(tr(
                    f"{row['Nutrient']} value ({row['Value']}) looks unrealistic. Please check the input.",
                    f"قيمة {row['Nutrient']} ({row['Value']}) تبدو غير منطقية. يرجى التأكد من المدخلات."
                ))

        # ── Step 4: Download ──────────────────
        csv_data = results_df.to_csv(index=False)
        st.download_button(
            label=f"  {tr('Download Results CSV', 'تحميل النتائج CSV')}",
            data=csv_data,
            file_name="vitavision_results.csv",
            mime="text/csv",
            use_container_width=True,
        )

# =========================================
# DASHBOARD TAB
# =========================================
if active_tab == "dashboard":
    results_df = st.session_state.get("results_df", pd.DataFrame())
    if not results_df.empty:
        save_analysis_report(results_df, tr("Current Session", "الجلسة الحالية"))
    reports = get_report_history()
    dir_val = "rtl" if is_arabic else "ltr"
    align = "right" if is_arabic else "left"

    if not reports:
        st.html(f"""
<div style="background:rgba(255,255,255,0.03); border:1px dashed rgba(0,191,255,0.20);
    border-radius:14px; padding:36px; color:#7A9BB5; text-align:center; direction:{dir_val};">
    <div style="font-size:16px; font-weight:700; margin-bottom:8px;">{safe_html(tr("No Analysis Results Yet", "لا توجد نتائج تحليل بعد"))}</div>
    <div style="font-size:13px;">
        {safe_html(tr(
            "Enter lab values manually or upload a CSV file from the Home tab, then run the analysis to unlock the dashboard.",
            "أدخل قيم التحاليل يدويًا أو ارفع ملف CSV من تبويب الرئيسية، ثم شغل التحليل لتظهر لوحة التحكم."
        ))}
    </div>
</div>
""")
        st.info(tr(
            "Report History & Backup export becomes available after analysis or after restoring a VitaVision PDF history file from Home.",
            "سيظهر تصدير سجل التقارير والنسخ الاحتياطي بعد التحليل أو بعد استرجاع ملف سجل VitaVision PDF من الصفحة الرئيسية."
        ))
    else:
        dashboard_v2.render(reports, ctx={
            "tr": tr,
            "is_arabic": is_arabic,
            "is_light_theme": is_light_theme,
            "nutrient_display_name": nutrient_display_name,
            "status_text": status_text,
            "status_color": status_color,
            "get_possible_causes": get_possible_causes,
            "get_recommendations": get_recommendations,
            "load_reminder": load_reminder,
            "save_reminder": save_reminder,
            "delete_reminder": delete_reminder,
            "days_until_next_test": days_until_next_test,
            "nutrient_readings_from_reports": nutrient_readings_from_reports,
            "report_to_df": report_to_df,
            "report_display_date": report_display_date,
            "delete_analysis_report": delete_analysis_report,
        })
        render_history_backup_panel(reports)

# =========================================
# ABOUT TAB (About + Contact merged)
# =========================================
if active_tab == "about":
    dir_val = "rtl" if is_arabic else "ltr"
    align   = "right" if is_arabic else "left"

    # About VitaVision
    st.html(f"""
<div class="vv-card" style="direction:{dir_val}; text-align:{align};">
    <div class="vv-card-title">{tr("About VitaVision", "عن VitaVision")}</div>
    <div class="vv-card-text">
        {tr(
            "VitaVision is an intelligent health tool that helps you interpret vitamin and mineral lab results instantly. "
            "It classifies your values as Deficient, Normal, or Excessive using medical reference ranges and a trained ML model, "
            "then provides clear explanations and recommendations.",
            "VitaVision أداة صحية ذكية تساعدك على تفسير نتائج تحاليل الفيتامينات والمعادن بشكل فوري. "
            "يصنف قيمك إلى ناقص أو طبيعي أو مرتفع باستخدام نطاقات مرجعية طبية ونموذج ذكاء اصطناعي مدرّب، "
            "ثم يقدم شرحاً واضحاً وتوصيات عملية."
        )}
    </div>
</div>
""")

    # How It Works
    steps = [
        tr("Enter your lab values manually or upload a CSV file", "أدخل قيم تحاليلك يدوياً أو ارفع ملف CSV"),
        tr("The system classifies each value against medical reference ranges", "النظام يصنف كل قيمة مقارنة بالنطاقات المرجعية الطبية"),
        tr("An ML model validates the classification with a confidence score", "نموذج ذكاء اصطناعي يؤكد التصنيف مع نسبة ثقة"),
        tr("You receive explanations, possible causes, and recommendations", "تحصل على شرح وأسباب محتملة وتوصيات"),
    ]
    steps_html = "".join(
        f'<li style="margin-bottom:10px; color:var(--text-secondary, #B8C8D8);">'
        f'<span style="color:#00BFFF; font-weight:700;">{i+1}.</span> {step}</li>'
        for i, step in enumerate(steps)
    )
    st.html(f"""
<div class="vv-card" style="direction:{dir_val}; text-align:{align};">
    <div class="vv-card-title">{tr("How It Works", "كيف يعمل")}</div>
    <ul style="list-style:none; padding:0; margin:12px 0 0;">{steps_html}</ul>
</div>
""")

    # Contact section
    st.html(f"""
<div class="vv-card" style="direction:{dir_val}; text-align:{align};">
    <div class="vv-card-title">{tr("Contact", "تواصل")}</div>
    <div class="vv-card-text" style="margin-bottom:16px;">
        {tr(
            "For inquiries or feedback:",
            "للاستفسارات أو الملاحظات:"
        )}
    </div>
    <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(200px,1fr)); gap:12px;">
        <div style="background:rgba(0,191,255,0.05); border:1px solid rgba(0,191,255,0.18);
                    border-radius:10px; padding:14px 16px; display:flex; align-items:center; gap:10px;">
            <span style="font-size:20px;">📧</span>
            <div>
                <div style="font-size:11px; color:#7A9BB5; text-transform:uppercase;">Email</div>
                <div style="font-size:13px; font-weight:600; color:var(--text-secondary, #B8C8D8);">—</div>
            </div>
        </div>
        <div style="background:rgba(0,119,181,0.07); border:1px solid rgba(0,119,181,0.25);
                    border-radius:10px; padding:14px 16px; display:flex; align-items:center; gap:10px;">
            <span style="font-size:20px;">🔗</span>
            <div>
                <div style="font-size:11px; color:#7A9BB5; text-transform:uppercase;">LinkedIn</div>
                <div style="font-size:13px; font-weight:600; color:var(--text-secondary, #B8C8D8);">—</div>
            </div>
        </div>
        <div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.12);
                    border-radius:10px; padding:14px 16px; display:flex; align-items:center; gap:10px;">
            <span style="font-size:20px;">💻</span>
            <div>
                <div style="font-size:11px; color:#7A9BB5; text-transform:uppercase;">GitHub</div>
                <div style="font-size:13px; font-weight:600; color:var(--text-secondary, #B8C8D8);">—</div>
            </div>
        </div>
    </div>
</div>
""")

    # Medical disclaimer
    st.html(f"""
<div class="disclaimer-banner" style="direction:{dir_val};">
    <span class="disclaimer-icon"></span>
    <div>
        <div class="disclaimer-title">{tr("Medical Disclaimer", "تنبيه طبي")}</div>
        <div class="disclaimer-text" style="text-align:{align};">
            {tr(
                "This tool is for educational purposes only. It does not replace medical diagnosis or professional consultation.",
                "هذه الأداة لأغراض تعليمية فقط. لا تغني عن التشخيص الطبي أو الاستشارة المهنية."
            )}
        </div>
    </div>
</div>
""")

# =========================================
# Footer
# =========================================
st.html("""
<div style="
    text-align: center;
    font-size: 13px;
    color: #3A5060;
    margin-top: 48px;
    padding: 20px;
    border-top: 1px solid rgba(255,255,255,0.05);
    font-family: 'Plus Jakarta Sans', 'Cairo', sans-serif;
">
    <span style="color:#005A80;">Vita</span><span style="color:#007A9E;">Vision</span>
    &nbsp;·&nbsp; © 2026 All rights reserved
</div>
""")

# =========================================
# Show disclaimer if not agreed
# =========================================
if not st.session_state["disclaimer_agreed"]:
    show_disclaimer()
