#!/usr/bin/env python3
"""Translate batch_mode.html body to bilingual DE/EN.

Special case: the 'jump detection' section has a pre-existing half-baked
bilingual attempt (DE/EN side by side without data-lang) AND a broken table
with 5 <td>s per row. Rebuilds the section cleanly.
"""
from pathlib import Path

p = Path('/home/claude/build/batch_mode.html')
html = p.read_text(encoding='utf-8')

REPS = []
def pair(old, new): REPS.append((old, new))

# ── Nav ──
NAV = [
    ('overview', 'Überblick', 'Overview'),
    ('input', 'Eingabe-CSV', 'Input CSV'),
    ('output', 'Ausgabe-CSV', 'Output CSV'),
    ('warmstart', 'Warm-Start', 'Warm-Start'),
    ('jumpdetect', 'Sprung-Erkennung', 'Jump Detection'),
    ('usage', 'Verwendung', 'Usage'),
    ('uformat', '-U: Format', '-U: Format'),
    ('tips', 'Hinweise', 'Tips'),
]
for anchor, de, en in NAV:
    pair(f'<a href="#{anchor}">{de}</a>',
         f'<a href="#{anchor}" data-lang="de">{de}</a>'
         f'<a href="#{anchor}" data-lang="en">{en}</a>')

# ── h2 ──
def h2(de, en):
    pair(f'<h2>{de}</h2>',
         f'<h2 data-lang="de">{de}</h2><h2 data-lang="en">{en}</h2>')

h2('Überblick', 'Overview')
h2('Eingabe-CSV — Format', 'Input CSV — Format')
h2('Ausgabe-CSV — Format', 'Output CSV — Format')
h2('Warm-Start', 'Warm-Start')
h2('Verwendung — CLI', 'Usage — CLI')
h2('-U: Datei — Einzelpunkt-Override', '-U: File — Single-point Override')
h2('Hinweise & Tipps', 'Notes & Tips')

# ── h3 ──
def h3(de, en):
    pair(f'<h3>{de}</h3>',
         f'<h3 data-lang="de">{de}</h3><h3 data-lang="en">{en}</h3>')

h3('Struktur', 'Structure')
h3('Regeln', 'Rules')
h3('Konkretes Beispiel', 'Concrete example')
h3('Spalten', 'Columns')
h3('Beispielausgabe', 'Example output')
h3('Minimaler Aufruf', 'Minimal invocation')
h3('Mit Solver-Auswahl', 'With solver selection')
h3('Mit Equilibrierung (empfohlen für aerothermodynamische Modelle)',
   'With equilibration (recommended for aerothermodynamic models)')
h3('Alle Variablen in Ausgabe', 'All variables in output')
h3('Mit Startwert-Optimierung', 'With starting-value optimization')
h3('Vollständige Optionsübersicht', 'Full option overview')
h3('CSV-Datei erstellen', 'Creating the CSV file')
h3('Betriebspunkte sortieren', 'Sorting operating points')
h3('Nicht-konvergierte Runs', 'Non-converged runs')
h3('Ausgabedatei', 'Output file')
h3('Große Parameterstudien', 'Large parameter studies')

# ── Overview section ──
pair('<p>Der Batch-Modus löst dasselbe Gleichungssystem (CAS-Datei) für viele\n  verschiedene Betriebspunkte. Jeder Betriebspunkt definiert neue Werte für\n  ausgewählte fixierte Eingabevariablen — alle freien Variablen werden vom\n  Solver berechnet.</p>',
     '<p data-lang="de">Der Batch-Modus löst dasselbe Gleichungssystem (CAS-Datei) für viele\n  verschiedene Betriebspunkte. Jeder Betriebspunkt definiert neue Werte für\n  ausgewählte fixierte Eingabevariablen — alle freien Variablen werden vom\n  Solver berechnet.</p>'
     '<p data-lang="en">Batch mode solves the same equation system (CAS file) for many different\n  operating points. Each operating point defines new values for selected fixed\n  input variables — all free variables are computed by the solver.</p>')

# Flow-card labels
pair('<span class="fc-label">Gleichungssystem<br>(unverändert für alle Runs)</span>',
     '<span class="fc-label" data-lang="de">Gleichungssystem<br>(unverändert für alle Runs)</span>'
     '<span class="fc-label" data-lang="en">Equation system<br>(same for all runs)</span>')
pair('<span class="fc-label">Betriebspunkte<br>(N Zeilen = N Runs)</span>',
     '<span class="fc-label" data-lang="de">Betriebspunkte<br>(N Zeilen = N Runs)</span>'
     '<span class="fc-label" data-lang="en">Operating points<br>(N rows = N runs)</span>')
pair('<span class="fc-label">result_batch.csv<br>(alle Ergebnisse)</span>',
     '<span class="fc-label" data-lang="de">result_batch.csv<br>(alle Ergebnisse)</span>'
     '<span class="fc-label" data-lang="en">result_batch.csv<br>(all results)</span>')

