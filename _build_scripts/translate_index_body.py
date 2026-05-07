#!/usr/bin/env python3
"""
Translates the body content of index.html to bilingual DE/EN.
Strategy: for each translatable element, duplicate it with a sibling
element marked with data-lang="en" — the existing CSS rules then show
exactly one based on body.lang-* class.

Also fixes pre-existing source bugs in three cards (batch_mode,
parser_reviews, solver_reviews) where DE+EN were duplicated without
data-lang attributes — both versions were showing simultaneously.
"""
import re
from pathlib import Path

p = Path('/home/claude/build/index.html')
html = p.read_text(encoding='utf-8')

# ─── Replacement helper ─────────────────────────────────────────────
# `dup_block(de, en)` returns (de, en_with_data_lang_added) so that the
# original DE block stays in place (we add data-lang="de" to it) and a
# parallel EN block is appended right after.

REPS = []  # list of (old_string, new_string)

def card_num(de_text, en_text):
    REPS.append((
        f'<div class="card-num">{de_text}</div>',
        f'<div class="card-num" data-lang="de">{de_text}</div>'
        f'<div class="card-num" data-lang="en">{en_text}</div>',
    ))

def card_title(de_text, en_text):
    REPS.append((
        f'<div class="card-title">{de_text}</div>',
        f'<div class="card-title" data-lang="de">{de_text}</div>'
        f'<div class="card-title" data-lang="en">{en_text}</div>',
    ))

def card_desc(de_text, en_text):
    """card-desc is multi-line in source, so we match the trimmed inner text."""
    REPS.append((de_text, en_text))  # caller passes already-formed full strings

def card_type(de_text, en_text, css_class):
    """Single-occurrence card-type spans with same class need full-element dup."""
    REPS.append((
        f'<span class="card-type {css_class}">{de_text}</span>',
        f'<span class="card-type {css_class}" data-lang="de">{de_text}</span>'
        f'<span class="card-type {css_class}" data-lang="en">{en_text}</span>',
    ))


# ─── 1. Hero stats (above <main>) ──────────────────────────────────
for de, en in [('Solver','Solvers'), ('Gleichungen','Equations'),
               ('Version','Version'), ('Plattform','Platform')]:
    REPS.append((
        f'<span class="stat-lbl">{de}</span>',
        f'<span class="stat-lbl" data-lang="de">{de}</span>'
        f'<span class="stat-lbl" data-lang="en">{en}</span>',
    ))


# ─── 2. Section h2 headings ────────────────────────────────────────
H2 = [
    ('Einstieg', 'Getting Started'),
    ('Grundlagen', 'Foundations'),
    ('Solver — Detaildokumentation', 'Solvers — Detailed Documentation'),
    ('Referenz', 'Reference'),
    ('Engineering-Wissen', 'Engineering Knowledge'),
    ('Versionshistorie', 'Version History'),
]
for de, en in H2:
    REPS.append((
        f'<h2>{de}</h2>',
        f'<h2 data-lang="de">{de}</h2><h2 data-lang="en">{en}</h2>',
    ))


# ─── 3. Section: Einstieg / Getting Started ────────────────────────

# Card 1: getting_started
card_num('Kapitel 0 — Start hier', 'Chapter 0 — Start here')
# card-title "Getting Started" stays the same in both languages
card_desc(
    '<div class="card-desc">\n'
    '        Von Null zum ersten Ergebnis in 10 Minuten — CLI-Aufruf und SolverAPI-Einbettung.\n'
    '        Zwei Einstiegspfade, Fehlerbehandlung, GUI-Integration. Voraussetzungen und Classpath.\n'
    '      </div>',
    '<div class="card-desc" data-lang="de">\n'
    '        Von Null zum ersten Ergebnis in 10 Minuten — CLI-Aufruf und SolverAPI-Einbettung.\n'
    '        Zwei Einstiegspfade, Fehlerbehandlung, GUI-Integration. Voraussetzungen und Classpath.\n'
    '      </div>\n'
    '      <div class="card-desc" data-lang="en">\n'
    '        From zero to first result in 10 minutes — CLI invocation and SolverAPI embedding.\n'
    '        Two entry paths, error handling, GUI integration. Prerequisites and classpath.\n'
    '      </div>',
)
card_type('Start', 'Start', 'comp')

# Card 2: troubleshooting
card_num('Hilfe', 'Help')
card_title('Troubleshooting &amp; FAQ', 'Troubleshooting &amp; FAQ')  # same
card_desc(
    '<div class="card-desc">\n'
    '        Häufige Probleme mit Symptom, Diagnose und Lösung — NOT_CONVERGED,\n'
    '        κ-Warnungen, NaN, ParseErrors, Versionsmischung.\n'
    '        Schnellreferenz: Symptom → Lösung auf einen Blick.\n'
    '      </div>',
    '<div class="card-desc" data-lang="de">\n'
    '        Häufige Probleme mit Symptom, Diagnose und Lösung — NOT_CONVERGED,\n'
    '        κ-Warnungen, NaN, ParseErrors, Versionsmischung.\n'
    '        Schnellreferenz: Symptom → Lösung auf einen Blick.\n'
    '      </div>\n'
    '      <div class="card-desc" data-lang="en">\n'
    '        Common issues with symptom, diagnosis, and fix — NOT_CONVERGED,\n'
    '        κ warnings, NaN, parse errors, version mismatches.\n'
    '        Quick reference: symptom → fix at a glance.\n'
    '      </div>',
)
card_type('Hilfe', 'Help', 'comp')

