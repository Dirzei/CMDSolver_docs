#!/usr/bin/env python3
"""Translate solver_newton_armijo.html body to bilingual DE/EN.

This is the most detailed of the three remaining solver pages — covers
theory, math-block, flowchart SVG, pseudocode, file list, parameter table,
behavior table, limit notes, and example output.
"""
from pathlib import Path
import re as _re

p = Path('/home/claude/build/solver_newton_armijo.html')
html = p.read_text(encoding='utf-8')

REPS = []
def pair(old, new): REPS.append((old, new))

# ── Nav ──
NAV = [
    ('theorie',       'Theorie',        'Theory'),
    ('flussdiagramm', 'Flussdiagramm',  'Flow chart'),
    ('pseudocode',    'Pseudocode',     'Pseudocode'),
    ('dateien',       'Dateien',        'Files'),
    ('parameter',     'Parameter',      'Parameters'),
    ('verhalten',     'Verhalten',      'Behavior'),
    ('grenzen',       'Grenzen',        'Limits'),
    ('beispiel',      'Beispiel',       'Example'),
]
for anchor, de, en in NAV:
    pair(f'<a href="#{anchor}">{de}</a>',
         f'<a href="#{anchor}" data-lang="de">{de}</a>'
         f'<a href="#{anchor}" data-lang="en">{en}</a>')

# ── h2 ──
def h2(de, en):
    pair(f'<h2>{de}</h2>',
         f'<h2 data-lang="de">{de}</h2><h2 data-lang="en">{en}</h2>')

h2('Theoretischer Kontext',     'Theoretical context')
h2('Flussdiagramm',             'Flow chart')
h2('Pseudocode',                'Pseudocode')
h2('Wichtige Dateien',          'Key files')
h2('Konfigurationsparameter',   'Configuration parameters')
h2('Konvergenzverhalten',       'Convergence behavior')
h2('Bekannte Grenzen',          'Known limits')
h2('Typische Ausgabe',          'Typical output')

# ── h3 ──
def h3(de, en):
    pair(f'<h3>{de}</h3>',
         f'<h3 data-lang="de">{de}</h3><h3 data-lang="en">{en}</h3>')

h3('Grundidee — allgemein verständlich', 'Idea — in plain words')
h3('Mathematische Formulierung',         'Mathematical formulation')
h3('Jacobi-Matrix in CMDSolver',         'Jacobian matrix in CMDSolver')
h3('Konvergenzrate',                     'Convergence rate')
h3('CLI-Aufruf',                         'CLI invocation')
h3('SolverAPI',                          'SolverAPI')
h3('Wann funktioniert Newton-Armijo gut?',
   'When does Newton-Armijo work well?')

# ── Theorie section paragraphs ──
pair('<p>\n    Das Newton-Raphson-Verfahren löst ein nichtlineares Gleichungssystem\n    <strong>F(x) = 0</strong> iterativ. Die Idee ist einfach: Man approximiert\n    die krumme Funktion F lokal durch eine Gerade (die Tangente) und berechnet\n    wo diese Gerade die Nulllinie schneidet. Dieser Schnittpunkt ist der nächste\n    Versuchspunkt. Das wiederholt man bis die Funktion nahe genug an Null ist.\n  </p>',
     '<p data-lang="de">\n    Das Newton-Raphson-Verfahren löst ein nichtlineares Gleichungssystem\n    <strong>F(x) = 0</strong> iterativ. Die Idee ist einfach: Man approximiert\n    die krumme Funktion F lokal durch eine Gerade (die Tangente) und berechnet\n    wo diese Gerade die Nulllinie schneidet. Dieser Schnittpunkt ist der nächste\n    Versuchspunkt. Das wiederholt man bis die Funktion nahe genug an Null ist.\n  </p>'
     '<p data-lang="en">\n    Newton-Raphson solves a nonlinear equation system <strong>F(x) = 0</strong>\n    iteratively. The idea is simple: locally approximate the curved function F\n    by a straight line (the tangent) and compute where that line crosses zero.\n    That intersection is the next trial point. Repeat until the function is\n    close enough to zero.\n  </p>')