pair('<p>BatchRunner wird automatisch aktiviert wenn die <code>-I:</code>-Datei\n  die Endung <code>.csv</code> hat. Die zugehörige CAS-Datei muss im selben\n  Verzeichnis liegen und denselben Dateinamen haben:</p>',
     '<p data-lang="de">BatchRunner wird automatisch aktiviert wenn die <code>-I:</code>-Datei\n  die Endung <code>.csv</code> hat. Die zugehörige CAS-Datei muss im selben\n  Verzeichnis liegen und denselben Dateinamen haben:</p>'
     '<p data-lang="en">BatchRunner is activated automatically when the <code>-I:</code> file has\n  the <code>.csv</code> extension. The matching CAS file must be in the same\n  directory and share the same filename:</p>')

# Code-comment lines inside the path-illustration <pre>
pair('parameterstudie.csv    ← Eingabe: -I:parameterstudie.csv\nparameterstudie.cas    ← Gleichungssystem (automatisch gesucht, gleicher Name)',
     '<span data-lang="de">parameterstudie.csv    ← Eingabe: -I:parameterstudie.csv\nparameterstudie.cas    ← Gleichungssystem (automatisch gesucht, gleicher Name)</span>'
     '<span data-lang="en">parameterstudie.csv    ← Input: -I:parameterstudie.csv\nparameterstudie.cas    ← Equation system (auto-located, same name)</span>')

pair('<div class="note blue">\n    <strong>Abgrenzung der Flags:</strong>\n    <code>-I:</code> bestimmt immer die Haupteingabedatei — <code>.cas</code> für Single-Run,\n    <code>.csv</code> für Batch-Modus.<br>\n    <code>-U:</code> ist für Variablen-Overrides (Einzelpunkte, Key:Value Format).<br>\n    <code>-C:</code> gibt die CAS-Basisdatei explizit an wenn sie nicht denselben Namen wie die CSV hat.\n  </div>',
     '<div class="note blue" data-lang="de">\n    <strong>Abgrenzung der Flags:</strong>\n    <code>-I:</code> bestimmt immer die Haupteingabedatei — <code>.cas</code> für Single-Run,\n    <code>.csv</code> für Batch-Modus.<br>\n    <code>-U:</code> ist für Variablen-Overrides (Einzelpunkte, Key:Value Format).<br>\n    <code>-C:</code> gibt die CAS-Basisdatei explizit an wenn sie nicht denselben Namen wie die CSV hat.\n  </div>'
     '<div class="note blue" data-lang="en">\n    <strong>Flag boundaries:</strong>\n    <code>-I:</code> always denotes the main input file — <code>.cas</code> for single run,\n    <code>.csv</code> for batch mode.<br>\n    <code>-U:</code> is for variable overrides (single point, Key:Value format).<br>\n    <code>-C:</code> explicitly specifies the CAS base file when it does not share the CSV\'s name.\n  </div>')

# ── Input section ──
# Structure pre-block (CSV header demo with comments)
pair('<pre># Kommentarzeilen beginnen mit # oder // — werden ignoriert\n# Leerzeilen werden ebenfalls ignoriert\n#\n# Erste Nicht-Kommentar-Zeile: Header mit Variablennamen\nVARNAME1, VARNAME2, VARNAME3\n# Danach: eine Zeile pro Betriebspunkt (Datenzeilen)\n289.83, 196273.07, 98136.5\n295.00, 200000.00, 98136.5\n300.00, 210000.00, 95000.0</pre>',
     '<pre data-lang="de"># Kommentarzeilen beginnen mit # oder // — werden ignoriert\n# Leerzeilen werden ebenfalls ignoriert\n#\n# Erste Nicht-Kommentar-Zeile: Header mit Variablennamen\nVARNAME1, VARNAME2, VARNAME3\n# Danach: eine Zeile pro Betriebspunkt (Datenzeilen)\n289.83, 196273.07, 98136.5\n295.00, 200000.00, 98136.5\n300.00, 210000.00, 95000.0</pre>'
     '<pre data-lang="en"># Comment lines start with # or // — they are ignored\n# Blank lines are also ignored\n#\n# First non-comment line: header with variable names\nVARNAME1, VARNAME2, VARNAME3\n# Then: one line per operating point (data rows)\n289.83, 196273.07, 98136.5\n295.00, 200000.00, 98136.5\n300.00, 210000.00, 95000.0</pre>')

# Rules table
pair('<thead><tr><th>Regel</th><th>Details</th></tr></thead>',
     '<thead><tr>'
     '<th data-lang="de">Regel</th><th data-lang="en">Rule</th>'
     '<th data-lang="de">Details</th><th data-lang="en">Details</th>'
     '</tr></thead>')

def td_pair(de, en):
    pair(f'<td>{de}</td>', f'<td data-lang="de">{de}</td><td data-lang="en">{en}</td>')

td_pair('Trennzeichen', 'Separator')
td_pair('Komma <code>,</code> — Leerzeichen vor/nach dem Komma werden ignoriert',
        'Comma <code>,</code> — whitespace before/after the comma is ignored')
td_pair('Header-Zeile', 'Header line')
td_pair('Erste Nicht-Kommentar-Zeile. Enthält die Variablennamen genau so wie\n            sie in der CAS-Datei deklariert sind (Groß-/Kleinschreibung egal).',
        'First non-comment line. Contains the variable names exactly as declared\n            in the CAS file (case-insensitive).')