# Card 3: examples
card_num('Beispiele', 'Examples')
card_title('Beispielmodelle', 'Example Models')
card_desc(
    '<div class="card-desc">\n'
    '        SimpleSystem (12 Gl.) und NozzleSystem (303 Gl.) mit vollständiger Erklärung.\n'
    '        Warum konvergiert welcher Solver? Starter-Template für eigene Modelle.\n'
    '      </div>',
    '<div class="card-desc" data-lang="de">\n'
    '        SimpleSystem (12 Gl.) und NozzleSystem (303 Gl.) mit vollständiger Erklärung.\n'
    '        Warum konvergiert welcher Solver? Starter-Template für eigene Modelle.\n'
    '      </div>\n'
    '      <div class="card-desc" data-lang="en">\n'
    '        SimpleSystem (12 eqs.) and NozzleSystem (303 eqs.) with full explanation.\n'
    '        Which solver converges, and why? Starter template for your own models.\n'
    '      </div>',
)
card_type('Praxis', 'Hands-on', 'comp')

# Card 4: api_reference
# card-num "API" stays
card_title('API-Referenz', 'API Reference')
card_desc(
    '<div class="card-desc">\n'
    '        Alle public Methoden von SolverAPI, SolverResult, SolverConfig.Builder,\n'
    '        ParseError und SolverType — für Einbettung in eigene Anwendungen.\n'
    '      </div>',
    '<div class="card-desc" data-lang="de">\n'
    '        Alle public Methoden von SolverAPI, SolverResult, SolverConfig.Builder,\n'
    '        ParseError und SolverType — für Einbettung in eigene Anwendungen.\n'
    '      </div>\n'
    '      <div class="card-desc" data-lang="en">\n'
    '        All public methods of SolverAPI, SolverResult, SolverConfig.Builder,\n'
    '        ParseError, and SolverType — for embedding into your own applications.\n'
    '      </div>',
)
card_type('Referenz', 'Reference', 'comp')


# ─── 4. Section: Grundlagen / Foundations ──────────────────────────

# Card 1: math_overview
card_num('Kapitel 1', 'Chapter 1')
card_title('Mathematischer Überblick', 'Mathematical Overview')
card_desc(
    '<div class="card-desc">\n'
    '        Nichtlineare Gleichungssysteme — implementierte und nicht implementierte\n'
    '        Lösungsverfahren. Klassifikation, Eigenschaften thermodynamischer Systeme,\n'
    '        Verfahrenswahl-Leitfaden.\n'
    '      </div>',
    '<div class="card-desc" data-lang="de">\n'
    '        Nichtlineare Gleichungssysteme — implementierte und nicht implementierte\n'
    '        Lösungsverfahren. Klassifikation, Eigenschaften thermodynamischer Systeme,\n'
    '        Verfahrenswahl-Leitfaden.\n'
    '      </div>\n'
    '      <div class="card-desc" data-lang="en">\n'
    '        Nonlinear equation systems — implemented and unimplemented\n'
    '        solution methods. Classification, properties of thermodynamic systems,\n'
    '        method-selection guide.\n'
    '      </div>',
)
card_type('Grundlagen', 'Foundations', 'math')

# Card 2: solver_comparison
card_num('Kapitel 2', 'Chapter 2')
card_title('Solver Vergleichsmatrix', 'Solver Comparison Matrix')
card_desc(
    '<div class="card-desc">\n'
    '        Alle 7 Solver im direkten Vergleich — Konvergenzrate, Rechenaufwand,\n'
    '        Robustheit, Empfehlungen. Testergebnisse SimpleSystem.cas. Entscheidungsbaum.\n'
    '      </div>',
    '<div class="card-desc" data-lang="de">\n'
    '        Alle 7 Solver im direkten Vergleich — Konvergenzrate, Rechenaufwand,\n'
    '        Robustheit, Empfehlungen. Testergebnisse SimpleSystem.cas. Entscheidungsbaum.\n'
    '      </div>\n'
    '      <div class="card-desc" data-lang="en">\n'
    '        All seven solvers in direct comparison — convergence rate, computational cost,\n'
    '        robustness, recommendations. Test results SimpleSystem.cas. Decision tree.\n'
    '      </div>',
)
card_type('Vergleich', 'Comparison', 'comp')


# ─── 5. Section: Solver — Detaildokumentation ──────────────────────

# Solver 1: NEWTON_ARMIJO
card_desc(
    '<div class="card-desc">\n'
    '        Standard-Solver. Dichte LU, Armijo-Backtracking.\n'
    '        Quadratische Konvergenz. Für kleine bis mittlere Systeme.\n'
    '      </div>',
    '<div class="card-desc" data-lang="de">\n'
    '        Standard-Solver. Dichte LU, Armijo-Backtracking.\n'
    '        Quadratische Konvergenz. Für kleine bis mittlere Systeme.\n'
    '      </div>\n'
    '      <div class="card-desc" data-lang="en">\n'
    '        Default solver. Dense LU, Armijo backtracking.\n'
    '        Quadratic convergence. For small to medium systems.\n'
    '      </div>',
)

