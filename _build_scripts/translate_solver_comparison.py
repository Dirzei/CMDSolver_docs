#!/usr/bin/env python3
"""Translates body content of solver_comparison.html to bilingual DE/EN."""
from pathlib import Path
import re

p = Path('/home/claude/build/solver_comparison.html')
html = p.read_text(encoding='utf-8')

REPS = []
def pair(old, new): REPS.append((old, new))

# ── Nav ──
pair('<a href="#matrix">Vergleichsmatrix</a>',
     '<a href="#matrix" data-lang="de">Vergleichsmatrix</a>'
     '<a href="#matrix" data-lang="en">Comparison Matrix</a>')
pair('<a href="#leistung">Testergebnisse</a>',
     '<a href="#leistung" data-lang="de">Testergebnisse</a>'
     '<a href="#leistung" data-lang="en">Test Results</a>')
pair('<a href="#anmerkungen">Anmerkungen</a>',
     '<a href="#anmerkungen" data-lang="de">Anmerkungen</a>'
     '<a href="#anmerkungen" data-lang="en">Notes</a>')
pair('<a href="#empfehlung">Empfehlung</a>',
     '<a href="#empfehlung" data-lang="de">Empfehlung</a>'
     '<a href="#empfehlung" data-lang="en">Recommendation</a>')

# ── h2 ──
def h2(de, en):
    pair(f'<h2>{de}</h2>',
         f'<h2 data-lang="de">{de}</h2><h2 data-lang="en">{en}</h2>')

h2('Vergleichsmatrix', 'Comparison Matrix')
h2('Testergebnisse — SimpleSystem.cas', 'Test Results — SimpleSystem.cas')
h2('Anmerkungen zu den Bewertungen', 'Notes on the Ratings')
h2('Entscheidungsbaum', 'Decision Tree')

# ── Star rating note ──
pair('<div class="note blue">\n    <strong>Bewertung:</strong>\n    <span class="star-full">★★★</span> Sehr gut &nbsp;\n    <span class="star-half">★★☆</span> Gut &nbsp;\n    <span class="star-half">★☆☆</span> Eingeschränkt &nbsp;\n    <span class="star-empty">☆☆☆</span> Ungeeignet\n    &nbsp;&nbsp;|&nbsp;&nbsp;\n    Fußnoten <sup>1–9</sup> erklären Bewertungen im Detail.\n  </div>',
     '<div class="note blue" data-lang="de">\n    <strong>Bewertung:</strong>\n    <span class="star-full">★★★</span> Sehr gut &nbsp;\n    <span class="star-half">★★☆</span> Gut &nbsp;\n    <span class="star-half">★☆☆</span> Eingeschränkt &nbsp;\n    <span class="star-empty">☆☆☆</span> Ungeeignet\n    &nbsp;&nbsp;|&nbsp;&nbsp;\n    Fußnoten <sup>1–9</sup> erklären Bewertungen im Detail.\n  </div>'
     '<div class="note blue" data-lang="en">\n    <strong>Rating:</strong>\n    <span class="star-full">★★★</span> Excellent &nbsp;\n    <span class="star-half">★★☆</span> Good &nbsp;\n    <span class="star-half">★☆☆</span> Limited &nbsp;\n    <span class="star-empty">☆☆☆</span> Unsuitable\n    &nbsp;&nbsp;|&nbsp;&nbsp;\n    Footnotes <sup>1–9</sup> explain ratings in detail.\n  </div>')

