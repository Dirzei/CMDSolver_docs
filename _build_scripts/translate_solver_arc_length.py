#!/usr/bin/env python3
"""Translate solver_arc_length.html body to bilingual DE/EN.

Also harmonizes the legacy <hr>+inline-styled <p> footer to match the
standard CMDSolver Docs footer pattern (same as solver_lm, solver_homotopy etc.).
"""
from pathlib import Path

p = Path('/home/claude/build/solver_arc_length.html')
html = p.read_text(encoding='utf-8')

REPS = []
def pair(old, new): REPS.append((old, new))

# ── Nav ──
NAV = [
    ('status',        'Status',                       'Status'),
    ('theorie',       'Theorie',                      'Theory'),
    ('flussdiagramm', 'Flussdiagramm',                'Flow chart'),
    ('pseudocode',    'Pseudocode',                   'Pseudocode'),
    ('dateien',       'Dateien',                      'Files'),
    ('verhalten',     'Verhalten auf NozzleSystem',   'Behavior on NozzleSystem'),
    ('grenzen',       'Grenzen',                      'Limits'),
]
for anchor, de, en in NAV:
    pair(f'<a href="#{anchor}">{de}</a>',
         f'<a href="#{anchor}" data-lang="de">{de}</a>'
         f'<a href="#{anchor}" data-lang="en">{en}</a>')

# ── h2 ──
def h2(de, en):
    pair(f'<h2>{de}</h2>',
         f'<h2 data-lang="de">{de}</h2><h2 data-lang="en">{en}</h2>')

h2('Status — wichtig zu lesen',         'Status — important to read')
h2('Theoretischer Kontext',             'Theoretical context')
h2('Flussdiagramm',                     'Flow chart')
h2('Pseudocode',                        'Pseudocode')
h2('Dateien',                           'Files')
h2('Verhalten auf NozzleSystem (n=303)','Behavior on NozzleSystem (n=303)')
h2('Grenzen — wann nicht verwenden',    'Limits — when not to use')

# ── h3 ──
def h3(de, en):
    pair(f'<h3>{de}</h3>',
         f'<h3 data-lang="de">{de}</h3><h3 data-lang="en">{en}</h3>')

h3('Warum Arc-Length statt t-Parametrisierung?',
   'Why arc length instead of t parametrization?')
h3('Mathematisches Setup',              'Mathematical setup')
h3('Predictor mit Vorzeichenwahl',      'Predictor with sign selection')
h3('Korrektor — Newton im erweiterten Raum',
   'Corrector — Newton in the extended space')
h3('Ursache',                           'Root cause')
h3('Was helfen würde (theoretisch)',    'What would help (theoretically)')
h3('Wann er gedacht ist',               'When it is intended for use')
h3('Roadmap',                           'Roadmap')

# ── Status section: 3 notes ──
pair('<div class="note red">\n    <strong>EXPERIMENTAL — derzeit nicht für produktive Nutzung empfohlen.</strong>\n    Dieser Solver ist mathematisch sauber implementiert, scheitert aber\n    auf dem NozzleSystem-Modell (n=303, gemischte Einheiten). Die\n    Initial-Tangente am Startpunkt ist bei stark schlecht konditionierter J₀\n    (kappa &gt; 10⁹) extrem in x-Richtung dominiert (‖ẋ‖ ≫ ṫ), was den\n    ersten Pfadschritt mathematisch in eine Sackgasse führt — selbst nach\n    ds-Reduktion. Siehe <a href="#verhalten">Verhalten auf NozzleSystem</a>.\n  </div>',
     '<div class="note red" data-lang="de">\n    <strong>EXPERIMENTAL — derzeit nicht für produktive Nutzung empfohlen.</strong>\n    Dieser Solver ist mathematisch sauber implementiert, scheitert aber\n    auf dem NozzleSystem-Modell (n=303, gemischte Einheiten). Die\n    Initial-Tangente am Startpunkt ist bei stark schlecht konditionierter J₀\n    (kappa &gt; 10⁹) extrem in x-Richtung dominiert (‖ẋ‖ ≫ ṫ), was den\n    ersten Pfadschritt mathematisch in eine Sackgasse führt — selbst nach\n    ds-Reduktion. Siehe <a href="#verhalten">Verhalten auf NozzleSystem</a>.\n  </div>'
     '<div class="note red" data-lang="en">\n    <strong>EXPERIMENTAL — currently not recommended for production use.</strong>\n    This solver is mathematically cleanly implemented but fails on the\n    NozzleSystem model (n=303, mixed units). At the starting point, when J₀\n    is severely ill-conditioned (kappa &gt; 10⁹), the initial tangent is\n    extremely dominated in the x direction (‖ẋ‖ ≫ ṫ), which mathematically\n    drives the first path step into a dead end — even after ds reduction.\n    See <a href="#verhalten">Behavior on NozzleSystem</a>.\n  </div>')