# Solver 2: NEWTON_SPARSE
card_desc(
    '<div class="card-desc">\n'
    '        GSPAR Sparse-LU statt dichter LU. Bis 10× schneller bei großen Systemen.\n'
    '        Kein Backtracking — für gute Startvektoren.\n'
    '      </div>',
    '<div class="card-desc" data-lang="de">\n'
    '        GSPAR Sparse-LU statt dichter LU. Bis 10× schneller bei großen Systemen.\n'
    '        Kein Backtracking — für gute Startvektoren.\n'
    '      </div>\n'
    '      <div class="card-desc" data-lang="en">\n'
    '        GSPAR sparse LU instead of dense LU. Up to 10× faster on large systems.\n'
    '        No backtracking — needs good starting vectors.\n'
    '      </div>',
)

# Solver 3: NEWTON_SPARSE_ARMIJO (recommended)
card_num('Solver 3 · NEWTON_SPARSE_ARMIJO ★ Empfohlen',
         'Solver 3 · NEWTON_SPARSE_ARMIJO ★ Recommended')
card_desc(
    '<div class="card-desc">\n'
    '        Beste Kombination: GSPAR Sparse-LU + Armijo-Backtracking.\n'
    '        Schnell und robust. Empfohlener Standard-Solver für die meisten Systeme.\n'
    '      </div>',
    '<div class="card-desc" data-lang="de">\n'
    '        Beste Kombination: GSPAR Sparse-LU + Armijo-Backtracking.\n'
    '        Schnell und robust. Empfohlener Standard-Solver für die meisten Systeme.\n'
    '      </div>\n'
    '      <div class="card-desc" data-lang="en">\n'
    '        Best combination: GSPAR sparse LU + Armijo backtracking.\n'
    '        Fast and robust. Recommended default solver for most systems.\n'
    '      </div>',
)

# Solver 4: LM
card_desc(
    '<div class="card-desc">\n'
    '        Robustester Solver für schlecht konditionierte Systeme (κ &gt; 10¹²).\n'
    '        Adaptiver Dämpfungsparameter μ kombiniert Newton mit Gradientenabstieg.\n'
    '      </div>',
    '<div class="card-desc" data-lang="de">\n'
    '        Robustester Solver für schlecht konditionierte Systeme (κ &gt; 10¹²).\n'
    '        Adaptiver Dämpfungsparameter μ kombiniert Newton mit Gradientenabstieg.\n'
    '      </div>\n'
    '      <div class="card-desc" data-lang="en">\n'
    '        Most robust solver for ill-conditioned systems (κ &gt; 10¹²).\n'
    '        Adaptive damping parameter μ combines Newton with gradient descent.\n'
    '      </div>',
)
REPS.append((
    '<span class="perf-chip">36 Iter · κ bis 10²⁵</span>',
    '<span class="perf-chip" data-lang="de">36 Iter · κ bis 10²⁵</span>'
    '<span class="perf-chip" data-lang="en">36 iter · κ up to 10²⁵</span>',
))

# Solver 5: BROYDEN
card_desc(
    '<div class="card-desc">\n'
    '        Rang-1-Update der Jacobi statt vollständigem Neuaufbau.\n'
    '        Günstiger pro Iteration — vorteilhaft bei Parameterstudien.\n'
    '      </div>',
    '<div class="card-desc" data-lang="de">\n'
    '        Rang-1-Update der Jacobi statt vollständigem Neuaufbau.\n'
    '        Günstiger pro Iteration — vorteilhaft bei Parameterstudien.\n'
    '      </div>\n'
    '      <div class="card-desc" data-lang="en">\n'
    '        Rank-1 update of the Jacobian instead of full rebuild.\n'
    '        Cheaper per iteration — advantageous for parameter studies.\n'
    '      </div>',
)
REPS.append((
    '<span class="perf-chip">25 Iter · O(n²) Update</span>',
    '<span class="perf-chip" data-lang="de">25 Iter · O(n²) Update</span>'
    '<span class="perf-chip" data-lang="en">25 iter · O(n²) update</span>',
))

# Solver 6: BROYDEN_SPARSE
card_desc(
    '<div class="card-desc">\n'
    '        Broyden-Update mit GSPAR Sparse-LU. Schnellster Solver im Testbetrieb (~9ms).\n'
    '        Ideal für Parameterstudien mit großen Systemen.\n'
    '      </div>',
    '<div class="card-desc" data-lang="de">\n'
    '        Broyden-Update mit GSPAR Sparse-LU. Schnellster Solver im Testbetrieb (~9ms).\n'
    '        Ideal für Parameterstudien mit großen Systemen.\n'
    '      </div>\n'
    '      <div class="card-desc" data-lang="en">\n'
    '        Broyden update with GSPAR sparse LU. Fastest solver in test runs (~9ms).\n'
    '        Ideal for parameter studies on large systems.\n'
    '      </div>',
)

# Solver 7: HOMOTOPY
card_title('Homotopie Arc-Length', 'Homotopy Arc-Length')
card_desc(
    '<div class="card-desc">\n'
    '        Klassische Continuation: Pfadverfolgung von einfachem Startproblem zum Zielproblem\n'
    '        via Predictor-Korrektor mit fester t-Parametrisierung.\n'
    '      </div>',
    '<div class="card-desc" data-lang="de">\n'
    '        Klassische Continuation: Pfadverfolgung von einfachem Startproblem zum Zielproblem\n'
    '        via Predictor-Korrektor mit fester t-Parametrisierung.\n'
    '      </div>\n'
    '      <div class="card-desc" data-lang="en">\n'
    '        Classical continuation: path tracking from a simple starting problem to the\n'
    '        target problem via predictor-corrector with fixed t-parametrization.\n'
    '      </div>',
)
REPS.append((
    '<span class="perf-chip">Pfad t∈[0,1]</span>',
    '<span class="perf-chip" data-lang="de">Pfad t∈[0,1]</span>'
    '<span class="perf-chip" data-lang="en">Path t∈[0,1]</span>',
))

