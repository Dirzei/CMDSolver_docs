#!/usr/bin/env python3
"""Translate solver_options.html body to bilingual DE/EN."""
from pathlib import Path

p = Path('/home/claude/build/solver_options.html')
html = p.read_text(encoding='utf-8')

REPS = []
def pair(old, new): REPS.append((old, new))

# ── Nav ──
NAV = [
    ('aufruf', 'Aufruf', 'Invocation'),
    ('allgemein', 'Allgemein', 'General'),
    ('solver-wahl', 'Solver-Wahl', 'Solver Choice'),
    ('homotopie', 'Homotopie', 'Homotopy'),
    ('broyden', 'Broyden', 'Broyden'),
    ('diagnose', 'Diagnose', 'Diagnostics'),
    ('batch', 'Batch', 'Batch'),
    ('uebersicht', 'Übersicht', 'Overview'),
]
for anchor, de, en in NAV:
    pair(f'<a href="#{anchor}">{de}</a>',
         f'<a href="#{anchor}" data-lang="de">{de}</a>'
         f'<a href="#{anchor}" data-lang="en">{en}</a>')

# ── h2 ──
def h2(de, en):
    pair(f'<h2>{de}</h2>',
         f'<h2 data-lang="de">{de}</h2><h2 data-lang="en">{en}</h2>')

h2('Grundaufruf', 'Basic Invocation')
h2('Allgemeine Optionen — für alle Solver', 'General Options — for All Solvers')
h2('Allgemeine Solver-Parameter', 'General Solver Parameters')
h2('Vollständige Übersicht — Solver und ihre Optionen',
   'Complete Overview — Solvers and Their Options')
h2('Diagnose- und Debug-Optionen', 'Diagnostic and Debug Options')
h2('Batch-Optionen', 'Batch Options')

# h2 with embedded code
pair('<h2>Homotopie-Optionen  <code style="font-size:12px">-SH:...</code></h2>',
     '<h2 data-lang="de">Homotopie-Optionen  <code style="font-size:12px">-SH:...</code></h2>'
     '<h2 data-lang="en">Homotopy Options  <code style="font-size:12px">-SH:...</code></h2>')
pair('<h2>Broyden-Optionen  <code style="font-size:12px">-SB:...</code></h2>',
     '<h2 data-lang="de">Broyden-Optionen  <code style="font-size:12px">-SB:...</code></h2>'
     '<h2 data-lang="en">Broyden Options  <code style="font-size:12px">-SB:...</code></h2>')

# ── h3 ──
def h3(de, en):
    pair(f'<h3>{de}</h3>',
         f'<h3 data-lang="de">{de}</h3><h3 data-lang="en">{en}</h3>')

h3('Vollständiges Beispiel', 'Complete example')
h3('Schnellreferenz — häufigste Kombinationen',
   'Quick reference — most common combinations')

# ── Aufruf section ──
# Code comments inside <pre>
def cmt(de, en):
    pair(f'<span class="cmt">{de}</span>',
         f'<span class="cmt" data-lang="de">{de}</span>'
         f'<span class="cmt" data-lang="en">{en}</span>')

cmt('// Batch-Modus', '// batch mode')
cmt('// Hilfe', '// help')
cmt('// alle Solver testen', '// test all solvers')

# Note about case-insensitive
pair('<div class="note blue">\n    <strong>Argumente sind case-insensitiv.</strong> <code>-S:NEWTON_ARMIJO</code>\n    und <code>-s:newton_armijo</code> sind gleichwertig. Pfade folgen dem\n    Betriebssystem (Windows: Backslash oder Forward-Slash).\n  </div>',
     '<div class="note blue" data-lang="de">\n    <strong>Argumente sind case-insensitiv.</strong> <code>-S:NEWTON_ARMIJO</code>\n    und <code>-s:newton_armijo</code> sind gleichwertig. Pfade folgen dem\n    Betriebssystem (Windows: Backslash oder Forward-Slash).\n  </div>'
     '<div class="note blue" data-lang="en">\n    <strong>Arguments are case-insensitive.</strong> <code>-S:NEWTON_ARMIJO</code>\n    and <code>-s:newton_armijo</code> are equivalent. Paths follow the\n    operating system (Windows: backslash or forward slash).\n  </div>')

