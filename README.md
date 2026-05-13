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

The app keeps predefined reference ranges in `app.py` as the primary classification logic.

- Below the lower reference limit: `Deficient`
- Between the lower and upper reference limits: `Normal`
- Above the upper reference limit: `Excessive`

The Streamlit app also loads the trained unified model from `models/vitavision_unified_model.pkl` and adds ML comparison columns to each analysis result:

- `ML Prediction`
- `ML Confidence`
- `Model Agreement`

This lets the app show the reference-range status and the trained model prediction side by side.

## Official Modeling Pipeline

The official data preparation and modeling workflow is `data/VitaVision_Colab_Full_Pipeline.ipynb`.

It rebuilds the cleaned/labeled dataset, applies the same reference-range logic used by the app, removes invalid or unrealistic values from the modeling dataset, trains and compares models, and exports the model artifacts for use in Streamlit.

Older notebooks in `data/` are kept as development history and references, but the full pipeline notebook is the version to use for the final project, report, and presentation.

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

## Deploy Online

The simplest hosting option is Streamlit Community Cloud.

Use these settings:

- Repository: `ABDULMALIK0001/VitaVision_Project`
- Branch: `main`
- Main file path: `app.py`

The app requires `requirements.txt` and `models/vitavision_unified_model.pkl` to be present in the repository.

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