# ── v2.12 note ──
pair('<div class="note amber">\n    <strong>Hinweis v2.12:</strong> Die folgende Vergleichsmatrix listet die\n    7 produktiv nutzbaren Solver. Zwei weitere Solver wurden experimentell\n    hinzugefügt aber sind hier nicht aufgeführt:\n    <ul style="margin-top: 0.4rem;">\n      <li><a href="solver_arc_length.html">ARC_LENGTH</a> — Bogen-Längen-Continuation\n        für Wendepunkte/Bifurkationen. Auf NozzleSystem nicht produktiv konvergent.</li>\n      <li><a href="solver_adaptive_lambda.html">ADAPTIVE_LAMBDA</a> — Wrapper über\n        Newton-Armijo. Phase 1 produktiv, Phase 2 (Continuation) experimentell.</li>\n    </ul>\n    Beide sind in den Detail-Seiten dokumentiert mit klarer Markierung wann\n    nicht zu verwenden.\n  </div>',
     '<div class="note amber" data-lang="de">\n    <strong>Hinweis v2.12:</strong> Die folgende Vergleichsmatrix listet die\n    7 produktiv nutzbaren Solver. Zwei weitere Solver wurden experimentell\n    hinzugefügt aber sind hier nicht aufgeführt:\n    <ul style="margin-top: 0.4rem;">\n      <li><a href="solver_arc_length.html">ARC_LENGTH</a> — Bogen-Längen-Continuation\n        für Wendepunkte/Bifurkationen. Auf NozzleSystem nicht produktiv konvergent.</li>\n      <li><a href="solver_adaptive_lambda.html">ADAPTIVE_LAMBDA</a> — Wrapper über\n        Newton-Armijo. Phase 1 produktiv, Phase 2 (Continuation) experimentell.</li>\n    </ul>\n    Beide sind in den Detail-Seiten dokumentiert mit klarer Markierung wann\n    nicht zu verwenden.\n  </div>'
     '<div class="note amber" data-lang="en">\n    <strong>Note v2.12:</strong> The following comparison matrix lists the\n    7 production-ready solvers. Two further solvers were added experimentally\n    but are not listed here:\n    <ul style="margin-top: 0.4rem;">\n      <li><a href="solver_arc_length.html">ARC_LENGTH</a> — arc-length continuation\n        for turning points/bifurcations. Not productively convergent on NozzleSystem.</li>\n      <li><a href="solver_adaptive_lambda.html">ADAPTIVE_LAMBDA</a> — wrapper around\n        Newton-Armijo. Phase 1 production-ready, Phase 2 (continuation) experimental.</li>\n    </ul>\n    Both are documented on their detail pages with a clear marker when not\n    to use them.\n  </div>')

# ── Comparison matrix table headers ──
pair('<th>Kriterium</th>',
     '<th data-lang="de">Kriterium</th><th data-lang="en">Criterion</th>')

# Section-row labels (colspan headers inside the table)
def sec_row(de, en):
    pair(f'<tr class="section-row"><td colspan="8">{de}</td></tr>',
         f'<tr class="section-row" data-lang="de"><td colspan="8">{de}</td></tr>'
         f'<tr class="section-row" data-lang="en"><td colspan="8">{en}</td></tr>')

sec_row('Konvergenzverhalten', 'Convergence Behavior')
sec_row('Rechenaufwand', 'Computational Cost')
sec_row('Einsatzbereich', 'Application Range')
sec_row('Implementierung', 'Implementation')

# ── First-column labels of comparison table ──
def td_pair(de, en):
    pair(f'<td>{de}</td>', f'<td data-lang="de">{de}</td><td data-lang="en">{en}</td>')

td_pair('Konvergenzrate <sup>1</sup>', 'Convergence rate <sup>1</sup>')
td_pair('Robustheit bei schlechtem Start <sup>2</sup>',
        'Robustness with bad start <sup>2</sup>')
td_pair('Robustheit bei hohem κ <sup>3</sup>',
        'Robustness at high κ <sup>3</sup>')
td_pair('Globale Konvergenz <sup>4</sup>',
        'Global convergence <sup>4</sup>')
td_pair('Aufwand pro Iteration <sup>5</sup>',
        'Cost per iteration <sup>5</sup>')
td_pair('Jacobi-Berechnung', 'Jacobian computation')
td_pair('Speicherbedarf <sup>6</sup>',
        'Memory footprint <sup>6</sup>')
td_pair('Parallelisierbar', 'Parallelizable')
td_pair('Empfohlene Systemgröße', 'Recommended system size')
td_pair('Konditionszahl κ <sup>3</sup>', 'Condition number κ <sup>3</sup>')
td_pair('Startvektornähe nötig <sup>2</sup>',
        'Starting-vector proximity needed <sup>2</sup>')
td_pair('Geeignet für Parameterstudien <sup>7</sup>',
        'Suitable for parameter studies <sup>7</sup>')
td_pair('Kernklasse', 'Core class')
td_pair('CLI-Schlüssel', 'CLI key')
td_pair('Lineare Algebra', 'Linear algebra')

# ── .na text inside cells (small labels next to stars) ──
def na(de, en):
    pair(f'<span class="na">{de}</span>',
         f'<span class="na" data-lang="de">{de}</span>'
         f'<span class="na" data-lang="en">{en}</span>')

