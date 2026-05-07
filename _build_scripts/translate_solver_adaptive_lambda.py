#!/usr/bin/env python3
"""Translate solver_adaptive_lambda.html body to bilingual DE/EN."""
from pathlib import Path
import re as _re

p = Path('/home/claude/build/solver_adaptive_lambda.html')
html = p.read_text(encoding='utf-8')

REPS = []
def pair(old, new): REPS.append((old, new))

# ── Nav ──
NAV = [
    ('status',        'Status',                     'Status'),
    ('idee',          'Grundidee',                  'Idea'),
    ('flussdiagramm', 'Flussdiagramm',              'Flow chart'),
    ('pseudocode',    'Pseudocode',                 'Pseudocode'),
    ('dateien',       'Dateien',                    'Files'),
    ('parameter',     'Parameter',                  'Parameters'),
    ('verhalten',     'Verhalten auf NozzleSystem', 'Behavior on NozzleSystem'),
    ('grenzen',       'Grenzen',                    'Limits'),
]
for anchor, de, en in NAV:
    pair(f'<a href="#{anchor}">{de}</a>',
         f'<a href="#{anchor}" data-lang="de">{de}</a>'
         f'<a href="#{anchor}" data-lang="en">{en}</a>')

# ── h2 ──
def h2(de, en):
    pair(f'<h2>{de}</h2>',
         f'<h2 data-lang="de">{de}</h2><h2 data-lang="en">{en}</h2>')

h2('Status — wichtig zu lesen',          'Status — important to read')
h2('Grundidee — Wrapper über bewährte Solver', 'Idea — wrapper over proven solvers')
h2('Flussdiagramm',                      'Flow chart')
h2('Pseudocode',                         'Pseudocode')
h2('Dateien',                            'Files')
h2('CLI-Parameter',                      'CLI parameters')
h2('Verhalten auf NozzleSystem',         'Behavior on NozzleSystem')
h2('Grenzen — wann nicht verwenden',     'Limits — when not to use')

# ── h3 ──
def h3(de, en):
    pair(f'<h3>{de}</h3>',
         f'<h3 data-lang="de">{de}</h3><h3 data-lang="en">{en}</h3>')

h3('Was diese Architektur attraktiv macht',
   'Why this architecture is attractive')
h3('Innerer Solver — Auswahl',          'Inner solver — selection')
h3('Beispiel-Aufrufe',                  'Example invocations')
h3('Phase 1 mit EQUILIBRATE — produktiv ✅',
   'Phase 1 with EQUILIBRATE — production-ready ✅')
h3('Phase 1 ohne Skalierung — auch produktiv ✅',
   'Phase 1 without scaling — also production-ready ✅')
h3('Phase 2 mit -SH:DIRECT=OFF — divergiert ❌',
   'Phase 2 with -SH:DIRECT=OFF — diverges ❌')
h3('Diagnose der Phase-2-Divergenz',    'Diagnostic of phase-2 divergence')
h3('Wann er sinnvoll ist',              'When it is useful')
h3('Roadmap',                           'Roadmap')

# ── Status section: 3 notes ──
pair('<div class="note green">\n    <strong>Phase 1 (try-direct-first) ist produktiv nutzbar.</strong>\n    Der Wrapper versucht zuerst den direkten inneren Solver mit\n    geerbter Skalierungsstrategie. Auf NozzleSystem konvergiert das\n    in 5 Iter (mit EQUILIBRATE) bzw. 6 Iter (ohne) in ~0.4 Sekunden —\n    identisch zu direktem NEWTON_ARMIJO. Praktisch sinnvoll als\n    "sicherer Wrapper" der bei Bedarf eine Continuation-Schicht hinzufügt.\n  </div>',
     '<div class="note green" data-lang="de">\n    <strong>Phase 1 (try-direct-first) ist produktiv nutzbar.</strong>\n    Der Wrapper versucht zuerst den direkten inneren Solver mit\n    geerbter Skalierungsstrategie. Auf NozzleSystem konvergiert das\n    in 5 Iter (mit EQUILIBRATE) bzw. 6 Iter (ohne) in ~0.4 Sekunden —\n    identisch zu direktem NEWTON_ARMIJO. Praktisch sinnvoll als\n    "sicherer Wrapper" der bei Bedarf eine Continuation-Schicht hinzufügt.\n  </div>'
     '<div class="note green" data-lang="en">\n    <strong>Phase 1 (try-direct-first) is production-ready.</strong>\n    The wrapper first tries the direct inner solver with the inherited scaling\n    strategy. On NozzleSystem this converges in 5 iter (with EQUILIBRATE) or\n    6 iter (without) in ~0.4 seconds — identical to direct NEWTON_ARMIJO.\n    Practically useful as a "safe wrapper" that adds a continuation layer when\n    needed.\n  </div>')