pair('<p>\n    Die <strong>Armijo-Liniensuche</strong> ist eine Sicherheitsbremse: Der reine\n    Newton-Schritt kann manchmal zu groß sein und die Lösung überspringen.\n    Armijo testet ob der volle Schritt das Residuum tatsächlich verkleinert —\n    wenn nicht, wird er halbiert und nochmal getestet, bis er "gut genug" ist.\n  </p>',
     '<p data-lang="de">\n    Die <strong>Armijo-Liniensuche</strong> ist eine Sicherheitsbremse: Der reine\n    Newton-Schritt kann manchmal zu groß sein und die Lösung überspringen.\n    Armijo testet ob der volle Schritt das Residuum tatsächlich verkleinert —\n    wenn nicht, wird er halbiert und nochmal getestet, bis er "gut genug" ist.\n  </p>'
     '<p data-lang="en">\n    The <strong>Armijo line search</strong> is a safety brake: the raw Newton\n    step can sometimes be too large and overshoot the solution. Armijo tests\n    whether the full step actually reduces the residual — if not, it is\n    halved and re-tested until it is "good enough".\n  </p>')

# math-block hi labels
def hi(de, en):
    pair(f'<span class="hi">{de}</span>',
         f'<span class="hi" data-lang="de">{de}</span>'
         f'<span class="hi" data-lang="en">{en}</span>')

hi('Ziel:',                 'Goal:')
hi('Schritt k:',            'Step k:')
hi('Jacobi-Matrix J(x):',   'Jacobian J(x):')

# math-block hi2 (Armijo-Bedingung)
pair('<span class="hi2">Armijo-Bedingung:</span>',
     '<span class="hi2" data-lang="de">Armijo-Bedingung:</span>'
     '<span class="hi2" data-lang="en">Armijo condition:</span>')

# math-block cmt comments
def cmt(de, en):
    pair(f'<span class="cmt">{de}</span>',
         f'<span class="cmt" data-lang="de">{de}</span>'
         f'<span class="cmt" data-lang="en">{en}</span>')

cmt('← lineares Gleichungssystem lösen', '← solve linear system')
cmt('← gedämpfter Update',               '← damped update')
cmt('← symbolisch via CASprzak',         '← symbolic via CASprzak')
cmt('← immer negativ → Abstieg garantiert',
    '← always negative → descent guaranteed')
cmt('← halbieren falls Bedingung verletzt',
    '← halve if condition violated')

# Jacobi description paragraphs
pair('<p>\n    Die Jacobi-Matrix wird <strong>symbolisch</strong> berechnet — nicht numerisch\n    via finite Differenzen. CASprzak differenziert jede Gleichung analytisch nach\n    jeder Variable. Das ist exakter und schneller als numerische Näherungen.\n    Der Aufbau erfolgt parallel über mehrere Threads (<code>AbstractSolver.buildJacobian()</code>).\n  </p>',
     '<p data-lang="de">\n    Die Jacobi-Matrix wird <strong>symbolisch</strong> berechnet — nicht numerisch\n    via finite Differenzen. CASprzak differenziert jede Gleichung analytisch nach\n    jeder Variable. Das ist exakter und schneller als numerische Näherungen.\n    Der Aufbau erfolgt parallel über mehrere Threads (<code>AbstractSolver.buildJacobian()</code>).\n  </p>'
     '<p data-lang="en">\n    The Jacobian is computed <strong>symbolically</strong> — not numerically\n    via finite differences. CASprzak differentiates every equation analytically\n    with respect to every variable. This is more accurate and faster than\n    numerical approximations. Assembly is parallelized over several threads\n    (<code>AbstractSolver.buildJacobian()</code>).\n  </p>')

pair('<p>\n    Die Konditionszahl κ der Jacobi wird in jedem Schritt geschätzt. Bei κ > 10¹²\n    wird eine Warnung ausgegeben und der Wechsel zu Levenberg-Marquardt empfohlen.\n  </p>',
     '<p data-lang="de">\n    Die Konditionszahl κ der Jacobi wird in jedem Schritt geschätzt. Bei κ > 10¹²\n    wird eine Warnung ausgegeben und der Wechsel zu Levenberg-Marquardt empfohlen.\n  </p>'
     '<p data-lang="en">\n    The condition number κ of the Jacobian is estimated at every step. When\n    κ > 10¹² a warning is issued and switching to Levenberg-Marquardt is\n    recommended.\n  </p>')