pair('<div class="note amber">\n    <strong>Wann er funktionieren würde:</strong> Auf Modellen mit moderater\n    Konditionszahl (kappa &lt; 10⁵) und normalisierten Variablen-Skalen\n    (alle in [0.1, 10]) sollte der Solver mathematisch korrekt durchlaufen.\n    Solche Modelle haben wir aktuell nicht im Test-Repository.\n  </div>',
     '<div class="note amber" data-lang="de">\n    <strong>Wann er funktionieren würde:</strong> Auf Modellen mit moderater\n    Konditionszahl (kappa &lt; 10⁵) und normalisierten Variablen-Skalen\n    (alle in [0.1, 10]) sollte der Solver mathematisch korrekt durchlaufen.\n    Solche Modelle haben wir aktuell nicht im Test-Repository.\n  </div>'
     '<div class="note amber" data-lang="en">\n    <strong>When it would work:</strong> on models with moderate condition\n    number (kappa &lt; 10⁵) and normalized variable scales (all in [0.1, 10])\n    the solver should run mathematically correctly. We currently have no such\n    models in the test repository.\n  </div>')

pair('<div class="note blue">\n    <strong>Empfehlung für jetzt:</strong> Verwende stattdessen\n    <a href="solver_newton_armijo.html">NEWTON_ARMIJO</a> mit\n    <code>-SC:EQUILIBRATE</code> oder <a href="solver_lm.html">LEVENBERG_MARQUARDT</a>\n    (v2.12 Newton-Direkt-Hybrid). Beide konvergieren auf NozzleSystem in 5 Iter.\n  </div>',
     '<div class="note blue" data-lang="de">\n    <strong>Empfehlung für jetzt:</strong> Verwende stattdessen\n    <a href="solver_newton_armijo.html">NEWTON_ARMIJO</a> mit\n    <code>-SC:EQUILIBRATE</code> oder <a href="solver_lm.html">LEVENBERG_MARQUARDT</a>\n    (v2.12 Newton-Direkt-Hybrid). Beide konvergieren auf NozzleSystem in 5 Iter.\n  </div>'
     '<div class="note blue" data-lang="en">\n    <strong>Recommendation for now:</strong> use\n    <a href="solver_newton_armijo.html">NEWTON_ARMIJO</a> with\n    <code>-SC:EQUILIBRATE</code> or <a href="solver_lm.html">LEVENBERG_MARQUARDT</a>\n    (v2.12 Newton-direct hybrid) instead. Both converge on NozzleSystem in 5 iterations.\n  </div>')

# ── Theorie section paragraphs ──
pair('<p>\n    Klassisches Continuation parametrisiert den Pfad mit <code>t ∈ [0, 1]</code>\n    von einer trivialen Startlösung zur Zielwertung. <strong>Problem:</strong>\n    wenn der Lösungspfad einen Wendepunkt hat (<code>dx/dt → ∞</code>, t kehrt\n    sich um), bricht t-Parametrisierung zusammen.\n  </p>',
     '<p data-lang="de">\n    Klassisches Continuation parametrisiert den Pfad mit <code>t ∈ [0, 1]</code>\n    von einer trivialen Startlösung zur Zielwertung. <strong>Problem:</strong>\n    wenn der Lösungspfad einen Wendepunkt hat (<code>dx/dt → ∞</code>, t kehrt\n    sich um), bricht t-Parametrisierung zusammen.\n  </p>'
     '<p data-lang="en">\n    Classical continuation parametrizes the path with <code>t ∈ [0, 1]</code>\n    from a trivial starting solution to the target evaluation. <strong>Problem:</strong>\n    when the solution path has a turning point (<code>dx/dt → ∞</code>, t reverses),\n    t parametrization breaks down.\n  </p>')

