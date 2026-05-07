#!/usr/bin/env python3
"""Translates body content of examples.html to bilingual DE/EN."""
from pathlib import Path

p = Path('/home/claude/build/examples.html')
html = p.read_text(encoding='utf-8')

REPS = []
def pair(old, new): REPS.append((old, new))

# ── Nav ──
pair('<a href="#simplesystem">SimpleSystem</a>',
     '<a href="#simplesystem" data-lang="de">SimpleSystem</a>'
     '<a href="#simplesystem" data-lang="en">SimpleSystem</a>')
pair('<a href="#nozzle">NozzleSystem</a>',
     '<a href="#nozzle" data-lang="de">NozzleSystem</a>'
     '<a href="#nozzle" data-lang="en">NozzleSystem</a>')
pair('<a href="#eigenes">Eigenes Modell</a>',
     '<a href="#eigenes" data-lang="de">Eigenes Modell</a>'
     '<a href="#eigenes" data-lang="en">Your own model</a>')

# ── h2 / h3 ──
def h2(de, en):
    pair(f'<h2>{de}</h2>',
         f'<h2 data-lang="de">{de}</h2><h2 data-lang="en">{en}</h2>')
def h3(de, en):
    pair(f'<h3>{de}</h3>',
         f'<h3 data-lang="de">{de}</h3><h3 data-lang="en">{en}</h3>')

h2('SimpleSystem.cas — Basis-Testsystem', 'SimpleSystem.cas — Base Test System')
h2('NozzleSystem_4_fixed.cas — Aerothermodynamisches Düsenmodell',
   'NozzleSystem_4_fixed.cas — Aerothermodynamic Nozzle Model')
h2('Eigenes Modell aufbauen — Schritt für Schritt',
   'Build Your Own Model — Step by Step')

h3('Was wird modelliert?', 'What is modeled?')
h3('Interessante Gleichungstypen', 'Interesting equation types')
h3('Konvergenzergebnisse aller Solver', 'Convergence results across all solvers')
h3('CLI-Aufruf', 'CLI invocation')
h3('SolverAPI-Aufruf', 'SolverAPI invocation')
h3('Modellstruktur', 'Model structure')
h3('Warum ist dieses Modell schwierig?', 'Why is this model challenging?')
h3('Solver-Empfehlung für dieses Modell', 'Solver recommendation for this model')
h3('Minimales Starter-Template', 'Minimal starter template')

# ── SimpleSystem section ──

# Badge text
pair('<span class="badge b-ok">12 Gleichungen · 20 Variablen · 8 fixiert</span>',
     '<span class="badge b-ok" data-lang="de">12 Gleichungen · 20 Variablen · 8 fixiert</span>'
     '<span class="badge b-ok" data-lang="en">12 equations · 20 variables · 8 fixed</span>')

# Model stats labels
def ms_lbl(de, en):
    pair(f'<span class="ms-lbl">{de}</span>',
         f'<span class="ms-lbl" data-lang="de">{de}</span>'
         f'<span class="ms-lbl" data-lang="en">{en}</span>')

ms_lbl('Gleichungen', 'Equations')
ms_lbl('Variablen', 'Variables')
ms_lbl('Fixiert', 'Fixed')
ms_lbl('Frei (Unbekannte)', 'Free (Unknowns)')
ms_lbl('Typisches κ', 'Typical κ')
ms_lbl('Thermodynamik', 'Thermodynamics')
ms_lbl('Atmosphäre', 'Atmosphere')

# What is modeled - paragraph 1
pair('<p>Ein vereinfachtes thermodynamisches System mit algebraischen Abhängigkeiten\n      zwischen Druck, Temperatur, Massenstrom und abgeleiteten Größen. Das Modell ist\n      speziell für Tests konzipiert — realistisch konditioniert aber ohne physikalisch\n      kritische Bereiche (kein Ma-Übergang, keine Phasenübergänge).</p>',
     '<p data-lang="de">Ein vereinfachtes thermodynamisches System mit algebraischen Abhängigkeiten\n      zwischen Druck, Temperatur, Massenstrom und abgeleiteten Größen. Das Modell ist\n      speziell für Tests konzipiert — realistisch konditioniert aber ohne physikalisch\n      kritische Bereiche (kein Ma-Übergang, keine Phasenübergänge).</p>'
     '<p data-lang="en">A simplified thermodynamic system with algebraic dependencies between\n      pressure, temperature, mass flow, and derived quantities. The model is specifically\n      designed for testing — realistically conditioned but without physically critical regions\n      (no Mach transition, no phase transitions).</p>')

