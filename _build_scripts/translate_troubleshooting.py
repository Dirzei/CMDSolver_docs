#!/usr/bin/env python3
"""Translates body content of troubleshooting.html to bilingual DE/EN."""
from pathlib import Path

p = Path('/home/claude/build/troubleshooting.html')
html = p.read_text(encoding='utf-8')

REPS = []
def add(de, en, wrapper='div'):
    """Wrap a block element with data-lang. de/en are the FULL element strings."""
    REPS.append((de, en))
def pair(old, new):
    REPS.append((old, new))

# ── Nav ──
NAV = [
    ('Konvergenz', 'Convergence'),
    ('Parser-Fehler', 'Parser errors'),
    ('Konditionszahl', 'Condition number'),
    ('NaN / Divergenz', 'NaN / divergence'),
    ('Performance', 'Performance'),
    ('FAQ', 'FAQ'),
    ('Schnellreferenz', 'Quick reference'),
]
for de, en in NAV:
    pair(f'>{de}</a>',
         f' data-lang="de">{de}</a><a data-lang="en"_TBD>{en}</a>')
# Actually safer: target the whole <a> by the unique href
pair('<a href="#konvergenz">Konvergenz</a>',
     '<a href="#konvergenz" data-lang="de">Konvergenz</a><a href="#konvergenz" data-lang="en">Convergence</a>')
pair('<a href="#parser">Parser-Fehler</a>',
     '<a href="#parser" data-lang="de">Parser-Fehler</a><a href="#parser" data-lang="en">Parser errors</a>')
pair('<a href="#kappa">Konditionszahl</a>',
     '<a href="#kappa" data-lang="de">Konditionszahl</a><a href="#kappa" data-lang="en">Condition number</a>')
pair('<a href="#nan">NaN / Divergenz</a>',
     '<a href="#nan" data-lang="de">NaN / Divergenz</a><a href="#nan" data-lang="en">NaN / divergence</a>')
pair('<a href="#performance">Performance</a>',
     '<a href="#performance" data-lang="de">Performance</a><a href="#performance" data-lang="en">Performance</a>')
pair('<a href="#faq">FAQ</a>',
     '<a href="#faq" data-lang="de">FAQ</a><a href="#faq" data-lang="en">FAQ</a>')
pair('<a href="#quickref">Schnellreferenz</a>',
     '<a href="#quickref" data-lang="de">Schnellreferenz</a><a href="#quickref" data-lang="en">Quick reference</a>')

# Remove the placeholder lines we accidentally added above
REPS[:] = REPS[7:]  # drop the bad first 7

# ── h2 section headings ──
def h2(de, en):
    pair(f'<h2>{de}</h2>',
         f'<h2 data-lang="de">{de}</h2><h2 data-lang="en">{en}</h2>')

h2('Konvergenzprobleme', 'Convergence Problems')
h2('Parser-Fehler', 'Parser Errors')
h2('Konditionszahl-Warnungen', 'Condition Number Warnings')
h2('NaN und Divergenz', 'NaN and Divergence')
h2('Performance-Probleme', 'Performance Problems')
h2('Häufige Fragen (FAQ)', 'Frequently Asked Questions (FAQ)')
h2('Schnellreferenz — Symptom → Lösung', 'Quick Reference — Symptom → Fix')

# ── Symptom titles (each unique) ──
def sym(de, en):
    pair(f'<span class="symptom-title">{de}</span>',
         f'<span class="symptom-title" data-lang="de">{de}</span>'
         f'<span class="symptom-title" data-lang="en">{en}</span>')

sym('Solver meldet NOT_CONVERGED — keine Fehlermeldung',
    'Solver reports NOT_CONVERGED — no error message')
sym('Solver iteriert bis maxIter ohne Verbesserung (fsum stagniert)',
    'Solver iterates to maxIter without improvement (fsum stagnates)')
sym('ParseError: "Variable not found" oder stille Fehler',
    'ParseError: "Variable not found" or silent failures')