pair('<p>\n    Bei einem Schallübergang im Düsenmodell gibt es typischerweise zwei\n    Lösungen für gegebenes Druckverhältnis (subsonic + supersonic), und der\n    Pfad zwischen ihnen läuft durch Ma=1 wo die Jacobi exakt singulär wird.\n    t-Parametrisierung kann diese Stelle nicht passieren, Bogen-Länge schon.\n  </p>',
     '<p data-lang="de">\n    Bei einem Schallübergang im Düsenmodell gibt es typischerweise zwei\n    Lösungen für gegebenes Druckverhältnis (subsonic + supersonic), und der\n    Pfad zwischen ihnen läuft durch Ma=1 wo die Jacobi exakt singulär wird.\n    t-Parametrisierung kann diese Stelle nicht passieren, Bogen-Länge schon.\n  </p>'
     '<p data-lang="en">\n    A sonic transition in a nozzle model typically has two solutions for a\n    given pressure ratio (subsonic + supersonic), and the path between them\n    passes through Ma=1 where the Jacobian becomes exactly singular.\n    t parametrization cannot cross this point — arc length can.\n  </p>')

# math-block hi labels
def hi(de, en):
    pair(f'<span class="hi">{de}</span>',
         f'<span class="hi" data-lang="de">{de}</span>'
         f'<span class="hi" data-lang="en">{en}</span>')

hi('Erweiterter Zustand:',          'Extended state:')
hi('Erweitertes System G(y) = 0:',  'Extended system G(y) = 0:')
hi('Skalierungs-Vektor w:',         'Scaling vector w:')

# math-block cmt comments
def cmt(de, en):
    pair(f'<span class="cmt">{de}</span>',
         f'<span class="cmt" data-lang="de">{de}</span>'
         f'<span class="cmt" data-lang="en">{en}</span>')

cmt('← n Gleichungen',              '← n equations')
cmt('← Bogen-Gleichung',            '← arc equation')
cmt('für x-Komponenten',            'for x components')
cmt('für t',                        'for t')
cmt('← n Gleichungen für n+1 Unbekannte',
    '← n equations for n+1 unknowns')
cmt('← Normierung + Vorzeichen',    '← normalization + sign')
cmt('n Zeilen',                     'n rows')
cmt('1 Zeile',                      '1 row')
cmt('direkte Inversion (Lehre aus LM v3b)',
    'direct inversion (lesson from LM v3b)')
cmt('Armijo im erweiterten Raum',   'Armijo in extended space')

# Bogen-Norm paragraph
pair('<p>\n    Die sphärische Bogen-Norm <code>‖w∘(y-y_prev)‖² = ds²</code> ist robuster\n    bei großem n als die einfachere Crisfield-Variante (linear in y), weil\n    sie auch bei ungenauer Tangente sinnvoll bleibt.\n  </p>',
     '<p data-lang="de">\n    Die sphärische Bogen-Norm <code>‖w∘(y-y_prev)‖² = ds²</code> ist robuster\n    bei großem n als die einfachere Crisfield-Variante (linear in y), weil\n    sie auch bei ungenauer Tangente sinnvoll bleibt.\n  </p>'
     '<p data-lang="en">\n    The spherical arc norm <code>‖w∘(y-y_prev)‖² = ds²</code> is more robust\n    at large n than the simpler Crisfield variant (linear in y) because it\n    remains meaningful even with an inaccurate tangent.\n  </p>')

pair('<p>\n    Tangente am Pfadpunkt y wird aus dem erweiterten System gelöst:\n  </p>',
     '<p data-lang="de">\n    Tangente am Pfadpunkt y wird aus dem erweiterten System gelöst:\n  </p>'
     '<p data-lang="en">\n    The tangent at path point y is obtained by solving the extended system:\n  </p>')