# Equation card titles
def eqn_title(de, en):
    pair(f'<div class="eqn-title">{de}</div>',
         f'<div class="eqn-title" data-lang="de">{de}</div>'
         f'<div class="eqn-title" data-lang="en">{en}</div>')

eqn_title('Gleichgewichtsgleichung — direkte Zuweisung',
          'Equilibrium equation — direct assignment')
eqn_title('CALL-Gleichung — thermodynamische Built-in Funktion',
          'CALL equation — thermodynamic built-in function')
eqn_title('Nichtlineare Gleichung — Potenz',
          'Nonlinear equation — power')
eqn_title('Struktureller IF — Betriebsmodus-Schalter',
          'Structural IF — operating-mode switch')
eqn_title('MofCondiRatio — Machzahl aus Flächenverhältnis',
          'MofCondiRatio — Mach number from area ratio')
eqn_title('JANAF-Enthalpieberechnung', 'JANAF enthalpy computation')

# Equation explanations (eqn-exp spans inside eqn-body)
def exp(de, en):
    pair(f'<span class="eqn-exp">{de}</span>',
         f'<span class="eqn-exp" data-lang="de">{de}</span>'
         f'<span class="eqn-exp" data-lang="en">{en}</span>')

exp('// Isentropenexponent κ = cp / (cp - R)',
    '// Isentropic exponent κ = cp / (cp - R)')
exp('// cp(T, WGR, FAR) aus BIfunctions.CpOfTNOZ()',
    '// cp(T, WGR, FAR) from BIfunctions.CpOfTNOZ()')
exp('// Ableitung numerisch (5-Punkte-Formel)',
    '// Derivative numerical (5-point formula)')
exp('// Statischer Druck aus Totaldruck via isentrope Beziehung',
    '// Static pressure from total pressure via isentropic relation')
exp('// EXP1, EXP2 = fixierte Hilfsgrößen aus dem INITIALIZE-Block',
    '// EXP1, EXP2 = fixed auxiliary quantities from the INITIALIZE block')
exp('// Schaltet zwischen Betriebsmodi zur Parse-Zeit — nicht zur Laufzeit',
    '// Switches between operating modes at parse time — not at runtime')
exp('// STATICSWITCH.Spec == Fixed → Umgebungsdruck direkt vorgegeben',
    '// STATICSWITCH.Spec == Fixed → ambient pressure given directly')
exp('// Löst A/A* = f(Ma, κ) numerisch nach Ma auf',
    '// Numerically solves A/A* = f(Ma, κ) for Ma')
exp('// Transzendente Gleichung — nur numerisch lösbar',
    '// Transcendental equation — only numerically solvable')
exp('// Ableitung via 5-Punkte-Formel in BIfunctions',
    '// Derivative via 5-point formula in BIfunctions')
exp('// Spezifische Enthalpie h(T) für Gasgemisch via JANAF-Polynome',
    '// Specific enthalpy h(T) for the gas mixture via JANAF polynomials')
exp('// 13 Eingaben — vollständige Gaszusammensetzung',
    '// 13 inputs — full gas composition')

# Convergence table — th headers
pair('<tr><th>Solver</th><th>Status</th><th>Iterationen</th><th>fsum</th><th>Zeit</th><th>Hinweis</th></tr>',
     '<tr>'
     '<th>Solver</th><th>Status</th>'
     '<th data-lang="de">Iterationen</th><th data-lang="en">Iterations</th>'
     '<th>fsum</th>'
     '<th data-lang="de">Zeit</th><th data-lang="en">Time</th>'
     '<th data-lang="de">Hinweis</th><th data-lang="en">Note</th>'
     '</tr>')

# Convergence table — note cells
def td_pair(de, en):
    pair(f'<td>{de}</td>', f'<td data-lang="de">{de}</td><td data-lang="en">{en}</td>')

td_pair('Gut konditioniertes System → quadratische Konvergenz',
        'Well-conditioned system → quadratic convergence')
td_pair('Sparse-LU schneller als dichte LU',
        'Sparse LU is faster than dense LU')
td_pair('★ Empfohlen — beste Kombination',
        '★ Recommended — best combination')
