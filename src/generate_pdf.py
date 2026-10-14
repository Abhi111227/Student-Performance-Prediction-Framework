"""
Generate compact, professional PDF summary for NOVORA Framework.
Covers: Tech Stack, Dataset, ML Model Training, Formulas, and End-to-End Flow.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            super().showPage()
        super().save()

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(36, 762, "NOVORA: Technical Architecture & Machine Learning Summary")
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.5)
            self.line(36, 756, 576, 756)
            
        # Footer
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(576, 24, page_str)
        self.drawString(36, 24, "CONFIDENTIAL & PROPRIETARY — NOVORA LEARNING ANALYTICS FRAMEWORK")
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(36, 34, 576, 34)
        self.restoreState()

def build_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=42
    )

    styles = getSampleStyleSheet()
    
    # Custom Palette
    primary_color = colors.HexColor("#312E81")    # Deep Indigo
    secondary_color = colors.HexColor("#4F46E5")  # Indigo
    dark_text = colors.HexColor("#0F172A")        # Slate 900
    body_text = colors.HexColor("#334155")        # Slate 700
    bg_light = colors.HexColor("#F8FAFC")         # Slate 50
    accent_emerald = colors.HexColor("#047857")   # Emerald 700

    # Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=primary_color
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#475569")
    )
    
    sec_heading = ParagraphStyle(
        'SecHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=primary_color,
        spaceBefore=8,
        spaceAfter=4
    )
    
    body_p = ParagraphStyle(
        'BodyP',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=body_text
    )

    tbl_head = ParagraphStyle(
        'TblHead',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white
    )

    tbl_cell = ParagraphStyle(
        'TblCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=10,
        textColor=body_text
    )

    tbl_cell_bold = ParagraphStyle(
        'TblCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=10,
        textColor=dark_text
    )

    formula_style = ParagraphStyle(
        'FormulaText',
        parent=styles['Normal'],
        fontName='Courier-Bold',
        fontSize=8.5,
        leading=11,
        textColor=primary_color
    )

    story = []

    # Title Banner Block
    story.append(Paragraph("NOVORA: Technical Architecture & ML Summary", title_style))
    story.append(Spacer(1, 2))
    story.append(Paragraph("End-to-End System Specifications • Frontend to Backend • Multi-Model Machine Learning Training", subtitle_style))
    story.append(Spacer(1, 6))
    story.append(HRFlowable(width="100%", thickness=1.5, color=secondary_color, spaceBefore=2, spaceAfter=8))

    # SECTION 1: FULL TECHNOLOGY STACK
    story.append(Paragraph("1. FULL TECHNOLOGY STACK (END-TO-END)", sec_heading))
    stack_data = [
        [Paragraph("Layer", tbl_head), Paragraph("Technologies", tbl_head), Paragraph("Role & Core Responsibility", tbl_head)],
        [
            Paragraph("Frontend (UI/UX)", tbl_cell_bold),
            Paragraph("HTML5, Tailwind CSS, Chart.js, FontAwesome", tbl_cell),
            Paragraph("Reactive single-page dashboard: direct numeric inputs, dynamic Chart.js cohort scatter plot with active student highlight, grade distribution histogram, and persistent localStorage history log.", tbl_cell)
        ],
        [
            Paragraph("Backend API", tbl_cell_bold),
            Paragraph("Node.js Serverless Functions (`api/predict.js`)", tbl_cell),
            Paragraph("Zero-cold-start REST endpoint with CORS support. Validates inputs, calculates blended inference, value-add trajectory, and target gap analysis.", tbl_cell)
        ],
        [
            Paragraph("Machine Learning", tbl_cell_bold),
            Paragraph("Python 3.13, Scikit-Learn, Pandas, NumPy, SciPy", tbl_cell),
            Paragraph("Data ingestion, 80/20 train-test partitioning, zero-leakage StandardScaler scaling, 6-algorithm benchmark, and .joblib model serialization.", tbl_cell)
        ],
        [
            Paragraph("Deployment", tbl_cell_bold),
            Paragraph("Vercel (`vercel.json`), Git, GitHub", tbl_cell),
            Paragraph("One-click automated cloud deployment with serverless routing rules, rewrite paths, and semantic per-phase Git version history.", tbl_cell)
        ]
    ]

    t_stack = Table(stack_data, colWidths=[90, 150, 300])
    t_stack.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), secondary_color),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, bg_light]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t_stack)
    story.append(Spacer(1, 8))

    # SECTION 2: DATASET AT A GLANCE
    story.append(Paragraph("2. DATASET SPECIFICATIONS & INPUT FEATURES", sec_heading))
    dataset_summary_text = (
        "Dataset contains <b>400 verified student records</b> (100% complete, 0 missing nulls, 0 duplicate instances). "
        "The objective is to predict final summative <b>Exam_Score (0 - 100)</b> using behavioral and formative indicators."
    )
    story.append(Paragraph(dataset_summary_text, body_p))
    story.append(Spacer(1, 4))

    feat_data = [
        [Paragraph("Feature Name", tbl_head), Paragraph("Data Type", tbl_head), Paragraph("Observed Range", tbl_head), Paragraph("Correlation (r)", tbl_head), Paragraph("Educational Significance", tbl_head)],
        [Paragraph("Study_Hours", tbl_cell_bold), Paragraph("float64", tbl_cell), Paragraph("1.05 – 9.91 hrs", tbl_cell), Paragraph("+0.8088", tbl_cell_bold), Paragraph("Weekly independent study hours; strongest linear predictor.", tbl_cell)],
        [Paragraph("Attendance", tbl_cell_bold), Paragraph("float64", tbl_cell), Paragraph("50.5% – 99.9%", tbl_cell), Paragraph("+0.3161", tbl_cell), Paragraph("Classroom presence rate; ensures instructional exposure.", tbl_cell)],
        [Paragraph("Assignments", tbl_cell_bold), Paragraph("int64", tbl_cell), Paragraph("0 – 10 tasks", tbl_cell), Paragraph("+0.4229", tbl_cell), Paragraph("Formative coursework submissions; active problem solving.", tbl_cell)],
        [Paragraph("Marks_Obtained", tbl_cell_bold), Paragraph("float64", tbl_cell), Paragraph("0.0% – 100.0%", tbl_cell), Paragraph("Integrated Anchor", tbl_cell), Paragraph("Midterm / internal continuous evaluation baseline for trajectory analysis.", tbl_cell)],
        [Paragraph("Exam_Score (Target)", tbl_cell_bold), Paragraph("float64", tbl_cell), Paragraph("24.38 – 100.0%", tbl_cell), Paragraph("1.0000", tbl_cell_bold), Paragraph("Final comprehensive examination outcome (Mean: 67.35, Std: 16.33).", tbl_cell)]
    ]

    t_feat = Table(feat_data, colWidths=[95, 55, 75, 75, 240])
    t_feat.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), primary_color),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, bg_light]),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
    ]))
    story.append(t_feat)
    story.append(Spacer(1, 8))

    # SECTION 3: MODEL TRAINING & BENCHMARKING
    story.append(Paragraph("3. MACHINE LEARNING MODEL TRAINING & LEADERBOARD", sec_heading))
    training_info = (
        "<b>Partitioning Strategy:</b> 80% Training (320 samples) / 20% Held-Out Testing (80 samples) with fixed <code>random_state=42</code>. "
        "Strict 5-Fold Cross-Validation was performed across all candidate algorithms to ensure zero overfitting."
    )
    story.append(Paragraph(training_info, body_p))
    story.append(Spacer(1, 4))

    lead_data = [
        [Paragraph("Rank & Model Name", tbl_head), Paragraph("Test R²", tbl_head), Paragraph("Adj. R²", tbl_head), Paragraph("MAE (Marks)", tbl_head), Paragraph("RMSE", tbl_head), Paragraph("5-Fold CV R²", tbl_head), Paragraph("Outcome Status", tbl_head)],
        [
            Paragraph("🥇 Linear Regression (OLS)", tbl_cell_bold),
            Paragraph("<b>0.9064</b>", tbl_cell_bold),
            Paragraph("0.9027", tbl_cell),
            Paragraph("<b>4.0298</b>", tbl_cell_bold),
            Paragraph("5.0432", tbl_cell),
            Paragraph("0.8984 ± 0.015", tbl_cell),
            Paragraph("<b>Champion Model</b>", tbl_cell_bold)
        ],
        [
            Paragraph("🥈 Ridge Regression (L2)", tbl_cell_bold),
            Paragraph("0.9064", tbl_cell),
            Paragraph("0.9027", tbl_cell),
            Paragraph("4.0306", tbl_cell),
            Paragraph("5.0436", tbl_cell),
            Paragraph("0.8984 ± 0.015", tbl_cell),
            Paragraph("Regularized Linear", tbl_cell)
        ],
        [
            Paragraph("🥉 Lasso Regression (L1)", tbl_cell_bold),
            Paragraph("0.9062", tbl_cell),
            Paragraph("0.9025", tbl_cell),
            Paragraph("4.0390", tbl_cell),
            Paragraph("5.0500", tbl_cell),
            Paragraph("0.8984 ± 0.015", tbl_cell),
            Paragraph("Sparse Baseline", tbl_cell)
        ],
        [
            Paragraph("4. Gradient Boosting", tbl_cell),
            Paragraph("0.8663", tbl_cell),
            Paragraph("0.8610", tbl_cell),
            Paragraph("4.7634", tbl_cell),
            Paragraph("6.0291", tbl_cell),
            Paragraph("0.8681 ± 0.012", tbl_cell),
            Paragraph("Ensemble Boosting", tbl_cell)
        ],
        [
            Paragraph("5. Random Forest (100 Trees)", tbl_cell),
            Paragraph("0.8499", tbl_cell),
            Paragraph("0.8440", tbl_cell),
            Paragraph("5.0829", tbl_cell),
            Paragraph("6.3867", tbl_cell),
            Paragraph("0.8532 ± 0.016", tbl_cell),
            Paragraph("Ensemble Bagging", tbl_cell)
        ],
        [
            Paragraph("6. Decision Tree Regressor", tbl_cell),
            Paragraph("0.7758", tbl_cell),
            Paragraph("0.7669", tbl_cell),
            Paragraph("6.1485", tbl_cell),
            Paragraph("7.8065", tbl_cell),
            Paragraph("0.7804 ± 0.040", tbl_cell),
            Paragraph("Single Tree Baseline", tbl_cell)
        ]
    ]

    t_lead = Table(lead_data, colWidths=[125, 55, 50, 60, 50, 85, 115])
    t_lead.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), secondary_color),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor("#EEF2FF"), colors.white, bg_light, colors.white, bg_light, colors.white]),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
    ]))
    story.append(t_lead)
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Why OLS Linear Regression Won:</b> The dataset exhibits strong linear determinism (r = 0.81 with study hours) with near-zero inter-predictor collinearity (|r| < 0.12). OLS provided the lowest prediction error (MAE: ±4.03 marks) with optimal coefficient interpretability.", body_p))
    story.append(Spacer(1, 8))

    # SECTION 4: EXACT MATHEMATICAL FORMULAS
    story.append(Paragraph("4. MATHEMATICAL FORMULATION & TRAJECTORY ENGINE", sec_heading))
    
    math_content = [
        [
            Paragraph("<b>Component</b>", tbl_head),
            Paragraph("<b>Exact Mathematical Equation & Weight Allocation</b>", tbl_head),
            Paragraph("<b>Pedagogical Interpretation</b>", tbl_head)
        ],
        [
            Paragraph("Behavioral Base Score", tbl_cell_bold),
            Paragraph("<code>Base_Score = 3.4209 + 4.7639*(Study) + 0.3795*(Attend) + 1.9669*(Assign)</code>", formula_style),
            Paragraph("+1 hr study = <b>+4.76 marks</b><br/>+10% attendance = <b>+3.80 marks</b><br/>+1 assignment = <b>+1.97 marks</b>", tbl_cell)
        ],
        [
            Paragraph("Blended Final Prediction", tbl_cell_bold),
            Paragraph("<code>Final_Score = 0.40*(Marks_Obtained) + 0.60*(Base_Score)</code>", formula_style),
            Paragraph("Combines prior formative midterm baseline (40%) with current study habit velocity (60%).", tbl_cell)
        ],
        [
            Paragraph("Value-Add Trajectory (Δ)", tbl_cell_bold),
            Paragraph("<code>Δ = Final_Score - Marks_Obtained</code>", formula_style),
            Paragraph("Δ > +3.0: <b>Accelerating Growth</b><br/>-3.0 ≤ Δ ≤ +3.0: <b>Steady Trajectory</b><br/>Δ < -3.0: <b>Declining Warning Alert</b>", tbl_cell)
        ],
        [
            Paragraph("Target Gap Analysis", tbl_cell_bold),
            Paragraph("<code>Hours_Needed = (Target_Score - Final_Score) / (4.7639 * 0.60)</code>", formula_style),
            Paragraph("Quantifies exact study hours or homework tasks required to elevate to next tier (Distinction 80%).", tbl_cell)
        ]
    ]

    t_math = Table(math_content, colWidths=[105, 265, 170])
    t_math.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), primary_color),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, bg_light]),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
    ]))
    story.append(t_math)
    story.append(Spacer(1, 8))

    # SECTION 5: SYSTEM WORKFLOW & APPLICATION MODULES
    story.append(Paragraph("5. END-TO-END WORKFLOW & APPLICATION MODULES", sec_heading))
    
    workflow_text = (
        "<b>Workflow:</b> "
        "<b>1. Data Input:</b> Educator or student inputs Marks Obtained, Study Hours, Attendance, and Assignments. "
        "<b>2. Real-Time Inference:</b> Client-side JS computes instant score (with serverless <code>/api/predict</code> API fallback). "
        "<b>3. Diagnostics:</b> Calculates Value-Add Trajectory (Growth/Decline), Risk Tier (High Performer, Moderate, At Risk), and Gap to Distinction. "
        "<b>4. Persistence:</b> Prediction logged to browser <code>localStorage</code> with search, filtering, and CSV export. "
        "<b>5. Action Plan:</b> System outputs a dynamic 4-Week Intervention Roadmap with prioritized weekly milestone goals."
    )
    story.append(Paragraph(workflow_text, body_p))
    story.append(Spacer(1, 6))

    # Footer metadata box
    meta_box = [
        [
            Paragraph(
                "<b>Deployment:</b> Vercel Cloud (Zero-Config via <code>vercel.json</code>) &nbsp;|&nbsp; "
                "<b>GitHub Repository:</b> <code>https://github.com/Abhi111227/Student-Performance-Prediction-Framework</code> &nbsp;|&nbsp; "
                "<b>Champion Model:</b> Ordinary Least Squares (R² = 90.64%)",
                tbl_cell
            )
        ]
    ]
    t_meta = Table(meta_box, colWidths=[540])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#EEF2FF")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#C7D2FE")),
        ('PADDING', (0, 0), (-1, -1), 4),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ]))
    story.append(t_meta)

    # Build PDF with NumberedCanvas
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[+] Successfully compiled PDF to: {filename}")

if __name__ == "__main__":
    out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "NOVORA_Technical_Architecture_and_ML_Summary.pdf"))
    build_pdf(out_path)