pair('<div class="note red">\n    <strong>Phase 2 (λ-Continuation) ist EXPERIMENTAL — derzeit nicht\n    produktiv konvergent auf NozzleSystem.</strong> Wenn Phase 1 scheitert\n    (oder per <code>-SH:DIRECT=OFF</code> übersprungen wird), startet die\n    λ-Schleife. Auf NozzleSystem divergiert der innere Solver auf dem\n    H_λ-System (siehe <a href="#verhalten">Diagnose</a>): Skalen-Mismatch\n    zwischen linearem Anteil <code>(1-λ)·J₀·(x-x₀)</code> und nichtlinearem\n    Anteil <code>λ·F(x)</code> bei großen <code>(x-x₀)</code>-Abweichungen.\n  </div>',
     '<div class="note red" data-lang="de">\n    <strong>Phase 2 (λ-Continuation) ist EXPERIMENTAL — derzeit nicht\n    produktiv konvergent auf NozzleSystem.</strong> Wenn Phase 1 scheitert\n    (oder per <code>-SH:DIRECT=OFF</code> übersprungen wird), startet die\n    λ-Schleife. Auf NozzleSystem divergiert der innere Solver auf dem\n    H_λ-System (siehe <a href="#verhalten">Diagnose</a>): Skalen-Mismatch\n    zwischen linearem Anteil <code>(1-λ)·J₀·(x-x₀)</code> und nichtlinearem\n    Anteil <code>λ·F(x)</code> bei großen <code>(x-x₀)</code>-Abweichungen.\n  </div>'
     '<div class="note red" data-lang="en">\n    <strong>Phase 2 (λ continuation) is EXPERIMENTAL — currently does not\n    converge productively on NozzleSystem.</strong> When phase 1 fails (or is\n    skipped via <code>-SH:DIRECT=OFF</code>), the λ loop starts. On\n    NozzleSystem the inner solver diverges on the H_λ system (see\n    <a href="#verhalten">diagnostic</a>): a scale mismatch between the linear\n    part <code>(1-λ)·J₀·(x-x₀)</code> and the nonlinear part <code>λ·F(x)</code>\n    at large <code>(x-x₀)</code> deviations.\n  </div>')

pair('<div class="note blue">\n    <strong>Empfehlung:</strong>\n    <ul style="margin-top: 0.4rem;">\n      <li>Für NozzleSystem-artige Probleme: stattdessen direkt\n        <a href="solver_newton_armijo.html">NEWTON_ARMIJO</a> mit\n        <code>-SC:EQUILIBRATE</code> oder\n        <a href="solver_lm.html">LEVENBERG_MARQUARDT</a> verwenden</li>\n      <li>ADAPTIVE_LAMBDA sinnvoll als Wrapper wenn Du <em>nicht weißt</em>\n        ob das Modell direkt konvergiert — Phase 1 versucht\'s, Phase 2\n        ist Fallback (mit den genannten Limitierungen)</li>\n    </ul>\n  </div>',
     '<div class="note blue" data-lang="de">\n    <strong>Empfehlung:</strong>\n    <ul style="margin-top: 0.4rem;">\n      <li>Für NozzleSystem-artige Probleme: stattdessen direkt\n        <a href="solver_newton_armijo.html">NEWTON_ARMIJO</a> mit\n        <code>-SC:EQUILIBRATE</code> oder\n        <a href="solver_lm.html">LEVENBERG_MARQUARDT</a> verwenden</li>\n      <li>ADAPTIVE_LAMBDA sinnvoll als Wrapper wenn Du <em>nicht weißt</em>\n        ob das Modell direkt konvergiert — Phase 1 versucht\'s, Phase 2\n        ist Fallback (mit den genannten Limitierungen)</li>\n    </ul>\n  </div>'
     '<div class="note blue" data-lang="en">\n    <strong>Recommendation:</strong>\n    <ul style="margin-top: 0.4rem;">\n      <li>For NozzleSystem-like problems: use\n        <a href="solver_newton_armijo.html">NEWTON_ARMIJO</a> with\n        <code>-SC:EQUILIBRATE</code> or\n        <a href="solver_lm.html">LEVENBERG_MARQUARDT</a> directly instead</li>\n      <li>ADAPTIVE_LAMBDA is useful as a wrapper when you <em>don\'t know</em>\n        whether the model converges directly — phase 1 tries, phase 2 is\n        fallback (with the limitations noted)</li>\n    </ul>\n  </div>')

# ── Idee section ──
pair('<p>\n    Statt eigene Continuation-Mathematik (wie HOMOTOPY oder ARC_LENGTH)\n    nutzt ADAPTIVE_LAMBDA den existierenden Newton-Armijo-Solver als\n    Engine und legt eine zweistufige Schicht darüber:\n  </p>',
     '<p data-lang="de">\n    Statt eigene Continuation-Mathematik (wie HOMOTOPY oder ARC_LENGTH)\n    nutzt ADAPTIVE_LAMBDA den existierenden Newton-Armijo-Solver als\n    Engine und legt eine zweistufige Schicht darüber:\n  </p>'
     '<p data-lang="en">\n    Instead of its own continuation mathematics (like HOMOTOPY or ARC_LENGTH),\n    ADAPTIVE_LAMBDA uses the existing Newton-Armijo solver as the engine and\n    adds a two-stage layer on top:\n  </p>')

# math-block hi labels
def hi(de, en):
    pair(f'<span class="hi">{de}</span>',
         f'<span class="hi" data-lang="de">{de}</span>'
         f'<span class="hi" data-lang="en">{en}</span>')

