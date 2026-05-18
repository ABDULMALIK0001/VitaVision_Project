"""
Clean VitaVision dashboard for the Streamlit project.

The page mirrors the React dashboard direction:
- calm dashboard header
- health score from 100
- priority focus chips
- compact stats
- trend chart
- quick recommendation
- latest values with previous-reading comparison
"""

from __future__ import annotations

import html

import pandas as pd
import plotly.graph_objects as go
import streamlit as st


STATUS_META = {
    "Normal": {"label_en": "Normal", "label_ar": "طبيعي", "color": "#1D9E75", "soft": "#E1F5EE", "text": "#085041"},
    "Deficient": {"label_en": "Low", "label_ar": "منخفض", "color": "#BA7517", "soft": "#FAEEDA", "text": "#633806"},
    "Excessive": {"label_en": "High", "label_ar": "مرتفع", "color": "#D85A30", "soft": "#FCEBEB", "text": "#501313"},
    "Invalid": {"label_en": "Needs review", "label_ar": "يحتاج مراجعة", "color": "#71857E", "soft": "#EEF2F0", "text": "#34423D"},
    "Unknown": {"label_en": "Unknown", "label_ar": "غير معروف", "color": "#71857E", "soft": "#EEF2F0", "text": "#34423D"},
}

CHANGE_META = {
    "improved": {"en": "Improved", "ar": "تحسن", "color": "#1D9E75", "bg": "#E1F5EE"},
    "worse": {"en": "Needs attention", "ar": "يحتاج انتباه", "color": "#D85A30", "bg": "#FCEBEB"},
    "stable": {"en": "Stable", "ar": "مستقر", "color": "#71857E", "bg": "#EEF2F0"},
    "new": {"en": "New reading", "ar": "قراءة جديدة", "color": "#185FA5", "bg": "#E6F1FB"},
}


def render(reports, ctx):
    _inject_styles(ctx)

    latest = reports[-1]
    results = latest.get("results", [])

    _hero(latest, ctx)
    _stat_grid(reports, results, ctx)
    _timeline_card(reports, ctx)
    _recommendation_strip(results, ctx)
    _latest_values(results, reports, ctx)