pair('<p>\n    Die letzte Gleichung wählt die Tangente in der Richtung der vorherigen —\n    verhindert Vorzeichen-Sprünge wenn der Pfad einen Wendepunkt überquert.\n  </p>',
     '<p data-lang="de">\n    Die letzte Gleichung wählt die Tangente in der Richtung der vorherigen —\n    verhindert Vorzeichen-Sprünge wenn der Pfad einen Wendepunkt überquert.\n  </p>'
     '<p data-lang="en">\n    The last equation picks the tangent in the direction of the previous one —\n    preventing sign jumps when the path crosses a turning point.\n  </p>')

pair('<p>\n    Klassisches Newton-Verfahren auf G(y)=0 mit (n+1)×(n+1) erweiterte Jacobi:\n  </p>',
     '<p data-lang="de">\n    Klassisches Newton-Verfahren auf G(y)=0 mit (n+1)×(n+1) erweiterte Jacobi:\n  </p>'
     '<p data-lang="en">\n    Classical Newton method on G(y)=0 with the (n+1)×(n+1) extended Jacobian:\n  </p>')

pair('<div class="note blue">\n    <strong>Direkte Inversion:</strong> Bei (n+1)×(n+1) Matrizen mit moderatem\n    n nutzen wir <code>MatrixSimple.inverse()</code> direkt — Lehre aus der\n    LM-Episode wo die Normalengleichung kappa quadrierte. Direkte Lösung\n    ist numerisch deutlich stabiler.\n  </div>',
     '<div class="note blue" data-lang="de">\n    <strong>Direkte Inversion:</strong> Bei (n+1)×(n+1) Matrizen mit moderatem\n    n nutzen wir <code>MatrixSimple.inverse()</code> direkt — Lehre aus der\n    LM-Episode wo die Normalengleichung kappa quadrierte. Direkte Lösung\n    ist numerisch deutlich stabiler.\n  </div>'
     '<div class="note blue" data-lang="en">\n    <strong>Direct inversion:</strong> for (n+1)×(n+1) matrices at moderate n\n    we use <code>MatrixSimple.inverse()</code> directly — a lesson from the LM\n    episode where the normal equation squared kappa. Direct solution is\n    significantly more numerically stable.\n  </div>')

# ── Flowchart SVG: duplicate the entire <svg> for DE / EN ──
import re as _re
DE_FLOW_RE = _re.compile(r'(<div class="flowchart">\s*<svg[^>]*>.*?</svg>\s*</div>)', _re.DOTALL)
m = DE_FLOW_RE.search(html)
if m:
    de_flow = m.group(1)
    en_flow = de_flow
    SVG_REPLACEMENTS = [
        ('START  y₀=(x₀, 0)',         'START  y₀=(x₀, 0)'),
        ('J₀ via FD + Skalierungs-Vektor w', 'J₀ via FD + scaling vector w'),
        ('Initial-Tangente am Startpunkt',   'Initial tangent at start point'),
        ('── Pfad-Schleife ──',              '── Path loop ──'),
        ('t ≥ 1?',                            't ≥ 1?'),
        ('Predictor (Tangenten-Euler)',       'Predictor (tangent Euler)'),
        ('Bounds-Projection auf x',           'Bounds projection on x'),
        ('Korrektor (Newton im erweiterten Raum)',
                                              'Corrector (Newton in extended space)'),
        ('G(y)=0 via Jaug⁻¹·G + Armijo',     'G(y)=0 via Jaug⁻¹·G + Armijo'),
        ('‖G‖ &lt; tol?',                     '‖G‖ &lt; tol?'),
        ('ds ← ds / 2',                       'ds ← ds / 2'),
        ('kleinerer Schritt',                 'smaller step'),
        ('Tangente neu berechnen + Vorzeichen-Korrektur',
                                              'Recompute tangent + sign correction'),
        ('y ← y_corr  · ds adaptiv anpassen', 'y ← y_corr  · adapt ds'),
    ]
    for de, en in SVG_REPLACEMENTS:
        en_flow = en_flow.replace(de, en)
    # ja/nein labels — replace standalone occurrences inside SVG <text>
    en_flow = en_flow.replace('>ja</text>', '>yes</text>')
    en_flow = en_flow.replace('>nein</text>', '>no</text>')

    new_block = (
        '<div data-lang="de">' + de_flow + '</div>'
        '<div data-lang="en">' + en_flow + '</div>'
    )
    pair(de_flow, new_block)