hi('Phase 1 — try-direct-first (Default an):',
   'Phase 1 — try-direct-first (default on):')
hi('Phase 2 — Continuation (wenn Phase 1 scheitert):',
   'Phase 2 — continuation (when phase 1 fails):')

# math-block German lines (in eq divs)
pair('<div class="eq">  versuche innerSolver.solve(F = 0, x₀)</div>',
     '<div class="eq" data-lang="de">  versuche innerSolver.solve(F = 0, x₀)</div>'
     '<div class="eq" data-lang="en">  try innerSolver.solve(F = 0, x₀)</div>')
pair('<div class="eq">  konvergiert? → fertig, kein Continuation</div>',
     '<div class="eq" data-lang="de">  konvergiert? → fertig, kein Continuation</div>'
     '<div class="eq" data-lang="en">  converged? → done, no continuation</div>')
pair('<div class="eq">  J₀ = FD-Jacobi am Startpunkt</div>',
     '<div class="eq" data-lang="de">  J₀ = FD-Jacobi am Startpunkt</div>'
     '<div class="eq" data-lang="en">  J₀ = FD Jacobian at start point</div>')
pair('<div class="eq">    versuche innerSolver.solve(F_λ = 0, x_current)</div>',
     '<div class="eq" data-lang="de">    versuche innerSolver.solve(F_λ = 0, x_current)</div>'
     '<div class="eq" data-lang="en">    try innerSolver.solve(F_λ = 0, x_current)</div>')
pair('<div class="eq">    konvergiert? → x_current = result, λ = λ_next</div>',
     '<div class="eq" data-lang="de">    konvergiert? → x_current = result, λ = λ_next</div>'
     '<div class="eq" data-lang="en">    converged? → x_current = result, λ = λ_next</div>')
pair('<div class="eq">                   wenn iter &lt; target/2: dλ *= 1.5</div>',
     '<div class="eq" data-lang="de">                   wenn iter &lt; target/2: dλ *= 1.5</div>'
     '<div class="eq" data-lang="en">                   if iter &lt; target/2: dλ *= 1.5</div>')
pair('<div class="eq">    fehlgeschlagen? → dλ /= 2,  retry</div>',
     '<div class="eq" data-lang="de">    fehlgeschlagen? → dλ /= 2,  retry</div>'
     '<div class="eq" data-lang="en">    failed? → dλ /= 2,  retry</div>')

# bullets — "Was diese Architektur attraktiv macht"
pair('<ul>\n    <li><strong>Nutzt was funktioniert:</strong> Newton-Armijo+EQUILIBRATE\n        konvergiert NozzleSystem in 5 Iter — wir bauen darüber, statt\n        parallel.</li>\n    <li><strong>Kein eigener Predictor:</strong> x_current ist Predictor —\n        Newton\'s Armijo macht den Rest (Schrittdämpfung, Akzeptanz).</li>\n    <li><strong>Inkrementell sicher:</strong> Phase 1 ist ein einfacher\n        Wrapper-Aufruf. Phase 2 wird nur aktiv wenn nötig.</li>\n    <li><strong>Innerer Solver erbt Skalierung:</strong>\n        <code>-SC:EQUILIBRATE</code> wirkt automatisch auf den inneren\n        Workhorse (Variante c).</li>\n  </ul>',
     '<ul data-lang="de">\n    <li><strong>Nutzt was funktioniert:</strong> Newton-Armijo+EQUILIBRATE\n        konvergiert NozzleSystem in 5 Iter — wir bauen darüber, statt\n        parallel.</li>\n    <li><strong>Kein eigener Predictor:</strong> x_current ist Predictor —\n        Newton\'s Armijo macht den Rest (Schrittdämpfung, Akzeptanz).</li>\n    <li><strong>Inkrementell sicher:</strong> Phase 1 ist ein einfacher\n        Wrapper-Aufruf. Phase 2 wird nur aktiv wenn nötig.</li>\n    <li><strong>Innerer Solver erbt Skalierung:</strong>\n        <code>-SC:EQUILIBRATE</code> wirkt automatisch auf den inneren\n        Workhorse (Variante c).</li>\n  </ul>'
     '<ul data-lang="en">\n    <li><strong>Uses what works:</strong> Newton-Armijo+EQUILIBRATE converges\n        NozzleSystem in 5 iter — we build on top, not in parallel.</li>\n    <li><strong>No custom predictor:</strong> x_current is the predictor —\n        Newton\'s Armijo does the rest (step damping, acceptance).</li>\n    <li><strong>Incrementally safe:</strong> phase 1 is a simple wrapper call.\n        Phase 2 only activates when needed.</li>\n    <li><strong>Inner solver inherits scaling:</strong>\n        <code>-SC:EQUILIBRATE</code> automatically affects the inner workhorse\n        (variant c).</li>\n  </ul>')

pair('<p>\n    Der innere Solver wird so konfiguriert:\n  </p>',
     '<p data-lang="de">\n    Der innere Solver wird so konfiguriert:\n  </p>'
     '<p data-lang="en">\n    The inner solver is configured as follows:\n  </p>')