def _inject_styles(ctx):
    ar = ctx["is_arabic"]
    light = ctx["is_light_theme"]
    direction = "rtl" if ar else "ltr"
    align = "right" if ar else "left"
    font = "'Cairo', sans-serif" if ar else "'Plus Jakarta Sans', sans-serif"

    if light:
        page = "#FAFDFC"
        card = "#FFFFFF"
        inner = "#F7FBF9"
        border = "#E4ECE8"
        text = "#2C2C2A"
        muted = "#6B7280"
        shadow = "0 14px 30px rgba(8, 80, 65, 0.06)"
        chart_grid = "#EDF3F1"
    else:
        page = "#08121A"
        card = "#101C24"
        inner = "#13232D"
        border = "rgba(255,255,255,0.10)"
        text = "#F0F4F8"
        muted = "#9AAAB8"
        shadow = "0 16px 34px rgba(0,0,0,0.22)"
        chart_grid = "rgba(255,255,255,0.08)"

    st.html(f"""
<style>
.vv-dash {{
    direction: {direction};
    text-align: {align};
    font-family: {font};
}}
.vv-card {{
    background: {card};
    border: 1px solid {border};
    border-radius: 8px;
    box-shadow: {shadow};
}}
.vv-hero {{
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    gap: 16px;
    margin: 8px 0 18px;
    flex-wrap: wrap;
}}
.vv-eyebrow {{
    color: #1D9E75;
    font-size: 12px;
    font-weight: 800;
    margin-bottom: 6px;
}}
.vv-title {{
    color: {text};
    font-size: 28px;
    line-height: 1.2;
    font-weight: 850;
    margin: 0;
    letter-spacing: 0;
}}
.vv-subtitle {{
    color: {muted};
    font-size: 13.5px;
    margin-top: 8px;
}}
.vv-health {{
    display: grid;
    grid-template-columns: 150px minmax(0, 1fr);
    gap: 18px;
    align-items: center;
    padding: 18px;
    margin-bottom: 14px;
}}
@media (max-width: 700px) {{
    .vv-health {{ grid-template-columns: 1fr; }}
}}
.vv-score-ring {{
    width: 118px;
    height: 118px;
    border-radius: 50%;
    margin: 0 auto;
    background: conic-gradient(var(--score-color) calc(var(--score) * 1%), #EDF3F1 0);
    display: grid;
    place-items: center;
}}
.vv-score-core {{
    width: 86px;
    height: 86px;
    border-radius: 50%;
    background: {card};
    display: grid;
    place-items: center;
    text-align: center;
}}
.vv-score-number {{
    color: {text};
    font-size: 30px;
    line-height: 1;
    font-weight: 850;
}}
.vv-score-label {{
    color: {muted};
    font-size: 10.5px;
    font-weight: 800;
    margin-top: 4px;
}}
.vv-health-title {{
    color: {text};
    font-size: 18px;
    font-weight: 850;
    margin-bottom: 6px;
}}
.vv-health-body {{
    color: {muted};
    font-size: 13.5px;
    line-height: 1.75;
    margin-bottom: 12px;
}}
.vv-chip-row {{
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
}}
.vv-chip {{
    display: inline-flex;
    align-items: center;
    gap: 7px;
    padding: 7px 10px;
    border-radius: 999px;
    background: var(--chip-bg);
    color: var(--chip-color);
    border: 1px solid var(--chip-border);
    font-size: 12px;
    font-weight: 800;
}}
.vv-chip-dot {{
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--chip-color);
}}
.vv-stats {{
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 12px;
    margin-bottom: 14px;
}}
@media (max-width: 820px) {{
    .vv-stats {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
}}
@media (max-width: 520px) {{
    .vv-stats {{ grid-template-columns: 1fr; }}
}}
.vv-stat {{
    border-radius: 8px;
    padding: 14px 16px;
    min-height: 88px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    background: var(--stat-bg);
    border: 1px solid var(--stat-border);
}}
.vv-stat-label {{
    color: var(--stat-text);
    opacity: 0.82;
    font-size: 12px;
    font-weight: 800;
}}
.vv-stat-value {{
    color: var(--stat-text);
    font-size: 28px;
    line-height: 1;
    font-weight: 850;
}}
.vv-section {{
    padding: 18px;
    margin-bottom: 14px;
}}
.vv-section-head {{
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    gap: 12px;
    flex-wrap: wrap;
    margin-bottom: 14px;
}}
.vv-section-title {{
    color: {text};
    font-size: 16px;
    font-weight: 850;
}}
.vv-section-sub {{
    color: {muted};
    font-size: 12px;
    margin-top: 3px;
}}
.vv-empty {{
    color: {muted};
    text-align: center;
    padding: 38px 16px;
    border: 1px dashed {border};
    border-radius: 8px;
    background: {inner};
}}
.vv-insight {{
    border-radius: 8px;
    padding: 13px 16px;
    margin-bottom: 14px;
    background: var(--insight-bg);
    color: var(--insight-text);
    border: 1px solid var(--insight-border);
    border-inline-start: 4px solid var(--insight-color);
}}
.vv-insight-title {{
    font-size: 13.5px;
    font-weight: 850;
    margin-bottom: 4px;
}}
.vv-insight-text {{
    font-size: 13.5px;
    line-height: 1.75;
    opacity: 0.92;
}}
.vv-values {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 12px;
}}
.vv-value-card {{
    min-height: 152px;
    padding: 14px;
    border-radius: 8px;
    background: {card};
    border: 1px solid {border};
    border-inline-start: 4px solid var(--status-color);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}}
.vv-value-head {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 8px;
}}
.vv-value-name {{
    color: {text};
    font-size: 14.5px;
    font-weight: 850;
}}
.vv-pill {{
    color: var(--status-text);
    background: var(--status-bg);
    padding: 3px 9px;
    border-radius: 999px;
    font-size: 11.5px;
    font-weight: 850;
}}
.vv-value-main {{
    color: var(--status-color);
    font-size: 22px;
    font-weight: 850;
    margin-top: 12px;
}}
.vv-range {{
    color: {muted};
    font-size: 11.5px;
    margin-top: 7px;
}}
.vv-bar {{
    position: relative;
    height: 8px;
    background: #EDF3F1;
    border-radius: 999px;
    overflow: hidden;
    margin-top: 10px;
}}
.vv-bar-zone {{
    position: absolute;
    top: 0;
    bottom: 0;
    left: 25%;
    right: 25%;
    background: #D7EEE6;
}}
.vv-bar-marker {{
    position: absolute;
    top: -2px;
    bottom: -2px;
    width: 4px;
    border-radius: 6px;
    background: var(--status-color);
}}
.vv-change-row {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 8px;
    margin-top: 10px;
}}
.vv-change {{
    color: var(--change-color);
    background: var(--change-bg);
    padding: 4px 9px;
    border-radius: 999px;
    font-size: 11.5px;
    font-weight: 850;
}}
.vv-change-note {{
    color: {muted};
    font-size: 11px;
}}
.vv-chart-grid-token {{
    color: {chart_grid};
}}
</style>
""")