# ── Helper for arg-desc blocks ──
def arg_desc(de_inner, en_inner):
    """Wrap an arg-desc block — match the entire <div class="arg-desc">…</div>."""
    pair(f'<div class="arg-desc">\n      {de_inner}\n    </div>',
         f'<div class="arg-desc" data-lang="de">\n      {de_inner}\n    </div>'
         f'<div class="arg-desc" data-lang="en">\n      {en_inner}\n    </div>')

# All 20 arg-desc blocks
arg_desc('Eingabedatei. Unterstützte Formate: <code>.cas</code> (Gleichungssystem),\n      <code>.dat</code> (Gleichungssystem), <code>.csv</code> (Batch-Parameterstudie).',
         'Input file. Supported formats: <code>.cas</code> (equation system),\n      <code>.dat</code> (equation system), <code>.csv</code> (batch parameter study).')

arg_desc('Solver-Auswahl. Standard: <code>NEWTON_ARMIJO</code>.',
         'Solver selection. Default: <code>NEWTON_ARMIJO</code>.')

arg_desc('Variable-Update-Datei — überschreibt Startwerte, Bounds und Status\n      aus der CAS-Datei. Format pro Zeile:\n      <br><code>Name:VAR; Value:1.0; Status:Fixed; Lower:0.0; Upper:2.0; Unit:m/s; Descr:text</code>',
         'Variable update file — overrides starting values, bounds, and status\n      from the CAS file. Per-line format:\n      <br><code>Name:VAR; Value:1.0; Status:Fixed; Lower:0.0; Upper:2.0; Unit:m/s; Descr:text</code>')

arg_desc('Skalierungsstrategie für die Jacobi-Matrix. Standard: <code>NONE</code>.\n      <br><code>NONE</code> — keine Skalierung\n      <br><code>DIAGONAL</code> — Skalierung über Jacobi-Diagonale\n      <br><code>UNIT_INTERVAL</code> — Skalierung über Variablen-Bounds',
         'Scaling strategy for the Jacobian. Default: <code>NONE</code>.\n      <br><code>NONE</code> — no scaling\n      <br><code>DIAGONAL</code> — scaling via Jacobian diagonal\n      <br><code>UNIT_INTERVAL</code> — scaling via variable bounds')

arg_desc('Residuen-Normierung (N3-Modus) aktivieren. Berechnet fsum als\n      <code>Σ|Fᵢ(x)|/|Fᵢ(x₀)|</code> statt <code>Σ|Fᵢ(x)|</code>.\n      Empfohlen bei Systemen mit sehr unterschiedlichen Gleichungsgrößenordnungen\n      (z.B. Pa-Gleichungen neben kg/s-Gleichungen).',
         'Enable residual normalization (N3 mode). Computes fsum as\n      <code>Σ|Fᵢ(x)|/|Fᵢ(x₀)|</code> instead of <code>Σ|Fᵢ(x)|</code>.\n      Recommended on systems with widely varying equation magnitudes\n      (e.g., Pa equations alongside kg/s equations).')

arg_desc('Test-Modus: alle 7 Solver werden nacheinander auf demselben Modell\n      ausgeführt und verglichen. Startwerte werden für jeden Solver zurückgesetzt.\n      Nützlich für Solver-Auswahl und Performance-Vergleich.',
         'Test mode: all 7 solvers are run sequentially on the same model and\n      compared. Starting values are reset for each solver. Useful for solver\n      selection and performance comparison.')

arg_desc('Zeigt die vollständige Hilfe mit allen Argumenten und verfügbaren Solvern.',
         'Shows the full help with all arguments and available solvers.')

# Homotopy
arg_desc('Anzahl der Homotopie-Schritte (Pfadpunkte). Standard: 10.\n      Mehr Schritte = kleinere Einzelschritte = robuster aber langsamer.\n      Bei komplexen Systemen: 50–100.',
         'Number of homotopy steps (path points). Default: 10.\n      More steps = smaller individual steps = more robust but slower.\n      For complex systems: 50–100.')

