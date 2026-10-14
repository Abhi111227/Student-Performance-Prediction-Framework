# 🎓 "NOVORA": Intelligent Learning Analytics & Student Success Prediction Framework
## End-to-End Machine Learning Lifecycle Technical Report (Phases 1 — 8)

---

## 📌 Executive Summary
**NOVORA** is an intelligent learning analytics system designed to predict student academic outcomes and provide proactive, data-driven early warnings for at-risk learners. By tracking student engagement—specifically weekly independent study hours, lecture attendance, and continuous coursework completion—the framework replaces retrospective grade tracking with anticipatory guidance.

The project was executed across the complete 8-phase Machine Learning Development Lifecycle (MLDLC):
1. **Phase 1: Problem Understanding** — Educational challenge definition, stakeholder objectives, and regression framing.
2. **Phase 2: Data Collection & Profiling** — Ingestion of 400 verified student records, schema definition, and statistical profiling.
3. **Phase 3: Data Preprocessing & Partitioning** — 80/20 train-test partitioning with zero-leakage `StandardScaler` transformations.
4. **Phase 4: Exploratory Data Analysis (EDA)** — Risk stratification: High Performers (42.25%), Moderate (42.00%), and At Risk (15.75%).
5. **Phase 5: Feature Engineering** — Formulation of interaction indices (`Study_Attendance_Index` achieving $r = +0.8506$).
6. **Phase 6: Model Development** — Parallel training of 6 algorithms (OLS, Ridge, Lasso, Decision Tree, Random Forest, Gradient Boosting).
7. **Phase 7: Model Evaluation & Serialization** — Ordinary Least Squares crowned champion with **Test $R^2 = 0.9064$**, **MAE = $4.03$ points**, and **RMSE = $5.04$ points**.
8. **Phase 8: Web Dashboard & Cloud Deployment** — Interactive analytics dashboard with instant prediction, serverless REST API, and Vercel cloud deployment.

---

## 🎯 1. Phase 1: Problem Understanding

### 1.1 Problem Statement
Educational institutions amass large amounts of behavioral and performance records. However, identifying students who require academic support prior to final summative exams remains difficult. Traditional interventions occur only after poor marks have already been recorded. NOVORA solves this by analyzing continuous behavioral indicators to forecast final exam outcomes early in the semester.

### 1.2 Mathematical Formulation
The task is framed as a supervised regression and risk classification problem:
$$y_i = f(\mathbf{x}_i) + \epsilon_i$$
where $\mathbf{x}_i = [\text{Study\_Hours}, \text{Attendance}, \text{Assignments\_Completed}]^T$, $y_i \in [0, 100]$ is the final `Exam_Score`, and $\epsilon_i \sim \mathcal{N}(0, \sigma^2)$ represents random disturbance.

### 1.3 Success Criteria
- Test $R^2 \ge 0.75$
- Test MAE $\le 6.00$ marks
- High statistical interpretability of model weights for pedagogical counseling.

---

## 📦 2. Phase 2: Data Collection & Integrity Verification

- **Dataset File:** `data/student_performance_data.csv`
- **Total Samples ($N$):** $400$
- **Total Features ($P$):** $4$ ($3$ independent predictors, $1$ target)
- **Integrity MD5:** `8cd90c8c60a66216797a9b7c8f0f67da`
- **Missing Values:** $0$ ($100\%$ completeness)
- **Duplicate Records:** $0$

### Feature Schema & Summary Statistics
| Feature Name | Type | Mean | Std Dev | Min | Median | Max | Correlation with `Exam_Score` |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| `Study_Hours` | float64 | 5.45 | 2.64 | 1.05 | 5.61 | 9.91 | **+0.8088** |
| `Attendance` | float64 | 74.99 | 14.69 | 50.54 | 75.16 | 99.99 | **+0.3161** |
| `Assignments_Completed` | int64 | 4.90 | 3.21 | 0.00 | 5.00 | 10.00 | **+0.4229** |
| **`Exam_Score` (Target)** | float64 | 67.35 | 16.33 | 24.38 | 66.89 | 100.00 | **1.0000** |

---

## ⚙️ 3. Phase 3: Data Preprocessing & Partitioning

To safeguard against data leakage:
- The raw dataset was partitioned into **$320$ training instances ($80\%$)** and **$80$ unseen testing instances ($20\%$)** using `random_state=42`.
- Standardization was fitted strictly on the training partition:
  $$\mu = [5.48, 74.91, 4.93], \quad \sigma = [2.61, 14.84, 3.20]$$
- Standardized matrices were exported to `data/train_scaled.csv` and `data/test_scaled.csv`.

---

## 🔬 4. Phase 4: Exploratory Data Analysis (EDA)

Students were categorized into three actionable academic tiers:
- **High Performers ($\ge 70.0\%$):** $169$ students ($42.25\%$) — Average study hours: $7.51\text{ hrs/wk}$.
- **Moderate Cohort ($50.0\% - 69.9\%$):** $168$ students ($42.00\%$) — Average study hours: $5.02\text{ hrs/wk}$.
- **At Risk Cohort ($< 50.0\%$):** $63$ students ($15.75\%$) — Average study hours: $2.61\text{ hrs/wk}$.

