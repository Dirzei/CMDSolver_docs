#!/usr/bin/env python3
"""Translate parser_syntax.html body to bilingual DE/EN."""
from pathlib import Path

p = Path('/home/claude/build/parser_syntax.html')
html = p.read_text(encoding='utf-8')

REPS = []
def pair(old, new): REPS.append((old, new))

# ── Nav ──
NAV = [
    ('struktur', 'Dateistruktur', 'File Structure'),
    ('variable', 'Variable', 'Variable'),
    ('initialize', 'Initialize', 'Initialize'),
    ('procedure', 'Procedure', 'Procedure'),
    ('gleichungen', 'Gleichungen', 'Equations'),
    ('kontrolle', 'Kontrollstrukturen', 'Control Flow'),
    ('operatoren', 'Operatoren', 'Operators'),
    ('funktionen', 'Funktionen', 'Functions'),
    ('kommentare', 'Kommentare', 'Comments'),
    ('beispiel', 'Vollständiges Beispiel', 'Complete Example'),
]
for anchor, de, en in NAV:
    pair(f'<a href="#{anchor}">{de}</a>',
         f'<a href="#{anchor}" data-lang="de">{de}</a>'
         f'<a href="#{anchor}" data-lang="en">{en}</a>')

# ── h2 ──
def h2(de, en):
    pair(f'<h2>{de}</h2>',
         f'<h2 data-lang="de">{de}</h2><h2 data-lang="en">{en}</h2>')

h2('Dateistruktur — Überblick', 'File Structure — Overview')
h2('Variablendeklaration', 'Variable Declaration')
h2('INITIALIZE Block', 'INITIALIZE Block')
h2('PROCEDURE — Built-in Funktionen einbinden',
   'PROCEDURE — Embedding Built-in Functions')
h2('Gleichungen', 'Equations')
h2('Kontrollstrukturen', 'Control Flow')
h2('Operatoren', 'Operators')
h2('Mathematische Funktionen', 'Mathematical Functions')
h2('Kommentare', 'Comments')
h2('Vollständiges Beispiel — Düsensegment',
   'Complete Example — Nozzle Segment')

# ── h3 ──
def h3(de, en):
    pair(f'<h3>{de}</h3>',
         f'<h3 data-lang="de">{de}</h3><h3 data-lang="en">{en}</h3>')

h3('Langform — VARIABLE Block', 'Long form — VARIABLE block')
h3('Kurzform — AS REAL Inline-Syntax', 'Short form — AS REAL inline syntax')
h3('Variablen-Attribute', 'Variable attributes')
h3('Variablennamen — QNAME-Konvention', 'Variable names — QNAME convention')
h3('Array-Variablen', 'Array variables')
h3('INTEGERPARAMETER — Konstante (neu in v2.10)',
   'INTEGERPARAMETER — Constant (new in v2.10)')
h3('Grundform', 'Basic form')
h3('Residuumsform', 'Residual form')
h3('IF / ELSE / ELSEIF / ENDIF', 'IF / ELSE / ELSEIF / ENDIF')
h3('Struktureller IF — VAR.SPEC Bedingung',
   'Structural IF — VAR.SPEC condition')
h3('FOR — Array-Expansion', 'FOR — array expansion')
h3('Arithmetische Operatoren', 'Arithmetic operators')
h3('Vergleichsoperatoren (in IF-Bedingungen)',
   'Comparison operators (in IF conditions)')
h3('Logische Operatoren', 'Logical operators')
h3('Sonderfunktionen — binäre Expansion (neu in v2.10)',
   'Special functions — binary expansion (new in v2.10)')

# ── Helper for cas-cmt comments inside syntax-block / cas-body ──
def cmt(de, en):
    pair(f'<span class="cas-cmt">{de}</span>',
         f'<span class="cas-cmt" data-lang="de">{de}</span>'
         f'<span class="cas-cmt" data-lang="en">{en}</span>')