td_pair('Mehr Iterationen wegen μ-Anpassung — κ hier kein Problem',
        'More iterations due to μ adjustment — κ is not an issue here')
td_pair('Superlinear statt quadratisch',
        'Superlinear rather than quadratic')
td_pair('Schnellster Gesamtlauf — Rang-1 Update + Sparse-LU',
        'Fastest overall — rank-1 update + sparse LU')
td_pair('*NaN normal — Homotopie gibt kein fsum über Standard-Kanal',
        '*NaN is normal — homotopy does not emit fsum on the standard channel')

# SolverAPI-Aufruf comments
pair('<span class="cmt">// Ergebnis prüfen</span>',
     '<span class="cmt" data-lang="de">// Ergebnis prüfen</span>'
     '<span class="cmt" data-lang="en">// Check result</span>')
pair('<span class="cmt">// Alle Werte ausgeben</span>',
     '<span class="cmt" data-lang="de">// Alle Werte ausgeben</span>'
     '<span class="cmt" data-lang="en">// Print all values</span>')
pair('System.out.println(<span class="str">"Konvergiert: "</span> + result.isConverged());',
     '<span data-lang="de">System.out.println(<span class="str">"Konvergiert: "</span> + result.isConverged());</span>'
     '<span data-lang="en">System.out.println(<span class="str">"Converged: "</span> + result.isConverged());</span>')
pair('System.out.println(<span class="str">"Iterationen: "</span> + result.getIterations());',
     '<span data-lang="de">System.out.println(<span class="str">"Iterationen: "</span> + result.getIterations());</span>'
     '<span data-lang="en">System.out.println(<span class="str">"Iterations: "</span> + result.getIterations());</span>')

# Note green box
pair('<div class="note green">\n        <strong>Als Regressions-Baseline:</strong> SimpleSystem.cas ist das Referenzsystem\n        für alle Solver-Tests. Nach jeder Änderung am Code muss <code>-TEST</code>\n        auf diesem Modell alle 7 Solver mit identischen Residuen liefern.\n        Referenzwerte: Newton 3 Iter / 3.16e-11, BroydenSparse ~9ms.\n      </div>',
     '<div class="note green" data-lang="de">\n        <strong>Als Regressions-Baseline:</strong> SimpleSystem.cas ist das Referenzsystem\n        für alle Solver-Tests. Nach jeder Änderung am Code muss <code>-TEST</code>\n        auf diesem Modell alle 7 Solver mit identischen Residuen liefern.\n        Referenzwerte: Newton 3 Iter / 3.16e-11, BroydenSparse ~9ms.\n      </div>'
     '<div class="note green" data-lang="en">\n        <strong>As a regression baseline:</strong> SimpleSystem.cas is the reference system\n        for all solver tests. After any code change, <code>-TEST</code> on this model\n        must produce identical residuals from all seven solvers.\n        Reference values: Newton 3 iter / 3.16e-11, BroydenSparse ~9ms.\n      </div>')

# ── NozzleSystem section ──
pair('<span class="badge b-warn">303 Gleichungen · 400+ Variablen · κ ~ 10²³</span>',
     '<span class="badge b-warn" data-lang="de">303 Gleichungen · 400+ Variablen · κ ~ 10²³</span>'
     '<span class="badge b-warn" data-lang="en">303 equations · 400+ variables · κ ~ 10²³</span>')

# What is modeled (Nozzle)
pair('<p>Ein vollständiges aerothermodynamisches Modell einer Schubdüse (Nozzle)\n      mit Mischer und Jetpipe. Das Modell berechnet Strömungsgrößen in mehreren\n      Stationen (F060, F080, F090, ...) vom Kerngasstrom über den Bypass bis\n      zum Düsenaustritt. Kerngrößen: Totaldruck, Totaltemperatur, Massenstrom,\n      statischer Druck, Machzahl, spezifische Wärme, Isentropenexponent.</p>',
     '<p data-lang="de">Ein vollständiges aerothermodynamisches Modell einer Schubdüse (Nozzle)\n      mit Mischer und Jetpipe. Das Modell berechnet Strömungsgrößen in mehreren\n      Stationen (F060, F080, F090, ...) vom Kerngasstrom über den Bypass bis\n      zum Düsenaustritt. Kerngrößen: Totaldruck, Totaltemperatur, Massenstrom,\n      statischer Druck, Machzahl, spezifische Wärme, Isentropenexponent.</p>'
     '<p data-lang="en">A complete aerothermodynamic model of a thrust nozzle with mixer and jet pipe.\n      The model computes flow quantities at several stations (F060, F080, F090, …)\n      from the core flow through the bypass to the nozzle exit. Key quantities: total\n      pressure, total temperature, mass flow, static pressure, Mach number, specific\n      heat, isentropic exponent.</p>')