td_pair('Variablentyp', 'Variable type')
pair('<td>Nur <strong>fixierte Variablen</strong> (Spec: Fixed) können als\n            Eingabe gesetzt werden. Freie Variablen werden vom Solver berechnet\n            und können nicht als CSV-Input verwendet werden.</td>',
     '<td data-lang="de">Nur <strong>fixierte Variablen</strong> (Spec: Fixed) können als\n            Eingabe gesetzt werden. Freie Variablen werden vom Solver berechnet\n            und können nicht als CSV-Input verwendet werden.</td>'
     '<td data-lang="en">Only <strong>fixed variables</strong> (Spec: Fixed) can be set as\n            input. Free variables are computed by the solver and cannot be used\n            as CSV input.</td>')
td_pair('Anzahl Spalten', 'Number of columns')
td_pair('Jede Datenzeile muss exakt so viele Werte haben wie der Header Spalten.\n            Zeilen mit falscher Spaltenanzahl werden mit WARNING übersprungen.',
        'Every data row must contain exactly as many values as the header has\n            columns. Rows with mismatched column counts are skipped with a WARNING.')
td_pair('Zahlenwerte', 'Numeric values')
td_pair('Nur numerische Werte — keine Einheiten, keine Strings. Exponentialnotation\n            wie <code>1.96e+05</code> ist erlaubt.',
        'Numeric values only — no units, no strings. Exponential notation such\n            as <code>1.96e+05</code> is allowed.')
td_pair('Kommentare', 'Comments')
td_pair('<code>#</code> oder <code>//</code> am Zeilenanfang — auch zwischen Datenzeilen',
        '<code>#</code> or <code>//</code> at line start — also between data rows')

# Concrete example pre block
pair('<pre># NozzleSystem Parameterstudie — Einlassbedingungen\n# Variablen: Totaltemperatur, Totaldruck, Umgebungsdruck\n#\n# PARTM.F060.TT  PARTM.F060.PT   AMB.PS\n  PARTM.F060.TT, PARTM.F060.PT,  AMB.PS\n  289.83,        196273.07,       98136.5\n  295.00,        200000.00,       98136.5\n  300.00,        210000.00,       95000.0\n  310.00,        220000.00,       95000.0\n  320.00,        230000.00,       90000.0</pre>',
     '<pre data-lang="de"># NozzleSystem Parameterstudie — Einlassbedingungen\n# Variablen: Totaltemperatur, Totaldruck, Umgebungsdruck\n#\n# PARTM.F060.TT  PARTM.F060.PT   AMB.PS\n  PARTM.F060.TT, PARTM.F060.PT,  AMB.PS\n  289.83,        196273.07,       98136.5\n  295.00,        200000.00,       98136.5\n  300.00,        210000.00,       95000.0\n  310.00,        220000.00,       95000.0\n  320.00,        230000.00,       90000.0</pre>'
     '<pre data-lang="en"># NozzleSystem parameter study — inlet conditions\n# Variables: total temperature, total pressure, ambient pressure\n#\n# PARTM.F060.TT  PARTM.F060.PT   AMB.PS\n  PARTM.F060.TT, PARTM.F060.PT,  AMB.PS\n  289.83,        196273.07,       98136.5\n  295.00,        200000.00,       98136.5\n  300.00,        210000.00,       95000.0\n  310.00,        220000.00,       95000.0\n  320.00,        230000.00,       90000.0</pre>')

pair('<div class="note blue">\n    <strong>Variablennamen prüfen:</strong> Wenn ein Variablenname im Header\n    nicht in der CAS-Datei gefunden wird, bricht BatchRunner mit einem Fehler ab.\n    Exakte Schreibweise aus der CAS-Datei verwenden (Punkte, Leerzeichen, Indizes).\n  </div>',
     '<div class="note blue" data-lang="de">\n    <strong>Variablennamen prüfen:</strong> Wenn ein Variablenname im Header\n    nicht in der CAS-Datei gefunden wird, bricht BatchRunner mit einem Fehler ab.\n    Exakte Schreibweise aus der CAS-Datei verwenden (Punkte, Leerzeichen, Indizes).\n  </div>'
     '<div class="note blue" data-lang="en">\n    <strong>Check variable names:</strong> if a variable name in the header is\n    not found in the CAS file, BatchRunner aborts with an error. Use the exact\n    spelling from the CAS file (dots, spaces, indices).\n  </div>')

pair('<div class="note amber">\n    <strong>Nur Fixed-Variablen als Input:</strong> Die CSV-Eingabe überschreibt\n    die <code>Value</code>-Felder der angegebenen Variablen für jeden Run.\n    Variablen die in der CAS-Datei als <code>Spec: Free</code> deklariert sind\n    können nicht als CSV-Input verwendet werden — BatchRunner meldet dies als Fehler.\n  </div>',
     '<div class="note amber" data-lang="de">\n    <strong>Nur Fixed-Variablen als Input:</strong> Die CSV-Eingabe überschreibt\n    die <code>Value</code>-Felder der angegebenen Variablen für jeden Run.\n    Variablen die in der CAS-Datei als <code>Spec: Free</code> deklariert sind\n    können nicht als CSV-Input verwendet werden — BatchRunner meldet dies als Fehler.\n  </div>'
     '<div class="note amber" data-lang="en">\n    <strong>Only fixed variables as input:</strong> CSV input overwrites the\n    <code>Value</code> field of the listed variables for every run. Variables\n    declared as <code>Spec: Free</code> in the CAS file cannot be used as CSV\n    input — BatchRunner reports this as an error.\n  </div>')

