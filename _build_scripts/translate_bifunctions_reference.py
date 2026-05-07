#!/usr/bin/env python3
"""Translate bifunctions_reference.html body to bilingual DE/EN."""
from pathlib import Path

p = Path('/home/claude/build/bifunctions_reference.html')
html = p.read_text(encoding='utf-8')

REPS = []
def pair(old, new): REPS.append((old, new))

# ── Nav ──
NAV = [
    ('architektur', 'Architektur', 'Architecture'),
    ('ableitung', 'Ableitungsmethodik', 'Differentiation'),
    ('schall', 'Schallgeschwindigkeit', 'Speed of Sound'),
    ('enthalpie', 'Enthalpie & cp', 'Enthalpy & cp'),
    ('atmosphaere', 'Atmosphäre', 'Atmosphere'),
    ('stroemung', 'Strömung', 'Flow'),
    ('verwendung', 'CAS-Verwendung', 'CAS Usage'),
]
for anchor, de, en in NAV:
    pair(f'<a href="#{anchor}">{de}</a>',
         f'<a href="#{anchor}" data-lang="de">{de}</a>'
         f'<a href="#{anchor}" data-lang="en">{en}</a>')

# ── h2 ──
def h2(de, en):
    pair(f'<h2>{de}</h2>',
         f'<h2 data-lang="de">{de}</h2><h2 data-lang="en">{en}</h2>')

h2('Architektur der Built-in Funktionen', 'Architecture of Built-in Functions')
h2('Ableitungsmethodik — 5-Punkte-Formel', 'Differentiation — 5-Point Formula')
h2('Schallgeschwindigkeits-Funktionen', 'Speed-of-Sound Functions')
h2('Enthalpie- und cp-Funktionen', 'Enthalpy and cp Functions')
h2('Atmosphärenmodell — ISA', 'Atmosphere Model — ISA')
h2('Strömungsmechanische Funktionen', 'Flow-mechanics Functions')
h2('CAS-Verwendung — PROCEDURE und CALL', 'CAS Usage — PROCEDURE and CALL')

# ── h3 ──
def h3(de, en):
    pair(f'<h3>{de}</h3>',
         f'<h3 data-lang="de">{de}</h3><h3 data-lang="en">{en}</h3>')

h3('Beispiel — cpOfTNOZ', 'Example — cpOfTNOZ')
h3('Vergleich: symbolisch vs. numerisch', 'Comparison: symbolic vs. numerical')
h3('JANAF-Polynome', 'JANAF polynomials')
h3('Vollständiges Prozedurenbeispiel', 'Complete procedure example')

# ── Helper for cmt comments ──
def cmt(de, en):
    pair(f'<span class="cmt">{de}</span>',
         f'<span class="cmt" data-lang="de">{de}</span>'
         f'<span class="cmt" data-lang="en">{en}</span>')

# ── Helper for hi labels in math-block ──
def hi(de, en):
    pair(f'<span class="hi">{de}</span>',
         f'<span class="hi" data-lang="de">{de}</span>'
         f'<span class="hi" data-lang="en">{en}</span>')

# ── Helper for func-card descriptions and arg lists ──
def func_desc(de_inner, en_inner):
    pair(f'<div class="func-desc">\n      {de_inner}\n    </div>',
         f'<div class="func-desc" data-lang="de">\n      {de_inner}\n    </div>'
         f'<div class="func-desc" data-lang="en">\n      {en_inner}\n    </div>')

# ── Architecture section ──
pair('<p>\n    Jede thermodynamische Funktion <code>func(args)</code> in BIfunctions hat\n    <strong>drei Signaturen</strong> die zusammen das Interface für den Solver bilden:\n  </p>',
     '<p data-lang="de">\n    Jede thermodynamische Funktion <code>func(args)</code> in BIfunctions hat\n    <strong>drei Signaturen</strong> die zusammen das Interface für den Solver bilden:\n  </p>'
     '<p data-lang="en">\n    Every thermodynamic function <code>func(args)</code> in BIfunctions has\n    <strong>three signatures</strong> that together form the solver interface:\n  </p>')