sym('INITIALIZE-Block Override wird ignoriert',
    'INITIALIZE block override is ignored')
sym('Kompilierfehler: hunderte Fehler nach Datei-Update',
    'Compilation errors: hundreds of errors after file update')
sym('Log: "kappa=4.62e+11 [POOR] — ill-conditioned Jacobian"',
    'Log: "kappa=4.62e+11 [POOR] — ill-conditioned Jacobian"')
sym('Log: "NaN detected — treating as divergence"',
    'Log: "NaN detected — treating as divergence"')
sym('Homotopie meldet fsum = NaN',
    'Homotopy reports fsum = NaN')
sym('Solver ist sehr langsam bei großem System (n &gt; 200)',
    'Solver is very slow on large systems (n &gt; 200)')

# ── diag-content blocks ──
# These are the meat of the troubleshooting steps. Each is a div containing
# <strong>title:</strong> body + sometimes a <pre>.
# I'll use the unique <strong>...</strong> as anchor.
def diag(strong_de, strong_en, body_de, body_en, pre=None):
    """Replace a diag-content block. We match by the strong tag + text."""
    # Build the full original block content as flexible regex isn't feasible — use text replacement.
    # Original pattern:
    #   <strong>strong_de</strong>\n          body_de\n          [optional pre]
    # We'll just match by strong + immediately following body, ignoring formatting nuances.
    # Actually, easiest: replace the <strong>...</strong> + body separately.
    pair(f'<strong>{strong_de}</strong>', f'<strong data-lang="de">{strong_de}</strong>'
                                          f'<strong data-lang="en">{strong_en}</strong>')

# ── Approach: translate each <strong>...</strong> heading inside diag steps,
#    plus the long body texts as separate replacements. ──

# Strong headings
S = [
    ('Schlechter Startvektor?', 'Bad starting vector?'),
    ('Startvektor inspizieren:', 'Inspect the starting vector:'),
    ('Andere Solver versuchen:', 'Try other solvers:'),
    ('Levenberg-Marquardt als robustere Alternative:', 'Levenberg-Marquardt as a more robust alternative:'),
    ('Homotopie als letztes Mittel:', 'Homotopy as a last resort:'),
    ('fsum-Verlauf im Log prüfen:', 'Inspect fsum trajectory in the log:'),
    ('Residuen-Normierung aktivieren:', 'Enable residual normalization:'),
    ('Gleichgewicht prüfen:', 'Check balance:'),
    ('ParseErrors im SolverResult prüfen:', 'Inspect ParseErrors on SolverResult:'),
    ('Variablenname-Tippfehler:', 'Variable-name typo:'),
    ('Variable deklariert aber nicht in Gleichung:', 'Variable declared but not used in equations:'),
    ('Syntax für Mehrfach-Punktnamen:', 'Syntax for multi-dot names:'),
    ('initStructSwitches vor INITIALIZE:', 'initStructSwitches before INITIALIZE:'),
    ('Versionsmischung:', 'Version mixing:'),
    ('Doppelte Klassendeklaration:', 'Duplicate class declaration:'),
    ('Ursachen für hohes κ:', 'Causes of high κ:'),
    ('Sofortmaßnahme: Levenberg-Marquardt:', 'Quick fix: Levenberg-Marquardt:'),
    ('Mittelfristig: Gleichungen normieren:', 'Medium-term: normalize equations:'),
    ('Physikalisch unmöglicher Zwischenwert:', 'Physically impossible intermediate value:'),
    ('Bounds strenger setzen:', 'Set tighter bounds:'),
    ('Armijo-Liniensuche hilft:', 'Armijo line search helps:'),
    ('Sparse-LU verwenden:', 'Use sparse LU:'),
    ('Broyden-Sparse für Parameterstudien:', 'Broyden-Sparse for parameter studies:'),
    ('BatchRunner für Parameterstudien:', 'BatchRunner for parameter studies:'),
    ('Lösung:', 'Fix:'),
]
for de, en in S:
    pair(f'<strong>{de}</strong>',
         f'<strong data-lang="de">{de}</strong><strong data-lang="en">{en}</strong>')