pair('<p>\n    In der Nähe der Lösung konvergiert Newton-Raphson <strong>quadratisch</strong>:\n    Wenn der Fehler im Schritt k gleich ε ist, ist er im Schritt k+1 proportional\n    zu ε². Das erklärt warum typische Systeme in 3-5 Iterationen konvergieren —\n    jede Iteration verdoppelt ungefähr die Anzahl korrekter Dezimalstellen.\n  </p>',
     '<p data-lang="de">\n    In der Nähe der Lösung konvergiert Newton-Raphson <strong>quadratisch</strong>:\n    Wenn der Fehler im Schritt k gleich ε ist, ist er im Schritt k+1 proportional\n    zu ε². Das erklärt warum typische Systeme in 3-5 Iterationen konvergieren —\n    jede Iteration verdoppelt ungefähr die Anzahl korrekter Dezimalstellen.\n  </p>'
     '<p data-lang="en">\n    Near the solution, Newton-Raphson converges <strong>quadratically</strong>:\n    if the error at step k is ε, then at step k+1 it is proportional to ε².\n    This is why typical systems converge in 3–5 iterations — each iteration\n    roughly doubles the number of correct decimal digits.\n  </p>')

# ── Flowchart SVG: duplicate for DE/EN ──
DE_FLOW_RE = _re.compile(r'(<div class="flowchart">\s*<svg[^>]*>.*?</svg>\s*</div>)', _re.DOTALL)
m = DE_FLOW_RE.search(html)
if m:
    de_flow = m.group(1)
    en_flow = de_flow
    SVG_REPLACEMENTS = [
        ('Startwerte laden',          'Load starting values'),
        ('── Iterationsschleife ──',  '── Iteration loop ──'),
        ('Jacobi-Matrix aufbauen',    'Build Jacobian matrix'),
        ('buildJacobian() — symbolisch, parallel',
                                       'buildJacobian() — symbolic, parallel'),
        ('Konditionszahl',            'Condition number'),
        ('LOG.warning',               'LOG.warning'),
        ('Newton-Schritt berechnen',  'Compute Newton step'),
        ('Armijo-Liniensuche',        'Armijo line search'),
        ('α anpassen bis Bedingung erfüllt',
                                       'adjust α until condition is met'),
        ('PhysicalProjector (Bounds)','PhysicalProjector (bounds)'),
        ('nein → nächste Iteration',  'no → next iteration'),
    ]
    for de, en in SVG_REPLACEMENTS:
        en_flow = en_flow.replace(de, en)
    en_flow = en_flow.replace('>ja</text>', '>yes</text>')
    en_flow = en_flow.replace('>nein</text>', '>no</text>')

    new_block = (
        '<div data-lang="de">' + de_flow + '</div>'
        '<div data-lang="en">' + en_flow + '</div>'
    )
    pair(de_flow, new_block)

# ── Pseudocode block: wrap with DE/EN ──
DE_PRE = '''<pre><span class="kw">function</span> <span class="fn">newton_armijo_solve</span>(F, x₀, tol, maxIter):

    x ← InitGuessApplier(x₀)       <span class="cmt">// Startwerte aus INITIALIZE-Block</span>
    
    <span class="kw">for</span> k = 0 <span class="kw">to</span> maxIter:
    
        <span class="cmt">// ── Jacobi aufbauen (parallel, symbolisch) ──</span>
        J ← buildJacobian(F, x)     <span class="cmt">// ∂Fᵢ/∂xⱼ via CASprzak</span>
        f ← F(x)                    <span class="cmt">// Residuumsvektor</span>
        
        <span class="cmt">// ── Konditionszahl schätzen ──</span>
        κ ← estimateCondition(J)
        <span class="kw">if</span> κ > 1e12: LOG.warning("ill-conditioned — consider LM")
        
        <span class="cmt">// ── Newton-Schritt ──</span>
        Δx ← −J⁻¹ · f              <span class="cmt">// lineares System lösen</span>
        
        <span class="cmt">// ── Armijo-Liniensuche ──</span>
        α ← 1.0                     <span class="cmt">// voller Schritt</span>
        slope ← −||f||²             <span class="cmt">// Abstiegsrichtung</span>
        <span class="kw">while</span> α > α_min:
            x_try ← x + α · Δx
            <span class="kw">if</span> ||F(x_try)||² ≤ ||f||² + c₁·α·slope:
                <span class="kw">break</span>            <span class="cmt">// Armijo-Bedingung erfüllt</span>
            α ← α · ρ              <span class="cmt">// Schritt halbieren (ρ = 0.5)</span>
        
        <span class="cmt">// ── Update ──</span>
        x ← x + α · Δx
        x ← PhysicalProjector(x)   <span class="cmt">// Bounds enforzen</span>
        
        <span class="cmt">// ── Konvergenzprüfung ──</span>
        fsum ← Σ|Fᵢ(x)|
        <span class="kw">if</span> fsum < tol:
            <span class="kw">return</span> CONVERGED, x, k, fsum
    
    <span class="kw">return</span> NOT_CONVERGED, x, maxIter, fsum</pre>'''