# Modellstruktur table headers
pair('<thead><tr><th>Bereich</th><th>Variablen-Prefix</th><th>Inhalt</th></tr></thead>',
     '<thead><tr>'
     '<th data-lang="de">Bereich</th><th data-lang="en">Area</th>'
     '<th data-lang="de">Variablen-Prefix</th><th data-lang="en">Variable prefix</th>'
     '<th data-lang="de">Inhalt</th><th data-lang="en">Content</th>'
     '</tr></thead>')

# Modellstruktur rows
td_pair('Global', 'Global')
td_pair('Konstanten (π, R_univ, Schalter)', 'Constants (π, R_univ, switches)')
td_pair('Geometrie', 'Geometry')
td_pair('Radien, Längen, Flächen', 'Radii, lengths, areas')
td_pair('Atmosphäre', 'Atmosphere')
td_pair('ISA-Bedingungen, Gaszusammensetzung', 'ISA conditions, gas composition')
td_pair('Kerngasstrom', 'Core flow')
td_pair('Station 060: Eintritt Kerngasstrom', 'Station 060: core flow inlet')
td_pair('Bypass', 'Bypass')
td_pair('Station 080: Bypass-Strom', 'Station 080: bypass flow')
td_pair('Mischer', 'Mixer')
td_pair('Station 090: nach Mischung', 'Station 090: after mixing')
td_pair('Düsenaustritt', 'Nozzle exit')
td_pair('Station 100: Düsenaustritt', 'Station 100: nozzle exit')
td_pair('Gesamtmodell', 'Full model')
td_pair('Schub, Schallgeschwindigkeit, Durchfluss', 'Thrust, speed of sound, mass flow')

# Warum ist dieses Modell schwierig - table
pair('<thead><tr><th>Ursache</th><th>Auswirkung</th></tr></thead>',
     '<thead><tr>'
     '<th data-lang="de">Ursache</th><th data-lang="en">Cause</th>'
     '<th data-lang="de">Auswirkung</th><th data-lang="en">Effect</th>'
     '</tr></thead>')

td_pair('Konditionszahl κ ~ 10²³', 'Condition number κ ~ 10²³')
td_pair('Druck in Pa (10⁵) und dimensionslose Größen (10⁻³) nebeneinander — riesige Spanne',
        'Pressure in Pa (10⁵) and dimensionless quantities (10⁻³) side by side — huge span')
td_pair('JANAF-Polynome als Built-in Funktionen',
        'JANAF polynomials as built-in functions')
td_pair('Numerische Ableitungen statt symbolischer — leicht mehr Fehler in der Jacobi',
        'Numerical derivatives instead of symbolic — slightly more error in the Jacobian')
td_pair('MofCondiRatio nahe Ma=1', 'MofCondiRatio near Ma=1')
td_pair('Funktion hat vertikale Tangente bei Ma=1 — Jacobi-Singularität möglich',
        'Function has a vertical tangent at Ma=1 — Jacobian singularity possible')
td_pair('Starke Kopplung aller Stationen', 'Strong coupling between all stations')
td_pair('Jede Gleichung hängt von vielen anderen ab — dichte Jacobi trotz Sparse-Struktur',
        'Each equation depends on many others — dense Jacobian despite sparse structure')

# Solver-Empfehlung pre comments
pair('<span class="cmt">// Empfohlen: Newton-Sparse-Armijo mit Diagnose-Modus</span>',
     '<span class="cmt" data-lang="de">// Empfohlen: Newton-Sparse-Armijo mit Diagnose-Modus</span>'
     '<span class="cmt" data-lang="en">// Recommended: Newton-Sparse-Armijo with diagnostic mode</span>')
pair('<span class="cmt">// Falls Newton nicht konvergiert: Levenberg-Marquardt</span>',
     '<span class="cmt" data-lang="de">// Falls Newton nicht konvergiert: Levenberg-Marquardt</span>'
     '<span class="cmt" data-lang="en">// If Newton does not converge: Levenberg-Marquardt</span>')