def _hero(latest_report, ctx):
    tr = ctx["tr"]
    last_date = ctx["report_display_date"](latest_report)
    st.html(f"""
<div class="vv-dash">
  <section class="vv-hero">
    <div>
      <div class="vv-eyebrow">{html.escape(tr("Analysis summary", "ملخص الحالة"))}</div>
      <h1 class="vv-title">{html.escape(tr("Dashboard", "لوحة النتائج"))}</h1>
      <div class="vv-subtitle">{html.escape(tr(f"Last test: {last_date}", f"آخر تحليل: {last_date}"))}</div>
    </div>
  </section>
</div>
""")


def _health_score_panel(reports, results, ctx):
    tr = ctx["tr"]
    score = _health_score(results)
    issues = _priority_issues(results)
    changes = _comparison_counts(reports, results, ctx)

    if score >= 85:
        color = "#1D9E75"
        title = tr("Strong health snapshot", "مؤشر صحي مطمئن")
        body = tr(
            "Your latest values look stable overall. Keep tracking the same nutrients over time.",
            "القيم الأخيرة تبدو مستقرة إجمالًا. استمر في متابعة نفس العناصر مع الوقت.",
        )
    elif score >= 65:
        color = "#BA7517"
        title = tr("A few values need follow-up", "توجد قيم تحتاج متابعة")
        body = tr(
            "The score highlights what to focus on first, without reading every detail.",
            "المؤشر يوضح لك أين تركز أولًا بدون قراءة كل التفاصيل.",
        )
    else:
        color = "#D85A30"
        title = tr("Follow-up is important", "المتابعة مهمة")
        body = tr(
            "Several values are outside the normal range. Use this dashboard as a guide and discuss persistent changes with a clinician.",
            "عدة قيم خارج النطاق الطبيعي. استخدم اللوحة كدليل وناقش التغيرات المستمرة مع مختص صحي.",
        )

    chips = []
    if issues:
        for item in issues[:3]:
            meta = _status_meta(item.get("Status"), ctx)
            name = ctx["nutrient_display_name"](item.get("Nutrient", ""))
            chips.append(_chip(name + " · " + meta["label"], meta["color"], meta["soft"]))
    else:
        meta = STATUS_META["Normal"]
        chips.append(_chip(tr("No urgent values in the latest report", "لا توجد قيم عاجلة في آخر قراءة"), meta["color"], meta["soft"]))

    if changes["tracked"]:
        chips.append(_chip(
            tr(f"{changes['improved']} improved · {changes['worse']} worsened", f"{changes['improved']} تحسن · {changes['worse']} تراجع"),
            "#185FA5",
            "#E6F1FB",
        ))

    st.html(f"""
<div class="vv-dash">
  <section class="vv-card vv-health">
    <div class="vv-score-ring" style="--score:{score}; --score-color:{color};">
      <div class="vv-score-core">
        <div>
          <div class="vv-score-number">{score}</div>
          <div class="vv-score-label">{html.escape(tr("out of 100", "من 100"))}</div>
        </div>
      </div>
    </div>
    <div>
      <div class="vv-health-title">{html.escape(title)}</div>
      <div class="vv-health-body">{html.escape(body)}</div>
      <div class="vv-chip-row">{''.join(chips)}</div>
    </div>
  </section>
</div>
""")