EN_PRE = '''<pre><span class="kw">function</span> <span class="fn">newton_armijo_solve</span>(F, x₀, tol, maxIter):

    x ← InitGuessApplier(x₀)       <span class="cmt">// starting values from INITIALIZE block</span>
    
    <span class="kw">for</span> k = 0 <span class="kw">to</span> maxIter:
    
        <span class="cmt">// ── Build Jacobian (parallel, symbolic) ──</span>
        J ← buildJacobian(F, x)     <span class="cmt">// ∂Fᵢ/∂xⱼ via CASprzak</span>
        f ← F(x)                    <span class="cmt">// residual vector</span>
        
        <span class="cmt">// ── Estimate condition number ──</span>
        κ ← estimateCondition(J)
        <span class="kw">if</span> κ > 1e12: LOG.warning("ill-conditioned — consider LM")
        
        <span class="cmt">// ── Newton step ──</span>
        Δx ← −J⁻¹ · f              <span class="cmt">// solve linear system</span>
        
        <span class="cmt">// ── Armijo line search ──</span>
        α ← 1.0                     <span class="cmt">// full step</span>
        slope ← −||f||²             <span class="cmt">// descent direction</span>
        <span class="kw">while</span> α > α_min:
            x_try ← x + α · Δx
            <span class="kw">if</span> ||F(x_try)||² ≤ ||f||² + c₁·α·slope:
                <span class="kw">break</span>            <span class="cmt">// Armijo condition met</span>
            α ← α · ρ              <span class="cmt">// halve step (ρ = 0.5)</span>
        
        <span class="cmt">// ── Update ──</span>
        x ← x + α · Δx
        x ← PhysicalProjector(x)   <span class="cmt">// enforce bounds</span>
        
        <span class="cmt">// ── Convergence check ──</span>
        fsum ← Σ|Fᵢ(x)|
        <span class="kw">if</span> fsum < tol:
            <span class="kw">return</span> CONVERGED, x, k, fsum
    
    <span class="kw">return</span> NOT_CONVERGED, x, maxIter, fsum</pre>'''

pair(DE_PRE,
     f'<div data-lang="de">{DE_PRE}</div><div data-lang="en">{EN_PRE}</div>')

pair('<div class="note blue">\n    <strong>Armijo-Parameter (Defaults):</strong>\n    <code>α_init = 1.0</code> · <code>α_min = 1e-8</code> ·\n    <code>c₁ = 1e-4</code> · <code>ρ = 0.5</code> (Halbierung)\n  </div>',
     '<div class="note blue" data-lang="de">\n    <strong>Armijo-Parameter (Defaults):</strong>\n    <code>α_init = 1.0</code> · <code>α_min = 1e-8</code> ·\n    <code>c₁ = 1e-4</code> · <code>ρ = 0.5</code> (Halbierung)\n  </div>'
     '<div class="note blue" data-lang="en">\n    <strong>Armijo parameters (defaults):</strong>\n    <code>α_init = 1.0</code> · <code>α_min = 1e-8</code> ·\n    <code>c₁ = 1e-4</code> · <code>ρ = 0.5</code> (halving)\n  </div>')

# ── Files section: file-desc divs (each ist different) ──
def file_desc(de_inner, en_inner):
    """Wrap a complete <div class='file-desc'>…</div> in DE/EN versions."""
    pair(f'<div class="file-desc">\n        {de_inner}\n      </div>',
         f'<div class="file-desc" data-lang="de">\n        {de_inner}\n      </div>'
         f'<div class="file-desc" data-lang="en">\n        {en_inner}\n      </div>')