arg_desc('Initiale Schrittweite Δt entlang des Homotopie-Pfades. Standard: 0.1.\n      Bei numerisch schwierigen Systemen (nahe Ma=1, Phasenübergang): 0.02.',
         'Initial step size Δt along the homotopy path. Default: 0.1.\n      For numerically difficult systems (near Ma=1, phase transition): 0.02.')

arg_desc('Innerer Korrektor-Solver für jeden Homotopie-Schritt. Standard: NEWTON_ARMIJO.\n      Bei schlecht konditionierten Systemen (κ > 10¹²): LEVENBERG_MARQUARDT.',
         'Inner corrector solver for each homotopy step. Default: NEWTON_ARMIJO.\n      On ill-conditioned systems (κ > 10¹²): LEVENBERG_MARQUARDT.')

arg_desc('Vorkonfigurierte Einstellung für kritische Systeme (z.B. Strömung nahe Ma=1,\n      Phasenübergänge). Setzt automatisch: STEPS=50, DS=0.02, DSMAX=0.1, ITER_TARGET=3.',
         'Preset for critical systems (e.g., flow near Ma=1, phase transitions).\n      Automatically sets: STEPS=50, DS=0.02, DSMAX=0.1, ITER_TARGET=3.')

# Broyden
arg_desc('Jacobi-Reset-Intervall — alle n Iterationen wird die Jacobi vollständig\n      neu berechnet statt durch Rang-1-Update aktualisiert. Standard: 25.\n      Kleinere Werte: robuster aber langsamer. Größere Werte: schneller aber\n      mehr Akkumulationsfehler.',
         'Jacobian reset interval — every n iterations the Jacobian is fully\n      rebuilt instead of being updated via rank-1 update. Default: 25.\n      Smaller values: more robust but slower. Larger values: faster but more\n      accumulated error.')

arg_desc('Konditionszahl-Schwellwert für erzwungenen Reset. Standard: 1e10.\n      Wenn κ(J) diesen Wert überschreitet, wird die Jacobi sofort neu\n      aufgebaut unabhängig vom Reset-Intervall.',
         'Condition-number threshold for forced reset. Default: 1e10.\n      When κ(J) exceeds this value, the Jacobian is rebuilt immediately\n      regardless of the reset interval.')

arg_desc('Konditionszahl-Schwellwert für Warm-Start bei Parameterstudien.\n      Wenn der Startvektor vom vorherigen BatchRunner-Run übernommen wird,\n      wird die Jacobi nur neu aufgebaut wenn κ diesen Wert überschreitet.',
         'Condition-number threshold for warm-start in parameter studies.\n      When the starting vector is carried over from the previous BatchRunner\n      run, the Jacobian is rebuilt only when κ exceeds this value.')

# Diagnose
arg_desc('Diagnose-Modus: Führt vor dem eigentlichen Solve einen\n      <code>InitialValueAnalyzer</code>-Durchlauf durch. Optimiert Startwerte\n      automatisch — besonders nützlich wenn viele Variablen schlecht initialisiert sind.\n      Der Solver startet dann mit einem besseren Startvektor.',
         'Diagnostic mode: runs an <code>InitialValueAnalyzer</code> pass before\n      the actual solve. Optimizes starting values automatically — especially\n      useful when many variables are poorly initialized. The solver then starts\n      with a better starting vector.')