na('O(n³) dicht', 'O(n³) dense')
na('viele Iter.', 'many iter.')
# These appear multiple times — handle via separate plain td_pair below

# Cells with text that needs translation (unique enough to match)
pair('<td>Jede Iter.</td>',
     '<td data-lang="de">Jede Iter.</td><td data-lang="en">Every iter.</td>')
pair('<td>Rang-1 Update</td>',
     '<td data-lang="de">Rang-1 Update</td><td data-lang="en">Rank-1 update</td>')
pair('<td>Innerer Solver</td>',
     '<td data-lang="de">Innerer Solver</td><td data-lang="en">Inner solver</td>')
# Each appears twice — duplicate the replacements
pair('<td>Jede Iter.</td>',
     '<td data-lang="de">Jede Iter.</td><td data-lang="en">Every iter.</td>')
pair('<td>Jede Iter.</td>',
     '<td data-lang="de">Jede Iter.</td><td data-lang="en">Every iter.</td>')
pair('<td>Jede Iter.</td>',
     '<td data-lang="de">Jede Iter.</td><td data-lang="en">Every iter.</td>')
pair('<td>Rang-1 Update</td>',
     '<td data-lang="de">Rang-1 Update</td><td data-lang="en">Rank-1 update</td>')

# Parallelizable rows: "✅ Jacobi" appears 5 times, "—" appears 2 times
# Replace inside the <td>...<span class="impl">✅</span> Jacobi</td> structure
pair('<td><span class="impl">✅</span> Jacobi</td>',
     '<td data-lang="de"><span class="impl">✅</span> Jacobi</td>'
     '<td data-lang="en"><span class="impl">✅</span> Jacobian</td>')
# Repeat for all 5
for _ in range(4):
    pair('<td><span class="impl">✅</span> Jacobi</td>',
         '<td data-lang="de"><span class="impl">✅</span> Jacobi</td>'
         '<td data-lang="en"><span class="impl">✅</span> Jacobian</td>')

# Systemgrößen and conditions (n < 200, &lt; 10⁸ etc.) — these are kept identical, no translation

# Startvektornähe values
pair('<td>Mittel</td>', '<td data-lang="de">Mittel</td><td data-lang="en">Medium</td>')
pair('<td>Hoch</td>', '<td data-lang="de">Hoch</td><td data-lang="en">High</td>')
pair('<td>Mittel</td>', '<td data-lang="de">Mittel</td><td data-lang="en">Medium</td>')
pair('<td>Gering</td>', '<td data-lang="de">Gering</td><td data-lang="en">Low</td>')
pair('<td>Hoch</td>', '<td data-lang="de">Hoch</td><td data-lang="en">High</td>')
pair('<td>Hoch</td>', '<td data-lang="de">Hoch</td><td data-lang="en">High</td>')
pair('<td>Sehr gering</td>', '<td data-lang="de">Sehr gering</td><td data-lang="en">Very low</td>')

# κ "beliebig" cell
pair('<td>beliebig</td>', '<td data-lang="de">beliebig</td><td data-lang="en">arbitrary</td>')

# Lineare Algebra cells
pair('<td>MatrixSimple<br>(dichte LU)</td>',
     '<td data-lang="de">MatrixSimple<br>(dichte LU)</td>'
     '<td data-lang="en">MatrixSimple<br>(dense LU)</td>')
pair('<td>GSPAR<br>(Sparse-LU)</td>',
     '<td data-lang="de">GSPAR<br>(Sparse-LU)</td>'
     '<td data-lang="en">GSPAR<br>(sparse LU)</td>')
# Each appears multiple times
for _ in range(2):
    pair('<td>MatrixSimple<br>(dichte LU)</td>',
         '<td data-lang="de">MatrixSimple<br>(dichte LU)</td>'
         '<td data-lang="en">MatrixSimple<br>(dense LU)</td>')
for _ in range(2):
    pair('<td>GSPAR<br>(Sparse-LU)</td>',
         '<td data-lang="de">GSPAR<br>(Sparse-LU)</td>'
         '<td data-lang="en">GSPAR<br>(sparse LU)</td>')

pair('<td>Innerer Solver <sup>8</sup></td>',
     '<td data-lang="de">Innerer Solver <sup>8</sup></td>'
     '<td data-lang="en">Inner solver <sup>8</sup></td>')