hi('Signatur 1 — Residuum:', 'Signature 1 — residual:')
hi('Signatur 2 — List-Form:', 'Signature 2 — list form:')
hi('Signatur 3 — Partielle Ableitung:', 'Signature 3 — partial derivative:')

cmt('  // Gibt 0 wenn output korrekt berechnet wurde',
    '  // Returns 0 when output is correctly computed')
cmt('  // Wird als Gleichungsresiduum F(x) = 0 verwendet',
    '  // Used as equation residual F(x) = 0')
cmt('  // Wrapper für EqnData-Aufruf via Reflection',
    '  // Wrapper for EqnData invocation via reflection')
cmt('  // Numerische Ableitung ∂(dFunc)/∂x_partial',
    '  // Numerical derivative ∂(dFunc)/∂x_partial')
cmt('  // Verwendet 5-Punkte-Formel, O(h⁴) Genauigkeit',
    '  // Uses 5-point formula, O(h⁴) accuracy')

pair('<div class="note blue">\n    <strong>Warum diese Struktur?</strong> Der Solver braucht für jede Gleichung\n    zwei Dinge: das Residuum F(x) und die Ableitungen ∂F/∂xᵢ für die Jacobi-Matrix.\n    Für Built-in Funktionen kann CASprzak nicht symbolisch differenzieren —\n    daher numerische Ableitungen via <code>funcDeriv</code>.\n  </div>',
     '<div class="note blue" data-lang="de">\n    <strong>Warum diese Struktur?</strong> Der Solver braucht für jede Gleichung\n    zwei Dinge: das Residuum F(x) und die Ableitungen ∂F/∂xᵢ für die Jacobi-Matrix.\n    Für Built-in Funktionen kann CASprzak nicht symbolisch differenzieren —\n    daher numerische Ableitungen via <code>funcDeriv</code>.\n  </div>'
     '<div class="note blue" data-lang="en">\n    <strong>Why this structure?</strong> The solver needs two things per\n    equation: the residual F(x) and the derivatives ∂F/∂xᵢ for the Jacobian.\n    For built-in functions, CASprzak cannot differentiate symbolically —\n    hence numerical derivatives via <code>funcDeriv</code>.\n  </div>')

cmt('// Residuum: cp - cpOfTNOZ(T, WGR, FAR) = 0',
    '// Residual: cp - cpOfTNOZ(T, WGR, FAR) = 0')
cmt('// In der CAS-Datei:', '// In the CAS file:')

# ── Differentiation section ──
pair('<p>\n    Alle partiellen Ableitungen der Built-in Funktionen werden <strong>numerisch</strong>\n    berechnet — nicht symbolisch wie bei normalen CAS-Gleichungen. Dies ist nötig\n    weil die thermodynamischen Polynome zu komplex für automatische Differentiation sind.\n  </p>',
     '<p data-lang="de">\n    Alle partiellen Ableitungen der Built-in Funktionen werden <strong>numerisch</strong>\n    berechnet — nicht symbolisch wie bei normalen CAS-Gleichungen. Dies ist nötig\n    weil die thermodynamischen Polynome zu komplex für automatische Differentiation sind.\n  </p>'
     '<p data-lang="en">\n    All partial derivatives of built-in functions are computed\n    <strong>numerically</strong> — not symbolically like normal CAS equations.\n    This is necessary because the thermodynamic polynomials are too complex for\n    automatic differentiation.\n  </p>')

hi('5-Punkte-Formel (O(h⁴) Genauigkeit):', '5-point formula (O(h⁴) accuracy):')
hi('Adaptive Schrittweite:', 'Adaptive step size:')

cmt('  // Relativ zur Variablengröße — vermeidet Auslöschung',
    '  // Relative to variable magnitude — avoids cancellation')