pair('<ul>\n    <li><strong>Algorithmus:</strong> NEWTON_ARMIJO als sicherer Default.\n        Per <code>-SH:INNER=LEVENBERG_MARQUARDT</code> (oder andere SolverTypes)\n        überschreibbar.</li>\n    <li><strong>Skalierungsstrategie:</strong> Geerbt aus dem Hauptaufruf\n        (<code>-SC:</code>) — das gilt für beide Phasen.</li>\n    <li><strong>maxIter, tolerance:</strong> Aus der äußeren SolverConfig\n        übernommen.</li>\n  </ul>',
     '<ul data-lang="de">\n    <li><strong>Algorithmus:</strong> NEWTON_ARMIJO als sicherer Default.\n        Per <code>-SH:INNER=LEVENBERG_MARQUARDT</code> (oder andere SolverTypes)\n        überschreibbar.</li>\n    <li><strong>Skalierungsstrategie:</strong> Geerbt aus dem Hauptaufruf\n        (<code>-SC:</code>) — das gilt für beide Phasen.</li>\n    <li><strong>maxIter, tolerance:</strong> Aus der äußeren SolverConfig\n        übernommen.</li>\n  </ul>'
     '<ul data-lang="en">\n    <li><strong>Algorithm:</strong> NEWTON_ARMIJO as safe default.\n        Overridable via <code>-SH:INNER=LEVENBERG_MARQUARDT</code> (or other\n        SolverTypes).</li>\n    <li><strong>Scaling strategy:</strong> inherited from the main call\n        (<code>-SC:</code>) — applies to both phases.</li>\n    <li><strong>maxIter, tolerance:</strong> taken from the outer SolverConfig.</li>\n  </ul>')

# ── Flowchart SVG: duplicate for DE/EN ──
DE_FLOW_RE = _re.compile(r'(<div class="flowchart">\s*<svg[^>]*>.*?</svg>\s*</div>)', _re.DOTALL)
m = DE_FLOW_RE.search(html)
if m:
    de_flow = m.group(1)
    en_flow = de_flow
    SVG_REPLACEMENTS = [
        ('Phase 1: direkt',                'Phase 1: direct'),
        ('── Phase 2: λ-Continuation ──',  '── Phase 2: λ continuation ──'),
        ('J₀ via FD am Startpunkt',        'J₀ via FD at start point'),
        ('Inner: solve F_λ(x) = 0 ab x_current',
                                            'Inner: solve F_λ(x) = 0 from x_current'),
        ('inner OK?',                       'inner OK?'),
        ('ja: λ ← λ_next',                  'yes: λ ← λ_next'),
    ]
    for de, en in SVG_REPLACEMENTS:
        en_flow = en_flow.replace(de, en)
    en_flow = en_flow.replace('>ja</text>', '>yes</text>')
    en_flow = en_flow.replace('>nein</text>', '>no</text>')

    new_block = (
        '<div data-lang="de">' + de_flow + '</div>'
        '<div data-lang="en">' + en_flow + '</div>'
    )
    pair(de_flow, new_block)

# ── Pseudocode block: wrap with DE/EN ──
DE_PRE = '''<pre><code>solve(sysData, useInitData):
  x₀ = extractFreeValues(sysData)

  // ---- Phase 1: try-direct-first ----
  if hcfg.tryDirectFirst:
    innerCfg = buildInnerConfig()              // Newton-Armijo + EQUILIBRATE etc.
    direct = innerCfg.solver.solve(sysData)
    if direct.converged:
      return success(direct)
    reset values to x₀                          // wichtig: x kann driften

  // ---- Phase 2: λ-Continuation ----
  J₀ = FD-Jacobi am Startpunkt
  x_current = x₀
  λ = 0,  dλ = 0.5
  innerSolver = SolverFactory.create(innerCfg)

  while λ &lt; 1:
    λ_next = min(λ + dλ, 1)
    subSystem = buildHomotopySystem(sysData, J₀, x₀, λ_next)
    applyValuesToSystem(subSystem, x_current)
    inner = innerSolver.solve(subSystem)

    if inner.converged:
      x_current = extractFreeValues(subSystem)
      λ = λ_next
      if inner.iter &lt; target/2:
        dλ = min(dλ * 1.5, 0.5)
    else:
      dλ /= 2
      if dλ &lt; 1e-3: abort

  return success(x_current)
</code></pre>'''

EN_PRE = '''<pre><code>solve(sysData, useInitData):
  x₀ = extractFreeValues(sysData)

  // ---- Phase 1: try-direct-first ----
  if hcfg.tryDirectFirst:
    innerCfg = buildInnerConfig()              // Newton-Armijo + EQUILIBRATE etc.
    direct = innerCfg.solver.solve(sysData)
    if direct.converged:
      return success(direct)
    reset values to x₀                          // important: x may have drifted

  // ---- Phase 2: λ continuation ----
  J₀ = FD Jacobian at start point
  x_current = x₀
  λ = 0,  dλ = 0.5
  innerSolver = SolverFactory.create(innerCfg)

  while λ &lt; 1:
    λ_next = min(λ + dλ, 1)
    subSystem = buildHomotopySystem(sysData, J₀, x₀, λ_next)
    applyValuesToSystem(subSystem, x_current)
    inner = innerSolver.solve(subSystem)

    if inner.converged:
      x_current = extractFreeValues(subSystem)
      λ = λ_next
      if inner.iter &lt; target/2:
        dλ = min(dλ * 1.5, 0.5)
    else:
      dλ /= 2
      if dλ &lt; 1e-3: abort

  return success(x_current)
</code></pre>'''

