import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import html
import json
import hashlib
import joblib
from pathlib import Path

# =========================================
# Page configuration
# =========================================
st.set_page_config(
    page_title="VitaVision Health Analyzer",
    page_icon="IconVitaVision.png",
    layout="wide"
)

if "language" not in st.session_state:
    st.session_state["language"] = "English"

if "disclaimer_agreed" not in st.session_state:
    st.session_state["disclaimer_agreed"] = False

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
        title = "⚠️Medical Disclaimer⚠️"
        text = (
            "VitaVision provides health-related insights based on laboratory values and predefined medical reference ranges. "
            "It is intended for educational and awareness purposes only, and should not be considered a substitute for medical diagnosis, "
            "consultation, or treatment.\n\n"
            "Although VitaVision aims to provide useful and accurate interpretations, it does not take into account the user's medical history, "
            "health conditions, medications, or other clinical factors that may affect the results.\n\n"
            "By using VitaVision, you acknowledge the following:\n"
            "• The results are generated automatically and may not fully reflect your health condition.\n"
            "• VitaVision does not replace consultation with a licensed doctor or healthcare professional.\n"
            "• Any medical decisions should only be made after consulting a qualified specialist.\n\n"
            "You also agree to use VitaVision responsibly and understand that the developers are not responsible for any misuse, "
            "misinterpretation, or decisions made based on the provided information.\n\n"
            "If you have symptoms or abnormal results, please seek professional medical advice immediately."
        )
        button_text = "I Agree and Continue"
    else:
        title = "⚠️تنبيه طبي⚠️"
        text = (
            "يقدم نظام VitaVision معلومات وتحليلات صحية مبنية على نتائج الفحوصات المخبرية ونطاقات مرجعية طبية محددة، "
            "وهو مخصص لأغراض تعليمية وتوعوية فقط، ولا يُعتبر بديلاً عن التشخيص الطبي أو الاستشارة أو العلاج.\n\n"
            "رغم أن نظام VitaVision يسعى لتقديم تفسيرات دقيقة ومفيدة، إلا أنه لا يأخذ بعين الاعتبار التاريخ الطبي "
            "للمستخدم أو الحالات الصحية أو الأدوية أو العوامل السريرية الأخرى التي قد تؤثر على النتائج.\n\n"
            "باستخدامك لنظام VitaVision، فإنك تقر بما يلي:\n"
            "• النتائج يتم توليدها بشكل آلي وقد لا تعكس حالتك الصحية بشكل كامل.\n"
            "• لا يغني نظام VitaVision عن استشارة طبيب أو مختص صحي مرخص.\n"
            "• أي قرارات طبية يجب أن تتم فقط بعد الرجوع إلى مختص مؤهل.\n\n"
            "كما توافق على استخدام نظام VitaVision بمسؤولية، وتدرك أن مطوري التطبيق غير مسؤولين عن أي استخدام "
            "خاطئ أو تفسير غير دقيق أو قرارات يتم اتخاذها بناءً على هذه المعلومات.\n\n"
            "في حال وجود أي أعراض أو نتائج غير طبيعية، يرجى مراجعة مختص صحي بشكل فوري."
        )
        button_text = "أوافق وأتابع"

    dir_val = "rtl" if is_ar else "ltr"
    align_val = "right" if is_ar else "left"

    formatted_text = text.replace("\n\n", "<br><br>").replace("\n", "<br>")

    st.html(f"""
<div style="
    border: 1px solid rgba(0,191,255,0.4);
    border-radius: 18px;
    padding: 28px 30px;
    background: linear-gradient(145deg, rgba(0,15,30,0.98), rgba(0,25,45,0.95));
    box-shadow: 0 8px 40px rgba(0,191,255,0.08), inset 0 1px 0 rgba(255,255,255,0.04);
">
    <div style="
        text-align: center;
        color: #00BFFF;
        font-size: 22px;
        font-weight: 800;
        margin-bottom: 22px;
        letter-spacing: 0.3px;
        font-family: 'Segoe UI', sans-serif;
    ">
        {title}
    </div>
    <div style="
        width: 60px;
        height: 2px;
        margin: 0 auto 22px;
        border-radius: 2px;
    "></div>
    <div style="
        color: #D8E8F0;
        font-size: 14.5px;
        line-height: 1.9;
        direction: {dir_val};
        text-align: {align_val};
        font-family: 'Segoe UI', 'Helvetica Neue', sans-serif;
        background: rgba(0,191,255,0.03);
        border-radius: 12px;
        padding: 18px 20px;
        border: 1px solid rgba(0,191,255,0.1);
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
        "",
        ["English", "العربية"],
        default=st.session_state["language_segment"],
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
        "",
        ["Dark", "Light"],
        default=st.session_state["theme_segment"],
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
    margin-left: auto !important;
    margin-right: 0 !important;
}}

[data-testid="stSegmentedControl"] div[role="group"] {{
    width: fit-content !important;
    display: inline-flex !important;
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    align-items: center !important;
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

div[role="radiogroup"][aria-label="button group"] {{
    width: fit-content !important;
    display: inline-flex !important;
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    align-items: center !important;
    margin-left: auto !important;
    margin-right: 0 !important;
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
    max-width: 620px !important;
    margin-top: -2px !important;
    margin-bottom: 26px !important;
}}

[data-testid="stRadio"] div[role="radiogroup"] {{
    display: grid !important;
    grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
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
# Navigation tabs
# =========================================
home_tab, dashboard_tab, about_tab, contact_tab = st.tabs([
    tr("Home", " الرئيسية"),
    tr("Dashboard", "لوحة التحكم"),
    tr("About", "عن المشروع"),
    tr("Contact", "تواصل معنا")
])

# =========================================
# Header
# =========================================
def render_header():
    subtitle = tr("Smart Insight for Vitamin Health", "Smart Insight for Vitamin Health")
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
# Styled results table
# =========================================
def render_results_table(df):
    dir_val = "rtl" if is_arabic else "ltr"
    align   = "right" if is_arabic else "left"

    headers = [
        tr("Nutrient","العنصر"), tr("Value","القيمة"), tr("Unit","الوحدة"),
        tr("Status","الحالة"), tr("ML Prediction","تنبؤ الموديل"), tr("Model Agreement","توافق الموديل"),
        tr("Low","الأدنى"), tr("High","الأقصى"),
        tr("Age","العمر"), tr("Gender","الجنس"),
    ]

    header_cells = "".join(
        f'<th style="padding:11px 16px; font-size:12px; font-weight:700; color:#7A9BB5; '
        f'letter-spacing:0.5px; text-transform:uppercase; background:rgba(0,191,255,0.05); '
        f'white-space:nowrap; text-align:{align};">{h}</th>'
        for h in headers
    )

    rows_html = ""
    for _, row in df.iterrows():
        status  = row.get("Status", "")
        color   = status_color(status)
        icon    = status_icon(status)
        ml_prediction = str(row.get("ML Prediction", MODEL_UNAVAILABLE))
        ml_confidence = str(row.get("ML Confidence", MODEL_UNAVAILABLE))
        ml_color = status_color(ml_prediction) if ml_prediction in MODEL_VALID_STATUSES else "#7A9BB5"
        ml_label = ml_prediction_text(ml_prediction)
        if ml_confidence and ml_confidence != MODEL_UNAVAILABLE:
            ml_label = f"{ml_label} ({ml_confidence})"
        agreement = str(row.get("Model Agreement", MODEL_UNAVAILABLE))
        agreement_color = model_agreement_color(agreement)
        gender_display = tr("Male","ذكر") if str(row.get("Gender","")).lower() in ["male","1","m"] else tr("Female","أنثى")

        cells = [
            f'<td style="font-weight:700; color:#F0F4F8;">{nutrient_display_name(row.get("Nutrient",""))}</td>',
            f'<td style="font-weight:700; color:{color}; font-size:16px;">{row.get("Value","")}</td>',
            f'<td style="color:#7A9BB5;">{row.get("Unit","")}</td>',
            f'<td><span style="display:inline-flex; align-items:center; gap:5px; padding:4px 12px; '
            f'border-radius:999px; font-size:12px; font-weight:700; color:{color}; '
            f'background:{color}18; border:1px solid {color}44;">'
            f'{icon} {status_text(status)}</span></td>',
            f'<td><span style="display:inline-flex; align-items:center; gap:5px; padding:4px 12px; '
            f'border-radius:999px; font-size:12px; font-weight:700; color:{ml_color}; '
            f'background:{ml_color}18; border:1px solid {ml_color}44;">'
            f'{ml_label}</span></td>',
            f'<td><span style="display:inline-flex; align-items:center; gap:5px; padding:4px 12px; '
            f'border-radius:999px; font-size:12px; font-weight:700; color:{agreement_color}; '
            f'background:{agreement_color}18; border:1px solid {agreement_color}44;">'
            f'{model_agreement_text(agreement)}</span></td>',
            f'<td style="color:#9AAAB8;">{row.get("Low","")}</td>',
            f'<td style="color:#9AAAB8;">{row.get("High","")}</td>',
            f'<td style="color:#9AAAB8;">{row.get("Age","")}</td>',
            f'<td style="color:#9AAAB8;">{gender_display}</td>',
        ]

        row_cells = "".join(
            f'<td style="padding:12px 16px; font-size:14px; text-align:{align}; '
            f'border-bottom:1px solid rgba(255,255,255,0.04);">{cell[cell.find(">")+1:]}'
            for cell in cells
        )
        rows_html += f'<tr style="transition:background 0.15s;" onmouseover="this.style.background=\'rgba(0,191,255,0.04)\'" onmouseout="this.style.background=\'transparent\'">{row_cells}</tr>'

    st.html(f"""
<div style="overflow-x:auto; border-radius:16px; border:1px solid rgba(0,191,255,0.18);
            box-shadow:0 4px 24px rgba(0,0,0,0.20); direction:{dir_val};">
    <table style="width:100%; border-collapse:collapse; font-family:'Plus Jakarta Sans','Cairo',sans-serif;">
        <thead>
            <tr>{header_cells}</tr>
        </thead>
        <tbody>
            {rows_html}
        </tbody>
    </table>
</div>
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
REPORTS_FILE = Path(__file__).resolve().parent / "reports" / "vitavision_reports.json"
REPORT_SCHEMA_VERSION = 1
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
    if not REPORTS_FILE.exists():
        return []
    try:
        payload = json.loads(REPORTS_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []

    reports = payload.get("reports", payload if isinstance(payload, list) else [])
    if not isinstance(reports, list):
        return []

    return sorted(
        [report for report in reports if isinstance(report, dict)],
        key=lambda report: str(report.get("created_at", "")),
    )

def save_report_history(reports):
    REPORTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": REPORT_SCHEMA_VERSION,
        "reports": reports,
    }
    REPORTS_FILE.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

def refresh_report_history_state():
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
    reports = get_report_history()
    if any(existing.get("signature") == report["signature"] for existing in reports):
        return None

    reports.append(report)
    save_report_history(reports)
    st.session_state["report_history"] = reports
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
        created_at.strftime("%b %d, %Y %H:%M"),
        created_at.strftime("%Y/%m/%d %H:%M"),
    )

