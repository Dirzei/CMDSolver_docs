#!/usr/bin/env python3
"""
Migrates all CMDSolver doc HTML files to bilingual + sticky-header + glow.

For each .html file (except linktest.html, which is a debug stub):
  1. Inserts <link rel="stylesheet" href="i18n.css"> right before </head>.
     The link is placed AFTER any inline <style> so its rules win on conflicts.
  2. Replaces the existing language-handling <script> block with an improved
     version that uses .active class (instead of inline styles) and adds the
     IntersectionObserver-driven .scrolled toggle on .doc-header.
  3. Inserts <div class="header-sentinel"></div> immediately before the
     <div class="doc-header">.
  4. Wraps the existing .doc-badge into a .doc-header-right container that
     also contains the new <div class="lang-switch"> with two .lang-btn buttons.
  5. Special: fixes infra_reviews.html where a stray "</style>" inside a CSS
     comment was prematurely closing the inline style block.
"""
import re, shutil
from pathlib import Path

SRC = Path('/home/claude')
DST = Path('/home/claude/build')
DST.mkdir(exist_ok=True)

# ─── Templates ──────────────────────────────────────────────────────

NEW_SCRIPT = '''<script>
(function(){
  var stored = '';
  try { stored = localStorage.getItem('cmdlang') || ''; } catch(e){}
  var lang = stored || 'de';

  function apply(l) {
    lang = l;
    try { localStorage.setItem('cmdlang', l); } catch(e){}
    document.documentElement.lang = l;
    var body = document.body;
    body.classList.remove('lang-de','lang-en');
    body.classList.add('lang-' + l);
    document.querySelectorAll('.lang-btn').forEach(function(b){
      b.classList.toggle('active', b.dataset.lang === l);
    });
  }

  document.addEventListener('DOMContentLoaded', function(){
    apply(lang);
    document.querySelectorAll('.lang-btn').forEach(function(b){
      b.addEventListener('click', function(){ apply(b.dataset.lang); });
    });
    // Sticky-Header Schatten via IntersectionObserver
    var sentinel = document.querySelector('.header-sentinel');
    var header   = document.querySelector('.doc-header');
    if (sentinel && header && 'IntersectionObserver' in window) {
      new IntersectionObserver(function(entries){
        header.classList.toggle('scrolled', !entries[0].isIntersecting);
      }).observe(sentinel);
    }
  });
})();
</script>'''

LANG_SWITCH_HTML = (
    '<div class="lang-switch">'
    '<button class="lang-btn" data-lang="de">DE</button>'
    '<button class="lang-btn" data-lang="en">EN</button>'
    '</div>'
)

# Pattern matches the entire existing language-handling <script>...</script>
SCRIPT_PATTERN = re.compile(
    r'<script>\s*\(function\(\)\{\s*var stored.*?\}\)\(\);\s*</script>',
    re.DOTALL,
)

# ─── Per-file transformer ──────────────────────────────────────────

def transform(html: str, filename: str) -> str:
    # Special pre-fix for infra_reviews.html: a comment "/* ... </style>"
    # ended the style tag inside a comment — re-open by stripping the literal.
    if filename == 'infra_reviews.html':
        html = html.replace(
            '/* Sprach-Sichtbarkeit via </style>',
            '/* Sprach-Sichtbarkeit via class auf body */\n</style>',
        )

    # 1. Inject <link rel="stylesheet" href="i18n.css"> before </head>.
    if 'href="i18n.css"' not in html:
        html = html.replace(
            '</head>',
            '<link rel="stylesheet" href="i18n.css">\n</head>',
            1,
        )

    # 2. Replace the existing language script with the improved version.
    if SCRIPT_PATTERN.search(html):
        html = SCRIPT_PATTERN.sub(NEW_SCRIPT, html, count=1)
    elif '<body>' in html and 'cmdlang' not in html:
        # File has no script yet — inject right after <body>
        html = html.replace('<body>', '<body>\n' + NEW_SCRIPT, 1)

    # 3. Insert sentinel immediately before <div class="doc-header">.
    if '<div class="header-sentinel">' not in html:
        html = re.sub(
            r'(<div class="doc-header">)',
            r'<div class="header-sentinel"></div>\n\1',
            html, count=1,
        )

    # 4. Wrap existing .doc-badge plus new .lang-switch into .doc-header-right.
    #    The .doc-badge in source files looks like:
    #       <span class="doc-badge solver">v2.12</span></div>
    #    where the </div> closes the .doc-header.
    #    We replace that with: <div class="doc-header-right">
    #                            <lang-switch>
    #                            <span class="doc-badge ...">v2.12</span>
    #                          </div>
    #                          </div>
    if 'class="lang-switch"' not in html:
        badge_re = re.compile(
            r'(<span class="doc-badge[^"]*">[^<]*</span>)\s*</div>'
        )
        m = badge_re.search(html)
        if m:
            replacement = (
                '<div class="doc-header-right">'
                + LANG_SWITCH_HTML
                + m.group(1)
                + '</div></div>'
            )
            html = html[:m.start()] + replacement + html[m.end():]

    return html


# ─── Run ───────────────────────────────────────────────────────────

SKIP = {'linktest.html', 'i18n_demo.html'}

processed, skipped = [], []
for p in sorted(SRC.glob('*.html')):
    if p.name in SKIP:
        skipped.append(p.name)
        continue
    src = p.read_text(encoding='utf-8')
    out = transform(src, p.name)
    (DST / p.name).write_text(out, encoding='utf-8')
    processed.append(p.name)

# also copy the docs.css verbatim into build/ so links inside files keep working
shutil.copy(SRC / 'docs.css', DST / 'docs.css')

print(f'Processed: {len(processed)} files')
for f in processed:
    print(f'  ✓ {f}')
print(f'Skipped: {", ".join(skipped) if skipped else "(none)"}')