# ── Pseudocode block — wrap the entire <pre>...</pre> in DE/EN pair ──
# The block contains German comments in code; translate those too.
DE_PRE = '''<pre><code>solve():
  y = (x₀, 0)
  J₀ = FD-Jacobi am Startpunkt
  w  = Skalierungs-Vektor [1/scale_x, ..., 1]
  tangent = computeInitialTangent(J₀, F(x₀))    // (-J₀⁻¹·F, 1) normiert

  while t &lt; 1:
    y_pred = y + ds · tangent
    projectBoundsOnX(y_pred)                     // x-Anteil clampen, t soft

    cr = corrector(y_pred, J₀, x₀, w, ds):
      while ‖G(y)‖ &gt; tol:
        Jaug = computeAugmentedJacobian(y, J₀, w, y_prev)
        dy   = -Jaug⁻¹ · G(y)                    // direkte Inversion
        α    = armijoStep(y, dy, G)              // ‖G‖²-Akzeptanz
        y   += α·dy
        projectBoundsOnX(y)

    if cr.converged:
      tangent = computeTangent(y, J₀, x₀, tangent_prev, w)
      // Vorzeichen aus dem akzeptierten Schritt prüfen
      y = cr.y
    else:
      ds = ds / 2
      if ds &lt; ds_min: abort
</code></pre>'''

EN_PRE = '''<pre><code>solve():
  y = (x₀, 0)
  J₀ = FD Jacobian at start point
  w  = scaling vector [1/scale_x, ..., 1]
  tangent = computeInitialTangent(J₀, F(x₀))    // (-J₀⁻¹·F, 1) normalized

  while t &lt; 1:
    y_pred = y + ds · tangent
    projectBoundsOnX(y_pred)                     // clamp x part, t soft

    cr = corrector(y_pred, J₀, x₀, w, ds):
      while ‖G(y)‖ &gt; tol:
        Jaug = computeAugmentedJacobian(y, J₀, w, y_prev)
        dy   = -Jaug⁻¹ · G(y)                    // direct inversion
        α    = armijoStep(y, dy, G)              // ‖G‖² acceptance
        y   += α·dy
        projectBoundsOnX(y)

    if cr.converged:
      tangent = computeTangent(y, J₀, x₀, tangent_prev, w)
      // verify sign from the accepted step
      y = cr.y
    else:
      ds = ds / 2
      if ds &lt; ds_min: abort
</code></pre>'''

pair(DE_PRE,
     f'<div data-lang="de">{DE_PRE}</div><div data-lang="en">{EN_PRE}</div>')

# ── Files section: file-desc spans ──
def filedesc(de, en):
    pair(f'<span class="file-desc">{de}</span>',
         f'<span class="file-desc" data-lang="de">{de}</span>'
         f'<span class="file-desc" data-lang="en">{en}</span>')

filedesc('Hauptklasse, 712 Zeilen — Phase 1 Implementierung',
         'Main class, 712 lines — phase 1 implementation')
filedesc('Wiederverwendet (steps, dsInit, dsMin, dsMax, iterTarget)',
         'Reused (steps, dsInit, dsMin, dsMax, iterTarget)')
filedesc('Bounds-Projection auf x-Anteil von y',
         'Bounds projection on the x part of y')