# ── Output section ──
pair('<p>BatchRunner schreibt die Ergebnisse in <code>result_batch.csv</code>\n  im aktuellen Arbeitsverzeichnis. Die Datei enthält:</p>',
     '<p data-lang="de">BatchRunner schreibt die Ergebnisse in <code>result_batch.csv</code>\n  im aktuellen Arbeitsverzeichnis. Die Datei enthält:</p>'
     '<p data-lang="en">BatchRunner writes the results to <code>result_batch.csv</code> in the\n  current working directory. The file contains:</p>')

pair('<pre>RUN, STATUS, ITER, FSUM, [Input-Variablen...], [freie Variablen...]</pre>',
     '<pre data-lang="de">RUN, STATUS, ITER, FSUM, [Input-Variablen...], [freie Variablen...]</pre>'
     '<pre data-lang="en">RUN, STATUS, ITER, FSUM, [input variables...], [free variables...]</pre>')

# Output columns table
pair('<thead><tr><th>Spalte</th><th>Typ</th><th>Beschreibung</th></tr></thead>',
     '<thead><tr>'
     '<th data-lang="de">Spalte</th><th data-lang="en">Column</th>'
     '<th data-lang="de">Typ</th><th data-lang="en">Type</th>'
     '<th data-lang="de">Beschreibung</th><th data-lang="en">Description</th>'
     '</tr></thead>')

td_pair('Laufende Nummer des Betriebspunkts (1-basiert)',
        'Sequential number of the operating point (1-based)')
td_pair('<code>CONVERGED</code> oder <code>FAILED</code>',
        '<code>CONVERGED</code> or <code>FAILED</code>')
td_pair('Anzahl Solver-Iterationen', 'Number of solver iterations')
td_pair('Finales Residuum ||F(x)||', 'Final residual ||F(x)||')
td_pair('Input-Variablen', 'Input variables')
td_pair('Werte aus der Eingabe-CSV (unverändert)',
        'Values from the input CSV (unchanged)')
td_pair('Freie Variablen', 'Free variables')
td_pair('Vom Solver berechnete Werte', 'Values computed by the solver')

pair('<div class="note blue">\n    <strong>-BA Flag:</strong> Mit <code>-BA</code> werden auch fixierte Variablen\n    in die Ausgabe geschrieben — nicht nur freie. Nützlich wenn man alle Größen\n    des Modells in einer Datei haben möchte.\n  </div>',
     '<div class="note blue" data-lang="de">\n    <strong>-BA Flag:</strong> Mit <code>-BA</code> werden auch fixierte Variablen\n    in die Ausgabe geschrieben — nicht nur freie. Nützlich wenn man alle Größen\n    des Modells in einer Datei haben möchte.\n  </div>'
     '<div class="note blue" data-lang="en">\n    <strong>-BA flag:</strong> with <code>-BA</code>, fixed variables are\n    written to the output as well — not just free ones. Useful when you want\n    every model quantity in a single file.\n  </div>')

# ── Warm-Start section ──
pair('<p>BatchRunner verwendet automatisch den Lösungsvektor des vorherigen\n  erfolgreichen Runs als Startvektor für den nächsten Run. Das ist der\n  größte Performancevorteil des Batch-Modus:</p>',
     '<p data-lang="de">BatchRunner verwendet automatisch den Lösungsvektor des vorherigen\n  erfolgreichen Runs als Startvektor für den nächsten Run. Das ist der\n  größte Performancevorteil des Batch-Modus:</p>'
     '<p data-lang="en">BatchRunner automatically uses the solution vector of the previous\n  successful run as the starting vector for the next run. This is the biggest\n  performance benefit of batch mode:</p>')

pair('<thead><tr><th>Situation</th><th>Startvektor für Run N</th></tr></thead>',
     '<thead><tr>'
     '<th data-lang="de">Situation</th><th data-lang="en">Situation</th>'
     '<th data-lang="de">Startvektor für Run N</th><th data-lang="en">Starting vector for run N</th>'
     '</tr></thead>')

td_pair('Run 1 (erster Run)', 'Run 1 (first run)')
td_pair('Startwerte aus der CAS-Datei (<code>Value</code>-Felder)',
        'Starting values from the CAS file (<code>Value</code> fields)')
td_pair('Run N, vorheriger Run konvergiert', 'Run N, previous run converged')
td_pair('Lösung von Run N-1 — <strong>Warm-Start</strong>',
        'Solution of run N-1 — <strong>warm-start</strong>')
td_pair('Run N, vorheriger Run nicht konvergiert',
        'Run N, previous run did not converge')
td_pair('Letzter konvergierter Zustand oder CAS-Startwerte',
        'Last converged state or CAS starting values')

