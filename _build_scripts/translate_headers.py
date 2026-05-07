#!/usr/bin/env python3
"""
Translates the header area (hero-sub, h1, tagline) of every doc page into EN
and wraps both DE and EN with data-lang attributes so the language switcher
displays the correct one.

Operates on the migrated files in /home/claude/build, modifying them in place.
"""
import re
from pathlib import Path

BUILD = Path('/home/claude/build')

# ─── Translation map ─────────────────────────────────────────────────
# Each entry has up to four keys: hero_sub, h1, tagline, breadcrumb
# Each is a (de, en) tuple. The DE side must match the source EXACTLY
# (whitespace tolerance is handled by regex), the EN side is the new translation.

T = {
  'api_reference.html': {
    'hero_sub': ('API Referenz', 'API Reference'),
    'h1':      ('Programmatische API<br>Vollständige Referenz',
                'Programmatic API<br>Complete Reference'),
    'tagline': ('Alle public Methoden von SolverAPI, SolverResult, SolverConfig.Builder, ParseError und SolverType — für die Einbettung von CMDSolver in eigene Anwendungen.',
                'All public methods of SolverAPI, SolverResult, SolverConfig.Builder, ParseError and SolverType — for embedding CMDSolver into your own applications.'),
  },
  'batch_mode.html': {
    'hero_sub': ('BatchRunner', 'BatchRunner'),
    'h1':      ('Batch-Modus &amp;<br>Parameterstudien',
                'Batch Mode &amp;<br>Parameter Studies'),
    'tagline': ('Automatisiertes Lösen von N Betriebspunkten aus einer CSV-Datei — mit Warm-Start, Konvergenzprotokoll und strukturierter Ausgabe.',
                'Automated solving of N operating points from a CSV file — with warm-start, convergence log, and structured output.'),
  },
  'bifunctions_reference.html': {
    'hero_sub': ('BIfunction Referenz', 'BIfunction Reference'),
    'h1':      ('BIfunctions<br>Thermodynamische Built-in Funktionen',
                'BIfunctions<br>Thermodynamic Built-in Functions'),
    'tagline': ('Überblick über die thermodynamischen Berechnungsfunktionen in CMDSolver — physikalischer Hintergrund, Gleichungen, Ableitungsmethodik und CAS-Verwendung.',
                'Overview of CMDSolver\'s thermodynamic computation functions — physical background, equations, derivation methodology, and CAS usage.'),
  },
  'dev_history.html': {
    'hero_sub': ('Entwicklungsgeschichte', 'Development History'),
    'h1':      ('Entwicklungsgeschichte<br>&amp; Bug Fix Log',
                'Development History<br>&amp; Bug Fix Log'),
    'tagline': ('Alle Entwicklungsphasen von der monolithischen Ursprungsversion bis v2.5 — und der vollständige Bug Fix Log mit allen behobenen und offenen Problemen.',
                'All development phases from the monolithic original version through v2.5 — and the complete bug fix log with all resolved and open issues.'),
  },
  'examples.html': {
    'hero_sub': ('Beispiele', 'Examples'),
    'h1':      ('Beispiele &amp; Tutorials', 'Examples &amp; Tutorials'),
    'tagline': ('Zwei Referenzmodelle mit vollständiger Erklärung — von einem einfachen algebraischen System bis zum komplexen aerothermodynamischen Düsenmodell. Welche Gleichungen sind interessant, warum konvergiert welcher Solver?',
                'Two reference models with full explanation — from a simple algebraic system to a complex aerothermodynamic nozzle model. Which equations are interesting, and why does each solver converge?'),
  },
  'getting_started.html': {
    'hero_sub': ('Schnellstart', 'Quick Start'),
    'h1':      ('Getting Started', 'Getting Started'),
    'tagline': ('Von Null zum ersten Ergebnis in 10 Minuten — CLI-Aufruf, SolverAPI-Einbettung und Ergebnis auslesen. Zwei Einstiegspfade je nach Anwendungsfall.',
                'From zero to first result in 10 minutes — CLI invocation, SolverAPI embedding, and reading the result. Two entry paths depending on use case.'),
  },
  'index.html': {
    'hero_sub':   ('Dokumentation', 'Documentation'),
    'h1':         ('CMDSolver', 'CMDSolver'),
    'tagline':    ('Modularer Newton-Solver für nichtlineare algebraische Gleichungssysteme. 7 Solver-Algorithmen, Jacobi-Equilibrierung, Batch-Parameterstudien, Pre-Solve Diagnose und systematisches Modell-Debugging.',
                   'Modular Newton solver for nonlinear algebraic equation systems. Seven solver algorithms, Jacobian equilibration, batch parameter studies, pre-solve diagnostics, and systematic model debugging.'),
    'breadcrumb_text': ('CMDSolver Dokumentation', 'CMDSolver Documentation'),
  },
  'infra_reviews.html': {
    'hero_sub': ('Code Review', 'Code Review'),
    'h1':      ('Solver-Infrastruktur<br>Code Review',
                'Solver Infrastructure<br>Code Review'),
    'tagline': ('Detail-Bewertungen der Solver-Basisklasse, Skalierung, Bounds-Projection und Konfigurations-Klassen. Diese Komponenten werden von allen Solvern geteilt.',
                'Detailed evaluations of the solver base class, scaling, bounds projection, and configuration classes. These components are shared by all solvers.'),
  },
  'lessons_learned.html': {
    'hero_sub': ('Lektionen', 'Lessons'),
    'h1':      ('Lessons Learned', 'Lessons Learned'),
    'tagline': ('Engineering-Erkenntnisse aus der Entwicklung von CMDSolver — gesammelt über alle Versionen von der monolithischen Ursprungsversion bis v2.5. Kategorisiert nach Architektur, Algorithmen, Refactoring, Debugging und Werkzeuge.',
                'Engineering insights from developing CMDSolver — gathered across all versions from the monolithic original through v2.5. Categorized by architecture, algorithms, refactoring, debugging, and tooling.'),
  },
  'maintenance.html': {
    'hero_sub': ('Wartung', 'Maintenance'),
    'h1':      ('Wartung &amp; Erweiterung', 'Maintenance &amp; Extension'),
    'tagline': ('Code verstehen, Fehler beheben, erweitern — für Entwickler mit und ohne Vorkenntnis des CMDSolver-Codes.',
                'Understanding the code, fixing bugs, extending it — for developers with or without prior knowledge of the CMDSolver code base.'),
  },
  'math_overview.html': {
    'hero_sub': ('Mathematik', 'Mathematics'),
    'h1':      ('Mathematische Grundlagen<br>Nichtlineare Gleichungssysteme',
                'Mathematical Foundations<br>Nonlinear Equation Systems'),
    'tagline': ('Überblick über numerische Lösungsverfahren für Systeme der Form F(x) = 0 — implementierte und nicht implementierte Methoden im Kontext thermodynamischer Modelle.',
                'Overview of numerical solution methods for systems of the form F(x) = 0 — implemented and unimplemented methods in the context of thermodynamic models.'),
    'breadcrumb_text': ('Mathematischer Überblick', 'Mathematical Overview'),
  },
  'parser_reviews.html': {
    'hero_sub': ('Code Review', 'Code Review'),
    'h1':      ('Parser-Komponenten<br>Code Review',
                'Parser Components<br>Code Review'),
    'tagline': ('Detail-Bewertungen aller Parser- und CAS-Datenstruktur-Komponenten. Diese sind über mehrere Versionen hinweg gereift und bilden das stabile Fundament des Solvers.',
                'Detailed evaluations of all parser and CAS data-structure components. These have matured across several versions and form the stable foundation of the solver.'),
  },
  'parser_syntax.html': {
    'hero_sub': ('Parser Syntax', 'Parser Syntax'),
    'h1':      ('CAS-Dateiformat<br>Parser Syntax Referenz',
                'CAS File Format<br>Parser Syntax Reference'),
    'tagline': ('Vollständige Referenz des CAS-Dateiformats — Sektionen, Variablendeklaration, Gleichungen, Kontrollstrukturen, Operatoren und mathematische Funktionen.',
                'Complete reference for the CAS file format — sections, variable declaration, equations, control structures, operators, and mathematical functions.'),
  },
  'roadmap.html': {
    'hero_sub': ('Roadmap', 'Roadmap'),
    'h1':      ('Roadmap &amp;<br>Offene Punkte', 'Roadmap &amp;<br>Open Items'),
    'tagline': ('Priorisierte Entwicklungsplanung für CMDSolver — Stand v2.10 — Solver-Erweiterungen, CAS-Dateierweiterungen, Performance, GUI-Vorbereitung und alternative Algorithmen. Mit Zeithorizont, Aufwandsschätzung und Wechselwirkungsanalyse.',
                'Prioritized development planning for CMDSolver — as of v2.10 — solver extensions, CAS file format extensions, performance, GUI preparation, and alternative algorithms. With time horizon, effort estimation, and interaction analysis.'),
  },
  'solver_adaptive_lambda.html': {
    'hero_sub': ('Experimentell', 'Experimental'),
    'h1':      ('Adaptive Lambda Continuation<br>Newton-driven Wrapper',
                'Adaptive Lambda Continuation<br>Newton-driven Wrapper'),
    'tagline': ('Pragmatischer Continuation-Wrapper über Newton-Armijo (oder andere innere Solver). Versucht zuerst direkten Lösungsweg, fällt bei Bedarf auf λ-Continuation zurück. <strong>Phase 1 (try-direct) funktioniert produktiv</strong>, Phase 2 (Continuation) ist auf NozzleSystem nicht zuverlässig — siehe <a href="#status">Status</a>.',
                'Pragmatic continuation wrapper around Newton-Armijo (or other inner solvers). First attempts a direct solve, falls back to λ-continuation when needed. <strong>Phase 1 (try-direct) works in production</strong>, Phase 2 (continuation) is not reliable on NozzleSystem — see <a href="#status">Status</a>.'),
  },
  'solver_arc_length.html': {
    'hero_sub': ('Experimentell', 'Experimental'),
    'h1':      ('Arc-Length Continuation<br>Bogen-Längen-Verfolgung',
                'Arc-Length Continuation<br>Path Tracking by Arc Length'),
    'tagline': ('Erweiterter Continuation-Solver mit zusätzlicher Pfad-Parametrisierung — konzeptionell für Pfade mit Wendepunkten oder Bifurkationen (z.B. echte Schallübergänge bei Ma=1). Nutzt erweiterten Zustand y=(x,t) und sphärische Bogen-Norm. <strong>Aktuell experimentell</strong> — auf NozzleSystem nicht produktiv konvergent (siehe <a href="#status">Status</a>).',
                'Extended continuation solver with additional path parametrization — designed for paths with turning points or bifurcations (e.g., genuine sonic transitions at Ma=1). Uses extended state y=(x,t) and spherical arc norm. <strong>Currently experimental</strong> — does not converge productively on NozzleSystem (see <a href="#status">Status</a>).'),
  },
  'solver_broyden.html': {
    'hero_sub': ('Solver 5 von 7', 'Solver 5 of 7'),
    'h1':      ('Broyden<br>Quasi-Newton', 'Broyden<br>Quasi-Newton'),
    'tagline': ('Quasi-Newton-Verfahren mit Rang-1-Update der Jacobi-Approximation. Günstiger pro Iteration als vollständiger Jacobi-Neuaufbau — besonders vorteilhaft bei Parameterstudien.',
                'Quasi-Newton method with rank-1 update of the Jacobian approximation. Cheaper per iteration than full Jacobian rebuild — especially advantageous for parameter studies.'),
  },
  'solver_broyden_sparse.html': {
    'hero_sub': ('Solver 6 von 7', 'Solver 6 of 7'),
    'h1':      ('Broyden<br>Quasi-Newton GSPAR', 'Broyden<br>Quasi-Newton GSPAR'),
    'tagline': ('Broyden-Update mit GSPAR Sparse-LU. Schnellster Solver im Testbetrieb — kombiniert günstige Jacobi-Updates mit effizienter Sparse-Linearalgebra.',
                'Broyden update with GSPAR sparse LU. Fastest solver in test runs — combines cheap Jacobian updates with efficient sparse linear algebra.'),
  },
  'solver_comparison.html': {
    'hero_sub': ('Vergleich', 'Comparison'),
    'h1':      ('Solver Vergleich', 'Solver Comparison'),
    'tagline': ('Alle 7 implementierten Solver im direkten Vergleich — Konvergenzverhalten, Rechenaufwand, Robustheit und Einsatzempfehlungen auf einen Blick.',
                'All seven implemented solvers in direct comparison — convergence behavior, computational cost, robustness, and usage recommendations at a glance.'),
    'breadcrumb_text': ('Solver Vergleich', 'Solver Comparison'),
  },
  'solver_homotopy.html': {
    'hero_sub': ('Solver 7 von 7', 'Solver 7 of 7'),
    'h1':      ('Homotopie<br>Arc-Length Continuation',
                'Homotopy<br>Arc-Length Continuation'),
    'tagline': ('Klassische Continuation: verfolgt einen glatten Lösungspfad von einem einfachen Startproblem zum Zielproblem mit fester t-Parametrisierung. Predictor-Korrektor-Schema mit innerem Newton-/LM-Solver. Verwandte Solver: <a href="solver_arc_length.html">ARC_LENGTH</a> (Bogen-Längen, experimental) und <a href="solver_adaptive_lambda.html">ADAPTIVE_LAMBDA</a> (Wrapper, Phase 1 produktiv).',
                'Classical continuation: follows a smooth solution path from a simple starting problem to the target problem with fixed t-parametrization. Predictor-corrector scheme with an inner Newton or LM solver. Related solvers: <a href="solver_arc_length.html">ARC_LENGTH</a> (arc-length, experimental) and <a href="solver_adaptive_lambda.html">ADAPTIVE_LAMBDA</a> (wrapper, Phase 1 in production).'),
  },
  'solver_lm.html': {
    'hero_sub': ('Solver 4 von 7', 'Solver 4 of 7'),
    'h1':      ('Levenberg-Marquardt', 'Levenberg-Marquardt'),
    'tagline': ('Robuster Solver für mäßig bis stark schlecht konditionierte Systeme. <strong>v2.12 Newton-Direkt-Hybrid</strong>: bei kleinem μ direkte <code>J⁻¹</code>-Inversion statt Normalengleichung — vermeidet kappa²-Verlust und konvergiert auf NozzleSystem (kappa=4.6×10¹¹) in 5 Iter mit <code>-SC:EQUILIBRATE</code>.',
                'Robust solver for moderately to severely ill-conditioned systems. <strong>v2.12 Newton-direct hybrid</strong>: at small μ, direct <code>J⁻¹</code> inversion instead of the normal equation — avoids kappa² loss and converges on NozzleSystem (kappa=4.6×10¹¹) in 5 iterations with <code>-SC:EQUILIBRATE</code>.'),
  },
  'solver_newton_armijo.html': {
    # Note: this file has no hero-sub — only h1 and tagline
    'h1':      ('Newton-Raphson<br>+ Armijo Liniensuche',
                'Newton-Raphson<br>+ Armijo Line Search'),
    'tagline': ('Der Standard-Solver von CMDSolver. Quadratische Konvergenz in der Nähe der Lösung, robuste Schrittweitenanpassung durch Armijo-Backtracking.',
                'CMDSolver\'s default solver. Quadratic convergence near the solution, robust step-size control via Armijo backtracking.'),
  },
  'solver_newton_sparse.html': {
    'hero_sub': ('Solver 2 von 7', 'Solver 2 of 7'),
    'h1':      ('Newton-GSPAR<br>Sparse LU', 'Newton-GSPAR<br>Sparse LU'),
    'tagline': ('Newton-Raphson mit GSPAR Sparse-LU — bis zu 10× schneller als dichte LU bei großen, dünn besetzten Jacobi-Matrizen. Kein Backtracking.',
                'Newton-Raphson with GSPAR sparse LU — up to 10× faster than dense LU for large, sparsely populated Jacobian matrices. No backtracking.'),
  },
  'solver_newton_sparse_armijo.html': {
    'hero_sub': ('Solver 3 von 7', 'Solver 3 of 7'),
    'h1':      ('Newton-GSPAR<br>Sparse LU + Armijo',
                'Newton-GSPAR<br>Sparse LU + Armijo'),
    'tagline': ('Die beste Kombination: GSPAR Sparse-LU für Geschwindigkeit, Armijo-Backtracking für Robustheit. Empfohlener Standard-Solver für große Systeme. ★ Empfehlung',
                'The best combination: GSPAR sparse LU for speed, Armijo backtracking for robustness. Recommended default solver for large systems. ★ Recommended'),
  },
  'solver_options.html': {
    'hero_sub': ('CLI Referenz', 'CLI Reference'),
    'h1':      ('Solver Optionen<br>CLI Referenz',
                'Solver Options<br>CLI Reference'),
    'tagline': ('Alle Kommandozeilenargumente für CASSolver — allgemeine Optionen, solver-spezifische Parameter, Diagnose, Batch-Modus und Sprung-Erkennung.',
                'All command-line arguments for CASSolver — general options, solver-specific parameters, diagnostics, batch mode, and jump detection.'),
  },
  'solver_reviews.html': {
    'hero_sub': ('Code Review', 'Code Review'),
    'h1':      ('Solver-Komponenten<br>Code Review',
                'Solver Components<br>Code Review'),
    'tagline': ('Detail-Bewertungen aller produktiven und experimentellen Solver-Implementierungen.',
                'Detailed evaluations of all production and experimental solver implementations.'),
  },
  'troubleshooting.html': {
    'hero_sub': ('Hilfe', 'Help'),
    'h1':      ('Probleme lösen', 'Troubleshooting'),
    'tagline': ('Häufige Probleme mit Symptom, Diagnose und konkreter Lösung — von Konvergenzfehlern über Parse-Probleme bis zu Performance-Fragen.',
                'Common issues with symptom, diagnosis, and concrete fix — from convergence failures and parse errors to performance questions.'),
  },
}


