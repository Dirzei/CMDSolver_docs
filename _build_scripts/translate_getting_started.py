#!/usr/bin/env python3
"""Translates body content of getting_started.html to bilingual DE/EN."""
from pathlib import Path

p = Path('/home/claude/build/getting_started.html')
html = p.read_text(encoding='utf-8')

REPS = []

def add(old, new):
    REPS.append((old, new))

# ── Nav links ──
def navlink(de, en):
    add(f'>{de}</a>', f' data-lang="de">{de}</a><a href="#" data-lang="en"_PLACEHOLDER>{en}</a>')

# Better approach: replace each entire <a href="#X">TEXT</a> nav link
add('<a href="#voraussetzungen">Voraussetzungen</a>',
    '<a href="#voraussetzungen" data-lang="de">Voraussetzungen</a>'
    '<a href="#voraussetzungen" data-lang="en">Prerequisites</a>')
add('<a href="#cli">CLI-Einstieg</a>',
    '<a href="#cli" data-lang="de">CLI-Einstieg</a>'
    '<a href="#cli" data-lang="en">CLI Entry</a>')
add('<a href="#api">API-Einstieg</a>',
    '<a href="#api" data-lang="de">API-Einstieg</a>'
    '<a href="#api" data-lang="en">API Entry</a>')
add('<a href="#ergebnis">Ergebnis lesen</a>',
    '<a href="#ergebnis" data-lang="de">Ergebnis lesen</a>'
    '<a href="#ergebnis" data-lang="en">Read Result</a>')
add('<a href="#naechste">Nächste Schritte</a>',
    '<a href="#naechste" data-lang="de">Nächste Schritte</a>'
    '<a href="#naechste" data-lang="en">Next Steps</a>')

# ── Section headings ──
def h2(de, en):
    add(f'<h2>{de}</h2>',
        f'<h2 data-lang="de">{de}</h2><h2 data-lang="en">{en}</h2>')

h2('Voraussetzungen', 'Prerequisites')
h2('Einstiegspfad 1 — CLI (Command Line)', 'Entry Path 1 — CLI (Command Line)')
h2('Einstiegspfad 2 — SolverAPI (Einbettung)', 'Entry Path 2 — SolverAPI (Embedding)')
h2('Ergebnis ausgeben', 'Read the Result')
h2('Nächste Schritte', 'Next Steps')

def h3(de, en):
    add(f'<h3>{de}</h3>',
        f'<h3 data-lang="de">{de}</h3><h3 data-lang="en">{en}</h3>')

h3('Classpath', 'Classpath')
h3('Alle Solver vergleichen', 'Compare all solvers')
h3('GUI-Integration — SolverLogger in JTextArea',
   'GUI integration — SolverLogger in JTextArea')

# ── Voraussetzungen table ──
add('<thead><tr><th>Komponente</th><th>Version</th><th>Beschaffung</th></tr></thead>',
    '<thead><tr>'
    '<th data-lang="de">Komponente</th><th data-lang="en">Component</th>'
    '<th>Version</th>'
    '<th data-lang="de">Beschaffung</th><th data-lang="en">Source</th>'
    '</tr></thead>')

add('<td>GraalVM 25 oder OpenJDK 17/21 empfohlen</td>',
    '<td data-lang="de">GraalVM 25 oder OpenJDK 17/21 empfohlen</td>'
    '<td data-lang="en">GraalVM 25 or OpenJDK 17/21 recommended</td>')
add('<td>Im Repository unter <code>libs/CASprzak.jar</code></td>',
    '<td data-lang="de">Im Repository unter <code>libs/CASprzak.jar</code></td>'
    '<td data-lang="en">In the repository at <code>libs/CASprzak.jar</code></td>')
add('<td>CMDSolver JAR oder Quellen</td>',
    '<td data-lang="de">CMDSolver JAR oder Quellen</td>'
    '<td data-lang="en">CMDSolver JAR or sources</td>')
add('<td>Repository <code>CMDSolver_repo</code>, Branch <code>main</code>, Tag <code>v2.5</code></td>',
    '<td data-lang="de">Repository <code>CMDSolver_repo</code>, Branch <code>main</code>, Tag <code>v2.5</code></td>'
    '<td data-lang="en">Repository <code>CMDSolver_repo</code>, branch <code>main</code>, tag <code>v2.5</code></td>')

# Classpath note paragraph
add('<p>In Eclipse: <em>Properties → Java Build Path → Libraries</em> → <code>CASprzak.jar</code> hinzufügen.</p>',
    '<p data-lang="de">In Eclipse: <em>Properties → Java Build Path → Libraries</em> → <code>CASprzak.jar</code> hinzufügen.</p>'
    '<p data-lang="en">In Eclipse: <em>Properties → Java Build Path → Libraries</em> → add <code>CASprzak.jar</code>.</p>')