# DIAG arg-desc is special — has nested ul. Treat manually.
pair('''<div class="arg-desc">
      Pre-Solve Modell-Diagnose: Analysiert das Gleichungssystem vor dem Solve
      systematisch und erstellt einen HTML-Bericht (<code>model_diagnostics.html</code>
      neben der CAS-Datei) mit Traffic-Light Status (GREEN/AMBER/RED).
      <br><br>
      Analysierte Kategorien:
      <ul style="margin:.4rem 0 0 1.2rem;line-height:2">
        <li><b>Bounds Consistency</b> — Lower &gt; Upper, Value außerhalb Bounds,
            zu enge/weite Bounds, negative Bounds für physikalische Einheiten</li>
        <li><b>NaN Risk</b> — SQRT/LOG/LN mit problematischen Bounds (bounds-basiert,
            keine False Positives bei sicheren Bounds)</li>
        <li><b>Scale Analysis</b> — Größenordnungs-Spanne über alle Variablen,
            Warnung ab 10⁴, Fehler ab 10⁸</li>
        <li><b>Structural Analysis</b> — Orphaned Variables, Constant Equations,
            System-Balance (freie Variablen vs. Gleichungen)</li>
        <li><b>Jacobian Analysis</b> — κ bei x₀, Null-Zeilen (nur bei freien
            Variablen mit Ableitungen ≈ 0), Null-Spalten</li>
        <li><b>Residual Analysis</b> — NaN in F(x₀), Residuen-Dominanz</li>
      </ul>
      Bei <code>NOT_CONVERGED</code> wird der Bericht automatisch erzeugt
      (auch ohne <code>-DIAG</code>).
      <br>Am Ende des Reports: konkrete Solver-Empfehlung basierend auf den Befunden.
    </div>''',
     '''<div class="arg-desc" data-lang="de">
      Pre-Solve Modell-Diagnose: Analysiert das Gleichungssystem vor dem Solve
      systematisch und erstellt einen HTML-Bericht (<code>model_diagnostics.html</code>
      neben der CAS-Datei) mit Traffic-Light Status (GREEN/AMBER/RED).
      <br><br>
      Analysierte Kategorien:
      <ul style="margin:.4rem 0 0 1.2rem;line-height:2">
        <li><b>Bounds Consistency</b> — Lower &gt; Upper, Value außerhalb Bounds,
            zu enge/weite Bounds, negative Bounds für physikalische Einheiten</li>
        <li><b>NaN Risk</b> — SQRT/LOG/LN mit problematischen Bounds (bounds-basiert,
            keine False Positives bei sicheren Bounds)</li>
        <li><b>Scale Analysis</b> — Größenordnungs-Spanne über alle Variablen,
            Warnung ab 10⁴, Fehler ab 10⁸</li>
        <li><b>Structural Analysis</b> — Orphaned Variables, Constant Equations,
            System-Balance (freie Variablen vs. Gleichungen)</li>
        <li><b>Jacobian Analysis</b> — κ bei x₀, Null-Zeilen (nur bei freien
            Variablen mit Ableitungen ≈ 0), Null-Spalten</li>
        <li><b>Residual Analysis</b> — NaN in F(x₀), Residuen-Dominanz</li>
      </ul>
      Bei <code>NOT_CONVERGED</code> wird der Bericht automatisch erzeugt
      (auch ohne <code>-DIAG</code>).
      <br>Am Ende des Reports: konkrete Solver-Empfehlung basierend auf den Befunden.
    </div><div class="arg-desc" data-lang="en">
      Pre-solve model diagnostics: systematically analyzes the equation system
      before the solve and produces an HTML report
      (<code>model_diagnostics.html</code> next to the CAS file) with traffic-light
      status (GREEN/AMBER/RED).
      <br><br>
      Categories analyzed:
      <ul style="margin:.4rem 0 0 1.2rem;line-height:2">
        <li><b>Bounds consistency</b> — Lower &gt; Upper, value outside bounds,
            bounds too tight/wide, negative bounds for physical units</li>
        <li><b>NaN risk</b> — SQRT/LOG/LN with problematic bounds (bounds-based,
            no false positives on safe bounds)</li>
        <li><b>Scale analysis</b> — magnitude span across all variables,
            warning from 10⁴, error from 10⁸</li>
        <li><b>Structural analysis</b> — orphaned variables, constant equations,
            system balance (free variables vs. equations)</li>
        <li><b>Jacobian analysis</b> — κ at x₀, zero rows (only on free
            variables with derivatives ≈ 0), zero columns</li>
        <li><b>Residual analysis</b> — NaN in F(x₀), residual dominance</li>
      </ul>
      On <code>NOT_CONVERGED</code> the report is generated automatically
      (even without <code>-DIAG</code>).
      <br>End of the report: concrete solver recommendation based on the findings.
    </div>''')

arg_desc('Startvektor-Dump: Schreibt alle Variablenwerte vor Iteration 0 in eine\n      Textdatei im <code>-U:</code>-Format. Nützlich für Debugging — der Dump\n      kann direkt als <code>-U:</code>-Datei wiederverwendet werden.',
         'Starting-vector dump: writes all variable values before iteration 0\n      into a text file in <code>-U:</code> format. Useful for debugging — the\n      dump can be reused directly as a <code>-U:</code> file.')

