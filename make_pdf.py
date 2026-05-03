#!/usr/bin/env python3
"""CMDSolver — PDF Documentation Generator"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether
)
from reportlab.platypus.flowables import Flowable
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY

# ── Colours ──────────────────────────────────────────────────────────────────
C_NAVY   = colors.HexColor('#1a3a5c')
C_BLUE   = colors.HexColor('#2e7dd1')
C_ORANGE = colors.HexColor('#e8602c')
C_LIGHT  = colors.HexColor('#f1f3f5')
C_WARN   = colors.HexColor('#fff3cd')
C_ERR    = colors.HexColor('#f8d7da')
C_OK     = colors.HexColor('#d4edda')
C_INFO   = colors.HexColor('#e8f4f8')
C_BORDER = colors.HexColor('#dee2e6')
C_CODE   = colors.HexColor('#1e2330')
C_WHITE  = colors.white

W, H = A4

# ── Styles ───────────────────────────────────────────────────────────────────
base = getSampleStyleSheet()

def S(name, parent='Normal', **kw):
    return ParagraphStyle(name, parent=base[parent], **kw)

sTitle    = S('DocTitle', 'Title',
              fontSize=28, textColor=C_WHITE, leading=34, spaceAfter=6)
sSubtitle = S('DocSub',   'Normal',
              fontSize=12, textColor=colors.HexColor('#cdd9e8'), spaceAfter=4)
sMeta     = S('DocMeta',  'Normal',
              fontSize=9,  textColor=colors.HexColor('#99aec4'))

sH1 = S('H1', 'Heading1',
        fontSize=18, textColor=C_NAVY, spaceBefore=24, spaceAfter=8,
        borderPadding=(0,0,4,0))
sH2 = S('H2', 'Heading2',
        fontSize=13, textColor=C_NAVY, spaceBefore=16, spaceAfter=6)
sH3 = S('H3', 'Heading3',
        fontSize=11, textColor=C_ORANGE, spaceBefore=10, spaceAfter=4,
        fontName='Helvetica-Bold')

sBody = S('Body', 'Normal',
          fontSize=10, leading=15, spaceAfter=6, textColor=colors.HexColor('#212529'))
sBullet = S('Bullet', 'Normal',
            fontSize=10, leading=14, leftIndent=14, spaceAfter=3,
            bulletIndent=4)
sCode = S('Code', 'Code',
          fontSize=8.5, leading=12, backColor=C_CODE, textColor=colors.HexColor('#cdd3e0'),
          leftIndent=10, rightIndent=10, borderPadding=8, spaceAfter=8)
sCaption = S('Cap', 'Normal',
             fontSize=8, textColor=colors.HexColor('#6c757d'), spaceAfter=4,
             alignment=TA_CENTER)
sTH = S('TH', 'Normal',
        fontSize=9, fontName='Helvetica-Bold', textColor=C_WHITE, leading=13)
sTD = S('TD', 'Normal',
        fontSize=9, leading=13)
sTDc = S('TDc', 'Normal',
         fontSize=9, leading=13, textColor=colors.HexColor('#6c757d'))
sCallout = S('Callout', 'Normal',
             fontSize=9.5, leading=14, leftIndent=8)

# ── Helper Flowables ─────────────────────────────────────────────────────────
def spacer(h=6): return Spacer(1, h)
def rule(color=C_BLUE, w=1.5): return HRFlowable(width='100%', thickness=w, color=color, spaceAfter=4)
def pb(): return PageBreak()

def h1(text, num=None):
    label = f"{num}. {text}" if num else text
    return [rule(C_BLUE, 2), Paragraph(label, sH1), spacer(4)]

def h2(text):
    return Paragraph(text, sH2)

def h3(text):
    return Paragraph(text, sH3)

def body(text):
    return Paragraph(text, sBody)

def bullet(items):
    return [Paragraph(f"• {it}", sBullet) for it in items]

def code(text):
    escaped = text.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
    return Paragraph(f'<font name="Courier">{escaped}</font>', sCode)

def callout(text, bg=C_INFO, border=C_BLUE):
    t = Table([[Paragraph(text, sCallout)]],
              colWidths=[W - 5.4*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg),
        ('LINEAFTER',  (0,0), (0,-1), 4, border),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING',  (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    return t

def make_table(headers, rows, colW=None):
    data = [[Paragraph(h, sTH) for h in headers]]
    for row in rows:
        data.append([Paragraph(str(c), sTD) for c in row])
    if colW is None:
        n = len(headers)
        colW = [(W - 5.4*cm) / n] * n
    t = Table(data, colWidths=colW, repeatRows=1)
    style = TableStyle([
        ('BACKGROUND',    (0,0), (-1,0),  C_NAVY),
        ('GRID',          (0,0), (-1,-1), 0.4, C_BORDER),
        ('ROWBACKGROUNDS',(0,1), (-1,-1), [C_WHITE, C_LIGHT]),
        ('VALIGN',        (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING',   (0,0), (-1,-1), 6),
        ('RIGHTPADDING',  (0,0), (-1,-1), 6),
        ('TOPPADDING',    (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ])
    t.setStyle(style)
    return t

# ── Cover page ───────────────────────────────────────────────────────────────
def make_cover_page():
    """Build cover as Platypus flowables with a full-page background via canvas callback."""
    def draw_cover(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(C_NAVY)
        canvas.rect(0, 0, W, H, fill=1, stroke=0)
        canvas.setFillColor(colors.HexColor('#2a5f9e'))
        canvas.rect(0, 0, W, H*0.35, fill=1, stroke=0)
        canvas.setFillColor(C_BLUE)
        canvas.rect(0, H*0.35, W, 5, fill=1, stroke=0)
        canvas.setFillColor(C_ORANGE)
        canvas.rect(0, H*0.35 + 5, W, 5, fill=1, stroke=0)
        # Title area
        canvas.setFillColor(C_WHITE)
        canvas.setFont('Helvetica-Bold', 40)
        canvas.drawString(2.5*cm, H*0.72, 'CMDSolver')
        canvas.setFont('Helvetica', 17)
        canvas.setFillColor(colors.HexColor('#b8cde4'))
        canvas.drawString(2.5*cm, H*0.66, 'Modular Nonlinear Equation System Solver')
        canvas.drawString(2.5*cm, H*0.62, 'for Aerothermodynamic Systems')
        canvas.setFillColor(colors.HexColor('#cdd9e8'))
        canvas.setFont('Helvetica', 13)
        canvas.drawString(2.5*cm, H*0.56, 'Technical Documentation')
        canvas.setFont('Helvetica', 10)
        canvas.setFillColor(colors.HexColor('#99aec4'))
        canvas.drawString(2.5*cm, H*0.50, 'Package: apps.eqnParser  ·  46 Java Source Files  ·  April 2026')
        canvas.drawString(2.5*cm, H*0.47, 'GraalVM 25 / OpenJDK 21  ·  CASprzak 0.3.0  ·  GSPAR (Grund/WIAS 1994)')
        # Feature box
        canvas.setFillColor(colors.HexColor('#0f2540'))
        canvas.roundRect(2.5*cm, H*0.12, W - 5*cm, H*0.18, 8, fill=1, stroke=0)
        canvas.setFont('Helvetica-Bold', 10)
        feats = [
            'GSPAR Sparse LU Solver (Grund, WIAS Berlin ~1994) — Java Port',
            'Newton-Armijo  ·  Levenberg-Marquardt  ·  Broyden  ·  Homotopy',
            'Symbolic Jacobian Assembly via CASprzak CAS Library',
            'Validated on 623-equation Aerothermodynamic Benchmark System',
        ]
        for i, feat in enumerate(feats):
            canvas.setFillColor(colors.HexColor('#b8cde4'))
            canvas.drawString(3.5*cm, H*0.27 - i*0.7*cm, feat)
        canvas.restoreState()

    return draw_cover


# ── Header / Footer ──────────────────────────────────────────────────────────
def on_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(C_NAVY)
    canvas.setFont('Helvetica', 7.5)
    canvas.drawString(2.5*cm, 1.5*cm, 'CMDSolver Technical Documentation')
    canvas.drawRightString(W - 2.5*cm, 1.5*cm, f'Page {doc.page}')
    canvas.setStrokeColor(C_BORDER)
    canvas.setLineWidth(0.4)
    canvas.line(2.5*cm, 1.8*cm, W - 2.5*cm, 1.8*cm)
    canvas.restoreState()


# ── Build story ───────────────────────────────────────────────────────────────
def build():
    out = '/home/claude/CMDSolver_docs/CMDSolver_Documentation.pdf'
    doc = SimpleDocTemplate(
        out, pagesize=A4,
        leftMargin=2.5*cm, rightMargin=2.5*cm,
        topMargin=2.5*cm, bottomMargin=2.5*cm,
        title='CMDSolver Technical Documentation',
        author='CMDSolver Development',
        subject='Nonlinear Equation System Solver for Aerothermodynamics',
    )
    story = []

    # ── COVER ──
    cover_fn = make_cover_page()
    # Use onFirstPage to draw the cover background
    story.append(pb())

    # ── TOC ──
    story += h1('Table of Contents')
    toc_items = [
        ('1.', 'Introduction', '3'),
        ('2.', 'Quick Start', '3'),
        ('3.', 'System Architecture', '4'),
        ('3.1', 'Parser Layer', '4'),
        ('3.2', 'Solver Strategy Pattern', '5'),
        ('3.3', 'GSPAR Sparse Solver Architecture', '5'),
        ('3.4', 'Thermodynamic Built-in Functions', '6'),
        ('4.', 'Newton-Armijo Solver', '6'),
        ('5.', 'Levenberg-Marquardt Solver', '7'),
        ('6.', 'Broyden Quasi-Newton Solver', '7'),
        ('7.', 'Homotopy / Arc-Length Continuation', '8'),
        ('8.', 'GSPAR Sparse LU Solver', '8'),
        ('9.', 'Command-Line Reference', '10'),
        ('10.', 'CAS File Format', '11'),
        ('11.', 'Development History', '12'),
        ('12.', 'Bug Fix Log', '13'),
        ('13.', 'Open Issues', '15'),
        ('14.', 'Lessons Learned', '17'),
        ('15.', 'Roadmap', '19'),
    ]
    toc_data = [[Paragraph(n, sTD), Paragraph(t, sTD), Paragraph(p, sTD)]
                for n, t, p in toc_items]
    toc_t = Table(toc_data, colWidths=[1.2*cm, 12.5*cm, 1.2*cm])
    toc_t.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 2),
        ('RIGHTPADDING', (0,0), (-1,-1), 2),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LINEBELOW', (0,-1), (-1,-1), 0.5, C_BORDER),
    ]))
    story.append(toc_t)
    story.append(pb())

    # ══════════════════════════════════════════════════════════════════════════
    # 1. INTRODUCTION
    # ══════════════════════════════════════════════════════════════════════════
    story += h1('Introduction', 1)
    story.append(body(
        'CMDSolver is a modular, command-line-driven solver for large nonlinear '
        'equation systems with a particular focus on aerothermodynamic process '
        'simulation. It follows the equation-oriented approach pioneered by '
        'simulators such as SpeedUp (later Aspen Technology): rather than solving '
        'component models sequentially, <i>all equations are solved simultaneously</i> '
        'as a single nonlinear system.'
    ))
    story.append(body(
        'The solver accepts equation systems described in a structured text format '
        '(.cas files), builds symbolic Jacobian matrices via the CASprzak computer '
        'algebra library, and provides multiple Newton-type solution strategies '
        'suitable for systems ranging from a few dozen to many hundreds of equations.'
    ))
    story.append(h2('Design Goals'))
    story += bullet([
        'Equation-oriented simulation of complex aerothermodynamic systems (gas turbines, jet engines, mixers, nozzles)',
        'Robustness under poor initial conditions and near-singular Jacobians (κ ~ 10<super>14</super>)',
        'Pluggable solver strategy pattern — solvers are interchangeable at runtime via -S: flag',
        'Transparent logging and diagnostic output (solver.log)',
        'Extensibility towards block-structured large sparse systems (n > 10,000)',
    ])
    story.append(spacer(8))
    story.append(make_table(
        ['Dependency', 'Version', 'Purpose'],
        [
            ['CASprzak', '0.3.0', 'Symbolic differentiation for Jacobian construction'],
            ['GraalVM / JDK', '25 (user), 21 JRE (CI)', 'Java runtime'],
            ['GSPAR', 'Grund/WIAS Berlin ~1994', 'Sparse LU factorisation (ported from Fortran)'],
        ],
        colW=[3.5*cm, 4.5*cm, 8.5*cm]
    ))

    # ══════════════════════════════════════════════════════════════════════════
    # 2. QUICK START
    # ══════════════════════════════════════════════════════════════════════════
    story += h1('Quick Start', 2)
    story.append(h2('Basic Solve'))
    story.append(code('java CASSolver -I:engine.cas'))
    story.append(h2('Solver Selection'))
    story.append(code(
        '# Newton with Armijo line search (default)\n'
        'java CASSolver -I:engine.cas -S:NEWTON_ARMIJO\n\n'
        '# Levenberg-Marquardt\n'
        'java CASSolver -I:engine.cas -S:LEVENBERG_MARQUARDT\n\n'
        '# GSPAR sparse LU (recommended for n > 200)\n'
        'java CASSolver -I:engine.cas -S:NEWTON_SPARSE\n\n'
        '# Homotopy for critical Ma=1 transitions\n'
        'java CASSolver -I:nozzle.cas -S:HOMOTOPY -SH:CRITICAL'
    ))
    story.append(h2('Output'))
    story.append(body(
        'Results are written to <code>solver.log</code> in the working directory and '
        'to stdout. Each iteration logs the current residual norm fsum and iteration '
        'counter ITER. The log level is INFO by default.'
    ))
    story.append(pb())

    # ══════════════════════════════════════════════════════════════════════════
    # 3. ARCHITECTURE
    # ══════════════════════════════════════════════════════════════════════════
    story += h1('System Architecture', 3)
    story.append(code(
        'cmd/\n'
        '  CASSolver.java              <- Entry point, CLI argument parsing\n\n'
        'apps/eqnParser/\n'
        '  EqnSysReader.java           <- .cas file parser (lexer + state machine)\n'
        '  EqnData.java                <- Single equation / init-data record\n'
        '  EqnSystem.java              <- Jacobian assembly, derivative matrix\n'
        '  SystemData.java             <- Parsed system: variables + equations\n'
        '  InitGuessApplier.java       <- Applies INIT block start values\n'
        '  SolverLogger.java           <- Centralised logging facade\n'
        '  SolverException.java        <- Exception hierarchy\n\n'
        '  buildInFunctions/\n'
        '    BIfunctions.java          <- ~80 thermodynamic built-in functions\n'
        '    ThermoConstants.java      <- JANAF/ISA physical constants\n\n'
        '  matrix/\n'
        '    MatrixSimple.java         <- Dense n x n matrix + Gauss-Jordan solver\n'
        '    DerivativeMatrix.java     <- Symbolic derivative table\n\n'
        '  solver/\n'
        '    AbstractSolver.java       <- Common infrastructure\n'
        '    NewtonArmijoSolver.java   <- Newton + Armijo line search\n'
        '    LevenbergMarquardtSolver  <- LM with adaptive damping\n'
        '    BroydenSolver.java        <- Rank-1 Broyden quasi-Newton\n'
        '    HomotopySolver.java       <- Arc-length continuation\n'
        '    GSPARSolver.java          <- Newton + GSPAR sparse LU\n\n'
        '    gspar/\n'
        '      SparseMatrix.java       <- CSR format + buildFromTriplets\n'
        '      GSPARWorkspace.java     <- Internal LU arrays\n'
        '      GSPAR.java              <- Core: factorize, solve, estimateCondition\n'
        '      GSPARPseudoCode.java    <- Pseudo-code generation + interpretation'
    ))

    story.append(h2('3.1 Parser Layer'))
    story.append(body(
        'The parser implements a line-by-line state machine in EqnSysReader. '
        'It reads .cas files and populates an EqnSysReaderDataBlock which is then '
        'finalised into a SystemData object. After parsing, unused variables are '
        'identified and removed — keeping the Jacobian as sparse as possible and '
        'forming the foundation for future hierarchical dot-notation variable names.'
    ))
    story.append(body(
        'Symbolic derivatives are computed once via CASprzak\'s FunctionParser '
        'and stored in a DerivativeMatrix. The Jacobian is evaluated numerically '
        'each iteration by substituting current variable values.'
    ))

    story.append(h2('3.2 Solver Strategy Pattern'))
    story.append(body(
        'All solvers extend AbstractSolver which provides evaluateF(), '
        'buildJacobian(), applyStep(), PhysicalProjector (bound clamping), '
        'and ResidualNormalizer. Concrete solvers override only computeStep() '
        'which returns the Newton step vector dx.'
    ))
    story.append(make_table(
        ['Component', 'Class', 'Responsibility'],
        [
            ['Strategy Interface', 'SolverStrategy', 'solve(SystemData, boolean) : List<OutputVariable>'],
            ['Configuration', 'SolverConfig', 'Immutable builder-pattern: tolerance, maxIter, pivot strategy'],
            ['Factory', 'SolverFactory', 'SolverType enum → SolverStrategy instance'],
            ['Infrastructure', 'AbstractSolver', 'evaluateF, buildJacobian, applyStep, PhysicalProjector'],
        ],
        colW=[3.5*cm, 4.5*cm, 8.5*cm]
    ))

    story.append(h2('3.3 GSPAR Sparse Solver Architecture'))
    story.append(make_table(
        ['Phase', 'When', 'Cost', 'Methods'],
        [
            ['Structure analysis', 'Once (first iteration)', 'O(nnz · fill-in)', 'dllugc → dllugb → dlluga → dllugd → dldsp1'],
            ['Numerical solve', 'Every Newton iteration', 'O(nnz)', 'dlfatr → dldint (pseudo-code) → dlsint'],
        ],
        colW=[3.5*cm, 3.5*cm, 3.5*cm, 6*cm]
    ))
    story.append(pb())

    # ══════════════════════════════════════════════════════════════════════════
    # 4-8: SOLVERS
    # ══════════════════════════════════════════════════════════════════════════
    story += h1('Newton-Armijo Solver', 4)
    story.append(body('<b>Flag:</b> <code>-S:NEWTON_ARMIJO</code> (default)'))
    story.append(body(
        'Classical Newton-Raphson with Armijo backtracking line search. '
        'Each iteration: (1) Build full Jacobian J(x<sub>k</sub>), '
        '(2) Solve J·dx = −F via Gauss-Jordan, '
        '(3) Armijo search for step size α, '
        '(4) Update x<sub>k+1</sub> = x<sub>k</sub> + α·dx.'
    ))
    story.append(callout(
        '<b>Verified:</b> Converges on the 623-equation aerothermodynamic benchmark '
        'in ~12 iterations — 2 more than the pre-refactoring version. '
        'The extra iterations are the overhead of the Armijo line search, which '
        'provides global convergence guarantees absent in the original damped Newton.',
        C_OK, colors.HexColor('#28a745')
    ))

    story += h1('Levenberg-Marquardt Solver', 5)
    story.append(body('<b>Flag:</b> <code>-S:LEVENBERG_MARQUARDT</code>'))
    story.append(body(
        'Adaptive damping strategy. Solves the modified system '
        '(J<super>T</super>J + μI)·dx = −J<super>T</super>·F where μ is adapted '
        'via the gain ratio ρ = actual reduction / predicted reduction. '
        'Recommended for systems near a sonic transition (Ma → 1) where the '
        'Jacobian becomes singular. μ is reduced by 1/3 on good steps and '
        'multiplied by 4 on rejected steps.'
    ))

    story += h1('Broyden Quasi-Newton Solver', 6)
    story.append(body('<b>Flag:</b> <code>-S:BROYDEN</code>'))
    story.append(body(
        'Rank-1 Broyden update avoids full Jacobian rebuilds between resets. '
        'The update: J<sub>k+1</sub> = J<sub>k</sub> + (y<sub>k</sub> − J<sub>k</sub>·s<sub>k</sub>) · '
        's<sub>k</sub><super>T</super> / (s<sub>k</sub><super>T</super>·s<sub>k</sub>), '
        'where s<sub>k</sub> = x<sub>k+1</sub> − x<sub>k</sub> and '
        'y<sub>k</sub> = F(x<sub>k+1</sub>) − F(x<sub>k</sub>).'
    ))
    story.append(callout(
        '<b>⚠ Current Limitation:</b> Broyden diverges on the 623-equation benchmark '
        'with multi-step updates because κ(J) ≈ 10<super>14</super> causes the rank-1 updates to '
        'corrupt the descent direction after one step. With broydenResetInterval=1 '
        '(the current default), Broyden reduces to Newton-Armijo and converges correctly. '
        'Root fix requires GMRES as the inner linear solver — see Open Issues §13.1.',
        C_WARN, colors.HexColor('#ffc107')
    ))

    story += h1('Homotopy / Arc-Length Continuation', 7)
    story.append(body('<b>Flag:</b> <code>-S:HOMOTOPY</code>'))
    story.append(body(
        'Embeds the original system F(x) = 0 into a parameter family '
        'H(x,t) = (1−t)·F(x<sub>0</sub>) + t·F(x) = 0 and traces the solution path '
        'from t=0 to t=1 using arc-length parameterisation to navigate past '
        'turning points. Each step: predictor (tangent direction) + corrector '
        '(inner Newton solve). Ideal for systems with critical parameter transitions.'
    ))

    story += h1('GSPAR Sparse LU Solver', 8)
    story.append(body('<b>Flag:</b> <code>-S:NEWTON_SPARSE</code>'))
    story.append(body(
        'Newton\'s method using the GSPAR sparse LU factoriser '
        '(Prof. Friedrich Grund, WIAS Berlin, ~1994). For n=623 equations '
        'with ~10 non-zeros per row, the Jacobian density is only ~1.6%, '
        'making sparse methods approximately 50× faster than dense Gauss-Jordan.'
    ))
    story.append(h3('Pivot Strategies'))
    story.append(make_table(
        ['MPIV', 'Name', 'Description'],
        [
            ['1 (default)', 'MIN_FILL', 'Minimize fill-in, O(N·M) cost analysis'],
            ['2', 'MARKOWITZ', 'Markowitz cost minimisation'],
            ['3', 'COLUMN', 'Column pivoting'],
            ['4', 'NONE', 'No pivoting (fastest, least robust)'],
        ],
        colW=[2.5*cm, 3.5*cm, 10.5*cm]
    ))
    story.append(h3('Fortran Bug Fixes Applied During Porting'))
    story.append(make_table(
        ['#', 'Routine', 'Original Bug', 'Fix', 'Source'],
        [
            ['1', 'DLDPCY', 'j+(icr(j)+1)*2+1', '+2 instead of +1', 'Borchardt 01.07.1998'],
            ['2', 'DLLUGE', 'NWOR ≥ 10·N+4·MA', '11·N+4·MA', 'Borchardt 10.06.1996'],
            ['3', 'DLLUGB', 'KOSTEN = N·N', 'Integer.MAX_VALUE', 'Borchardt 10.06.1996'],
            ['4', 'DLLUGE IPAR(9)', '10·N+4·MLU', '11·N+4·MLU', 'Borchardt 10.06.1996'],
            ['5', 'DLSOLA', 'X(I)=B(I) after DLSOLK overwrote backward substitution', 'Removed', 'Independent'],
            ['6', 'DLNORI', 'Missing JE≠0 guard before ILU[JE]', 'Added while-loop guard', 'Independent'],
        ],
        colW=[0.7*cm, 2.5*cm, 5*cm, 4*cm, 4.3*cm]
    ))
    story.append(pb())

    # ══════════════════════════════════════════════════════════════════════════
    # 9. CLI REFERENCE
    # ══════════════════════════════════════════════════════════════════════════
    story += h1('Command-Line Reference', 9)

    story.append(h2('Input / Output (alle Solver)'))
    story.append(make_table(
        ['Flag', 'Beschreibung'],
        [
            ['-I:<file>', 'Pflicht. *.cas/*.dat = Single-Run; *.csv = Batch-Mode (automatisch)'],
            ['-U:<file>', 'Variable-Update-Datei — überschreibt Werte/Bounds aus der CAS-Datei'],
            ['-C:<file>', 'CAS-Basismodell für Batch-Mode'],
            ['-DV:<file>', 'Startvektordump im -U Format'],
            ['-h', 'Hilfe ausgeben und beenden'],
        ],
        colW=[4*cm, 12*cm]
    ))

    story.append(h2('Solver-Auswahl (-S:)'))
    story.append(make_table(
        ['Flag', 'Solver', 'Skalierung'],
        [
            ['-S:NEWTON_ARMIJO', 'Newton-Raphson + Armijo (Standard)', 'NONE'],
            ['-S:BROYDEN', 'Broyden Quasi-Newton adaptiv', 'NONE'],
            ['-S:LEVENBERG_MARQUARDT', 'Levenberg-Marquardt', 'DIAGONAL'],
            ['-S:HOMOTOPY', 'Homotopie / Arc-Length', 'DIAGONAL (LM)'],
            ['-S:NEWTON_SPARSE', 'Newton + GSPAR Sparse LU', 'NONE'],
        ],
        colW=[5.5*cm, 7*cm, 3.5*cm]
    ))

    story.append(h2('Allgemeine Optionen (alle Solver)'))
    story.append(make_table(
        ['Flag', 'Beschreibung'],
        [
            ['-SN', 'Relative Residuumsnormierung ||F||/||F(x0)||'],
            ['-SC:NONE', 'Keine Skalierung (Default Newton/Broyden/Sparse)'],
            ['-SC:DIAGONAL', 'Diagonale Jacobi-Skalierung (Default LM/Homotopy)'],
            ['-DI', 'Startwert-Diagnose + Optimierung: Residuumsdiagnose, uninit. Variablen, Propagation, Sensitivität'],
        ],
        colW=[4*cm, 12*cm]
    ))

    story.append(h2('Broyden-Optionen (-S:BROYDEN)'))
    story.append(make_table(
        ['Flag', 'Default', 'Beschreibung'],
        [
            ['-SB:RESET=n', '1', 'Jacobi-Reset-Intervall. 10 = adaptiver Broyden-Modus'],
            ['-SB:KAPPA=x', '1e12', 'Konditionszahl-Schwelle für erzwungenen Rebuild'],
        ],
        colW=[4.5*cm, 2.5*cm, 9*cm]
    ))

    story.append(h2('Homotopie-Optionen (-S:HOMOTOPY)'))
    story.append(make_table(
        ['Flag', 'Default', 'Beschreibung'],
        [
            ['-SH:STEPS=n', '10', 'Anzahl Fortsetzungsschritte t=0 bis 1'],
            ['-SH:DS=x', '0.1', 'Initiale Bogenlängen-Schrittweite'],
            ['-SH:INNER=typ', 'LM', 'Innerer Solver: NEWTON_ARMIJO, LEVENBERG_MARQUARDT, BROYDEN'],
            ['-SH:CRITICAL', '—', 'Preset für Ma=1 Übergänge: 50 Schritte, ds=0.02'],
        ],
        colW=[4.5*cm, 2.5*cm, 9*cm]
    ))

    story.append(h2('Batch-Mode Optionen (-I:*.csv)'))
    story.append(make_table(
        ['Flag', 'Beschreibung'],
        [
            ['-BA', 'Alle Variablen ausgeben (auch Fixed). Default: nur freie.'],
            ['-C:<file>', 'CAS-Basismodell (alternativ: gleichnamige *.cas neben *.csv)'],
        ],
        colW=[4*cm, 12*cm]
    ))

    story.append(h2('Kombinations-Übersicht'))
    story.append(make_table(
        ['Solver', 'Kompatible Zusatz-Flags'],
        [
            ['NEWTON_ARMIJO', '-SN, -SC:*, -DI, -U, -DV'],
            ['BROYDEN', '-SB:RESET, -SB:KAPPA, -SN, -SC:*, -DI, -U, -DV'],
            ['LEVENBERG_MARQUARDT', '-SN, -SC:*, -DI, -U, -DV'],
            ['HOMOTOPY', '-SH:STEPS, -SH:DS, -SH:INNER, -SH:CRITICAL, -SN, -SC:*, -DI, -U'],
            ['NEWTON_SPARSE', '-SN, -SC:*, -DI, -U, -DV'],
            ['Batch (*.csv)', '-C, -BA, -S:*, -SN, -SC:*'],
        ],
        colW=[5*cm, 11*cm]
    ))

    story += h1('CAS File Format', 10)
    story.append(body(
        'The .cas format is a structured text language parsed by EqnSysReader. '
        'Variables are declared with full metadata; equations are written in '
        'implicit form F(x)=0 using standard mathematical notation with built-in '
        'function calls.'
    ))
    story.append(code(
        'VARIABLE\n'
        '  T_in AS REAL(Value:288.15; Unit:[K]; Lower:200; Upper:2000;)\n'
        '  p_in AS REAL(Value:101325; Unit:[Pa]; Lower:1; Upper:1e7;)\n'
        '  Ma   AS REAL(Value:0.5;   Unit:[-]; Lower:0;  Upper:10;)\n'
        '  T_st AS REAL(Value:270;   Unit:[K]; Status:Fixed)\n'
        'END\n\n'
        'EQUATION\n'
        '  T_st = T_in / (1 + (GAMMA-1)/2 * Ma^2);\n'
        'END\n\n'
        'INIT\n'
        '  T_in: Value=290; Lower=200; Upper=2000;\n'
        'END'
    ))
    story.append(make_table(
        ['Block Keyword', 'Purpose'],
        [
            ['VARIABLE … END', 'Variable declarations with name, value, bounds, unit, status'],
            ['EQUATION … END', 'Equations in implicit form (left − right = 0)'],
            ['INIT … END', 'Initial guess overrides — applied before solve via InitGuessApplier'],
            ['PROCEDURE … END', 'Built-in thermodynamic function call block'],
            ['FOR … END', 'Loop expansion for array-indexed variables'],
            ['IF … ELSE … END', 'Conditional equations (active based on current values)'],
        ],
        colW=[4.5*cm, 12*cm]
    ))
    story.append(pb())

    # ══════════════════════════════════════════════════════════════════════════
    # 11. DEVELOPMENT HISTORY
    # ══════════════════════════════════════════════════════════════════════════
    story += h1('Development History', 11)

    story.append(h2('Phase 1 — Original Monolithic Solver'))
    story.append(body(
        'The original codebase consisted of a single EqnSystem.java with all parsing, '
        'Jacobian assembly, and Newton iteration inlined. The solver used a damped Newton '
        'method without line search and was tightly coupled to the Swing GUI.'
    ))
    story += bullet([
        'GUI-coupled: solver code imported Swing classes (HTMLDocument, JTextPane)',
        'Fixed-point damping (0.5–1.0) instead of adaptive line search',
        'All variables tracked by name string — aliases not separated from names',
        'No exception hierarchy — errors returned as status flags',
        'Broyden variant (NewtonBroydenGMRES) existed as a separate class using GMRES',
    ])

    story.append(h2('Phase 2 — Structural Refactoring'))
    story.append(body('Concerns separated into distinct classes:'))
    story += bullet([
        'InitGuessApplier extracted from EqnSystem.run()',
        'EqnSysReaderGui separated from backend EqnSysReader (no Swing imports in backend)',
        'SolverLogger introduced as a centralised java.util.logging facade',
        'SolverException hierarchy: ParseException, SystemDimensionException, SolverRuntimeException, SingularJacobianException, NaNException',
    ])

    story.append(h2('Phase 3 — Strategy Pattern and New Solvers'))
    story.append(body(
        'The solver was completely rewritten using the Strategy pattern. New solvers '
        'implemented: NewtonArmijoSolver, LevenbergMarquardtSolver, BroydenSolver, '
        'HomotopySolver. AbstractSolver provides shared infrastructure. '
        'SolverConfig (builder pattern) encapsulates all parameters. '
        'SolverFactory maps SolverType → SolverStrategy.'
    ))

    story.append(h2('Phase 4 — GSPAR Sparse Solver Port'))
    story.append(body(
        'The 3,259-line Fortran GSPAR code (Grund, WIAS Berlin, ~1994) was ported to Java '
        'across four new classes: SparseMatrix, GSPARWorkspace, GSPAR, GSPARPseudoCode. '
        'The port included: CSR format with DLFASO/DLFATR, structure analysis with '
        'pivoting (DLLUGB), pseudo-code generation for LU, forward, and backward '
        'passes (DLDPCB/C/D/R/S/T/U/X/Y), and the pseudo-code interpreters '
        '(DLDINT, DLSINT). Six bugs from the original Fortran were corrected.'
    ))

    story.append(h2('Phase 5 — Bug Fixing and Stabilisation'))
    story.append(body(
        'Over 20 bugs were identified and fixed across the codebase — '
        'ranging from critical algorithmic errors (wrong map key in InitGuessApplier, '
        'race condition in parallel Jacobian) to subtle numerical issues '
        '(digit transposition in ISA pressure table, wrong exponent in nozzle area ratio). '
        'See the Bug Fix Log for the complete list.'
    ))
    story.append(pb())

    # ══════════════════════════════════════════════════════════════════════════
    # 12. BUG FIX LOG
    # ══════════════════════════════════════════════════════════════════════════
    story += h1('Bug Fix Log', 12)

    story.append(h2('Critical Algorithmic Bugs'))

    story.append(h3('BF-01: InitGuessApplier — Wrong Map Key'))
    story.append(callout(
        '<b>Severity: Critical.</b> The values HashMap uses variable aliases (e.g. \\x_0) '
        'as keys, not variable names. InitGuessApplier called values.replace(varName, value). '
        'Since varName is never a map key, replace() silently does nothing. All INIT block '
        'values were ignored. The solver ran with default values, not user-specified starting points. '
        '<b>Fix:</b> values.replace(varAlias, value).',
        C_ERR, C_ORANGE
    ))

    story.append(h3('BF-02: evaluateF() Timing — Frozen Residual'))
    story.append(callout(
        '<b>Severity: Critical.</b> fsum was computed from the old f vector (before applyStep), '
        'so the convergence monitor appeared frozen at the initial residual. '
        '<b>Fix:</b> evaluateF() is called after every applyStep().',
        C_ERR, C_ORANGE
    ))

    story.append(h3('BF-03: Jacobian Parallelisation Race Condition'))
    story.append(callout(
        '<b>Severity: Critical.</b> MatrixSimple.setValueAt() is not thread-safe. '
        'Parallel Jacobian construction (threshold n>50) caused silent non-deterministic '
        'data corruption — sometimes converging, sometimes diverging. '
        '<b>Fix:</b> PARALLEL_JACOBI_THRESHOLD = 99999 (disabled).',
        C_ERR, C_ORANGE
    ))

    story.append(h3('BF-04: Variable Scaling Applied to values Map'))
    story.append(callout(
        '<b>Severity: Critical.</b> VariableScaler.scaleValues() modified the same values '
        'map that evaluateF() reads. Thermodynamic functions received scaled values '
        '(p ≈ 1 Pa instead of 100,000 Pa), immediately producing NaN. '
        '<b>Fix:</b> scaleValues() call removed; feature disabled pending redesign.',
        C_ERR, C_ORANGE
    ))

    story.append(h2('Parser Bugs'))
    story.append(make_table(
        ['ID', 'Location', 'Description', 'Fix'],
        [
            ['BF-06', 'EqnSysReader', 'Array detection triggered by unit [m/s] in AS clause',
             'Check only part before " AS " using split(" as ")[0]'],
            ['BF-07', 'EqnData.setEquation()', '"ATANGES" typo in token split regex (3 places)',
             'Corrected to "ATANGENS"'],
            ['BF-08', 'EqnSysReaderDataBlock', 'getTmpProcDef() returns null → NullPointerException',
             'New initTmpProcDef(name) method that instantiates ProcDef first'],
            ['BF-09', 'EqnSysReader', 'Stray duplicate finally block outside method after inline expansion',
             'Removed stray block'],
        ],
        colW=[1.2*cm, 3.5*cm, 7*cm, 5*cm]
    ))

    story.append(h2('Thermodynamic Function Bugs'))
    story.append(make_table(
        ['ID', 'Location', 'Description', 'Fix'],
        [
            ['BF-10', 'BIfunctions L656', 'Nozzle area ratio: Math.pow(fac, -fac) used wrong exponent',
             'Math.pow(fac, -fac1) where fac1=(γ+1)/(2(γ−1))'],
            ['BF-11', 'BIfunctions L776', 'ISA pressure: 5474.583 Pa instead of 5474.853 Pa',
             'Digit transposition corrected'],
            ['BF-12', 'BIfunctions L778', 'ISA layer index initialised to 1 instead of -1',
             'int index = -1 (signals "not found")'],
        ],
        colW=[1.2*cm, 3.5*cm, 7*cm, 5*cm]
    ))
    story.append(pb())

    # ══════════════════════════════════════════════════════════════════════════
    # 13. OPEN ISSUES
    # ══════════════════════════════════════════════════════════════════════════
    story += h1('Open Issues', 13)

    story.append(h2('13.1 Broyden Quasi-Newton — Resolved via Adaptive Checkpoint/Rollback ✓'))
    story.append(callout(
        '<b>Status: Resolved.</b> '
        'Broyden with -S:BROYDEN -SB:RESET=10 converges in 11 iterations on the '
        '623-equation benchmark with only 2-3 Jacobian builds instead of 12.',
        C_OK, colors.HexColor('#28a745')
    ))
    story.append(body(
        'The root cause — κ ≈ 10<super>14</super> causing sign flip in gradF0 after rank-1 '
        'updates — is mitigated by the adaptive checkpoint/rollback strategy: on divergence '
        '(fsum &gt; 2 × checkpoint fsum) the solver restores the pre-update state and halves '
        'the interval. After 3 consecutive rollbacks it falls back to pure Newton.'
    ))
    story.append(body(
        '<b>Remaining improvement:</b> GMRES as inner linear solver would allow larger '
        'reset intervals without divergence risk. Current Gauss-Jordan is sufficient for the benchmark.'
    ))

    story.append(h2('13.2 Variable Scaling — Architecture Incomplete'))
    story.append(body(
        'Scaling flags -SC:DIAGONAL and -SC:UNIT_INTERVAL produce a warning and '
        'fall back to -SC:NONE. A correct scaling architecture requires consistent '
        'transformation throughout the entire solve loop: scale values → build Jacobian '
        'in scaled space → solve → unscale dx → unscale before thermodynamic calls. '
        'Step 5 conflicts with physical-unit requirements of thermodynamic functions.'
    ))

    story.append(h2('13.3 GMRES Linear Solver — Not Yet Implemented'))
    story.append(body(
        'GMRES is required as the inner linear solver for stable Broyden updates '
        'and ILU-preconditioned iterations on near-singular systems. The AbstractSolver '
        'architecture is designed to accept a pluggable linear solver — GMRES would '
        'slot in as an alternative to Gauss-Jordan and GSPAR in computeStep().'
    ))

    story.append(h2('13.4 Block-Structured Hierarchical Variable Names'))
    story.append(body(
        'The parser supports flat variable names only. Infrastructure for '
        'dot-notation hierarchy (e.g. turbine.stage1.T_in) is partially in place: '
        'unused variables are removed after parsing. Remaining work: LEX-based parser '
        'for nested SECTION…END blocks, automatic variable prefixing, and '
        'block-triangular decomposition via Tarjan SCC for solver ordering.'
    ))

    story.append(h2('13.5 Additional Pending Items'))
    story.append(make_table(
        ['Item', 'Status', 'Notes'],
        [
            ['Jacobian parallelisation', 'Disabled', 'MatrixSimple not thread-safe; threshold=99999'],
            ['Parser line numbers in errors', 'Pending', 'ParseException class ready; plumbing needed'],
            ['GSPAR first benchmark test', 'Pending', 'Compiles and verifies; awaiting runtime test'],
            ['ILU preconditioner for GMRES', 'Pending', 'GSPAR LU as natural preconditioner'],
            ['SolverState for op. point variation', 'Pending', 'Warm-start across -U file runs'],
            ['// line comments in parser', 'Pending', 'Minor parser extension'],
        ],
        colW=[5*cm, 3*cm, 8.5*cm]
    ))
    story.append(pb())

    # ══════════════════════════════════════════════════════════════════════════
    # 14. LESSONS LEARNED
    # ══════════════════════════════════════════════════════════════════════════
    story += h1('Lessons Learned', 14)

    lessons = [
        (
            '14.1 Scaling Cannot Be Added Incrementally',
            'The single most expensive mistake was attempting to add variable scaling '
            'as an optional layer on top of an existing architecture. Scaling is a global '
            'concern: the values map, the Jacobian, the line search, and the thermodynamic '
            'function evaluations must all agree on whether they operate in physical or '
            'scaled space. Retrofitting scaling required multiple iterations and ultimately '
            'the feature had to be disabled.',
            'Design scaling into the architecture from the start, or treat it as a complete system rewrite.'
        ),
        (
            '14.2 Adaptive Strategies Outperform Fixed Strategies Under Uncertainty',
            'The initial Broyden implementation diverged with fixed multi-step updates on a '
            '623-equation system with κ ≈ 10e14. Rather than replacing the entire solver, '
            'an adaptive checkpoint/rollback strategy resolved the instability: start conservative '
            '(interval=1, = Newton), probe aggressively (increase interval on good steps), '
            'rollback safely (restore checkpoint on divergence, halve interval). '
            'Result: 11 vs 12 iterations, 2-3 vs 12 Jacobian builds on the benchmark.',
            'Adaptive strategies that degrade gracefully under failure outperform fixed strategies '
            'that assume ideal behaviour. Start conservative, probe aggressively, rollback safely.'
        ),
        (
            '14.3 HashMap.replace() Fails Silently on Missing Keys',
            'HashMap.replace(key, value) returns null and does nothing if the key does not '
            'exist — no exception, no warning. This caused BF-01 where all initial values '
            'were silently discarded. The system appeared to run correctly but used default '
            'variable values throughout.',
            'Prefer put() over replace() unless "key missing → do nothing" is explicitly desired. '
            'Add assertion or LOG.warning when replace() returns null.'
        ),
        (
            '14.4 Thread Safety Must Be Verified Before Enabling Parallelism',
            'Enabling parallel Jacobian construction without verifying thread-safety of '
            'MatrixSimple.setValueAt() caused silent non-deterministic data corruption (BF-03). '
            'The corruption was intermittent — sometimes the solver converged, sometimes diverged '
            '— making it extremely hard to diagnose.',
            'Never add parallelism to shared mutable state without explicit synchronisation analysis. '
            'Non-deterministic bugs are the hardest to find.'
        ),
        (
            '14.5 Fortran Port — Sentinel Values and Index Conventions',
            'Fortran uses 1-based array indexing and uses 0 as a sentinel (end of chain). '
            'Java uses 0-based indexing. Converting GSPAR required systematically shifting all '
            'array accesses by -1 and replacing sentinel 0 with -1. Missing even one conversion '
            'causes silent out-of-bounds access in the linked-list traversals.',
            'Define a conversion convention before starting a Fortran port and enforce it '
            'mechanically throughout — especially for pointer-like linked-list sentinel values.'
        ),
        (
            '14.6 Debug Logging Invaluable for Convergence Diagnosis',
            'Adding LOG.info("DEBUG Iter %d: fsum=%.3e ||dx||=%.3e") immediately revealed '
            'two separate bugs: the frozen fsum (BF-02, evaluateF timing) and the Broyden '
            'sign flip. Without this, both would have been dismissed as "solver does not '
            'converge" without actionable diagnosis.',
            'Instrument convergence loops with detailed per-iteration logging from the beginning, '
            'not as an afterthought. The cost is negligible; the diagnostic value is enormous.'
        ),
        (
            '14.7 The Equation-Oriented Approach Scales — Sequential-Modular Does Not',
            'The SpeedUp/Aspen approach of solving all equations simultaneously is the right '
            'architecture for complex coupled aerothermodynamic systems. Sequential-modular '
            'simulation (solve component by component) breaks down for systems with strong '
            'recycle streams and feedback loops. CMDSolver\'s equation-oriented design handles '
            'these naturally without special recycle handling logic.',
            'For tightly coupled systems, invest in the equation-oriented infrastructure upfront '
            '— it pays back immediately in generality and robustness.'
        ),
        (
            '14.8 Symbolic Differentiation Accurate but Needs Analytical Complement',
            'CASprzak provides exact symbolic derivatives, eliminating finite-difference errors. '
            'However, it cannot differentiate built-in procedure calls (cpOfT, htofTTref, etc.). '
            'These require analytical derivative implementations in BIfunctions. '
            'Finite-difference fallback (adaptive h = max(10e-4·|x|, 10e-6)) was implemented '
            'for the 19 locations where symbolic derivatives are unavailable.',
            'CAS-based differentiation is excellent for algebraic equations. '
            'Supplement with carefully implemented analytical derivatives for complex built-in functions.'
        ),
    ]

    for title, desc, lesson in lessons:
        story.append(KeepTogether([
            h3(title),
            body(desc),
            callout(f'<b>Lesson:</b> {lesson}', C_INFO, C_BLUE),
            spacer(6),
        ]))

    story.append(pb())

    # ══════════════════════════════════════════════════════════════════════════
    # 15. ROADMAP
    # ══════════════════════════════════════════════════════════════════════════
    story += h1('Roadmap', 15)
    story.append(make_table(
        ['Priority', 'Item', 'Status', 'Notes'],
        [
            ['P1', 'Test GSPAR on 623-eq benchmark', 'Pending', 'First real-world validation of Java GSPAR port'],
            ['P1', 'GMRES linear solver', 'Pending', 'Required for stable Broyden; architecture ready'],
            ['P2', 'Broyden + GMRES integration', 'Pending', 'Replaces Gauss-Jordan in BroydenSolver'],
            ['P2', 'Variable scaling (redesign)', 'Pending', 'Transformer pattern around evaluateF()'],
            ['P2', 'Parser line numbers in errors', 'Pending', 'ParseException infrastructure ready'],
            ['P3', 'LEX hierarchical parser', 'Pending', 'Enables dot-notation, block structure, Tarjan SCC'],
            ['P3', 'ILU preconditioner for GMRES', 'Pending', 'GSPAR LU structure as natural preconditioner'],
            ['P3', 'Thread-safe Jacobian parallelism', 'Pending', 'Per-row local arrays; speedup for n>500'],
            ['P4', 'SolverState for op. point variation', 'Pending', 'Warm-start across -U runs'],
            ['P4', '// line comments in parser', 'Pending', 'Minor parser extension'],
        ],
        colW=[1.8*cm, 4.5*cm, 2.2*cm, 8*cm]
    ))

    story.append(spacer(20))
    story.append(rule(C_BORDER, 0.5))
    story.append(Paragraph(
        'CMDSolver Technical Documentation  ·  Generated April 2026  ·  '
        'Package: apps.eqnParser  ·  46 Java source files  ·  GraalVM 25 / OpenJDK 21',
        S('Footer', 'Normal', fontSize=8, textColor=colors.HexColor('#6c757d'), alignment=TA_CENTER)
    ))

    def first_page(canvas, doc):
        cover_fn(canvas, doc)
    doc.build(story, onFirstPage=first_page, onLaterPages=on_page)
    print(f"PDF written to {out}")


if __name__ == '__main__':
    build()