pair('<span class="cmt">// Bei κ-Warnungen und LM-Problemen: Homotopie kritisch</span>',
     '<span class="cmt" data-lang="de">// Bei κ-Warnungen und LM-Problemen: Homotopie kritisch</span>'
     '<span class="cmt" data-lang="en">// On κ warnings and LM issues: homotopy critical</span>')

# Note amber - bekanntes Problem
pair('<div class="note amber">\n        <strong>Bekanntes Problem:</strong> Das NozzleSystem_4_fixed konvergiert\n        mit Newton und LM bei guten Startwerten. Homotopie zeigt bei diesem Modell\n        Stagnationsverhalten — Verbesserung durch echten Tangenten-Prädiktor geplant\n        (Roadmap R-03). Bei Konvergenzproblemen zuerst <code>-DI</code> versuchen\n        und Startwerte in der <code>-U:</code>-Datei manuell setzen.\n      </div>',
     '<div class="note amber" data-lang="de">\n        <strong>Bekanntes Problem:</strong> Das NozzleSystem_4_fixed konvergiert\n        mit Newton und LM bei guten Startwerten. Homotopie zeigt bei diesem Modell\n        Stagnationsverhalten — Verbesserung durch echten Tangenten-Prädiktor geplant\n        (Roadmap R-03). Bei Konvergenzproblemen zuerst <code>-DI</code> versuchen\n        und Startwerte in der <code>-U:</code>-Datei manuell setzen.\n      </div>'
     '<div class="note amber" data-lang="en">\n        <strong>Known issue:</strong> NozzleSystem_4_fixed converges with Newton and LM\n        given good starting values. Homotopy shows stagnation on this model — improvement\n        via a true tangent predictor is planned (Roadmap R-03). On convergence issues,\n        try <code>-DI</code> first and set starting values manually in the <code>-U:</code> file.\n      </div>')

# ── Eigenes Modell section ──
pair('<p>Empfohlene Vorgehensweise beim Aufbau eines neuen CAS-Modells:</p>',
     '<p data-lang="de">Empfohlene Vorgehensweise beim Aufbau eines neuen CAS-Modells:</p>'
     '<p data-lang="en">Recommended approach for building a new CAS model:</p>')

# Steps table headers
pair('<thead><tr><th>Schritt</th><th>Aktion</th><th>Tipp</th></tr></thead>',
     '<thead><tr>'
     '<th data-lang="de">Schritt</th><th data-lang="en">Step</th>'
     '<th data-lang="de">Aktion</th><th data-lang="en">Action</th>'
     '<th data-lang="de">Tipp</th><th data-lang="en">Tip</th>'
     '</tr></thead>')

# Steps content
td_pair('Variablen definieren — erst alle Fixed, dann Free',
        'Define variables — first all Fixed, then Free')
td_pair('Beginne mit physikalisch bekannten Größen als Fixed. Nur was wirklich unbekannt ist als Free.',
        'Start with physically known quantities as Fixed. Only what is truly unknown becomes Free.')
td_pair('Gleichgewicht prüfen: n Gleichungen = n Freie',
        'Check balance: n equations = n free variables')
td_pair('<code>-I:model.cas -TEST</code> zeigt Systemgröße. Zu viele Gleichungen → System überbestimmt.',
        '<code>-I:model.cas -TEST</code> shows system size. Too many equations → overdetermined system.')
td_pair('Startwerte physikalisch sinnvoll wählen',
        'Choose physically sensible starting values')
td_pair('Schlechte Startwerte sind häufigste Konvergenz-Ursache. Mit <code>-DI</code> automatisch verbessern.',
        'Poor starting values are the most common cause of non-convergence. Improve them automatically with <code>-DI</code>.')
td_pair('Bounds setzen', 'Set bounds')
td_pair('Lower/Upper sollten physikalisch sinnvoll sein — PhysicalProjector verhindert negative Drücke etc.',
        'Lower/Upper should be physically sensible — PhysicalProjector prevents negative pressures etc.')
td_pair('Mit Newton-Sparse-Armijo testen', 'Test with Newton-Sparse-Armijo')
td_pair('Konvergiert meist in 3–10 Iterationen bei gut formulierten Systemen.',
        'Usually converges in 3–10 iterations on well-formulated systems.')
