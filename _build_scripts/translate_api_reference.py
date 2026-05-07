#!/usr/bin/env python3
"""Translates body content of api_reference.html to bilingual DE/EN."""
from pathlib import Path

p = Path('/home/claude/build/api_reference.html')
html = p.read_text(encoding='utf-8')

REPS = []
def pair(old, new): REPS.append((old, new))

# ── Nav ──
NAV = [
  ('SolverAPI', 'SolverAPI'),
  ('SolverResult', 'SolverResult'),
  ('SolverConfig', 'SolverConfig'),
  ('ParseError', 'ParseError'),
  ('SolverType', 'SolverType'),
  ('HomotopyConfig', 'HomotopyConfig'),
]
for label_de, label_en in NAV:
    # nav links use #anchor format - extract the anchor name (lowercased)
    anchor = label_de.lower().replace('config', 'config')
    # Easier: explicit replacements
    pass

pair('<a href="#solverapi">SolverAPI</a>',
     '<a href="#solverapi" data-lang="de">SolverAPI</a>'
     '<a href="#solverapi" data-lang="en">SolverAPI</a>')
pair('<a href="#solverresult">SolverResult</a>',
     '<a href="#solverresult" data-lang="de">SolverResult</a>'
     '<a href="#solverresult" data-lang="en">SolverResult</a>')
pair('<a href="#solverconfig">SolverConfig</a>',
     '<a href="#solverconfig" data-lang="de">SolverConfig</a>'
     '<a href="#solverconfig" data-lang="en">SolverConfig</a>')
pair('<a href="#parseerror">ParseError</a>',
     '<a href="#parseerror" data-lang="de">ParseError</a>'
     '<a href="#parseerror" data-lang="en">ParseError</a>')
pair('<a href="#solvertype">SolverType</a>',
     '<a href="#solvertype" data-lang="de">SolverType</a>'
     '<a href="#solvertype" data-lang="en">SolverType</a>')
pair('<a href="#homotopyconfig">HomotopyConfig</a>',
     '<a href="#homotopyconfig" data-lang="de">HomotopyConfig</a>'
     '<a href="#homotopyconfig" data-lang="en">HomotopyConfig</a>')

# ── h2 ──
def h2(de, en):
    pair(f'<h2>{de}</h2>',
         f'<h2 data-lang="de">{de}</h2><h2 data-lang="en">{en}</h2>')
h2('SolverAPI', 'SolverAPI')
h2('SolverResult', 'SolverResult')
h2('SolverConfig.Builder', 'SolverConfig.Builder')
h2('ParseError', 'ParseError')
h2('SolverType — Enum', 'SolverType — Enum')
h2('HomotopyConfig', 'HomotopyConfig')

# ── Top note (Method-Chaining) ──
pair('<div class="note blue">\n  <strong>Method-Chaining:</strong> Alle <code>SolverAPI</code>-Setter geben\n  <code>this</code> zurück und können daher verkettet werden.\n  <span class="method-chain">↩ this</span> zeigt diese Methoden an.\n</div>',
     '<div class="note blue" data-lang="de">\n  <strong>Method-Chaining:</strong> Alle <code>SolverAPI</code>-Setter geben\n  <code>this</code> zurück und können daher verkettet werden.\n  <span class="method-chain">↩ this</span> zeigt diese Methoden an.\n</div>'
     '<div class="note blue" data-lang="en">\n  <strong>Method chaining:</strong> all <code>SolverAPI</code> setters return\n  <code>this</code> and can therefore be chained.\n  <span class="method-chain">↩ this</span> marks these methods.\n</div>')

