# 🎓 "NOVORA": Intelligent Learning Analytics & Student Success Prediction Framework

A comprehensive, production-grade Machine Learning predictive analytics platform engineered to forecast student academic performance (`Exam_Score`), identify at-risk learners early, and deliver proactive pedagogical interventions.

---

## 📌 Project Architecture & Lifecycle Status

| Phase | Description | Status | Primary Artifacts |
| :--- | :--- | :---: | :--- |
| **Phase 1: Problem Understanding** | Educational domain analysis, stakeholder mapping, regression formulation | ✅ Complete | [`reports/NOVORA_Comprehensive_ML_Report.md`](reports/NOVORA_Comprehensive_ML_Report.md) |
| **Phase 2: Data Collection & Profiling** | 400 verified student records, schema validation, data dictionary | ✅ Complete | [`data/student_performance_data.csv`](data/student_performance_data.csv), [`src/data_collection.py`](src/data_collection.py) |
| **Phase 3: Data Preprocessing** | 80/20 train-test partitioning (320/80), zero-leakage StandardScaler scaling | ✅ Complete | [`src/preprocessing.py`](src/preprocessing.py), [`data/train_data.csv`](data/train_data.csv) |
| **Phase 4: Exploratory Analysis (EDA)** | Risk stratification (High Performer: 42.25%, Moderate: 42.0%, At Risk: 15.75%) | ✅ Complete | [`src/eda.py`](src/eda.py), [`reports/figures/eda/`](reports/figures/eda/) |
| **Phase 5: Feature Engineering** | Compound `Study_Attendance_Index` achieving $r = +0.8506$ correlation | ✅ Complete | [`src/feature_engineering.py`](src/feature_engineering.py), [`data/train_features.csv`](data/train_features.csv) |
| **Phase 6: Model Development** | Benchmarked 6 algorithms (OLS, Ridge, Lasso, CART, Random Forest, GBDT) | ✅ Complete | [`src/model_training.py`](src/model_training.py) |
| **Phase 7: Model Evaluation** | Ordinary Least Squares champion: **Test $R^2 = 0.9064$**, **MAE = $4.03$ points** | ✅ Complete | [`models/best_model.joblib`](models/best_model.joblib), [`reports/model_leaderboard.csv`](reports/model_leaderboard.csv) |
| **Phase 8: Web Dashboard & Deployment** | Responsive analytics dashboard, serverless prediction API, Vercel ready | ✅ Complete | [`public/index.html`](public/index.html), [`api/predict.js`](api/predict.js), [`vercel.json`](vercel.json) |

---

## 🏆 Model Performance Benchmark

Evaluated on 80 unseen test records with 5-fold cross-validation:

| Rank | Model Name | Test $R^2$ | Adjusted $R^2$ | Test MAE | Test RMSE | 5-Fold CV $R^2$ |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| 🥇 | **Linear Regression (OLS)** | **$0.9064$** | **$0.9027$** | **$4.0298$** | **$5.0432$** | **$0.8984 \pm 0.015$** |
| 🥈 | **Ridge Regression ($L_2$)** | $0.9064$ | $0.9027$ | $4.0306$ | $5.0436$ | $0.8984 \pm 0.015$ |
| 🥉 | **Lasso Regression ($L_1$)** | $0.9062$ | $0.9025$ | $4.0390$ | $5.0500$ | $0.8984 \pm 0.015$ |
| 4 | **Gradient Boosting Regressor** | $0.8663$ | $0.8610$ | $4.7634$ | $6.0291$ | $0.8681 \pm 0.012$ |
| 5 | **Random Forest Regressor** | $0.8499$ | $0.8440$ | $5.0829$ | $6.3867$ | $0.8532 \pm 0.016$ |
| 6 | **Decision Tree Regressor** | $0.7758$ | $0.7669$ | $6.1485$ | $7.8065$ | $0.7804 \pm 0.040$ |

### 🧮 Mathematical Model Equation
$$\widehat{\text{Exam\_Score}} = 3.4209 + 4.7639 \cdot \text{Study\_Hours} + 0.3795 \cdot \text{Attendance} + 1.9669 \cdot \text{Assignments\_Completed}$$

---

## 🌐 Deploying to Vercel

### Option 1: Automatic 1-Click Import via Vercel Dashboard
1. Push this repository to your GitHub account (`https://github.com/Abhin1122/...`).
2. Go to [vercel.com](https://vercel.com) and click **"Add New Project"**.
3. Select your repository. Vercel will automatically detect `vercel.json` and deploy immediately.

### Option 2: Deploy via Vercel CLI
```bash
# In the project directory:
npx vercel
```

---

## 🚀 Local Reproduction & Execution

### 1. Run Complete Machine Learning Pipeline
```bash
# Phase 2: Ingestion & Profiling
py -3 src/data_collection.py

# Phase 3: Preprocessing & Scaling
py -3 src/preprocessing.py

# Phase 4: Exploratory Data Analysis
py -3 src/eda.py

# Phase 5: Feature Engineering
py -3 src/feature_engineering.py

# Phase 6 & 7: Model Training & Evaluation
py -3 src/model_training.py
```

### 2. Launch Local Web Application
```bash
# Option A: Python Built-in Web Server
py -3 -m http.server 3000 --directory public

# Option B: Node.js / npx
npx serve public
```
Visit `http://localhost:3000` in your browser.
