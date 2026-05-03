import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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
home_tab, about_tab, contact_tab = st.tabs([
    tr("Home", " الرئيسية"),
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

# =========================================
# Nutrient display names
# =========================================
def nutrient_display_name(nutrient):
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
    nutrient = str(nutrient).strip()
    if nutrient == "Ferritin":
        return get_ferritin_range(gender)
    return REFERENCE_RANGES.get(nutrient)

def validate_value(value, range_info):
    if value is None:
        return False, tr("Missing value.", "القيمة مفقودة.")
    if value <= 0:
        return False, tr("Value cannot be negative.", "القيمة لا يمكن أن تكون سالبة.")
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
# Analyze row (unchanged logic)
# =========================================
def analyze_row(row):
    nutrient = str(row.get("Nutrient", "")).strip()
    value    = float(row.get("Value", 0))
    gender   = normalize_gender(row.get("Gender", "Male"))
    age      = row.get("Age", None)
    range_info = get_range(nutrient, gender)

    if range_info is None:
        return {
            "Age": age, "Gender": gender, "Nutrient": nutrient, "Value": value,
            "Unit": "Unknown", "Low": None, "High": None, "Status": "Unknown",
            "Explanation": tr("Unknown nutrient.", "عنصر غير معروف"),
            "Possible Causes": "", "Recommendations": "",
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
        }

    low, high, unit = range_info["low"], range_info["high"], range_info["unit"]
    status = classify_value(value, low, high)

    return {
        "Age": age, "Gender": gender, "Nutrient": nutrient, "Value": value,
        "Unit": unit, "Low": low, "High": high, "Status": status,
        "Explanation": get_explanation(nutrient, value, unit, status, low, high),
        "Possible Causes": "; ".join(get_possible_causes(nutrient, status)),
        "Recommendations": "; ".join(get_recommendations(status)),
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
        tr("Status","الحالة"), tr("Low","الأدنى"), tr("High","الأقصى"),
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
        gender_display = tr("Male","ذكر") if str(row.get("Gender","")).lower() in ["male","1","m"] else tr("Female","أنثى")

        cells = [
            f'<td style="font-weight:700; color:#F0F4F8;">{nutrient_display_name(row.get("Nutrient",""))}</td>',
            f'<td style="font-weight:700; color:{color}; font-size:16px;">{row.get("Value","")}</td>',
            f'<td style="color:#7A9BB5;">{row.get("Unit","")}</td>',
            f'<td><span style="display:inline-flex; align-items:center; gap:5px; padding:4px 12px; '
            f'border-radius:999px; font-size:12px; font-weight:700; color:{color}; '
            f'background:{color}18; border:1px solid {color}44;">'
            f'{icon} {status_text(status)}</span></td>',
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
                gender_value = 1 if gender_text in ["Male", "ذكر"] else 2
                st.session_state["manual_items"].append({
                    "Age": age, "Gender": gender_value,
                    "Nutrient": nutrient, "Value": value,
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
                          tr("Nutrient","العنصر"), tr("Value","القيمة"), ""]
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
    <td style="padding:10px 14px; text-align:center;">
        <span id="del_{i}" style="cursor:pointer; color:#FF4B4B; font-size:12px; padding:3px 8px;
                                   border:1px solid rgba(255,75,75,0.30); border-radius:6px;">✕</span>
    </td>
</tr>"""

            st.html(f"""
<div style="overflow-x:auto; border-radius:14px; border:1px solid rgba(255,255,255,0.07); direction:{dir_val};">
    <table style="width:100%; border-collapse:collapse; font-family:'Plus Jakarta Sans','Cairo',sans-serif;">
        <thead><tr>{header_cells}</tr></thead>
        <tbody>{rows_html}</tbody>
    </table>
</div>""")

        if analyze_manual_clicked:
            if len(st.session_state["manual_items"]) == 0:
                st.warning(tr("Please add at least one nutrient.", "يرجى إضافة عنصر واحد على الأقل."))
            else:
                with st.spinner(tr("Analyzing...", "جاري التحليل...")):
                    input_df = pd.DataFrame(st.session_state["manual_items"])
                    analyzed = [analyze_row(r) for _, r in input_df.iterrows()]
                    st.session_state["results_df"] = pd.DataFrame(analyzed)

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
                                })
                    st.session_state["results_df"]  = pd.DataFrame(analyzed)
                    st.session_state["csv_input_df"] = df.copy()

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
