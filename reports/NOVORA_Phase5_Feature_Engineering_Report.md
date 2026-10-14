# NOVORA: Phase 5 Technical Report — Feature Engineering & Interaction Modeling

## 📌 1. Phase Objective & Rationale
Phase 5 develops domain-informed feature representations to capture non-linear student learning interactions. While individual raw predictors (`Study_Hours`, `Attendance`, `Assignments_Completed`) exhibit strong linear relationships with `Exam_Score`, real-world academic success is compounded when students consistently attend class and dedicate independent study hours outside class.

---

## 🛠️ 2. Engineered Features Formulation

### 2.1 Study-Attendance Compound Index (`Study_Attendance_Index`)
- **Mathematical Formulation:**
  $$\text{Study\_Attendance\_Index} = \frac{\text{Study\_Hours} \times \text{Attendance}}{100.0}$$
- **Domain Rationale:** Independent study time is significantly amplified when paired with high lecture attendance. A student studying 8 hours per week with 95% attendance exhibits deeper mastery than one studying 8 hours while missing half the instructional curriculum.
- **Empirical Result:** Achieved a Pearson correlation of **$r = +0.8506$** with `Exam_Score`, outperforming raw study hours ($r = +0.8182$).

### 2.2 Normalized Assignment Completion Rate (`Assignment_Rate`)
- **Mathematical Formulation:**
  $$\text{Assignment\_Rate} = \frac{\text{Assignments\_Completed}}{10.0}$$
- **Domain Rationale:** Scales discrete assignment counts to a continuous decimal fraction $[0.0, 1.0]$ representing overall coursework completion rate.
- **Empirical Result:** $r = +0.4212$ with target exam score.

### 2.3 Study Diligence & Coursework Interaction (`Study_Assignment_Product`)
- **Mathematical Formulation:**
  $$\text{Study\_Assignment\_Product} = \text{Study\_Hours} \times (\text{Assignments\_Completed} + 1)$$
- **Domain Rationale:** Examines whether active problem-solving coursework multiplies the benefit of self-study hours.
- **Empirical Result:** $r = +0.7737$.

---

## 📊 3. Feature Correlation Comparison (Training Set, $N=320$)

| Feature Name | Type | Formula | Correlation ($r$) |
| :--- | :--- | :--- | :---: |
| **`Study_Attendance_Index`** | **Engineered** | $(\text{Study\_Hours} \times \text{Attendance}) / 100$ | **$+0.8506$** |
| `Study_Hours` | Raw Baseline | $\text{Study\_Hours}$ | $+0.8182$ |
| `Study_Assignment_Product` | Engineered | $\text{Study\_Hours} \times (\text{Assignments} + 1)$ | $+0.7737$ |
| `Assignment_Rate` | Engineered | $\text{Assignments} / 10.0$ | $+0.4212$ |
| `Assignments_Completed` | Raw Baseline | $\text{Assignments\_Completed}$ | $+0.4212$ |
| `Attendance` | Raw Baseline | $\text{Attendance}$ | $+0.2984$ |

---

## 📦 4. Exported Datasets
- `data/train_features.csv`: Full augmented training matrix (320 rows $\times$ 7 columns)
- `data/test_features.csv`: Full augmented testing matrix (80 rows $\times$ 7 columns)
- `reports/figures/feature_engineering/engineered_features_correlation.png`: Bar comparison chart
- `reports/feature_engineering_summary.json`: Parameter metadata