cmt('  // Bei x = 200000 Pa: h ≈ 2 Pa  (sinnvolle Schrittweite)',
    '  // For x = 200000 Pa: h ≈ 2 Pa  (sensible step)')
cmt('  // Bei x = 0.001:    h ≈ 1e-8   (absolute Untergrenze)',
    '  // For x = 0.001:    h ≈ 1e-8   (absolute lower bound)')

pair('<div class="note green">\n    <strong>Genauigkeit:</strong> Die 5-Punkte-Formel hat einen Fehler von O(h⁴) —\n    bei h=1e-5·x ist der Ableitungsfehler typisch unter 1e-10 relativ.\n    Das ist ausreichend für Newton-Konvergenz bis fsum ~ 1e-9.\n  </div>',
     '<div class="note green" data-lang="de">\n    <strong>Genauigkeit:</strong> Die 5-Punkte-Formel hat einen Fehler von O(h⁴) —\n    bei h=1e-5·x ist der Ableitungsfehler typisch unter 1e-10 relativ.\n    Das ist ausreichend für Newton-Konvergenz bis fsum ~ 1e-9.\n  </div>'
     '<div class="note green" data-lang="en">\n    <strong>Accuracy:</strong> the 5-point formula has an error of O(h⁴) —\n    at h=1e-5·x the derivative error is typically below 1e-10 relative.\n    Sufficient for Newton convergence down to fsum ~ 1e-9.\n  </div>')

# Comparison table
pair('<thead><tr><th>Aspekt</th><th>Symbolisch (CASprzak)</th><th>Numerisch (BIfunctions)</th></tr></thead>',
     '<thead><tr>'
     '<th data-lang="de">Aspekt</th><th data-lang="en">Aspect</th>'
     '<th data-lang="de">Symbolisch (CASprzak)</th><th data-lang="en">Symbolic (CASprzak)</th>'
     '<th data-lang="de">Numerisch (BIfunctions)</th><th data-lang="en">Numerical (BIfunctions)</th>'
     '</tr></thead>')

def td_pair(de, en):
    pair(f'<td>{de}</td>', f'<td data-lang="de">{de}</td><td data-lang="en">{en}</td>')

td_pair('Genauigkeit', 'Accuracy')
td_pair('Exakt (Maschinengenauigkeit)', 'Exact (machine precision)')
td_pair('O(h⁴) ≈ 1e-15 relativ', 'O(h⁴) ≈ 1e-15 relative')
td_pair('Geschwindigkeit', 'Speed')
td_pair('Schnell (direkte Auswertung)', 'Fast (direct evaluation)')
td_pair('4 Funktionsauswertungen pro Ableitung',
        '4 function evaluations per derivative')
td_pair('Anwendbar auf', 'Applicable to')
td_pair('Algebraische Ausdrücke', 'Algebraic expressions')
td_pair('Beliebige stetige Funktionen', 'Arbitrary continuous functions')
td_pair('Verwendung in CMDSolver', 'Use in CMDSolver')
td_pair('Alle normalen Gleichungen', 'All ordinary equations')
td_pair('Nur CALL-Gleichungen (BIfunctions)', 'CALL equations only (BIfunctions)')

# ── Speed-of-Sound section ──
pair('<p>\n    Die Schallgeschwindigkeit in Luft/Abgas hängt von Temperatur, Druck und\n    Gaszusammensetzung ab. CMDSolver verwendet JANAF-Polynome für die\n    thermodynamischen Eigenschaften als Basis.\n  </p>',
     '<p data-lang="de">\n    Die Schallgeschwindigkeit in Luft/Abgas hängt von Temperatur, Druck und\n    Gaszusammensetzung ab. CMDSolver verwendet JANAF-Polynome für die\n    thermodynamischen Eigenschaften als Basis.\n  </p>'
     '<p data-lang="en">\n    The speed of sound in air/exhaust depends on temperature, pressure, and\n    gas composition. CMDSolver uses JANAF polynomials as the basis for\n    thermodynamic properties.\n  </p>')