# ── Section: Dateistruktur ──
pair('<p>\n    Eine CAS-Datei besteht aus mehreren Sektionen die in beliebiger Reihenfolge\n    auftreten können. Der Parser ist <strong>case-insensitiv</strong> — Schlüsselwörter\n    können groß oder klein geschrieben werden.\n  </p>',
     '<p data-lang="de">\n    Eine CAS-Datei besteht aus mehreren Sektionen die in beliebiger Reihenfolge\n    auftreten können. Der Parser ist <strong>case-insensitiv</strong> — Schlüsselwörter\n    können groß oder klein geschrieben werden.\n  </p>'
     '<p data-lang="en">\n    A CAS file consists of multiple sections that may appear in any order.\n    The parser is <strong>case-insensitive</strong> — keywords can be written\n    in upper or lower case.\n  </p>')

cmt('// ── Sektion 1: Prozedurendeklaration ──────────────────',
    '// ── Section 1: Procedure declaration ──────────────────')
cmt('// ── Sektion 2: Variablendeklaration ───────────────────',
    '// ── Section 2: Variable declaration ───────────────────')
cmt('// oder Kurzschreibweise:', '// or short form:')
cmt('// ── Sektion 3: Startwert-Overrides ────────────────────',
    '// ── Section 3: Starting-value overrides ──────────────')
cmt('// ── Sektion 4: Gleichungen ────────────────────────────',
    '// ── Section 4: Equations ──────────────────────────────')

pair('<div class="note blue">\n    <strong>Parsing-Reihenfolge:</strong> Der Parser liest die Datei zweimal —\n    erst werden alle Variablen und Prozeduren erfasst, dann werden die Gleichungen\n    interpretiert. Die physische Reihenfolge in der Datei spielt für den Parser\n    keine Rolle.\n  </div>',
     '<div class="note blue" data-lang="de">\n    <strong>Parsing-Reihenfolge:</strong> Der Parser liest die Datei zweimal —\n    erst werden alle Variablen und Prozeduren erfasst, dann werden die Gleichungen\n    interpretiert. Die physische Reihenfolge in der Datei spielt für den Parser\n    keine Rolle.\n  </div>'
     '<div class="note blue" data-lang="en">\n    <strong>Parsing order:</strong> the parser reads the file twice — first all\n    variables and procedures are collected, then the equations are interpreted.\n    The physical order in the file does not matter to the parser.\n  </div>')

# ── cas-header titles ──
def cas_header(de, en):
    pair(f'<div class="cas-header">{de}</div>',
         f'<div class="cas-header" data-lang="de">{de}</div>'
         f'<div class="cas-header" data-lang="en">{en}</div>')

cas_header('Syntax — VARIABLE Block', 'Syntax — VARIABLE block')
cas_header('Syntax — AS REAL (empfohlen für moderne Modelle)',
           'Syntax — AS REAL (recommended for modern models)')
cas_header('Array-Deklaration', 'Array declaration')
cas_header('INTEGERPARAMETER Syntax', 'INTEGERPARAMETER syntax')
cas_header('INITIALIZE Block Syntax', 'INITIALIZE block syntax')
cas_header('Prozedur-Deklaration + Aufruf', 'Procedure declaration + call')
cas_header('Gleichungs-Beispiele', 'Equation examples')
cas_header('IF-Block Syntax', 'IF block syntax')
cas_header('Struktureller IF (VAR.SPEC)', 'Structural IF (VAR.SPEC)')
cas_header('FOR-Schleife', 'FOR loop')
cas_header('Kommentar-Syntax', 'Comment syntax')
cas_header('Beispiel: Isentrope Düsenströmung (vereinfacht)',
           'Example: isentropic nozzle flow (simplified)')