file_desc('<strong>NewtonArmijoSolver.java</strong>\n        Implementiert <code>computeStep()</code> — berechnet J⁻¹·F und führt\n        Armijo-Backtracking durch. Enthält auch den Startvektor-Dump\n        (<code>-DV:</code> Option).\n        <br><code>apps/eqnParser/solver/NewtonArmijoSolver.java</code>',
          '<strong>NewtonArmijoSolver.java</strong>\n        Implements <code>computeStep()</code> — computes J⁻¹·F and performs\n        Armijo backtracking. Also contains the starting-vector dump\n        (<code>-DV:</code> option).\n        <br><code>apps/eqnParser/solver/NewtonArmijoSolver.java</code>')

file_desc('<strong>AbstractSolver.java</strong>\n        Basisklasse aller Solver. Enthält die Hauptiteration:\n        Jacobi aufbauen → <code>computeStep()</code> → Update → Konvergenzprüfung.\n        Stagnationserkennung und PhysicalProjector-Aufruf.\n        <br><code>apps/eqnParser/solver/AbstractSolver.java</code>',
          '<strong>AbstractSolver.java</strong>\n        Base class of all solvers. Contains the main iteration:\n        build Jacobian → <code>computeStep()</code> → update → convergence check.\n        Stagnation detection and PhysicalProjector call.\n        <br><code>apps/eqnParser/solver/AbstractSolver.java</code>')

file_desc('<strong>DerivativeMatrix.java</strong>\n        Aufbau der Jacobi-Matrix aus den CASprzak-Ableitungen.\n        Wird von <code>AbstractSolver.buildJacobian()</code> parallel aufgerufen.\n        <br><code>apps/eqnParser/matrix/DerivativeMatrix.java</code>',
          '<strong>DerivativeMatrix.java</strong>\n        Builds the Jacobian from the CASprzak derivatives. Called in parallel\n        by <code>AbstractSolver.buildJacobian()</code>.\n        <br><code>apps/eqnParser/matrix/DerivativeMatrix.java</code>')

file_desc('<strong>MatrixSimple.java</strong>\n        Dichte Matrixklasse mit <code>inverse()</code> — Gauss-Elimination.\n        Wird von Newton-Armijo für J⁻¹ verwendet. Bei großen Systemen\n        ineffizient → dann GSPAR-Variante verwenden.\n        <br><code>apps/eqnParser/matrix/MatrixSimple.java</code>',
          '<strong>MatrixSimple.java</strong>\n        Dense matrix class with <code>inverse()</code> — Gaussian elimination.\n        Used by Newton-Armijo for J⁻¹. Inefficient on large systems →\n        use the GSPAR variant in that case.\n        <br><code>apps/eqnParser/matrix/MatrixSimple.java</code>')

file_desc('<strong>PhysicalProjector.java</strong>\n        Projiziert Variablen nach jedem Update auf physikalisch gültige Werte\n        (T ≥ 1K, p ≥ 1Pa, etc.). Verhindert dass der Solver in physikalisch\n        unmögliche Bereiche läuft.\n        <br><code>apps/eqnParser/solver/PhysicalProjector.java</code>',
          '<strong>PhysicalProjector.java</strong>\n        Projects variables onto physically valid values after each update\n        (T ≥ 1K, p ≥ 1Pa, etc.). Prevents the solver from drifting into\n        physically impossible regions.\n        <br><code>apps/eqnParser/solver/PhysicalProjector.java</code>')

file_desc('<strong>ConditionEstimator.java</strong>\n        Schätzt die Konditionszahl κ der Jacobi. Klassifiziert als\n        GOOD / POOR / CRITICAL. Bei CRITICAL wird LM empfohlen.\n        <br><code>apps/eqnParser/solver/ConditionEstimator.java</code>',
          '<strong>ConditionEstimator.java</strong>\n        Estimates the condition number κ of the Jacobian. Classifies as\n        GOOD / POOR / CRITICAL. On CRITICAL, LM is recommended.\n        <br><code>apps/eqnParser/solver/ConditionEstimator.java</code>')

file_desc('<strong>SolverConfig.java</strong>\n        Konfigurationsklasse — Toleranz, maxIter, Armijo-Parameter,\n        Skalierungsstrategie. Wird über CLI-Argumente oder <code>SolverAPI</code>\n        gesetzt.\n        <br><code>apps/eqnParser/solver/SolverConfig.java</code>',
          '<strong>SolverConfig.java</strong>\n        Configuration class — tolerance, maxIter, Armijo parameters,\n        scaling strategy. Set via CLI arguments or <code>SolverAPI</code>.\n        <br><code>apps/eqnParser/solver/SolverConfig.java</code>')

