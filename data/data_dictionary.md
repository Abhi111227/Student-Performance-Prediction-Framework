# NOVORA: Dataset & Feature Dictionary

## 1. Dataset Overview
- **File Name:** `student_performance_data.csv`
- **Location:** `data/student_performance_data.csv`
- **Total Records (Instances):** 400
- **Total Features (Attributes):** 4
- **Missing Values:** 0 (100% complete)
- **Target Variable:** `Exam_Score` (Continuous academic outcome)

---

## 2. Feature Definitions & Schema

| Feature Name | Technical Data Type | Educational Role | Measurement Unit | Value Range (Observed) | Description & Domain Significance |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`Study_Hours`** | `float64` (Continuous) | Independent Predictor (Behavioral) | Hours per week | `1.05` to `9.91` (Mean: `5.45 hrs`) | Represents the average weekly time dedicated by the student to independent self-directed study outside formal lectures. Strong positive indicator of academic diligence. |
| **`Attendance`** | `float64` (Continuous) | Independent Predictor (Engagement) | Percentage (`%`) | `50.54%` to `99.99%` (Mean: `74.99%`) | Measures the percentage of scheduled class sessions attended by the student over the academic semester. Reflects presence and routine exposure to instruction. |
| **`Assignments_Completed`** | `int64` (Discrete) | Independent Predictor (Coursework) | Count (Tasks) | `0` to `10` (Mean: `4.90`) | The number of mandatory or continuous-evaluation assignments completed and submitted on schedule out of a total curriculum quota of 10 tasks. |
| **`Exam_Score`** | `float64` (Continuous) | **Target Variable (Academic Outcome)** | Score / Percentage (`0-100`) | `24.38` to `100.00` (Mean: `67.35`) | The comprehensive final summative examination score earned by the student. Serves as the primary ground truth label for academic success prediction. |

---

## 3. Data Integrity & Validation Checks
- **Null Value Assessment:** All 400 rows contain non-null entries across all features.
- **Range Validity:** All values lie strictly within realistic educational boundaries:
  - `Study_Hours` $\in [0, 24]$
  - `Attendance` $\in [0, 100]$
  - `Assignments_Completed` $\in [0, 10]$
  - `Exam_Score` $\in [0, 100]$
- **Duplication Audit:** 0 duplicate rows detected.
- **Encoding:** Standard UTF-8, comma-separated values.
