from __future__ import annotations

import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score
from sklearn.model_selection import GroupShuffleSplit
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


RANDOM_STATE = 42
FEATURES = ["Age", "Gender", "Nutrient", "Value"]
TARGET = "Label"
GROUP = "SEQN"
LABEL_ORDER = ["Deficient", "Normal", "Excessive"]


def find_dataset() -> Path:
    candidates = [
        Path("vitavision_final_labeled_dataset.csv"),
        Path("data/vitavision_final_labeled_dataset.csv"),
    ]
    for path in candidates:
        if path.exists():
            return path
    raise FileNotFoundError(
        "Could not find vitavision_final_labeled_dataset.csv. "
        "Run this script from the project root or data folder."
    )


def load_and_standardize(data_path: Path) -> pd.DataFrame:
    df_raw = pd.read_csv(data_path)
    required_columns = ["SEQN", "Age", "Gender", "Nutrient", "Value", "Label"]
    missing_columns = [col for col in required_columns if col not in df_raw.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    df = df_raw[required_columns].copy()
    df["SEQN"] = pd.to_numeric(df["SEQN"], errors="coerce")
    df["Age"] = pd.to_numeric(df["Age"], errors="coerce")
    df["Gender"] = pd.to_numeric(df["Gender"], errors="coerce")
    df["Value"] = pd.to_numeric(df["Value"], errors="coerce")
    df["Nutrient"] = df["Nutrient"].astype(str).str.strip()
    df["Label"] = df["Label"].astype(str).str.strip()

    nutrient_name_map = {
        "Vitamin_D": "Vitamin D",
        "Vitamin_C": "Vitamin C",
        "Vitamin_A": "Vitamin A",
        "Vitamin_E": "Vitamin E",
        "Vitamin_K": "Vitamin K",
        "B12": "Vitamin B12",
        "B6": "Vitamin B6",
    }
    df["Nutrient"] = df["Nutrient"].replace(nutrient_name_map)

    df = df.dropna(subset=required_columns).copy()
    df["SEQN"] = df["SEQN"].astype(int)
    df["Gender"] = df["Gender"].astype(int)
    df = df[df["Label"].isin(LABEL_ORDER)].copy()
    return df


def patient_level_split(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    first_splitter = GroupShuffleSplit(
        n_splits=1,
        test_size=0.20,
        random_state=RANDOM_STATE,
    )
    train_val_idx, test_idx = next(
        first_splitter.split(df, df[TARGET], groups=df[GROUP])
    )

    train_val_df = df.iloc[train_val_idx].reset_index(drop=True)
    test_df = df.iloc[test_idx].reset_index(drop=True)

    second_splitter = GroupShuffleSplit(
        n_splits=1,
        test_size=0.20,
        random_state=RANDOM_STATE,
    )
    train_idx, val_idx = next(
        second_splitter.split(
            train_val_df,
            train_val_df[TARGET],
            groups=train_val_df[GROUP],
        )
    )

    train_df = train_val_df.iloc[train_idx].reset_index(drop=True)
    val_df = train_val_df.iloc[val_idx].reset_index(drop=True)
    return train_df, val_df, test_df


def build_logistic_regression_model() -> Pipeline:
    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), ["Nutrient"]),
            ("num", StandardScaler(), ["Age", "Gender", "Value"]),
        ]
    )

    return Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            (
                "classifier",
                LogisticRegression(
                    max_iter=3000,
                    random_state=RANDOM_STATE,
                    class_weight="balanced",
                ),
            ),
        ]
    )


def build_random_forest_model() -> Pipeline:
    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), ["Nutrient"]),
            ("num", "passthrough", ["Age", "Gender", "Value"]),
        ]
    )

    return Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            (
                "classifier",
                RandomForestClassifier(
                    n_estimators=300,
                    random_state=RANDOM_STATE,
                    class_weight="balanced",
                    n_jobs=-1,
                ),
            ),
        ]
    )


def evaluate(name: str, y_true: pd.Series, y_pred) -> dict[str, float | str]:
    return {
        "split": name,
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "macro_f1": float(f1_score(y_true, y_pred, average="macro")),
    }