# Now translate the body texts that follow. They are inside <div class="diag-content">.
# Easier: replace each entire diag-content block by matching unique substring of body.

# Helper to match a body text and split it into DE/EN spans wrapped on the closing </div>.
# Each diag-content has:
#   <div class="diag-content">
#     <strong>X</strong>
#     body text...
#     [optional <pre>...</pre>]
#   </div>
# Strategy: wrap entire body text after the </strong> in <span data-lang="de">…</span><span data-lang="en">…</span>
# before any <pre> or before </div>.

# I'll use distinctive substring fragments to find each body and replace.

BODIES = [
  # Strong DE → body DE → body EN
  ('Diagnose-Modus aktivieren: <code>-DI</code> lässt <code>InitialValueAnalyzer</code>\n          die Startwerte optimieren. Oft reicht das.',
   'Enable diagnostic mode: <code>-DI</code> lets <code>InitialValueAnalyzer</code>\n          optimize the starting values. Often that\'s enough.'),
  ('<code>-DV:start.txt</code> schreibt den tatsächlichen Startvektor vor Iteration 0.\n          Physikalisch plausibel? Temperatur &gt; 0K? Druck &gt; 0Pa?',
   '<code>-DV:start.txt</code> writes the actual starting vector before iteration 0.\n          Physically plausible? Temperature &gt; 0K? Pressure &gt; 0Pa?'),
  ('<code>-TEST</code> zeigt alle 7 Solver. Konvergiert einer davon → Startwert-Problem.\n          Konvergiert keiner → Modell-Problem.',
   '<code>-TEST</code> runs all 7 solvers. If one converges → starting-value issue.\n          If none converges → model issue.'),
  ('Bei κ-Warnungen im Log immer LM versuchen.',
   'Always try LM when κ warnings appear in the log.'),
  ('Sinkt fsum gar nicht? → Schlechter Startvektor oder falsches Vorzeichen in Gleichung.\n          Sinkt fsum anfangs, stagniert dann? → Möglicherweise zwei Lösungen oder nahezu singuläre Jacobi.',
   'Does fsum not drop at all? → Bad starting vector or wrong sign in an equation.\n          Drops initially, then stagnates? → Possibly two solutions or nearly singular Jacobian.'),
  ('Bei gemischten Einheiten (Pa + kg/s) kann eine Gleichung dominieren.\n          <code>-SN</code> normiert auf Startwert-Residuen.',
   'With mixed units (Pa + kg/s) one equation can dominate.\n          <code>-SN</code> normalizes to starting-value residuals.'),
  ('n freie Variablen = n Gleichungen? Log zeigt beim Start:\n          <code>Starting ... [n=X, maxIter=100, ...]</code> — X muss der Anzahl freier Variablen entsprechen.',
   'n free variables = n equations? At startup the log shows:\n          <code>Starting ... [n=X, maxIter=100, ...]</code> — X must match the number of free variables.'),
  ('Jeder ParseError enthält Zeilennummer und Kontext.',
   'Every ParseError contains a line number and context.'),
  ('CMDSolver ist case-insensitiv — aber Punkt-Notation muss exakt stimmen.\n          <code>PARTM.F060.PS</code> ≠ <code>PARTM.F060.Ps</code> (Letzteres würde nach toUpperCase zu ersterem).',
   'CMDSolver is case-insensitive — but the dot notation must match exactly.\n          <code>PARTM.F060.PS</code> ≠ <code>PARTM.F060.Ps</code> (the latter would become the former after toUpperCase).'),
  ('Freie Variable ohne Gleichung → System ist unterbestimmt.\n          Jede freie Variable braucht genau eine Gleichung die sie "bestimmt".',
   'Free variable without an equation → the system is underdetermined.\n          Every free variable needs exactly one equation that "determines" it.'),
  ('Für <code>PARTM.F060.PS.Upper = ...</code> muss der vollständige Name\n          vor dem letzten Punkt stehen. Der Parser verwendet <code>lastIndexOf(\'.\')</code>.',
   'For <code>PARTM.F060.PS.Upper = ...</code> the full name must appear\n          before the last dot. The parser uses <code>lastIndexOf(\'.\')</code>.'),
  ('Strukturelle IF-Bedingungen (VAR.SPEC==FIXED) müssen vor dem INITIALIZE-Block\n          ausgewertet werden. Das macht <code>EqnSystem</code> automatisch — wenn der\n          Aufruf fehlt (z.B. bei direktem EqnData-Aufruf) funktioniert INITIALIZE nicht.',
   'Structural IF conditions (VAR.SPEC==FIXED) must be evaluated before the INITIALIZE\n          block. <code>EqnSystem</code> does this automatically — if the call is missing\n          (e.g., on direct EqnData usage) INITIALIZE will not work.'),
  ('Wahrscheinlichste Ursache. Dateien aus v2.3 und v2.4+\n          dürfen nicht gemischt werden. v2.4\'s <code>EqnSysReader</code> ruft\n          <code>ParseError</code>-Methoden auf die in v2.3\'s <code>SystemData</code> fehlen.',
   'Most likely cause. Files from v2.3 and v2.4+\n          must not be mixed. v2.4\'s <code>EqnSysReader</code> calls\n          <code>ParseError</code> methods that are missing from v2.3\'s <code>SystemData</code>.'),
  ('Alle Dateien aus demselben ZIP kopieren.', 'Copy all files from the same ZIP.'),
  ('Wenn 2: Javadoc steht nach statt vor <code>public class</code>.',
   'If 2: Javadoc is placed after instead of before <code>public class</code>.'),
  ('Gemischte Einheiten (Pa ~ 10⁵, kg/s ~ 1, dimensionslos ~ 10⁻³) erzeugen\n          riesige Spanne in der Jacobi. Verschiedene Größenordnungen werden direkt\n          im Jacobi-Eintrag sichtbar.',
   'Mixed units (Pa ~ 10⁵, kg/s ~ 1, dimensionless ~ 10⁻³) produce a huge span\n          in the Jacobian. Different orders of magnitude become visible directly\n          in the Jacobian entries.'),
  ('LM ist robust bis κ ~ 10²⁵. Einfach Solver wechseln:',
   'LM is robust up to κ ~ 10²⁵. Simply switch solvers:'),
  ('Gleichungen in Pa durch 1e5 teilen, kg/s-Gleichungen durch 1 lassen.\n          Das reduziert die Spanne in der Jacobi und verbessert κ um 2–4 Größenordnungen.',
   'Divide Pa equations by 1e5, leave kg/s equations as-is.\n          This reduces the span in the Jacobian and improves κ by 2–4 orders of magnitude.'),
  ('Eine Gleichung hat einen Wert außerhalb des physikalischen Bereichs erzeugt —\n          z.B. negative Temperatur in SQRT(T), Division durch Null.\n          PhysicalProjector fängt viele Fälle, aber nicht alle.',
   'An equation produced a value outside the physical range —\n          e.g., negative temperature in SQRT(T), division by zero.\n          PhysicalProjector catches many cases, but not all.'),
  ('Lower-Bounds für T (≥ 1K), p (≥ 1Pa), Flächen (≥ 1e-6 m²) verhindern\n          physikalisch unmögliche Zwischenwerte. PhysicalProjector projiziert nur\n          auf User-Bounds wenn diese enger sind als die physikalischen Defaults.',
   'Lower bounds for T (≥ 1K), p (≥ 1Pa), areas (≥ 1e-6 m²) prevent\n          physically impossible intermediate values. PhysicalProjector only projects\n          onto user bounds when they are tighter than the physical defaults.'),
  ('<code>NEWTON_SPARSE_ARMIJO</code> halbiert den Schritt wenn der Versuchspunkt\n          NaN erzeugt. Ohne Armijo (<code>NEWTON_SPARSE</code>) kann NaN sofort auftreten.',
   '<code>NEWTON_SPARSE_ARMIJO</code> halves the step when the trial point\n          produces NaN. Without Armijo (<code>NEWTON_SPARSE</code>), NaN can occur immediately.'),
  ('<code>NEWTON_ARMIJO</code> verwendet dichte LU (O(n³)).\n          <code>NEWTON_SPARSE_ARMIJO</code> verwendet GSPAR Sparse-LU (O(nnz)) — bis 10× schneller.',
   '<code>NEWTON_ARMIJO</code> uses dense LU (O(n³)).\n          <code>NEWTON_SPARSE_ARMIJO</code> uses GSPAR sparse LU (O(nnz)) — up to 10× faster.'),
  ('Wenn viele ähnliche Betriebspunkte gelöst werden: <code>BROYDEN_SPARSE</code>\n          spart Jacobi-Neuaufbauten. ~9ms vs ~30ms für SimpleSystem.',
   'When many similar operating points are solved: <code>BROYDEN_SPARSE</code>\n          saves Jacobian rebuilds. ~9ms vs ~30ms for SimpleSystem.'),
  ('CSV-Datei mit allen Betriebspunkten → <code>-I:studie.csv</code>.\n          Läuft alle Punkte sequenziell mit Warm-Start-Option.',
   'CSV file with all operating points → <code>-I:studie.csv</code>.\n          Runs all points sequentially with the warm-start option.'),
]

