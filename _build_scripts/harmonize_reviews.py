#!/usr/bin/env python3
"""Harmonize layout of infra_reviews.html / parser_reviews.html / solver_reviews.html
with the rest of the documentation:

1. Clean up the duplicated <style> block, add classes for Quick-Jump table.
2. Insert a Bewertungs-Legende (rating legend) at the top.
3. Insert a Quick-Jump table as the first section, plus a counter line.
4. Wrap every <div class="review-block"> in <section id="..."> and promote h3 → h2.
5. Replace the bespoke footer with the standard CMDSolver Docs footer pattern,
   including Prev / Next links in DE + EN.

The text content of existing reviews is left untouched — bilingual migration
of review bodies is a separate phase.
"""
from pathlib import Path
import re

# ──────────────────────────────────────────────────────────────────────────
#  Per-file metadata: title, version-string in footer, prev/next links,
#  and the list of (anchor, review-id, title, rating, file-meta) for the
#  Quick-Jump table.
# ──────────────────────────────────────────────────────────────────────────

PAGES = {
    'infra_reviews.html': {
        'footer_de': 'CMDSolver Docs · Code Review · Infrastruktur · v2.12',
        'footer_en': 'CMDSolver Docs · Code Review · Infrastructure · v2.12',
        'prev_href': 'index.html', 'prev_de': '← Übersicht',     'prev_en': '← Overview',
        'next_href': 'parser_reviews.html', 'next_de': 'Parser Review →', 'next_en': 'Parser Review →',
        'jump_caption_de': '4 Reviews · 2× A · 2× B',
        'jump_caption_en': '4 reviews · 2× A · 2× B',
        'reviews': [
            ('abstractsolver',   'INFRA-01', 'AbstractSolver',                                          'A', 'AbstractSolver.java',     '828'),
            ('equilibrator',     'INFRA-02', 'JacobiEquilibrator',                                      'A', 'JacobiEquilibrator.java', '212'),
            ('projector-scaler', 'INFRA-03', 'PhysicalProjector & VariableScaler',                      'B', 'PhysicalProjector.java + VariableScaler.java', '333 + 248'),
            ('config',           'INFRA-04', 'SolverConfig, SolverFactory, HomotopyConfig, SolverType', 'B', 'SolverConfig + SolverFactory + HomotopyConfig + SolverType', '299 + 89 + 231 + 89'),
        ],
    },
    'parser_reviews.html': {
        'footer_de': 'CMDSolver Docs · Code Review · Parser · v2.12',
        'footer_en': 'CMDSolver Docs · Code Review · Parser · v2.12',
        'prev_href': 'infra_reviews.html', 'prev_de': '← Infra Review', 'prev_en': '← Infra Review',
        'next_href': 'solver_reviews.html', 'next_de': 'Solver Review →', 'next_en': 'Solver Review →',
        'jump_caption_de': '4 Reviews · 2× A · 2× B',
        'jump_caption_en': '4 reviews · 2× A · 2× B',
        'reviews': [
            ('eqnsysreader', 'PARSER-01', 'EqnSysReader',                  'B', 'EqnSysReader.java',           '~1200'),
            ('eqndata',      'PARSER-02', 'EqnData & Conditional-Logik',   'B', 'EqnData.java',                '~800'),
            ('bifunctions',  'PARSER-03', 'BIfunctions (Built-in Funktionen)', 'A', 'BIfunctions.java',         '~600'),
            ('systemdata',   'PARSER-04', 'SystemData & Variable',         'A', 'SystemData.java + Variable.java', '~500'),
        ],
    },
    'solver_reviews.html': {
        'footer_de': 'CMDSolver Docs · Code Review · Solver · v2.12',
        'footer_en': 'CMDSolver Docs · Code Review · Solver · v2.12',
        'prev_href': 'parser_reviews.html', 'prev_de': '← Parser Review', 'prev_en': '← Parser Review',
        'next_href': 'index.html', 'next_de': 'Übersicht →', 'next_en': 'Overview →',
        'jump_caption_de': '7 Reviews · 3× A · 1× B · 2× C · 1× D',
        'jump_caption_en': '7 reviews · 3× A · 1× B · 2× C · 1× D',
        'reviews': [
            ('newton-armijo',   'SOLVER-01', 'NewtonArmijoSolver',                   'A', 'NewtonArmijoSolver.java',       '228'),
            ('lm',              'SOLVER-02', 'LevenbergMarquardtSolver (v3b)',       'A', 'LevenbergMarquardtSolver.java', '393'),
            ('broyden',         'SOLVER-03', 'BroydenSolver',                        'B', 'BroydenSolver.java',            '713'),
            ('gspar',           'SOLVER-04', 'GSPAR-Solver-Familie (3 Solver)',      'A', 'GSPARSolver + NewtonArmijoGSPARSolver + BroydenGSPARSolver', '386 + 132 + 257'),
            ('homotopy',        'SOLVER-05', 'HomotopySolver (klassisch)',           'C', 'HomotopySolver.java',           '801'),
            ('arc-length',      'SOLVER-06', 'ArcLengthHomotopySolver (experimental)', 'D', 'ArcLengthHomotopySolver.java', '712'),
            ('adaptive-lambda', 'SOLVER-07', 'AdaptiveLambdaSolver (Phase 1 produktiv)', 'C', 'AdaptiveLambdaSolver.java', '375'),
        ],
    },
}