hi('Schallgeschwindigkeit (allgemein):', 'Speed of sound (general):')
hi('JANAF-basierte Berechnung:', 'JANAF-based computation:')

cmt('  // κ = cp/cv = Isentropenexponent', '  // κ = cp/cv = isentropic exponent')
cmt('  // R = spezifische Gaskonstante [J/kgK]',
    '  // R = specific gas constant [J/kgK]')
cmt('  // T = Temperatur [K]', '  // T = temperature [K]')

# Note: "Polynom in T" appears in eq, not cmt — translate via direct replacement
pair('<div class="eq">  cp(T) = Σ aᵢ · Tⁱ   (Polynom in T)</div>',
     '<div class="eq" data-lang="de">  cp(T) = Σ aᵢ · Tⁱ   (Polynom in T)</div>'
     '<div class="eq" data-lang="en">  cp(T) = Σ aᵢ · Tⁱ   (polynomial in T)</div>')
pair('<div class="eq">  a(T, p, Zusammensetzung) = √(κ · R · T)</div>',
     '<div class="eq" data-lang="de">  a(T, p, Zusammensetzung) = √(κ · R · T)</div>'
     '<div class="eq" data-lang="en">  a(T, p, composition) = √(κ · R · T)</div>')

# func-card descriptions for speed-of-sound
func_desc('Schallgeschwindigkeit <strong>trockener Luft</strong> basierend auf JANAF-Thermodynamik.\n      Berücksichtigt die vollständige Gaszusammensetzung (N₂, O₂, Ar, CO₂, Ne, He, CH₄, Kr, H₂, N₂O, Xe).',
          'Speed of sound for <strong>dry air</strong>, based on JANAF thermodynamics.\n      Accounts for the full gas composition (N₂, O₂, Ar, CO₂, Ne, He, CH₄, Kr, H₂, N₂O, Xe).')

func_desc('Schallgeschwindigkeit <strong>feuchter Luft</strong> — wie softdryJANAF\n      plus Wasseranteil fH2O. Relevant für Einlaufbedingungen mit Luftfeuchtigkeit.',
          'Speed of sound for <strong>moist air</strong> — like softdryJANAF\n      plus water fraction fH2O. Relevant for inlet conditions with humidity.')

func_desc('Schallgeschwindigkeit <strong>heißer Abgase</strong> (nach Verbrennung).\n      Verwendet separate JANAF-Koeffizienten für den Hochtemperaturbereich (T > 1000K).',
          'Speed of sound for <strong>hot exhaust gases</strong> (post-combustion).\n      Uses separate JANAF coefficients for the high-temperature regime (T > 1000K).')

# func-args entries — only translate where there is German text
def dt_dd(de_inner, en_inner):
    """Translate a single <dt>x</dt><dd>...</dd> pair where DD has German text."""
    pair(f'<dd>{de_inner}</dd>',
         f'<dd data-lang="de">{de_inner}</dd>'
         f'<dd data-lang="en">{en_inner}</dd>')

dt_dd('Ausgabevariable: Schallgeschwindigkeit [m/s]',
      'Output variable: speed of sound [m/s]')
# These appear multiple times (Temperatur [K], Totaldruck [Pa], etc.) — handle each occurrence
dt_dd('Temperatur [K]', 'Temperature [K]')
dt_dd('Totaldruck [Pa]', 'Total pressure [Pa]')
dt_dd('Molenbrüche der Gaskomponenten [−]',
      'Mole fractions of gas components [−]')

# ── Enthalpy section ──
pair('<p>\n    JANAF (Joint Army-Navy-Air Force) Thermochemische Tabellen liefern\n    Polynomkoeffizienten für thermodynamische Eigenschaften von Gasen in\n    Abhängigkeit von der Temperatur. CMDSolver verwendet diese für cp(T) und h(T).\n  </p>',
     '<p data-lang="de">\n    JANAF (Joint Army-Navy-Air Force) Thermochemische Tabellen liefern\n    Polynomkoeffizienten für thermodynamische Eigenschaften von Gasen in\n    Abhängigkeit von der Temperatur. CMDSolver verwendet diese für cp(T) und h(T).\n  </p>'
     '<p data-lang="en">\n    JANAF (Joint Army-Navy-Air Force) Thermochemical Tables provide polynomial\n    coefficients for the temperature-dependent thermodynamic properties of\n    gases. CMDSolver uses these for cp(T) and h(T).\n  </p>')