# ── Verhalten section ──
pair('<div class="note red">\n    <strong>Initial-Tangente komplett in x-Richtung dominiert:</strong>\n    Aus dem Test-Log:\n    <pre>Initial tangent: ṫ=2.67e-07  ‖ẋ‖_max=5.33e+04\nPath step 1: ds=1.00e-01  predict t=0.0000  ‖ẋ‖_max=5.33e+04\nCorrector failed at path step 1, reducing ds to 5.00e-02\nPath step 2: ds=5.00e-02  predict t=0.0000  ‖ẋ‖_max=5.33e+04\nCorrector failed at path step 2, reducing ds to 2.50e-02\n...</pre>\n  </div>',
     '<div class="note red" data-lang="de">\n    <strong>Initial-Tangente komplett in x-Richtung dominiert:</strong>\n    Aus dem Test-Log:\n    <pre>Initial tangent: ṫ=2.67e-07  ‖ẋ‖_max=5.33e+04\nPath step 1: ds=1.00e-01  predict t=0.0000  ‖ẋ‖_max=5.33e+04\nCorrector failed at path step 1, reducing ds to 5.00e-02\nPath step 2: ds=5.00e-02  predict t=0.0000  ‖ẋ‖_max=5.33e+04\nCorrector failed at path step 2, reducing ds to 2.50e-02\n...</pre>\n  </div>'
     '<div class="note red" data-lang="en">\n    <strong>Initial tangent completely dominated in the x direction:</strong>\n    From the test log:\n    <pre>Initial tangent: ṫ=2.67e-07  ‖ẋ‖_max=5.33e+04\nPath step 1: ds=1.00e-01  predict t=0.0000  ‖ẋ‖_max=5.33e+04\nCorrector failed at path step 1, reducing ds to 5.00e-02\nPath step 2: ds=5.00e-02  predict t=0.0000  ‖ẋ‖_max=5.33e+04\nCorrector failed at path step 2, reducing ds to 2.50e-02\n...</pre>\n  </div>')

pair('<p>\n    Die Initial-Tangente kommt aus <code>J₀·ẋ = -F(x₀)</code> mit ṫ=1.\n    Bei NozzleSystem ist <code>‖F(x₀)‖ ≈ 1.35·10⁷</code> und kappa(J₀) ≈ 5·10¹¹ — daher\n    sind die ẋ-Komponenten extrem groß. Nach Normierung\n    <code>‖w∘ẏ‖=1</code> dominiert ẋ den gesamten Tangentenvektor, und ṫ\n    wird auf 2.67·10⁻⁷ verschoben.\n  </p>',
     '<p data-lang="de">\n    Die Initial-Tangente kommt aus <code>J₀·ẋ = -F(x₀)</code> mit ṫ=1.\n    Bei NozzleSystem ist <code>‖F(x₀)‖ ≈ 1.35·10⁷</code> und kappa(J₀) ≈ 5·10¹¹ — daher\n    sind die ẋ-Komponenten extrem groß. Nach Normierung\n    <code>‖w∘ẏ‖=1</code> dominiert ẋ den gesamten Tangentenvektor, und ṫ\n    wird auf 2.67·10⁻⁷ verschoben.\n  </p>'
     '<p data-lang="en">\n    The initial tangent comes from <code>J₀·ẋ = -F(x₀)</code> with ṫ=1.\n    On NozzleSystem <code>‖F(x₀)‖ ≈ 1.35·10⁷</code> and kappa(J₀) ≈ 5·10¹¹ —\n    so the ẋ components are extremely large. After normalization\n    <code>‖w∘ẏ‖=1</code> ẋ dominates the entire tangent vector, and ṫ is\n    pushed down to 2.67·10⁻⁷.\n  </p>')

pair('<p>\n    Predictor <code>y + ds·tangent</code> mit ds=0.1 bewegt sich daher fast\n    ausschließlich in x-Richtung — t bleibt bei 0. Bounds-Projection clampt\n    viele x-Komponenten an ihre Grenzen, danach ist die Bogen-Constraint\n    <code>‖w∘(y-y_prev)‖² = ds²</code> nicht mehr erfüllbar, und der\n    Korrektor scheitert auch nach ds-Halbierungen.\n  </p>',
     '<p data-lang="de">\n    Predictor <code>y + ds·tangent</code> mit ds=0.1 bewegt sich daher fast\n    ausschließlich in x-Richtung — t bleibt bei 0. Bounds-Projection clampt\n    viele x-Komponenten an ihre Grenzen, danach ist die Bogen-Constraint\n    <code>‖w∘(y-y_prev)‖² = ds²</code> nicht mehr erfüllbar, und der\n    Korrektor scheitert auch nach ds-Halbierungen.\n  </p>'
     '<p data-lang="en">\n    The predictor <code>y + ds·tangent</code> with ds=0.1 therefore moves\n    almost entirely in the x direction — t stays at 0. Bounds projection\n    clamps many x components to their limits, after which the arc constraint\n    <code>‖w∘(y-y_prev)‖² = ds²</code> can no longer be satisfied, and the\n    corrector fails even after ds halvings.\n  </p>')

