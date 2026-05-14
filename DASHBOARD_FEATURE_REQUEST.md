# VitaVision Dashboard Feature Request

## الهدف

إضافة ميزة جديدة إلى مشروع VitaVision وهي تبويب مستقل باسم **Dashboard / لوحة التحكم** داخل تطبيق Streamlit.

الهدف من الميزة هو عرض ملخص تحليلي وبصري لنتائج تحاليل الفيتامينات والمعادن بعد إدخال البيانات يدويًا أو رفع ملف CSV.

---

## خلفية عن المشروع الحالي

المشروع الحالي مبني باستخدام:

- Python
- Streamlit
- pandas
- Plotly

الملف الرئيسي للتطبيق:

```text
app.py
```

حاليًا يقوم التطبيق بتحليل نتائج المستخدم من خلال الدالة:

```python
analyze_row(row)
```

ويتم حفظ النتائج داخل:

```python
st.session_state["results_df"]
```

النتائج تحتوي غالبًا على الأعمدة التالية:

```text
Age, Gender, Nutrient, Value, Unit, Low, High, Status, Explanation, Possible Causes, Recommendations
```

وقيم عمود `Status` تكون مثل:

```text
Deficient
Normal
Excessive
Invalid
Unknown
Error
```

---

## الميزة المطلوبة

إضافة تبويب جديد في الواجهة باسم:

```text
Dashboard
```

وفي النسخة العربية:

```text
لوحة التحكم
```

يظهر التبويب بجانب التبويبات الحالية:

```text
Home | About | Contact
```

ليصبح:

```text
Home | Dashboard | About | Contact
```

---

## سيناريو الاستخدام

1. يدخل المستخدم إلى تطبيق VitaVision.
2. يقوم بإدخال نتائج التحاليل يدويًا أو رفع ملف CSV.
3. يضغط على زر التحليل.
4. يقوم النظام بتصنيف النتائج إلى:
   - Normal
   - Deficient
   - Excessive
   - أو حالات أخرى مثل Invalid / Error
5. ينتقل المستخدم إلى تبويب Dashboard.
6. يرى ملخصًا سريعًا لنتائجه:
   - إجمالي التحاليل
   - عدد النتائج الطبيعية
   - عدد النتائج الناقصة
   - عدد النتائج المرتفعة
   - نسبة النتائج غير الطبيعية
7. يستطيع المستخدم مشاهدة الرسوم البيانية واستخدام الفلاتر لعرض نتائج محددة.

---

## User Story

As a VitaVision user,  
I want to view a dashboard summary of my vitamin and mineral analysis results,  
so that I can quickly understand my overall health status and identify which nutrients need attention.

---

## المتطلبات الوظيفية

يجب أن تحتوي لوحة التحكم على:

1. تبويب مستقل باسم Dashboard / لوحة التحكم.
2. رسالة واضحة إذا لم توجد نتائج تحليل بعد.
3. بطاقات إحصائية تعرض:
   - Total Results
   - Normal
   - Deficient
   - Excessive
   - Abnormal Percentage
4. رسم Pie Chart يوضح توزيع الحالات.
5. رسم Bar Chart يوضح حالة كل عنصر غذائي.
6. فلاتر حسب:
   - Status
   - Nutrient
7. جدول يعرض النتائج بعد الفلترة.
8. دعم اللغة الإنجليزية والعربية باستخدام دالة `tr(en, ar)` الموجودة في المشروع.
9. عدم التأثير على وظائف الإدخال اليدوي أو رفع CSV الحالية.

---

## Acceptance Criteria

- يظهر تبويب Dashboard في الواجهة.
- إذا لم يتم تحليل أي بيانات، تظهر رسالة تطلب من المستخدم إدخال أو رفع بيانات أولًا.
- بعد التحليل، تظهر الإحصائيات بشكل صحيح بناءً على `st.session_state["results_df"]`.
- تظهر الرسوم البيانية باستخدام Plotly.
- تعمل الفلاتر بدون تعديل البيانات الأصلية.
- تعمل الميزة مع الإدخال اليدوي ورفع CSV.
- تدعم اللغة العربية والإنجليزية.
- لا يتم حذف أو تغيير منطق التحليل الحالي.