pair('<div class="note green">\n    <strong>Vorteil:</strong> Bei nahe beieinanderliegenden Betriebspunkten\n    (z.B. Kennfeldberechnung in kleinen Schritten) konvergiert der Solver\n    typisch in 2-4 Iterationen statt 10-15. Das reduziert die Gesamtlaufzeit\n    einer Parameterstudie um Faktor 3-5.\n  </div>',
     '<div class="note green" data-lang="de">\n    <strong>Vorteil:</strong> Bei nahe beieinanderliegenden Betriebspunkten\n    (z.B. Kennfeldberechnung in kleinen Schritten) konvergiert der Solver\n    typisch in 2-4 Iterationen statt 10-15. Das reduziert die Gesamtlaufzeit\n    einer Parameterstudie um Faktor 3-5.\n  </div>'
     '<div class="note green" data-lang="en">\n    <strong>Advantage:</strong> for closely spaced operating points (e.g.,\n    map computation in small steps), the solver typically converges in 2–4\n    iterations instead of 10–15. This reduces the total runtime of a parameter\n    study by a factor of 3–5.\n  </div>')

pair('<div class="note amber">\n    <strong>Hinweis:</strong> Wenn die Betriebspunkte in der CSV-Datei weit\n    auseinander liegen, kann der Warm-Start den Solver fehlleiten. In diesem\n    Fall ist es besser die Betriebspunkte nach Ähnlichkeit zu sortieren oder\n    ohne Warm-Start zu arbeiten.\n  </div>',
     '<div class="note amber" data-lang="de">\n    <strong>Hinweis:</strong> Wenn die Betriebspunkte in der CSV-Datei weit\n    auseinander liegen, kann der Warm-Start den Solver fehlleiten. In diesem\n    Fall ist es besser die Betriebspunkte nach Ähnlichkeit zu sortieren oder\n    ohne Warm-Start zu arbeiten.\n  </div>'
     '<div class="note amber" data-lang="en">\n    <strong>Note:</strong> when the operating points in the CSV are far apart,\n    the warm-start can mislead the solver. In that case it is better to sort\n    the operating points by similarity or to work without warm-start.\n  </div>')

# ── Usage section ──
pair('<p>Liest <code>parameterstudie.cas</code> aus demselben Verzeichnis.\n  Ergebnis: <code>result_batch.csv</code> im Arbeitsverzeichnis.</p>',
     '<p data-lang="de">Liest <code>parameterstudie.cas</code> aus demselben Verzeichnis.\n  Ergebnis: <code>result_batch.csv</code> im Arbeitsverzeichnis.</p>'
     '<p data-lang="en">Reads <code>parameterstudie.cas</code> from the same directory.\n  Result: <code>result_batch.csv</code> in the working directory.</p>')

pair('<p>Nur für Run 1 relevant — ab Run 2 übernimmt der Warm-Start.</p>',
     '<p data-lang="de">Nur für Run 1 relevant — ab Run 2 übernimmt der Warm-Start.</p>'
     '<p data-lang="en">Only relevant for run 1 — from run 2 onward the warm-start takes over.</p>')

# Options table (in usage section)
pair('<thead><tr><th>Option</th><th>Beschreibung</th></tr></thead>',
     '<thead><tr>'
     '<th>Option</th>'
     '<th data-lang="de">Beschreibung</th><th data-lang="en">Description</th>'
     '</tr></thead>')

td_pair('Aktiviert Batch-Modus. Zugehörige CAS-Datei im selben Verzeichnis.',
        'Activates batch mode. Matching CAS file in the same directory.')
td_pair('Solver-Auswahl — gilt für alle Runs.',
        'Solver selection — applies to all runs.')
td_pair('Skalierungsstrategie — <code>EQUILIBRATE</code> empfohlen.',
        'Scaling strategy — <code>EQUILIBRATE</code> recommended.')
td_pair('Alle Variablen (auch Fixed) in Ausgabe schreiben.',
        'Write all variables (including fixed) to the output.')
td_pair('Startwert-Diagnose und -Optimierung (nur Run 1).',
        'Starting-value diagnostics and optimization (run 1 only).')
td_pair('Pre-Solve Diagnose vor Run 1.', 'Pre-solve diagnostics before run 1.')
td_pair('Residuen-Normierung — für Systeme mit sehr unterschiedlichen Einheiten.',
        'Residual normalization — for systems with widely varying units.')

# ── -U: Datei section ──
pair('<p>Für einen einzelnen Betriebspunkt können Variablen-Overrides mit\n  <code>-U:datei.txt</code> gesetzt werden — ohne eine CSV-Datei zu erstellen.\n  Das Format ist ein semikolon-getrenntes Key:Value Format, eine Variable pro Zeile:</p>',
     '<p data-lang="de">Für einen einzelnen Betriebspunkt können Variablen-Overrides mit\n  <code>-U:datei.txt</code> gesetzt werden — ohne eine CSV-Datei zu erstellen.\n  Das Format ist ein semikolon-getrenntes Key:Value Format, eine Variable pro Zeile:</p>'
     '<p data-lang="en">For a single operating point, variable overrides can be set with\n  <code>-U:file.txt</code> — without creating a CSV file. The format is\n  semicolon-separated key:value, one variable per line:</p>')

