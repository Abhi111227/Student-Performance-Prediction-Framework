"""
=============================================================================
NOVORA: Intelligent Learning Analytics and Student Success Prediction Framework
Phase 6 & Phase 7: Multi-Model Development, Benchmarking & Evaluation
=============================================================================
"""

import os
import json
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import cross_val_score
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

def adjusted_r2(r2: float, n: int, p: int) -> float:
    """Calculate Adjusted R-Squared."""
    if n - p - 1 <= 0:
        return r2
    return 1 - (1 - r2) * (n - 1) / (n - p - 1)

def run_model_training():
    print("=" * 70)
    print(">>> PHASE 6 & 7: MODEL TRAINING & RIGOROUS BENCHMARKING")
    print("=" * 70)

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    data_dir = os.path.join(base_dir, "data")
    models_dir = os.path.join(base_dir, "models")
    reports_dir = os.path.join(base_dir, "reports")
    fig_dir = os.path.join(reports_dir, "figures", "models")

    os.makedirs(models_dir, exist_ok=True)
    os.makedirs(fig_dir, exist_ok=True)

    # 1. Load Data
    train_df = pd.read_csv(os.path.join(data_dir, "train_data.csv"))
    test_df = pd.read_csv(os.path.join(data_dir, "test_data.csv"))

    feature_cols = ['Study_Hours', 'Attendance', 'Assignments_Completed']
    target_col = 'Exam_Score'

    X_train = train_df[feature_cols]
    y_train = train_df[target_col]
    X_test = test_df[feature_cols]
    y_test = test_df[target_col]

    n_test = len(y_test)
    p = len(feature_cols)

    # 2. Define Model Portfolio
    models = {
        "Linear Regression (OLS)": LinearRegression(),
        "Ridge Regression (L2)": Ridge(alpha=1.0, random_state=42),
        "Lasso Regression (L1)": Lasso(alpha=0.1, random_state=42),
        "Decision Tree Regressor": DecisionTreeRegressor(max_depth=5, random_state=42),
        "Random Forest Regressor": RandomForestRegressor(n_estimators=100, max_depth=6, random_state=42),
        "Gradient Boosting Regressor": GradientBoostingRegressor(n_estimators=100, learning_rate=0.05, max_depth=3, random_state=42)
    }

    # 3. Benchmark Models
    results = []
    trained_models = {}
    test_predictions = {}

    for name, model in models.items():
        # Train model
        model.fit(X_train, y_train)
        trained_models[name] = model

        # Predict
        y_train_pred = model.predict(X_train)
        y_test_pred = model.predict(X_test)
        test_predictions[name] = y_test_pred

        # Metrics
        train_r2 = r2_score(y_train, y_train_pred)
        test_r2 = r2_score(y_test, y_test_pred)
        adj_r2 = adjusted_r2(test_r2, n_test, p)
        mae = mean_absolute_error(y_test, y_test_pred)
        mse = mean_squared_error(y_test, y_test_pred)
        rmse = np.sqrt(mse)

        # 5-Fold Cross Validation on Train Split
        cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring="r2")
        cv_mean = cv_scores.mean()
        cv_std = cv_scores.std()

        results.append({
            "Model": name,
            "Train R2": round(train_r2, 4),
            "Test R2": round(test_r2, 4),
            "Adjusted R2": round(adj_r2, 4),
            "MAE": round(mae, 4),
            "MSE": round(mse, 4),
            "RMSE": round(rmse, 4),
            "5-Fold CV R2 (Mean)": round(cv_mean, 4),
            "CV Std": round(cv_std, 4)
        })

    leaderboard_df = pd.DataFrame(results).sort_values(by="Test R2", ascending=False)
    print("\n" + "-" * 70)
    print(">>> MODEL PERFORMANCE LEADERBOARD (Sorted by Test R2)")
    print("-" * 70)
    print(leaderboard_df.to_string(index=False))

    # Save leaderboard
    leaderboard_csv = os.path.join(reports_dir, "model_leaderboard.csv")
    leaderboard_json = os.path.join(reports_dir, "model_leaderboard.json")
    leaderboard_df.to_csv(leaderboard_csv, index=False)
    leaderboard_df.to_json(leaderboard_json, orient="records", indent=4)
    print(f"\n[+] Exported leaderboard to: {leaderboard_csv}")

    # 4. Identify Best Performing Model
    best_model_name = leaderboard_df.iloc[0]["Model"]
    best_model = trained_models[best_model_name]
    best_metrics = leaderboard_df.iloc[0].to_dict()
    print(f"\n[+] Best Selected Model: {best_model_name} (Test R2: {best_metrics['Test R2']:.4f}, RMSE: {best_metrics['RMSE']:.4f})")

    # Serialize Best Model
    best_model_path = os.path.join(models_dir, "best_model.joblib")
    joblib.dump(best_model, best_model_path)
    print(f"[+] Serialized best model to: {best_model_path}")

    # Extract Linear Regression formula coefficients for client-side instant execution
    lr_model = trained_models["Linear Regression (OLS)"]
    model_params = {
        "best_model_name": best_model_name,
        "features": feature_cols,
        "intercept": float(lr_model.intercept_),
        "coefficients": {
            col: float(coef) for col, coef in zip(feature_cols, lr_model.coef_)
        },
        "formula": f"Exam_Score = {lr_model.intercept_:.4f} + ({lr_model.coef_[0]:.4f} * Study_Hours) + ({lr_model.coef_[1]:.4f} * Attendance) + ({lr_model.coef_[2]:.4f} * Assignments_Completed)",
        "metrics": best_metrics
    }

    params_path = os.path.join(models_dir, "model_parameters.json")
    with open(params_path, "w") as f:
        json.dump(model_params, f, indent=4)
    print(f"[+] Saved model parameter dictionary: {params_path}")
    print(f"    Mathematical Formula: {model_params['formula']}")

    # 5. Generate High-Quality Visualizations
    # Plot 1: Model Test R2 Comparison
    plt.figure(figsize=(10, 5))
    bars = plt.barh(leaderboard_df["Model"], leaderboard_df["Test R2"], color="#1f77b4", edgecolor="black")
    plt.title("NOVORA Framework: Model Test R² Benchmark", fontsize=13, fontweight="bold")
    plt.xlabel("Coefficient of Determination (R²)")
    plt.xlim(0, 1.0)
    for bar in bars:
        w = bar.get_width()
        plt.text(w + 0.015, bar.get_y() + bar.get_height() / 2, f"R² = {w:.4f}", va="center", fontweight="bold", fontsize=10)
    plt.tight_layout()
    r2_plot_path = os.path.join(fig_dir, "model_r2_comparison.png")
    plt.savefig(r2_plot_path, dpi=300)
    plt.close()
    print(f"[+] Saved R2 comparison plot: {r2_plot_path}")

    # Plot 2: MAE and RMSE Comparison
    fig, ax = plt.subplots(figsize=(11, 5))
    x = np.arange(len(leaderboard_df))
    width = 0.35
    ax.bar(x - width/2, leaderboard_df["MAE"], width, label="MAE", color="#ff7f0e", edgecolor="black")
    ax.bar(x + width/2, leaderboard_df["RMSE"], width, label="RMSE", color="#d62728", edgecolor="black")
    ax.set_ylabel("Error Metric (Exam Points)")
    ax.set_title("NOVORA Framework: Error Metrics Comparison (MAE vs RMSE)", fontsize=13, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(leaderboard_df["Model"], rotation=15, ha="right", fontsize=9)
    ax.legend()
    plt.tight_layout()
    err_plot_path = os.path.join(fig_dir, "model_mae_rmse_comparison.png")
    plt.savefig(err_plot_path, dpi=300)
    plt.close()
    print(f"[+] Saved MAE/RMSE plot: {err_plot_path}")

    # Plot 3: Actual vs Predicted (Best Model)
    best_pred = test_predictions[best_model_name]
    plt.figure(figsize=(7, 7))
    plt.scatter(y_test, best_pred, color="#2ca02c", alpha=0.7, edgecolors="k", s=50, label="Student Predictions")
    # Reference perfect prediction line
    min_val = min(y_test.min(), best_pred.min())
    max_val = max(y_test.max(), best_pred.max())
    plt.plot([min_val, max_val], [min_val, max_val], 'r--', lw=2, label="Ideal 1:1 Identity Line")
    plt.title(f"Actual vs Predicted Exam Score ({best_model_name})", fontsize=13, fontweight="bold")
    plt.xlabel("Actual Exam Score (%)", fontsize=11)
    plt.ylabel("Predicted Exam Score (%)", fontsize=11)
    plt.legend(loc="upper left")
    plt.tight_layout()
    act_plot_path = os.path.join(fig_dir, "actual_vs_predicted_best_model.png")
    plt.savefig(act_plot_path, dpi=300)
    plt.close()
    print(f"[+] Saved actual vs predicted plot: {act_plot_path}")

    # Plot 4: Residuals Distribution (Best Model)
    residuals = y_test - best_pred
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    axes[0].scatter(best_pred, residuals, color="#1f77b4", alpha=0.7, edgecolors="k")
    axes[0].axhline(0, color="red", linestyle="--", lw=1.5)
    axes[0].set_title("Residuals vs Fitted Values (Homoscedasticity Check)", fontweight="bold")
    axes[0].set_xlabel("Fitted Values (Predicted Exam Score)")
    axes[0].set_ylabel("Residuals (Actual - Predicted)")

    sns.histplot(residuals, kde=True, ax=axes[1], color="#9467bd", edgecolor="black")
    axes[1].axvline(0, color="red", linestyle="--", lw=1.5)
    axes[1].set_title("Residuals Distribution (Normality Check)", fontweight="bold")
    axes[1].set_xlabel("Residual Error")

    plt.suptitle(f"Residual Diagnostic Suite ({best_model_name})", fontsize=14, fontweight="bold", y=1.02)
    plt.tight_layout()
    res_plot_path = os.path.join(fig_dir, "residual_plot_best_model.png")
    plt.savefig(res_plot_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"[+] Saved residual diagnostics plot: {res_plot_path}")

    print("\n" + "=" * 70)
    print(">>> PHASE 6 & 7 MODEL TRAINING & EVALUATION COMPLETED")
    print("=" * 70)

if __name__ == "__main__":
    run_model_training()