# ── Variable section: Variablen-Attribute table ──
pair('<thead><tr><th>Attribut</th><th>Typ</th><th>Pflicht</th><th>Beschreibung</th></tr></thead>',
     '<thead><tr>'
     '<th data-lang="de">Attribut</th><th data-lang="en">Attribute</th>'
     '<th data-lang="de">Typ</th><th data-lang="en">Type</th>'
     '<th data-lang="de">Pflicht</th><th data-lang="en">Required</th>'
     '<th data-lang="de">Beschreibung</th><th data-lang="en">Description</th>'
     '</tr></thead>')

def td_pair(de, en):
    pair(f'<td>{de}</td>', f'<td data-lang="de">{de}</td><td data-lang="en">{en}</td>')

# Variable attribute rows
td_pair('Empfohlen', 'Recommended')
td_pair('Untere physikalische Schranke. PhysicalProjector verwendet diesen Wert.',
        'Lower physical bound. PhysicalProjector uses this value.')
td_pair('Ja', 'Yes')
td_pair('Startwert für den Solver. Guter Startwert beschleunigt Konvergenz erheblich.',
        'Starting value for the solver. A good starting value speeds up convergence significantly.')
td_pair('Empfohlen', 'Recommended')
td_pair('Obere physikalische Schranke.', 'Upper physical bound.')
td_pair('Ja', 'Yes')
pair('<td><strong>Fixed:</strong> bekannter Wert (Randbedingung). <strong>Free:</strong> Unbekannte die der Solver bestimmt.</td>',
     '<td data-lang="de"><strong>Fixed:</strong> bekannter Wert (Randbedingung). <strong>Free:</strong> Unbekannte die der Solver bestimmt.</td>'
     '<td data-lang="en"><strong>Fixed:</strong> known value (boundary condition). <strong>Free:</strong> unknown that the solver determines.</td>')
td_pair('Nein', 'No')
td_pair('Einheit als String in Anführungszeichen. Nur dokumentarisch — kein Unit-Check.',
        'Unit as a quoted string. Documentation only — no unit checking.')
td_pair('Nein', 'No')
td_pair('Beschreibungstext. Erscheint in result.out.',
        'Description text. Appears in result.out.')
td_pair('Nein', 'No')
td_pair('LaTeX-Symbol für Dokumentation (z.B. <code>"P_{T,060}"</code>). Nicht vom Solver verwendet.',
        'LaTeX symbol for documentation (e.g., <code>"P_{T,060}"</code>). Not used by the solver.')

# QNAME paragraph
pair('<p>\n    CMDSolver unterstützt Mehrfach-Punkt-Namen (Qualified Names) für hierarchische\n    Modellstrukturen. Der Punkt ist kein Operator sondern Teil des Namens:\n  </p>',
     '<p data-lang="de">\n    CMDSolver unterstützt Mehrfach-Punkt-Namen (Qualified Names) für hierarchische\n    Modellstrukturen. Der Punkt ist kein Operator sondern Teil des Namens:\n  </p>'
     '<p data-lang="en">\n    CMDSolver supports multi-dot names (qualified names) for hierarchical\n    model structures. The dot is not an operator but part of the name:\n  </p>')

# QNAME comments
cmt('← gültiger Variablenname (keine Operatoren)', '← valid variable name (no operators)')
cmt('← hierarchisch: Modul.Variable', '← hierarchical: module.variable')
cmt('← hierarchisch: Bereich.Größe', '← hierarchical: area.quantity')
cmt('← hierarchisch: Station.Größe', '← hierarchical: station.quantity')