for de_body, en_body in BODIES:
    pair(de_body, f'<span data-lang="de">{de_body}</span><span data-lang="en">{en_body}</span>')

# ── Konditionszahl section: paragraph at section top ──
pair('<p>Konditionszahl κ misst wie empfindlich das System auf kleine Änderungen reagiert.\n      κ &gt; 10⁸ ist problematisch, κ &gt; 10¹² gefährlich für Newton.</p>',
     '<p data-lang="de">Konditionszahl κ misst wie empfindlich das System auf kleine Änderungen reagiert.\n      κ &gt; 10⁸ ist problematisch, κ &gt; 10¹² gefährlich für Newton.</p>'
     '<p data-lang="en">The condition number κ measures how sensitive the system is to small changes.\n      κ &gt; 10⁸ is problematic, κ &gt; 10¹² dangerous for Newton.</p>')

# Homotopy NaN paragraph
pair('<p>Das ist <strong>normal</strong>. Der Homotopie-Solver gibt kein fsum über\n      den Standard-Kanal aus — er hat eine eigene interne Konvergenzprüfung über\n      den Pfadfortschritt t → 1. Nur der <code>isConverged()</code>-Status ist maßgeblich.</p>',
     '<p data-lang="de">Das ist <strong>normal</strong>. Der Homotopie-Solver gibt kein fsum über\n      den Standard-Kanal aus — er hat eine eigene interne Konvergenzprüfung über\n      den Pfadfortschritt t → 1. Nur der <code>isConverged()</code>-Status ist maßgeblich.</p>'
     '<p data-lang="en">This is <strong>normal</strong>. The homotopy solver does not emit fsum on the\n      standard channel — it has its own internal convergence check based on path\n      progress t → 1. Only the <code>isConverged()</code> status matters.</p>')