---

## التعديل المطلوب في التبويبات

ابحث في `app.py` عن تعريف التبويبات الحالي، ويكون قريبًا من الشكل التالي:

```python
home_tab, about_tab, contact_tab = st.tabs([
    tr("Home", "الرئيسية"),
    tr("About", "عن المشروع"),
    tr("Contact", "تواصل معنا")
])
```

استبدله بهذا الشكل:

```python
home_tab, dashboard_tab, about_tab, contact_tab = st.tabs([
    tr("Home", "الرئيسية"),
    tr("Dashboard", "لوحة التحكم"),
    tr("About", "عن المشروع"),
    tr("Contact", "تواصل معنا")
])
```

---

## كود مرجعي مقترح للداشبورد

ضع الكود التالي بعد نهاية جزء:

```python
with home_tab:
```

وقبل بداية:

```python
with about_tab:
```

الكود:

```python
# =========================================
# DASHBOARD TAB
# =========================================
with dashboard_tab:
    render_header()

    section_title(tr("Dashboard", "لوحة التحكم"), 26, "")

    results_df = st.session_state.get("results_df", pd.DataFrame())

    if results_df.empty:
        st.info(tr(
            "No analysis results yet. Please enter lab values or upload a CSV file first.",
            "لا توجد نتائج تحليل حتى الآن. يرجى إدخال قيم التحاليل أو رفع ملف CSV أولًا."
        ))
    else:
        valid_statuses = ["Normal", "Deficient", "Excessive"]
        dashboard_df = results_df[results_df["Status"].isin(valid_statuses)].copy()

        total_results = len(results_df)
        normal_count = len(results_df[results_df["Status"] == "Normal"])
        deficient_count = len(results_df[results_df["Status"] == "Deficient"])
        excessive_count = len(results_df[results_df["Status"] == "Excessive"])
        abnormal_count = deficient_count + excessive_count

        abnormal_percent = 0
        if total_results > 0:
            abnormal_percent = round((abnormal_count / total_results) * 100, 1)

        col1, col2, col3, col4, col5 = st.columns(5)

        col1.metric(tr("Total", "الإجمالي"), total_results)
        col2.metric(tr("Normal", "طبيعي"), normal_count)
        col3.metric(tr("Deficient", "ناقص"), deficient_count)
        col4.metric(tr("Excessive", "مرتفع"), excessive_count)
        col5.metric(tr("Abnormal %", "نسبة غير الطبيعي"), f"{abnormal_percent}%")

        st.markdown("---")

        if dashboard_df.empty:
            st.warning(tr(
                "There are no valid analysis results to visualize.",
                "لا توجد نتائج تحليل صالحة لعرضها في الرسوم البيانية."
            ))
        else:
            status_counts = (
                dashboard_df["Status"]
                .value_counts()
                .reset_index()
            )
            status_counts.columns = ["Status", "Count"]

            if language == "English":
                status_label_col = "Status"
                status_color_map = {
                    "Normal": "#1DB954",
                    "Deficient": "#FF4B4B",
                    "Excessive": "#FFA500",
                }
            else:
                status_counts["Status_Display"] = status_counts["Status"].map({
                    "Normal": "طبيعي",
                    "Deficient": "ناقص",
                    "Excessive": "مرتفع",
                })
                status_label_col = "Status_Display"
                status_color_map = {
                    "طبيعي": "#1DB954",
                    "ناقص": "#FF4B4B",
                    "مرتفع": "#FFA500",
                }

            fig_status = px.pie(
                status_counts,
                names=status_label_col,
                values="Count",
                hole=0.45,
                title=tr("Status Distribution", "توزيع الحالات"),
                color=status_label_col,
                color_discrete_map=status_color_map,
            )

            fig_status.update_layout(
                height=380,
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#9AAAB8", family="Plus Jakarta Sans, Cairo"),
                legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#B8C8D8")),
                title=dict(font=dict(color="#B8C8D8", size=15)),
            )

            st.plotly_chart(fig_status, use_container_width=True, config={"displayModeBar": False})

            nutrient_status = (
                dashboard_df
                .groupby(["Nutrient", "Status"])
                .size()
                .reset_index(name="Count")
            )

            if language != "English":
                nutrient_status["Status_Display"] = nutrient_status["Status"].map({
                    "Normal": "طبيعي",
                    "Deficient": "ناقص",
                    "Excessive": "مرتفع",
                })
                bar_color_col = "Status_Display"
                bar_color_map = {
                    "طبيعي": "#1DB954",
                    "ناقص": "#FF4B4B",
                    "مرتفع": "#FFA500",
                }
            else:
                bar_color_col = "Status"
                bar_color_map = {
                    "Normal": "#1DB954",
                    "Deficient": "#FF4B4B",
                    "Excessive": "#FFA500",
                }

            fig_nutrients = px.bar(
                nutrient_status,
                x="Nutrient",
                y="Count",
                color=bar_color_col,
                title=tr("Nutrient Status Overview", "نظرة عامة على حالة العناصر"),
                color_discrete_map=bar_color_map,
            )

            fig_nutrients.update_layout(
                height=420,
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#9AAAB8", family="Plus Jakarta Sans, Cairo"),
                xaxis=dict(tickangle=-30),
                legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#B8C8D8")),
                title=dict(font=dict(color="#B8C8D8", size=15)),
            )

            st.plotly_chart(fig_nutrients, use_container_width=True, config={"displayModeBar": False})

        st.markdown("---")

        filter_col1, filter_col2 = st.columns(2)

        with filter_col1:
            selected_status = st.multiselect(
                tr("Filter by Status", "فلترة حسب الحالة"),
                options=list(results_df["Status"].dropna().unique()),
                default=list(results_df["Status"].dropna().unique()),
            )

        with filter_col2:
            selected_nutrients = st.multiselect(
                tr("Filter by Nutrient", "فلترة حسب العنصر"),
                options=list(results_df["Nutrient"].dropna().unique()),
                default=list(results_df["Nutrient"].dropna().unique()),
            )

        filtered_df = results_df[
            (results_df["Status"].isin(selected_status)) &
            (results_df["Nutrient"].isin(selected_nutrients))
        ].copy()

        section_title(tr("Filtered Results", "النتائج بعد الفلترة"), 22, "")
        st.dataframe(filtered_df, use_container_width=True)
```

---

## ملاحظات تنفيذية مهمة

1. لا تحذف الدوال الحالية مثل:

```python
analyze_row()
render_summary_stats()
render_results_table()
render_result_card()
create_reference_chart()
```

2. لا تغير طريقة حفظ النتائج الحالية:

```python
st.session_state["results_df"]
```

3. يجب أن يعتمد الداشبورد على النتائج الموجودة في `results_df` فقط.

4. يجب اختبار الميزة باستخدام:

```text
test_patient.csv
```

5. بعد إضافة الميزة، شغل التطبيق باستخدام:

```bash
streamlit run app.py
```

---

## اختبار سريع متوقع

باستخدام ملف `test_patient.csv`، يجب أن يظهر في Dashboard:

- عدد إجمالي للتحاليل.
- توزيع بين Normal و Deficient و Excessive.
- رسم دائري للحالات.
- رسم عمودي للعناصر.
- جدول قابل للفلترة.

---

## الأثر المتوقع

إضافة Dashboard ستجعل VitaVision أكثر احترافية، لأنها تحول النتائج من مجرد جدول وبطاقات إلى لوحة تحليلية تساعد المستخدم على فهم حالته بسرعة واتخاذ قرار أفضل حول العناصر التي تحتاج متابعة.