# Batch
arg_desc('Batch-Modus: Wenn die Eingabedatei eine <code>.csv</code>-Datei ist,\n      wird automatisch BatchRunner aktiviert. Die CSV enthält eine Zeile pro\n      Betriebspunkt mit Variablenwerten. Die zugehörige <code>.cas</code>-Datei\n      wird automatisch gesucht (gleiches Verzeichnis, gleicher Name).\n      → <a href="batch_mode.html">Vollständige Batch-Dokumentation</a>',
         'Batch mode: when the input file is a <code>.csv</code>, BatchRunner is\n      activated automatically. The CSV contains one line per operating point\n      with variable values. The matching <code>.cas</code> file is located\n      automatically (same directory, same name).\n      → <a href="batch_mode.html">Full batch documentation</a>')

arg_desc('Batch-Ausgabe: Alle Variablen in die Batch-Ausgabedatei schreiben —\n      auch fixierte Variablen. Standard: nur freie Variablen.',
         'Batch output: write all variables to the batch output file — including\n      fixed variables. Default: only free variables.')

arg_desc('Warm-Start Sprung-Erkennung: Wenn sich ein Input-Wert zwischen zwei\n      aufeinanderfolgenden Runs um mehr als den angegebenen relativen Anteil ändert,\n      wird der Warm-Start verworfen und mit den CAS-Startwerten neu begonnen.\n      <br><br>\n      Standard: <code>0.20</code> (20%). Der maximale relative Sprung wird über\n      alle Input-Spalten berechnet:\n      <br>\n      <code>relJump = |neu - alt| / max(|alt|, |neu|, 1e-10)</code>\n      <br><br>\n      Besonders nützlich bei Sägezahnkurven als Batch-Input — verhindert dass\n      der Warm-Start bei großen Sprüngen den Solver fehlleitet.\n      <code>0</code> deaktiviert die Erkennung vollständig.',
         'Warm-start jump detection: if an input value changes between two\n      consecutive runs by more than the given relative fraction, the warm start\n      is discarded and the run restarts with the CAS starting values.\n      <br><br>\n      Default: <code>0.20</code> (20 %). The maximum relative jump is computed\n      across all input columns:\n      <br>\n      <code>relJump = |new - old| / max(|old|, |new|, 1e-10)</code>\n      <br><br>\n      Particularly useful with sawtooth curves as batch input — prevents the\n      warm start from misleading the solver on large jumps.\n      <code>0</code> disables detection entirely.')

# ── arg-tag labels ──
def arg_tag(de, en):
    pair(f'<span class="arg-tag all">{de}</span>',
         f'<span class="arg-tag all" data-lang="de">{de}</span>'
         f'<span class="arg-tag all" data-lang="en">{en}</span>')

# 'Alle Solver' appears many times
for _ in range(8):
    arg_tag('Alle Solver', 'All solvers')
# 'Alle Solver (nur Batch)' twice
pair('<span class="arg-tag all">Alle Solver (nur Batch)</span>',
     '<span class="arg-tag all" data-lang="de">Alle Solver (nur Batch)</span>'
     '<span class="arg-tag all" data-lang="en">All solvers (batch only)</span>')
pair('<span class="arg-tag all">Alle Solver (nur Batch)</span>',
     '<span class="arg-tag all" data-lang="de">Alle Solver (nur Batch)</span>'
     '<span class="arg-tag all" data-lang="en">All solvers (batch only)</span>')

# 'Nur HOMOTOPY' (4x)
for _ in range(4):
    pair('<span class="arg-tag exclusive">Nur HOMOTOPY</span>',
         '<span class="arg-tag exclusive" data-lang="de">Nur HOMOTOPY</span>'
         '<span class="arg-tag exclusive" data-lang="en">HOMOTOPY only</span>')
# 'Nur BROYDEN / BROYDEN_SPARSE' (3x)
for _ in range(3):
    pair('<span class="arg-tag exclusive">Nur BROYDEN / BROYDEN_SPARSE</span>',
         '<span class="arg-tag exclusive" data-lang="de">Nur BROYDEN / BROYDEN_SPARSE</span>'
         '<span class="arg-tag exclusive" data-lang="en">BROYDEN / BROYDEN_SPARSE only</span>')