# "Was helfen würde" list
pair('<ul>\n    <li>Andere Tangenten-Skalierung mit erzwungenem ṫ-Mindestbetrag</li>\n    <li>Equilibrator-Integration auf der ∂H/∂x-Submatrix</li>\n    <li>Soft-Bogen-Constraint (Slack-Variable) im Korrektor</li>\n  </ul>',
     '<ul data-lang="de">\n    <li>Andere Tangenten-Skalierung mit erzwungenem ṫ-Mindestbetrag</li>\n    <li>Equilibrator-Integration auf der ∂H/∂x-Submatrix</li>\n    <li>Soft-Bogen-Constraint (Slack-Variable) im Korrektor</li>\n  </ul>'
     '<ul data-lang="en">\n    <li>Different tangent scaling with an enforced minimum on ṫ</li>\n    <li>Equilibrator integration on the ∂H/∂x submatrix</li>\n    <li>Soft arc constraint (slack variable) in the corrector</li>\n  </ul>')

pair('<p>\n    Diese Verbesserungen sind nicht implementiert weil kein Test-Modell mit\n    Wendepunkt verfügbar ist — Verbesserungen wären spekulativ ohne\n    Validierungsmöglichkeit.\n  </p>',
     '<p data-lang="de">\n    Diese Verbesserungen sind nicht implementiert weil kein Test-Modell mit\n    Wendepunkt verfügbar ist — Verbesserungen wären spekulativ ohne\n    Validierungsmöglichkeit.\n  </p>'
     '<p data-lang="en">\n    These improvements are not implemented because no test model with a\n    turning point is available — they would be speculative without a way to\n    validate them.\n  </p>')

# ── Grenzen section ──
pair('<ul>\n    <li>\n      <strong>Modelle mit kappa(J₀) &gt; 10⁹ und stark gemischten Skalen</strong> —\n      Initial-Tangente wird unbrauchbar (siehe NozzleSystem-Beispiel oben).\n    </li>\n    <li>\n      <strong>Modelle ohne tatsächliche Wendepunkte</strong> — t-Parametrisierte\n      Methoden (HOMOTOPY, ADAPTIVE_LAMBDA) sind einfacher und genauso\n      gut für reguläre Pfade.\n    </li>\n    <li>\n      <strong>Wenn Newton-Armijo direkt konvergiert</strong> — der einfachere\n      Solver ist schneller (5 Iter, 0.4 s auf NozzleSystem) und numerisch\n      stabiler.\n    </li>\n  </ul>',
     '<ul data-lang="de">\n    <li>\n      <strong>Modelle mit kappa(J₀) &gt; 10⁹ und stark gemischten Skalen</strong> —\n      Initial-Tangente wird unbrauchbar (siehe NozzleSystem-Beispiel oben).\n    </li>\n    <li>\n      <strong>Modelle ohne tatsächliche Wendepunkte</strong> — t-Parametrisierte\n      Methoden (HOMOTOPY, ADAPTIVE_LAMBDA) sind einfacher und genauso\n      gut für reguläre Pfade.\n    </li>\n    <li>\n      <strong>Wenn Newton-Armijo direkt konvergiert</strong> — der einfachere\n      Solver ist schneller (5 Iter, 0.4 s auf NozzleSystem) und numerisch\n      stabiler.\n    </li>\n  </ul>'
     '<ul data-lang="en">\n    <li>\n      <strong>Models with kappa(J₀) &gt; 10⁹ and strongly mixed scales</strong> —\n      the initial tangent becomes unusable (see NozzleSystem example above).\n    </li>\n    <li>\n      <strong>Models without actual turning points</strong> — t-parametrized\n      methods (HOMOTOPY, ADAPTIVE_LAMBDA) are simpler and equally good for\n      regular paths.\n    </li>\n    <li>\n      <strong>When Newton-Armijo converges directly</strong> — the simpler\n      solver is faster (5 iter, 0.4 s on NozzleSystem) and more numerically\n      stable.\n    </li>\n  </ul>')

