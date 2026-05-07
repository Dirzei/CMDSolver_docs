#!/usr/bin/env python3
"""
Adds collapsible sections to index.html using <details>/<summary>.
- Replaces <section> with <details class="section" open data-key="..."> and
  wraps the existing <h2> tags in a <summary> element.
- Adds CSS for the collapsed/expanded states and chevron animation.
- Adds JS for localStorage-based persistence (per-section).
- Adds an "Alle aufklappen / Alle einklappen" toolbar above <main>.
"""
import re
from pathlib import Path

p = Path('/home/claude/build/index.html')
html = p.read_text(encoding='utf-8')

# ─── 1. CSS additions ────────────────────────────────────────────────
# Inserted right before the closing </style> in the inline stylesheet.

CSS = '''
/* ── Collapsible sections ─────────────────────────────────────────── */
details.section {
  margin-bottom: 2rem;
  scroll-margin-top: 5rem;
}
details.section[open] {
  margin-bottom: 3.5rem;
}
details.section > summary {
  list-style: none;        /* Firefox */
  cursor: pointer;
  user-select: none;
  margin-bottom: 1.4rem;
  padding-bottom: .5rem;
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
  gap: .6rem;
  transition: border-bottom-color .15s, color .15s;
}
details.section > summary::-webkit-details-marker { display: none; }  /* Safari */
details.section > summary:hover { border-bottom-color: var(--border2); }
details.section > summary:hover h2 { color: var(--text2); }

/* Bullet (kept from original h2::before) */
details.section > summary::before {
  content: '';
  display: inline-block;
  width: 8px; height: 8px;
  border-radius: 50%;
  background: var(--accent);
  flex-shrink: 0;
  transition: background .15s;
}
details.section:not([open]) > summary::before { background: var(--text3); }

/* h2 inside summary keeps its existing style — just remove its own margin */
details.section > summary > h2 {
  font-size: 12px; font-family: var(--mono);
  letter-spacing: .12em; text-transform: uppercase;
  color: var(--text3); margin: 0;
  border: none; padding: 0;
  display: inline; transition: color .15s;
}

/* Chevron on the right side */
details.section > summary::after {
  content: '';
  margin-left: auto;
  width: 7px; height: 7px;
  border-right: 1.5px solid var(--text3);
  border-bottom: 1.5px solid var(--text3);
  transform: rotate(-45deg);     /* points up — collapsed */
  transition: transform .2s ease;
  flex-shrink: 0;
}
details.section[open] > summary::after {
  transform: rotate(45deg);      /* points down — expanded */
}

/* When closed, also add a small "n items" hint */
details.section > summary > .item-count {
  font-family: var(--mono); font-size: 10px;
  color: var(--text3); margin-left: .8rem;
  letter-spacing: .05em; text-transform: none;
}
details.section[open] > summary > .item-count { display: none; }

/* ── Expand-/Collapse-All toolbar ─────────────────────────────────── */
.section-toolbar {
  display: flex; gap: .5rem; align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  font-family: var(--mono); font-size: 11px;
}
.section-toolbar button {
  background: none;
  border: 1px solid var(--border2);
  color: var(--text3);
  padding: 4px 12px;
  border-radius: 4px;
  cursor: pointer;
  font-family: var(--mono);
  font-size: 11px;
  letter-spacing: .04em;
  transition: all .15s;
}
.section-toolbar button:hover {
  border-color: var(--accent);
  color: var(--accent);
}
'''

# Insert CSS just before </style>
old_style_close = '</style>'
new_style_close = CSS + '\n</style>'
html = html.replace(old_style_close, new_style_close, 1)


# ─── 2. Section transformations ─────────────────────────────────────
# We replace each <section><h2>...</h2> ... </section> with
# <details class="section" open data-key="X"><summary><h2>...</h2></summary> ... </details>

# Map (DE-h2-text, EN-h2-text) → (data-key, item_count)
# item_count is approximate, used as small hint when collapsed
SECTIONS = [
    ('Einstieg',                      'Getting Started',                   'einstieg',          4),
    ('Grundlagen',                    'Foundations',                       'grundlagen',        2),
    ('Solver — Detaildokumentation',  'Solvers — Detailed Documentation',  'solver-detail',     9),
    ('Referenz',                      'Reference',                         'referenz',          4),
    ('Engineering-Wissen',            'Engineering Knowledge',             'engineering',       7),
    ('Versionshistorie',              'Version History',                   'versionshistorie',  None),
]