# ── Testergebnisse section ──
pair('<p>\n    Gemessen auf SimpleSystem.cas: 12 Gleichungen, 20 Variablen (8 fixiert),\n    CMDSolver v2.5, Java 21, Windows 10.\n  </p>',
     '<p data-lang="de">\n    Gemessen auf SimpleSystem.cas: 12 Gleichungen, 20 Variablen (8 fixiert),\n    CMDSolver v2.5, Java 21, Windows 10.\n  </p>'
     '<p data-lang="en">\n    Measured on SimpleSystem.cas: 12 equations, 20 variables (8 fixed),\n    CMDSolver v2.5, Java 21, Windows 10.\n  </p>')

# Test results table headers
pair('<th>Solver</th>\n        <th>Status</th>\n        <th>Iterationen</th>\n        <th>fsum</th>\n        <th>Zeit (ms)</th>\n        <th>Empfehlung</th>',
     '<th>Solver</th>\n        <th>Status</th>\n        <th data-lang="de">Iterationen</th><th data-lang="en">Iterations</th>\n        <th>fsum</th>\n        <th data-lang="de">Zeit (ms)</th><th data-lang="en">Time (ms)</th>\n        <th data-lang="de">Empfehlung</th><th data-lang="en">Recommendation</th>')

# Test results — recommendation cells
td_pair('Standard für kleine Systeme', 'Default for small systems')
td_pair('Schnellster bei gut konditionierten Systemen',
        'Fastest on well-conditioned systems')
pair('<td><strong>Beste Gesamtwahl</strong> ← empfohlen</td>',
     '<td data-lang="de"><strong>Beste Gesamtwahl</strong> ← empfohlen</td>'
     '<td data-lang="en"><strong>Best overall choice</strong> ← recommended</td>')
td_pair('Bei schlechter Kondition bevorzugen',
        'Prefer for poor conditioning')
td_pair('Gut für Parameterstudien', 'Good for parameter studies')
td_pair('Schnellster Gesamtlauf', 'Fastest overall run')
td_pair('Nur bei Konvergenzproblemen', 'Only on convergence problems')

# Important note
pair('<div class="note amber">\n    <strong>Wichtig:</strong> Diese Ergebnisse gelten für ein kleines, gut konditioniertes\n    Testsystem. Bei größeren oder schlechter konditionierten Systemen können die\n    relativen Stärken der Solver deutlich abweichen.\n  </div>',
     '<div class="note amber" data-lang="de">\n    <strong>Wichtig:</strong> Diese Ergebnisse gelten für ein kleines, gut konditioniertes\n    Testsystem. Bei größeren oder schlechter konditionierten Systemen können die\n    relativen Stärken der Solver deutlich abweichen.\n  </div>'
     '<div class="note amber" data-lang="en">\n    <strong>Important:</strong> These results are for a small, well-conditioned\n    test system. On larger or worse-conditioned systems, the relative strengths\n    of the solvers can differ significantly.\n  </div>')

# ── Footnotes ──
def footnote(num, de_strong, en_strong, de_text, en_text):
    de_full = f'<sup>{num}</sup> <strong>{de_strong}</strong>\n    {de_text}'
    en_full = f'<sup>{num}</sup> <strong>{en_strong}</strong>\n    {en_text}'
    pair(f'<p>{de_full}</p>',
         f'<p data-lang="de">{de_full}</p><p data-lang="en">{en_full}</p>')

footnote(1, 'Konvergenzrate:', 'Convergence rate:',
    'Newton-Raphson und seine Varianten konvergieren <em>quadratisch</em> in der Nähe der Lösung\n    — der Fehler wird pro Iteration quadriert. LM und Broyden konvergieren superlinear.\n    Homotopie konvergiert abhängig von der Schrittweite des Pfades — typisch linear.',
    'Newton-Raphson and its variants converge <em>quadratically</em> near the solution —\n    the error is squared per iteration. LM and Broyden converge superlinearly.\n    Homotopy converges depending on path step size — typically linearly.')

