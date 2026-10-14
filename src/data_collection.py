"""
=============================================================================
NOVORA: Intelligent Learning Analytics and Student Success Prediction Framework
Phase 2: Data Collection, Verification, and Exploratory Profiling
=============================================================================
"""

import os
import json
import hashlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def compute_checksum(filepath: str) -> str:
    """Calculate MD5 checksum to verify data integrity."""
    hasher = hashlib.md5()
    with open(filepath, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def load_and_verify_dataset(csv_path: str) -> pd.DataFrame:
    """
    Activity: Import dataset into analytical environment and verify integrity.
    """
    print("=" * 70)
    print(">>> PHASE 2: DATA COLLECTION & VERIFICATION")
    print("=" * 70)

    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Dataset not found at target path: {csv_path}")

    file_size_bytes = os.path.getsize(csv_path)
    checksum = compute_checksum(csv_path)

    print(f"[+] File Location:      {csv_path}")
    print(f"[+] File Size:          {file_size_bytes} bytes ({file_size_bytes / 1024:.2f} KB)")
    print(f"[+] MD5 Integrity Hash: {checksum}")

    # Read dataset
    df = pd.read_csv(csv_path)
    print("[+] Status:             Dataset successfully imported into Pandas DataFrame.")
    return df

def audit_dataset_structure(df: pd.DataFrame) -> dict:
    """
    Activity: Examine dataset dimensions, structure, attribute types, and nulls.
    """
    rows, cols = df.shape
    memory_usage = df.memory_usage(deep=True).sum() / 1024  # in KB
    null_counts = df.isnull().sum().to_dict()
    total_nulls = df.isnull().sum().sum()
    duplicate_count = int(df.duplicated().sum())

    print("\n" + "-" * 70)
    print(">>> 1. DATASET DIMENSIONS & STRUCTURAL AUDIT")
    print("-" * 70)
    print(f"Total Rows (Instances):       {rows}")
    print(f"Total Columns (Features):     {cols}")
    print(f"Total Data Points (Cells):    {rows * cols}")
    print(f"Estimated Memory Footprint:   {memory_usage:.2f} KB")
    print(f"Duplicate Rows Detected:      {duplicate_count}")
    print(f"Total Missing / Null Values:  {total_nulls}")

    print("\nAttribute Breakdown & Schema:")
    schema_info = []
    for col in df.columns:
        dtype = str(df[col].dtype)
        non_null = int(df[col].notnull().sum())
        null_n = int(df[col].isnull().sum())
        n_unique = int(df[col].nunique())
        col_type = "Numeric (Continuous)" if dtype.startswith("float") else ("Numeric (Discrete)" if dtype.startswith("int") else "Categorical")
        schema_info.append({
            "Feature Name": col,
            "Data Type": dtype,
            "Type Category": col_type,
            "Non-Null Count": non_null,
            "Missing Count": null_n,
            "Unique Values": n_unique
        })
        print(f"  * {col:<24} | Type: {dtype:<8} | Non-Null: {non_null}/{rows} | Unique: {n_unique:<4} | Category: {col_type}")

    return {
        "dimensions": {"rows": rows, "columns": cols, "total_elements": rows * cols},
        "memory_usage_kb": round(memory_usage, 2),
        "duplicate_rows": duplicate_count,
        "total_nulls": int(total_nulls),
        "schema": schema_info
    }

def generate_statistical_summaries(df: pd.DataFrame) -> pd.DataFrame:
    """
    Activity: Generate comprehensive descriptive statistical summaries.
    """
    print("\n" + "-" * 70)
    print(">>> 2. DESCRIPTIVE STATISTICAL PROFILING")
    print("-" * 70)

    stats_list = []
    for col in df.select_dtypes(include=[np.number]).columns:
        series = df[col]
        mean_val = series.mean()
        std_val = series.std()
        median_val = series.median()
        mode_val = series.mode().iloc[0] if not series.mode().empty else np.nan
        min_val = series.min()
        q25 = series.quantile(0.25)
        q75 = series.quantile(0.75)
        iqr = q75 - q25
        max_val = series.max()
        range_val = max_val - min_val
        skewness = series.skew()
        kurtosis = series.kurtosis()
        
        # Outlier counts using 1.5 * IQR rule
        lower_bound = q25 - 1.5 * iqr
        upper_bound = q75 + 1.5 * iqr
        outliers = int(((series < lower_bound) | (series > upper_bound)).sum())

        stats_list.append({
            "Feature": col,
            "Count": len(series),
            "Mean": round(mean_val, 3),
            "Std Dev": round(std_val, 3),
            "Median": round(median_val, 3),
            "Mode": round(mode_val, 3),
            "Min": round(min_val, 3),
            "Q25 (25%)": round(q25, 3),
            "Q50 (Median)": round(median_val, 3),
            "Q75 (75%)": round(q75, 3),
            "Max": round(max_val, 3),
            "Range": round(range_val, 3),
            "IQR": round(iqr, 3),
            "Skewness": round(skewness, 3),
            "Kurtosis": round(kurtosis, 3),
            "IQR Outliers": outliers
        })

    summary_df = pd.DataFrame(stats_list)
    print(summary_df.to_string(index=False))
    return summary_df

def compute_correlation_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """Compute Pearson correlation matrix with target variable."""
    corr_matrix = df.corr()
    print("\n" + "-" * 70)
    print(">>> 3. PEARSON CORRELATION MATRIX (Target: Exam_Score)")
    print("-" * 70)
    print(corr_matrix.round(4).to_string())
    return corr_matrix

def generate_visualizations(df: pd.DataFrame, output_dir: str):
    """
    Activity: Render visual distributions, boxplots, correlation heatmap, and scatter plots.
    """
    os.makedirs(output_dir, exist_ok=True)
    sns.set_theme(style="whitegrid", palette="muted")

    # 1. Feature Distributions (Histograms + KDE)
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes = axes.flatten()
    features = list(df.columns)

    colors = ['#1f77b4', '#2ca02c', '#ff7f0e', '#d62728']

    for i, col in enumerate(features):
        ax = axes[i]
        sns.histplot(df[col], kde=True, ax=ax, color=colors[i % len(colors)], edgecolor='black', alpha=0.6)
        ax.set_title(f"Distribution of {col}", fontsize=13, fontweight='bold')
        ax.set_xlabel(col, fontsize=11)
        ax.set_ylabel("Frequency", fontsize=11)
        # Add mean and median vertical lines
        ax.axvline(df[col].mean(), color='red', linestyle='--', linewidth=1.5, label=f"Mean: {df[col].mean():.2f}")
        ax.axvline(df[col].median(), color='green', linestyle=':', linewidth=1.5, label=f"Median: {df[col].median():.2f}")
        ax.legend(loc='upper right')

    plt.suptitle("NOVORA Framework - Phase 2: Feature Distribution Analysis", fontsize=16, fontweight='bold', y=0.98)
    plt.tight_layout()
    dist_path = os.path.join(output_dir, "feature_distributions.png")
    plt.savefig(dist_path, dpi=300)
    plt.close()
    print(f"[+] Saved distribution chart to: {dist_path}")

    # 2. Boxplots for Outlier Detection
    fig, axes = plt.subplots(1, 4, figsize=(16, 5))
    for i, col in enumerate(features):
        sns.boxplot(y=df[col], ax=axes[i], color=colors[i % len(colors)], width=0.4, fliersize=4)
        axes[i].set_title(f"Boxplot: {col}", fontsize=12, fontweight='bold')
        axes[i].set_ylabel(col, fontsize=11)

    plt.suptitle("NOVORA Framework - Phase 2: Outlier Audit & Dispersion Analysis", fontsize=15, fontweight='bold', y=1.02)
    plt.tight_layout()
    box_path = os.path.join(output_dir, "feature_boxplots.png")
    plt.savefig(box_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[+] Saved boxplot chart to: {box_path}")

    # 3. Correlation Heatmap
    plt.figure(figsize=(8, 6))
    corr = df.corr()
    mask = np.triu(np.ones_like(corr, dtype=bool))
    sns.heatmap(corr, annot=True, fmt=".3f", cmap="vlag", vmin=-1, vmax=1, cbar_kws={'label': 'Pearson Correlation'}, linewidths=1)
    plt.title("NOVORA Framework - Feature Correlation Matrix", fontsize=14, fontweight='bold', pad=12)
    plt.tight_layout()
    corr_path = os.path.join(output_dir, "correlation_heatmap.png")
    plt.savefig(corr_path, dpi=300)
    plt.close()
    print(f"[+] Saved correlation heatmap to: {corr_path}")

    # 4. Pairwise Relationship / Scatter with Target
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    predictors = [c for c in df.columns if c != 'Exam_Score']
    for i, col in enumerate(predictors):
        sns.regplot(data=df, x=col, y='Exam_Score', ax=axes[i], scatter_kws={'alpha': 0.6, 'color': colors[i]}, line_kws={'color': 'darkred'})
        axes[i].set_title(f"{col} vs Exam_Score", fontsize=12, fontweight='bold')
        axes[i].set_xlabel(col, fontsize=11)
        axes[i].set_ylabel("Exam_Score", fontsize=11)

    plt.suptitle("NOVORA Framework - Bivariate Association with Academic Target (Exam_Score)", fontsize=15, fontweight='bold', y=1.02)
    plt.tight_layout()
    scatter_path = os.path.join(output_dir, "bivariate_scatterplots.png")
    plt.savefig(scatter_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[+] Saved bivariate scatterplots to: {scatter_path}")

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    data_path = os.path.join(base_dir, "data", "student_performance_data.csv")
    reports_dir = os.path.join(base_dir, "reports")
    figures_dir = os.path.join(reports_dir, "figures")

    os.makedirs(reports_dir, exist_ok=True)
    os.makedirs(figures_dir, exist_ok=True)

    # 1. Load and Verify
    df = load_and_verify_dataset(data_path)

    # 2. Structure & Dimensions Audit
    struct_audit = audit_dataset_structure(df)

    # 3. Descriptive Stats
    stats_df = generate_statistical_summaries(df)

    # 4. Correlation
    corr_df = compute_correlation_matrix(df)

    # 5. Export structured summaries
    stats_df.to_csv(os.path.join(reports_dir, "data_summary.csv"), index=False)
    corr_df.to_csv(os.path.join(reports_dir, "correlation_matrix.csv"))

    audit_export = {
        "project_name": "NOVORA: Intelligent Learning Analytics and Student Success Prediction Framework",
        "phase": "Phase 2 - Data Collection & Ingestion",
        "dataset_file": os.path.basename(data_path),
        "audit_metrics": struct_audit,
        "descriptive_statistics": stats_df.to_dict(orient="records"),
        "correlation_with_target": corr_df["Exam_Score"].to_dict()
    }

    with open(os.path.join(reports_dir, "data_collection_audit.json"), "w") as f:
        json.dump(audit_export, f, indent=4)

    print(f"\n[+] Exported statistical summary: {os.path.join(reports_dir, 'data_summary.csv')}")
    print(f"[+] Exported audit JSON:           {os.path.join(reports_dir, 'data_collection_audit.json')}")

    # 6. Generate Figures
    generate_visualizations(df, figures_dir)

    print("\n" + "=" * 70)
    print(">>> DELIVERABLES VERIFICATION COMPLETE")
    print(f"[+] Deliverable 1: Dataset successfully imported ({df.shape[0]} rows x {df.shape[1]} columns)")
    print(f"[+] Deliverable 2: Dataset dimensions, attributes, and statistical profile documented")
    print("=" * 70)

if __name__ == "__main__":
    main()