# Solver 8: ARC_LENGTH (experimental)
card_desc(
    '<div class="card-desc">\n'
    '        Bogen-Längen-Verfolgung im erweiterten Zustand y=(x,t) — konzeptionell für\n'
    '        Pfade mit Wendepunkten / Bifurkationen. Aktuell experimentell, auf NozzleSystem\n'
    '        nicht produktiv konvergent.\n'
    '      </div>',
    '<div class="card-desc" data-lang="de">\n'
    '        Bogen-Längen-Verfolgung im erweiterten Zustand y=(x,t) — konzeptionell für\n'
    '        Pfade mit Wendepunkten / Bifurkationen. Aktuell experimentell, auf NozzleSystem\n'
    '        nicht produktiv konvergent.\n'
    '      </div>\n'
    '      <div class="card-desc" data-lang="en">\n'
    '        Path tracking by arc length in extended state y=(x,t) — designed for\n'
    '        paths with turning points / bifurcations. Currently experimental, not\n'
    '        productively convergent on NozzleSystem.\n'
    '      </div>',
)
REPS.append((
    '<span class="perf-chip">Wendepunkte</span>',
    '<span class="perf-chip" data-lang="de">Wendepunkte</span>'
    '<span class="perf-chip" data-lang="en">Turning points</span>',
))

# Solver 9: ADAPTIVE_LAMBDA
card_desc(
    '<div class="card-desc">\n'
    '        Pragmatischer Wrapper: Phase 1 versucht Newton direkt (produktiv),\n'
    '        Phase 2 fällt auf λ-Continuation zurück (experimentell auf NozzleSystem).\n'
    '      </div>',
    '<div class="card-desc" data-lang="de">\n'
    '        Pragmatischer Wrapper: Phase 1 versucht Newton direkt (produktiv),\n'
    '        Phase 2 fällt auf λ-Continuation zurück (experimentell auf NozzleSystem).\n'
    '      </div>\n'
    '      <div class="card-desc" data-lang="en">\n'
    '        Pragmatic wrapper: Phase 1 tries Newton directly (production-ready),\n'
    '        Phase 2 falls back to λ-continuation (experimental on NozzleSystem).\n'
    '      </div>',
)


# ─── 6. Section: Referenz / Reference ──────────────────────────────

# Card 1: solver_options
card_num('Kapitel 3', 'Chapter 3')
card_title('Solver Optionen — CLI Referenz', 'Solver Options — CLI Reference')
card_desc(
    '<div class="card-desc">\n'
    '        Alle Kommandozeilenargumente: allgemeine Optionen für alle Solver,\n'
    '        solver-exklusive Parameter (-SH: Homotopie, -SB: Broyden),\n'
    '        Diagnose-Optionen und Batch-Modus.\n'
    '      </div>',
    '<div class="card-desc" data-lang="de">\n'
    '        Alle Kommandozeilenargumente: allgemeine Optionen für alle Solver,\n'
    '        solver-exklusive Parameter (-SH: Homotopie, -SB: Broyden),\n'
    '        Diagnose-Optionen und Batch-Modus.\n'
    '      </div>\n'
    '      <div class="card-desc" data-lang="en">\n'
    '        All command-line arguments: general options for all solvers,\n'
    '        solver-specific parameters (-SH: Homotopy, -SB: Broyden),\n'
    '        diagnostic options, and batch mode.\n'
    '      </div>',
)
card_type('Referenz', 'Reference', 'math')

# Card 2: batch_mode — fix pre-existing duplication and add data-lang
REPS.append((
    '    <a href="batch_mode.html" class="index-card">\n'
    '      <div class="card-num">Kapitel 4</div>\n'
    '      <div class="card-num">Chapter 4</div>\n'
    '      <div class="card-title">Batch-Modus &amp; Parameterstudien</div>\n'
    '      <div class="card-title">Batch Mode &amp; Parameter Studies</div>\n'
    '      <div class="card-desc">\n'
    '        Automatisiertes Lösen von N Betriebspunkten aus einer CSV-Datei.\n'
    '        Eingabe/Ausgabe-Format, Warm-Start, Sprung-Erkennung (-BC:JUMPTHRESH),\n'
    '        Bounds-Analyse und Laufzeit-Ausgabe.\n'
    '      </div>\n'
    '      <div class="card-desc">\n'
    '        Automated solving of N operating points from a CSV file.\n'
    '        Input/output format, warm-start, jump detection (-BC:JUMPTHRESH),\n'
    '        bounds analysis and timing output.\n'
    '      </div>\n'
    '      <div class="card-meta"><span class="card-type math">Referenz</span></div>\n'
    '    </a>',

    '    <a href="batch_mode.html" class="index-card">\n'
    '      <div class="card-num" data-lang="de">Kapitel 4</div>\n'
    '      <div class="card-num" data-lang="en">Chapter 4</div>\n'
    '      <div class="card-title" data-lang="de">Batch-Modus &amp; Parameterstudien</div>\n'
    '      <div class="card-title" data-lang="en">Batch Mode &amp; Parameter Studies</div>\n'
    '      <div class="card-desc" data-lang="de">\n'
    '        Automatisiertes Lösen von N Betriebspunkten aus einer CSV-Datei.\n'
    '        Eingabe/Ausgabe-Format, Warm-Start, Sprung-Erkennung (-BC:JUMPTHRESH),\n'
    '        Bounds-Analyse und Laufzeit-Ausgabe.\n'
    '      </div>\n'
    '      <div class="card-desc" data-lang="en">\n'
    '        Automated solving of N operating points from a CSV file.\n'
    '        Input/output format, warm-start, jump detection (-BC:JUMPTHRESH),\n'
    '        bounds analysis and timing output.\n'
    '      </div>\n'
    '      <div class="card-meta">'
    '<span class="card-type math" data-lang="de">Referenz</span>'
    '<span class="card-type math" data-lang="en">Reference</span>'
    '</div>\n'
    '    </a>',
))