hi('JANAF cp-Polynom:', 'JANAF cp polynomial:')
hi('JANAF Enthalpie:', 'JANAF enthalpy:')
hi('Gemischung (mehrere Gaskomponenten):', 'Mixing (multiple gas components):')

cmt('  // a₆ = Integrationskonstante (Bildungsenthalpie)',
    '  // a₆ = integration constant (enthalpy of formation)')

pair('<div class="eq">  cp_mix(T) = Σᵢ fᵢ · cpᵢ(T)   (massengewichtetes Mittel)</div>',
     '<div class="eq" data-lang="de">  cp_mix(T) = Σᵢ fᵢ · cpᵢ(T)   (massengewichtetes Mittel)</div>'
     '<div class="eq" data-lang="en">  cp_mix(T) = Σᵢ fᵢ · cpᵢ(T)   (mass-weighted average)</div>')

# func-card descriptions
func_desc('Spezifische Wärmekapazität cp bei gegebener Temperatur und Gaszusammensetzung\n      (einschließlich Wasser). JANAF-Polynome, gültig für T = 200K bis 6000K.',
          'Specific heat capacity cp for given temperature and gas composition\n      (including water). JANAF polynomials, valid for T = 200K to 6000K.')

dt_dd('Ausgabe: cp [J/kgK]', 'Output: cp [J/kgK]')
dt_dd('Molenbrüche [−]', 'Mole fractions [−]')

func_desc('cp für Triebwerksanwendungen — vereinfachtes Polynom mit Wassergehalt (wgr)\n      und Kraftstoff-Luft-Verhältnis (far). Schneller als vollständiges JANAF,\n      optimiert für den Temperaturbereich 200K–1500K.',
          'cp for engine applications — simplified polynomial with water content (wgr)\n      and fuel-air ratio (far). Faster than full JANAF, optimized for the\n      temperature range 200K–1500K.')

dt_dd('Water-Gas-Ratio [−]', 'Water-gas ratio [−]')
dt_dd('Fuel-Air-Ratio [−]', 'Fuel-air ratio [−]')

func_desc('cp für Düsenanwendungen — separates Polynom optimiert für die Bedingungen\n      in Schubdüsen (hohe Temperaturen, Verbrennungsprodukte). Unterschiedliche\n      Polynomkoeffizienten oberhalb und unterhalb 1000K.',
          'cp for nozzle applications — separate polynomial optimized for thrust-nozzle\n      conditions (high temperatures, combustion products). Different polynomial\n      coefficients above and below 1000K.')

func_desc('Spezifische Enthalpie h(T) für feuchte Luft/Abgasgemisch via JANAF-Integration.\n      Referenztemperatur: 0K (absolute Enthalpie).',
          'Specific enthalpy h(T) for moist air / exhaust mixture via JANAF integration.\n      Reference temperature: 0K (absolute enthalpy).')

func_desc('Enthalpie feuchter Luft einschließlich Verdampfungsenthalpie des Wassers.\n      Berücksichtigt den Phasenübergang Wasser ↔ Wasserdampf.',
          'Enthalpy of moist air including the enthalpy of vaporization of water.\n      Accounts for the water ↔ water-vapor phase transition.')

func_desc('Kraftstoff-Enthalpie als Funktion von Temperatur, Referenztemperatur\n      und Kraftstoffzusammensetzung (Kohlenstoff- fC und Wasserstoffanteil fH).\n      Basiert auf JANAF-Daten für Kohlenwasserstoffe.',
          'Fuel enthalpy as a function of temperature, reference temperature, and\n      fuel composition (carbon fraction fC and hydrogen fraction fH).\n      Based on JANAF data for hydrocarbons.')