def _stat_grid(reports, results, ctx):
    tr = ctx["tr"]
    total = len(reports)
    low = sum(1 for result in results if str(result.get("Status")) == "Deficient")
    high = sum(1 for result in results if str(result.get("Status")) == "Excessive")
    issues = low + high
    tracked = len({result.get("Nutrient") for result in results if result.get("Nutrient")})
    improved = _comparison_counts(reports, results, ctx)["improved"]

    cards = [
        (tr("Reports", "التقارير"), total, "#71857E", "#EEF2F0"),
        (tr("Need follow-up", "قيم تحتاج متابعة"), issues, "#D85A30" if issues else "#1D9E75", "#FCEBEB" if issues else "#E1F5EE"),
        (tr("Tracked nutrients", "عناصر متتبعة"), tracked, "#1D9E75", "#E1F5EE"),
        (tr("Improved", "تحسن"), improved if improved else "—", "#1D9E75", "#E1F5EE"),
    ]

    cards_html = "".join(
        f"""
        <div class="vv-stat" style="--stat-bg:{bg}; --stat-border:{color}25; --stat-text:{color};">
          <div class="vv-stat-label">{html.escape(str(label))}</div>
          <div class="vv-stat-value">{html.escape(str(value))}</div>
        </div>
        """
        for label, value, color, bg in cards
    )

    st.html(f'<div class="vv-dash"><section class="vv-stats">{cards_html}</section></div>')


def _timeline_card(reports, ctx):
    tr = ctx["tr"]
    names = sorted(
        [
            name for name in _all_nutrient_names(reports)
            if any(
                reading.get("valid") and reading.get("value") is not None
                for reading in ctx["nutrient_readings_from_reports"](reports, name)
            )
        ],
        key=ctx["nutrient_display_name"],
    )
    if not names:
        return

    selected = st.session_state.get("vv_clean_timeline", names[0])
    if selected not in names:
        selected = names[0]

    readings = ctx["nutrient_readings_from_reports"](reports, selected)
    valid = [reading for reading in readings if reading.get("valid") and reading.get("value") is not None]

    with st.container(border=True):
        st.html(f"""
<div class="vv-dash">
  <div class="vv-section-head">
    <div>
      <div class="vv-section-title">{html.escape(tr("Value trend", "تغير القيم مع الوقت"))}</div>
      <div class="vv-section-sub">{html.escape(tr(f"{len(valid)} measurement points", f"{len(valid)} نقطة قياس"))}</div>
    </div>
  </div>
</div>
""")
        selected = st.selectbox(
            tr("Choose nutrient", "اختر العنصر"),
            options=names,
            index=names.index(selected),
            format_func=ctx["nutrient_display_name"],
            key="vv_clean_timeline",
        )
        _render_timeline_chart(reports, selected, ctx)