def latest_report():
    reports = get_report_history()
    return reports[-1] if reports else None

def dashboard_status_options(df):
    if "Status" not in df.columns:
        return []
    seen = [str(status) for status in df["Status"].dropna().unique().tolist()]
    ordered = [status for status in DASHBOARD_STATUS_ORDER if status in seen]
    extras = sorted([status for status in seen if status not in DASHBOARD_STATUS_ORDER])
    return ordered + extras

def dashboard_nutrient_options(df):
    if "Nutrient" not in df.columns:
        return []
    nutrients = [str(nutrient) for nutrient in df["Nutrient"].dropna().unique().tolist()]
    return sorted(nutrients, key=lambda value: nutrient_display_name(value))

def dashboard_signature(df):
    if df.empty:
        return ""
    signature_cols = [
        col for col in ["Nutrient", "Value", "Unit", "Low", "High", "Status"]
        if col in df.columns
    ]
    if not signature_cols:
        return ""
    stable_df = df[signature_cols].copy().sort_values(signature_cols).reset_index(drop=True)
    return stable_df.to_json(orient="records", force_ascii=False)

def record_dashboard_report(df):
    if df.empty or "Nutrient" not in df.columns or "Status" not in df.columns:
        return

    signature = dashboard_signature(df)
    if not signature:
        return

    if "dashboard_reports" not in st.session_state:
        st.session_state["dashboard_reports"] = []

    if st.session_state.get("dashboard_last_signature") == signature:
        return

    st.session_state["dashboard_reports"].append({
        "created_at": pd.Timestamp.now(),
        "results": df.copy(),
        "signature": signature,
    })
    st.session_state["dashboard_last_signature"] = signature

def dashboard_reports():
    reports = st.session_state.get("dashboard_reports", [])
    return [report for report in reports if isinstance(report.get("results"), pd.DataFrame)]

def dashboard_latest_results(df):
    reports = dashboard_reports()
    if reports:
        latest_df = reports[-1]["results"]
        if isinstance(latest_df, pd.DataFrame) and not latest_df.empty:
            return latest_df.copy()
    return df.copy()

def dashboard_days_since_last():
    reports = dashboard_reports()
    if not reports:
        return 0
    last_date = reports[-1].get("created_at", pd.Timestamp.now())
    try:
        delta = pd.Timestamp.now() - pd.Timestamp(last_date)
        return max(int(delta.days), 0)
    except Exception:
        return 0

def dashboard_abnormal_count(df):
    if "Status" not in df.columns:
        return 0
    return int(df["Status"].isin(["Deficient", "Excessive"]).sum())

def model_agreement_dashboard_value(df):
    if df.empty or "Model Agreement" not in df.columns:
        return tr("N/A", "غير متوفر"), ""

    agreement_series = df["Model Agreement"].astype(str)
    available = agreement_series[agreement_series.isin(["Agree", "Different"])]
    if available.empty:
        return tr("N/A", "غير متوفر"), ""

    agree_count = int((available == "Agree").sum())
    agreement_percent = round((agree_count / len(available)) * 100)
    card_class = "soft-green" if agreement_percent >= 90 else "soft-amber"
    return f"{agreement_percent}%", card_class

def dashboard_improvement_pct():
    reports = dashboard_reports()
    if len(reports) < 2:
        return 0

    previous_df = reports[-2]["results"]
    latest_df = reports[-1]["results"]
    previous_score = max(dashboard_abnormal_count(previous_df), 1)
    latest_score = dashboard_abnormal_count(latest_df)
    return round(((previous_score - latest_score) / previous_score) * 100)