# ── CLI section ──
add('<div class="note blue">\n    <strong>Wähle diesen Pfad wenn:</strong> Du CMDSolver direkt von der Kommandozeile\n    oder aus einem Skript aufrufen willst — ohne Java-Code zu schreiben.\n  </div>',
    '<div class="note blue" data-lang="de">\n    <strong>Wähle diesen Pfad wenn:</strong> Du CMDSolver direkt von der Kommandozeile\n    oder aus einem Skript aufrufen willst — ohne Java-Code zu schreiben.\n  </div>\n  <div class="note blue" data-lang="en">\n    <strong>Choose this path if:</strong> you want to invoke CMDSolver directly from the command line\n    or from a script — without writing any Java code.\n  </div>')

# Step titles + paragraphs (CLI)
def step_title(de, en):
    add(f'<div class="step-title">{de}</div>',
        f'<div class="step-title" data-lang="de">{de}</div>'
        f'<div class="step-title" data-lang="en">{en}</div>')

step_title('CAS-Modell bereitstellen', 'Provide a CAS model')

add('<p>Lege eine <code>.cas</code>-Datei mit Variablen und Gleichungen an.\n      Das einfachste Beispiel — ein lineares System mit 2 Unbekannten:</p>',
    '<p data-lang="de">Lege eine <code>.cas</code>-Datei mit Variablen und Gleichungen an.\n      Das einfachste Beispiel — ein lineares System mit 2 Unbekannten:</p>'
    '<p data-lang="en">Create a <code>.cas</code> file with variables and equations.\n      The simplest example — a linear system with 2 unknowns:</p>')

step_title('Solver aufrufen', 'Invoke the solver')

add('<p>Mit expliziter Solver-Wahl und Diagnose-Modus:</p>',
    '<p data-lang="de">Mit expliziter Solver-Wahl und Diagnose-Modus:</p>'
    '<p data-lang="en">With explicit solver choice and diagnostic mode:</p>')

step_title('Ausgabe lesen', 'Read the output')

add('<p>CMDSolver schreibt <code>result.out</code> ins Arbeitsverzeichnis und gibt\n      die Konvergenztabelle auf der Konsole aus:</p>',
    '<p data-lang="de">CMDSolver schreibt <code>result.out</code> ins Arbeitsverzeichnis und gibt\n      die Konvergenztabelle auf der Konsole aus:</p>'
    '<p data-lang="en">CMDSolver writes <code>result.out</code> to the working directory and prints\n      the convergence table to the console:</p>')

step_title('Startwerte anpassen (optional)', 'Adjust starting values (optional)')

add('<p>Erstelle eine <code>-U:</code>-Datei um Startwerte oder Bounds zur Laufzeit\n      zu überschreiben — ohne die CAS-Datei zu ändern:</p>',
    '<p data-lang="de">Erstelle eine <code>-U:</code>-Datei um Startwerte oder Bounds zur Laufzeit\n      zu überschreiben — ohne die CAS-Datei zu ändern:</p>'
    '<p data-lang="en">Create a <code>-U:</code> file to override starting values or bounds at runtime —\n      without modifying the CAS file:</p>')

# ── API section ──
add('<div class="note blue">\n    <strong>Wähle diesen Pfad wenn:</strong> Du CMDSolver in ein bestehendes Java-Framework\n    einbetten willst — ohne CLI, ohne argv, programmatisch steuerbar.\n  </div>',
    '<div class="note blue" data-lang="de">\n    <strong>Wähle diesen Pfad wenn:</strong> Du CMDSolver in ein bestehendes Java-Framework\n    einbetten willst — ohne CLI, ohne argv, programmatisch steuerbar.\n  </div>\n  <div class="note blue" data-lang="en">\n    <strong>Choose this path if:</strong> you want to embed CMDSolver into an existing Java framework —\n    no CLI, no argv, fully programmatic.\n  </div>')

step_title('Einfachster Aufruf — Modell laden und lösen',
           'Simplest call — load model and solve')
step_title('Method-Chaining — vollständige Konfiguration',
           'Method chaining — full configuration')
step_title('Fehlerbehandlung — ParseErrors und Konvergenzfehler',
           'Error handling — ParseErrors and convergence failures')
step_title('Parameterstudie — mehrere Betriebspunkte',
           'Parameter study — multiple operating points')

# ── Ergebnis ausgeben section ──
add('<thead><tr><th>Methode</th><th>Verwendung</th><th>Beschreibung</th></tr></thead>',
    '<thead><tr>'
    '<th data-lang="de">Methode</th><th data-lang="en">Method</th>'
    '<th data-lang="de">Verwendung</th><th data-lang="en">Use</th>'
    '<th data-lang="de">Beschreibung</th><th data-lang="en">Description</th>'
    '</tr></thead>')

# Method table rows
def td_pair(de, en):
    add(f'<td>{de}</td>', f'<td data-lang="de">{de}</td><td data-lang="en">{en}</td>')