# 'Nur NEWTON_ARMIJO' (1x)
pair('<span class="arg-tag exclusive">Nur NEWTON_ARMIJO</span>',
     '<span class="arg-tag exclusive" data-lang="de">Nur NEWTON_ARMIJO</span>'
     '<span class="arg-tag exclusive" data-lang="en">NEWTON_ARMIJO only</span>')

# ── Solver-Wahl section paragraph and note ──
pair('<p>Diese Parameter gelten für alle direkten Solver (Newton, LM, Broyden) —\n  nicht für Homotopie (die hat eigene <code>-SH:</code> Parameter).</p>',
     '<p data-lang="de">Diese Parameter gelten für alle direkten Solver (Newton, LM, Broyden) —\n  nicht für Homotopie (die hat eigene <code>-SH:</code> Parameter).</p>'
     '<p data-lang="en">These parameters apply to all direct solvers (Newton, LM, Broyden) —\n  not to homotopy (which has its own <code>-SH:</code> parameters).</p>')

pair('<div class="note blue">\n    <strong>Hinweis:</strong> Toleranz und maximale Iterationen werden über\n    <code>SolverConfig</code> gesetzt — aktuell nicht direkt über CLI-Argumente\n    konfigurierbar. Standard-Werte: <code>tol=1e-7</code>, <code>maxIter=100</code>.\n    Über <code>SolverAPI</code> sind diese Werte programmtisch setzbar.\n  </div>',
     '<div class="note blue" data-lang="de">\n    <strong>Hinweis:</strong> Toleranz und maximale Iterationen werden über\n    <code>SolverConfig</code> gesetzt — aktuell nicht direkt über CLI-Argumente\n    konfigurierbar. Standard-Werte: <code>tol=1e-7</code>, <code>maxIter=100</code>.\n    Über <code>SolverAPI</code> sind diese Werte programmtisch setzbar.\n  </div>'
     '<div class="note blue" data-lang="en">\n    <strong>Note:</strong> Tolerance and maximum iterations are set via\n    <code>SolverConfig</code> — currently not directly configurable through\n    CLI arguments. Defaults: <code>tol=1e-7</code>, <code>maxIter=100</code>.\n    These values are settable programmatically through <code>SolverAPI</code>.\n  </div>')

# Parameter table
pair('<thead><tr><th>Parameter</th><th>Default</th><th>Gilt für</th><th>Beschreibung</th></tr></thead>',
     '<thead><tr>'
     '<th>Parameter</th><th>Default</th>'
     '<th data-lang="de">Gilt für</th><th data-lang="en">Applies to</th>'
     '<th data-lang="de">Beschreibung</th><th data-lang="en">Description</th>'
     '</tr></thead>')

def td_pair(de, en):
    pair(f'<td>{de}</td>', f'<td data-lang="de">{de}</td><td data-lang="en">{en}</td>')

# Param table rows
td_pair('Alle direkten Solver', 'All direct solvers')
td_pair('Konvergenzschwelle: ||F(x)|| &lt; tolerance',
        'Convergence threshold: ||F(x)|| &lt; tolerance')
td_pair('Alle direkten Solver', 'All direct solvers')
td_pair('Maximale Iterationen vor Abbruch', 'Maximum iterations before abort')
td_pair('Initialer Schrittweiten-Faktor α', 'Initial step-size factor α')
td_pair('Minimales α vor Abbruch der Liniensuche',
        'Minimum α before line search aborts')
td_pair('Reduktionsfaktor pro Backtracking-Schritt',
        'Reduction factor per backtracking step')
td_pair('Wolfe-Bedingungskonstante c₁', 'Wolfe condition constant c₁')
td_pair('Initialer μ-Faktor (× max Diagonale JᵀJ)',
        'Initial μ factor (× max diagonal of JᵀJ)')
td_pair('μ-Erhöhungsfaktor bei schlechtem Schritt',
        'μ increase factor on bad step')
td_pair('μ-Reduktionsfaktor bei gutem Schritt',
        'μ reduction factor on good step')