pair('<div class="note amber">\n    <strong>Bugfix B27/B28 (v2.3):</strong> Bounds-Overrides im INITIALIZE-Block\n    für Mehrfach-Punkt-Namen werden korrekt via <code>lastIndexOf(\'.\')</code>\n    extrahiert. <code>PARTM.F060.PS.Upper = ...</code> setzt korrekt den Upper-Bound\n    von <code>PARTM.F060.PS</code>.\n  </div>',
     '<div class="note amber" data-lang="de">\n    <strong>Bugfix B27/B28 (v2.3):</strong> Bounds-Overrides im INITIALIZE-Block\n    für Mehrfach-Punkt-Namen werden korrekt via <code>lastIndexOf(\'.\')</code>\n    extrahiert. <code>PARTM.F060.PS.Upper = ...</code> setzt korrekt den Upper-Bound\n    von <code>PARTM.F060.PS</code>.\n  </div>'
     '<div class="note amber" data-lang="en">\n    <strong>Bugfix B27/B28 (v2.3):</strong> bounds overrides in the INITIALIZE\n    block for multi-dot names are correctly extracted via <code>lastIndexOf(\'.\')</code>.\n    <code>PARTM.F060.PS.Upper = ...</code> correctly sets the upper bound of\n    <code>PARTM.F060.PS</code>.\n  </div>')

# Array comment
cmt('// Erzeugt: ARRAY_VAR[0], ARRAY_VAR[1], ..., ARRAY_VAR[4]',
    '// Generates: ARRAY_VAR[0], ARRAY_VAR[1], ..., ARRAY_VAR[4]')

# INTEGERPARAMETER paragraph
pair('<p>\n    INTEGERPARAMETER definiert eine ganzzahlige Konstante die beim Parsing als\n    Präprozessor-Macro überall im Modell substituiert wird — in Arraygrenzen,\n    FOR-Schleifen und Gleichungen.\n  </p>',
     '<p data-lang="de">\n    INTEGERPARAMETER definiert eine ganzzahlige Konstante die beim Parsing als\n    Präprozessor-Macro überall im Modell substituiert wird — in Arraygrenzen,\n    FOR-Schleifen und Gleichungen.\n  </p>'
     '<p data-lang="en">\n    INTEGERPARAMETER defines an integer constant which, at parse time, is\n    substituted as a preprocessor macro everywhere in the model — in array\n    bounds, FOR loops, and equations.\n  </p>')

# INTEGERPARAMETER cas-cmt comments
cmt('// Deklaration', '// Declaration')
cmt('// Verwendung in Array-Deklaration', '// Use in array declaration')
cmt('// Verwendung in FOR-Schleife', '// Use in FOR loop')
cmt('// Verwendung in Gleichungen', '// Use in equations')
cmt('// wird zu: TOTAL_STAGES = 5 * 1.0', '// becomes: TOTAL_STAGES = 5 * 1.0')

pair('<div class="note blue">\n    <strong>Substitution:</strong> INTEGERPARAMETER werden als Wortgrenzen-sicheres\n    Macro substituiert — <code>NSTAGES_OLD</code> wird nicht verändert wenn\n    <code>NSTAGES</code> definiert ist.\n  </div>',
     '<div class="note blue" data-lang="de">\n    <strong>Substitution:</strong> INTEGERPARAMETER werden als Wortgrenzen-sicheres\n    Macro substituiert — <code>NSTAGES_OLD</code> wird nicht verändert wenn\n    <code>NSTAGES</code> definiert ist.\n  </div>'
     '<div class="note blue" data-lang="en">\n    <strong>Substitution:</strong> INTEGERPARAMETER values are substituted as\n    word-boundary-safe macros — <code>NSTAGES_OLD</code> is left untouched when\n    <code>NSTAGES</code> is defined.\n  </div>')

# ── INITIALIZE section ──
pair('<p>\n    Der INITIALIZE-Block überschreibt Startwerte, Lower- und Upper-Bounds\n    nach dem initialen Parsing. Er wird <strong>nach</strong> der\n    Variablendeklaration ausgewertet — nützlich um Bounds dynamisch\n    aus anderen Variablen zu berechnen.\n  </p>',
     '<p data-lang="de">\n    Der INITIALIZE-Block überschreibt Startwerte, Lower- und Upper-Bounds\n    nach dem initialen Parsing. Er wird <strong>nach</strong> der\n    Variablendeklaration ausgewertet — nützlich um Bounds dynamisch\n    aus anderen Variablen zu berechnen.\n  </p>'
     '<p data-lang="en">\n    The INITIALIZE block overrides starting values and lower/upper bounds\n    after initial parsing. It is evaluated <strong>after</strong> variable\n    declaration — useful for computing bounds dynamically from other variables.\n  </p>')

