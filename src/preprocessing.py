"""
=============================================================================
NOVORA: Intelligent Learning Analytics and Student Success Prediction Framework
Phase 3: Data Preprocessing & Train-Test Partitioning Pipeline
=============================================================================
"""

import os
import json
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler

def run_preprocessing():
    print("=" * 70)
    print(">>> PHASE 3: DATA PREPROCESSING & PARTITIONING")
    print("=" * 70)

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    data_path = os.path.join(base_dir, "data", "student_performance_data.csv")
    models_dir = os.path.join(base_dir, "models")
    reports_dir = os.path.join(base_dir, "reports")
    data_dir = os.path.join(base_dir, "data")

    os.makedirs(models_dir, exist_ok=True)
    os.makedirs(reports_dir, exist_ok=True)

    # 1. Load Data
    df = pd.read_csv(data_path)
    print(f"[+] Loaded raw dataset: {df.shape[0]} rows, {df.shape[1]} columns")

    # 2. Define Features and Target
    feature_cols = ['Study_Hours', 'Attendance', 'Assignments_Completed']
    target_col = 'Exam_Score'

    X = df[feature_cols]
    y = df[target_col]

    # 3. Train-Test Split (80% Train, 20% Test)
    # Fixed random state to ensure exact scientific reproducibility
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42
    )

    print(f"[+] Data Partitioning:")
    print(f"    - Training Set:   {X_train.shape[0]} samples (80.0%)")
    print(f"    - Testing Set:    {X_test.shape[0]} samples (20.0%)")

    # Save unscaled train and test datasets
    train_df = pd.concat([X_train, y_train], axis=1)
    test_df = pd.concat([X_test, y_test], axis=1)

    train_path = os.path.join(data_dir, "train_data.csv")
    test_path = os.path.join(data_dir, "test_data.csv")
    train_df.to_csv(train_path, index=False)
    test_df.to_csv(test_path, index=False)
    print(f"[+] Saved unscaled train data: {train_path}")
    print(f"[+] Saved unscaled test data:  {test_path}")

    # 4. Feature Scaling (StandardScaler - z-score standardization)
    # Strictly fit ONLY on training data to prevent data leakage
    scaler = StandardScaler()
    X_train_scaled = pd.DataFrame(
        scaler.fit_transform(X_train),
        columns=feature_cols,
        index=X_train.index
    )
    X_test_scaled = pd.DataFrame(
        scaler.transform(X_test),
        columns=feature_cols,
        index=X_test.index
    )

    # Save scaler artifact
    scaler_path = os.path.join(models_dir, "scaler.joblib")
    joblib.dump(scaler, scaler_path)
    print(f"[+] Scaler fitted and serialized to: {scaler_path}")

    # Save scaled train and test data
    train_scaled_df = pd.concat([X_train_scaled, y_train], axis=1)
    test_scaled_df = pd.concat([X_test_scaled, y_test], axis=1)

    train_scaled_path = os.path.join(data_dir, "train_scaled.csv")
    test_scaled_path = os.path.join(data_dir, "test_scaled.csv")
    train_scaled_df.to_csv(train_scaled_path, index=False)
    test_scaled_df.to_csv(test_scaled_path, index=False)
    print(f"[+] Saved scaled train data:   {train_scaled_path}")
    print(f"[+] Saved scaled test data:    {test_scaled_path}")

    # 5. Preprocessing Audit Summary
    summary = {
        "phase": "Phase 3: Data Preprocessing",
        "split_ratio": {"train": 0.8, "test": 0.2},
        "random_state": 42,
        "sample_counts": {
            "total": len(df),
            "train": len(X_train),
            "test": len(X_test)
        },
        "features": feature_cols,
        "target": target_col,
        "scaler_type": "StandardScaler",
        "scaler_means": {col: float(mean) for col, mean in zip(feature_cols, scaler.mean_)},
        "scaler_scales": {col: float(scale) for col, scale in zip(feature_cols, scaler.scale_)},
        "train_target_stats": {
            "mean": float(y_train.mean()),
            "std": float(y_train.std()),
            "min": float(y_train.min()),
            "max": float(y_train.max())
        },
        "test_target_stats": {
            "mean": float(y_test.mean()),
            "std": float(y_test.std()),
            "min": float(y_test.min()),
            "max": float(y_test.max())
        }
    }

    summary_path = os.path.join(reports_dir, "preprocessing_summary.json")
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=4)
    print(f"[+] Preprocessing summary exported: {summary_path}")

    print("\n" + "=" * 70)
    print(">>> PHASE 3 PREPROCESSING COMPLETED SUCCESSFULLY")
    print("=" * 70)

if __name__ == "__main__":
    run_preprocessing()