pair(DE_PRE,
     f'<div data-lang="de">{DE_PRE}</div><div data-lang="en">{EN_PRE}</div>')

# ── Files section ──
def filedesc(de, en):
    pair(f'<span class="file-desc">{de}</span>',
         f'<span class="file-desc" data-lang="de">{de}</span>'
         f'<span class="file-desc" data-lang="en">{en}</span>')

filedesc('Hauptklasse, 375 Zeilen — Phase 1 + Phase 2',
         'Main class, 375 lines — phase 1 + phase 2')
filedesc('Wiederverwendet, neu: <code>tryDirectFirst</code>-Feld (Default true)',
         'Reused, new: <code>tryDirectFirst</code> field (default true)')
filedesc('Helper-Methoden (buildHomotopySystem, computeInitialJacobian, ...) sind package-private und werden geteilt',
         'Helper methods (buildHomotopySystem, computeInitialJacobian, ...) are package-private and shared')

# ── Parameter section ──
pair('<th>Parameter</th>\n        <th>Default</th>\n        <th>Beschreibung</th>',
     '<th>Parameter</th>\n        <th>Default</th>\n        <th data-lang="de">Beschreibung</th><th data-lang="en">Description</th>')

def td_pair(de, en):
    pair(f'<td>{de}</td>', f'<td data-lang="de">{de}</td><td data-lang="en">{en}</td>')

td_pair('Aktiviert den Solver', 'Activates the solver')
td_pair('Skalierungsstrategie wird auf den inneren Solver vererbt\n          (NONE / EQUILIBRATE / DIAGONAL)',
        'Scaling strategy is inherited by the inner solver\n          (NONE / EQUILIBRATE / DIAGONAL)')
td_pair('Phase 1 (try-direct-first) ein/aus. OFF erzwingt\n          Phase 2 (Continuation) auch wenn Phase 1 erfolgreich wäre',
        'Phase 1 (try-direct-first) on/off. OFF forces phase 2 (continuation)\n          even when phase 1 would succeed')
td_pair('Algorithmus des inneren Solvers (NEWTON_ARMIJO, LEVENBERG_MARQUARDT, BROYDEN)',
        'Algorithm of the inner solver (NEWTON_ARMIJO, LEVENBERG_MARQUARDT, BROYDEN)')
td_pair('Maximal-Anzahl Pfadschritte in Phase 2',
        'Maximum number of path steps in phase 2')
td_pair('Initiale dλ-Schrittweite (wird intern auf 0.5 erhöht)',
        'Initial dλ step size (raised internally to 0.5)')

# code-comments in pre block
def cmt(de, en):
    pair(f'<span class="cmt">{de}</span>',
         f'<span class="cmt" data-lang="de">{de}</span>'
         f'<span class="cmt" data-lang="en">{en}</span>')

cmt('# Standard: Phase 1 versucht NEWTON_ARMIJO+EQUILIBRATE direkt',
    '# Default: phase 1 tries NEWTON_ARMIJO+EQUILIBRATE directly')
cmt('# Continuation erzwingen (auch wenn direkt klappen würde)',
    '# Force continuation (even if direct would succeed)')
cmt('# Mit LM als innerem Solver',
    '# With LM as the inner solver')

# ── Verhalten section ──
pair('<pre><code>$ -S:ADAPTIVE_LAMBDA -SC:EQUILIBRATE\n\n[INFO] Phase 1: trying direct Newton-Raphson + Armijo line search (scaling=EQUILIBRATE)\n[INFO] Iter 0: ||F||=2.27e+07\n[INFO] Iter 5: ||F||=8.99e-09  ← konvergiert\n[INFO] Phase 1 succeeded: direct solver converged in 5 iter — no continuation needed</code></pre>',
     '<pre data-lang="de"><code>$ -S:ADAPTIVE_LAMBDA -SC:EQUILIBRATE\n\n[INFO] Phase 1: trying direct Newton-Raphson + Armijo line search (scaling=EQUILIBRATE)\n[INFO] Iter 0: ||F||=2.27e+07\n[INFO] Iter 5: ||F||=8.99e-09  ← konvergiert\n[INFO] Phase 1 succeeded: direct solver converged in 5 iter — no continuation needed</code></pre>'
     '<pre data-lang="en"><code>$ -S:ADAPTIVE_LAMBDA -SC:EQUILIBRATE\n\n[INFO] Phase 1: trying direct Newton-Raphson + Armijo line search (scaling=EQUILIBRATE)\n[INFO] Iter 0: ||F||=2.27e+07\n[INFO] Iter 5: ||F||=8.99e-09  ← converged\n[INFO] Phase 1 succeeded: direct solver converged in 5 iter — no continuation needed</code></pre>')