pair('<ul>\n    <li>Modelle mit echten Wendepunkten oder Bifurkationen (z.B. Schallübergang)</li>\n    <li>Pfade die t-Parametrisierung topologisch nicht passieren kann</li>\n    <li>Forschungsanwendungen mit normalisierten dimensionslosen Größen</li>\n  </ul>',
     '<ul data-lang="de">\n    <li>Modelle mit echten Wendepunkten oder Bifurkationen (z.B. Schallübergang)</li>\n    <li>Pfade die t-Parametrisierung topologisch nicht passieren kann</li>\n    <li>Forschungsanwendungen mit normalisierten dimensionslosen Größen</li>\n  </ul>'
     '<ul data-lang="en">\n    <li>Models with real turning points or bifurcations (e.g., sonic transition)</li>\n    <li>Paths that t parametrization cannot topologically traverse</li>\n    <li>Research applications with normalized dimensionless quantities</li>\n  </ul>')

pair('<p>\n    Eine Phase 2 mit Equilibrator-Integration und Tangenten-Reskalierung ist\n    konzeptionell skizziert aber nicht implementiert. Ohne Modell mit\n    Wendepunkt zum Validieren wäre die Implementierung blind. Die aktuelle\n    Phase 1 dient als mathematisches Skelett und kann später ausgebaut\n    werden wenn ein passendes Test-Modell vorliegt.\n  </p>',
     '<p data-lang="de">\n    Eine Phase 2 mit Equilibrator-Integration und Tangenten-Reskalierung ist\n    konzeptionell skizziert aber nicht implementiert. Ohne Modell mit\n    Wendepunkt zum Validieren wäre die Implementierung blind. Die aktuelle\n    Phase 1 dient als mathematisches Skelett und kann später ausgebaut\n    werden wenn ein passendes Test-Modell vorliegt.\n  </p>'
     '<p data-lang="en">\n    A phase 2 with equilibrator integration and tangent rescaling is\n    conceptually sketched but not implemented. Without a model with a turning\n    point to validate against, the implementation would be blind. The current\n    phase 1 serves as a mathematical skeleton and can be extended later when\n    a suitable test model becomes available.\n  </p>')

# ── Footer harmonization ──
# Replace the legacy <hr>+inline-styled <p> footer with the standard pattern.
OLD_FOOTER = '''<footer>
  <hr>
  <p style="color: #4a5568; font-size: 12px; text-align: center;">
    CMDSolver Documentation — Solver 8/9 — ArcLengthHomotopySolver (experimental, v2.12)
  </p>
</footer>'''

NEW_FOOTER = '''<footer>
  <span data-lang="de">CMDSolver Docs · ArcLength-Homotopie (experimental) · v2.12</span><span data-lang="en">CMDSolver Docs · Arc-Length Homotopy (experimental) · v2.12</span>
  <span>
    <a href="solver_homotopy.html" data-lang="de">← Homotopie</a><a href="solver_homotopy.html" data-lang="en">← Homotopy</a>
    &nbsp;|&nbsp;
    <a href="solver_adaptive_lambda.html" data-lang="de">Adaptive-Lambda →</a><a href="solver_adaptive_lambda.html" data-lang="en">Adaptive-Lambda →</a>
  </span>
</footer>'''

pair(OLD_FOOTER, NEW_FOOTER)

# Apply
missing = []
for i, (old, new) in enumerate(REPS):
    if old not in html: missing.append((i, old[:80])); continue
    html = html.replace(old, new, 1)

p.write_text(html, encoding='utf-8')
print(f'solver_arc_length.html: {len(REPS) - len(missing)} / {len(REPS)} replacements')
if missing:
    print('NOT FOUND:')
    for i, s in missing[:10]: print(f'  #{i}: {s!r}')