# Card 3: parser_syntax
card_num('Kapitel 5', 'Chapter 5')  # Note: applies to first occurrence
# Will be: parser_syntax has Kapitel 5; bifunctions also has Kapitel 5 (source typo)
# str.replace replaces the first match each call — ok if we only do one card_num('Kapitel 5'), it replaces first.
# Add a second one for the bifunctions card so both get replaced.
card_title('CAS-Dateiformat — Parser Syntax', 'CAS File Format — Parser Syntax')
card_desc(
    '<div class="card-desc">\n'
    '        Vollständige Parser-Referenz: Sektionen, Variablendeklaration (Langform + AS REAL),\n'
    '        INITIALIZE-Block, PROCEDURE/CALL, Gleichungen, IF/ELSEIF/ENDIF/FOR,\n'
    '        Operatoren und mathematische Funktionen.\n'
    '      </div>',
    '<div class="card-desc" data-lang="de">\n'
    '        Vollständige Parser-Referenz: Sektionen, Variablendeklaration (Langform + AS REAL),\n'
    '        INITIALIZE-Block, PROCEDURE/CALL, Gleichungen, IF/ELSEIF/ENDIF/FOR,\n'
    '        Operatoren und mathematische Funktionen.\n'
    '      </div>\n'
    '      <div class="card-desc" data-lang="en">\n'
    '        Complete parser reference: sections, variable declaration (long form + AS REAL),\n'
    '        INITIALIZE block, PROCEDURE/CALL, equations, IF/ELSEIF/ENDIF/FOR,\n'
    '        operators, and mathematical functions.\n'
    '      </div>',
)

# Card 4: bifunctions_reference
# Card 4 also has "Kapitel 5" — but our card_num was scheduled to replace first occurrence only.
# After parser_syntax's "Kapitel 5" got replaced, the next still-untouched "Kapitel 5"
# is the bifunctions one. We add a second replacement explicitly.
REPS.append((
    '<div class="card-num">Kapitel 5</div>',
    '<div class="card-num" data-lang="de">Kapitel 5</div>'
    '<div class="card-num" data-lang="en">Chapter 5</div>',
))
card_title('BIfunctions — Thermodynamische Funktionen',
           'BIfunctions — Thermodynamic Functions')
card_desc(
    '<div class="card-desc">\n'
    '        Alle Built-in Funktionen mit physikalischem Hintergrund: JANAF-Polynome,\n'
    '        ISA-Atmosphärenmodell (9 Schichten), Schallgeschwindigkeit, Enthalpie, cp,\n'
    '        MofCondiRatio. Numerische Ableitungen via 5-Punkte-Formel O(h⁴).\n'
    '      </div>',
    '<div class="card-desc" data-lang="de">\n'
    '        Alle Built-in Funktionen mit physikalischem Hintergrund: JANAF-Polynome,\n'
    '        ISA-Atmosphärenmodell (9 Schichten), Schallgeschwindigkeit, Enthalpie, cp,\n'
    '        MofCondiRatio. Numerische Ableitungen via 5-Punkte-Formel O(h⁴).\n'
    '      </div>\n'
    '      <div class="card-desc" data-lang="en">\n'
    '        All built-in functions with physical background: JANAF polynomials,\n'
    '        ISA atmosphere model (9 layers), speed of sound, enthalpy, cp,\n'
    '        MofCondiRatio. Numerical derivatives via 5-point formula O(h⁴).\n'
    '      </div>',
)
# Both parser_syntax and bifunctions cards have card-type "Referenz" math.
# Our card_type() helper replaces only first occurrence. We need a second one.
# Actually card_type for solver_options also used 'math' Referenz — that already
# got replaced. So we need two MORE for parser_syntax and bifunctions.
# Easiest: just add raw replacements for the remaining two occurrences.
REPS.append((
    '<span class="card-type math">Referenz</span>',
    '<span class="card-type math" data-lang="de">Referenz</span>'
    '<span class="card-type math" data-lang="en">Reference</span>',
))
REPS.append((
    '<span class="card-type math">Referenz</span>',
    '<span class="card-type math" data-lang="de">Referenz</span>'
    '<span class="card-type math" data-lang="en">Reference</span>',
))


# ─── 7. Section: Engineering-Wissen / Engineering Knowledge ────────