def render_dashboard_styles():
    st.markdown("""
<style>
.vv-dashboard-page {
    direction: inherit;
}
.vv-dashboard-header {
    margin: 10px 0 24px;
}
.vv-dashboard-title {
    font-family: 'Plus Jakarta Sans','Cairo',sans-serif;
    font-size: 30px;
    font-weight: 800;
    line-height: 1.15;
    color: var(--text-main);
    margin: 0 0 6px;
}
.vv-dashboard-subtitle {
    color: var(--text-muted);
    font-size: 14px;
    font-weight: 500;
}
.vv-dashboard-metrics {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 14px;
    margin: 8px 0 24px;
}
.vv-dashboard-card {
    min-height: 110px;
    border: 1px solid #dfe7e5;
    border-radius: 12px;
    padding: 22px 22px;
    background: #ffffff;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}
.vv-dashboard-card.soft-green {
    background: #dff3ee;
    border-color: #dff3ee;
}
.vv-dashboard-card.soft-red {
    background: #fde9e9;
    border-color: #fde9e9;
}
.vv-dashboard-card.soft-amber {
    background: #fff3dd;
    border-color: #f3d49c;
}
.vv-dashboard-card.soft-blue {
    background: #e7f3ff;
    border-color: #c9def5;
}
.vv-dashboard-card-label {
    color: #6b7280;
    font-size: 13px;
    font-weight: 600;
}
.vv-dashboard-card-value {
    color: #062f2f;
    font-size: 30px;
    font-weight: 800;
    line-height: 1;
}
.vv-dashboard-panel-title {
    color: #111827;
    font-family: 'Plus Jakarta Sans','Cairo',sans-serif;
    font-size: 19px;
    font-weight: 800;
    margin: 2px 0 4px;
}
.vv-dashboard-panel-subtitle {
    color: #6b7280;
    font-size: 13px;
}
.vv-dashboard-results-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
    gap: 14px;
    margin: 14px 0 28px;
}
.vv-dashboard-result-card {
    min-height: 156px;
    background: #ffffff;
    border: 1px solid #dfe7e5;
    border-left: 6px solid #9ca3af;
    border-radius: 12px;
    padding: 16px 17px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}
.vv-dashboard-result-card.normal {
    background: #e8f5e9;
    border-color: #b7dfbd;
    border-left-color: #1DB954;
}
.vv-dashboard-result-card.deficient {
    background: #ffebee;
    border-color: #f4b8c0;
    border-left-color: #FF4B4B;
}
.vv-dashboard-result-card.excessive {
    background: #fff3e0;
    border-color: #f1c88d;
    border-left-color: #FFA500;
}
.vv-dashboard-result-card.invalid,
.vv-dashboard-result-card.unknown,
.vv-dashboard-result-card.error {
    background: #f4f7fb;
    border-color: #d8e0ea;
    border-left-color: #6b7280;
}
.vv-dashboard-status-pill {
    width: fit-content;
    border-radius: 999px;
    padding: 5px 10px;
    background: rgba(255,255,255,0.72);
    color: #111827;
    font-size: 12px;
    font-weight: 800;
}
.vv-dashboard-result-name {
    color: #111827;
    font-size: 17px;
    font-weight: 800;
    margin-top: 14px;
}
.vv-dashboard-result-value {
    color: #062f2f;
    font-size: 24px;
    font-weight: 800;
    line-height: 1.1;
    margin-top: 8px;
}
.vv-dashboard-result-range {
    color: #4b5563;
    font-size: 12px;
    font-weight: 600;
    margin-top: 8px;
}
.vv-tracking-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(245px, 1fr));
    gap: 14px;
    margin: 14px 0 26px;
}
.vv-tracking-card {
    min-height: 230px;
    border-radius: 12px;
    border: 1px solid #dfe7e5;
    border-left: 6px solid #9ca3af;
    background: #ffffff;
    padding: 17px 18px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}
.vv-tracking-card.normal {
    border-left-color: #1DB954;
}
.vv-tracking-card.deficient {
    border-left-color: #FF4B4B;
}
.vv-tracking-card.excessive {
    border-left-color: #FFA500;
}
.vv-tracking-card.invalid,
.vv-tracking-card.unknown,
.vv-tracking-card.error {
    border-left-color: #6b7280;
}
.vv-tracking-name {
    color: #111827;
    font-size: 18px;
    font-weight: 800;
}
.vv-tracking-value {
    color: #062f2f;
    font-size: 28px;
    font-weight: 800;
    line-height: 1.1;
    margin-top: 8px;
}
.vv-tracking-meta {
    color: #4b5563;
    font-size: 12.5px;
    font-weight: 600;
    line-height: 1.55;
    margin-top: 7px;
}
.vv-tracking-delta {
    width: fit-content;
    margin-top: 10px;
    border-radius: 999px;
    padding: 5px 10px;
    background: #eef6ff;
    color: #145089;
    font-size: 12px;
    font-weight: 800;
}
.vv-tracking-warning {
    margin-top: 9px;
    border-radius: 9px;
    padding: 8px 10px;
    background: #fff8e8;
    color: #7a4d0b;
    font-size: 12px;
    font-weight: 700;
}
.vv-sparkline {
    width: 100%;
    height: 52px;
    margin-top: 14px;
}
.vv-sparkline-empty {
    height: 52px;
    margin-top: 14px;
    border-radius: 10px;
    background: #f5f7fa;
    color: #6b7280;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    font-weight: 700;
}
.vv-dashboard-recommendations {
    background: #ffffff;
    border: 1px solid #dfe7e5;
    border-radius: 12px;
    padding: 22px 24px;
    margin: 18px 0 26px;
}
.vv-dashboard-recommendation-item {
    border-top: 1px solid #edf1f4;
    padding: 14px 0;
}
.vv-dashboard-recommendation-item:first-child {
    border-top: none;
    padding-top: 4px;
}
.vv-dashboard-recommendation-title {
    color: #111827;
    font-weight: 800;
    font-size: 14px;
    margin-bottom: 6px;
}
.vv-dashboard-recommendation-text {
    color: #4b5563;
    font-size: 13px;
    line-height: 1.65;
}
.vv-dashboard-disclaimer {
    margin-top: 10px;
    padding: 12px 14px;
    border-radius: 10px;
    background: #fff8e8;
    color: #7a4d0b;
    font-size: 12.5px;
    font-weight: 700;
}
.vv-dashboard-alert {
    margin-top: 20px;
    background: #fff3dd;
    border: 1px solid #f3d49c;
    border-radius: 10px;
    padding: 20px 24px;
    color: #8a5a16;
    font-size: 15px;
    line-height: 1.8;
}
.vv-dashboard-alert-title {
    color: #8a4b05;
    font-weight: 800;
    margin-bottom: 6px;
}
.vv-dashboard-empty {
    background: #ffffff;
    border: 1px solid #dfe7e5;
    border-radius: 12px;
    padding: 32px;
    color: #4b5563;
}
@media (max-width: 900px) {
    .vv-dashboard-metrics {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }
}
@media (max-width: 560px) {
    .vv-dashboard-metrics {
        grid-template-columns: 1fr;
    }
}
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

def render_dashboard_metric_cards_legacy(df):
    status_series = df["Status"].astype(str) if "Status" in df.columns else pd.Series(dtype=str)
    total_reports = max(len(dashboard_reports()), 1)
    attention_cases = int(status_series.isin(["Deficient", "Excessive"]).sum())
    tracked_nutrients = int(df["Nutrient"].dropna().nunique()) if "Nutrient" in df.columns else len(df)
    improvement = dashboard_improvement_pct()

    cards = [
        {
            "label": tr("Total Reports", "إجمالي التقارير"),
            "value": total_reports,
            "class": "",
        },
        {
            "label": tr("Attention Cases", "حالات تحتاج متابعة"),
            "value": attention_cases,
            "class": "soft-red" if attention_cases else "soft-green",
        },
        {
            "label": tr("Tracked Vitamins", "فيتامينات متابعة"),
            "value": tracked_nutrients,
            "class": "soft-green",
        },
        {
            "label": tr("Improvement", "تحسن"),
            "value": f"{improvement:+g}%",
            "class": "soft-green" if improvement >= 0 else "soft-red",
        },
    ]

    cards_html = ""
    for card in cards:
        cards_html += f"""
        <div class="vv-dashboard-card {card['class']}">
            <div class="vv-dashboard-card-label">{safe_html(card['label'])}</div>
            <div class="vv-dashboard-card-value">{safe_html(card['value'])}</div>
        </div>
        """

    st.html(f"""
<div class="vv-dashboard-metrics">
    {cards_html}
</div>
""")

def render_dashboard_metric_cards(df):
    status_series = df["Status"].astype(str) if "Status" in df.columns else pd.Series(dtype=str)
    total_reports = max(len(dashboard_reports()), 1)
    deficiencies_found = int((status_series == "Deficient").sum())
    normal_results = int((status_series == "Normal").sum())
    model_agreement_value, model_agreement_class = model_agreement_dashboard_value(df)
    reports = dashboard_reports()
    if reports:
        last_check = pd.Timestamp(reports[-1].get("created_at", pd.Timestamp.now()))
        last_check_label = tr(
            last_check.strftime("%b %d, %H:%M"),
            last_check.strftime("%d/%m %H:%M"),
        )
    else:
        last_check_label = tr("Current session", "الجلسة الحالية")

    cards = [
        {
            "label": tr("Total Reports", "إجمالي التقارير"),
            "value": total_reports,
            "class": "soft-blue",
        },
        {
            "label": tr("Deficiencies Found", "النواقص المكتشفة"),
            "value": deficiencies_found,
            "class": "soft-amber" if deficiencies_found else "soft-green",
        },
        {
            "label": tr("Normal Results", "النتائج الطبيعية"),
            "value": normal_results,
            "class": "soft-green",
        },
        {
            "label": tr("Model Agreement", "توافق الموديل"),
            "value": model_agreement_value,
            "class": model_agreement_class,
        },
        {
            "label": tr("Last Check", "آخر تحليل"),
            "value": last_check_label,
            "class": "",
        },
    ]

    cards_html = ""
    for card in cards:
        cards_html += f"""
        <div class="vv-dashboard-card {card['class']}">
            <div class="vv-dashboard-card-label">{safe_html(card['label'])}</div>
            <div class="vv-dashboard-card-value">{safe_html(card['value'])}</div>
        </div>
        """

    st.html(f"""
<div class="vv-dashboard-metrics">
    {cards_html}
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

def dashboard_range_text(row):
    low = row.get("Low", None)
    high = row.get("High", None)
    unit = row.get("Unit", "")
    if low is None or high is None or pd.isna(low) or pd.isna(high):
        return tr("Reference range unavailable", "النطاق المرجعي غير متاح")
    return tr(
        f"Normal range: {dashboard_number(low)}-{dashboard_number(high)} {unit}",
        f"النطاق الطبيعي: {dashboard_number(low)}-{dashboard_number(high)} {unit}",
    )

def render_dashboard_result_cards(df):
    if df.empty:
        return

    align = "right" if is_arabic else "left"
    dir_val = "rtl" if is_arabic else "ltr"
    cards_html = ""

    for _, row in df.iterrows():
        status = str(row.get("Status", "Unknown"))
        status_class = dashboard_status_class(status)
        nutrient = nutrient_display_name(str(row.get("Nutrient", "")))
        value_text = dashboard_number(row.get("Value", ""))
        unit = safe_html(row.get("Unit", ""))
        value_with_unit = f"{safe_html(value_text)} {unit}".strip()
        range_text = dashboard_range_text(row)
        ml_prediction = str(row.get("ML Prediction", MODEL_UNAVAILABLE))
        ml_confidence = str(row.get("ML Confidence", MODEL_UNAVAILABLE))
        agreement = str(row.get("Model Agreement", MODEL_UNAVAILABLE))
        ml_suffix = "" if ml_confidence == MODEL_UNAVAILABLE else f" ({ml_confidence})"
        model_text = tr(
            f"ML: {ml_prediction_text(ml_prediction)}{ml_suffix} | {model_agreement_text(agreement)}",
            f"الموديل: {ml_prediction_text(ml_prediction)}{ml_suffix} | {model_agreement_text(agreement)}",
        )

        cards_html += f"""
        <div class="vv-dashboard-result-card {status_class}" style="text-align:{align};">
            <div>
                <div class="vv-dashboard-status-pill">{safe_html(status_text(status))}</div>
                <div class="vv-dashboard-result-name">{safe_html(nutrient)}</div>
            </div>
            <div>
                <div class="vv-dashboard-result-value">{value_with_unit}</div>
                <div class="vv-dashboard-result-range">{safe_html(range_text)}</div>
                <div class="vv-dashboard-result-range">{safe_html(model_text)}</div>
            </div>
        </div>
        """

    section_title(tr("Latest Analysis Results", "نتائج آخر تحليل"), 22, "")
    st.html(f"""
<div style="direction:{dir_val};">
    <div class="vv-dashboard-panel-subtitle" style="text-align:{align}; margin-bottom:10px;">
        {safe_html(tr(
            "Each card shows the submitted value, status, and reference range.",
            "تعرض كل بطاقة القيمة المدخلة والحالة والنطاق الطبيعي."
        ))}
    </div>
    <div class="vv-dashboard-results-grid">
        {cards_html}
    </div>
</div>
""")

def render_dashboard_snapshot(df):
    if df.empty or "Status" not in df.columns:
        return

    abnormal_df = df[df["Status"].isin(["Deficient", "Excessive"])].copy()
    invalid_count = int(df["Status"].isin(["Invalid", "Unknown", "Error"]).sum())
    total = len(df)
    abnormal_count = len(abnormal_df)
    abnormal_percent = round((abnormal_count / total) * 100, 1) if total else 0

    if abnormal_count == 0:
        color = status_color("Normal")
        title = tr("Smart Snapshot", "الملخص الذكي")
        text = tr(
            "Your current valid results are within the normal range. Keep tracking future readings for a clearer trend.",
            "النتائج الصالحة الحالية ضمن النطاق الطبيعي. استمر في متابعة القراءات القادمة للحصول على صورة أوضح."
        )
    else:
        color = "#FFA500" if abnormal_percent < 50 else status_color("Deficient")
        attention_names = []
        if "Nutrient" in abnormal_df.columns:
            attention_names = [
                nutrient_display_name(nutrient)
                for nutrient in abnormal_df["Nutrient"].dropna().astype(str).unique().tolist()[:4]
            ]
        attention_text = ", ".join(attention_names)
        title = tr("Follow-up Suggested", "يوصى بالمتابعة")
        text = tr(
            f"{abnormal_count} result(s) need attention ({abnormal_percent:g}%): {attention_text}. Review these values with a healthcare professional if they persist.",
            f"{abnormal_count} نتيجة تحتاج متابعة ({abnormal_percent:g}%): {attention_text}. راجع هذه القيم مع مختص صحي إذا استمرت."
        )

    if invalid_count:
        text += tr(
            f" {invalid_count} input(s) could not be classified and may need correction.",
            f" توجد {invalid_count} مدخلات لم يتم تصنيفها وقد تحتاج إلى تصحيح."
        )

    if "Model Agreement" in df.columns:
        agreement_series = df["Model Agreement"].astype(str)
        available = agreement_series[agreement_series.isin(["Agree", "Different"])]
        if not available.empty:
            agree_count = int((available == "Agree").sum())
            text += tr(
                f" The ML model agreed with the reference-range status for {agree_count}/{len(available)} model-checked result(s).",
                f" توافق الموديل مع حالة النطاقات في {agree_count}/{len(available)} نتيجة تم فحصها بالموديل."
            )

    dir_val = "rtl" if is_arabic else "ltr"
    align = "right" if is_arabic else "left"

    st.html(f"""
<div class="vv-dashboard-alert" style="direction:{dir_val}; text-align:{align}; border-color:{color}55;">
    <div class="vv-dashboard-alert-title">{safe_html(title)}</div>
    <div>
        {safe_html(text)}
    </div>
</div>
""")

def apply_dashboard_plot_layout(fig, height=390):
    fig.update_layout(
        height=height,
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        font=dict(color="#4B5563", family="Plus Jakarta Sans, Cairo"),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#4B5563")),
        legend_title_text="",
        title=dict(font=dict(color="#111827", size=15)),
        margin=dict(l=20, r=20, t=55, b=45),
    )
    return fig

def dashboard_timeline_points(selected_nutrient, fallback_df):
    points = []
    reports = dashboard_reports()
    if not reports and not fallback_df.empty:
        reports = [{
            "created_at": pd.Timestamp.now(),
            "results": fallback_df,
        }]

    for index, report in enumerate(reports, start=1):
        report_df = report.get("results")
        if not isinstance(report_df, pd.DataFrame) or report_df.empty:
            continue
        nutrient_rows = report_df[
            report_df["Nutrient"].astype(str) == str(selected_nutrient)
        ].copy()
        if nutrient_rows.empty:
            continue

        row = nutrient_rows.iloc[-1]
        value = pd.to_numeric(row.get("Value"), errors="coerce")
        if pd.isna(value):
            continue

        created_at = pd.Timestamp(report.get("created_at", pd.Timestamp.now()))
        label = tr(
            created_at.strftime("%b %d, %H:%M"),
            created_at.strftime("%d/%m %H:%M"),
        )
        points.append({
            "label": label,
            "value": float(value),
            "status": row.get("Status", "Unknown"),
            "unit": row.get("Unit", ""),
            "reference_low": row.get("Low", None),
            "reference_high": row.get("High", None),
            "reading": index,
        })

    return points

def render_dashboard_timeline(df):
    nutrient_options = dashboard_nutrient_options(df)
    if not nutrient_options:
        st.info(tr(
            "Timeline will appear after nutrient data is available.",
            "سيظهر الرسم الزمني بعد توفر بيانات العناصر."
        ))
        return

    current_selection = st.session_state.get("dashboard_timeline_nutrient")
    if current_selection not in nutrient_options:
        st.session_state["dashboard_timeline_nutrient"] = nutrient_options[0]

    with st.container(border=True):
        if is_arabic:
            control_col, title_col = st.columns([1.05, 4])
        else:
            title_col, control_col = st.columns([4, 1.05])

        with title_col:
            align = "right" if is_arabic else "left"
            st.html(f"""
<div style="text-align:{align}; padding:6px 4px 0;">
    <div class="vv-dashboard-panel-title">{safe_html(tr("Values Over Time", "تطور القيم عبر الزمن"))}</div>
    <div class="vv-dashboard-panel-subtitle">{safe_html(tr(
        "Session readings",
        f"{max(len(dashboard_reports()), 1)} نقطة قياس"
    ))}</div>
</div>
""")

        with control_col:
            selected_nutrient = st.selectbox(
                tr("Nutrient", "العنصر"),
                nutrient_options,
                index=nutrient_options.index(st.session_state["dashboard_timeline_nutrient"]),
                format_func=nutrient_display_name,
                label_visibility="collapsed",
                key="dashboard_timeline_nutrient",
            )

        points = dashboard_timeline_points(selected_nutrient, df)
        if not points:
            st.info(tr(
                "No numeric readings are available for this nutrient.",
                "لا توجد قراءات رقمية متاحة لهذا العنصر."
            ))
            return

        values = [point["value"] for point in points]
        labels = [point["label"] for point in points]
        mode = "lines+markers" if len(points) > 1 else "markers+text"

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=labels,
            y=values,
            mode=mode,
            text=[f"{value:g}" for value in values] if len(points) == 1 else None,
            textposition="top center",
            line=dict(color="#1aa37a", width=3),
            marker=dict(
                size=10,
                color="#b87418",
                line=dict(color="#ffffff", width=2),
            ),
            hovertemplate="%{x}<br>%{y:g}<extra></extra>",
            name=nutrient_display_name(selected_nutrient),
        ))

        low_values = [
            pd.to_numeric(point["reference_low"], errors="coerce")
            for point in points
            if point.get("reference_low") is not None
        ]
        high_values = [
            pd.to_numeric(point["reference_high"], errors="coerce")
            for point in points
            if point.get("reference_high") is not None
        ]
        numeric_refs = [
            float(value) for value in low_values + high_values
            if not pd.isna(value)
        ]
        y_candidates = values + numeric_refs
        y_min = min(y_candidates) if y_candidates else 0
        y_max = max(y_candidates) if y_candidates else 1
        padding = max((y_max - y_min) * 0.25, 1)

        fig.update_layout(
            height=310,
            plot_bgcolor="#ffffff",
            paper_bgcolor="#ffffff",
            font=dict(color="#4B5563", family="Plus Jakarta Sans, Cairo"),
            margin=dict(l=34, r=22, t=18, b=38),
            xaxis=dict(
                showgrid=False,
                zeroline=False,
                tickfont=dict(color="#4B5563", size=11),
                linecolor="#6b7280",
            ),
            yaxis=dict(
                range=[max(y_min - padding, 0), y_max + padding],
                gridcolor="#e8ecef",
                griddash="dot",
                zeroline=False,
                tickfont=dict(color="#4B5563", size=11),
                linecolor="#6b7280",
            ),
            showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

def dashboard_chart_rows(df):
    chart_rows = []
    required_cols = {"Nutrient", "Value", "Low", "High", "Status", "Unit"}
    if df.empty or not required_cols.issubset(df.columns):
        return pd.DataFrame()

    for _, row in df.iterrows():
        value = pd.to_numeric(row.get("Value"), errors="coerce")
        low = pd.to_numeric(row.get("Low"), errors="coerce")
        high = pd.to_numeric(row.get("High"), errors="coerce")
        if pd.isna(value) or pd.isna(low) or pd.isna(high) or high <= low:
            continue

        position = ((float(value) - float(low)) / (float(high) - float(low))) * 100
        display_position = min(max(position, -35), 135)
        status = str(row.get("Status", "Unknown"))
        chart_rows.append({
            "Nutrient": nutrient_display_name(str(row.get("Nutrient", ""))),
            "Value": float(value),
            "Unit": str(row.get("Unit", "")),
            "Low": float(low),
            "High": float(high),
            "Status": status,
            "Status Text": status_text(status),
            "Position": display_position,
            "Actual Position": position,
            "Color": {
                "Normal": "#1DB954",
                "Deficient": "#FF4B4B",
                "Excessive": "#FFA500",
            }.get(status, "#6b7280"),
        })

    return pd.DataFrame(chart_rows)

def render_dashboard_range_chart(df):
    chart_df = dashboard_chart_rows(df)
    if chart_df.empty:
        st.info(tr(
            "The range chart will appear after numeric results with reference ranges are available.",
            "سيظهر مخطط النطاق بعد توفر نتائج رقمية مع نطاقات مرجعية."
        ))
        return

    align = "right" if is_arabic else "left"
    section_title(tr("Results vs Normal Range", "النتائج مقارنة بالنطاق الطبيعي"), 22, "")
    st.html(f"""
<div class="vv-dashboard-panel-subtitle" style="text-align:{align}; margin-bottom:8px;">
    {safe_html(tr(
        "The green band marks the normal range. Values left of it are low; values right of it are high.",
        "يوضح الشريط الأخضر النطاق الطبيعي. القيم على اليسار منخفضة، والقيم على اليمين مرتفعة."
    ))}
</div>
""")

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=chart_df["Position"],
        y=chart_df["Nutrient"],
        orientation="h",
        marker_color=chart_df["Color"],
        text=[
            f"{value:g} {unit} | {status}"
            for value, unit, status in zip(chart_df["Value"], chart_df["Unit"], chart_df["Status Text"])
        ],
        textposition="auto",
        customdata=[
            [f"{row['Value']:g} {row['Unit']}", f"{row['Low']:g}-{row['High']:g} {row['Unit']}", f"{row['Actual Position']:.1f}%"]
            for _, row in chart_df.iterrows()
        ],
        hovertemplate="<b>%{y}</b><br>%{customdata[0]}<br>%{customdata[1]}<br>%{customdata[2]}<extra></extra>",
    ))
    fig.add_vrect(x0=0, x1=100, fillcolor="rgba(29,185,84,0.08)", line_width=0, layer="below")
    fig.add_vline(x=0, line_color="#1DB954", line_dash="dot", line_width=1)
    fig.add_vline(x=100, line_color="#1DB954", line_dash="dot", line_width=1)
    fig.update_layout(
        height=max(340, 42 * len(chart_df) + 120),
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        font=dict(color="#4B5563", family="Plus Jakarta Sans, Cairo"),
        margin=dict(l=24, r=24, t=18, b=42),
        xaxis=dict(
            range=[-40, 140],
            title=tr("Position inside normal range (%)", "الموضع داخل النطاق الطبيعي (%)"),
            gridcolor="#e8ecef",
            zeroline=False,
        ),
        yaxis=dict(autorange="reversed"),
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

def dashboard_recommendation_items(row):
    recommendations = str(row.get("Recommendations", "")).strip()
    if recommendations:
        return [item.strip() for item in recommendations.split(";") if item.strip()]
    return get_recommendations(str(row.get("Status", "Unknown")))

def render_dashboard_recommendations(df):
    if df.empty or "Status" not in df.columns:
        return

    focus_statuses = ["Deficient", "Excessive", "Invalid", "Unknown", "Error"]
    focus_df = df[df["Status"].astype(str).isin(focus_statuses)].copy()
    normal_count = int((df["Status"].astype(str) == "Normal").sum())
    align = "right" if is_arabic else "left"
    dir_val = "rtl" if is_arabic else "ltr"
    items_html = ""

    if focus_df.empty:
        items_html = f"""
        <div class="vv-dashboard-recommendation-item">
            <div class="vv-dashboard-recommendation-title">{safe_html(tr("All Current Results Are Normal", "كل النتائج الحالية طبيعية"))}</div>
            <div class="vv-dashboard-recommendation-text">
                {safe_html(tr(
                    "Maintain healthy habits and keep tracking future lab results for a clearer long-term pattern.",
                    "حافظ على العادات الصحية واستمر في متابعة التحاليل القادمة للحصول على صورة أوضح على المدى الطويل."
                ))}
            </div>
        </div>
        """
    else:
        for _, row in focus_df.iterrows():
            nutrient = nutrient_display_name(str(row.get("Nutrient", "")))
            status = str(row.get("Status", "Unknown"))
            rec_text = " ".join(dashboard_recommendation_items(row))
            items_html += f"""
            <div class="vv-dashboard-recommendation-item">
                <div class="vv-dashboard-recommendation-title">{safe_html(nutrient)} - {safe_html(status_text(status))}</div>
                <div class="vv-dashboard-recommendation-text">{safe_html(rec_text)}</div>
            </div>
            """

        if normal_count:
            items_html += f"""
            <div class="vv-dashboard-recommendation-item">
                <div class="vv-dashboard-recommendation-title">{safe_html(tr("Normal Results", "النتائج الطبيعية"))}</div>
                <div class="vv-dashboard-recommendation-text">
                    {safe_html(tr(
                        f"{normal_count} result(s) are within the normal range.",
                        f"{normal_count} نتيجة ضمن النطاق الطبيعي."
                    ))}
                </div>
            </div>
            """

    section_title(tr("Recommendations", "التوصيات"), 22, "")
    st.html(f"""
<div class="vv-dashboard-recommendations" style="direction:{dir_val}; text-align:{align};">
    {items_html}
    <div class="vv-dashboard-disclaimer">
        {safe_html(tr(
            "These are general recommendations and do not replace medical advice from a qualified healthcare professional.",
            "هذه توصيات عامة ولا تغني عن استشارة مختص صحي مؤهل."
        ))}
    </div>
</div>
""")

def render_dashboard_charts(df):
    render_dashboard_range_chart(df)

def render_dashboard_filters_table(df, key_prefix="dashboard"):
    status_options = dashboard_status_options(df)
    nutrient_options = dashboard_nutrient_options(df)

    if not status_options or not nutrient_options:
        st.info(tr(
            "Filters will appear after results include both status and nutrient data.",
            "ستظهر الفلاتر بعد توفر بيانات الحالة والعنصر في النتائج."
        ))
        return

    filter_col1, filter_col2 = st.columns(2)
    with filter_col1:
        selected_status = st.multiselect(
            tr("Filter by Status", "فلترة حسب الحالة"),
            options=status_options,
            default=status_options,
            format_func=status_text,
            key=f"{key_prefix}_status_filter",
        )
    with filter_col2:
        selected_nutrients = st.multiselect(
            tr("Filter by Nutrient", "فلترة حسب العنصر"),
            options=nutrient_options,
            default=nutrient_options,
            format_func=nutrient_display_name,
            key=f"{key_prefix}_nutrient_filter",
        )

    if selected_status and selected_nutrients:
        filtered_df = df[
            (df["Status"].astype(str).isin(selected_status)) &
            (df["Nutrient"].astype(str).isin(selected_nutrients))
        ].copy()
    else:
        filtered_df = df.iloc[0:0].copy()

    section_title(tr("Filtered Results", "النتائج بعد الفلترة"), 22, "")
    if filtered_df.empty:
        st.info(tr(
            "No results match the selected filters.",
            "لا توجد نتائج تطابق الفلاتر المحددة."
        ))
    else:
        render_results_table(filtered_df)

def report_option_label(report):
    counts = report.get("summary", {})
    return tr(
        f"{report_display_date(report)} | {report.get('source', 'Report')} | {counts.get('total', 0)} item(s) | {report_overall_status_text(report.get('overall_status', ''))}",
        f"{report_display_date(report)} | {report.get('source', 'تقرير')} | {counts.get('total', 0)} عنصر | {report_overall_status_text(report.get('overall_status', ''))}",
    )

def selected_report_from_history(reports):
    report_ids = [report["report_id"] for report in reports]
    if st.session_state.get("selected_report_id") not in report_ids:
        st.session_state["selected_report_id"] = reports[-1]["report_id"]

    newest_first = list(reversed(reports))
    selected_id = st.selectbox(
        tr("Select report", "اختر التقرير"),
        options=[report["report_id"] for report in newest_first],
        index=[report["report_id"] for report in newest_first].index(st.session_state["selected_report_id"]),
        format_func=lambda report_id: report_option_label(
            next(report for report in reports if report["report_id"] == report_id)
        ),
        key="selected_report_id",
    )
    return next(report for report in reports if report["report_id"] == selected_id)

def render_latest_report_summary_legacy(report):
    counts = report.get("summary", {})
    follow_up = counts.get("deficient", 0) + counts.get("excessive", 0) + counts.get("invalid", 0)
    report_df = report_to_df(report)
    model_agreement_value, model_agreement_class = model_agreement_dashboard_value(report_df)
    cards = [
        {
            "label": tr("Latest Report", "آخر تقرير"),
            "value": report_display_date(report),
            "class": "soft-blue",
        },
        {
            "label": tr("Needs Follow-up", "تحتاج متابعة"),
            "value": follow_up,
            "class": "soft-amber" if follow_up else "soft-green",
        },
        {
            "label": tr("Normal Results", "النتائج الطبيعية"),
            "value": counts.get("normal", 0),
            "class": "soft-green",
        },
        {
            "label": tr("Model Agreement", "توافق الموديل"),
            "value": model_agreement_value,
            "class": model_agreement_class,
        },
        {
            "label": tr("Overall Status", "الحالة العامة"),
            "value": report_overall_status_text(report.get("overall_status", "")),
            "class": "soft-red" if report.get("overall_status") == "Needs Review" else "",
        },
    ]

    cards_html = ""
    for card in cards:
        cards_html += f"""
        <div class="vv-dashboard-card {card['class']}">
            <div class="vv-dashboard-card-label">{safe_html(card['label'])}</div>
            <div class="vv-dashboard-card-value" style="font-size:24px;">{safe_html(card['value'])}</div>
        </div>
        """

    st.html(f"""
<div class="vv-dashboard-metrics">
    {cards_html}
</div>
""")

def render_latest_report_summary(report, reports):
    counts = report.get("summary", {})
    follow_up = counts.get("deficient", 0) + counts.get("excessive", 0) + counts.get("invalid", 0)
    tracked_nutrients = len(nutrient_names_from_reports(reports))
    latest_df = report_to_df(report)
    model_agreement_value, model_agreement_class = model_agreement_dashboard_value(latest_df)
    cards = [
        {
            "label": tr("Total Reports", "إجمالي التقارير"),
            "value": len(reports),
            "class": "soft-blue",
        },
        {
            "label": tr("Latest Report", "آخر تقرير"),
            "value": report_display_date(report),
            "class": "",
        },
        {
            "label": tr("Tracked Nutrients", "العناصر المتابعة"),
            "value": tracked_nutrients,
            "class": "soft-green",
        },
        {
            "label": tr("Model Agreement", "توافق الموديل"),
            "value": model_agreement_value,
            "class": model_agreement_class,
        },
        {
            "label": tr("Needs Follow-up", "تحتاج متابعة"),
            "value": follow_up,
            "class": "soft-amber" if follow_up else "soft-green",
        },
    ]

    cards_html = ""
    for card in cards:
        cards_html += f"""
        <div class="vv-dashboard-card {card['class']}">
            <div class="vv-dashboard-card-label">{safe_html(card['label'])}</div>
            <div class="vv-dashboard-card-value" style="font-size:24px;">{safe_html(card['value'])}</div>
        </div>
        """

    st.html(f"""
<div class="vv-dashboard-metrics">
    {cards_html}
</div>
""")

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
            tr("Invalid", "غير صالح"): counts.get("invalid", 0),
            tr("Status", "الحالة"): report_overall_status_text(report.get("overall_status", "")),
        })

    section_title(tr("Report History", "سجل التقارير"), 22, "")
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
        <line x1="8" y1="{height - 8}" x2="{width - 8}" y2="{height - 8}" stroke="#e5e7eb" stroke-width="1" />
        <polyline fill="none" stroke="{color}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" points="{' '.join(points)}" />
        {''.join(circles)}
    </svg>
    """

def render_vitamin_tracking_cards(reports):
    nutrient_names = nutrient_names_from_reports(reports)
    if not nutrient_names:
        st.info(tr(
            "Add a report to start tracking nutrients over time.",
            "أضف تقريرًا للبدء في متابعة العناصر عبر الزمن."
        ))
        return None

    section_title(tr("Vitamin Tracking", "متابعة الفيتامينات والمعادن"), 22, "")

    selected = st.selectbox(
        tr("Choose nutrient for timeline", "اختر العنصر لعرض الخط الزمني"),
        options=nutrient_names,
        index=0,
        format_func=nutrient_display_name,
        key="tracking_selected_nutrient",
    )

    align = "right" if is_arabic else "left"
    dir_val = "rtl" if is_arabic else "ltr"
    cards_html = ""

    for nutrient in nutrient_names:
        readings = nutrient_readings_from_reports(reports, nutrient)
        latest = latest_nutrient_reading(readings)
        valid_readings = valid_nutrient_readings(readings)
        status = latest.get("status", "Unknown") if latest else "Unknown"
        status_class = dashboard_status_class(status)
        status_label = status_text(status)
        color = status_color(status)
        value = latest.get("value") if latest else None
        raw_value = latest.get("raw_value") if latest else ""
        unit = latest.get("unit", "") if latest else ""
        value_label = f"{dashboard_number(value if value is not None else raw_value)} {safe_html(unit)}".strip()
        invalid_count = len([reading for reading in readings if not reading.get("valid")])
        invalid_note = ""
        if invalid_count:
            invalid_note = f"""
            <div class="vv-tracking-warning">
                {safe_html(tr(
                    f"{invalid_count} invalid reading(s) excluded from trend.",
                    f"تم استبعاد {invalid_count} قراءة غير صالحة من التتبع."
                ))}
            </div>
            """

        cards_html += f"""
        <div class="vv-tracking-card {status_class}" style="text-align:{align};">
            <div>
                <div class="vv-dashboard-status-pill">{safe_html(status_label)}</div>
                <div class="vv-tracking-name">{safe_html(nutrient_display_name(nutrient))}</div>
                <div class="vv-tracking-value">{value_label}</div>
                <div class="vv-tracking-meta">{safe_html(nutrient_range_label(latest))}</div>
                <div class="vv-tracking-delta">{safe_html(nutrient_delta_text(valid_readings))}</div>
                {invalid_note}
            </div>
            {sparkline_svg(valid_readings, color)}
        </div>
        """

    st.html(f"""
