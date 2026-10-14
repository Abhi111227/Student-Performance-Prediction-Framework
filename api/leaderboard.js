// Vercel Serverless Function: Model Leaderboard API
// Framework: NOVORA

module.exports = (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Content-Type', 'application/json');

  const leaderboard = [
    {
      rank: 1,
      model: "Linear Regression (OLS)",
      train_r2: 0.9030,
      test_r2: 0.9064,
      adjusted_r2: 0.9027,
      mae: 4.0298,
      mse: 25.4341,
      rmse: 5.0432,
      cv_mean: 0.8984,
      cv_std: 0.0150,
      status: "Selected Optimal Model"
    },
    {
      rank: 2,
      model: "Ridge Regression (L2)",
      train_r2: 0.9030,
      test_r2: 0.9064,
      adjusted_r2: 0.9027,
      mae: 4.0306,
      mse: 25.4377,
      rmse: 5.0436,
      cv_mean: 0.8984,
      cv_std: 0.0150,
      status: "Regularized Alternative"
    },
    {
      rank: 3,
      model: "Lasso Regression (L1)",
      train_r2: 0.9030,
      test_r2: 0.9062,
      adjusted_r2: 0.9025,
      mae: 4.0390,
      mse: 25.5024,
      rmse: 5.0500,
      cv_mean: 0.8984,
      cv_std: 0.0150,
      status: "Sparse Baseline"
    },
    {
      rank: 4,
      model: "Gradient Boosting Regressor",
      train_r2: 0.9467,
      test_r2: 0.8663,
      adjusted_r2: 0.8610,
      mae: 4.7634,
      mse: 36.3501,
      rmse: 6.0291,
      cv_mean: 0.8681,
      cv_std: 0.0125,
      status: "Ensemble Boosting"
    },
    {
      rank: 5,
      model: "Random Forest Regressor",
      train_r2: 0.9537,
      test_r2: 0.8499,
      adjusted_r2: 0.8440,
      mae: 5.0829,
      mse: 40.7897,
      rmse: 6.3867,
      cv_mean: 0.8532,
      cv_std: 0.0165,
      status: "Ensemble Bagging"
    },
    {
      rank: 6,
      model: "Decision Tree Regressor",
      train_r2: 0.9120,
      test_r2: 0.7758,
      adjusted_r2: 0.7669,
      mae: 6.1485,
      mse: 60.9416,
      rmse: 7.8065,
      cv_mean: 0.7804,
      cv_std: 0.0397,
      status: "Non-linear Baseline"
    }
  ];

  res.status(200).json({
    framework: "NOVORA",
    evaluation_partition: "80 Samples (20% Unseen Test Split)",
    leaderboard: leaderboard
  });
};