pair('<p>\n    Mit GAMMA-Bound-Fix (Lower=1.05) im Modell konvergiert Newton auch\n    ohne Equilibrator:\n  </p>',
     '<p data-lang="de">\n    Mit GAMMA-Bound-Fix (Lower=1.05) im Modell konvergiert Newton auch\n    ohne Equilibrator:\n  </p>'
     '<p data-lang="en">\n    With the GAMMA bound fix (Lower=1.05) in the model, Newton also converges\n    without the equilibrator:\n  </p>')

pair('<pre><code>$ -S:ADAPTIVE_LAMBDA\n\n[INFO] Phase 1: trying direct (scaling=NONE)\n[INFO] Iter 6: ||F||=1.64e-08  ← konvergiert\n[INFO] Phase 1 succeeded: direct solver converged in 6 iter</code></pre>',
     '<pre data-lang="de"><code>$ -S:ADAPTIVE_LAMBDA\n\n[INFO] Phase 1: trying direct (scaling=NONE)\n[INFO] Iter 6: ||F||=1.64e-08  ← konvergiert\n[INFO] Phase 1 succeeded: direct solver converged in 6 iter</code></pre>'
     '<pre data-lang="en"><code>$ -S:ADAPTIVE_LAMBDA\n\n[INFO] Phase 1: trying direct (scaling=NONE)\n[INFO] Iter 6: ||F||=1.64e-08  ← converged\n[INFO] Phase 1 succeeded: direct solver converged in 6 iter</code></pre>')

pair('<pre><code>$ -S:ADAPTIVE_LAMBDA -SC:EQUILIBRATE -SH:DIRECT=OFF\n\n[INFO] Phase 2: starting lambda continuation\n[INFO] Step 1: λ 0.0000 → 0.5000\n[INFO] inner Iter 0: ||F||=9.02e+07     ← schon größer als Original-||F(x₀)||\n[INFO] inner Iter 99: ||F||=1.33e+10    ← divergiert\n[WARN]   → failed at λ=0.5000, reducing dλ\n[INFO] Step 2: λ 0.0000 → 0.2500\n[INFO] inner Iter 0: ||F||=2.92e+07\n... (gleiche Divergenz)</code></pre>',
     '<pre data-lang="de"><code>$ -S:ADAPTIVE_LAMBDA -SC:EQUILIBRATE -SH:DIRECT=OFF\n\n[INFO] Phase 2: starting lambda continuation\n[INFO] Step 1: λ 0.0000 → 0.5000\n[INFO] inner Iter 0: ||F||=9.02e+07     ← schon größer als Original-||F(x₀)||\n[INFO] inner Iter 99: ||F||=1.33e+10    ← divergiert\n[WARN]   → failed at λ=0.5000, reducing dλ\n[INFO] Step 2: λ 0.0000 → 0.2500\n[INFO] inner Iter 0: ||F||=2.92e+07\n... (gleiche Divergenz)</code></pre>'
     '<pre data-lang="en"><code>$ -S:ADAPTIVE_LAMBDA -SC:EQUILIBRATE -SH:DIRECT=OFF\n\n[INFO] Phase 2: starting lambda continuation\n[INFO] Step 1: λ 0.0000 → 0.5000\n[INFO] inner Iter 0: ||F||=9.02e+07     ← already larger than original ||F(x₀)||\n[INFO] inner Iter 99: ||F||=1.33e+10    ← diverges\n[WARN]   → failed at λ=0.5000, reducing dλ\n[INFO] Step 2: λ 0.0000 → 0.2500\n[INFO] inner Iter 0: ||F||=2.92e+07\n... (same divergence)</code></pre>')

pair('<p>\n    Das Sub-System <code>F_λ(x) = (1-λ)·J₀·(x-x₀) + λ·F(x) = 0</code> hat\n    bei NozzleSystem ein konzeptionelles Skalen-Problem:\n  </p>',
     '<p data-lang="de">\n    Das Sub-System <code>F_λ(x) = (1-λ)·J₀·(x-x₀) + λ·F(x) = 0</code> hat\n    bei NozzleSystem ein konzeptionelles Skalen-Problem:\n  </p>'
     '<p data-lang="en">\n    The sub-system <code>F_λ(x) = (1-λ)·J₀·(x-x₀) + λ·F(x) = 0</code> has a\n    conceptual scale problem on NozzleSystem:\n  </p>')