td_pair('Einzelne Variable', 'Single variable')
td_pair('Gibt Double.NaN wenn nicht vorhanden', 'Returns Double.NaN if not present')
td_pair('Existenzprüfung', 'Existence check')
td_pair('Vor getValue() aufrufen wenn unsicher', 'Call before getValue() when unsure')
td_pair('Alle Variablen', 'All variables')
add('<td>Gibt unmodifizierbare Map&lt;String, Double&gt; zurück</td>',
    '<td data-lang="de">Gibt unmodifizierbare Map&lt;String, Double&gt; zurück</td>'
    '<td data-lang="en">Returns an unmodifiable Map&lt;String, Double&gt;</td>')
td_pair('Vollständige Ausgabe', 'Full output')
td_pair('Alle Variablen als formatierter String', 'All variables as a formatted string')
td_pair('Datei schreiben', 'Write to file')
td_pair('Semikolon-getrenntes Format', 'Semicolon-separated format')
td_pair('GUI / Stream', 'GUI / stream')
td_pair('Für JTextArea, StringWriter, etc.', 'For JTextArea, StringWriter, etc.')

# ── Nächste Schritte table ──
add('<thead><tr><th>Ziel</th><th>Kapitel</th></tr></thead>',
    '<thead><tr>'
    '<th data-lang="de">Ziel</th><th data-lang="en">Goal</th>'
    '<th data-lang="de">Kapitel</th><th data-lang="en">Chapter</th>'
    '</tr></thead>')

td_pair('CAS-Datei schreiben', 'Write a CAS file')
add('<td><a href="parser_syntax.html">Kapitel 4 — Parser Syntax</a></td>',
    '<td data-lang="de"><a href="parser_syntax.html">Kapitel 4 — Parser Syntax</a></td>'
    '<td data-lang="en"><a href="parser_syntax.html">Chapter 4 — Parser Syntax</a></td>')
td_pair('Richtigen Solver wählen', 'Choose the right solver')
add('<td><a href="solver_comparison.html">Kapitel 2 — Solver Vergleich</a></td>',
    '<td data-lang="de"><a href="solver_comparison.html">Kapitel 2 — Solver Vergleich</a></td>'
    '<td data-lang="en"><a href="solver_comparison.html">Chapter 2 — Solver Comparison</a></td>')
td_pair('Alle CLI-Optionen', 'All CLI options')
add('<td><a href="solver_options.html">Kapitel 3 — Solver Optionen</a></td>',
    '<td data-lang="de"><a href="solver_options.html">Kapitel 3 — Solver Optionen</a></td>'
    '<td data-lang="en"><a href="solver_options.html">Chapter 3 — Solver Options</a></td>')
td_pair('Solver konvergiert nicht', 'Solver does not converge')
add('<td><a href="troubleshooting.html">Troubleshooting</a></td>',
    '<td data-lang="de"><a href="troubleshooting.html">Troubleshooting</a></td>'
    '<td data-lang="en"><a href="troubleshooting.html">Troubleshooting</a></td>')
td_pair('Alle API-Methoden', 'All API methods')
add('<td><a href="api_reference.html">API-Referenz</a></td>',
    '<td data-lang="de"><a href="api_reference.html">API-Referenz</a></td>'
    '<td data-lang="en"><a href="api_reference.html">API Reference</a></td>')
td_pair('Vollständiges Beispielmodell', 'Complete example model')
add('<td><a href="examples.html">Beispiele</a></td>',
    '<td data-lang="de"><a href="examples.html">Beispiele</a></td>'
    '<td data-lang="en"><a href="examples.html">Examples</a></td>')

# ── Footer ──
add('<span>CMDSolver Docs · Getting Started · v2.5</span>',
    '<span data-lang="de">CMDSolver Docs · Getting Started · v2.5</span>'
    '<span data-lang="en">CMDSolver Docs · Getting Started · v2.5</span>')
add('<a href="index.html">← Übersicht</a>',
    '<a href="index.html" data-lang="de">← Übersicht</a>'
    '<a href="index.html" data-lang="en">← Overview</a>')
add('<a href="math_overview.html">Mathematischer Überblick →</a>',
    '<a href="math_overview.html" data-lang="de">Mathematischer Überblick →</a>'
    '<a href="math_overview.html" data-lang="en">Mathematical Overview →</a>')

# ── Apply ──
missing = []
for i, (old, new) in enumerate(REPS):
    if old not in html:
        missing.append((i, old[:80]))
        continue
    html = html.replace(old, new, 1)

p.write_text(html, encoding='utf-8')
print(f'Applied {len(REPS) - len(missing)} / {len(REPS)} replacements')
if missing:
    print('NOT FOUND:')
    for i, s in missing[:10]:
        print(f'  #{i}: {s}…')