def main() -> None:
    data_path = find_dataset()
    df = load_and_standardize(data_path)
    train_df, val_df, test_df = patient_level_split(df)

    X_train, y_train = train_df[FEATURES], train_df[TARGET]
    X_val, y_val = val_df[FEATURES], val_df[TARGET]
    X_test, y_test = test_df[FEATURES], test_df[TARGET]

    baseline = DummyClassifier(strategy="most_frequent", random_state=RANDOM_STATE)
    baseline.fit(X_train, y_train)
    baseline_val_pred = baseline.predict(X_val)

    logistic_model = build_logistic_regression_model()
    logistic_model.fit(X_train, y_train)

    random_forest_model = build_random_forest_model()
    random_forest_model.fit(X_train, y_train)

    logistic_val_pred = logistic_model.predict(X_val)
    logistic_test_pred = logistic_model.predict(X_test)

    rf_val_pred = random_forest_model.predict(X_val)
    rf_test_pred = random_forest_model.predict(X_test)

    baseline_scores = evaluate("validation_baseline", y_val, baseline_val_pred)
    logistic_val_scores = evaluate("validation_logistic_regression", y_val, logistic_val_pred)
    logistic_test_scores = evaluate("test_logistic_regression", y_test, logistic_test_pred)
    rf_val_scores = evaluate("validation_random_forest", y_val, rf_val_pred)
    rf_test_scores = evaluate("test_random_forest", y_test, rf_test_pred)

    model_candidates = [
        {
            "name": "Logistic Regression",
            "model": logistic_model,
            "validation": logistic_val_scores,
            "test": logistic_test_scores,
            "val_pred": logistic_val_pred,
            "test_pred": logistic_test_pred,
        },
        {
            "name": "Random Forest",
            "model": random_forest_model,
            "validation": rf_val_scores,
            "test": rf_test_scores,
            "val_pred": rf_val_pred,
            "test_pred": rf_test_pred,
        },
    ]
    best_candidate = max(
        model_candidates,
        key=lambda candidate: candidate["validation"]["macro_f1"],
    )

    print("Dataset:", data_path.resolve())
    print("Rows:", len(df), "Patients:", df[GROUP].nunique())
    print("Train rows/patients:", len(train_df), train_df[GROUP].nunique())
    print("Validation rows/patients:", len(val_df), val_df[GROUP].nunique())
    print("Test rows/patients:", len(test_df), test_df[GROUP].nunique())
    print()
    print("Baseline:", baseline_scores)
    print("Logistic Regression validation:", logistic_val_scores)
    print("Logistic Regression test:", logistic_test_scores)
    print("Random Forest validation:", rf_val_scores)
    print("Random Forest test:", rf_test_scores)
    print("Selected best model:", best_candidate["name"])
    print()
    print("Logistic Regression validation classification report:")
    print(classification_report(y_val, logistic_val_pred, digits=4))
    print("Logistic Regression test classification report:")
    print(classification_report(y_test, logistic_test_pred, digits=4))
    print("Random Forest validation classification report:")
    print(classification_report(y_val, rf_val_pred, digits=4))
    print("Random Forest test classification report:")
    print(classification_report(y_test, rf_test_pred, digits=4))
    print("Selected model test confusion matrix:")
    print(
        pd.DataFrame(
            confusion_matrix(y_test, best_candidate["test_pred"], labels=LABEL_ORDER),
            index=LABEL_ORDER,
            columns=LABEL_ORDER,
        )
    )

    project_root = Path.cwd()
    if project_root.name == "data":
        model_dir = project_root.parent / "models"
    else:
        model_dir = project_root / "models"
    model_dir.mkdir(parents=True, exist_ok=True)

    logistic_model_path = model_dir / "vitavision_logistic_regression_model.pkl"
    random_forest_model_path = model_dir / "vitavision_random_forest_model.pkl"
    model_path = model_dir / "vitavision_unified_model.pkl"
    metadata_path = model_dir / "vitavision_unified_model_metadata.json"
    comparison_path = model_dir / "vitavision_model_comparison.csv"

    joblib.dump(logistic_model, logistic_model_path)
    joblib.dump(random_forest_model, random_forest_model_path)
    joblib.dump(best_candidate["model"], model_path)

    comparison_df = pd.DataFrame(
        [
            baseline_scores,
            logistic_val_scores,
            logistic_test_scores,
            rf_val_scores,
            rf_test_scores,
        ]
    )
    comparison_df.to_csv(comparison_path, index=False)

    metadata = {
        "model_name": "VitaVision Unified Random Forest",
        "model_file": str(model_path),
        "selected_model": best_candidate["name"],
        "logistic_regression_model_file": str(logistic_model_path),
        "random_forest_model_file": str(random_forest_model_path),
        "model_comparison_file": str(comparison_path),
        "features": FEATURES,
        "target": TARGET,
        "classes": LABEL_ORDER,
        "random_state": RANDOM_STATE,
        "split_strategy": "patient-level GroupShuffleSplit using SEQN",
        "train_rows": int(len(train_df)),
        "validation_rows": int(len(val_df)),
        "test_rows": int(len(test_df)),
        "validation_baseline_accuracy": baseline_scores["accuracy"],
        "validation_baseline_macro_f1": baseline_scores["macro_f1"],
        "logistic_regression_validation_accuracy": logistic_val_scores["accuracy"],
        "logistic_regression_validation_macro_f1": logistic_val_scores["macro_f1"],
        "logistic_regression_test_accuracy": logistic_test_scores["accuracy"],
        "logistic_regression_test_macro_f1": logistic_test_scores["macro_f1"],
        "random_forest_validation_accuracy": rf_val_scores["accuracy"],
        "random_forest_validation_macro_f1": rf_val_scores["macro_f1"],
        "random_forest_test_accuracy": rf_test_scores["accuracy"],
        "random_forest_test_macro_f1": rf_test_scores["macro_f1"],
        "validation_accuracy": best_candidate["validation"]["accuracy"],
        "validation_macro_f1": best_candidate["validation"]["macro_f1"],
        "test_accuracy": best_candidate["test"]["accuracy"],
        "test_macro_f1": best_candidate["test"]["macro_f1"],
        "nutrient_name_convention": "Use names such as Vitamin D, Vitamin B12, Vitamin E, Zinc, Ferritin",
    }
    metadata_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    print()
    print("Saved Logistic Regression model:", logistic_model_path.resolve())
    print("Saved Random Forest model:", random_forest_model_path.resolve())
    print("Saved model:", model_path.resolve())
    print("Saved metadata:", metadata_path.resolve())
    print("Saved comparison:", comparison_path.resolve())


if __name__ == "__main__":
    main()
