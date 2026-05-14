# 🌿 VitaVision — Vitamin & Mineral Lab Analyzer

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?logo=streamlit)
![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-orange?logo=scikitlearn)
![License](https://img.shields.io/badge/License-Educational-green)

**تطبيق ذكي لتفسير نتائج تحاليل الفيتامينات والمعادن**  
*An intelligent web app for interpreting vitamin and mineral laboratory results*

</div>

---

## 📋 نبذة عن المشروع | About

**VitaVision** هو تطبيق ويب تفاعلي مبني بـ Streamlit يساعد المستخدمين على تفسير نتائج تحاليلهم المخبرية للفيتامينات والمعادن بطريقة سهلة وواضحة. يعتمد التطبيق على نطاقات مرجعية طبية معتمدة ونموذج Machine Learning مدرّب على بيانات حقيقية.

**VitaVision** is an interactive web application built with Streamlit that helps users interpret their vitamin and mineral laboratory results in a clear and intuitive way. The app relies on established medical reference ranges and a Machine Learning model trained on real-world data.

---

## ✨ المميزات | Features

| الميزة | Feature |
|--------|---------|
| 📝 إدخال يدوي لقيم التحاليل | Manual lab value input |
| 📂 رفع ملفات CSV مباشرة | CSV file upload support |
| 🌐 واجهة ثنائية اللغة (عربي / إنجليزي) | Bilingual interface (Arabic / English) |
| 🌙 وضع مظلم ومضيء | Dark and Light mode |
| 🤖 مقارنة مع نموذج ML | ML model comparison |
| 📊 لوحة تحكم تحليلية | Analytical Dashboard |
| 📄 تصدير النتائج CSV | Downloadable CSV results |
| ⚠️ إخلاء مسؤولية طبي | Medical disclaimer |

---

## 🧪 العناصر الغذائية المدعومة | Supported Nutrients

| العنصر | Nutrient | الوحدة | Unit |
|--------|----------|--------|------|
| فيتامين أ | Vitamin A | µg/dL | µg/dL |
| فيتامين ب6 | Vitamin B6 | mg/L | mg/L |
| فيتامين ب12 | Vitamin B12 | pg/mL | pg/mL |
| فيتامين ج | Vitamin C | mg/dL | mg/dL |
| فيتامين د | Vitamin D | ng/mL | ng/mL |
| فيتامين هـ | Vitamin E | mg/dL | mg/dL |
| فيتامين ك | Vitamin K | ng/mL | ng/mL |
| الكالسيوم | Calcium | mg/dL | mg/dL |
| الفيريتين | Ferritin | ng/mL | ng/mL |
| الفولات | Folate | ng/mL | ng/mL |
| المغنيسيوم | Magnesium | mg/dL | mg/dL |
| الزنك | Zinc | µg/dL | µg/dL |

---

## 🤖 نموذج الذكاء الاصطناعي | ML Model

تم تدريب النموذج باستخدام بيانات حقيقية من NHANES (National Health and Nutrition Examination Survey):

| المقياس | Metric | القيمة | Value |
|---------|--------|--------|-------|
| النموذج المختار | Selected Model | Random Forest | Random Forest |
| دقة الاختبار | Test Accuracy | **99.95%** | **99.95%** |
| F1 Score (Macro) | F1 Score (Macro) | **99.92%** | **99.92%** |
| حجم بيانات التدريب | Training Data | 51,438 صف | 51,438 rows |
| حجم بيانات الاختبار | Test Data | 16,031 صف | 16,031 rows |
| استراتيجية التقسيم | Split Strategy | Patient-level GroupShuffleSplit | Patient-level GroupShuffleSplit |

**المدخلات:** العمر، الجنس، العنصر الغذائي، القيمة  
**المخرجات:** Deficient / Normal / Excessive

---

## 🗂️ هيكل المشروع | Project Structure

```
VitaVision_Project/
│
├── app.py                                      # التطبيق الرئيسي (4120+ سطر)
├── requirements.txt                            # المكتبات المطلوبة
├── README.md                                   # توثيق المشروع
├── DASHBOARD_FEATURE_REQUEST.md               # مواصفات لوحة التحكم
│
├── data/
│   ├── VitaVision_Colab_Full_Pipeline.ipynb   # Pipeline الرسمي
│   ├── vitavision_final_labeled_dataset.csv    # البيانات الموحدة
│   ├── [nutrient]_cleaned.csv                  # بيانات نظيفة لكل عنصر
│   └── [nutrient]_labeled.csv                  # بيانات مصنّفة لكل عنصر
│
├── models/
│   ├── vitavision_unified_model.pkl            # النموذج الرئيسي (Random Forest)
│   ├── vitavision_random_forest_model.pkl
│   ├── vitavision_logistic_regression_model.pkl
│   ├── vitavision_hybrid_model_v1.pkl
│   ├── vitavision_unified_model_metadata.json  # معلومات النموذج
│   └── vitavision_model_comparison.csv         # مقارنة النماذج
│
├── reports/
│   └── vitavision_reports.json                 # تقارير المستخدمين المحفوظة
│
├── test_patient.csv                            # بيانات اختبار جاهزة
└── test_patient.xlsx                           # بيانات اختبار (Excel)
```

---

## 🚀 تشغيل التطبيق | Run the App

### تثبيت المتطلبات | Install Requirements

```bash
pip install -r requirements.txt
```

### التشغيل المحلي | Local Run

```bash
streamlit run app.py
```

ثم افتح المتصفح على | Then open:

```
http://localhost:8501
```

---

## ☁️ النشر على الإنترنت | Deploy Online

أسهل طريقة للنشر هي **Streamlit Community Cloud**:

1. ارفع المشروع على GitHub
2. اذهب إلى [share.streamlit.io](https://share.streamlit.io)
3. استخدم الإعدادات التالية:

| الإعداد | Value |
|---------|-------|
| Repository | `ABDULMALIK0001/VitaVision_Project` |
| Branch | `main` |
| Main file path | `app.py` |

> تأكد من وجود `requirements.txt` و `models/vitavision_unified_model.pkl` في المستودع.

---

## 📊 منطق التصنيف | Classification Logic

```
القيمة < الحد الأدنى                           →  Deficient  (ناقص)
الحد الأدنى ≤ القيمة ≤ الحد الأعلى            →  Normal     (طبيعي)
القيمة > الحد الأعلى                           →  Excessive  (مرتفع)
```

يعرض التطبيق نتيجتين جنباً إلى جنب:
- **نتيجة النطاق المرجعي** — القاعدة الأساسية للتصنيف
- **تنبؤ نموذج ML** — مع نسبة الثقة ومدى التوافق بين النتيجتين

---

## 🏗️ Pipeline الرسمي للبيانات والنمذجة

الملف `data/VitaVision_Colab_Full_Pipeline.ipynb` هو المرجع الرسمي ويقوم بـ:

1. إعادة بناء مجموعة البيانات النظيفة والمصنّفة
2. تطبيق نفس منطق النطاقات المرجعية المستخدم في التطبيق
3. إزالة القيم غير الواقعية أو الخاطئة
4. تدريب النماذج ومقارنتها
5. تصدير ملفات النماذج للاستخدام في Streamlit

> الملفات القديمة في `data/` محفوظة كمرجع لتاريخ التطوير فقط.

---

## ⚠️ إخلاء المسؤولية | Disclaimer

VitaVision هو أداة **تعليمية وتوعوية فقط**. لا يُعتبر بديلاً عن التشخيص الطبي أو الاستشارة أو العلاج. في حال وجود أي أعراض أو نتائج غير طبيعية، يرجى مراجعة طبيب مختص فوراً.

*VitaVision is an educational and awareness tool only. It does not replace medical diagnosis, consultation, or treatment. If you have symptoms or abnormal results, please consult a qualified healthcare professional immediately.*

---

<div align="center">
Made with ❤️ by ABDULMALIK
</div>
