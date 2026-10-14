# 🎓 "NOVORA": Intelligent Learning Analytics & Student Success Prediction Framework
## Enterprise Educational Predictive Intelligence Platform (v2.0)

A machine learning-driven learning analytics platform engineered to forecast student academic performance (`Exam_Score`), evaluate value-add growth trajectory from prior assessment marks, and deliver targeted pedagogical intervention roadmaps.

---

## 📌 Project Overview & Architecture

NOVORA follows the complete **Machine Learning Development Lifecycle (MLDLC)** and provides an enterprise-ready educational web application for educators, students, and academic leaders:

```
┌─────────────────────────────────────────────────────────────┐
│                   NOVORA Learning Platform                  │
├──────────────────────────────┬──────────────────────────────┤
│ 🔮 Prediction Studio         │ Direct inputs, Marks Obtained│
│                              │ Value-Add Trajectory & Gaps  │
├──────────────────────────────┼──────────────────────────────┤
│ 📊 Cohort Analytics          │ Real 400-student dataset KPIs│
│                              │ Chart.js scatter & histogram │
├──────────────────────────────┼──────────────────────────────┤
│ 📚 Subject-Wise Insights     │ 5 Academic courses & benchmarks│
├──────────────────────────────┼──────────────────────────────┤
│ 📈 Prediction History        │ localStorage tracking & CSV  │
├──────────────────────────────┼──────────────────────────────┤
│ 🎯 Action Roadmaps           │ 4-Week structured plans      │
└──────────────────────────────┴──────────────────────────────┘
```

---

## 🚀 Key Modules & Capabilities

### 1. 🔮 Prediction Studio (Core Hub)
- **Direct Manual Data Input:** Type numerical values directly for:
  - **Student Identifier / Name**
  - **Subject / Course Selection**
  - **Marks Obtained** *(Continuous Internal / Mid-Term Evaluation Marks out of 100)*
  - **Weekly Self-Study Hours** *(0 – 24 hrs)*
  - **Class Attendance Rate** *(0 – 100%)*
  - **Assignments Completed** *(0 – 10 tasks)*
- **Integrated Prediction Workflow:**
  - Evaluates both historical assessment baseline ($M$) and current behavioral engagement velocity ($S, A, C$).
  - **Value-Add Trajectory ($\Delta$):** Shows whether the student is accelerating ($+8.5\text{ pts}$), holding steady, or exhibiting an at-risk decline relative to their midterm marks.
  - **Target Gap Analysis:** Computes the exact additional study hours ($+1.4\text{ hrs}$) or assignment submissions ($+2\text{ tasks}$) needed to reach the next grade threshold (Passing, Merit, Distinction).
  - Quick-fill archetypes: `[ ⚠️ At-Risk ]`, `[ 👤 Average ]`, `[ ⭐ Top Scorer ]`.

### 2. 📊 Cohort & Performance Analytics
- **Empirical Dataset KPIs:** Powered by the real 400 student dataset:
  - Cohort Volume: $400$ verified records ($100\%$ complete)
  - Historical Mean Score: $67.35\%$ (Std Dev: $16.33$ pts)
  - Cohort Pass Rate: $84.25\%$ ($337$ of $400$ students $\ge 50\%$)
  - Distinction Rate: $42.25\%$ ($169$ of $400$ students $\ge 70\%$)
- **Interactive Visualizations:**
  - **Grade Distribution Chart:** High Performers ($42.25\%$), Moderate ($42.0\%$), At Risk ($15.75\%$).
  - **Live Scatter Plot with Active Highlight:** Historical dataset scatter points (Study Hours vs Exam Score) featuring a **golden diamond marker** showing where the evaluated student sits relative to the entire historical cohort.
  - **Marginal Effort-to-Score Matrix:** Quantified returns ($+1\text{ hr study} = +4.76\text{ pts}$, $+10\%\text{ attendance} = +3.80\text{ pts}$, $+1\text{ assignment} = +1.97\text{ pts}$).

