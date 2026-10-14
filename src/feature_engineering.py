"""
=============================================================================
NOVORA: Intelligent Learning Analytics and Student Success Prediction Framework
Phase 5: Feature Engineering & Domain-Informed Interaction Modeling
=============================================================================
"""

import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Construct domain-informed behavioral and engagement features.
    """
    df_feat = df.copy()

    # 1. Study Attendance Interaction (Compound exposure & self-study index)
    df_feat["Study_Attendance_Index"] = (df_feat["Study_Hours"] * df_feat["Attendance"]) / 100.0

    # 2. Assignment Completion Proportion (0.0 to 1.0 continuous scale)
    df_feat["Assignment_Rate"] = df_feat["Assignments_Completed"] / 10.0

    # 3. Study and Coursework Diligence Interaction
    df_feat["Study_Assignment_Product"] = df_feat["Study_Hours"] * (df_feat["Assignments_Completed"] + 1)

    return df_feat

def run_feature_engineering():
    print("=" * 70)
    print(">>> PHASE 5: FEATURE ENGINEERING")
    print("=" * 70)

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    data_dir = os.path.join(base_dir, "data")
    reports_dir = os.path.join(base_dir, "reports")
    fig_dir = os.path.join(reports_dir, "figures", "feature_engineering")

    os.makedirs(fig_dir, exist_ok=True)

    # Load unscaled train and test datasets from Phase 3
    train_path = os.path.join(data_dir, "train_data.csv")
    test_path = os.path.join(data_dir, "test_data.csv")

    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)

    print(f"[+] Loaded Train Data: {train_df.shape[0]} rows")
    print(f"[+] Loaded Test Data:  {test_df.shape[0]} rows")

    # Apply feature transformations
    train_feat = engineer_features(train_df)
    test_feat = engineer_features(test_df)

    # Save engineered feature tables
    train_feat_path = os.path.join(data_dir, "train_features.csv")
    test_feat_path = os.path.join(data_dir, "test_features.csv")
    train_feat.to_csv(train_feat_path, index=False)
    test_feat.to_csv(test_feat_path, index=False)
    print(f"[+] Saved train features: {train_feat_path}")
    print(f"[+] Saved test features:  {test_feat_path}")

    # Analyze correlations with Exam_Score on training set
    corr_series = train_feat.corr()["Exam_Score"].sort_values(ascending=False)
    print("\n[+] Correlation with Exam_Score (Training Set):")
    for feat, r in corr_series.items():
        if feat != "Exam_Score":
            print(f"    - {feat:<28}: r = {r:+.4f}")

    # Visualizing Engineered Feature Impact
    plt.figure(figsize=(10, 6))
    features_only = corr_series.drop("Exam_Score")
    colors = ["#2ca02c" if "Index" in f or "Rate" in f or "Product" in f else "#1f77b4" for f in features_only.index]
    ax = sns.barplot(x=features_only.values, y=features_only.index, palette=colors, edgecolor="black")
    plt.title("NOVORA: Feature Relevance with Target Exam Score (Base vs Engineered)", fontsize=13, fontweight="bold")
    plt.xlabel("Pearson Correlation Coefficient (r)")
    for i, v in enumerate(features_only.values):
        ax.text(v + 0.015, i, f"{v:+.3f}", va="center", fontweight="bold", fontsize=10)
    plt.xlim(0, 1.0)
    plt.tight_layout()

    feat_corr_path = os.path.join(fig_dir, "engineered_features_correlation.png")
    plt.savefig(feat_corr_path, dpi=300)
    plt.close()
    print(f"[+] Saved feature correlation chart: {feat_corr_path}")

    # Export summary metadata
    summary = {
        "phase": "Phase 5: Feature Engineering",
        "engineered_features": [
            {
                "name": "Study_Attendance_Index",
                "formula": "(Study_Hours * Attendance) / 100.0",
                "description": "Composite engagement metric combining weekly independent hours with class presence rate.",
                "correlation_with_target": round(float(corr_series["Study_Attendance_Index"]), 4)
            },
            {
                "name": "Assignment_Rate",
                "formula": "Assignments_Completed / 10.0",
                "description": "Normalized assignment completion fraction (0.0 to 1.0).",
                "correlation_with_target": round(float(corr_series["Assignment_Rate"]), 4)
            },
            {
                "name": "Study_Assignment_Product",
                "formula": "Study_Hours * (Assignments_Completed + 1)",
                "description": "Interaction proxy assessing compounded study diligence and coursework practice.",
                "correlation_with_target": round(float(corr_series["Study_Assignment_Product"]), 4)
            }
        ],
        "train_shape": train_feat.shape,
        "test_shape": test_feat.shape
    }

    summary_path = os.path.join(reports_dir, "feature_engineering_summary.json")
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=4)
    print(f"[+] Exported summary JSON: {summary_path}")

    print("\n" + "=" * 70)
    print(">>> PHASE 5 FEATURE ENGINEERING COMPLETED SUCCESSFULLY")
    print("=" * 70)

if __name__ == "__main__":
    run_feature_engineering()