td_pair('Falls nicht konvergiert: Diagnose', 'If not converged: diagnose')
td_pair('Log nach κ-Warnungen durchsuchen. <code>-DV:start.txt</code> Startvektor inspizieren.',
        'Search the log for κ warnings. Inspect the starting vector with <code>-DV:start.txt</code>.')
td_pair('Batch-Parameterstudie', 'Batch parameter study')
td_pair('CSV-Datei mit Betriebspunkten → <code>-I:studie.csv</code>. BroydenSparse für schnelle Serien.',
        'CSV file with operating points → <code>-I:studie.csv</code>. BroydenSparse for fast series.')

# Starter template comments
pair('<span class="cmt">// template.cas — Minimal-Vorlage für ein neues Modell</span>',
     '<span class="cmt" data-lang="de">// template.cas — Minimal-Vorlage für ein neues Modell</span>'
     '<span class="cmt" data-lang="en">// template.cas — minimal template for a new model</span>')
pair('<span class="cmt">// ── Fixierte Eingangsgrößen ────────────────────────────</span>',
     '<span class="cmt" data-lang="de">// ── Fixierte Eingangsgrößen ────────────────────────────</span>'
     '<span class="cmt" data-lang="en">// ── Fixed input quantities ─────────────────────────────</span>')
pair('<span class="cmt">// ── Unbekannte (freie Variablen) ───────────────────────</span>',
     '<span class="cmt" data-lang="de">// ── Unbekannte (freie Variablen) ───────────────────────</span>'
     '<span class="cmt" data-lang="en">// ── Unknowns (free variables) ─────────────────────────</span>')
pair('<span class="cmt">// ── Gleichungen (n frei = n Gleichungen) ───────────────</span>',
     '<span class="cmt" data-lang="de">// ── Gleichungen (n frei = n Gleichungen) ───────────────</span>'
     '<span class="cmt" data-lang="en">// ── Equations (n free = n equations) ──────────────────</span>')
pair('<span class="cmt">// Gleichung 1</span>',
     '<span class="cmt" data-lang="de">// Gleichung 1</span>'
     '<span class="cmt" data-lang="en">// Equation 1</span>')
pair('<span class="cmt">// Gleichung 2</span>',
     '<span class="cmt" data-lang="de">// Gleichung 2</span>'
     '<span class="cmt" data-lang="en">// Equation 2</span>')
pair('<span class="cmt">// Aufruf:</span>',
     '<span class="cmt" data-lang="de">// Aufruf:</span>'
     '<span class="cmt" data-lang="en">// Invocation:</span>')

# Description strings inside template
pair('Description: <span class="str">"Eingangsgröße A"</span>',
     '<span data-lang="de">Description: <span class="str">"Eingangsgröße A"</span></span>'
     '<span data-lang="en">Description: <span class="str">"Input A"</span></span>')
pair('Description: <span class="str">"Eingangsgröße B"</span>',
     '<span data-lang="de">Description: <span class="str">"Eingangsgröße B"</span></span>'
     '<span data-lang="en">Description: <span class="str">"Input B"</span></span>')
pair('Description: <span class="str">"Unbekannte X"</span>, Lower: 0, Value: 50',
     '<span data-lang="de">Description: <span class="str">"Unbekannte X"</span></span>'
     '<span data-lang="en">Description: <span class="str">"Unknown X"</span></span>, Lower: 0, Value: 50')
pair('Description: <span class="str">"Unbekannte Y"</span>, Lower: 200',
     '<span data-lang="de">Description: <span class="str">"Unbekannte Y"</span></span>'
     '<span data-lang="en">Description: <span class="str">"Unknown Y"</span></span>, Lower: 200')

# ── Footer ──
pair('<span>CMDSolver Docs · Beispielmodelle · v2.5</span>',
     '<span data-lang="de">CMDSolver Docs · Beispielmodelle · v2.5</span>'
     '<span data-lang="en">CMDSolver Docs · Example Models · v2.5</span>')
pair('<a href="api_reference.html">← API-Referenz</a>',
     '<a href="api_reference.html" data-lang="de">← API-Referenz</a>'
     '<a href="api_reference.html" data-lang="en">← API Reference</a>')
pair('<a href="troubleshooting.html">Troubleshooting →</a>',
     '<a href="troubleshooting.html" data-lang="de">Troubleshooting →</a>'
     '<a href="troubleshooting.html" data-lang="en">Troubleshooting →</a>')

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