# ── api-class-desc (6 of them) ──
API_CLASS_DESCS = [
  ('Programmatischer Einstiegspunkt für CMDSolver ohne CLI. Kapselt Laden, Konfiguration\n      und Ausführung in einer fluenten API. Thread-safety: eine Instanz pro Thread.',
   'Programmatic entry point for CMDSolver without CLI. Encapsulates loading, configuration,\n      and execution in a fluent API. Thread safety: one instance per thread.'),
  ('Unveränderliches Ergebnis-Objekt eines <code>solve()</code>-Aufrufs. Enthält den Lösungsvektor,\n      Konvergenzstatus, ParseErrors und Diagnose-Informationen.',
   'Immutable result object from a <code>solve()</code> call. Contains the solution vector,\n      convergence status, ParseErrors, and diagnostic information.'),
  ('Builder-Pattern für unveränderliche <code>SolverConfig</code>-Objekte. Wird intern von <code>SolverAPI</code>\n      verwendet — kann aber auch direkt für vorgefertigte Konfigurationen genutzt werden.',
   'Builder pattern for immutable <code>SolverConfig</code> objects. Used internally by <code>SolverAPI</code>\n      — can also be used directly for predefined configurations.'),
  ('Strukturierter Parser-Fehler mit Zeilennummer, Schweregrad und Kontext. Wird von\n      <code>SolverResult.getParseErrors()</code> zurückgegeben.',
   'Structured parser error with line number, severity, and context. Returned by\n      <code>SolverResult.getParseErrors()</code>.'),
  ('Enum aller verfügbaren Solver-Algorithmen. 7 produktive Solver: NEWTON_ARMIJO,\n      NEWTON_SPARSE, NEWTON_SPARSE_ARMIJO, LEVENBERG_MARQUARDT, BROYDEN, BROYDEN_SPARSE, HOMOTOPY.',
   'Enum of all available solver algorithms. 7 production solvers: NEWTON_ARMIJO,\n      NEWTON_SPARSE, NEWTON_SPARSE_ARMIJO, LEVENBERG_MARQUARDT, BROYDEN, BROYDEN_SPARSE, HOMOTOPY.'),
  ('Konfiguration für den Homotopie-Solver — Anzahl Schritte, Schrittweite, innerer Solver.',
   'Configuration for the homotopy solver — number of steps, step size, inner solver.'),
]

# Convert to in-place wrappers using data-lang on the api-class-desc div
for de, en in API_CLASS_DESCS:
    pair(f'<div class="api-class-desc">\n      {de}\n    </div>',
         f'<div class="api-class-desc" data-lang="de">\n      {de}\n    </div>'
         f'<div class="api-class-desc" data-lang="en">\n      {en}\n    </div>')