<div style="direction:{dir_val};">
    <div class="vv-tracking-grid">
        {cards_html}
    </div>
</div>
""")
    return selected

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

    if len(valid_readings) < 2:
        st.info(tr(
            "This nutrient needs at least two valid readings to show a timeline.",
            "هذا العنصر يحتاج قراءتين صالحتين على الأقل لعرض الخط الزمني."
        ))
        return

    trend_df = pd.DataFrame(valid_readings)
    marker_colors = [status_color(status) for status in trend_df["status"]]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=trend_df["date"],
        y=trend_df["value"],
        mode="lines+markers+text",
        text=[f"{value:g}" for value in trend_df["value"]],
        textposition="top center",
        line=dict(color="#00BFFF", width=3),
        marker=dict(size=12, color=marker_colors, line=dict(color="#ffffff", width=2)),
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

    fig.update_layout(
        height=400,
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        font=dict(color="#4B5563", family="Plus Jakarta Sans, Cairo"),
        margin=dict(l=24, r=24, t=24, b=48),
        xaxis=dict(showgrid=False),
        yaxis=dict(gridcolor="#e8ecef", title=trend_df["unit"].iloc[-1]),
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

def render_report_trends(reports, selected_report):
    nutrient_names = sorted({
        str(result.get("Nutrient", ""))
        for report in reports
        for result in report.get("results", [])
        if result.get("Nutrient")
    }, key=nutrient_display_name)

    if not nutrient_names:
        return

    selected_df = report_to_df(selected_report)
    preferred = None
    if "Nutrient" in selected_df.columns and not selected_df.empty:
        preferred = str(selected_df.iloc[0].get("Nutrient", ""))
    if preferred not in nutrient_names:
        preferred = nutrient_names[0]

    section_title(tr("Trends", "تطور التحاليل"), 22, "")
    selected_nutrient = st.selectbox(
        tr("Track nutrient over reports", "تابع العنصر عبر التقارير"),
        options=nutrient_names,
        index=nutrient_names.index(preferred),
        format_func=nutrient_display_name,
        key="report_trend_nutrient",
    )

    points = []
    skipped_invalid = 0
    for report in reports:
        for result in report.get("results", []):
            if str(result.get("Nutrient", "")) != selected_nutrient:
                continue
            status = str(result.get("Status", "Unknown"))
            value = pd.to_numeric(result.get("Value"), errors="coerce")
            if status in ["Invalid", "Unknown", "Error"] or pd.isna(value):
                skipped_invalid += 1
                continue
            points.append({
                "Date": report_display_date(report),
                "Value": float(value),
                "Status": status_text(status),
                "Unit": result.get("Unit", ""),
                "Low": pd.to_numeric(result.get("Low"), errors="coerce"),
                "High": pd.to_numeric(result.get("High"), errors="coerce"),
            })

    if skipped_invalid:
        st.warning(tr(
            f"{skipped_invalid} invalid reading(s) were excluded from the trend chart.",
            f"تم استبعاد {skipped_invalid} قراءة غير صالحة من مخطط التطور."
        ))

    if len(points) < 2:
        st.info(tr(
            "Add at least two valid reports for this nutrient to see a trend.",
            "أضف تقريرين صالحين على الأقل لهذا العنصر لعرض التطور."
        ))
        return

    trend_df = pd.DataFrame(points)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=trend_df["Date"],
        y=trend_df["Value"],
        mode="lines+markers+text",
        text=[f"{value:g}" for value in trend_df["Value"]],
        textposition="top center",
        line=dict(color="#00BFFF", width=3),
        marker=dict(size=10, color="#1DB954", line=dict(color="#ffffff", width=2)),
        hovertemplate="%{x}<br>%{y:g}<extra></extra>",
    ))

    low_values = trend_df["Low"].dropna()
    high_values = trend_df["High"].dropna()
    if not low_values.empty and not high_values.empty:
        low = float(low_values.iloc[-1])
        high = float(high_values.iloc[-1])
        fig.add_hrect(y0=low, y1=high, fillcolor="rgba(29,185,84,0.10)", line_width=0, layer="below")
        fig.add_hline(y=low, line_color="#1DB954", line_dash="dot")
        fig.add_hline(y=high, line_color="#1DB954", line_dash="dot")

    fig.update_layout(
        height=360,
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        font=dict(color="#4B5563", family="Plus Jakarta Sans, Cairo"),
        margin=dict(l=24, r=24, t=24, b=44),
        xaxis=dict(showgrid=False),
        yaxis=dict(gridcolor="#e8ecef", title=trend_df["Unit"].iloc[-1]),
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

def render_report_dashboard_legacy(reports):
    latest = reports[-1]
    render_latest_report_summary_legacy(latest)
    render_report_history_table(reports)

    selected_report = selected_report_from_history(reports)
    selected_df = report_to_df(selected_report)

    section_title(tr("Selected Report", "التقرير المحدد"), 22, "")
    st.caption(report_option_label(selected_report))
    render_report_actions(selected_report, selected_df)

    if selected_df.empty:
        st.info(tr("This report has no saved results.", "هذا التقرير لا يحتوي على نتائج محفوظة."))
        return

    render_dashboard_result_cards(selected_df)
    render_report_trends(reports, selected_report)
    render_dashboard_recommendations(selected_df)
    render_dashboard_snapshot(selected_df)

def render_report_dashboard(reports):
    latest = reports[-1]
    latest_df = report_to_df(latest)

    render_latest_report_summary(latest, reports)
    selected_nutrient = render_vitamin_tracking_cards(reports)
    render_selected_nutrient_timeline(reports, selected_nutrient)

    section_title(tr("Latest Report Details", "تفاصيل آخر تقرير"), 22, "")
    st.caption(report_option_label(latest))
    render_report_actions(latest, latest_df, key_prefix="latest")

    if latest_df.empty:
        st.info(tr("This report has no saved results.", "هذا التقرير لا يحتوي على نتائج محفوظة."))
        render_report_history_table(reports)
        return

    render_dashboard_result_cards(latest_df)
    render_dashboard_charts(latest_df)
    render_dashboard_filters_table(latest_df, key_prefix="latest_dashboard")
    render_dashboard_recommendations(latest_df)
    render_dashboard_snapshot(latest_df)

    render_report_history_table(reports)
    selected_report = selected_report_from_history(reports)
    selected_df = report_to_df(selected_report)
    section_title(tr("Selected Report Review", "مراجعة التقرير المحدد"), 22, "")
    st.caption(report_option_label(selected_report))
    render_report_actions(selected_report, selected_df, key_prefix="selected")

    if selected_report.get("report_id") != latest.get("report_id"):
        if selected_df.empty:
            st.info(tr("This report has no saved results.", "هذا التقرير لا يحتوي على نتائج محفوظة."))
        else:
            render_dashboard_result_cards(selected_df)
            render_dashboard_charts(selected_df)
            render_dashboard_filters_table(selected_df, key_prefix="selected_dashboard")
            render_dashboard_recommendations(selected_df)
            render_dashboard_snapshot(selected_df)

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
with home_tab:
    render_header()

    section_title(tr("Input Method", "طريقة الإدخال"), icon="")

    input_mode = st.radio(
        "",
        [tr("Manual Input", "إدخال يدوي"), tr("Upload CSV", "رفع CSV")],
        label_visibility="collapsed",
        horizontal=True,
    )

    manual_label = tr("Manual Input", "إدخال يدوي")
    csv_label    = tr("Upload CSV",   "رفع CSV")

    # ── Manual input ──────────────────────────
    if input_mode == manual_label:
        section_title(tr("Enter Lab Values", "أدخل قيم التحليل"), 22, "")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            age = st.number_input(tr("Age", "العمر"), min_value=0, max_value=120, value=25, step=1)
        with col2:
            gender_text = st.selectbox(tr("Gender", "الجنس"), [tr("Male", "ذكر"), tr("Female", "أنثى")])
        with col3:
            nutrient = st.selectbox(tr("Nutrient", "العنصر"), list(REFERENCE_RANGES.keys()) + ["Ferritin"])
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
    else:
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

    # ── Results ────────────────────────────────
    results_df = st.session_state["results_df"]

    if not results_df.empty:
        section_title(tr("Results Summary", "ملخص النتائج"), 26, "")
        render_summary_stats(results_df)

        section_title(tr("Results Table", "جدول النتائج"), 22, "")
        render_results_table(results_df)

        section_title(tr("Smart Result Cards", "بطاقات النتائج الذكية"), 22, "")
        for _, row in results_df.iterrows():
            render_result_card(row)

        # ── Visualizations ────────────────────
        section_title(tr("Visualizations", "الرسوم البيانية"), 26, "")

        valid_results = results_df[
            results_df["Status"].isin(["Deficient", "Normal", "Excessive"])
        ].copy()

        if not valid_results.empty:
            color_map = {"Deficient": "#FF4B4B", "Normal": "#1DB954", "Excessive": "#FFA500"}

            

            section_title(tr("Status Distribution", "توزيع الحالات"), 20)

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

            section_title(tr("Reference Range Visualization", "مقارنة القيمة بالنطاق الطبيعي"), 20)

        for i, row in valid_results.reset_index(drop=True).iterrows():
            fig_ref = create_reference_chart(row)
            if fig_ref is not None:
                st.plotly_chart(
                    fig_ref,
                    use_container_width=True,
                    config={
                        "displayModeBar": False,
                        "scrollZoom": False,
                        "doubleClick": False,
                        "staticPlot": True
                    },
                    key=f"ref_chart_{i}"
                )

        # Invalid warnings
        invalid_results = results_df[results_df["Status"] == "Invalid"].copy()
        if not invalid_results.empty:
            section_title(tr("Input Warnings", "تنبيهات الإدخال"), 22, "⚠️")
            for _, row in invalid_results.iterrows():
                st.error(tr(
                    f"{row['Nutrient']} value ({row['Value']}) looks unrealistic. Please check the input.",
                    f"قيمة {row['Nutrient']} ({row['Value']}) تبدو غير منطقية. يرجى التأكد من المدخلات."
                ))

        # Download
        section_title(tr("Download Results", "تحميل النتائج"), 22, "")
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
with dashboard_tab:
    render_dashboard_styles()

    results_df = st.session_state.get("results_df", pd.DataFrame())
    if not results_df.empty:
        save_analysis_report(results_df, tr("Current Session", "الجلسة الحالية"))
    reports = get_report_history()
    dir_val = "rtl" if is_arabic else "ltr"
    align = "right" if is_arabic else "left"

    render_dashboard_header()

    if not reports:
        st.html(f"""
