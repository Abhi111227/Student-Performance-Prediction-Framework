# NOVORA: Phase 6 & 7 Technical Report — Model Development, Multi-Algorithm Benchmarking & Evaluation

## 📌 1. Phase Objective & Overview
Phase 6 and Phase 7 form the predictive engine of the NOVORA framework. The objective is to design, train, cross-validate, evaluate, and serialize machine learning models capable of predicting student final exam scores with high statistical fidelity.

A portfolio of six machine learning algorithms spanning linear, regularized, tree-based, and ensemble methods was evaluated on identical $80/20$ train-test splits under strict 5-fold cross-validation.

---

## 🤖 2. Evaluated Model Architectures

1. **Ordinary Least Squares (OLS) Linear Regression**: Baseline parametric model assuming linear feature-outcome mapping.
2. **Ridge Regression ($L_2$ Regularization)**: Shrinks coefficient magnitudes to mitigate potential feature collinearity and variance.
3. **Lasso Regression ($L_1$ Regularization)**: Imposes sparsity on regression weights to penalize non-informative features.
4. **Decision Tree Regressor (CART)**: Non-parametric recursive splitting model capable of capturing non-linear step responses.
5. **Random Forest Regressor**: Ensemble bagging technique aggregating 100 decorrelated decision trees.
6. **Gradient Boosting Regressor**: Sequential boosting ensemble minimizing residual loss through gradient descent on regression trees.

---

## 📈 3. Rigorous Evaluation Metrics
Models were assessed using standard regression evaluation criteria:
- **Coefficient of Determination ($R^2$)**: Proportion of variance in academic score explained by the model:
  $$R^2 = 1 - \frac{\sum (y_i - \hat{y}_i)^2}{\sum (y_i - \bar{y})^2}$$
- **Adjusted $R^2$**: Corrects for degrees of freedom and prevents inflated optimism:
  $$\text{Adj } R^2 = 1 - \left[\frac{(1 - R^2)(n - 1)}{n - p - 1}\right]$$
- **Mean Absolute Error (MAE)**: Average absolute deviation in score points:
  $$\text{MAE} = \frac{1}{n}\sum_{i=1}^{n} |y_i - \hat{y}_i|$$
- **Root Mean Squared Error (RMSE)**: Penalizes larger prediction errors:
  $$\text{RMSE} = \sqrt{\frac{1}{n}\sum_{i=1}^{n} (y_i - \hat{y}_i)^2}$$
- **5-Fold Cross-Validation Score**: Evaluates generalization stability across 5 independent validation folds.

---

## 🏆 4. Model Performance Benchmark & Leaderboard

The empirical results on unseen evaluation data ($N_{\text{test}} = 80$):

| Rank | Model Name | Train $R^2$ | Test $R^2$ | Adjusted $R^2$ | Test MAE | Test RMSE | 5-Fold CV $R^2$ (Mean $\pm$ Std) |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| 🥇 | **Linear Regression (OLS)** | $0.9030$ | **$0.9064$** | **$0.9027$** | **$4.0298$** | **$5.0432$** | $0.8984 \pm 0.0150$ |
| 🥈 | **Ridge Regression ($L_2$)** | $0.9030$ | $0.9064$ | $0.9027$ | $4.0306$ | $5.0436$ | $0.8984 \pm 0.0150$ |
| 🥉 | **Lasso Regression ($L_1$)** | $0.9030$ | $0.9062$ | $0.9025$ | $4.0390$ | $5.0500$ | $0.8984 \pm 0.0150$ |
| 4 | **Gradient Boosting Regressor** | $0.9467$ | $0.8663$ | $0.8610$ | $4.7634$ | $6.0291$ | $0.8681 \pm 0.0125$ |
| 5 | **Random Forest Regressor** | $0.9537$ | $0.8499$ | $0.8440$ | $5.0829$ | $6.3867$ | $0.8532 \pm 0.0165$ |
| 6 | **Decision Tree Regressor** | $0.9120$ | $0.7758$ | $0.7669$ | $6.1485$ | $7.8065$ | $0.7804 \pm 0.0397$ |

### 🧮 Mathematical Model Equation
The optimal model is the Ordinary Least Squares formulation:
$$\widehat{\text{Exam\_Score}} = 3.4209 + 4.7639 \cdot \text{Study\_Hours} + 0.3795 \cdot \text{Attendance} + 1.9669 \cdot \text{Assignments\_Completed}$$

#### Pedagogical Interpretability:
- **Baseline Intercept ($3.42$):** Expected score without participation or study.
- **Study Hours Multiplier ($+4.76\text{ marks/hr}$):** Each additional weekly study hour increases the exam score by approximately **$4.76$ points**.
- **Attendance Contribution ($+0.38\text{ marks/\%}$):** Every 10% increase in attendance contributes approximately **$3.8$ marks**.
- **Assignment Completion Value ($+1.97\text{ marks/task}$):** Each completed homework assignment yields approximately **$1.97$ marks**.

---

## 📦 5. Serialized Deliverables
- `models/best_model.joblib`: Serialized scikit-learn model artifact.
- `models/model_parameters.json`: Explicit mathematical formula and coefficients for zero-latency client/server inference.
- `reports/model_leaderboard.csv`: Full benchmark comparison matrix.
- `reports/figures/models/`:
  - `model_r2_comparison.png`
  - `model_mae_rmse_comparison.png`
  - `actual_vs_predicted_best_model.png`
  - `residual_plot_best_model.png`
