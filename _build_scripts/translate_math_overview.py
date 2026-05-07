#!/usr/bin/env python3
"""Translates body content of math_overview.html to bilingual DE/EN."""
from pathlib import Path
import re

p = Path('/home/claude/build/math_overview.html')
html = p.read_text(encoding='utf-8')

REPS = []
def pair(old, new): REPS.append((old, new))

# ── Nav ──
pair('<a href="#problem">Das Problem</a>',
     '<a href="#problem" data-lang="de">Das Problem</a>'
     '<a href="#problem" data-lang="en">The Problem</a>')
pair('<a href="#klassifikation">Klassifikation</a>',
     '<a href="#klassifikation" data-lang="de">Klassifikation</a>'
     '<a href="#klassifikation" data-lang="en">Classification</a>')
pair('<a href="#implementiert">Implementiert</a>',
     '<a href="#implementiert" data-lang="de">Implementiert</a>'
     '<a href="#implementiert" data-lang="en">Implemented</a>')
pair('<a href="#nicht-implementiert">Weitere Verfahren</a>',
     '<a href="#nicht-implementiert" data-lang="de">Weitere Verfahren</a>'
     '<a href="#nicht-implementiert" data-lang="en">Other Methods</a>')
pair('<a href="#wahl">Verfahrenswahl</a>',
     '<a href="#wahl" data-lang="de">Verfahrenswahl</a>'
     '<a href="#wahl" data-lang="en">Method Selection</a>')

# ── h2 / h3 ──
def h2(de, en):
    pair(f'<h2>{de}</h2>',
         f'<h2 data-lang="de">{de}</h2><h2 data-lang="en">{en}</h2>')
def h3(de, en):
    pair(f'<h3>{de}</h3>',
         f'<h3 data-lang="de">{de}</h3><h3 data-lang="en">{en}</h3>')

h2('Das Problem — F(x) = 0', 'The Problem — F(x) = 0')
h2('Klassifikation der Verfahren', 'Classification of Methods')
h2('Implementierte Verfahren', 'Implemented Methods')
h2('Weitere Verfahren (nicht implementiert)', 'Other Methods (not implemented)')
h2('Leitfaden zur Verfahrenswahl', 'Method Selection Guide')

h3('Eigenschaften thermodynamischer Systeme', 'Properties of Thermodynamic Systems')
h3('1. Newton-Raphson (mit Varianten)', '1. Newton-Raphson (with Variants)')
h3('2. Levenberg-Marquardt', '2. Levenberg-Marquardt')
h3('3. Broyden Quasi-Newton', '3. Broyden Quasi-Newton')
h3('4. Homotopie (Arc-Length Continuation)', '4. Homotopy (Arc-Length Continuation)')
h3('Trust-Region Methoden', 'Trust-Region Methods')
h3('Dogleg-Verfahren', 'Dogleg Method')
h3('GMRES / Krylov-Unterraum Methoden', 'GMRES / Krylov Subspace Methods')
h3('Anderson Acceleration', 'Anderson Acceleration')
h3('Fixpunkt-Iteration (Gauss-Seidel für Gleichungssysteme)',
   'Fixed-Point Iteration (Gauss-Seidel for Equation Systems)')
h3('Globales Newton mit Regularisierung', 'Global Newton with Regularization')
h3('Parallele / Verteilte Newton-Verfahren', 'Parallel / Distributed Newton Methods')

# ── Section "Das Problem" ──
pair('<p>\n    In thermodynamischen Modellen wie den Triebwerks- und Düsenmodellen von CMDSolver\n    entstehen <strong>nichtlineare algebraische Gleichungssysteme</strong>. Jede Gleichung\n    beschreibt eine physikalische Beziehung zwischen Variablen wie Druck, Temperatur,\n    Massenstrom oder Geometriegrößen.\n  </p>',
     '<p data-lang="de">\n    In thermodynamischen Modellen wie den Triebwerks- und Düsenmodellen von CMDSolver\n    entstehen <strong>nichtlineare algebraische Gleichungssysteme</strong>. Jede Gleichung\n    beschreibt eine physikalische Beziehung zwischen Variablen wie Druck, Temperatur,\n    Massenstrom oder Geometriegrößen.\n  </p>'
     '<p data-lang="en">\n    Thermodynamic models such as CMDSolver\'s engine and nozzle models give rise to\n    <strong>nonlinear algebraic equation systems</strong>. Every equation describes\n    a physical relationship between variables such as pressure, temperature,\n    mass flow, or geometric quantities.\n  </p>')