<div class="vv-dashboard-empty" style="direction:{dir_val}; text-align:{align};">
    <div class="vv-dashboard-panel-title">{safe_html(tr("No Analysis Results Yet", "لا توجد نتائج تحليل بعد"))}</div>
    <div class="vv-dashboard-panel-subtitle">
        {safe_html(tr(
            "Enter lab values manually or upload a CSV file from the Home tab, then run the analysis to unlock the dashboard.",
            "أدخل قيم التحاليل يدويًا أو ارفع ملف CSV من تبويب الرئيسية، ثم شغل التحليل لتظهر لوحة التحكم."
        ))}
    </div>
</div>
""")
    else:
        render_report_dashboard(reports)

# =========================================
# ABOUT TAB
# =========================================
with about_tab:
    render_header()
    dir_val = "rtl" if is_arabic else "ltr"
    align   = "right" if is_arabic else "left"

    cards = [
        {
            "icon": "",
            "title": tr("About VitaVision", "عن VitaVision"),
            "text": tr(
                "VitaVision is an intelligent decision-support system designed to simplify the interpretation of vitamin and mineral laboratory results. It transforms raw lab values into meaningful health insights, helping users quickly understand whether their levels fall within a healthy range.",
                "VitaVision هو نظام ذكي لدعم اتخاذ القرار مصمم لتبسيط تفسير نتائج تحاليل الفيتامينات والمعادن، حيث يحول القيم المخبرية إلى معلومات صحية مفهومة تساعد المستخدم على معرفة حالته بسهولة."
            ),
            "items": [
                tr("Provides instant classification of lab results", "تصنيف فوري لنتائج التحاليل"),
                tr("Uses scientifically defined reference ranges", "يعتمد على نطاقات مرجعية علمية"),
                tr("Offers simplified explanations for better understanding", "يقدم شرح مبسط لفهم أفضل"),
                tr("Designed as an educational and supportive tool", "مصمم كأداة تعليمية داعمة"),
            ],
        },
        {
            "icon": "",
            "title": tr("Project Scope", "نطاق المشروع"),
            "text": tr(
                "The VitaVision system focuses on analyzing vitamin and mineral lab results by classifying them into Deficient, Normal, or Excessive categories. It enhances user understanding by providing contextual explanations, possible causes, and actionable recommendations.",
                "يركز نظام VitaVision على تحليل نتائج الفيتامينات والمعادن وتصنيفها إلى ناقص أو طبيعي أو مرتفع، مع تقديم تفسير واضح وأسباب محتملة وتوصيات عملية تساعد المستخدم."
            ),
            "items": [
                tr("Supports multiple nutrients and lab indicators", "يدعم عدة عناصر غذائية وتحاليل"),
                tr("Provides visual comparison with reference ranges", "يعرض مقارنة بصرية مع النطاق الطبيعي"),
                tr("Includes both manual input and CSV upload", "يدعم الإدخال اليدوي ورفع CSV"),
                tr("Helps users make informed health decisions", "يساعد المستخدم على اتخاذ قرارات صحية واعية"),
            ],
        },
        {
            "icon": "",
            "title": tr("Alignment with Saudi Vision 2030", "التوافق مع رؤية السعودية 2030"),
            "text": tr(
                "VitaVision supports Saudi Vision 2030 by promoting digital transformation in the healthcare sector. It enhances health awareness, empowers individuals to better understand their medical data, and contributes to improving the overall quality of life through smart health solutions.",
                "يدعم مشروع VitaVision رؤية السعودية 2030 من خلال تعزيز التحول الرقمي في القطاع الصحي، ورفع الوعي الصحي، وتمكين الأفراد من فهم بياناتهم الطبية بشكل أفضل، والمساهمة في تحسين جودة الحياة عبر حلول صحية ذكية."
            ),
            "items": [
                tr("Supports digital health transformation", "يدعم التحول الرقمي الصحي"),
                tr("Enhances health awareness in society", "يعزز الوعي الصحي في المجتمع"),
                tr("Empowers individuals with health insights", "يمكن الأفراد من فهم حالتهم الصحية"),
                tr("Contributes to improving quality of life", "يساهم في تحسين جودة الحياة"),
            ],
        },
        {
            "icon": "",
            "title": tr("How It Works", "كيف يعمل النظام"),
            "text": tr(
                "The system analyzes each nutrient value by comparing it against medically defined reference ranges. It then classifies the result and enhances it using intelligent logic to generate explanations, possible causes, and recommendations.",
                "يقوم النظام بتحليل كل قيمة غذائية بمقارنتها مع النطاقات المرجعية الطبية، ثم يصنف النتيجة ويضيف شرحًا ذكيًا مع الأسباب المحتملة والتوصيات."
            ),
            "items": [
                tr("Input → Processing → Classification", "إدخال ← معالجة ← تصنيف"),
                tr("Rule-based + Intelligent logic", "يعتمد على قواعد + منطق ذكي"),
                tr("Generates explanations and recommendations", "يولد شرح وتوصيات"),
            ],
        },
    ]

    for card in cards:
        items_html = "".join(f"<li>{it}</li>" for it in card["items"])
        st.html(f"""