RATE_LABELS = {
    'A': ('A — Exzellent',           'A — Excellent'),
    'B': ('B — Gut',                 'B — Good'),
    'C': ('C — Verbesserungspotential', 'C — Room for improvement'),
    'D': ('D — Refactoring nötig',   'D — Refactoring needed'),
}

# ──────────────────────────────────────────────────────────────────────────
#  Cleaned-up CSS block (replaces both the duplicated review CSS and adds
#  classes for the Quick-Jump table and rating-legend).
# ──────────────────────────────────────────────────────────────────────────

CLEAN_CSS = '''<style>
/* ── Review-Karten ───────────────────────────────────── */
.review-rating { font-size: 13px; padding: 2px 10px; border-radius: 4px; font-weight: 600; }
.rate-A { background: rgba(62,207,142,.12);  color: #3ecf8e; }
.rate-B { background: rgba(74,158,255,.12);  color: #4a9eff; }
.rate-C { background: rgba(240,160,48,.12);  color: #f0a030; }
.rate-D { background: rgba(255,92,92,.12);   color: #ff5c5c; }

.review-block { background: #13161b; border: 1px solid #2e3540; border-radius: 8px;
  padding: 1.2rem 1.4rem; margin-bottom: 1.5rem; }
.review-head { display: flex; align-items: baseline; gap: 0.8rem; flex-wrap: wrap; margin-bottom: 0.3rem; }
.review-head h2 { margin: 0; font-size: 18px; color: #e8ecf4; border: 0; padding: 0; }
.review-id { color: #7f8a99; font-size: 12px; font-family: 'IBM Plex Mono', monospace; }
.review-meta { color: #7f8a99; font-size: 12px; margin-bottom: 0.8rem; }
.review-strengths strong { color: #3ecf8e; }
.review-weaknesses { margin-top: 0.6rem; }
.review-weaknesses strong { color: #f0a030; }
.review-fazit { color: #c8cdd6; margin-top: 0.6rem; font-style: italic;
  border-top: 1px solid #2e3540; padding-top: 0.8rem; }

/* Section-Wrapper schluckt das Karten-Margin so dass nichts springt */
section.review-section { margin: 0 0 1.5rem 0; padding: 0; border: 0; }
section.review-section .review-block { margin-bottom: 0; }

/* ── Bewertungs-Legende ──────────────────────────────── */
.rating-legend { display: flex; gap: 0.6rem; flex-wrap: wrap; align-items: center;
  margin-top: 0.4rem; }
.rating-legend .review-rating { font-size: 12px; }

/* ── Quick-Jump-Tabelle ──────────────────────────────── */
.review-jump-table { margin-bottom: 0.8rem; }
.review-jump-table td { padding: 6px 10px; vertical-align: middle; }
.review-jump-table td:first-child { color: #7f8a99; font-family: 'IBM Plex Mono', monospace;
  font-size: 11px; white-space: nowrap; }
.review-jump-table td:nth-child(2) a { color: #e8ecf4; font-weight: 500; text-decoration: none; }
.review-jump-table td:nth-child(2) a:hover { color: var(--accent); }
.review-jump-table td:nth-child(3) { color: #7f8a99; font-family: 'IBM Plex Mono', monospace;
  font-size: 11px; }
.review-jump-table td:nth-child(4) { color: #7f8a99; font-size: 12px; text-align: right;
  white-space: nowrap; }
.review-jump-table td:last-child { text-align: right; white-space: nowrap; }
.review-counter { color: #7f8a99; font-size: 12px; margin-top: 0.6rem; }

/* ── i18n Language Switcher ──────────────────────────── */
.lang-switch { display: flex; align-items: center; gap: .4rem;
  font-family: var(--mono); font-size: 11px; }
.lang-btn { background: none; border: 1px solid var(--border2);
  color: var(--text3); padding: 3px 9px; border-radius: 4px;
  cursor: pointer; font-family: var(--mono); font-size: 11px;
  transition: all .15s; letter-spacing: .06em; }
.lang-btn:hover { border-color: var(--accent); color: var(--accent); }
.lang-btn.active { background: rgba(74,158,255,.12); border-color: var(--accent);
  color: var(--accent); font-weight: 600; }
</style>'''


