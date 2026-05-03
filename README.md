# VitaVision

VitaVision is a Streamlit-based decision-support web app for interpreting vitamin and mineral laboratory results. It helps users enter lab values manually or by CSV, compare values with predefined medical reference ranges, and view clear classifications, explanations, possible causes, recommendations, and visual summaries.

## Features

- Manual input for lab values
- CSV upload support
- Bilingual interface: English and Arabic
- Dark and light mode
- Classification into Deficient, Normal, or Excessive
- Reference range visualization
- Result summaries and downloadable CSV output

## Current Decision Logic

The current app classifies results using predefined reference ranges in `app.py`.

- Below the lower reference limit: `Deficient`
- Between the lower and upper reference limits: `Normal`
- Above the upper reference limit: `Excessive`

Model files may exist in the project, but the current Streamlit app does not yet use a trained machine learning model for prediction.

## Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the App

From the project folder, run:

```bash
streamlit run app.py
```

Then open the local URL shown in the terminal, usually:

```text
http://localhost:8501
```

## Project Structure

```text
VitaVision_Project/
  app.py
  requirements.txt
  README.md
  data/
  models/
  test_patient.csv
  test_patient.xlsx
```

## Disclaimer

VitaVision is an educational and decision-support tool. It does not replace medical diagnosis or professional healthcare advice.