pair('<pre># Kommentare mit # oder // werden ignoriert\n/* Block-Kommentare ebenfalls */\nName:PARTM.F060.TT; Value:289.83; Lower:200.0; Upper:400.0; Status:Fixed; Unit:K; Descr:Totaltemperatur\nName:PARTM.F060.PT; Value:196273.07; Lower:50000.0; Upper:500000.0; Status:Fixed; Unit:Pa\nName:AMB.PS; Value:98136.5; Status:Fixed; Unit:Pa</pre>',
     '<pre data-lang="de"># Kommentare mit # oder // werden ignoriert\n/* Block-Kommentare ebenfalls */\nName:PARTM.F060.TT; Value:289.83; Lower:200.0; Upper:400.0; Status:Fixed; Unit:K; Descr:Totaltemperatur\nName:PARTM.F060.PT; Value:196273.07; Lower:50000.0; Upper:500000.0; Status:Fixed; Unit:Pa\nName:AMB.PS; Value:98136.5; Status:Fixed; Unit:Pa</pre>'
     '<pre data-lang="en"># Comments with # or // are ignored\n/* Block comments too */\nName:PARTM.F060.TT; Value:289.83; Lower:200.0; Upper:400.0; Status:Fixed; Unit:K; Descr:Total temperature\nName:PARTM.F060.PT; Value:196273.07; Lower:50000.0; Upper:500000.0; Status:Fixed; Unit:Pa\nName:AMB.PS; Value:98136.5; Status:Fixed; Unit:Pa</pre>')

# Field reference table
pair('<thead><tr><th>Feld</th><th>Pflicht</th><th>Beschreibung</th></tr></thead>',
     '<thead><tr>'
     '<th data-lang="de">Feld</th><th data-lang="en">Field</th>'
     '<th data-lang="de">Pflicht</th><th data-lang="en">Required</th>'
     '<th data-lang="de">Beschreibung</th><th data-lang="en">Description</th>'
     '</tr></thead>')

td_pair('✅ Ja', '✅ Yes')
td_pair('Variablenname exakt wie in der CAS-Datei',
        'Variable name exactly as in the CAS file')
td_pair('✅ Ja', '✅ Yes')
td_pair('Startwert / Fixwert', 'Starting / fixed value')
td_pair('Nein', 'No')
td_pair('<code>Fixed</code> oder <code>Free</code> — überschreibt CAS-Deklaration',
        '<code>Fixed</code> or <code>Free</code> — overrides the CAS declaration')
td_pair('Nein', 'No')
td_pair('Untere Schranke', 'Lower bound')
td_pair('Nein', 'No')
td_pair('Obere Schranke', 'Upper bound')
td_pair('Nein', 'No')
td_pair('Einheit (nur für Dokumentation)', 'Unit (documentation only)')
td_pair('Nein', 'No')
td_pair('Beschreibung (nur für Dokumentation)', 'Description (documentation only)')

pair('<p>Verwendung für Single-Run:</p>',
     '<p data-lang="de">Verwendung für Single-Run:</p>'
     '<p data-lang="en">Usage for single run:</p>')

pair('<div class="note blue">\n    <strong>Hinweis:</strong> Die <code>-U:</code>-Datei kann auch im Batch-Modus\n    verwendet werden — die Overrides gelten dann als Basiswerte für Run 1,\n    werden aber durch die CSV-Werte überschrieben.\n  </div>',
     '<div class="note blue" data-lang="de">\n    <strong>Hinweis:</strong> Die <code>-U:</code>-Datei kann auch im Batch-Modus\n    verwendet werden — die Overrides gelten dann als Basiswerte für Run 1,\n    werden aber durch die CSV-Werte überschrieben.\n  </div>'
     '<div class="note blue" data-lang="en">\n    <strong>Note:</strong> the <code>-U:</code> file can also be used in batch\n    mode — the overrides then act as base values for run 1 but are overwritten\n    by the CSV values.\n  </div>')

# ── Jump-detection section: rebuild the broken parts cleanly ──
# The h2 has DE and EN already side by side without data-lang
pair('<h2><span>Warm-Start Sprung-Erkennung</span>\n      <span>Warm-Start Jump Detection</span></h2>',
     '<h2><span data-lang="de">Warm-Start Sprung-Erkennung</span>'
     '<span data-lang="en">Warm-Start Jump Detection</span></h2>')

# Two intro paragraphs (DE and EN already separate divs, but no data-lang)
pair('<div>\n    <p>Bei Parameterstudien mit Sägezahnkurven als Input (z.B. Druck steigt,\n    fällt, steigt wieder) kann der Warm-Start schaden: der Solver startet mit\n    der Lösung des letzten Betriebspunkts, der weit entfernt ist.</p>\n    <p>Die Sprung-Erkennung verwirft den Warm-Start automatisch wenn sich\n    eine Input-Variable um mehr als den Schwellwert ändert:</p>\n  </div>\n  <div>\n    <p>For parameter studies with sawtooth-shaped inputs (e.g. pressure rises,\n    falls, rises again), the warm-start can be counterproductive: the solver\n    starts from the previous solution which may be far away.</p>\n    <p>Jump detection automatically discards the warm-start when any input\n    variable changes by more than the threshold:</p>\n  </div>',
     '<div data-lang="de">\n    <p>Bei Parameterstudien mit Sägezahnkurven als Input (z.B. Druck steigt,\n    fällt, steigt wieder) kann der Warm-Start schaden: der Solver startet mit\n    der Lösung des letzten Betriebspunkts, der weit entfernt ist.</p>\n    <p>Die Sprung-Erkennung verwirft den Warm-Start automatisch wenn sich\n    eine Input-Variable um mehr als den Schwellwert ändert:</p>\n  </div>\n  <div data-lang="en">\n    <p>For parameter studies with sawtooth-shaped inputs (e.g. pressure rises,\n    falls, rises again), the warm-start can be counterproductive: the solver\n    starts from the previous solution which may be far away.</p>\n    <p>Jump detection automatically discards the warm-start when any input\n    variable changes by more than the threshold:</p>\n  </div>')