def build_legend():
    """Build the rating legend as a note blue block, bilingual."""
    rate_chips_de = ' '.join(
        f'<span class="review-rating rate-{r}">{RATE_LABELS[r][0]}</span>'
        for r in 'ABCD'
    )
    rate_chips_en = ' '.join(
        f'<span class="review-rating rate-{r}">{RATE_LABELS[r][1]}</span>'
        for r in 'ABCD'
    )
    return (
        '<div class="note blue" data-lang="de">\n'
        '    <strong>Bewertungsskala:</strong>\n'
        '    <div class="rating-legend">' + rate_chips_de + '</div>\n'
        '  </div>\n'
        '  <div class="note blue" data-lang="en">\n'
        '    <strong>Rating scale:</strong>\n'
        '    <div class="rating-legend">' + rate_chips_en + '</div>\n'
        '  </div>'
    )


def build_quick_jump(reviews, caption_de, caption_en):
    """Build the Quick-Jump section with a table of all reviews on this page."""
    rows = []
    for anchor, rid, title, rate, file, lines in reviews:
        # Title may contain & — escape for HTML if needed
        safe_title = title.replace('&', '&amp;')
        rate_label_de = RATE_LABELS[rate][0]
        rate_label_en = RATE_LABELS[rate][1]
        rows.append(
            f'      <tr>\n'
            f'        <td>{rid}</td>\n'
            f'        <td><a href="#{anchor}">{safe_title}</a></td>\n'
            f'        <td><code>{file}</code></td>\n'
            f'        <td>{lines}</td>\n'
            f'        <td>'
            f'<span class="review-rating rate-{rate}" data-lang="de">{rate_label_de}</span>'
            f'<span class="review-rating rate-{rate}" data-lang="en">{rate_label_en}</span>'
            f'</td>\n'
            f'      </tr>'
        )
    rows_html = '\n'.join(rows)

    return (
        '<section id="uebersicht">\n'
        '  <h2 data-lang="de">Übersicht</h2><h2 data-lang="en">Overview</h2>\n'
        '\n'
        '  <div class="tbl-wrap">\n'
        '  <table class="review-jump-table">\n'
        '    <thead><tr>\n'
        '      <th>ID</th>\n'
        '      <th data-lang="de">Komponente</th><th data-lang="en">Component</th>\n'
        '      <th data-lang="de">Datei</th><th data-lang="en">File</th>\n'
        '      <th data-lang="de">Zeilen</th><th data-lang="en">Lines</th>\n'
        '      <th data-lang="de">Bewertung</th><th data-lang="en">Rating</th>\n'
        '    </tr></thead>\n'
        '    <tbody>\n' + rows_html + '\n'
        '    </tbody>\n'
        '  </table>\n'
        '  </div>\n'
        '\n'
        f'  <div class="review-counter" data-lang="de">{caption_de}</div>\n'
        f'  <div class="review-counter" data-lang="en">{caption_en}</div>\n'
        '</section>'
    )


def build_footer(meta):
    """Build the standard CMDSolver Docs footer with Prev/Next links."""
    return (
        '<footer>\n'
        f'  <span data-lang="de">{meta["footer_de"]}</span>'
        f'<span data-lang="en">{meta["footer_en"]}</span>\n'
        '  <span>\n'
        f'    <a href="{meta["prev_href"]}" data-lang="de">{meta["prev_de"]}</a>'
        f'<a href="{meta["prev_href"]}" data-lang="en">{meta["prev_en"]}</a>\n'
        '    &nbsp;|&nbsp;\n'
        f'    <a href="{meta["next_href"]}" data-lang="de">{meta["next_de"]}</a>'
        f'<a href="{meta["next_href"]}" data-lang="en">{meta["next_en"]}</a>\n'
        '  </span>\n'
        '</footer>'
    )


