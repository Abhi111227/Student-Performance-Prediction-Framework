# 🎓 "NOVORA": Intelligent Learning Analytics & Student Success Prediction Framework

A Machine Learning-based predictive analytics system engineered to forecast student academic performance and support data-driven pedagogical interventions.

---

## 📌 Project Overview
The Student Performance Prediction System ("NOVORA") follows the complete **Machine Learning Development Lifecycle (MLDLC)** to model academic performance from historical educational and behavioral attributes:
1. **Phase 1: Problem Understanding** `[COMPLETED]`
2. **Phase 2: Data Collection & Profiling** `[COMPLETED]`
3. **Phase 3: Data Preprocessing**
4. **Phase 4: Exploratory Data Analysis (EDA)**
5. **Phase 5: Feature Engineering**
6. **Phase 6: Model Development**
7. **Phase 7: Model Evaluation**
8. **Phase 8: Model Deployment & Monitoring**

---

## 📂 Project Repository Structure
```
Projectt/
├── data/
│   ├── student_performance_data.csv        # Primary dataset (400 samples, 4 features)
│   └── data_dictionary.md                  # Comprehensive schema and feature dictionary
├── notebooks/
│   └── NOVORA_Phase1_Phase2_Data_Collection.ipynb  # Interactive walkthrough notebook
├── reports/
│   ├── NOVORA_Phase1_Phase2_Report.md      # Detailed academic and engineering report
│   ├── data_summary.csv                    # Descriptive statistics export
│   ├── correlation_matrix.csv              # Pearson correlation matrix
│   ├── data_collection_audit.json          # Machine-readable audit output
│   └── figures/
│       ├── feature_distributions.png       # Histograms and KDE curves
│       ├── feature_boxplots.png            # Boxplots for outlier inspection
│       ├── correlation_heatmap.png         # Pearson correlation heatmap
│       └── bivariate_scatterplots.png      # Scatterplots vs Exam_Score
├── src/
│   └── data_collection.py                  # Automated ingestion & profiling pipeline
└── README.md                               # Project documentation
```

---

## 🎯 Phase 1: Problem Understanding
- **Objective:** Build an intelligent ML model capable of predicting student academic performance (`Exam_Score`).
- **Predictive Factors:**
  - `Study_Hours`: Weekly independent study hours
  - `Attendance`: Semester class attendance percentage
  - `Assignments_Completed`: Completed coursework assignments (out of 10)
  - `Exam_Score`: Summative academic outcome (0-100 scale)
- **Expected Outcome:** Accurate performance forecasting, early risk detection, and proactive intervention support.

---

## 📦 Phase 2: Data Collection & Deliverables

### ✅ Deliverable 1: Dataset Successfully Imported
- **File:** `data/student_performance_data.csv`
- **File Size:** 7,578 bytes (7.40 KB)
- **Integrity Hash (MD5):** `8cd90c8c60a66216797a9b7c8f0f67da`

### ✅ Deliverable 2: Dataset Dimensions Documented
- **Sample Count (Rows):** `400` instances
- **Feature Count (Columns):** `4` columns (`Study_Hours`, `Attendance`, `Assignments_Completed`, `Exam_Score`)
- **Total Data Points:** `1,600`
- **Completeness:** `100%` (0 missing values, 0 duplicate records, 0 outliers)

### Statistical Highlights
| Feature | Type | Mean | Std Dev | Min | Median | Max | Correlation with `Exam_Score` |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| `Study_Hours` | float64 | 5.45 | 2.64 | 1.05 | 5.61 | 9.91 | **+0.8088** |
| `Attendance` | float64 | 74.99 | 14.69 | 50.54 | 75.16 | 99.99 | **+0.3161** |
| `Assignments_Completed` | int64 | 4.90 | 3.21 | 0.00 | 5.00 | 10.00 | **+0.4229** |
| `Exam_Score` *(Target)* | float64 | 67.35 | 16.33 | 24.38 | 66.89 | 100.00 | **1.0000** |

---

## 🚀 How to Run

### 1. Execute the Data Collection & Profiling Pipeline
```bash
python src/data_collection.py
```
This script will re-verify the dataset, calculate all statistical metrics, export `reports/data_summary.csv` and `reports/data_collection_audit.json`, and regenerate all plots in `reports/figures/`.

### 2. Launch the Interactive Notebook
Open `notebooks/NOVORA_Phase1_Phase2_Data_Collection.ipynb` in VSCode, Jupyter Notebook, or JupyterLab.