footnote(2, 'Robustheit bei schlechtem Startvektor:', 'Robustness with bad starting vector:',
    'Newton-Verfahren haben nur lokale Konvergenzgarantien — der Startvektor muss nahe\n    genug an der Lösung liegen. Die Armijo-Liniensuche verbessert den globalen\n    Einzugsbereich erheblich. LM ist durch den Dämpfungsparameter λ robuster.\n    Homotopie ist am robustesten — sie braucht nur einen Startvektor der das\n    vereinfachte Problem H(x,0)=0 löst (typisch: die Initialwerte aus dem CAS-Modell).',
    'Newton methods only have local convergence guarantees — the starting vector must\n    lie close enough to the solution. Armijo line search significantly enlarges the\n    global basin of attraction. LM is more robust thanks to the damping parameter λ.\n    Homotopy is the most robust — it only needs a starting vector that solves the\n    simplified problem H(x,0)=0 (typically the initial values from the CAS model).')

footnote(3, 'Konditionszahl κ:', 'Condition number κ:',
    'κ ist das Verhältnis des größten zum kleinsten Singulärwert der Jacobi-Matrix.\n    Hohe κ bedeutet fast-singuläre Jacobi — kleine Fehler in F werden zu großen\n    Fehlern in Δx verstärkt. LM regularisiert durch λI und ist deshalb robust\n    bis κ ~ 10²⁵. Die Homotopie-Schritte sind ebenfalls weniger empfindlich da\n    der Prädiktor-Korrektor-Ansatz kleinere lokale Linearisierungsfehler macht.\n    Seit v2.12 reduziert die Skalierungsoption <code>-SC:EQUILIBRATE</code>\n    (Sinkhorn-Knopp R·J·C) κ adaptiv um typisch 8-10 Größenordnungen bei\n    Systemen mit gemischten Einheiten — orthogonal zur Solver-Wahl.',
    'κ is the ratio of largest to smallest singular value of the Jacobian.\n    High κ means a near-singular Jacobian — small errors in F amplify into large\n    errors in Δx. LM regularizes via λI and is therefore robust up to κ ~ 10²⁵.\n    Homotopy steps are also less sensitive because the predictor-corrector approach\n    makes smaller local linearization errors.\n    Since v2.12, the scaling option <code>-SC:EQUILIBRATE</code>\n    (Sinkhorn-Knopp R·J·C) adaptively reduces κ by typically 8–10 orders of\n    magnitude on systems with mixed units — orthogonal to solver choice.')

footnote(4, 'Globale Konvergenz:', 'Global convergence:',
    '"Global" bedeutet hier: Konvergenz auch von weit entfernten Startvektoren.\n    Nur Homotopie bietet echte globale Konvergenzgarantien (unter regulären Bedingungen).\n    Newton+Armijo hat einen vergrößerten Einzugsbereich gegenüber reinem Newton.',
    '"Global" here means: convergence also from far-away starting vectors.\n    Only homotopy offers true global convergence guarantees (under regularity conditions).\n    Newton+Armijo has an enlarged basin of attraction compared to plain Newton.')

footnote(5, 'Aufwand pro Iteration (nnz = Anzahl Nicht-Null-Einträge der Jacobi):',
    'Cost per iteration (nnz = number of non-zero entries in the Jacobian):',
    'Dichte LU: O(n³). Sparse-LU (GSPAR): O(nnz · log n) bis O(n · nnz) je nach Struktur.\n    Broyden-Update: O(n²) — günstiger als Neuaufbau O(n³), aber akkumuliert Approximationsfehler.\n    Homotopie hat mehrere innere Solver-Aufrufe pro Homotopie-Schritt.',
    'Dense LU: O(n³). Sparse LU (GSPAR): O(nnz · log n) to O(n · nnz) depending on structure.\n    Broyden update: O(n²) — cheaper than full rebuild O(n³), but accumulates approximation error.\n    Homotopy has multiple inner solver calls per homotopy step.')

footnote(6, 'Speicherbedarf (n = Systemgröße, nnz = Nicht-Null-Einträge):',
    'Memory footprint (n = system size, nnz = non-zero entries):',
    'Dichte Matrix: n² Einträge — bei n=500: 250.000 doubles = 2MB.\n    Sparse-Matrix (GSPAR): nur nnz Einträge — bei 5% Besetzung und n=500: ~12.500 doubles = 100KB.\n    Für thermodynamische Systeme ist die Jacobi typischerweise zu 5-15% besetzt.',
    'Dense matrix: n² entries — for n=500: 250,000 doubles = 2 MB.\n    Sparse matrix (GSPAR): only nnz entries — at 5 % fill and n=500: ~12,500 doubles = 100 KB.\n    For thermodynamic systems the Jacobian is typically 5–15 % populated.')