for de_h2, en_h2, key, n_items in SECTIONS:
    # Find the <section> containing this exact bilingual h2 pair
    h2_pattern = (f'<h2 data-lang="de">{de_h2}</h2>'
                  f'<h2 data-lang="en">{en_h2}</h2>')
    # Replace <section>\n  <h2_pattern> with <details ...><summary>...
    open_old = f'<section>\n  {h2_pattern}'

    if n_items is not None:
        count_de = f'<span class="item-count" data-lang="de">{n_items} Einträge</span>'
        count_en = f'<span class="item-count" data-lang="en">{n_items} entries</span>'
        count_html = count_de + count_en
    else:
        count_html = ''

    open_new = (f'<details class="section" open data-key="{key}">\n'
                f'  <summary>{h2_pattern}{count_html}</summary>')

    if open_old in html:
        html = html.replace(open_old, open_new, 1)
        print(f'  ✓ {key}')
    else:
        print(f'  ✗ {key} — open tag pattern not found')


# Now replace the closing </section> tags with </details>
# This is simple since after our open replacements, every <details class="section">
# has a matching </section> that should become </details>.
html = html.replace('</section>', '</details>')


# ─── 3. Toolbar above <main>'s first section ────────────────────────
# Insert toolbar right after <main> opening
toolbar_html = '''<div class="section-toolbar">
  <button class="expand-all" data-lang="de">Alle aufklappen</button>
  <button class="expand-all" data-lang="en">Expand all</button>
  <button class="collapse-all" data-lang="de">Alle einklappen</button>
  <button class="collapse-all" data-lang="en">Collapse all</button>
</div>

'''
# We want the buttons styled with the same lang-switching mechanism, but the
# CSS rules in i18n.css only apply to span/div/p/h*/li/td/th — NOT button.
# So we need a small addition: button[data-lang] should also work.
# Easier approach: wrap each pair in a <span> that DOES match the rules.
toolbar_html = '''<div class="section-toolbar">
  <span data-lang="de"><button class="expand-all">Alle aufklappen</button></span>
  <span data-lang="en"><button class="expand-all">Expand all</button></span>
  <span data-lang="de"><button class="collapse-all">Alle einklappen</button></span>
  <span data-lang="en"><button class="collapse-all">Collapse all</button></span>
</div>

'''

html = html.replace('<main>\n\n', '<main>\n\n' + toolbar_html, 1)


# ─── 4. JavaScript for persistence + toolbar ────────────────────────
# Insert before the closing </body>.

JS = '''<script>
(function(){
  // ── localStorage-Persistenz pro Sektion ──────────────────────────
  // Schlüssel: "cmdsection:<data-key>" → "open" | "closed"
  function storageKey(k){ return 'cmdsection:' + k; }

  document.addEventListener('DOMContentLoaded', function(){
    document.querySelectorAll('details.section').forEach(function(d){
      var key = d.dataset.key;
      if (!key) return;
      // Restore saved state
      try {
        var saved = localStorage.getItem(storageKey(key));
        if (saved === 'closed') d.removeAttribute('open');
        else if (saved === 'open') d.setAttribute('open', '');
        // No saved state → keep default "open"
      } catch(e) {}
      // Persist on every toggle
      d.addEventListener('toggle', function(){
        try {
          localStorage.setItem(storageKey(key), d.open ? 'open' : 'closed');
        } catch(e) {}
      });
    });

    // ── Expand-/Collapse-All Buttons ──────────────────────────────
    document.querySelectorAll('.expand-all').forEach(function(b){
      b.addEventListener('click', function(){
        document.querySelectorAll('details.section').forEach(function(d){
          if (!d.open) d.setAttribute('open', '');  // toggle event fires → persists
        });
      });
    });
    document.querySelectorAll('.collapse-all').forEach(function(b){
      b.addEventListener('click', function(){
        document.querySelectorAll('details.section').forEach(function(d){
          if (d.open) d.removeAttribute('open');
        });
      });
    });
  });
})();
</script>
'''

html = html.replace('</body>', JS + '</body>', 1)


# ─── Write back ──────────────────────────────────────────────────────
p.write_text(html, encoding='utf-8')
print('\n✓ Collapsible sections applied to index.html')