# ── FAQ ──
FAQ = [
  ('Wie viele Gleichungen kann CMDSolver lösen?',
   'How many equations can CMDSolver handle?',
   'Theoretisch unbegrenzt. Praktisch getestet bis ~600 Gleichungen (623-Gleichungen Benchmark).\n    Mit GSPAR Sparse-LU sind 1000–2000 Gleichungen realistisch. Bei n &gt; 2000 wird\n    GMRES als linearer Solver benötigt (Roadmap R-02).',
   'Theoretically unlimited. Practically tested up to ~600 equations (623-equation benchmark).\n    With GSPAR sparse LU, 1000–2000 equations are realistic. For n &gt; 2000, GMRES\n    is needed as a linear solver (Roadmap R-02).'),
  ('Warum ist die Jacobi dicht obwohl das System sparse aussieht?',
   'Why is the Jacobian dense even though the system looks sparse?',
   'In thermodynamischen Modellen hängen viele Variablen über physikalische Zusammenhänge\n    zusammen — Gaszusammensetzung beeinflusst cp beeinflusst κ beeinflusst Schallgeschwindigkeit\n    beeinflusst Machzahl usw. Das erzeugt trotzdem eine relativ dünn besetzte Jacobi\n    (5–15% Besetzung) — GSPAR Sparse-LU ist dennoch deutlich schneller als dichte LU.',
   'In thermodynamic models, many variables are coupled via physical relationships —\n    gas composition affects cp affects κ affects speed of sound affects Mach number, etc.\n    This still produces a relatively sparse Jacobian (5–15% fill) — GSPAR sparse LU is\n    nevertheless much faster than dense LU.'),
  ('Kann ich CMDSolver in einem Multi-Thread-Kontext verwenden?',
   'Can I use CMDSolver in a multi-threaded context?',
   'Ja — eine <code>SolverAPI</code>-Instanz pro Thread. Instanzen sind nicht thread-sicher\n    untereinander, aber mehrere unabhängige Instanzen können parallel laufen.\n    Der interne Jacobi-Aufbau ist aktuell nicht parallelisiert\n    (<code>PARALLEL_JACOBI_THRESHOLD = 99999</code>).',
   'Yes — one <code>SolverAPI</code> instance per thread. Instances are not thread-safe\n    with each other, but multiple independent instances can run in parallel.\n    Internal Jacobian assembly is currently not parallelized\n    (<code>PARALLEL_JACOBI_THRESHOLD = 99999</code>).'),
  ('Warum hat die CAS-Datei Semikolon am Ende jeder Gleichung?',
   'Why does the CAS file have a semicolon at the end of every equation?',
   'Das Semikolon ist das Gleichungsende-Zeichen — der Parser behandelt es als Abschluss\n    der Residuumsform <code>LHS − (RHS) = 0</code>. Ohne Semikolon kann der Parser\n    nicht unterscheiden ob die Zeile weitergeht. In der AS-REAL-Kurzform ist das Semikolon\n    ebenfalls obligatorisch.',
   'The semicolon is the equation terminator — the parser treats it as the end of the\n    residual form <code>LHS − (RHS) = 0</code>. Without it, the parser cannot tell\n    whether the line continues. In the AS-REAL short form the semicolon is mandatory too.'),
  ('Was bedeutet "Fixed" vs "Free" für eine Variable?',
   'What does "Fixed" vs "Free" mean for a variable?',
   '<strong>Fixed:</strong> Die Variable ist eine bekannte Randbedingung — ihr Wert ist\n    vorgegeben und wird vom Solver nicht verändert. <strong>Free:</strong> Die Variable\n    ist eine Unbekannte die der Solver bestimmt. Anzahl Free-Variablen muss gleich\n    Anzahl der Gleichungen sein.',
   '<strong>Fixed:</strong> the variable is a known boundary condition — its value is\n    given and not changed by the solver. <strong>Free:</strong> the variable is an\n    unknown that the solver determines. The number of free variables must equal the\n    number of equations.'),
  ('Kann ich die Lösung eines Betriebspunkts als Startvektor für den nächsten verwenden?',
   'Can I use the solution of one operating point as the starting vector for the next?',
   'Mit der <code>-DV:</code> Option wird der aktuelle Startvektor in eine Datei geschrieben\n    die dann mit <code>-U:</code> als Startvektor für den nächsten Lauf verwendet werden kann.\n    SolverState Warm-Start (Roadmap R-14) wird das automatisieren.',
   'With the <code>-DV:</code> option the current starting vector is written to a file\n    which can then be passed via <code>-U:</code> as the starting vector for the next run.\n    SolverState warm-start (Roadmap R-14) will automate this.'),
  ('Warum funktionieren ABS(), ROUND() und TRUNCATE() manchmal schlecht mit Newton?',
   'Why do ABS(), ROUND(), and TRUNCATE() sometimes work badly with Newton?',
   'Diese Funktionen sind an Knicken und Sprüngen nicht differenzierbar. Newton braucht\n    glatte Ableitungen. An den Unstetigkeitsstellen (ABS bei 0, ROUND bei .5) ist die\n    symbolische Ableitung undefiniert und die numerische Ableitung ungenau. Als Alternative:\n    glatte Approximationen verwenden, z.B. <code>ABS(x) ≈ SQRT(x^2 + ε)</code> mit\n    kleinem ε &gt; 0.',
   'These functions are not differentiable at kinks and jumps. Newton needs smooth\n    derivatives. At the discontinuities (ABS at 0, ROUND at .5) the symbolic derivative\n    is undefined and the numerical one is inaccurate. As an alternative, use smooth\n    approximations, e.g., <code>ABS(x) ≈ SQRT(x^2 + ε)</code> with small ε &gt; 0.'),
  ('Wie debugge ich eine Gleichung die immer NaN liefert?',
   'How do I debug an equation that always returns NaN?',
   'Startvektor mit <code>-DV:start.txt</code> speichern, Werte manuell in einer\n    Tabellenkalkulation nachrechnen. Welche Variable hat einen unmöglichen Wert?\n    Dann Bounds für diese Variable strenger setzen und <code>-DI</code> aktivieren.',
   'Save the starting vector with <code>-DV:start.txt</code>, then recompute values\n    manually in a spreadsheet. Which variable has an impossible value? Tighten that\n    variable\'s bounds and enable <code>-DI</code>.'),
]