# Card 1: lessons_learned
card_num('Kapitel 7', 'Chapter 7')
# card-title "Lessons Learned" stays
card_desc(
    '<div class="card-desc">\n'
    '        18 Engineering-Erkenntnisse aus allen Entwicklungsphasen — Architektur,\n'
    '        Algorithmen, Refactoring, Debugging, Werkzeuge. 8 klassische + 10 neue\n'
    '        Erkenntnisse seit v2.3. Das wichtigste Kapitel für langfristige Wartbarkeit.\n'
    '      </div>',
    '<div class="card-desc" data-lang="de">\n'
    '        18 Engineering-Erkenntnisse aus allen Entwicklungsphasen — Architektur,\n'
    '        Algorithmen, Refactoring, Debugging, Werkzeuge. 8 klassische + 10 neue\n'
    '        Erkenntnisse seit v2.3. Das wichtigste Kapitel für langfristige Wartbarkeit.\n'
    '      </div>\n'
    '      <div class="card-desc" data-lang="en">\n'
    '        18 engineering insights from all development phases — architecture,\n'
    '        algorithms, refactoring, debugging, tooling. 8 classical + 10 new\n'
    '        insights since v2.3. The most important chapter for long-term maintainability.\n'
    '      </div>',
)
card_type('Wissen', 'Knowledge', 'math')

# Card 2: dev_history
card_num('Kapitel 8', 'Chapter 8')
card_title('Entwicklungsgeschichte &amp; Bug Fix Log',
           'Development History &amp; Bug Fix Log')
card_desc(
    '<div class="card-desc">\n'
    '        9 Entwicklungsphasen von der monolithischen Ursprungsversion bis v2.5.\n'
    '        Vollständiger Bug Fix Log (27+ Bugs, BF-01–BF-12 + B27–B28 + Refactoring-Bugs\n'
    '        + GSPAR Fortran-Port). Offene Punkte mit Status.\n'
    '      </div>',
    '<div class="card-desc" data-lang="de">\n'
    '        9 Entwicklungsphasen von der monolithischen Ursprungsversion bis v2.5.\n'
    '        Vollständiger Bug Fix Log (27+ Bugs, BF-01–BF-12 + B27–B28 + Refactoring-Bugs\n'
    '        + GSPAR Fortran-Port). Offene Punkte mit Status.\n'
    '      </div>\n'
    '      <div class="card-desc" data-lang="en">\n'
    '        9 development phases from the monolithic original through v2.5.\n'
    '        Complete bug fix log (27+ bugs, BF-01–BF-12 + B27–B28 + refactoring bugs\n'
    '        + GSPAR Fortran port). Open items with status.\n'
    '      </div>',
)
card_type('Geschichte', 'History', 'math')

# Card 3: maintenance
card_num('Kapitel 6', 'Chapter 6')
card_title('Wartung &amp; Entwicklung', 'Maintenance &amp; Development')
card_desc(
    '<div class="card-desc">\n'
    '        Zwei Einstiegspunkte: Schnelleinstieg (Architektur, Rezepte, Checkliste)\n'
    '        und vollständige Einführung (Datenfluss, Klassen, Erweiterungspunkte,\n'
    '        Fallstricke, Build-Umgebung). Toggle-Button schaltet zwischen Modi.\n'
    '      </div>',
    '<div class="card-desc" data-lang="de">\n'
    '        Zwei Einstiegspunkte: Schnelleinstieg (Architektur, Rezepte, Checkliste)\n'
    '        und vollständige Einführung (Datenfluss, Klassen, Erweiterungspunkte,\n'
    '        Fallstricke, Build-Umgebung). Toggle-Button schaltet zwischen Modi.\n'
    '      </div>\n'
    '      <div class="card-desc" data-lang="en">\n'
    '        Two entry points: quick start (architecture, recipes, checklist)\n'
    '        and full introduction (data flow, classes, extension points,\n'
    '        pitfalls, build environment). Toggle button switches between modes.\n'
    '      </div>',
)
card_type('Wartung', 'Maintenance', 'math')

# Card 4: roadmap
card_num('Kapitel 9', 'Chapter 9')
card_title('Roadmap &amp; Offene Punkte', 'Roadmap &amp; Open Items')
card_desc(
    '<div class="card-desc">\n'
    '        18 priorisierte Entwicklungspunkte mit Zeithorizont, Aufwandsschätzung und\n'
    '        Wechselwirkungsanalyse. Solver-Erweiterungen (GMRES, Trust-Region, Anderson),\n'
    '        CAS-Erweiterungen (MIN/MAX, SQR, SECTION), Performance, Architektur, GUI-Vorbereitung.\n'
    '      </div>',
    '<div class="card-desc" data-lang="de">\n'
    '        18 priorisierte Entwicklungspunkte mit Zeithorizont, Aufwandsschätzung und\n'
    '        Wechselwirkungsanalyse. Solver-Erweiterungen (GMRES, Trust-Region, Anderson),\n'
    '        CAS-Erweiterungen (MIN/MAX, SQR, SECTION), Performance, Architektur, GUI-Vorbereitung.\n'
    '      </div>\n'
    '      <div class="card-desc" data-lang="en">\n'
    '        18 prioritized development items with time horizon, effort estimation, and\n'
    '        interaction analysis. Solver extensions (GMRES, Trust-Region, Anderson),\n'
    '        CAS extensions (MIN/MAX, SQR, SECTION), performance, architecture, GUI preparation.\n'
    '      </div>',
)
card_type('Planung', 'Planning', 'math')