cmt('// Startwert setzen', '// Set starting value')
cmt('// Lower-Bound überschreiben', '// Override lower bound')
cmt('// Upper-Bound überschreiben', '// Override upper bound')
cmt('// Konstante', '// Constant')

pair('<div class="note blue">\n    <strong>Auswertungsreihenfolge:</strong> INITIALIZE-Ausdrücke werden\n    in Dateireihenfolge ausgewertet. Spätere Zeilen können frühere überschreiben.\n    Expressions auf der rechten Seite können andere Variablen referenzieren —\n    deren Werte stammen aus der Variablendeklaration.\n  </div>',
     '<div class="note blue" data-lang="de">\n    <strong>Auswertungsreihenfolge:</strong> INITIALIZE-Ausdrücke werden\n    in Dateireihenfolge ausgewertet. Spätere Zeilen können frühere überschreiben.\n    Expressions auf der rechten Seite können andere Variablen referenzieren —\n    deren Werte stammen aus der Variablendeklaration.\n  </div>'
     '<div class="note blue" data-lang="en">\n    <strong>Evaluation order:</strong> INITIALIZE expressions are evaluated in\n    file order. Later lines can override earlier ones. Expressions on the right\n    side may reference other variables — their values come from the variable\n    declaration.\n  </div>')

# ── PROCEDURE section ──
pair('<p>\n    Prozeduren verbinden CAS-Variablen mit den thermodynamischen Built-in\n    Funktionen aus <code>BIfunctions.java</code>. Die Deklaration definiert\n    Eingang und Ausgang; der Aufruf erfolgt über <code>CALL</code>.\n  </p>',
     '<p data-lang="de">\n    Prozeduren verbinden CAS-Variablen mit den thermodynamischen Built-in\n    Funktionen aus <code>BIfunctions.java</code>. Die Deklaration definiert\n    Eingang und Ausgang; der Aufruf erfolgt über <code>CALL</code>.\n  </p>'
     '<p data-lang="en">\n    Procedures connect CAS variables to the thermodynamic built-in functions\n    in <code>BIfunctions.java</code>. The declaration defines inputs and outputs;\n    the call is made via <code>CALL</code>.\n  </p>')

cmt('// Deklaration (am Dateianfang)', '// Declaration (at file start)')
cmt('// Verwendung im Gleichungsteil', '// Use in the equations section')
cmt('← Name der BIfunction', '← BIfunction name')

# Procedure keyword table
pair('<thead><tr><th>Prozedur-Schlüsselwort</th><th>Bedeutung</th></tr></thead>',
     '<thead><tr>'
     '<th data-lang="de">Prozedur-Schlüsselwort</th><th data-lang="en">Procedure keyword</th>'
     '<th data-lang="de">Bedeutung</th><th data-lang="en">Meaning</th>'
     '</tr></thead>')

td_pair('Beginnt Prozedurendeklaration', 'Starts a procedure declaration')
td_pair('Name der Built-in Funktion (aus BIfunctions)',
        'Name of the built-in function (from BIfunctions)')
td_pair('Anzahl und Typ der Eingaben', 'Number and type of inputs')
td_pair('Anzahl und Typ der Ausgaben (aktuell nur 1)',
        'Number and type of outputs (currently only 1)')
td_pair('Beendet Prozedurendeklaration', 'Ends the procedure declaration')