def harmonize(filename, meta):
    p = Path('/home/claude/build') / filename
    html = p.read_text(encoding='utf-8')
    original_size = len(html)

    # ── 1. Replace the entire <style>…</style> block at the top with CLEAN_CSS.
    html, n = re.subn(r'<style>.*?</style>', CLEAN_CSS, html, count=1, flags=re.DOTALL)
    assert n == 1, f'CSS block not found in {filename}'

    # ── 2. Wrap every <div class="review-block" id="..."> in a <section> and
    #       promote the inner <h3> to <h2>.
    #
    # The block is already opened with `<div class="review-block" id="ANCHOR">`
    # and closed by a matching </div>. We don't try to find the matching </div>
    # via regex — instead we wrap each opening tag with `<section id="ANCHOR" class="review-section">`
    # and let the closing of the review-block end the section as well.
    # That requires inserting `</section>` AFTER the matching </div>.
    #
    # Approach: each review-block is a top-level child of <main>. The blocks are
    # separated by HTML comments like <!-- ─────── INFRA-01: ... ─────── -->.
    # We find each block, swap in section wrappers, and at the end re-emit.

    # Promote h3 → h2 only inside review-head (the page's only h3s)
    html = re.sub(
        r'(<div class="review-head">\s*<span class="review-id">[^<]+</span>\s*)<h3>([^<]+)</h3>',
        r'\1<h2>\2</h2>',
        html
    )

    # ── 3. Wrap each review-block in a <section>. Match the full block including
    #       its closing </div>. We rely on the fact that review-blocks are separated
    #       in the source by either <!-- comments --> or by </main>.
    #
    # We identify each block by its opening <div class="review-block" id="ANCHOR">,
    # then walk forward counting <div> / </div> to find its matching close.
    def wrap_blocks(src):
        out = []
        i = 0
        pat = re.compile(r'<div class="review-block" id="([^"]+)">')
        while True:
            m = pat.search(src, i)
            if not m:
                out.append(src[i:])
                break
            anchor = m.group(1)
            # Append everything up to the start of this match
            out.append(src[i:m.start()])
            # Walk forward to find the matching </div>. We need to balance
            # nested <div>...</div>. Start counting at depth 1 (we just opened one).
            depth = 1
            j = m.end()
            tag_re = re.compile(r'<(/?)div\b[^>]*>')
            while depth > 0:
                tm = tag_re.search(src, j)
                if not tm:
                    raise RuntimeError(f'unbalanced div for {anchor}')
                if tm.group(1) == '':  # opening
                    depth += 1
                else:  # closing
                    depth -= 1
                j = tm.end()
            # Now src[m.start():j] is the full review-block including </div>.
            block_html = src[m.start():j]
            # Remove the id from the inner div (we move it to the section)
            block_html_noid = re.sub(
                r'<div class="review-block" id="[^"]+">',
                '<div class="review-block">',
                block_html, count=1
            )
            out.append(
                f'<section id="{anchor}" class="review-section">\n'
                f'  {block_html_noid}\n'
                f'</section>'
            )
            i = j
        return ''.join(out)

    html = wrap_blocks(html)

    # ── 4. Insert legend + Quick-Jump as the first content inside <main>.
    legend = build_legend()
    qj = build_quick_jump(meta['reviews'], meta['jump_caption_de'], meta['jump_caption_en'])
    intro = '\n\n' + legend + '\n\n' + qj + '\n\n'

    # Replace the first occurrence of `<main>\n\n` (or `<main>\n`) with `<main>` + intro.
    html = re.sub(r'<main>\s*\n', '<main>\n' + intro, html, count=1)

    # ── 5. Replace the bespoke <footer>…</footer> with the standard footer.
    new_footer = build_footer(meta)
    html, n = re.subn(r'<footer>.*?</footer>', new_footer, html, count=1, flags=re.DOTALL)
    assert n == 1, f'Footer not found in {filename}'

    p.write_text(html, encoding='utf-8')
    new_size = len(html)
    print(f'  {filename}: {original_size} → {new_size} bytes ({new_size - original_size:+d})')


# ──────────────────────────────────────────────────────────────────────────
#  Run
# ──────────────────────────────────────────────────────────────────────────

print('Harmonizing review pages:')
for filename, meta in PAGES.items():
    harmonize(filename, meta)
print('Done.')