# Card 5: infra_reviews — has nested <span class="new-badge">
REPS.append((
    '<div class="card-num"><span class="new-badge">NEU v2.12</span> Kapitel 10</div>',
    '<div class="card-num" data-lang="de"><span class="new-badge">NEU v2.12</span> Kapitel 10</div>'
    '<div class="card-num" data-lang="en"><span class="new-badge">NEW v2.12</span> Chapter 10</div>',
))
# card-title "Code Review" stays
card_desc(
    '<div class="card-desc">\n'
    '        Bewertung aller Parser-, Solver- und Infrastruktur-Komponenten von A\n'
    '        (exzellent) bis D (problematisch). 11 Komponenten begutachtet,\n'
    '        Empfehlungen für Refactoring und Stand der Code-Qualität nach v2.12.\n'
    '      </div>',
    '<div class="card-desc" data-lang="de">\n'
    '        Bewertung aller Parser-, Solver- und Infrastruktur-Komponenten von A\n'
    '        (exzellent) bis D (problematisch). 11 Komponenten begutachtet,\n'
    '        Empfehlungen für Refactoring und Stand der Code-Qualität nach v2.12.\n'
    '      </div>\n'
    '      <div class="card-desc" data-lang="en">\n'
    '        Assessment of all parser, solver, and infrastructure components from A\n'
    '        (excellent) to D (problematic). 11 components reviewed,\n'
    '        recommendations for refactoring, and code-quality status after v2.12.\n'
    '      </div>',
)

# Card 6: parser_reviews — fix pre-existing duplication
REPS.append((
    '    <a href="parser_reviews.html" class="index-card">\n'
    '      <div class="card-num">Code Review</div>\n'
    '      <div class="card-title">Parser Code Review</div>\n'
    '      <div class="card-desc">Bewertung der Parser-Komponenten: EqnSysReader (Note B), EqnData, BIfunctions.</div>\n'
    '      <div class="card-desc">Assessment of parser components: EqnSysReader (Grade B), EqnData, BIfunctions.</div>\n'
    '      <div class="card-meta"><span class="card-type comp">Review</span></div>\n'
    '    </a>',

    '    <a href="parser_reviews.html" class="index-card">\n'
    '      <div class="card-num">Code Review</div>\n'
    '      <div class="card-title">Parser Code Review</div>\n'
    '      <div class="card-desc" data-lang="de">Bewertung der Parser-Komponenten: EqnSysReader (Note B), EqnData, BIfunctions.</div>\n'
    '      <div class="card-desc" data-lang="en">Assessment of parser components: EqnSysReader (Grade B), EqnData, BIfunctions.</div>\n'
    '      <div class="card-meta"><span class="card-type comp">Review</span></div>\n'
    '    </a>',
))

# Card 7: solver_reviews — fix pre-existing duplication
REPS.append((
    '    <a href="solver_reviews.html" class="index-card">\n'
    '      <div class="card-num">Code Review</div>\n'
    '      <div class="card-title">Solver Code Review</div>\n'
    '      <div class="card-desc">Bewertung aller 7 Solver (Newton-Armijo Note A, LM v3b Note A, GSPAR-Familie Note A).</div>\n'
    '      <div class="card-desc">Assessment of all 7 solvers (Newton-Armijo Grade A, LM v3b Grade A, GSPAR family Grade A).</div>\n'
    '      <div class="card-meta"><span class="card-type comp">Review</span></div>\n'
    '    </a>',

    '    <a href="solver_reviews.html" class="index-card">\n'
    '      <div class="card-num">Code Review</div>\n'
    '      <div class="card-title">Solver Code Review</div>\n'
    '      <div class="card-desc" data-lang="de">Bewertung aller 7 Solver (Newton-Armijo Note A, LM v3b Note A, GSPAR-Familie Note A).</div>\n'
    '      <div class="card-desc" data-lang="en">Assessment of all 7 solvers (Newton-Armijo Grade A, LM v3b Grade A, GSPAR family Grade A).</div>\n'
    '      <div class="card-meta"><span class="card-type comp">Review</span></div>\n'
    '    </a>',
))


# ─── 8. Section: Versionshistorie / Version History ────────────────

# Table headers
REPS.append((
    '<thead><tr><th>Version</th><th>Inhalt</th><th>Status</th></tr></thead>',
    '<thead><tr>'
    '<th>Version</th>'
    '<th data-lang="de">Inhalt</th><th data-lang="en">Content</th>'
    '<th>Status</th>'
    '</tr></thead>',
))

# Version row contents (the <td> with the description)
def vers_row(de, en):
    REPS.append((
        f'<td>{de}</td>',
        f'<td data-lang="de">{de}</td><td data-lang="en">{en}</td>',
    ))

vers_row('Baseline — Newton-Armijo, LM, Broyden',
         'Baseline — Newton-Armijo, LM, Broyden')  # same
vers_row('GSPAR Sparse-LU, paralleler Jacobi-Aufbau',
         'GSPAR sparse LU, parallel Jacobian assembly')
vers_row('SolverAPI, Logging-Bereinigung, Javadoc, ELSEIF-Expansion, B27/B28 Bugfixes',
         'SolverAPI, logging cleanup, Javadoc, ELSEIF expansion, B27/B28 bugfixes')