def _render_timeline_chart(reports, nutrient, ctx):
    readings = ctx["nutrient_readings_from_reports"](reports, nutrient)
    valid = [reading for reading in readings if reading.get("valid") and reading.get("value") is not None]
    if not valid:
        _empty_state(ctx["tr"]("Not enough data yet.", "لا توجد بيانات كافية بعد."))
        return

    light = ctx["is_light_theme"]
    fg = "#36564C" if light else "#9AAAB8"
    grid = "#EDF3F1" if light else "rgba(255,255,255,0.08)"

    dates = [pd.to_datetime(reading["created_at"]) for reading in valid]
    show_year = len({date_value.year for date_value in dates}) > 1
    label_format = "%d/%m/%Y" if show_year else "%d/%m"
    xs = [str(i + 1) for i in range(len(valid))]
    x_labels = [date_value.strftime(label_format) for date_value in dates]
    ys = [float(reading["value"]) for reading in valid]
    colors = [_status_meta(reading.get("status"), ctx)["color"] for reading in valid]
    hover = [
        f"<b>{value:g}</b><br>{date_value.strftime('%Y/%m/%d')}<br>{ctx['status_text'](reading.get('status'))}"
        for value, date_value, reading in zip(ys, dates, valid)
    ]

    y_min = min(ys)
    y_max = max(ys)
    span = y_max - y_min
    pad = max(span * 0.25, 0.5) if span else max(abs(y_min) * 0.05, 1.0)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=xs,
        y=ys,
        mode="lines+markers" if len(xs) > 1 else "markers",
        line=dict(color="#1D9E75", width=2.8, shape="spline"),
        marker=dict(size=10, color=colors, line=dict(color="#FFFFFF", width=1.7)),
        text=hover,
        hovertemplate="%{text}<extra></extra>",
    ))
    fig.update_layout(
        height=285,
        margin=dict(t=12, b=34, l=34, r=16),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        xaxis=dict(
            type="category",
            tickmode="array",
            tickvals=xs,
            ticktext=x_labels,
            showgrid=False,
            color=fg,
            zeroline=False,
            showline=False,
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor=grid,
            griddash="dot",
            color=fg,
            zeroline=False,
            showline=False,
            range=[y_min - pad, y_max + pad],
        ),
        font=dict(family="Cairo, Plus Jakarta Sans, sans-serif", color=fg, size=12),
        hoverlabel=dict(bgcolor="#FFFFFF" if light else "#0F2433", font_color="#0F2433" if light else "#F0F4F8"),
    )
    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})


def _recommendation_strip(results, ctx):
    tr = ctx["tr"]
    issues = [result for result in results if str(result.get("Status")) in ("Deficient", "Excessive")]

    if not issues:
        color = "#1D9E75"
        bg = "#E1F5EE"
        title = tr("Everything looks healthy", "كل شيء يبدو مطمئنًا")
        text = tr(
            "All measured values are within their normal ranges. Maintain your healthy routine.",
            "كل القيم المقاسة ضمن النطاق الطبيعي. استمر على نمطك الصحي.",
        )
    elif len(issues) == 1:
        color = "#BA7517"
        bg = "#FAEEDA"
        name = ctx["nutrient_display_name"](issues[0].get("Nutrient", ""))
        title = tr(f"Follow up: {name}", f"يحتاج متابعة: {name}")
        text = tr(
            "One value needs attention. Track it again and discuss persistent changes with a clinician.",
            "توجد قيمة تحتاج انتباهًا. تابعها مرة أخرى وناقش استمرار التغير مع مختص صحي.",
        )
    else:
        color = "#D85A30"
        bg = "#FCEBEB"
        title = tr("Follow-up recommended", "توجد قيم تحتاج متابعة")
        text = tr(
            "Several values are outside the normal range. Focus first on the priority items above.",
            "عدة قيم خارج النطاق الطبيعي. ركز أولًا على العناصر المهمة بالأعلى.",
        )

    st.html(f"""
<div class="vv-dash">
  <section class="vv-insight" style="--insight-bg:{bg}; --insight-border:{color}30; --insight-color:{color}; --insight-text:{_status_text_color(color)};">
    <div class="vv-insight-title">{html.escape(title)}</div>
    <div class="vv-insight-text">{html.escape(text)}</div>
  </section>
</div>
""")


def _latest_values(results, reports, ctx):
    tr = ctx["tr"]
    if not results:
        _empty_state(tr("No values to display.", "لا توجد قيم لعرضها."))
        return

    priority = {"Excessive": 0, "Deficient": 1, "Invalid": 2, "Normal": 3}
    sorted_results = sorted(results, key=lambda result: priority.get(str(result.get("Status")), 9))
    cards = "".join(_value_card(result, reports, ctx) for result in sorted_results)

    st.html(f"""
<div class="vv-dash">
  <section class="vv-card vv-section">
    <div class="vv-section-head">
      <div>
        <div class="vv-section-title">{html.escape(tr("Latest values", "آخر القيم"))}</div>
        <div class="vv-section-sub">{html.escape(tr("Priority values appear first", "القيم الأهم تظهر أولًا"))}</div>
      </div>
    </div>
    <div class="vv-values">{cards}</div>
  </section>
</div>
""")