# math-block .cmt comments inside Das Problem
def cmt(de, en):
    pair(f'<span class="cmt">{de}</span>',
         f'<span class="cmt" data-lang="de">{de}</span>'
         f'<span class="cmt" data-lang="en">{en}</span>')

cmt('// n Gleichungen, n Unbekannte', '// n equations, n unknowns')
cmt('// freie Variablen (Druck, Temp, ...)', '// free variables (pressure, temp, ...)')
cmt('// i-te Gleichung als Residuum', '// i-th equation as residual')
cmt('// Massenerhaltung', '// mass conservation')
cmt('// Druckverhältnis', '// pressure ratio')
cmt('// Thermodynamik', '// thermodynamics')

# math-block .hi keywords
def hi(de, en):
    pair(f'<span class="hi">{de}</span>',
         f'<span class="hi" data-lang="de">{de}</span>'
         f'<span class="hi" data-lang="en">{en}</span>')

hi('Gesucht:', 'Find:')
hi('wobei:', 'where:')
hi('Beispiel (Düsengleichung):', 'Example (nozzle equation):')

# Properties paragraph
pair('<p>\n    Die Gleichungssysteme in CMDSolver haben spezifische Eigenschaften die\n    die Wahl des Lösungsverfahrens stark beeinflussen:\n  </p>',
     '<p data-lang="de">\n    Die Gleichungssysteme in CMDSolver haben spezifische Eigenschaften die\n    die Wahl des Lösungsverfahrens stark beeinflussen:\n  </p>'
     '<p data-lang="en">\n    The equation systems in CMDSolver have specific properties that strongly\n    influence the choice of solution method:\n  </p>')

# Properties table
pair('<thead><tr><th>Eigenschaft</th><th>Typischer Wert</th><th>Auswirkung</th></tr></thead>',
     '<thead><tr>'
     '<th data-lang="de">Eigenschaft</th><th data-lang="en">Property</th>'
     '<th data-lang="de">Typischer Wert</th><th data-lang="en">Typical Value</th>'
     '<th data-lang="de">Auswirkung</th><th data-lang="en">Implication</th>'
     '</tr></thead>')

def td_pair(de, en):
    pair(f'<td>{de}</td>', f'<td data-lang="de">{de}</td><td data-lang="en">{en}</td>')

td_pair('Systemgröße n', 'System size n')
td_pair('Kleine Systeme: dichte LU. Große: Sparse-Methoden',
        'Small systems: dense LU. Large: sparse methods')
td_pair('Nichtlinearitätsgrad', 'Degree of nonlinearity')
td_pair('Mittel bis hoch', 'Moderate to high')
td_pair('Startvektornähe entscheidend für Konvergenz',
        'Starting-vector proximity is decisive for convergence')
td_pair('Konditionszahl κ', 'Condition number κ')
td_pair('Hohe κ → Newton instabil → LM oder Homotopie',
        'High κ → Newton unstable → LM or homotopy')
td_pair('Physikalische Bounds', 'Physical bounds')
td_pair('PhysicalProjector nach jedem Update nötig',
        'PhysicalProjector needed after every update')
td_pair('Jacobi-Besetzung', 'Jacobian fill')
td_pair('Dünn besetzt (sparse)', 'Sparsely populated')
td_pair('Sparse-LU bis zu 10× schneller als dichte LU',
        'Sparse LU up to 10× faster than dense LU')
td_pair('Ableitungen', 'Derivatives')
td_pair('Symbolisch (CASprzak)', 'Symbolic (CASprzak)')
td_pair('Exakt, kein Finite-Differenzen-Fehler',
        'Exact, no finite-difference error')

# ── Section "Klassifikation" — duplicate the SVG flowchart ──
# Strategy: wrap the entire .flowchart container in DE/EN versions.
# Only the SVG <text> elements change between languages. To keep this simple,
# I'll wrap the .flowchart div pair-style.

# Read current SVG block, build the EN version by replacing German labels.
# Then wrap both in data-lang divs.