func_desc('Sättigungsdampfdruck als Funktion von Temperatur und Wasseranteil.\n      Verwendet die Antoine-Gleichung für H₂O:',
          'Saturation vapor pressure as a function of temperature and water fraction.\n      Uses the Antoine equation for H₂O:')

pair('<div class="eq">p_sat(T) = exp(A − B/(C + T))   [Antoine-Gleichung]</div>',
     '<div class="eq" data-lang="de">p_sat(T) = exp(A − B/(C + T))   [Antoine-Gleichung]</div>'
     '<div class="eq" data-lang="en">p_sat(T) = exp(A − B/(C + T))   [Antoine equation]</div>')

cmt('// Koeffizienten A, B, C aus NIST-Datenbank',
    '// Coefficients A, B, C from the NIST database')

# ── Atmosphere section ──
pair('<p>\n    Das International Standard Atmosphere (ISA) Modell beschreibt Temperatur\n    und Druck als Funktion der Höhe. CMDSolver implementiert das vollständige\n    ISA-Modell bis 80km Höhe mit 9 Schichten.\n  </p>',
     '<p data-lang="de">\n    Das International Standard Atmosphere (ISA) Modell beschreibt Temperatur\n    und Druck als Funktion der Höhe. CMDSolver implementiert das vollständige\n    ISA-Modell bis 80km Höhe mit 9 Schichten.\n  </p>'
     '<p data-lang="en">\n    The International Standard Atmosphere (ISA) model describes temperature\n    and pressure as a function of altitude. CMDSolver implements the full ISA\n    model up to 80 km altitude with 9 layers.\n  </p>')

hi('ISA Temperaturprofil (schichtenweise):', 'ISA temperature profile (layer-wise):')
hi('ISA Druckprofil:', 'ISA pressure profile:')
hi('ISA + ΔTISA (Temperaturabweichung vom Standard):',
   'ISA + ΔTISA (deviation from standard):')

# math-block eq with German inline
pair('<div class="eq">  In Gradientschichten (βⱼ ≠ 0):</div>',
     '<div class="eq" data-lang="de">  In Gradientschichten (βⱼ ≠ 0):</div>'
     '<div class="eq" data-lang="en">  In gradient layers (βⱼ ≠ 0):</div>')
pair('<div class="eq">  In Isothermschichten (βⱼ = 0):</div>',
     '<div class="eq" data-lang="de">  In Isothermschichten (βⱼ = 0):</div>'
     '<div class="eq" data-lang="en">  In isothermal layers (βⱼ = 0):</div>')

# ISA layer table
pair('<thead><tr><th>Schicht</th><th>Höhe [km]</th><th>β [K/km]</th><th>Bezeichnung</th></tr></thead>',
     '<thead><tr>'
     '<th data-lang="de">Schicht</th><th data-lang="en">Layer</th>'
     '<th data-lang="de">Höhe [km]</th><th data-lang="en">Altitude [km]</th>'
     '<th>β [K/km]</th>'
     '<th data-lang="de">Bezeichnung</th><th data-lang="en">Name</th>'
     '</tr></thead>')

td_pair('Troposphäre', 'Troposphere')
td_pair('Untere Stratosphäre (isotherm)', 'Lower stratosphere (isothermal)')
td_pair('Mittlere Stratosphäre', 'Middle stratosphere')
td_pair('Obere Stratosphäre', 'Upper stratosphere')
td_pair('Stratopause (isotherm)', 'Stratopause (isothermal)')
td_pair('Untere Mesosphäre', 'Lower mesosphere')
td_pair('Obere Mesosphäre', 'Upper mesosphere')

func_desc('ISA-Temperatur als Funktion der Höhe. Berücksichtigt alle 9 ISA-Schichten.',
          'ISA temperature as a function of altitude. Covers all 9 ISA layers.')

