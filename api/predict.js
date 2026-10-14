// Vercel Serverless Function: Predict Student Performance
// Framework: NOVORA (Model: OLS Linear Regression, Test R2: 0.9064)

module.exports = (req, res) => {
  // Enable CORS
  res.setHeader('Access-Control-Allow-Credentials', true);
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET,OPTIONS,PATCH,DELETE,POST,PUT');
  res.setHeader(
    'Access-Control-Allow-Headers',
    'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version'
  );

  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  // Parse parameters from GET query or POST body
  const params = req.method === 'POST' ? req.body : req.query;
  const studyHours = parseFloat(params.study_hours ?? params.studyHours ?? 5.0);
  const attendance = parseFloat(params.attendance ?? 75.0);
  const assignments = parseFloat(params.assignments_completed ?? params.assignments ?? 5.0);

  // Exact OLS Regression Parameters from Phase 6
  // Exam_Score = 3.4209 + (4.7639 * Study_Hours) + (0.3795 * Attendance) + (1.9669 * Assignments_Completed)
  const intercept = 3.4209;
  const cStudy = 4.7639;
  const cAttend = 0.3795;
  const cAssign = 1.9669;

  let rawScore = intercept + (cStudy * studyHours) + (cAttend * attendance) + (cAssign * assignments);
  let predictedScore = Math.min(100.0, Math.max(0.0, rawScore));

  // Determine Academic Risk Tier
  let riskTier = "Moderate";
  let statusColor = "#1f77b4";
  let badge = "Passing";
  let recommendation = "";

  if (predictedScore >= 75.0) {
    riskTier = "High Performer";
    statusColor = "#2ca02c";
    badge = "Distinction / Excellent";
    recommendation = "Student demonstrates strong mastery and disciplined study habits. Encourage honors coursework and leadership.";
  } else if (predictedScore >= 50.0) {
    riskTier = "Moderate";
    statusColor = "#ff7f0e";
    badge = "Passing / Satisfactory";
    const addStudy = Math.min(4, Math.max(1, Math.round((75 - predictedScore) / cStudy)));
    recommendation = `Targeting an additional ${addStudy} weekly self-study hours and maintaining >=80% attendance would elevate the student to High Performer status.`;
  } else {
    riskTier = "At Risk";
    statusColor = "#d62728";
    badge = "Critical / Intervention Required";
    recommendation = "Immediate academic intervention advised: mandatory tutoring sessions, coursework remediation, and weekly attendance check-ins.";
  }

  // Estimated percentile using Gaussian approximation (mean: 67.35, std: 16.33)
  const z = (predictedScore - 67.35) / 16.33;
  // Approximation of cumulative normal distribution
  const percentile = Math.min(99.9, Math.max(0.1, Math.round((1.0 / (1.0 + Math.exp(-1.6 * z))) * 100)));

  res.status(200).json({
    framework: "NOVORA: Learning Analytics & Success Prediction",
    status: "success",
    inputs: {
      study_hours: studyHours,
      attendance_percentage: attendance,
      assignments_completed: assignments
    },
    prediction: {
      exam_score: parseFloat(predictedScore.toFixed(2)),
      risk_tier: riskTier,
      badge: badge,
      color: statusColor,
      estimated_percentile: percentile,
      guidance: recommendation
    },
    model_metadata: {
      model_name: "Ordinary Least Squares (OLS) Linear Regression",
      test_r2: 0.9064,
      adjusted_r2: 0.9027,
      test_mae: 4.0298,
      test_rmse: 5.0432,
      formula: "Exam_Score = 3.4209 + 4.7639*(Study_Hours) + 0.3795*(Attendance) + 1.9669*(Assignments)"
    }
  });
};