<div class="vv-card" style="direction:{dir_val}; text-align:{align};">
    <div class="vv-card-title">
        <span style="margin-{'left' if not is_arabic else 'right'}:8px;">{card['icon']}</span>{card['title']}
    </div>
    <div class="vv-card-text">{card['text']}</div>
    <ul class="vv-card-list">{items_html}</ul>
</div>
""")

    # Disclaimer banner
    st.html(f"""
<div class="disclaimer-banner" style="direction:{dir_val};">
    <span class="disclaimer-icon"></span>
    <div>
        <div class="disclaimer-title">{tr("Medical Disclaimer", "تنبيه طبي")}</div>
        <div class="disclaimer-text" style="text-align:{align};">
            {tr(
                "This result is not a medical diagnosis. Please consult a healthcare professional before making any medical decision.",
                "هذه النتيجة ليست تشخيصًا طبيًا. يرجى استشارة مختص صحي قبل اتخاذ أي قرار طبي."
            )}
        </div>
    </div>
</div>
""")

# =========================================
# CONTACT TAB
# =========================================
with contact_tab:
    render_header()
    dir_val = "rtl" if is_arabic else "ltr"
    align   = "right" if is_arabic else "left"

    st.html(f"""
<div class="vv-card" style="direction:{dir_val}; text-align:{align};">
    <div class="vv-card-title">  {tr("Contact Us", "تواصل معنا")}</div>
    <div class="vv-card-text" style="margin-bottom:20px;">
        {tr(
            "For any inquiries or feedback, feel free to reach out through the following channels:",
            "لأي استفسار أو ملاحظات، تواصل معنا عبر القنوات التالية:"
        )}
    </div>

    <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(220px,1fr)); gap:14px;">

        <a href="mailto:your@email.com" style="text-decoration:none;">
            <div style="background:rgba(0,191,255,0.05); border:1px solid rgba(0,191,255,0.18);
                        border-radius:12px; padding:16px 18px; transition:all 0.2s;
                        display:flex; align-items:center; gap:12px;"
                 onmouseover="this.style.borderColor='rgba(0,191,255,0.50)';this.style.background='rgba(0,191,255,0.10)'"
                 onmouseout="this.style.borderColor='rgba(0,191,255,0.18)';this.style.background='rgba(0,191,255,0.05)'">
                <span style="font-size:22px;">📧</span>
                <div>
                    <div style="font-size:11px; color:#7A9BB5; text-transform:uppercase; letter-spacing:0.5px;">Email</div>
                    <div style="font-size:14px; font-weight:600; color:#B8C8D8;">your@email.com</div>
                </div>
            </div>
        </a>

        <a href="https://linkedin.com/in/yourname" target="_blank" style="text-decoration:none;">
            <div style="background:rgba(0,119,181,0.07); border:1px solid rgba(0,119,181,0.25);
                        border-radius:12px; padding:16px 18px; transition:all 0.2s;
                        display:flex; align-items:center; gap:12px;"
                 onmouseover="this.style.borderColor='rgba(0,119,181,0.55)';this.style.background='rgba(0,119,181,0.14)'"
                 onmouseout="this.style.borderColor='rgba(0,119,181,0.25)';this.style.background='rgba(0,119,181,0.07)'">
                <span style="font-size:22px;">🔗</span>
                <div>
                    <div style="font-size:11px; color:#7A9BB5; text-transform:uppercase; letter-spacing:0.5px;">LinkedIn</div>
                    <div style="font-size:14px; font-weight:600; color:#B8C8D8;">linkedin.com/in/yourname</div>
                </div>
            </div>
        </a>

        <a href="https://github.com/yourname" target="_blank" style="text-decoration:none;">
            <div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.12);
                        border-radius:12px; padding:16px 18px; transition:all 0.2s;
                        display:flex; align-items:center; gap:12px;"
                 onmouseover="this.style.borderColor='rgba(255,255,255,0.30)';this.style.background='rgba(255,255,255,0.07)'"
                 onmouseout="this.style.borderColor='rgba(255,255,255,0.12)';this.style.background='rgba(255,255,255,0.03)'">
                <span style="font-size:22px;">💻</span>
                <div>
                    <div style="font-size:11px; color:#7A9BB5; text-transform:uppercase; letter-spacing:0.5px;">GitHub</div>
                    <div style="font-size:14px; font-weight:600; color:#B8C8D8;">github.com/yourname</div>
                </div>
            </div>
        </a>

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