DE_FLOW_RE = re.compile(r'(<div class="flowchart">.*?</div>)', re.DOTALL)
m = DE_FLOW_RE.search(html)
if m:
    de_flow_html = m.group(1)
    # Translate all SVG text labels
    en_flow_html = de_flow_html
    SVG_REPLACEMENTS = [
        ('F(x) = 0 lösen', 'Solve F(x) = 0'),
        ('Newton-Typ', 'Newton-type'),
        ('Quasi-Newton', 'Quasi-Newton'),
        ('Globalisierung', 'Globalization'),
        ('Newton-Raphson', 'Newton-Raphson'),
        ('LM / Gauss-Newton', 'LM / Gauss-Newton'),
        ('Trust-Region', 'Trust-Region'),
        ('GMRES/Krylov', 'GMRES/Krylov'),
        ('Broyden', 'Broyden'),
        ('Anderson Acc.', 'Anderson Acc.'),
        ('Homotopie', 'Homotopy'),
        ('Fixpunkt-Iter.', 'Fixed-point iter.'),
        ('✅ implementiert', '✅ implemented'),
        ('○ nicht impl.', '○ not impl.'),
    ]
    for de, en in SVG_REPLACEMENTS:
        en_flow_html = en_flow_html.replace(de, en)

    # Wrap with data-lang divs (use class to avoid affecting layout)
    new_block = (
        '<div data-lang="de">' + de_flow_html + '</div>'
        '<div data-lang="en">' + en_flow_html + '</div>'
    )
    pair(de_flow_html, new_block)

# ── Section "Implementierte Verfahren" ──
pair('<p>\n    Die Familie der Newton-Verfahren linearisiert F lokal durch die Jacobi-Matrix J\n    und löst das entstehende lineare System. Unterschiede liegen in der Lösung\n    des linearen Systems (dicht vs. sparse) und der Schrittdämpfung.\n  </p>',
     '<p data-lang="de">\n    Die Familie der Newton-Verfahren linearisiert F lokal durch die Jacobi-Matrix J\n    und löst das entstehende lineare System. Unterschiede liegen in der Lösung\n    des linearen Systems (dicht vs. sparse) und der Schrittdämpfung.\n  </p>'
     '<p data-lang="en">\n    The Newton family linearizes F locally via the Jacobian matrix J and solves\n    the resulting linear system. Variants differ in how the linear system is\n    solved (dense vs. sparse) and in step damping.\n  </p>')

# Newton variants table
pair('<thead><tr><th>Variante</th><th>Lineares System</th><th>Dämpfung</th><th>Stärke</th></tr></thead>',
     '<thead><tr>'
     '<th data-lang="de">Variante</th><th data-lang="en">Variant</th>'
     '<th data-lang="de">Lineares System</th><th data-lang="en">Linear System</th>'
     '<th data-lang="de">Dämpfung</th><th data-lang="en">Damping</th>'
     '<th data-lang="de">Stärke</th><th data-lang="en">Strength</th>'
     '</tr></thead>')

td_pair('Dichte LU (MatrixSimple)', 'Dense LU (MatrixSimple)')
td_pair('Armijo-Backtracking', 'Armijo backtracking')
td_pair('Robustheit bei nichtlinearen Systemen', 'Robustness on nonlinear systems')
td_pair('GSPAR Sparse-LU', 'GSPAR sparse LU')
td_pair('Keine', 'None')
td_pair('Geschwindigkeit bei großen Systemen', 'Speed on large systems')
td_pair('Beste Kombination: schnell + robust', 'Best combination: fast + robust')

# LM paragraph
pair('<p>\n    LM kombiniert Newton-Raphson mit Gradientenabstieg über einen adaptiven\n    Dämpfungsparameter λ. Bei großem λ verhält sich LM wie Gradientenabstieg\n    (robust, langsam), bei kleinem λ wie Newton (schnell, lokal). Besonders\n    geeignet für schlecht konditionierte Systeme.\n  </p>',
     '<p data-lang="de">\n    LM kombiniert Newton-Raphson mit Gradientenabstieg über einen adaptiven\n    Dämpfungsparameter λ. Bei großem λ verhält sich LM wie Gradientenabstieg\n    (robust, langsam), bei kleinem λ wie Newton (schnell, lokal). Besonders\n    geeignet für schlecht konditionierte Systeme.\n  </p>'
     '<p data-lang="en">\n    LM combines Newton-Raphson with gradient descent via an adaptive damping\n    parameter λ. For large λ, LM behaves like gradient descent (robust, slow);\n    for small λ, like Newton (fast, local). Especially well-suited for\n    ill-conditioned systems.\n  </p>')