pair('<ul>\n    <li>Linearer Anteil <code>J₀·(x-x₀)</code> wächst <em>linear</em> mit\n        |x-x₀|. Bei großen Newton-Schritten dominiert er F(x).</li>\n    <li>Bounds-Verletzungen: <code>FULLM.F080.PS = -2.02e+06 (Lower=1000)</code>,\n        <code>FULLM.F180.RHO = -22 (Lower=0)</code> — Newton\'s Schritt\n        treibt Variablen weit aus zulässigen Bereichen.</li>\n    <li>Equilibrator-Skalen springen zwischen Iter sprunghaft\n        (<code>rowScale_min: 2.16e-12 → 2.96e-16</code>) — System verliert\n        seine Konsistenz.</li>\n  </ul>',
     '<ul data-lang="de">\n    <li>Linearer Anteil <code>J₀·(x-x₀)</code> wächst <em>linear</em> mit\n        |x-x₀|. Bei großen Newton-Schritten dominiert er F(x).</li>\n    <li>Bounds-Verletzungen: <code>FULLM.F080.PS = -2.02e+06 (Lower=1000)</code>,\n        <code>FULLM.F180.RHO = -22 (Lower=0)</code> — Newton\'s Schritt\n        treibt Variablen weit aus zulässigen Bereichen.</li>\n    <li>Equilibrator-Skalen springen zwischen Iter sprunghaft\n        (<code>rowScale_min: 2.16e-12 → 2.96e-16</code>) — System verliert\n        seine Konsistenz.</li>\n  </ul>'
     '<ul data-lang="en">\n    <li>The linear part <code>J₀·(x-x₀)</code> grows <em>linearly</em> with\n        |x-x₀|. On large Newton steps it dominates F(x).</li>\n    <li>Bounds violations: <code>FULLM.F080.PS = -2.02e+06 (Lower=1000)</code>,\n        <code>FULLM.F180.RHO = -22 (Lower=0)</code> — Newton\'s step pushes\n        variables far outside admissible ranges.</li>\n    <li>Equilibrator scales jump abruptly between iterations\n        (<code>rowScale_min: 2.16e-12 → 2.96e-16</code>) — the system loses\n        its consistency.</li>\n  </ul>')

pair('<p>\n    Das ist <strong>kein Solver-Bug</strong>, sondern eine Folge der\n    Problem-Topologie: das Modell hat enge Bounds (Drücke ≥ 1000 Pa)\n    und Newton-Armijo\'s Armijo-Dämpfung reicht nicht aus um auf dem\n    H_λ-System zu konvergieren — selbst wenn er auf dem reinen F-System\n    konvergieren würde.\n  </p>',
     '<p data-lang="de">\n    Das ist <strong>kein Solver-Bug</strong>, sondern eine Folge der\n    Problem-Topologie: das Modell hat enge Bounds (Drücke ≥ 1000 Pa)\n    und Newton-Armijo\'s Armijo-Dämpfung reicht nicht aus um auf dem\n    H_λ-System zu konvergieren — selbst wenn er auf dem reinen F-System\n    konvergieren würde.\n  </p>'
     '<p data-lang="en">\n    This is <strong>not a solver bug</strong> but a consequence of the\n    problem topology: the model has tight bounds (pressures ≥ 1000 Pa) and\n    Newton-Armijo\'s Armijo damping is not sufficient to converge on the H_λ\n    system — even when it would converge on the plain F system.\n  </p>')

# ── Grenzen section ──
pair('<ul>\n    <li>\n      <strong>Phase 2 auf Modellen mit engen Bounds und kappa &gt; 10⁹:</strong>\n      Funktioniert nicht zuverlässig (siehe NozzleSystem-Diagnose oben).\n      Diese Modelle sind besser direkt mit Newton-Armijo+EQUILIBRATE oder\n      LM zu lösen.\n    </li>\n    <li>\n      <strong>Phase 1 wenn Newton sicher direkt scheitert:</strong> Spart\n      ein paar Iterationen wenn man Continuation eh braucht — dann\n      <code>-SH:DIRECT=OFF</code> setzen. Aber ehrlicherweise ist dann\n      auch Phase 2 fragwürdig.\n    </li>\n  </ul>',
     '<ul data-lang="de">\n    <li>\n      <strong>Phase 2 auf Modellen mit engen Bounds und kappa &gt; 10⁹:</strong>\n      Funktioniert nicht zuverlässig (siehe NozzleSystem-Diagnose oben).\n      Diese Modelle sind besser direkt mit Newton-Armijo+EQUILIBRATE oder\n      LM zu lösen.\n    </li>\n    <li>\n      <strong>Phase 1 wenn Newton sicher direkt scheitert:</strong> Spart\n      ein paar Iterationen wenn man Continuation eh braucht — dann\n      <code>-SH:DIRECT=OFF</code> setzen. Aber ehrlicherweise ist dann\n      auch Phase 2 fragwürdig.\n    </li>\n  </ul>'
     '<ul data-lang="en">\n    <li>\n      <strong>Phase 2 on models with tight bounds and kappa &gt; 10⁹:</strong>\n      Does not work reliably (see NozzleSystem diagnostic above). These\n      models are better solved directly with Newton-Armijo+EQUILIBRATE or LM.\n    </li>\n    <li>\n      <strong>Phase 1 when Newton is sure to fail directly:</strong> saves a\n      few iterations if continuation is needed anyway — then set\n      <code>-SH:DIRECT=OFF</code>. But honestly, phase 2 is also questionable\n      in that case.\n    </li>\n  </ul>')