# ── SolverAPI cmt comments ──
cmt('// Standard',  '// default')
cmt('// Standard', '// default')

# ── Parameter table ──
pair('<tr><th>Parameter</th><th>CLI</th><th>Default</th><th>Beschreibung</th></tr>',
     '<tr>'
     '<th>Parameter</th><th>CLI</th><th>Default</th>'
     '<th data-lang="de">Beschreibung</th><th data-lang="en">Description</th>'
     '</tr>')

def td_pair(de, en):
    pair(f'<td>{de}</td>', f'<td data-lang="de">{de}</td><td data-lang="en">{en}</td>')

td_pair('Konvergenzschwelle für ||F(x)||', 'Convergence threshold for ||F(x)||')
td_pair('Maximale Iterationszahl',         'Maximum number of iterations')
td_pair('Initialer Schrittweitenfaktor α', 'Initial step-size factor α')
td_pair('Minimaler α-Wert vor Abbruch',    'Minimum α before abort')
td_pair('Armijo-Konstante c₁ (Abstiegsbedingung)',
        'Armijo constant c₁ (descent condition)')
td_pair('Reduktionsfaktor ρ pro Backtracking-Schritt',
        'Reduction factor ρ per backtracking step')
td_pair('Startwertoptimierung vor dem Solve',
        'Starting-value optimization before solve')
td_pair('Startvektor in Datei schreiben (für Debugging)',
        'Write starting vector to file (for debugging)')

# ── Verhalten table ──
pair('<thead><tr><th>Situation</th><th>Verhalten</th><th>Empfehlung</th></tr></thead>',
     '<thead><tr>'
     '<th data-lang="de">Situation</th><th data-lang="en">Situation</th>'
     '<th data-lang="de">Verhalten</th><th data-lang="en">Behavior</th>'
     '<th data-lang="de">Empfehlung</th><th data-lang="en">Recommendation</th>'
     '</tr></thead>')

td_pair('Gut konditioniertes System (κ &lt; 10⁶)',
        'Well-conditioned system (κ &lt; 10⁶)')
td_pair('Standard-Wahl', 'Default choice')
td_pair('Guter Startvektor nahe der Lösung',
        'Good starting vector near the solution')
td_pair('Quadratische Konvergenz', 'Quadratic convergence')
td_pair('Mittelgroße Systeme (n &lt; 500)', 'Medium systems (n &lt; 500)')
td_pair('Dichte LU ist effizient', 'Dense LU is efficient')
td_pair('Schlecht konditioniert (κ &gt; 10¹²)',
        'Ill-conditioned (κ &gt; 10¹²)')
td_pair('→ Levenberg-Marquardt', '→ Levenberg-Marquardt')
td_pair('Schlechter Startvektor weit von Lösung',
        'Bad starting vector far from solution')
td_pair('→ -DI oder Homotopie', '→ -DI or homotopy')
td_pair('Große Systeme (n &gt; 500)', 'Large systems (n &gt; 500)')
td_pair('→ NEWTON_SPARSE_ARMIJO', '→ NEWTON_SPARSE_ARMIJO')

# Badge values that contain German words
def badge(klass, de, en):
    pair(f'<span class="badge {klass}">{de}</span>',
         f'<span class="badge {klass}" data-lang="de">{de}</span>'
         f'<span class="badge {klass}" data-lang="en">{en}</span>')

badge('b-ok',   '✅ Optimal',  '✅ Optimal')
badge('b-ok',   '✅ 3-5 Iter', '✅ 3-5 iter')
badge('b-ok',   '✅ Schnell',  '✅ Fast')
badge('b-warn', '⚠️ Instabil', '⚠️ Unstable')
badge('b-warn', '⚠️ Langsam', '⚠️ Slow')
badge('b-warn', '⚠️ Langsam', '⚠️ Slow')

# ── Grenzen section: 4 notes ──
pair('<div class="note red">\n    <strong>Singuläre Jacobi:</strong> Wenn J singulär ist (κ → ∞) wirft der Solver\n    eine <code>SingularJacobianException</code>. Das passiert typischerweise wenn\n    zwei Gleichungen identisch sind oder eine Variable in keiner Gleichung vorkommt.\n  </div>',
     '<div class="note red" data-lang="de">\n    <strong>Singuläre Jacobi:</strong> Wenn J singulär ist (κ → ∞) wirft der Solver\n    eine <code>SingularJacobianException</code>. Das passiert typischerweise wenn\n    zwei Gleichungen identisch sind oder eine Variable in keiner Gleichung vorkommt.\n  </div>'
     '<div class="note red" data-lang="en">\n    <strong>Singular Jacobian:</strong> when J is singular (κ → ∞) the solver\n    throws a <code>SingularJacobianException</code>. This typically happens when\n    two equations are identical or a variable does not appear in any equation.\n  </div>')