dt_dd('Ausgabe: Temperatur [K]', 'Output: temperature [K]')
dt_dd('Flughöhe [m]', 'Flight altitude [m]')
dt_dd('Temperaturabweichung vom ISA-Standard [K] (0 = ISA-Standard)',
      'Temperature offset from ISA standard [K] (0 = ISA standard)')

func_desc('ISA-Druck als Funktion der Höhe und Temperaturabweichung.\n      Verwendet die barometrische Höhenformel schichtenweise.',
          'ISA pressure as a function of altitude and temperature offset.\n      Uses the barometric formula layer by layer.')

dt_dd('Ausgabe: Druck [Pa]', 'Output: pressure [Pa]')
dt_dd('Flughöhe [m]', 'Flight altitude [m]')
dt_dd('Temperaturabweichung [K]', 'Temperature offset [K]')
dt_dd('Spezifische Gaskonstante [J/kgK] (Luft: 287.058)',
      'Specific gas constant [J/kgK] (air: 287.058)')

func_desc('Relative Luftfeuchtigkeit als Funktion der Höhe — standardmäßiges\n      Atmosphärenprofil für Feuchtemodelle.',
          'Relative humidity as a function of altitude — standard atmospheric\n      profile for humidity models.')

# ── Flow section ──
func_desc('Machzahl aus dem Flächenverhältnis A/A* (Kanaldivergenz-Verhältnis).\n      Löst die isentrope Durchflussgleichung numerisch.',
          'Mach number from the area ratio A/A* (channel divergence ratio).\n      Solves the isentropic flow equation numerically.')

hi('Isentrope Durchflussgleichung:', 'Isentropic flow equation:')
cmt('  // Wird nach Ma aufgelöst (numerisch, da transzendent)',
    '  // Solved for Ma (numerically, since transcendental)')

dt_dd('Ausgabe: Machzahl [−]', 'Output: Mach number [−]')
dt_dd('Flächenverhältnis A/A* [−]', 'Area ratio A/A* [−]')
dt_dd('Isentropenexponent κ = cp/cv [−]', 'Isentropic exponent κ = cp/cv [−]')

pair('<div class="note blue">\n    <strong>Bedeutung für Düsenmodelle:</strong> MofCondiRatio ist zentral für\n    alle konvergent-divergenten Düsenberechnungen (Laval-Düse). Das Flächenverhältnis\n    bestimmt eindeutig die Machzahl — bis auf die Zweideutigkeit subsonic/supersonic\n    die durch die Randbedingungen aufgelöst wird.\n  </div>',
     '<div class="note blue" data-lang="de">\n    <strong>Bedeutung für Düsenmodelle:</strong> MofCondiRatio ist zentral für\n    alle konvergent-divergenten Düsenberechnungen (Laval-Düse). Das Flächenverhältnis\n    bestimmt eindeutig die Machzahl — bis auf die Zweideutigkeit subsonic/supersonic\n    die durch die Randbedingungen aufgelöst wird.\n  </div>'
     '<div class="note blue" data-lang="en">\n    <strong>Significance for nozzle models:</strong> MofCondiRatio is central\n    to all convergent-divergent nozzle calculations (Laval nozzle). The area\n    ratio uniquely determines the Mach number — up to the subsonic/supersonic\n    ambiguity, which is resolved by the boundary conditions.\n  </div>')

# ── CAS Usage section ──
pair('<p>\n    Built-in Funktionen werden über das PROCEDURE/CALL-System eingebunden.\n    Jede Funktion braucht eine Prozedurendeklaration die den BIfunction-Namen\n    mit einer CAS-Prozedur verknüpft.\n  </p>',
     '<p data-lang="de">\n    Built-in Funktionen werden über das PROCEDURE/CALL-System eingebunden.\n    Jede Funktion braucht eine Prozedurendeklaration die den BIfunction-Namen\n    mit einer CAS-Prozedur verknüpft.\n  </p>'
     '<p data-lang="en">\n    Built-in functions are integrated via the PROCEDURE/CALL system. Each\n    function needs a procedure declaration that ties the BIfunction name to a\n    CAS procedure.\n  </p>')