hi('LM-System:', 'LM system:')
cmt('// λ groß → Gradientenabstieg (stabiler)', '// λ large → gradient descent (more stable)')
cmt('// λ klein → Newton-Schritt (schneller)', '// λ small → Newton step (faster)')
cmt('// λ wird adaptiv nach Fortschritt angepasst', '// λ is adapted based on progress')

# Broyden paragraph
pair('<p>\n    Broyden aktualisiert die Jacobi-Approximation durch einen Rang-1-Update\n    statt sie neu aufzubauen. Das spart Rechenzeit pro Iteration — besonders\n    vorteilhaft wenn die Jacobi-Berechnung teuer ist. Zwei Varianten:\n    mit dichter und mit GSPAR Sparse-LU.\n  </p>',
     '<p data-lang="de">\n    Broyden aktualisiert die Jacobi-Approximation durch einen Rang-1-Update\n    statt sie neu aufzubauen. Das spart Rechenzeit pro Iteration — besonders\n    vorteilhaft wenn die Jacobi-Berechnung teuer ist. Zwei Varianten:\n    mit dichter und mit GSPAR Sparse-LU.\n  </p>'
     '<p data-lang="en">\n    Broyden updates the Jacobian approximation via a rank-1 update instead\n    of rebuilding it. This saves computation per iteration — especially\n    advantageous when Jacobian assembly is expensive. Two variants:\n    with dense and with GSPAR sparse LU.\n  </p>')

hi('Broyden-Update:', 'Broyden update:')
cmt('// Rang-1-Korrektur — O(n²) statt O(n³) für Neuaufbau',
    '// Rank-1 correction — O(n²) instead of O(n³) for full rebuild')

# Homotopy paragraph
pair('<p>\n    Homotopie löst nicht direkt F(x) = 0, sondern konstruiert einen glatten Pfad\n    von einem einfachen Startproblem H(x,0) = 0 zum Zielproblem H(x,1) = F(x) = 0.\n    Besonders geeignet wenn der Startvektor weit von der Lösung entfernt ist\n    oder bei stark nichtlinearen Systemen.\n  </p>',
     '<p data-lang="de">\n    Homotopie löst nicht direkt F(x) = 0, sondern konstruiert einen glatten Pfad\n    von einem einfachen Startproblem H(x,0) = 0 zum Zielproblem H(x,1) = F(x) = 0.\n    Besonders geeignet wenn der Startvektor weit von der Lösung entfernt ist\n    oder bei stark nichtlinearen Systemen.\n  </p>'
     '<p data-lang="en">\n    Homotopy does not solve F(x) = 0 directly but constructs a smooth path\n    from a simple starting problem H(x,0) = 0 to the target H(x,1) = F(x) = 0.\n    Especially useful when the starting vector is far from the solution or\n    on strongly nonlinear systems.\n  </p>')

hi('Homotopie-Funktion:', 'Homotopy function:')
cmt('// t=0: einfaches Startproblem (Startwerte)', '// t=0: simple starting problem (initial values)')
cmt('// t=1: Original-Problem F(x) = 0', '// t=1: original problem F(x) = 0')
cmt('// Arc-Length: Pfad wird nach Bogenlänge parametrisiert',
    '// Arc-length: path is parametrized by arc length')

# ── Section "Weitere Verfahren" ──
pair('<div class="note blue">\n    <strong>Hinweis:</strong> Die folgenden Verfahren sind für thermodynamische\n    Gleichungssysteme prinzipiell geeignet. Sie sind in CMDSolver nicht implementiert,\n    könnten aber für spezielle Anwendungsfälle relevant sein.\n  </div>',
     '<div class="note blue" data-lang="de">\n    <strong>Hinweis:</strong> Die folgenden Verfahren sind für thermodynamische\n    Gleichungssysteme prinzipiell geeignet. Sie sind in CMDSolver nicht implementiert,\n    könnten aber für spezielle Anwendungsfälle relevant sein.\n  </div>'
     '<div class="note blue" data-lang="en">\n    <strong>Note:</strong> The following methods are in principle suitable for\n    thermodynamic equation systems. They are not implemented in CMDSolver,\n    but could be relevant for special use cases.\n  </div>')