pair('<div class="note amber">\n    <strong>Lokale Konvergenz:</strong> Newton-Raphson konvergiert nur lokal —\n    der Startvektor muss nahe genug an der Lösung sein. Bei schlechten Startwerten\n    kann der Solver divergieren oder in einer falschen Lösung stecken bleiben.\n    <code>-DI</code> (Diagnose-Modus) verbessert den Startvektor automatisch.\n  </div>',
     '<div class="note amber" data-lang="de">\n    <strong>Lokale Konvergenz:</strong> Newton-Raphson konvergiert nur lokal —\n    der Startvektor muss nahe genug an der Lösung sein. Bei schlechten Startwerten\n    kann der Solver divergieren oder in einer falschen Lösung stecken bleiben.\n    <code>-DI</code> (Diagnose-Modus) verbessert den Startvektor automatisch.\n  </div>'
     '<div class="note amber" data-lang="en">\n    <strong>Local convergence:</strong> Newton-Raphson only converges locally —\n    the starting vector must lie close enough to the solution. With poor\n    starting values the solver can diverge or get stuck in a wrong solution.\n    <code>-DI</code> (diagnostic mode) improves the starting vector automatically.\n  </div>')

pair('<div class="note amber">\n    <strong>Dichte Jacobi:</strong> Die Matrixinversion kostet O(n³) —\n    für große Systeme (n &gt; 200) ist NEWTON_SPARSE_ARMIJO deutlich effizienter.\n  </div>',
     '<div class="note amber" data-lang="de">\n    <strong>Dichte Jacobi:</strong> Die Matrixinversion kostet O(n³) —\n    für große Systeme (n &gt; 200) ist NEWTON_SPARSE_ARMIJO deutlich effizienter.\n  </div>'
     '<div class="note amber" data-lang="en">\n    <strong>Dense Jacobian:</strong> the matrix inversion costs O(n³) —\n    for large systems (n &gt; 200) NEWTON_SPARSE_ARMIJO is significantly more\n    efficient.\n  </div>')

pair('<div class="note blue">\n    <strong>PhysicalProjector Interaktion:</strong> Wenn der Projektor aggressiv\n    eingreift (viele Bounds-Verletzungen) kann das die Konvergenz verlangsamen,\n    weil der effektive Schritt vom Newton-Schritt abweicht.\n  </div>',
     '<div class="note blue" data-lang="de">\n    <strong>PhysicalProjector Interaktion:</strong> Wenn der Projektor aggressiv\n    eingreift (viele Bounds-Verletzungen) kann das die Konvergenz verlangsamen,\n    weil der effektive Schritt vom Newton-Schritt abweicht.\n  </div>'
     '<div class="note blue" data-lang="en">\n    <strong>PhysicalProjector interaction:</strong> when the projector\n    intervenes aggressively (many bounds violations), convergence can slow\n    down because the effective step deviates from the Newton step.\n  </div>')