Key insight: Chronic study deficits ($< 3.5\text{ hrs/week}$) combined with attendance $< 65\%$ yields a $> 88\%$ probability of falling into the at-risk category.

---

## 🛠️ 5. Phase 5: Feature Engineering

Three composite features were engineered and validated:
1. **`Study_Attendance_Index` = $(\text{Study\_Hours} \times \text{Attendance}) / 100$**: Captured compound exposure; correlation with `Exam_Score` rose to **$r = +0.8506$**.
2. **`Assignment_Rate` = $\text{Assignments\_Completed} / 10.0$**: Continuous completion fraction ($r = +0.4212$).
3. **`Study_Assignment_Product` = $\text{Study\_Hours} \times (\text{Assignments} + 1)$**: Diligence multiplier ($r = +0.7737$).

---

## 🏆 6. Phase 6 & 7: Model Benchmarking & Evaluation

Six algorithms were trained and evaluated on the held-out test partition ($N=80$):

| Rank | Model Name | Test $R^2$ | Adjusted $R^2$ | Test MAE | Test RMSE | 5-Fold CV $R^2$ | Status |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| 🥇 | **Linear Regression (OLS)** | **$0.9064$** | **$0.9027$** | **$4.0298$** | **$5.0432$** | **$0.8984 \pm 0.015$** | **Champion Model** |
| 🥈 | **Ridge Regression ($L_2$)** | $0.9064$ | $0.9027$ | $4.0306$ | $5.0436$ | $0.8984 \pm 0.015$ | Regularized Baseline |
| 🥉 | **Lasso Regression ($L_1$)** | $0.9062$ | $0.9025$ | $4.0390$ | $5.0500$ | $0.8984 \pm 0.015$ | Sparse Baseline |
| 4 | **Gradient Boosting Regressor** | $0.8663$ | $0.8610$ | $4.7634$ | $6.0291$ | $0.8681 \pm 0.012$ | Ensemble Boosting |
| 5 | **Random Forest Regressor** | $0.8499$ | $0.8440$ | $5.0829$ | $6.3867$ | $0.8532 \pm 0.016$ | Ensemble Bagging |
| 6 | **Decision Tree Regressor** | $0.7758$ | $0.7669$ | $6.1485$ | $7.8065$ | $0.7804 \pm 0.040$ | Non-linear Tree |

### Champion Model Equation & Weights
$$\widehat{\text{Exam\_Score}} = 3.4209 + 4.7639 \cdot \text{Study\_Hours} + 0.3795 \cdot \text{Attendance} + 1.9669 \cdot \text{Assignments\_Completed}$$

- **Intercept ($3.42$):** Baseline minimum outcome without study or attendance.
- **$\beta_{\text{Study\_Hours}} = +4.76$:** Each additional weekly study hour contributes $+4.76$ points.
- **$\beta_{\text{Attendance}} = +0.38$:** Every $10\%$ increase in attendance contributes $+3.80$ points.
- **$\beta_{\text{Assignments}} = +1.97$:** Each submitted assignment contributes $+1.97$ points.

---

## 🌐 7. Phase 8: Web Dashboard & Vercel Deployment

An interactive single-page web platform was developed and configured for Vercel:
- **Interactive Prediction Studio:** Instant recalculation using reactive sliders.
- **Serverless REST API:** `/api/predict` endpoint serving predictions with CORS support.
- **Leaderboard API:** `/api/leaderboard` serving algorithmic benchmarks in JSON format.
- **Visual Analytics Viewer:** In-app inspection of all generated diagrams and heatmaps.
- **Zero-Latency In-Browser Execution:** Client-side formula evaluation alongside cloud API fallback.

---

## 📋 Summary of Project Deliverables

| Deliverable | Location | Description |
| :--- | :--- | :--- |
| **Primary Dataset** | `data/student_performance_data.csv` | 400 records, 4 attributes, verified checksum |
| **Data Dictionary** | `data/data_dictionary.md` | Feature metadata and measurement units |
| **Ingestion Pipeline** | `src/data_collection.py` | Automated dataset ingestion & audit script |
| **Preprocessing Pipeline** | `src/preprocessing.py` | Train-test partitioning & scaler serialization |
| **EDA Engine** | `src/eda.py` | Risk stratification & cohort visualizer |
| **Feature Engineering** | `src/feature_engineering.py` | Interaction indices and correlation analyzer |
| **Model Training & Benchmarking** | `src/model_training.py` | 6-model cross-validated training suite |
| **Champion Model Weights** | `models/model_parameters.json` | Exact equation parameters for inference |
| **Serialized Model** | `models/best_model.joblib` | Scikit-learn serialized pipeline |
| **Interactive Web Application** | `public/index.html` | Responsive single-page analytics dashboard |
| **Vercel Serverless Function** | `api/predict.js` | REST endpoint for automated predictions |
| **Vercel Deployment Spec** | `vercel.json` | Production deployment configuration |
| **End-to-End Jupyter Notebook** | `notebooks/NOVORA_Phase1_Phase2_Data_Collection.ipynb` | Executable analytical walkthrough |
| **Git Version Control** | `.git/` | 5 discrete, semantic per-phase commits |