def _value_card(result, reports, ctx):
    nutrient = result.get("Nutrient", "")
    status = str(result.get("Status", "Unknown"))
    meta = _status_meta(status, ctx)
    name = ctx["nutrient_display_name"](nutrient)
    value = _number_text(result.get("Value"))
    unit = str(result.get("Unit", "") or "")
    low = result.get("Low")
    high = result.get("High")
    range_text = _range_text(low, high, unit, ctx)
    marker = _range_marker(result.get("Value"), low, high)
    change = _nutrient_change(reports, nutrient, ctx)
    change_html = _change_html(change, ctx)
    marker_html = "" if marker is None else f'<div class="vv-bar-marker" style="right:calc({100 - marker:.1f}% - 2px);"></div>'

    return f"""
<article class="vv-value-card" style="--status-color:{meta['color']}; --status-bg:{meta['soft']}; --status-text:{meta['text']};">
  <div>
    <div class="vv-value-head">
      <div>
        <div class="vv-value-name">{html.escape(name)}</div>
      </div>
      <span class="vv-pill">{html.escape(meta['label'])}</span>
    </div>
    <div class="vv-value-main">{html.escape(value)} <span style="font-size:11.5px; color:#6B7280;">{html.escape(unit)}</span></div>
    <div class="vv-bar"><div class="vv-bar-zone"></div>{marker_html}</div>
    <div class="vv-range">{html.escape(range_text)}</div>
  </div>
  {change_html}
</article>
"""


def _health_score(results):
    if not results:
        return 0
    penalty = 0.0
    for result in results:
        status = str(result.get("Status", "Unknown"))
        if status == "Normal":
            continue
        if status in ("Deficient", "Excessive"):
            penalty += 16 + min(_severity_score(result) * 18, 14)
        elif status == "Invalid":
            penalty += 12
        else:
            penalty += 6
    return int(max(0, min(100, round(100 - penalty))))


def _priority_issues(results):
    issues = [result for result in results if str(result.get("Status")) in ("Deficient", "Excessive", "Invalid")]
    return sorted(issues, key=_severity_score, reverse=True)


def _severity_score(result):
    status = str(result.get("Status", "Unknown"))
    if status == "Invalid":
        return 1.0
    try:
        value = float(result.get("Value"))
        low = float(result.get("Low"))
        high = float(result.get("High"))
    except (TypeError, ValueError):
        return 0.5 if status in ("Deficient", "Excessive") else 0.0
    if pd.isna(value) or pd.isna(low) or pd.isna(high):
        return 0.5 if status in ("Deficient", "Excessive") else 0.0
    if status == "Deficient" and low:
        return max(0.0, (low - value) / abs(low))
    if status == "Excessive" and high:
        return max(0.0, (value - high) / abs(high))
    return 0.0


def _all_nutrient_names(reports):
    return {
        str(result.get("Nutrient", ""))
        for report in reports
        for result in report.get("results", [])
        if result.get("Nutrient")
    }


def _comparison_counts(reports, results, ctx):
    counts = {"improved": 0, "worse": 0, "stable": 0, "tracked": 0}
    for result in results:
        change = _nutrient_change(reports, result.get("Nutrient"), ctx)
        if not change or change["kind"] == "new":
            continue
        counts["tracked"] += 1
        counts[change["kind"]] = counts.get(change["kind"], 0) + 1
    return counts