# ── Homotopy/Broyden notes ──
pair('<div class="note amber">\n    <strong>Nur für <code>-S:HOMOTOPY</code></strong> — alle <code>-SH:</code>\n    Argumente werden ignoriert wenn ein anderer Solver gewählt ist.\n  </div>',
     '<div class="note amber" data-lang="de">\n    <strong>Nur für <code>-S:HOMOTOPY</code></strong> — alle <code>-SH:</code>\n    Argumente werden ignoriert wenn ein anderer Solver gewählt ist.\n  </div>'
     '<div class="note amber" data-lang="en">\n    <strong>Only for <code>-S:HOMOTOPY</code></strong> — all <code>-SH:</code>\n    arguments are ignored when a different solver is selected.\n  </div>')

pair('<div class="note amber">\n    <strong>Nur für <code>-S:BROYDEN</code> und <code>-S:BROYDEN_SPARSE</code></strong>\n  </div>',
     '<div class="note amber" data-lang="de">\n    <strong>Nur für <code>-S:BROYDEN</code> und <code>-S:BROYDEN_SPARSE</code></strong>\n  </div>'
     '<div class="note amber" data-lang="en">\n    <strong>Only for <code>-S:BROYDEN</code> and <code>-S:BROYDEN_SPARSE</code></strong>\n  </div>')

# ── Übersicht table ──
pair('<th>Option</th>\n        <th>Newton<br>Armijo</th>\n        <th>Newton<br>Sparse</th>\n        <th>Newton<br>Sparse+A</th>\n        <th>LM</th>\n        <th>Broyden</th>\n        <th>Broyden<br>Sparse</th>\n        <th>Homotopie</th>',
     '<th>Option</th>\n        <th>Newton<br>Armijo</th>\n        <th>Newton<br>Sparse</th>\n        <th>Newton<br>Sparse+A</th>\n        <th>LM</th>\n        <th>Broyden</th>\n        <th>Broyden<br>Sparse</th>\n        <th data-lang="de">Homotopie</th><th data-lang="en">Homotopy</th>')

# Special table rows with German cell text (the "DV: Startvektor-Dump" row)
pair('<td><code>-DV: Startvektor-Dump</code></td>',
     '<td data-lang="de"><code>-DV: Startvektor-Dump</code></td>'
     '<td data-lang="en"><code>-DV: Starting-vector dump</code></td>')
td_pair('Armijo-Parameter', 'Armijo parameters')
td_pair('LM μ-Parameter', 'LM μ parameters')

# ── Schnellreferenz code comments ──
cmt('// Standard (empfohlen für die meisten Systeme)',
    '// Default (recommended for most systems)')
cmt('// Mit schlechten Startwerten', '// With poor starting values')
cmt('// Großes System, guter Startvektor', '// Large system, good starting vector')
cmt('// Schlecht konditioniert (κ-Warnungen im Log)',
    '// Ill-conditioned (κ warnings in the log)')
cmt('// Newton scheitert, LM scheitert', '// Newton fails, LM fails')
cmt('// Parameterstudie', '// Parameter study')
cmt('// Solver vergleichen', '// Compare solvers')
cmt('// Startvektor analysieren', '// Analyze starting vector')

# ── Footer ──
pair('<span>CMDSolver Docs · Solver Optionen · v2.5</span>',
     '<span data-lang="de">CMDSolver Docs · Solver Optionen · v2.5</span>'
     '<span data-lang="en">CMDSolver Docs · Solver Options · v2.5</span>')
pair('<a href="solver_comparison.html">← Vergleichsmatrix</a>',
     '<a href="solver_comparison.html" data-lang="de">← Vergleichsmatrix</a>'
     '<a href="solver_comparison.html" data-lang="en">← Comparison Matrix</a>')
pair('<a href="parser_syntax.html">Parser →</a>',
     '<a href="parser_syntax.html" data-lang="de">Parser →</a>'
     '<a href="parser_syntax.html" data-lang="en">Parser →</a>')

# Apply
missing = []
for i, (old, new) in enumerate(REPS):
    if old not in html: missing.append((i, old[:80])); continue
    html = html.replace(old, new, 1)

p.write_text(html, encoding='utf-8')
print(f'solver_options.html: {len(REPS) - len(missing)} / {len(REPS)} replacements')
if missing:
    print('NOT FOUND:')
    for i, s in missing[:10]: print(f'  #{i}: {s!r}')