# ── Gleichungen ──
pair('<p>\n    Jede Gleichung hat die Form <code>LHS = RHS;</code> und wird vom Parser\n    in die Residuumsform <code>LHS − (RHS)</code> umgewandelt.\n    Das Semikolon am Ende ist obligatorisch.\n  </p>',
     '<p data-lang="de">\n    Jede Gleichung hat die Form <code>LHS = RHS;</code> und wird vom Parser\n    in die Residuumsform <code>LHS − (RHS)</code> umgewandelt.\n    Das Semikolon am Ende ist obligatorisch.\n  </p>'
     '<p data-lang="en">\n    Every equation has the form <code>LHS = RHS;</code> and is converted by the\n    parser into residual form <code>LHS − (RHS)</code>. The trailing semicolon\n    is mandatory.\n  </p>')

cmt('// Einfache Gleichung', '// Simple equation')
cmt('// Mit mathematischen Funktionen', '// With mathematical functions')
cmt('// Potenz', '// Power')
cmt('// CALL-Gleichung (Built-in Funktion)', '// CALL equation (built-in function)')

# math-block hi labels
def hi(de, en):
    pair(f'<span class="hi">{de}</span>',
         f'<span class="hi" data-lang="de">{de}</span>'
         f'<span class="hi" data-lang="en">{en}</span>')

hi('CAS-Gleichung:', 'CAS equation:')
hi('Residuumsform:', 'Residual form:')
hi('Solver-Ziel:', 'Solver goal:')

# ── Kontrollstrukturen ──
cmt('// ELSEIF — wird durch Pre-Processing expandiert',
    '// ELSEIF — expanded by preprocessing')

pair('<div class="note blue">\n    <strong>ELSEIF-Expansion (v2.3):</strong> ELSEIF wird durch Pre-Processing\n    in verschachtelte IF/ELSE-Blöcke expandiert. Mehrfaches ELSEIF ist möglich.\n  </div>',
     '<div class="note blue" data-lang="de">\n    <strong>ELSEIF-Expansion (v2.3):</strong> ELSEIF wird durch Pre-Processing\n    in verschachtelte IF/ELSE-Blöcke expandiert. Mehrfaches ELSEIF ist möglich.\n  </div>'
     '<div class="note blue" data-lang="en">\n    <strong>ELSEIF expansion (v2.3):</strong> ELSEIF is expanded into nested\n    IF/ELSE blocks via preprocessing. Multiple ELSEIFs are supported.\n  </div>')

# Structural IF paragraph
pair('<p>\n    Eine spezielle IF-Form wertet den Status (Fixed/Free) einer Variable\n    zur Parse-Zeit aus — nicht zur Laufzeit. Das erlaubt unterschiedliche\n    Gleichungsstrukturen je nach Modellkonfiguration:\n  </p>',
     '<p data-lang="de">\n    Eine spezielle IF-Form wertet den Status (Fixed/Free) einer Variable\n    zur Parse-Zeit aus — nicht zur Laufzeit. Das erlaubt unterschiedliche\n    Gleichungsstrukturen je nach Modellkonfiguration:\n  </p>'
     '<p data-lang="en">\n    A special IF form evaluates a variable\'s status (Fixed/Free) at parse\n    time — not at runtime. This allows different equation structures\n    depending on model configuration:\n  </p>')

cmt('// Diese Gleichung gilt wenn STATICSWITCH fixiert ist',
    '// This equation applies when STATICSWITCH is fixed')
cmt('// Diese Gleichung gilt wenn STATICSWITCH frei ist',
    '// This equation applies when STATICSWITCH is free')

# FOR comment
cmt('// Expandiert zu 5 Gleichungen: ARRAY_VAR[0]=..., ARRAY_VAR[1]=..., etc.',
    '// Expands to 5 equations: ARRAY_VAR[0]=..., ARRAY_VAR[1]=..., etc.')

# ── Operators section: kw-chip strings (these have op label inside the chip) ──
def chip(de, en):
    pair(f'<span class="kw-chip op">{de}</span>',
         f'<span class="kw-chip op" data-lang="de">{de}</span>'
         f'<span class="kw-chip op" data-lang="en">{en}</span>')