# ── Beispiel section: pre blocks and note green ──
pair('<pre><span class="cmt">// Erfolgreicher Lauf — SimpleSystem.cas</span>\nINFO: Starting Newton-Raphson + Armijo line search\n      [n=12, maxIter=100, tol=1.00e-07]\n\nINFO: --> Iter=0: ||F||= 2.3451e+03  max f[3]= 1.2e+03\nINFO: --> Iter=1: ||F||= 4.8721e+01  max f[3]= 3.1e+01\nINFO: --> Iter=2: ||F||= 2.1043e-04  max f[7]= 1.4e-04\nINFO: --> Iter=3: ||F||= 3.1623e-11  <span class="str">← Konvergenz</span>\nINFO: Converged at iter 3: fsum=3.162e-11 &lt; tol=1.00e-07</pre>',
     '<pre data-lang="de"><span class="cmt">// Erfolgreicher Lauf — SimpleSystem.cas</span>\nINFO: Starting Newton-Raphson + Armijo line search\n      [n=12, maxIter=100, tol=1.00e-07]\n\nINFO: --> Iter=0: ||F||= 2.3451e+03  max f[3]= 1.2e+03\nINFO: --> Iter=1: ||F||= 4.8721e+01  max f[3]= 3.1e+01\nINFO: --> Iter=2: ||F||= 2.1043e-04  max f[7]= 1.4e-04\nINFO: --> Iter=3: ||F||= 3.1623e-11  <span class="str">← Konvergenz</span>\nINFO: Converged at iter 3: fsum=3.162e-11 &lt; tol=1.00e-07</pre>'
     '<pre data-lang="en"><span class="cmt">// Successful run — SimpleSystem.cas</span>\nINFO: Starting Newton-Raphson + Armijo line search\n      [n=12, maxIter=100, tol=1.00e-07]\n\nINFO: --> Iter=0: ||F||= 2.3451e+03  max f[3]= 1.2e+03\nINFO: --> Iter=1: ||F||= 4.8721e+01  max f[3]= 3.1e+01\nINFO: --> Iter=2: ||F||= 2.1043e-04  max f[7]= 1.4e-04\nINFO: --> Iter=3: ||F||= 3.1623e-11  <span class="str">← convergence</span>\nINFO: Converged at iter 3: fsum=3.162e-11 &lt; tol=1.00e-07</pre>')

pair('<pre><span class="cmt">// Warnung bei schlechter Kondition</span>\nWARN: Iter   0: condition=POOR  kappa=4.62e+11 — ill-conditioned Jacobian\nWARN: Iter   0: Frobenius kappa=5.96e+23 [CRITICAL] — consider switching to LM</pre>',
     '<pre data-lang="de"><span class="cmt">// Warnung bei schlechter Kondition</span>\nWARN: Iter   0: condition=POOR  kappa=4.62e+11 — ill-conditioned Jacobian\nWARN: Iter   0: Frobenius kappa=5.96e+23 [CRITICAL] — consider switching to LM</pre>'
     '<pre data-lang="en"><span class="cmt">// Warning on poor conditioning</span>\nWARN: Iter   0: condition=POOR  kappa=4.62e+11 — ill-conditioned Jacobian\nWARN: Iter   0: Frobenius kappa=5.96e+23 [CRITICAL] — consider switching to LM</pre>')

pair('<div class="note green">\n    <strong>Testergebnis v2.5 (SimpleSystem.cas, 12 Gleichungen):</strong>\n    Status: CONVERGED · Iterationen: 3 · fsum: 3.1623e-11 · Zeit: ~40ms\n  </div>',
     '<div class="note green" data-lang="de">\n    <strong>Testergebnis v2.5 (SimpleSystem.cas, 12 Gleichungen):</strong>\n    Status: CONVERGED · Iterationen: 3 · fsum: 3.1623e-11 · Zeit: ~40ms\n  </div>'
     '<div class="note green" data-lang="en">\n    <strong>Test result v2.5 (SimpleSystem.cas, 12 equations):</strong>\n    Status: CONVERGED · Iterations: 3 · fsum: 3.1623e-11 · Time: ~40 ms\n  </div>')

# ── Footer (already standard pattern, just add data-lang) ──
pair('<span>CMDSolver Docs · Newton-Raphson + Armijo · v2.5</span>',
     '<span data-lang="de">CMDSolver Docs · Newton-Raphson + Armijo · v2.5</span>'
     '<span data-lang="en">CMDSolver Docs · Newton-Raphson + Armijo · v2.5</span>')
pair('<a href="index.html">← Übersicht</a>',
     '<a href="index.html" data-lang="de">← Übersicht</a>'
     '<a href="index.html" data-lang="en">← Overview</a>')
pair('<a href="solver_newton_sparse.html">Newton-GSPAR →</a>',
     '<a href="solver_newton_sparse.html" data-lang="de">Newton-GSPAR →</a>'
     '<a href="solver_newton_sparse.html" data-lang="en">Newton-GSPAR →</a>')

# Apply
missing = []
for i, (old, new) in enumerate(REPS):
    if old not in html: missing.append((i, old[:80])); continue
    html = html.replace(old, new, 1)

p.write_text(html, encoding='utf-8')
print(f'solver_newton_armijo.html: {len(REPS) - len(missing)} / {len(REPS)} replacements')
if missing:
    print('NOT FOUND:')
    for i, s in missing[:10]: print(f'  #{i}: {s!r}')