footnote(7, 'Geeignet für Parameterstudien (BatchRunner):',
    'Suitable for parameter studies (BatchRunner):',
    'Bei Parameterstudien werden viele ähnliche Punkte gelöst. Broyden kann die\n    Jacobi vom vorherigen Punkt als Startapproximation verwenden. Newton-Sparse\n    profitiert von schneller Faktorisierung. Homotopie ist zu langsam pro Run.',
    'Parameter studies solve many similar points. Broyden can use the previous\n    point\'s Jacobian as starting approximation. Newton-Sparse benefits from fast\n    factorization. Homotopy is too slow per run.')

footnote(8, 'Homotopie — innerer Solver:', 'Homotopy — inner solver:',
    'Der Homotopie-Korrektor verwendet selbst einen Newton-basierten inneren Solver.\n    Standard ist <code>NEWTON_ARMIJO</code>. Konfigurierbar via\n    <code>-SH:INNER=LEVENBERG_MARQUARDT</code> für schlecht konditionierte Systeme.',
    'The homotopy corrector itself uses a Newton-based inner solver.\n    Default is <code>NEWTON_ARMIJO</code>. Configurable via\n    <code>-SH:INNER=LEVENBERG_MARQUARDT</code> for ill-conditioned systems.')

footnote(9, 'Homotopie fsum = NaN:', 'Homotopy fsum = NaN:',
    'Der Homotopie-Solver meldet kein fsum über den normalen Ausgabekanal —\n    er hat eine eigene interne Konvergenzprüfung über den Pfadfortschritt (t → 1).\n    NaN bedeutet "nicht verfügbar", nicht "Fehler". Status CONVERGED ist maßgeblich.',
    'The homotopy solver does not report fsum on the normal output channel —\n    it has its own internal convergence check based on path progress (t → 1).\n    NaN means "not available", not "error". The CONVERGED status is authoritative.')

# ── Decision tree SVG (duplicate the entire flowchart for DE/EN) ──
DE_FLOW_RE = re.compile(r'(<div class="flowchart">\s*<svg[^>]*>.*?</svg>\s*</div>)', re.DOTALL)
m = DE_FLOW_RE.search(html)
if m:
    de_flow = m.group(1)
    en_flow = de_flow
    SVG_REPLACEMENTS = [
        ('Modell lösen', 'Solve model'),
        ('Guter Startvektor?', 'Good starting vector?'),
        ('Parameterstudie?', 'Parameter study?'),
        # Note: ja/nein appear multiple times — global string replace handles them all
        # but we need to be careful not to break "ja" inside other words.
        # The svg uses them as standalone <text> contents.
    ]
    for de, en in SVG_REPLACEMENTS:
        en_flow = en_flow.replace(de, en)
    # Replace ">ja<" and ">nein<" specifically (not as substring of words)
    en_flow = en_flow.replace('>ja</text>', '>yes</text>')
    en_flow = en_flow.replace('>nein</text>', '>no</text>')

    new_block = (
        '<div data-lang="de">' + de_flow + '</div>'
        '<div data-lang="en">' + en_flow + '</div>'
    )
    pair(de_flow, new_block)

# ── Footer ──
pair('<span>CMDSolver Docs · Solver Vergleich · v2.5</span>',
     '<span data-lang="de">CMDSolver Docs · Solver Vergleich · v2.5</span>'
     '<span data-lang="en">CMDSolver Docs · Solver Comparison · v2.5</span>')
pair('<a href="math_overview.html">← Mathematischer Überblick</a>',
     '<a href="math_overview.html" data-lang="de">← Mathematischer Überblick</a>'
     '<a href="math_overview.html" data-lang="en">← Mathematical Overview</a>')
pair('<a href="solver_newton_armijo.html">Newton-Armijo →</a>',
     '<a href="solver_newton_armijo.html" data-lang="de">Newton-Armijo →</a>'
     '<a href="solver_newton_armijo.html" data-lang="en">Newton-Armijo →</a>')

# ── Apply ──
missing = []
for i, (old, new) in enumerate(REPS):
    if old not in html: missing.append((i, old[:80])); continue
    html = html.replace(old, new, 1)

p.write_text(html, encoding='utf-8')
print(f'Applied {len(REPS) - len(missing)} / {len(REPS)} replacements')
if missing:
    print('NOT FOUND:')
    for i, s in missing[:15]: print(f'  #{i}: {s!r}')