chip('+  Addition', '+  addition')
chip('-  Subtraktion', '-  subtraction')
chip('*  Multiplikation', '*  multiplication')
chip('/  Division', '/  division')
chip('^  Potenz', '^  power')
chip('( )  Klammerung', '( )  grouping')
# Logical (AND, OR, NOT) stay identical — no translation needed

# Comparison operators table
pair('<thead><tr><th>Operator</th><th>Fortran-Stil</th><th>Bedeutung</th></tr></thead>',
     '<thead><tr>'
     '<th>Operator</th>'
     '<th data-lang="de">Fortran-Stil</th><th data-lang="en">Fortran style</th>'
     '<th data-lang="de">Bedeutung</th><th data-lang="en">Meaning</th>'
     '</tr></thead>')

td_pair('Gleich', 'Equal')
td_pair('Ungleich', 'Not equal')
td_pair('Kleiner als', 'Less than')
td_pair('Kleiner gleich', 'Less than or equal')
td_pair('Größer als', 'Greater than')
td_pair('Größer gleich', 'Greater than or equal')

# ── Math functions section ──
pair('<p>\n    Diese Funktionen können direkt in Gleichungen verwendet werden.\n    Sie werden vom Parser in CASprzak-Syntax übersetzt und symbolisch differenziert.\n    Reihenfolge in der FUNC_MAP garantiert korrekte Übersetzung (längere Matches vor kürzeren).\n  </p>',
     '<p data-lang="de">\n    Diese Funktionen können direkt in Gleichungen verwendet werden.\n    Sie werden vom Parser in CASprzak-Syntax übersetzt und symbolisch differenziert.\n    Reihenfolge in der FUNC_MAP garantiert korrekte Übersetzung (längere Matches vor kürzeren).\n  </p>'
     '<p data-lang="en">\n    These functions can be used directly in equations. The parser translates\n    them into CASprzak syntax and differentiates them symbolically. The order\n    in FUNC_MAP guarantees correct translation (longer matches before shorter).\n  </p>')

pair('<thead><tr><th>CAS-Name</th><th>Alias</th><th>Mathematik</th><th>CASprzak</th></tr></thead>',
     '<thead><tr>'
     '<th>CAS-Name</th><th>Alias</th>'
     '<th data-lang="de">Mathematik</th><th data-lang="en">Math</th>'
     '<th>CASprzak</th>'
     '</tr></thead>')

pair('<div class="note amber">\n    <strong>Hinweis zu ABS, ROUND, TRUNCATE:</strong> Diese Funktionen sind nicht\n    überall differenzierbar — an Knicken und Sprüngen ist die symbolische Ableitung\n    undefiniert. Der Solver kann an solchen Stellen Probleme haben.\n    Falls möglich, glattere Alternativen verwenden.\n  </div>',
     '<div class="note amber" data-lang="de">\n    <strong>Hinweis zu ABS, ROUND, TRUNCATE:</strong> Diese Funktionen sind nicht\n    überall differenzierbar — an Knicken und Sprüngen ist die symbolische Ableitung\n    undefiniert. Der Solver kann an solchen Stellen Probleme haben.\n    Falls möglich, glattere Alternativen verwenden.\n  </div>'
     '<div class="note amber" data-lang="en">\n    <strong>Note on ABS, ROUND, TRUNCATE:</strong> these functions are not\n    differentiable everywhere — at kinks and jumps the symbolic derivative is\n    undefined. The solver can struggle at such points. Use smoother alternatives\n    where possible.\n  </div>')

# Special functions table
pair('<thead><tr><th>CAS-Syntax</th><th>Expansion</th><th>Hinweis</th></tr></thead>',
     '<thead><tr>'
     '<th>CAS-Syntax</th>'
     '<th data-lang="de">Expansion</th><th data-lang="en">Expansion</th>'
     '<th data-lang="de">Hinweis</th><th data-lang="en">Note</th>'
     '</tr></thead>')

td_pair('Quadrat — überall differenzierbar', 'Square — differentiable everywhere')
td_pair('Knick bei a=b — Newton kann dort langsamer werden',
        'Kink at a=b — Newton can slow down there')