# Trust-Region paragraphs
pair('<p>\n    Ähnlich wie LM, aber mit expliziter Schrittweitenkontrolle über einen\n    "Vertrauensbereich" (Trust-Region) Δ. Der Newton-Schritt wird auf eine\n    Kugel mit Radius Δ beschränkt. Δ wird adaptiv angepasst basierend auf\n    dem Verhältnis von vorhergesagtem zu tatsächlichem Fortschritt.\n  </p>',
     '<p data-lang="de">\n    Ähnlich wie LM, aber mit expliziter Schrittweitenkontrolle über einen\n    "Vertrauensbereich" (Trust-Region) Δ. Der Newton-Schritt wird auf eine\n    Kugel mit Radius Δ beschränkt. Δ wird adaptiv angepasst basierend auf\n    dem Verhältnis von vorhergesagtem zu tatsächlichem Fortschritt.\n  </p>'
     '<p data-lang="en">\n    Similar to LM but with explicit step-size control via a "trust region" Δ.\n    The Newton step is restricted to a ball of radius Δ. Δ is adapted based\n    on the ratio of predicted to actual progress.\n  </p>')

pair('<p>\n    <strong>Vorteil gegenüber LM:</strong> Geometrisch intuitiveres Modell,\n    bessere theoretische Konvergenzeigenschaften. Standard in modernen\n    Optimierungsbibliotheken (z.B. MINPACK, SciPy).\n  </p>',
     '<p data-lang="de">\n    <strong>Vorteil gegenüber LM:</strong> Geometrisch intuitiveres Modell,\n    bessere theoretische Konvergenzeigenschaften. Standard in modernen\n    Optimierungsbibliotheken (z.B. MINPACK, SciPy).\n  </p>'
     '<p data-lang="en">\n    <strong>Advantage over LM:</strong> Geometrically more intuitive model,\n    better theoretical convergence properties. Standard in modern optimization\n    libraries (e.g., MINPACK, SciPy).\n  </p>')

# Dogleg paragraph
pair('<p>\n    Kombination aus Newton-Schritt und Cauchy-Punkt (steilstem Abstieg) innerhalb\n    der Trust-Region. Berechnet einen "geknickten" Pfad (Dogleg) zwischen beiden.\n    Effizienter als reines Trust-Region bei gut konditionierten Systemen.\n  </p>',
     '<p data-lang="de">\n    Kombination aus Newton-Schritt und Cauchy-Punkt (steilstem Abstieg) innerhalb\n    der Trust-Region. Berechnet einen "geknickten" Pfad (Dogleg) zwischen beiden.\n    Effizienter als reines Trust-Region bei gut konditionierten Systemen.\n  </p>'
     '<p data-lang="en">\n    Combination of the Newton step and the Cauchy point (steepest descent)\n    inside the trust region. Computes a "bent" path (dogleg) between the two.\n    More efficient than pure trust-region on well-conditioned systems.\n  </p>')

# GMRES paragraphs
pair('<p>\n    Für sehr große Systeme (n &gt; 10.000) ist selbst GSPAR Sparse-LU zu teuer.\n    GMRES (Generalized Minimal Residual) löst das lineare System J·Δx = −F\n    iterativ ohne die Jacobi explizit zu faktorisieren. Benötigt nur\n    Matrix-Vektor-Produkte J·v.\n  </p>',
     '<p data-lang="de">\n    Für sehr große Systeme (n &gt; 10.000) ist selbst GSPAR Sparse-LU zu teuer.\n    GMRES (Generalized Minimal Residual) löst das lineare System J·Δx = −F\n    iterativ ohne die Jacobi explizit zu faktorisieren. Benötigt nur\n    Matrix-Vektor-Produkte J·v.\n  </p>'
     '<p data-lang="en">\n    For very large systems (n &gt; 10,000), even GSPAR sparse LU becomes too\n    expensive. GMRES (Generalized Minimal Residual) solves the linear system\n    J·Δx = −F iteratively without explicitly factorizing the Jacobian. It\n    only requires matrix-vector products J·v.\n  </p>')

pair('<p>\n    <strong>Relevanz für CMDSolver:</strong> Bei den aktuellen Modellgrößen\n    (bis ~500 Gleichungen) nicht nötig. Interessant wenn Netzwerke aus vielen\n    Modulen zu sehr großen Systemen zusammengesetzt werden.\n  </p>',
     '<p data-lang="de">\n    <strong>Relevanz für CMDSolver:</strong> Bei den aktuellen Modellgrößen\n    (bis ~500 Gleichungen) nicht nötig. Interessant wenn Netzwerke aus vielen\n    Modulen zu sehr großen Systemen zusammengesetzt werden.\n  </p>'
     '<p data-lang="en">\n    <strong>Relevance for CMDSolver:</strong> Not needed at current model\n    sizes (up to ~500 equations). Becomes interesting when networks of many\n    modules combine into very large systems.\n  </p>')