def _nutrient_change(reports, nutrient, ctx):
    if not nutrient:
        return {"kind": "new", "delta": None, "unit": ""}
    readings = ctx["nutrient_readings_from_reports"](reports, nutrient)
    valid = [reading for reading in readings if reading.get("valid") and reading.get("value") is not None]
    if len(valid) < 2:
        unit = valid[-1].get("unit", "") if valid else ""
        return {"kind": "new", "delta": None, "unit": unit}

    previous = valid[-2]
    current = valid[-1]
    try:
        delta = float(current.get("value")) - float(previous.get("value"))
    except (TypeError, ValueError):
        return {"kind": "stable", "delta": None, "unit": current.get("unit", "")}

    prev_status = str(previous.get("status", "Unknown"))
    curr_status = str(current.get("status", "Unknown"))
    if abs(delta) < 1e-9 and prev_status == curr_status:
        kind = "stable"
    elif curr_status == "Normal" and prev_status != "Normal":
        kind = "improved"
    elif prev_status == "Normal" and curr_status != "Normal":
        kind = "worse"
    elif curr_status == prev_status == "Deficient":
        kind = "improved" if delta > 0 else "worse"
    elif curr_status == prev_status == "Excessive":
        kind = "improved" if delta < 0 else "worse"
    elif curr_status == prev_status:
        kind = "stable"
    else:
        kind = "worse"

    return {"kind": kind, "delta": delta, "unit": current.get("unit", "")}


def _change_html(change, ctx):
    tr = ctx["tr"]
    change = change or {"kind": "new", "delta": None, "unit": ""}
    meta = CHANGE_META.get(change["kind"], CHANGE_META["stable"])
    label = tr(meta["en"], meta["ar"])
    delta = _delta_text(change.get("delta"), change.get("unit", ""))
    note = tr("first reading", "أول قراءة") if change["kind"] == "new" else tr("vs previous", "مقارنة بالسابق")
    return f"""
<div class="vv-change-row">
  <span class="vv-change" style="--change-color:{meta['color']}; --change-bg:{meta['bg']};">{html.escape(label + delta)}</span>
  <span class="vv-change-note">{html.escape(note)}</span>
</div>
"""


def _chip(text, color, bg):
    return f"""
<span class="vv-chip" style="--chip-color:{color}; --chip-bg:{bg}; --chip-border:{color}25;">
  <span class="vv-chip-dot"></span>{html.escape(str(text))}
</span>
"""


def _status_meta(status, ctx):
    status = str(status or "Unknown")
    meta = STATUS_META.get(status, STATUS_META["Unknown"]).copy()
    meta["label"] = ctx["tr"](meta["label_en"], meta["label_ar"])
    return meta


def _number_text(value):
    try:
        numeric = float(value)
        if pd.isna(numeric):
            return "—"
        return f"{numeric:g}"
    except (TypeError, ValueError):
        return "—"


def _range_text(low, high, unit, ctx):
    tr = ctx["tr"]
    try:
        lo = float(low)
        hi = float(high)
        if pd.isna(lo) or pd.isna(hi):
            raise ValueError
        return tr(f"Normal: {lo:g}-{hi:g} {unit}", f"الطبيعي: {lo:g}-{hi:g} {unit}")
    except (TypeError, ValueError):
        return tr("Normal range unavailable", "النطاق الطبيعي غير متوفر")


def _range_marker(value, low, high):
    try:
        v = float(value)
        lo = float(low)
        hi = float(high)
    except (TypeError, ValueError):
        return None
    if pd.isna(v) or pd.isna(lo) or pd.isna(hi) or hi <= lo:
        return None
    span = hi - lo
    axis_low = max(0, lo - span * 0.5)
    axis_high = hi + span * 0.5
    if axis_high <= axis_low:
        return None
    return max(3, min(97, ((v - axis_low) / (axis_high - axis_low)) * 100))


def _delta_text(delta, unit):
    if delta is None:
        return ""
    if abs(delta) < 1e-9:
        return " 0"
    sign = "+" if delta > 0 else ""
    unit_text = f" {unit}" if unit else ""
    return f" {sign}{delta:g}{unit_text}"


def _status_text_color(color):
    if color == "#D85A30":
        return "#501313"
    if color == "#BA7517":
        return "#633806"
    return "#085041"


def _empty_state(message):
    st.html(f'<div class="vv-dash"><div class="vv-empty">{html.escape(message)}</div></div>')