# ─── Replacement engine ─────────────────────────────────────────────

def make_bilingual(html: str, t: dict, filename: str) -> str:
    # 1. hero-sub: <div class="hero-sub">XYZ</div>
    if 'hero_sub' in t:
        de, en = t['hero_sub']
        old = f'<div class="hero-sub">{de}</div>'
        new = (f'<div class="hero-sub">'
               f'<span data-lang="de">{de}</span>'
               f'<span data-lang="en">{en}</span></div>')
        if old in html:
            html = html.replace(old, new, 1)
        else:
            print(f'  ! hero-sub not matched in {filename}')

    # 2. h1: matches <h1>...</h1> OR <h1 id="...">...</h1>
    if 'h1' in t:
        de, en = t['h1']
        # Capture optional attributes on h1
        pat = re.compile(r'<h1(\s[^>]*)?>' + re.escape(de) + r'</h1>')
        m = pat.search(html)
        if m:
            attrs = m.group(1) or ''
            # Build two h1 elements with combined attributes + data-lang
            replacement = (f'<h1{attrs} data-lang="de">{de}</h1>'
                           f'<h1{attrs} data-lang="en">{en}</h1>')
            html = html[:m.start()] + replacement + html[m.end():]
        else:
            print(f'  ! h1 not matched in {filename}')

    # 3. tagline: <p class="tagline">...</p>
    if 'tagline' in t:
        de, en = t['tagline']
        # Use regex with DOTALL to span newlines, and normalize whitespace
        # in the source for matching
        pat = re.compile(
            r'<p class="tagline">\s*' + re.escape(de).replace(r'\ ', r'\s+') + r'\s*</p>',
            re.DOTALL,
        )
        m = pat.search(html)
        if m:
            replacement = (f'<p class="tagline" data-lang="de">{de}</p>\n  '
                           f'<p class="tagline" data-lang="en">{en}</p>')
            html = html[:m.start()] + replacement + html[m.end():]
        else:
            # Try without whitespace flexibility (exact match)
            old = f'<p class="tagline">{de}</p>'
            if old in html:
                replacement = (f'<p class="tagline" data-lang="de">{de}</p>\n  '
                               f'<p class="tagline" data-lang="en">{en}</p>')
                html = html.replace(old, replacement, 1)
            else:
                print(f'  ! tagline not matched in {filename}')

    # 4. breadcrumb special-case: span with just a translatable text
    if 'breadcrumb_text' in t:
        de, en = t['breadcrumb_text']
        old = f'<span>{de}</span>'
        new = (f'<span data-lang="de">{de}</span>'
               f'<span data-lang="en">{en}</span>')
        if old in html:
            html = html.replace(old, new, 1)
        else:
            print(f'  ! breadcrumb-text not matched in {filename}')

    return html


# ─── Run ────────────────────────────────────────────────────────────

count = 0
for fname, t in T.items():
    p = BUILD / fname
    if not p.exists():
        print(f'  SKIP {fname} (file not found)')
        continue
    src = p.read_text(encoding='utf-8')
    out = make_bilingual(src, t, fname)
    if out != src:
        p.write_text(out, encoding='utf-8')
        print(f'  ✓ {fname}')
        count += 1
    else:
        print(f'  · {fname} (no changes)')

print(f'\nTranslated headers in {count} / {len(T)} files.')