for q_de, q_en, a_de, a_en in FAQ:
    pair(f'<div class="faq-q">{q_de}</div>',
         f'<div class="faq-q" data-lang="de">{q_de}</div>'
         f'<div class="faq-q" data-lang="en">{q_en}</div>')
    pair(a_de, f'<span data-lang="de">{a_de}</span><span data-lang="en">{a_en}</span>')

# ── Schnellreferenz title and rows ──
pair('<div class="quick-ref-title">Häufige Symptome</div>',
     '<div class="quick-ref-title" data-lang="de">Häufige Symptome</div>'
     '<div class="quick-ref-title" data-lang="en">Common Symptoms</div>')

# qr-sym entries: only those that contain German
QR_SYM = [
    ('κ &gt; 10¹² Warnung', 'κ &gt; 10¹² warning'),
    ('fsum stagniert', 'fsum stagnates'),
    ('ParseError Zeilennummer', 'ParseError line number'),
    ('INITIALIZE-Block ignoriert', 'INITIALIZE block ignored'),
    ('150+ Kompilierfehler', '150+ compile errors'),
    ('Solver zu langsam', 'Solver too slow'),
    ('Doppelte Klasse EqnData', 'Duplicate class EqnData'),
    ('System.out in Framework', 'System.out in framework'),
]
for de, en in QR_SYM:
    pair(f'<span class="qr-sym">{de}</span>',
         f'<span class="qr-sym" data-lang="de">{de}</span>'
         f'<span class="qr-sym" data-lang="en">{en}</span>')

