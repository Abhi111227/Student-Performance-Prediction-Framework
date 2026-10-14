// Vercel Serverless Function: Advanced Student Performance Prediction & Trajectory Engine
// Framework: NOVORA v2.0 (Integrated Marks Obtained + OLS Model Weights)

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
  const studentName = (params.student_name || params.studentName || 'Student').trim();
  const subject = (params.subject || 'General Academic Cohort').trim();
  
  const studyHours = Math.min(24.0, Math.max(0.0, parseFloat(params.study_hours ?? params.studyHours ?? 5.5)));
  const attendance = Math.min(100.0, Math.max(0.0, parseFloat(params.attendance ?? 75.0)));
  const assignments = Math.min(10.0, Math.max(0.0, parseFloat(params.assignments_completed ?? params.assignments ?? 5.0)));
  
  // Marks Obtained (Internal / Mid-Term Assessment: 0 - 100)
  const hasMarksObtained = params.marks_obtained !== undefined && params.marks_obtained !== '' && params.marks_obtained !== null;
  const marksObtained = hasMarksObtained ? Math.min(100.0, Math.max(0.0, parseFloat(params.marks_obtained))) : null;

  // Exact Champion OLS Model Weights (Phase 6):
  // Behavioral Score = 3.4209 + (4.7639 * Study_Hours) + (0.3795 * Attendance) + (1.9669 * Assignments)
  const intercept = 3.4209;
  const cStudy = 4.7639;
  const cAttend = 0.3795;
  const cAssign = 1.9669;

  const behavioralScore = intercept + (cStudy * studyHours) + (cAttend * attendance) + (cAssign * assignments);

  // Blended Prediction: Integrate Marks Obtained (40% prior assessment + 60% behavioral trajectory)
  let predictedScore;
  let trajectoryValue = 0;
  let momentumStatus = "Steady";

  if (hasMarksObtained && !isNaN(marksObtained)) {
    // Blended formulation: Prior marks provide anchor (40%), current study habits drive velocity (60%)
    const rawBlend = (0.40 * marksObtained) + (0.60 * behavioralScore);
    predictedScore = Math.min(100.0, Math.max(0.0, rawBlend));
    trajectoryValue = parseFloat((predictedScore - marksObtained).toFixed(2));

    if (trajectoryValue > 3.0) {
      momentumStatus = "Accelerating Growth";
    } else if (trajectoryValue < -3.0) {
      momentumStatus = "Declining Trajectory Warning";
    } else {
      momentumStatus = "Consistent Pace";
    }
  } else {
    predictedScore = Math.min(100.0, Math.max(0.0, behavioralScore));
  }

  // Grade & Risk Tier
  let gradeLetter = "B";
  let riskTier = "Moderate";
  let badge = "Passing / Satisfactory";
  let statusColor = "#1f77b4";

  if (predictedScore >= 80.0) {
    gradeLetter = "A+";
    riskTier = "High Performer";
    badge = "Distinction / First Class";
    statusColor = "#16a34a";
  } else if (predictedScore >= 70.0) {
    gradeLetter = "A";
    riskTier = "High Performer";
    badge = "Merit / Above Average";
    statusColor = "#22c55e";
  } else if (predictedScore >= 50.0) {
    gradeLetter = "B";
    riskTier = "Moderate";
    badge = "Passing / Satisfactory";
    statusColor = "#d97706";
  } else {
    gradeLetter = "F";
    riskTier = "At Risk";
    badge = "Critical / Intervention Required";
    statusColor = "#dc2626";
  }

  // Target Gap Analysis to Next Band
  let targetTier = "Distinction (80%)";
  let gapPoints = 0;
  let studyHoursNeeded = 0;
  let assignmentsNeeded = 0;

  if (predictedScore < 50.0) {
    targetTier = "Passing (50%)";
    gapPoints = parseFloat((50.0 - predictedScore).toFixed(1));
    studyHoursNeeded = parseFloat((gapPoints / cStudy).toFixed(1));
    assignmentsNeeded = Math.min(10 - assignments, Math.ceil(gapPoints / cAssign));
  } else if (predictedScore < 80.0) {
    targetTier = "Distinction (80%)";
    gapPoints = parseFloat((80.0 - predictedScore).toFixed(1));
    studyHoursNeeded = parseFloat((gapPoints / cStudy).toFixed(1));
    assignmentsNeeded = Math.min(10 - assignments, Math.ceil(gapPoints / cAssign));
  } else {
    targetTier = "Perfect Mastery (100%)";
    gapPoints = parseFloat((100.0 - predictedScore).toFixed(1));
    studyHoursNeeded = parseFloat((gapPoints / cStudy).toFixed(1));
    assignmentsNeeded = 0;
  }

  // Estimated Percentile in 400 Student Cohort (Mean: 67.35, Std: 16.33)
  const z = (predictedScore - 67.35) / 16.33;
  const percentile = Math.min(99, Math.max(1, Math.round((1.0 / (1.0 + Math.exp(-1.6 * z))) * 100)));

  res.status(200).json({
    framework: "NOVORA Learning Analytics v2.0",
    status: "success",
    timestamp: new Date().toISOString(),
    student: {
      name: studentName,
      subject: subject
    },
    inputs: {
      marks_obtained: marksObtained,
      study_hours: studyHours,
      attendance_percentage: attendance,
      assignments_completed: assignments
    },
    prediction: {
      predicted_score: parseFloat(predictedScore.toFixed(2)),
      grade_letter: gradeLetter,
      risk_tier: riskTier,
      badge: badge,
      color: statusColor,
      percentile: percentile,
      trajectory: {
        momentum: momentumStatus,
        delta: trajectoryValue,
        description: trajectoryValue > 0 
          ? `+${trajectoryValue} points higher than marks obtained` 
          : `${trajectoryValue} points relative to marks obtained`
      },
      gap_analysis: {
        next_target: targetTier,
        points_needed: gapPoints,
        study_hours_payoff: studyHoursNeeded,
        assignments_payoff: assignmentsNeeded
      }
    },
    model_metadata: {
      engine: "Ordinary Least Squares (OLS) + Formative Blending",
      test_r2: 0.9064,
      test_mae: 4.0298,
      formula: "Final_Score = 0.40*(Marks_Obtained) + 0.60*(3.4209 + 4.7639*Study + 0.3795*Attend + 1.9669*Assign)"
    }
  });
};
