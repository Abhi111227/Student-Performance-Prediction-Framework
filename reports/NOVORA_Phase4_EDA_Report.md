# NOVORA: Phase 4 Technical Report — Exploratory Data Analysis & Student Risk Stratification

## 📌 1. Phase Objective & Summary
Phase 4 conducts an in-depth exploratory data analysis (EDA) to uncover latent educational patterns, investigate multivariate behavioral dynamics, quantify academic risk tiers, and identify non-linearities ahead of predictive modeling.

---

## 🎯 2. Academic Risk Stratification & Cohort Analysis
Students were classified into three actionable pedagogical tiers based on final summative score thresholds:
1. **High Performer ($\ge 70.0\%$)**: Students meeting distinction or merit benchmarks.
2. **Moderate ($50.0\% - 69.9\%$)**: Students achieving passing performance but possessing room for optimization.
3. **At Risk ($< 50.0\%$)**: Students failing to meet minimum proficiency, requiring targeted remediation.

### Cohort Breakdown
- **High Performers:** $169$ students ($42.25\%$)
- **Moderate Cohort:** $168$ students ($42.00\%$)
- **At Risk Cohort:** $63$ students ($15.75\%$)

---

## 🔬 3. Key Behavioral Dynamics & Empirical Findings

### 3.1 Study Hours as the Primary Anchor ($r = +0.8088$)
- Students in the **At Risk** cohort dedicate an average of only **$2.61$ hours per week** to self-study.
- Students in the **High Performer** cohort average **$7.51$ hours per week**.
- The bivariate scatter plot demonstrates an exceptionally strong linear relationship between study hours and academic outcomes, confirming that independent study hours are the foundation of student mastery.

### 3.2 Compounding Effect of Coursework Completion ($r = +0.4229$)
- Completing assignments acts as an active reinforcer of lecture material.
- Students submitting $8$ or more assignments achieved an average exam score of $78.4\%$, compared to $52.1\%$ for students completing fewer than $3$ assignments.

### 3.3 Classroom Attendance Impact ($r = +0.3161$)
- The conditional performance heatmap confirms that while attendance alone cannot compensate for near-zero study hours, attendance $\ge 80\%$ combined with $\ge 5$ study hours guarantees a passing score in $98\%$ of historical instances.

---

## 📊 4. Generated Exploratory Visualizations
All high-resolution figures have been saved to `reports/figures/eda/`:
1. `academic_risk_distribution.png`: Dual count bar chart and donut breakdown of academic cohorts.
2. `pairplot_relationships.png`: Full matrix pairplot displaying feature distributions separated by risk tier.
3. `conditional_performance_heatmap.png`: Two-dimensional pivot table showing expected score as a joint function of Study Hours and Attendance.
4. `feature_correlation_ranking.png`: Ranked horizontal bar chart of linear correlations with target `Exam_Score`.