# Anderson paragraph
pair('<p>\n    Beschleunigt Fixpunkt-Iterationen x ← G(x) durch Extrapolation aus mehreren\n    vergangenen Iterationswerten. Besonders effektiv bei Systemen die natürlich\n    als Fixpunkt-Iteration formuliert werden können — z.B. bei schwacher Kopplung\n    zwischen Modulen in einer modularen Stream-Architektur.\n  </p>',
     '<p data-lang="de">\n    Beschleunigt Fixpunkt-Iterationen x ← G(x) durch Extrapolation aus mehreren\n    vergangenen Iterationswerten. Besonders effektiv bei Systemen die natürlich\n    als Fixpunkt-Iteration formuliert werden können — z.B. bei schwacher Kopplung\n    zwischen Modulen in einer modularen Stream-Architektur.\n  </p>'
     '<p data-lang="en">\n    Accelerates fixed-point iterations x ← G(x) by extrapolating from several\n    past iteration values. Especially effective for systems that can be naturally\n    formulated as a fixed-point iteration — e.g., when there is weak coupling\n    between modules in a modular stream architecture.\n  </p>')

# Fixpunkt-Iter paragraph
pair('<p>\n    Löst jede Gleichung sequenziell nach einer Variablen auf und iteriert.\n    Konvergiert nur bei kontraktiven Abbildungen — für allgemeine\n    thermodynamische Systeme meist nicht geeignet. War der klassische Ansatz\n    in frühen Prozesssimulatoren (ASPEN, gPROMS vor Version 3).\n  </p>',
     '<p data-lang="de">\n    Löst jede Gleichung sequenziell nach einer Variablen auf und iteriert.\n    Konvergiert nur bei kontraktiven Abbildungen — für allgemeine\n    thermodynamische Systeme meist nicht geeignet. War der klassische Ansatz\n    in frühen Prozesssimulatoren (ASPEN, gPROMS vor Version 3).\n  </p>'
     '<p data-lang="en">\n    Solves each equation sequentially for one variable and iterates.\n    Converges only for contractive mappings — usually unsuitable for general\n    thermodynamic systems. Was the classical approach in early process\n    simulators (ASPEN, gPROMS before version 3).\n  </p>')

# Globales Newton paragraph
pair('<p>\n    Fügt der Jacobi eine Regularisierungsmatrix hinzu: J_reg = J + εI.\n    Einfacher als LM aber weniger theoretisch fundiert. Kann bei sehr\n    schlecht konditionierten Systemen als erster Schritt vor LM nützlich sein.\n  </p>',
     '<p data-lang="de">\n    Fügt der Jacobi eine Regularisierungsmatrix hinzu: J_reg = J + εI.\n    Einfacher als LM aber weniger theoretisch fundiert. Kann bei sehr\n    schlecht konditionierten Systemen als erster Schritt vor LM nützlich sein.\n  </p>'
     '<p data-lang="en">\n    Adds a regularization matrix to the Jacobian: J_reg = J + εI.\n    Simpler than LM but less theoretically grounded. Can be useful as a\n    first step before LM on very ill-conditioned systems.\n  </p>')

# Parallele paragraph
pair('<p>\n    Für zukünftige modulare Architekturen: Wenn das System in Teilsysteme\n    (Mixer, Jetpipe, Nozzle) aufgeteilt wird, kann jedes Teilsystem parallel\n    gelöst werden. Block-Newton-Verfahren lösen die Teilsysteme und iterieren\n    über die Kopplung (Stream-Variablen). Relevant für die geplante\n    Stream-Architektur.\n  </p>',
     '<p data-lang="de">\n    Für zukünftige modulare Architekturen: Wenn das System in Teilsysteme\n    (Mixer, Jetpipe, Nozzle) aufgeteilt wird, kann jedes Teilsystem parallel\n    gelöst werden. Block-Newton-Verfahren lösen die Teilsysteme und iterieren\n    über die Kopplung (Stream-Variablen). Relevant für die geplante\n    Stream-Architektur.\n  </p>'
     '<p data-lang="en">\n    For future modular architectures: when the system is split into subsystems\n    (mixer, jet pipe, nozzle), each subsystem can be solved in parallel.\n    Block-Newton methods solve the subsystems and iterate over the coupling\n    (stream variables). Relevant for the planned stream architecture.\n  </p>')