# ── method-desc (49 entries) ──
# Each is wrapped in <div class="method-desc">...</div>. Some span multiple lines.
# Strategy: replace the FULL <div class="method-desc">...</div> with a pair.
M = [
  ('Erzeugt eine neue SolverAPI-Instanz mit Standard-Konfiguration\n      (Newton-Armijo, tol=1e-7, maxIter=100).',
   'Creates a new SolverAPI instance with default configuration\n      (Newton-Armijo, tol=1e-7, maxIter=100).'),
  ('Lädt und parst eine CAS-Datei vom Dateisystem. Muss vor <code>solve()</code> aufgerufen werden.',
   'Loads and parses a CAS file from the file system. Must be called before <code>solve()</code>.'),
  ('Lädt das CAS-Modell aus einem String statt aus einer Datei. Nützlich für dynamisch generierte Modelle oder Unit-Tests. <code>refVal</code> typisch: <code>content.length()</code>.',
   'Loads the CAS model from a string instead of a file. Useful for dynamically generated models or unit tests. <code>refVal</code> is typically <code>content.length()</code>.'),
  ('Lädt eine <code>-U:</code>-Datei mit Variablen-Overrides (Startwerte, Bounds, Status).\n      Äquivalent zu <code>-U:</code> auf der CLI.',
   'Loads a <code>-U:</code> file with variable overrides (starting values, bounds, status).\n      Equivalent to <code>-U:</code> on the CLI.'),
  ('Setzt den Startwert einer freien Variablen. Der Status (Free/Fixed) wird nicht geändert. Name ist case-insensitiv.',
   'Sets the starting value of a free variable. The status (Free/Fixed) is not changed. Name is case-insensitive.'),
  ('Fixiert eine Variable auf den angegebenen Wert — ändert Status auf Fixed und setzt den Wert. Damit wird die Variable zur Randbedingung.',
   'Fixes a variable to the given value — changes its status to Fixed and assigns the value. This turns the variable into a boundary condition.'),
  ('Wählt den Solver-Algorithmus. Standard: <code>NEWTON_ARMIJO</code>.\n      Empfohlen: <code>NEWTON_SPARSE_ARMIJO</code> für die meisten Systeme.',
   'Selects the solver algorithm. Default: <code>NEWTON_ARMIJO</code>.\n      Recommended: <code>NEWTON_SPARSE_ARMIJO</code> for most systems.'),
  ('Setzt die absolute Konvergenzschwelle ||F(x)|| &lt; tolerance. Standard: <code>1e-7</code>.',
   'Sets the absolute convergence threshold ||F(x)|| &lt; tolerance. Default: <code>1e-7</code>.'),
  ('Relatives Abbruchkriterium (neu in v2.10). Konvergenz wenn <code>fsum/fsum_initial &lt; toleranceRelative</code>.\n      Standard: <code>0.0</code> (deaktiviert).',
   'Relative termination criterion (new in v2.10). Convergence when <code>fsum/fsum_initial &lt; toleranceRelative</code>.\n      Default: <code>0.0</code> (disabled).'),
  ('Maximale Iterationen vor Abbruch. Standard: <code>100</code>. Bei LM oder Homotopie ggf. auf 200+ erhöhen.',
   'Maximum iterations before abort. Default: <code>100</code>. For LM or homotopy, raise to 200+ if needed.'),
  ('Setzt die Skalierungsstrategie. <code>NONE</code> (Standard), <code>DIAGONAL</code>, <code>UNIT_INTERVAL</code>. Aktuell experimentell.',
   'Sets the scaling strategy. <code>NONE</code> (default), <code>DIAGONAL</code>, <code>UNIT_INTERVAL</code>. Currently experimental.'),
  ('Aktiviert Residuen-Normierung: fsum = Σ|Fᵢ(x)|/|Fᵢ(x₀)|. Hilfreich bei Systemen mit sehr unterschiedlichen Gleichungsgrößenordnungen.',
   'Enables residual normalization: fsum = Σ|Fᵢ(x)|/|Fᵢ(x₀)|. Helpful for systems with widely varying equation magnitudes.'),
  ('Aktiviert Diagnose-Modus: <code>InitialValueAnalyzer</code> optimiert Startwerte vor dem Solve. Äquivalent zu <code>-DI</code> auf der CLI.',
   'Enables diagnostic mode: <code>InitialValueAnalyzer</code> optimizes starting values before solving. Equivalent to <code>-DI</code> on the CLI.'),
  ('Setzt Homotopie-Konfiguration — nur relevant wenn <code>setSolverType(HOMOTOPY)</code>. Vorgefertigte Konfigurationen: <code>HomotopyConfig.standard()</code>, <code>HomotopyConfig.critical()</code>.',
   'Sets homotopy configuration — only relevant when <code>setSolverType(HOMOTOPY)</code>. Predefined configurations: <code>HomotopyConfig.standard()</code>, <code>HomotopyConfig.critical()</code>.'),
  ('Setzt eine vollständige <code>SolverConfig</code> — überschreibt alle vorherigen setSolverType/setTolerance/etc. Aufrufe.',
   'Sets a complete <code>SolverConfig</code> — overrides any prior setSolverType/setTolerance/etc. calls.'),
  ('Führt den Solve-Prozess aus. Gibt immer ein <code>SolverResult</code> zurück — auch bei Fehler oder Nicht-Konvergenz. Niemals null.',
   'Runs the solve. Always returns a <code>SolverResult</code> — even on failure or non-convergence. Never null.'),
  ('Gibt <code>true</code> zurück wenn ||F(x)|| &lt; tolerance.',
   'Returns <code>true</code> if ||F(x)|| &lt; tolerance.'),
  ('Anzahl Solver-Iterationen. <code>-1</code> wenn nicht verfügbar (Homotopie).',
   'Number of solver iterations. <code>-1</code> if unavailable (Homotopy).'),
  ('Finales ||F(x)|| nach letztem Iterationsschritt. NaN wenn nicht verfügbar.',
   'Final ||F(x)|| after the last iteration step. NaN if unavailable.'),
  ('Fehlermeldung wenn nicht konvergiert. <code>null</code> bei Erfolg.',
   'Error message when not converged. <code>null</code> on success.'),
  ('Gelöster Wert einer Variablen. Name ist case-insensitiv.\n      Gibt <code>Double.NaN</code> wenn Variable nicht vorhanden.',
   'Solved value of a variable. Name is case-insensitive.\n      Returns <code>Double.NaN</code> if the variable is not present.'),
  ('Prüft ob eine Variable im Lösungsvektor vorhanden ist.',
   'Checks whether a variable is present in the solution vector.'),
  ('Alle gelösten Variablenwerte als unveränderliche Map. Schlüssel sind Großbuchstaben-Variablennamen. Leere Map wenn kein Modell geladen.',
   'All solved variable values as an immutable map. Keys are uppercase variable names. Empty map if no model is loaded.'),
  ('Gibt <code>true</code> wenn fatale ParseErrors beim CAS-Parsing aufgetreten sind.',
   'Returns <code>true</code> if fatal ParseErrors occurred during CAS parsing.'),
  ('Alle ParseErrors (ERROR/WARNING/INFO) aus dem Parser-Lauf. Leere Liste wenn keine.',
   'All ParseErrors (ERROR/WARNING/INFO) from the parser run. Empty list if none.'),
  ('Vollständiger Lösungsvektor als formatierter String — alle Variablen mit Wert, Bounds, Einheit und Status.',
   'Complete solution vector as a formatted string — all variables with value, bounds, unit, and status.'),
  ('Schreibt den Lösungsvektor in eine Datei (Semikolon-getrenntes Format).',
   'Writes the solution vector to a file (semicolon-separated format).'),
  ('Schreibt den Lösungsvektor in einen beliebigen <code>Writer</code> — für GUI-Integration via <code>StringWriter</code> oder <code>JTextArea</code>.',
   'Writes the solution vector to any <code>Writer</code> — for GUI integration via <code>StringWriter</code> or <code>JTextArea</code>.'),
  ('Solver-Algorithmus. Standard: <code>NEWTON_ARMIJO</code>.',
   'Solver algorithm. Default: <code>NEWTON_ARMIJO</code>.'),
  ('Maximale Iterationen. Standard: <code>100</code>.',
   'Maximum iterations. Default: <code>100</code>.'),
  ('Konvergenzschwelle. Standard: <code>1e-7</code>.',
   'Convergence threshold. Default: <code>1e-7</code>.'),
  ('Initialer Schrittweiten-Faktor für Armijo-Backtracking. Standard: <code>1.0</code>.',
   'Initial step-size factor for Armijo backtracking. Default: <code>1.0</code>.'),
  ('Minimales α vor Abbruch der Liniensuche. Standard: <code>1e-4</code>.',
   'Minimum α before line search aborts. Default: <code>1e-4</code>.'),
  ('Reduktionsfaktor pro Backtracking-Schritt. Standard: <code>0.5</code>.',
   'Reduction factor per backtracking step. Default: <code>0.5</code>.'),
  ('Initialer LM-Dämpfungsparameter. Standard: <code>1e-6</code>.',
   'Initial LM damping parameter. Default: <code>1e-6</code>.'),
  ('μ-Erhöhungsfaktor (Standard: 2.0) und Reduktionsfaktor (Standard: 5.0) für LM.',
   'μ increase factor (default: 2.0) and reduction factor (default: 5.0) for LM.'),
  ('Jacobi-Reset-Intervall für Broyden. Standard: <code>25</code>.',
   'Jacobian reset interval for Broyden. Default: <code>25</code>.'),
  ('N3-Residuen-Normierung aktivieren. Standard: <code>false</code>.',
   'Enable N3 residual normalization. Default: <code>false</code>.'),
  ('Erzeugt eine unveränderliche <code>SolverConfig</code>-Instanz.',
   'Creates an immutable <code>SolverConfig</code> instance.'),
  ('Schweregrad: <code>ERROR</code> (fatal, Solve nicht möglich), <code>WARNING</code> (möglicherweise problematisch), <code>INFO</code> (Hinweis).',
   'Severity: <code>ERROR</code> (fatal, solve impossible), <code>WARNING</code> (potentially problematic), <code>INFO</code> (informational).'),
  ('Zeilennummer in der CAS-Datei wo der Fehler aufgetreten ist. <code>-1</code> wenn nicht bekannt.',
   'Line number in the CAS file where the error occurred. <code>-1</code> if unknown.'),
  ('Fehlerbeschreibung.', 'Error description.'),
  ('Zeilen-Inhalt oder Kontext-String zur Fehlerlokalisierung. Kann <code>null</code> sein.',
   'Line content or context string for error localization. May be <code>null</code>.'),
  ('Formatierter String: <code>[ERROR] Line 47: Beschreibung — Kontext</code>',
   'Formatted string: <code>[ERROR] Line 47: description — context</code>'),
  ('Beschreibungstext des Solvers für Log-Ausgaben.',
   'Descriptive text of the solver for log output.'),
  ('Parst einen SolverType aus einem String. Case-insensitiv. Gibt <code>NEWTON_ARMIJO</code> als Fallback wenn unbekannt.',
   'Parses a SolverType from a string. Case-insensitive. Returns <code>NEWTON_ARMIJO</code> as fallback if unknown.'),
  ('Standard: 10 Schritte, ds=0.1, innerer Solver: NEWTON_ARMIJO.',
   'Default: 10 steps, ds=0.1, inner solver: NEWTON_ARMIJO.'),
  ('Für schwierige Systeme (κ > 10¹², Ma-Übergänge): 50 Schritte, ds=0.02, dsMax=0.1, iterTarget=3.',
   'For challenging systems (κ > 10¹², Ma transitions): 50 steps, ds=0.02, dsMax=0.1, iterTarget=3.'),
  ('Erzeugt einen Builder für individuelle Konfiguration.\n      Methoden: <code>steps(int)</code>, <code>dsInit(double)</code>, <code>dsMax(double)</code>, <code>iterTarget(int)</code>, <code>innerSolver(SolverType)</code>, <code>maxOuterIter(int)</code>.',
   'Creates a builder for custom configuration.\n      Methods: <code>steps(int)</code>, <code>dsInit(double)</code>, <code>dsMax(double)</code>, <code>iterTarget(int)</code>, <code>innerSolver(SolverType)</code>, <code>maxOuterIter(int)</code>.'),
]

for de, en in M:
    pair(f'<div class="method-desc">{de}</div>',
         f'<div class="method-desc" data-lang="de">{de}</div>'
         f'<div class="method-desc" data-lang="en">{en}</div>')

# ── method-return strings ──
pair('<div class="method-return">Gibt: <span>diese Instanz für Method-Chaining</span></div>',
     '<div class="method-return" data-lang="de">Gibt: <span>diese Instanz für Method-Chaining</span></div>'
     '<div class="method-return" data-lang="en">Returns: <span>this instance for method chaining</span></div>')

# ── Inline cmt comments in code blocks ──
pair('<span class="cmt">// Umgebungsdruck fixieren</span>',
     '<span class="cmt" data-lang="de">// Umgebungsdruck fixieren</span>'
     '<span class="cmt" data-lang="en">// Fix the ambient pressure</span>')

# ── Footer ──
# Find the actual footer text first
pair('<span>CMDSolver Docs · API-Referenz · v2.5</span>',
     '<span data-lang="de">CMDSolver Docs · API-Referenz · v2.5</span>'
     '<span data-lang="en">CMDSolver Docs · API Reference · v2.5</span>')

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
