# NOVORA: Phase 3 Technical Report — Data Preprocessing & Partitioning

## 📌 1. Phase Objective & Overview
Phase 3 establishes an empirical data preparation pipeline to ensure models are trained on representative data without risk of data leakage. 

Key activities include:
1. Validating raw dataset integrity and bounds.
2. Establishing an $80/20$ train-test split ($320$ training instances, $80$ evaluation instances).
3. Implementing feature scaling (Standardization / Z-score normalization) fitted strictly on training data.
4. Serializing preprocessed datasets and the fitted `StandardScaler` artifact.

---

## ⚙️ 2. Methodology & Leakage Prevention Strategy
In supervised machine learning, data leakage occurs when information from the evaluation dataset influences preprocessing transformations. 

To eliminate leakage:
- **Partitioning Precedes Transformation:** The dataset is split into training ($80\%$) and testing ($20\%$) subsets using a fixed pseudo-random seed (`random_state=42`).
- **Strict In-Sample Fitting:** Feature transformation parameters (mean $\mu$ and standard deviation $\sigma$) are estimated **exclusively** on the training partition:
  $$z = \frac{x - \mu_{\text{train}}}{\sigma_{\text{train}}}$$
- **Out-of-Sample Transformation:** The test split is transformed using the stored $\mu_{\text{train}}$ and $\sigma_{\text{train}}$ without re-estimating any parameters.

---

## 📊 3. Partitioning Statistics

| Attribute | Full Dataset ($N=400$) | Training Partition ($N_{\text{train}}=320$) | Testing Partition ($N_{\text{test}}=80$) |
| :--- | :---: | :---: | :---: |
| **`Study_Hours` (Mean $\pm$ Std)** | $5.45 \pm 2.64$ | $5.48 \pm 2.61$ | $5.32 \pm 2.78$ |
| **`Attendance` (Mean $\pm$ Std)** | $74.99\% \pm 14.69\%$ | $74.91\% \pm 14.86\%$ | $75.29\% \pm 14.07\%$ |
| **`Assignments_Completed` (Mean $\pm$ Std)** | $4.90 \pm 3.21$ | $4.93 \pm 3.20$ | $4.78 \pm 3.26$ |
| **`Exam_Score` (Mean $\pm$ Std)** | $67.35 \pm 16.33$ | $67.61 \pm 16.14$ | $66.30 \pm 17.15$ |

> **Validation Note:** The means and standard deviations across both splits demonstrate strong statistical alignment, confirming that random partitioning maintained unbiased target and predictor distributions.

---

## 📦 4. Serialized Artifacts
- `data/train_data.csv`: Unscaled training data (320 rows)
- `data/test_data.csv`: Unscaled testing data (80 rows)
- `data/train_scaled.csv`: Standardized training features with target
- `data/test_scaled.csv`: Standardized test features with target
- `models/scaler.joblib`: Serialized `StandardScaler` object for inference
- `reports/preprocessing_summary.json`: Metadata and transformation logs