# ── Section "Verfahrenswahl" ──
pair('<tr><th>Situation</th><th>Empfehlung</th><th>Begründung</th></tr>',
     '<tr>'
     '<th data-lang="de">Situation</th><th data-lang="en">Situation</th>'
     '<th data-lang="de">Empfehlung</th><th data-lang="en">Recommendation</th>'
     '<th data-lang="de">Begründung</th><th data-lang="en">Reason</th>'
     '</tr>')

td_pair('Standardfall, guter Startvektor', 'Default case, good starting vector')
td_pair('Beste Kombination aus Geschwindigkeit und Robustheit',
        'Best combination of speed and robustness')
td_pair('Kleines System (n &lt; 50)', 'Small system (n &lt; 50)')
td_pair('Dichte LU schnell genug, einfache Implementierung',
        'Dense LU fast enough, simple implementation')
td_pair('Schlechte Kondition (κ &gt; 10¹²)', 'Poor conditioning (κ &gt; 10¹²)')
td_pair('Robuster gegenüber nahezu singulärer Jacobi',
        'More robust against near-singular Jacobian')
td_pair('Schlechter Startvektor / weit von Lösung',
        'Bad starting vector / far from solution')
td_pair('Verfolgt Lösungspfad von einfachem Start',
        'Tracks the solution path from a simple start')
td_pair('Viele ähnliche Runs (Parameterstudie)',
        'Many similar runs (parameter study)')
td_pair('Jacobi-Update günstiger als Neuberechnung',
        'Jacobian update cheaper than recomputation')
td_pair('Debugging / Analyse', 'Debugging / analysis')
td_pair('Alle 7 Solver vergleichen', 'Compare all 7 solvers')

# Faustregel note
pair('<div class="note green">\n    <strong>Faustregel:</strong> Beginne immer mit <code>NEWTON_SPARSE_ARMIJO</code>.\n    Wechsle zu LM wenn κ-Warnungen auftreten. Verwende Homotopie nur wenn\n    Newton und LM nicht konvergieren — Homotopie ist langsamer aber robuster.\n  </div>',
     '<div class="note green" data-lang="de">\n    <strong>Faustregel:</strong> Beginne immer mit <code>NEWTON_SPARSE_ARMIJO</code>.\n    Wechsle zu LM wenn κ-Warnungen auftreten. Verwende Homotopie nur wenn\n    Newton und LM nicht konvergieren — Homotopie ist langsamer aber robuster.\n  </div>'
     '<div class="note green" data-lang="en">\n    <strong>Rule of thumb:</strong> Always start with <code>NEWTON_SPARSE_ARMIJO</code>.\n    Switch to LM when κ warnings appear. Use homotopy only when Newton and LM\n    fail to converge — homotopy is slower but more robust.\n  </div>')

# Status badges that contain German labels — only "-TEST Modus" has DE text
pair('<span class="badge b-info">-TEST Modus</span>',
     '<span class="badge b-info" data-lang="de">-TEST Modus</span>'
     '<span class="badge b-info" data-lang="en">-TEST Mode</span>')

# ── Footer ──
pair('<span>CMDSolver Docs · Mathematischer Überblick · v2.5</span>',
     '<span data-lang="de">CMDSolver Docs · Mathematischer Überblick · v2.5</span>'
     '<span data-lang="en">CMDSolver Docs · Mathematical Overview · v2.5</span>')
pair('<a href="index.html">← Übersicht</a>',
     '<a href="index.html" data-lang="de">← Übersicht</a>'
     '<a href="index.html" data-lang="en">← Overview</a>')
pair('<a href="solver_comparison.html">Vergleichsmatrix →</a>',
     '<a href="solver_comparison.html" data-lang="de">Vergleichsmatrix →</a>'
     '<a href="solver_comparison.html" data-lang="en">Comparison Matrix →</a>')

# Apply
missing = []
for i, (old, new) in enumerate(REPS):
    if old not in html: missing.append((i, old[:80])); continue
    html = html.replace(old, new, 1)

p.write_text(html, encoding='utf-8')
print(f'Applied {len(REPS) - len(missing)} / {len(REPS)} replacements')
if missing:
    print('NOT FOUND:')
    for i, s in missing[:10]: print(f'  #{i}: {s!r}')