# Lookup table headers
pair('<tr><th>BIfunction</th><th>CALL: Name</th><th>Eingaben</th><th>Ausgabe</th></tr>',
     '<tr>'
     '<th>BIfunction</th><th>CALL: Name</th>'
     '<th data-lang="de">Eingaben</th><th data-lang="en">Inputs</th>'
     '<th data-lang="de">Ausgabe</th><th data-lang="en">Output</th>'
     '</tr>')

# Lookup table cells with German text
td_pair('Schallgeschwindigkeit [m/s]', 'Speed of sound [m/s]')
td_pair('Schallgeschwindigkeit [m/s]', 'Speed of sound [m/s]')
td_pair('wie softdryJANAF + fH2O', 'like softdryJANAF + fH2O')
td_pair('cp Düse [J/kgK]', 'cp nozzle [J/kgK]')
td_pair('h feucht [J/kg]', 'h moist [J/kg]')
td_pair('h Kraftstoff [J/kg]', 'h fuel [J/kg]')
td_pair('Machzahl [−]', 'Mach number [−]')
td_pair('rel. Feuchte [−]', 'rel. humidity [−]')

# Procedure example comments
cmt('// Prozedurendeklaration am Dateianfang',
    '// Procedure declaration at file start')
cmt('// Verwendung in Gleichung', '// Use in equation')

pair('<div class="note amber">\n    <strong>Hinweis zur Ableitungsqualität:</strong> Da Built-in Funktionen\n    numerisch differenziert werden, können an Unstetigkeitsstellen (z.B.\n    ISA-Schichtgrenzen, Phasenübergänge) Ableitungsfehler auftreten.\n    Der Newton-Solver kann dort Konvergenzprobleme zeigen — in diesem Fall\n    Levenberg-Marquardt oder Homotopie verwenden.\n  </div>',
     '<div class="note amber" data-lang="de">\n    <strong>Hinweis zur Ableitungsqualität:</strong> Da Built-in Funktionen\n    numerisch differenziert werden, können an Unstetigkeitsstellen (z.B.\n    ISA-Schichtgrenzen, Phasenübergänge) Ableitungsfehler auftreten.\n    Der Newton-Solver kann dort Konvergenzprobleme zeigen — in diesem Fall\n    Levenberg-Marquardt oder Homotopie verwenden.\n  </div>'
     '<div class="note amber" data-lang="en">\n    <strong>Note on derivative quality:</strong> because built-in functions\n    are differentiated numerically, derivative errors can occur at\n    discontinuities (e.g., ISA layer boundaries, phase transitions). The\n    Newton solver may show convergence issues there — in which case use\n    Levenberg-Marquardt or homotopy.\n  </div>')

# ── Footer ──
pair('<span>CMDSolver Docs · BIfunctions Referenz · v2.5</span>',
     '<span data-lang="de">CMDSolver Docs · BIfunctions Referenz · v2.5</span>'
     '<span data-lang="en">CMDSolver Docs · BIfunctions Reference · v2.5</span>')
pair('<a href="parser_syntax.html">← Parser Syntax</a>',
     '<a href="parser_syntax.html" data-lang="de">← Parser Syntax</a>'
     '<a href="parser_syntax.html" data-lang="en">← Parser Syntax</a>')
pair('<a href="index.html">← Übersicht</a>',
     '<a href="index.html" data-lang="de">← Übersicht</a>'
     '<a href="index.html" data-lang="en">← Overview</a>')

# Apply
missing = []
for i, (old, new) in enumerate(REPS):
    if old not in html: missing.append((i, old[:80])); continue
    html = html.replace(old, new, 1)

p.write_text(html, encoding='utf-8')
print(f'bifunctions_reference.html: {len(REPS) - len(missing)} / {len(REPS)} replacements')
if missing:
    print('NOT FOUND:')
    for i, s in missing[:10]: print(f'  #{i}: {s!r}')