# The broken table — 5 td per row should be 3, with DE and EN cells split.
# Fix by replacing the entire <table>...</table>.
pair('''<table>
    <thead><tr>
      <th>Flag</th>
      <th>Beschreibung</th>
      <th>Standard</th>
    </tr></thead>
    <tbody>
      <tr>
        <td>-BC:JUMPTHRESH=0.20</td>
        <td>Warm-Start verwerfen wenn relativer Sprung &gt; 20%</td>
        <td>Ja (20%)</td>
        <td>Discard warm-start if relative jump &gt; 20%</td>
        <td>Yes (20%)</td>
      </tr>
      <tr>
        <td>-BC:JUMPTHRESH=0.10</td>
        <td>Engere Schwelle für feine Sägezahnkurven</td>
        <td>—</td>
        <td>Tighter threshold for fine sawtooth curves</td>
        <td>—</td>
      </tr>
      <tr>
        <td>-BC:JUMPTHRESH=0</td>
        <td>Sprung-Erkennung deaktivieren</td>
        <td>—</td>
        <td>Disable jump detection entirely</td>
        <td>—</td>
      </tr>
    </tbody>
  </table>''',
     '''<table>
    <thead><tr>
      <th>Flag</th>
      <th data-lang="de">Beschreibung</th><th data-lang="en">Description</th>
      <th data-lang="de">Standard</th><th data-lang="en">Default</th>
    </tr></thead>
    <tbody>
      <tr>
        <td>-BC:JUMPTHRESH=0.20</td>
        <td data-lang="de">Warm-Start verwerfen wenn relativer Sprung &gt; 20%</td>
        <td data-lang="en">Discard warm-start if relative jump &gt; 20%</td>
        <td data-lang="de">Ja (20%)</td>
        <td data-lang="en">Yes (20%)</td>
      </tr>
      <tr>
        <td>-BC:JUMPTHRESH=0.10</td>
        <td data-lang="de">Engere Schwelle für feine Sägezahnkurven</td>
        <td data-lang="en">Tighter threshold for fine sawtooth curves</td>
        <td>—</td>
      </tr>
      <tr>
        <td>-BC:JUMPTHRESH=0</td>
        <td data-lang="de">Sprung-Erkennung deaktivieren</td>
        <td data-lang="en">Disable jump detection entirely</td>
        <td>—</td>
      </tr>
    </tbody>
  </table>''')

# Log output captions (DE and EN already separate)
pair('<p><b>Log-Ausgabe bei erkanntem Sprung:</b></p>\n  <p><b>Log output when jump detected:</b></p>',
     '<p data-lang="de"><b>Log-Ausgabe bei erkanntem Sprung:</b></p>'
     '<p data-lang="en"><b>Log output when jump detected:</b></p>')

# Recommendation note (DE and EN side by side)
pair('<div class="note amber">\n    <strong>Empfehlung:</strong>\n    <strong>Recommendation:</strong>\n    <span>Betriebspunkte in der CSV monoton sortieren (aufsteigend oder\n    absteigend) wenn möglich — dann ist der Warm-Start immer günstig und\n    die Sprung-Erkennung greift selten ein.</span>\n    <span>Sort operating points monotonically (ascending or descending)\n    in the CSV when possible — the warm-start is always beneficial and\n    jump detection rarely triggers.</span>\n  </div>',
     '<div class="note amber" data-lang="de">\n    <strong>Empfehlung:</strong>\n    <span>Betriebspunkte in der CSV monoton sortieren (aufsteigend oder\n    absteigend) wenn möglich — dann ist der Warm-Start immer günstig und\n    die Sprung-Erkennung greift selten ein.</span>\n  </div>'
     '<div class="note amber" data-lang="en">\n    <strong>Recommendation:</strong>\n    <span>Sort operating points monotonically (ascending or descending)\n    in the CSV when possible — the warm-start is always beneficial and\n    jump detection rarely triggers.</span>\n  </div>')

# ── Tips section ──
pair('<p>Die CSV-Datei kann in Excel, LibreOffice Calc oder einem Texteditor erstellt werden.\n  Wichtig: als UTF-8 oder ASCII speichern, nicht als Excel-Format (<code>.xlsx</code>).</p>',
     '<p data-lang="de">Die CSV-Datei kann in Excel, LibreOffice Calc oder einem Texteditor erstellt werden.\n  Wichtig: als UTF-8 oder ASCII speichern, nicht als Excel-Format (<code>.xlsx</code>).</p>'
     '<p data-lang="en">The CSV file can be created in Excel, LibreOffice Calc, or a text editor.\n  Important: save as UTF-8 or ASCII, not as Excel format (<code>.xlsx</code>).</p>')

pair('<p>Für optimale Warm-Start-Effizienz die Betriebspunkte so sortieren dass\n  benachbarte Zeilen physikalisch ähnliche Zustände beschreiben — z.B. Druck\n  monoton steigend, Temperatur monoton steigend.</p>',
     '<p data-lang="de">Für optimale Warm-Start-Effizienz die Betriebspunkte so sortieren dass\n  benachbarte Zeilen physikalisch ähnliche Zustände beschreiben — z.B. Druck\n  monoton steigend, Temperatur monoton steigend.</p>'
     '<p data-lang="en">For best warm-start efficiency, sort operating points so that adjacent\n  rows describe physically similar states — e.g., pressure monotonically rising,\n  temperature monotonically rising.</p>')