# qr-sol entries with German text
QR_SOL = [
    ('→ <code>-DI</code> → <code>-S:LEVENBERG_MARQUARDT</code> → <code>-S:HOMOTOPY -SH:CRITICAL</code>',
     '→ <code>-DI</code> → <code>-S:LEVENBERG_MARQUARDT</code> → <code>-S:HOMOTOPY -SH:CRITICAL</code>'),
    ('→ <code>-S:LEVENBERG_MARQUARDT</code> — immer',
     '→ <code>-S:LEVENBERG_MARQUARDT</code> — always'),
    ('→ Bounds prüfen, <code>NEWTON_SPARSE_ARMIJO</code> (hat Backtracking)',
     '→ Check bounds, <code>NEWTON_SPARSE_ARMIJO</code> (has backtracking)'),
    ('→ <code>-SN</code> (Residuen-Normierung), Gleichungsformulierung prüfen',
     '→ <code>-SN</code> (residual normalization), check equation formulation'),
    ('→ <code>result.getParseErrors().forEach(e -&gt; print(e.format()))</code>',
     '→ <code>result.getParseErrors().forEach(e -&gt; print(e.format()))</code>'),
    ('→ Syntax: <code>VAR.Lower = x;</code> und <code>VAR.Upper = x;</code> mit Semikolon',
     '→ Syntax: <code>VAR.Lower = x;</code> and <code>VAR.Upper = x;</code> with semicolon'),
    ('→ Versionsmischung — alle Dateien aus einem ZIP kopieren',
     '→ Version mixing — copy all files from one ZIP'),
    ('→ Nach EqnData-Refactoring verloren — aus v2.5 ZIP wiederherstellen',
     '→ Lost after EqnData refactoring — restore from v2.5 ZIP'),
    ('→ <code>-S:NEWTON_SPARSE_ARMIJO</code> oder <code>-S:BROYDEN_SPARSE</code>',
     '→ <code>-S:NEWTON_SPARSE_ARMIJO</code> or <code>-S:BROYDEN_SPARSE</code>'),
    ('→ Normal — nur <code>isConverged()</code> ist maßgeblich',
     '→ Normal — only <code>isConverged()</code> is authoritative'),
    ('→ Javadoc muss VOR <code>public class</code> stehen',
     '→ Javadoc must be BEFORE <code>public class</code>'),
    ('→ SolverLogger Handler registrieren (R-16) — System.out ist bereinigt ab v2.3',
     '→ Register a SolverLogger handler (R-16) — System.out is clean since v2.3'),
]
for de, en in QR_SOL:
    pair(f'<span class="qr-sol">{de}</span>',
         f'<span class="qr-sol" data-lang="de">{de}</span>'
         f'<span class="qr-sol" data-lang="en">{en}</span>')