pair('<ul>\n    <li><strong>Als Wrapper bei unbekanntem Modell-Verhalten:</strong>\n        Phase 1 versucht\'s pragmatisch, Phase 2 ist Sicherheitsnetz.\n        Bei moderaten Modellen kann Phase 2 helfen.</li>\n    <li><strong>Phase 1 alleine als Default-Solver:</strong> Identische\n        Performance zu Newton-Armijo, aber mit eingebautem Fallback-Verhalten\n        falls die innere Konvergenz scheitert.</li>\n  </ul>',
     '<ul data-lang="de">\n    <li><strong>Als Wrapper bei unbekanntem Modell-Verhalten:</strong>\n        Phase 1 versucht\'s pragmatisch, Phase 2 ist Sicherheitsnetz.\n        Bei moderaten Modellen kann Phase 2 helfen.</li>\n    <li><strong>Phase 1 alleine als Default-Solver:</strong> Identische\n        Performance zu Newton-Armijo, aber mit eingebautem Fallback-Verhalten\n        falls die innere Konvergenz scheitert.</li>\n  </ul>'
     '<ul data-lang="en">\n    <li><strong>As a wrapper for unknown model behavior:</strong> phase 1\n        tries pragmatically, phase 2 is the safety net. On moderate models\n        phase 2 can help.</li>\n    <li><strong>Phase 1 alone as default solver:</strong> identical\n        performance to Newton-Armijo, but with built-in fallback behavior\n        if inner convergence fails.</li>\n  </ul>')

pair('<p>\n    Phase 2 könnte mit folgenden Verbesserungen produktiv werden:\n  </p>',
     '<p data-lang="de">\n    Phase 2 könnte mit folgenden Verbesserungen produktiv werden:\n  </p>'
     '<p data-lang="en">\n    Phase 2 could become production-ready with the following improvements:\n  </p>')

pair('<ul>\n    <li>Skalen-bewusste H_λ-Definition: <code>F_λ = (1-λ)·D·(x-x₀) + λ·F(x)</code>\n      mit Diagonalmatrix D passend zu F-Skalen</li>\n    <li>Bounds-Vorhersage im äußeren Loop — kleineres dλ wählen wenn\n      Bounds-Verletzung droht</li>\n    <li>Trust-Region zwischen λ-Schritten</li>\n  </ul>',
     '<ul data-lang="de">\n    <li>Skalen-bewusste H_λ-Definition: <code>F_λ = (1-λ)·D·(x-x₀) + λ·F(x)</code>\n      mit Diagonalmatrix D passend zu F-Skalen</li>\n    <li>Bounds-Vorhersage im äußeren Loop — kleineres dλ wählen wenn\n      Bounds-Verletzung droht</li>\n    <li>Trust-Region zwischen λ-Schritten</li>\n  </ul>'
     '<ul data-lang="en">\n    <li>Scale-aware H_λ definition: <code>F_λ = (1-λ)·D·(x-x₀) + λ·F(x)</code>\n      with diagonal matrix D matched to F scales</li>\n    <li>Bounds prediction in the outer loop — pick a smaller dλ when bounds\n      violation looms</li>\n    <li>Trust region between λ steps</li>\n  </ul>')

pair('<p>\n    Diese Verbesserungen sind nicht implementiert weil das vorhandene\n    Test-Modell (NozzleSystem mit GAMMA-Fix) Phase 1 löst und kein\n    weiteres pathologisches Modell zur Validierung verfügbar ist.\n  </p>',
     '<p data-lang="de">\n    Diese Verbesserungen sind nicht implementiert weil das vorhandene\n    Test-Modell (NozzleSystem mit GAMMA-Fix) Phase 1 löst und kein\n    weiteres pathologisches Modell zur Validierung verfügbar ist.\n  </p>'
     '<p data-lang="en">\n    These improvements are not implemented because the existing test model\n    (NozzleSystem with GAMMA fix) is solved by phase 1 and no further\n    pathological model is available for validation.\n  </p>')

# ── Footer harmonization ──
OLD_FOOTER = '''<footer>
  <hr>
  <p style="color: #4a5568; font-size: 12px; text-align: center;">
    CMDSolver Documentation — Solver 9/9 — AdaptiveLambdaSolver (Phase 1 produktiv, Phase 2 experimental, v2.12)
  </p>
</footer>'''

NEW_FOOTER = '''<footer>
  <span data-lang="de">CMDSolver Docs · Adaptive-Lambda (Phase 1 produktiv, Phase 2 experimental) · v2.12</span><span data-lang="en">CMDSolver Docs · Adaptive-Lambda (phase 1 production, phase 2 experimental) · v2.12</span>
  <span>
    <a href="solver_arc_length.html" data-lang="de">← Arc-Length</a><a href="solver_arc_length.html" data-lang="en">← Arc-Length</a>
    &nbsp;|&nbsp;
    <a href="index.html" data-lang="de">Übersicht →</a><a href="index.html" data-lang="en">Overview →</a>
  </span>
</footer>'''

pair(OLD_FOOTER, NEW_FOOTER)

# Apply
missing = []
for i, (old, new) in enumerate(REPS):
    if old not in html: missing.append((i, old[:80])); continue
    html = html.replace(old, new, 1)

p.write_text(html, encoding='utf-8')
print(f'solver_adaptive_lambda.html: {len(REPS) - len(missing)} / {len(REPS)} replacements')
if missing:
    print('NOT FOUND:')
    for i, s in missing[:10]: print(f'  #{i}: {s!r}')