pair('<p>Runs mit <code>STATUS = FAILED</code> haben in der Ausgabe für freie\n  Variablen den letzten Solver-Zustand (nicht konvergiert). Diese Werte\n  können unphysikalisch sein. Empfehlung: gefilterte Auswertung nur über\n  <code>CONVERGED</code>-Zeilen.</p>',
     '<p data-lang="de">Runs mit <code>STATUS = FAILED</code> haben in der Ausgabe für freie\n  Variablen den letzten Solver-Zustand (nicht konvergiert). Diese Werte\n  können unphysikalisch sein. Empfehlung: gefilterte Auswertung nur über\n  <code>CONVERGED</code>-Zeilen.</p>'
     '<p data-lang="en">Runs with <code>STATUS = FAILED</code> contain the last (non-converged)\n  solver state for free variables. These values may be unphysical. Recommendation:\n  filter analysis to <code>CONVERGED</code> rows only.</p>')

pair('<p><code>result_batch.csv</code> wird immer ins Arbeitsverzeichnis geschrieben\n  (<code>-DI</code> Arbeitsverzeichnis = dort wo der java-Aufruf stattfindet).\n  Bei wiederholten Runs wird die Datei überschrieben.</p>',
     '<p data-lang="de"><code>result_batch.csv</code> wird immer ins Arbeitsverzeichnis geschrieben\n  (<code>-DI</code> Arbeitsverzeichnis = dort wo der java-Aufruf stattfindet).\n  Bei wiederholten Runs wird die Datei überschrieben.</p>'
     '<p data-lang="en"><code>result_batch.csv</code> is always written to the working directory\n  (the directory the java invocation runs from). On repeated runs the file is\n  overwritten.</p>')

pair('<p>Für sehr viele Betriebspunkte (N &gt; 1000) empfiehlt sich\n  <code>-S:BROYDEN_SPARSE</code> — Broyden mit GSPAR ist pro Run schneller\n  als Newton weil die Jacobi nicht jede Iteration neu aufgebaut wird.</p>',
     '<p data-lang="de">Für sehr viele Betriebspunkte (N &gt; 1000) empfiehlt sich\n  <code>-S:BROYDEN_SPARSE</code> — Broyden mit GSPAR ist pro Run schneller\n  als Newton weil die Jacobi nicht jede Iteration neu aufgebaut wird.</p>'
     '<p data-lang="en">For very many operating points (N &gt; 1000), <code>-S:BROYDEN_SPARSE</code>\n  is recommended — Broyden with GSPAR is faster per run than Newton because the\n  Jacobian is not rebuilt every iteration.</p>')

pair('<div class="note blue">\n    <strong>Parameterstudie vs. Optimierung:</strong> BatchRunner ist kein\n    Optimierungsalgorithmus — er löst das Gleichungssystem für vorgegebene\n    Eingabewerte. Für automatische Optimierung (z.B. Wirkungsgradmaximierung)\n    muss ein externer Optimizer die CSV-Datei generieren und die Ausgabe auswerten.\n  </div>',
     '<div class="note blue" data-lang="de">\n    <strong>Parameterstudie vs. Optimierung:</strong> BatchRunner ist kein\n    Optimierungsalgorithmus — er löst das Gleichungssystem für vorgegebene\n    Eingabewerte. Für automatische Optimierung (z.B. Wirkungsgradmaximierung)\n    muss ein externer Optimizer die CSV-Datei generieren und die Ausgabe auswerten.\n  </div>'
     '<div class="note blue" data-lang="en">\n    <strong>Parameter study vs. optimization:</strong> BatchRunner is not an\n    optimization algorithm — it solves the equation system for given input\n    values. For automatic optimization (e.g., efficiency maximization) an\n    external optimizer must generate the CSV file and evaluate the output.\n  </div>')

# ── Footer ──
pair('<span>CMDSolver Docs · Batch-Modus & Parameterstudien · v2.13</span>',
     '<span data-lang="de">CMDSolver Docs · Batch-Modus & Parameterstudien · v2.13</span>'
     '<span data-lang="en">CMDSolver Docs · Batch Mode & Parameter Studies · v2.13</span>')
pair('<a href="solver_options.html">← Solver Optionen</a>',
     '<a href="solver_options.html" data-lang="de">← Solver Optionen</a>'
     '<a href="solver_options.html" data-lang="en">← Solver Options</a>')
pair('<a href="index.html">Startseite</a>',
     '<a href="index.html" data-lang="de">Startseite</a>'
     '<a href="index.html" data-lang="en">Home</a>')

# Apply
missing = []
for i, (old, new) in enumerate(REPS):
    if old not in html: missing.append((i, old[:80])); continue
    html = html.replace(old, new, 1)

p.write_text(html, encoding='utf-8')
print(f'batch_mode.html: {len(REPS) - len(missing)} / {len(REPS)} replacements')
if missing:
    print('NOT FOUND:')
    for i, s in missing[:10]: print(f'  #{i}: {s!r}')