# Replace the actual hard-coded "qr-sym" line for `&gt;`-encoded one — in the source the entry uses `&gt;` already.
# For "ParseError Zeilennummer" the entry has plain text. Already covered above.

# Also handle simple non-translated qr-sym/qr-sol pairs that have no German:
pair('<span class="qr-sym">NOT_CONVERGED</span>',
     '<span class="qr-sym" data-lang="de">NOT_CONVERGED</span>'
     '<span class="qr-sym" data-lang="en">NOT_CONVERGED</span>')
pair('<span class="qr-sym">NaN detected</span>',
     '<span class="qr-sym" data-lang="de">NaN detected</span>'
     '<span class="qr-sym" data-lang="en">NaN detected</span>')
pair('<span class="qr-sym">isCallEqn() undefined</span>',
     '<span class="qr-sym" data-lang="de">isCallEqn() undefined</span>'
     '<span class="qr-sym" data-lang="en">isCallEqn() undefined</span>')
pair('<span class="qr-sym">Homotopie fsum=NaN</span>',
     '<span class="qr-sym" data-lang="de">Homotopie fsum=NaN</span>'
     '<span class="qr-sym" data-lang="en">Homotopy fsum=NaN</span>')

# ── Footer ──
pair('<span>CMDSolver Docs · Troubleshooting &amp; FAQ · v2.5</span>',
     '<span data-lang="de">CMDSolver Docs · Troubleshooting &amp; FAQ · v2.5</span>'
     '<span data-lang="en">CMDSolver Docs · Troubleshooting &amp; FAQ · v2.5</span>')
pair('<a href="examples.html">← Beispiele</a>',
     '<a href="examples.html" data-lang="de">← Beispiele</a>'
     '<a href="examples.html" data-lang="en">← Examples</a>')
pair('<a href="index.html">← Übersicht</a>',
     '<a href="index.html" data-lang="de">← Übersicht</a>'
     '<a href="index.html" data-lang="en">← Overview</a>')

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
    for i, s in missing[:15]:
        print(f'  #{i}: {s!r}')