td_pair('Knick bei a=b — Newton kann dort langsamer werden',
        'Kink at a=b — Newton can slow down there')

pair('<div class="note blue">\n    <strong>MIN/MAX Alternative bei Newton-Problemen:</strong>\n    Bei Konvergenzproblemen an der Knickstelle glattere Approximation verwenden:\n    <code>MIN(a,b) ≈ 0.5*(a+b-SQRT((a-b)^2+0.001))</code>\n  </div>',
     '<div class="note blue" data-lang="de">\n    <strong>MIN/MAX Alternative bei Newton-Problemen:</strong>\n    Bei Konvergenzproblemen an der Knickstelle glattere Approximation verwenden:\n    <code>MIN(a,b) ≈ 0.5*(a+b-SQRT((a-b)^2+0.001))</code>\n  </div>'
     '<div class="note blue" data-lang="en">\n    <strong>MIN/MAX alternative for Newton problems:</strong>\n    Use a smoother approximation when convergence struggles at the kink:\n    <code>MIN(a,b) ≈ 0.5*(a+b-SQRT((a-b)^2+0.001))</code>\n  </div>')

# ── Kommentare ──
cmt('// Zeilenkommentar — alles bis Zeilenende',
    '// Line comment — everything to end of line')
cmt('/* Blockkommentar\n   über mehrere Zeilen */',
    '/* Block comment\n   spanning multiple lines */')
cmt('// Kommentar am Zeilenende', '// Comment at end of line')

# ── Beispiel section ──
cmt('/* Isentrope Düsenströmung — vereinfachtes Segment\n   Unbekannte: PS, GAMMA, CP (3 Gleichungen, 3 Unbekannte) */',
    '/* Isentropic nozzle flow — simplified segment\n   Unknowns: PS, GAMMA, CP (3 equations, 3 unknowns) */')

cmt('// ── Prozedurendeklaration ─────────────────────────────',
    '// ── Procedure declaration ─────────────────────────────')
cmt('// ── Variablen ─────────────────────────────────────────',
    '// ── Variables ─────────────────────────────────────────')
cmt('// ── Gleichungen ───────────────────────────────────────',
    '// ── Equations ─────────────────────────────────────────')

cmt('// Gleichung 1: cp via Built-in Funktion',
    '// Equation 1: cp via built-in function')
cmt('// Gleichung 2: Isentropenexponent aus cp und Rgas',
    '// Equation 2: isentropic exponent from cp and Rgas')
cmt('// Gleichung 3: Statischer Druck (isentrop, Ma=0.8 angenommen)',
    '// Equation 3: static pressure (isentropic, Ma=0.8 assumed)')

# ── Footer ──
pair('<span>CMDSolver Docs · Parser Syntax · v2.5</span>',
     '<span data-lang="de">CMDSolver Docs · Parser Syntax · v2.5</span>'
     '<span data-lang="en">CMDSolver Docs · Parser Syntax · v2.5</span>')
pair('<a href="solver_options.html">← Solver Optionen</a>',
     '<a href="solver_options.html" data-lang="de">← Solver Optionen</a>'
     '<a href="solver_options.html" data-lang="en">← Solver Options</a>')
pair('<a href="bifunctions_reference.html">BIfunctions →</a>',
     '<a href="bifunctions_reference.html" data-lang="de">BIfunctions →</a>'
     '<a href="bifunctions_reference.html" data-lang="en">BIfunctions →</a>')

# Apply
missing = []
for i, (old, new) in enumerate(REPS):
    if old not in html: missing.append((i, old[:80])); continue
    html = html.replace(old, new, 1)

p.write_text(html, encoding='utf-8')
print(f'parser_syntax.html: {len(REPS) - len(missing)} / {len(REPS)} replacements')
if missing:
    print('NOT FOUND:')
    for i, s in missing[:10]: print(f'  #{i}: {s!r}')