vers_row('ParseError-Infrastruktur — strukturierte Fehlerbehandlung mit Zeilennummern',
         'ParseError infrastructure — structured error handling with line numbers')
vers_row('LinkedHashMap Refactoring (EqnData) + Output-Writer (SolverResult)',
         'LinkedHashMap refactoring (EqnData) + output writer (SolverResult)')

# Multi-line version cells: match by the unique keyword
REPS.append((
    '<td>FUNC_MAP-Bugfix, Javadoc-Komplettierung, SQR/MIN/MAX-Expansion, GUI-Vorbereitung,\n'
    '            Homotopie Tangenten-Prädiktor (R-03), relatives Abbruchkriterium (R-13)</td>',
    '<td data-lang="de">FUNC_MAP-Bugfix, Javadoc-Komplettierung, SQR/MIN/MAX-Expansion, GUI-Vorbereitung,\n'
    '            Homotopie Tangenten-Prädiktor (R-03), relatives Abbruchkriterium (R-13)</td>'
    '<td data-lang="en">FUNC_MAP bugfix, Javadoc completion, SQR/MIN/MAX expansion, GUI preparation,\n'
    '            Homotopy tangent predictor (R-03), relative termination criterion (R-13)</td>',
))
REPS.append((
    '<td>7-Solver-Stabilisierung — alle Solver-Typen auf NozzleSystem_4_fixed verifiziert.\n'
    '            JacobiEquilibrator-Klasse vorbereitet (noch nicht in Solve-Loop integriert)</td>',
    '<td data-lang="de">7-Solver-Stabilisierung — alle Solver-Typen auf NozzleSystem_4_fixed verifiziert.\n'
    '            JacobiEquilibrator-Klasse vorbereitet (noch nicht in Solve-Loop integriert)</td>'
    '<td data-lang="en">7-solver stabilization — all solver types verified on NozzleSystem_4_fixed.\n'
    '            JacobiEquilibrator class prepared (not yet integrated into solve loop)</td>',
))
REPS.append((
    '<td>R-01 umgesetzt: Jacobi-Equilibrierung (Sinkhorn-Knopp R·J·C) als\n'
    '            <code>-SC:EQUILIBRATE</code>. Inline-Armijo-Refactor in den vier\n'
    '            Newton-Armijo/Broyden-Solvern, dadurch DIAGONAL/UNIT_INTERVAL erstmals\n'
    '            funktionsfähig. NONE-Modus bit-exakt rückwärtskompatibel zu v2.11</td>',
    '<td data-lang="de">R-01 umgesetzt: Jacobi-Equilibrierung (Sinkhorn-Knopp R·J·C) als\n'
    '            <code>-SC:EQUILIBRATE</code>. Inline-Armijo-Refactor in den vier\n'
    '            Newton-Armijo/Broyden-Solvern, dadurch DIAGONAL/UNIT_INTERVAL erstmals\n'
    '            funktionsfähig. NONE-Modus bit-exakt rückwärtskompatibel zu v2.11</td>'
    '<td data-lang="en">R-01 implemented: Jacobian equilibration (Sinkhorn-Knopp R·J·C) as\n'
    '            <code>-SC:EQUILIBRATE</code>. Inline-Armijo refactor in the four\n'
    '            Newton-Armijo/Broyden solvers, making DIAGONAL/UNIT_INTERVAL functional\n'
    '            for the first time. NONE mode bit-exact backward-compatible with v2.11</td>',
))

# Status badges (appear 7 times for "Archiv")
REPS.append((
    '<span class="badge b-na">Archiv</span>',
    '<span class="badge b-na" data-lang="de">Archiv</span>'
    '<span class="badge b-na" data-lang="en">Archive</span>',
))
# Need 7 of them
for _ in range(6):
    REPS.append((
        '<span class="badge b-na">Archiv</span>',
        '<span class="badge b-na" data-lang="de">Archiv</span>'
        '<span class="badge b-na" data-lang="en">Archive</span>',
    ))
REPS.append((
    '<span class="badge b-ok">✅ Aktuell</span>',
    '<span class="badge b-ok" data-lang="de">✅ Aktuell</span>'
    '<span class="badge b-ok" data-lang="en">✅ Current</span>',
))


# ─── 9. Footer ─────────────────────────────────────────────────────

REPS.append((
    '<span>CMDSolver Dokumentation · v2.12 · Mai 2026</span>',
    '<span data-lang="de">CMDSolver Dokumentation · v2.12 · Mai 2026</span>'
    '<span data-lang="en">CMDSolver Documentation · v2.12 · May 2026</span>',
))
REPS.append((
    '<span>Alle Solver getestet auf NozzleSystem_4_fixed.cas · Java 21</span>',
    '<span data-lang="de">Alle Solver getestet auf NozzleSystem_4_fixed.cas · Java 21</span>'
    '<span data-lang="en">All solvers tested on NozzleSystem_4_fixed.cas · Java 21</span>',
))


# ─── Apply all replacements ────────────────────────────────────────

missing = []
for i, (old, new) in enumerate(REPS):
    if old not in html:
        missing.append((i, old[:80]))
        continue
    html = html.replace(old, new, 1)

p.write_text(html, encoding='utf-8')

print(f'Applied {len(REPS) - len(missing)} / {len(REPS)} replacements')
if missing:
    print(f'\n{len(missing)} not found:')
    for i, snippet in missing[:20]:
        print(f'  #{i}: {snippet}…')