### 3. 📚 Subject-Wise Academic Insights
- Detailed benchmarks across 5 academic courses:
  1. **Machine Learning & Analytics** (4 Credits • Avg: 71.0% • Pass: 88.2% • Min Study: 6.0 hrs/wk)
  2. **Mathematics for Computing** (4 Credits • Avg: 64.2% • Pass: 79.5% • Min Study: 6.5 hrs/wk)
  3. **Data Structures & Algorithms** (4 Credits • Avg: 62.8% • Pass: 76.4% • Min Study: 7.0 hrs/wk)
  4. **Computer Networks** (3 Credits • Avg: 69.8% • Pass: 86.0% • Min Study: 4.5 hrs/wk)
  5. **Applied Physics** (4 Credits • Avg: 65.4% • Pass: 81.0% • Min Study: 5.5 hrs/wk)
- One-click `[ Load into Prediction Studio ]` action pre-populates subject benchmarks.

### 4. 📈 Prediction History & Progress Tracking
- **Full `localStorage` Persistence:** Predictions are automatically saved and preserved across browser sessions.
- **Search & Filter:** Search by student name or subject; filter by risk tier.
- **Actions:** Reload any previous prediction back into the studio with one click, delete records, or export the entire history to **CSV**.

### 5. 🎯 Personalized 4-Week Action Roadmaps
- Customized intervention roadmap dynamically generated based on the student's evaluated numbers:
  - **Week 1:** Habit & Attendance Reset (Lecture attendance stabilization)
  - **Week 2:** Coursework Mastery (Clearing backlogs, $+1.97\text{ pts}$ per task)
  - **Week 3:** Deep Study Sprints (Targeted hours on high-yield topics)
  - **Week 4:** Exam Simulation & Polish (Mock exams and error analysis)
- Print-ready format for academic counseling meetings.

---

## 🏆 Model Performance Benchmark

Evaluated on 80 unseen test records under 5-fold cross-validation:

| Rank | Model Name | Test $R^2$ | Adjusted $R^2$ | Test MAE | Test RMSE | 5-Fold CV $R^2$ | Status |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| 🥇 | **Linear Regression (OLS)** | **$0.9064$** | **$0.9027$** | **$4.0298$** | **$5.0432$** | **$0.8984 \pm 0.015$** | **Champion Model** |
| 🥈 | **Ridge Regression ($L_2$)** | $0.9064$ | $0.9027$ | $4.0306$ | $5.0436$ | $0.8984 \pm 0.015$ | Regularized Baseline |
| 🥉 | **Lasso Regression ($L_1$)** | $0.9062$ | $0.9025$ | $4.0390$ | $5.0500$ | $0.8984 \pm 0.015$ | Sparse Baseline |
| 4 | **Gradient Boosting Regressor** | $0.8663$ | $0.8610$ | $4.7634$ | $6.0291$ | $0.8681 \pm 0.012$ | Ensemble Boosting |
| 5 | **Random Forest Regressor** | $0.8499$ | $0.8440$ | $5.0829$ | $6.3867$ | $0.8532 \pm 0.016$ | Ensemble Bagging |
| 6 | **Decision Tree Regressor** | $0.7758$ | $0.7669$ | $6.1485$ | $7.8065$ | $0.7804 \pm 0.040$ | Non-linear Baseline |

### Mathematical Blended Prediction Equation
$$\widehat{\text{Exam\_Score}} = 0.40 \cdot \text{Marks\_Obtained} + 0.60 \cdot \left[3.4209 + 4.7639 \cdot \text{Study} + 0.3795 \cdot \text{Attend} + 1.9669 \cdot \text{Assign}\right]$$

---

## 🌐 Cloud Deployment (Vercel)

The repository is configured for zero-configuration deployment via [`vercel.json`](vercel.json):
```bash
# Push to GitHub:
git push origin main
```
Import [`https://github.com/Abhi111227/Student-Performance-Prediction-Framework`](https://github.com/Abhi111227/Student-Performance-Prediction-Framework) directly into [Vercel](https://vercel.com) for instant cloud hosting.

---

## 💻 Local Execution
```bash
# Preview the application locally:
py -3 -m http.server 3000 --directory public
```
Visit `http://localhost:3000` in your web browser.
