#!/usr/bin/env python3
"""
Restore page-specific <style> blocks from the old documentation into the
current (bilingual) versions. The old docs had a two-tier CSS approach:
  <link rel="stylesheet" href="docs.css">  ← shared styles
  <style>                                  ← page-specific styles (LOST in migration)
    .symptom { ... }
    ...
  </style>

The bilingual migration kept the docs.css content inline but discarded the
second <style> block. This script extracts that block from each old HTML and
re-inserts it into the current HTML, just before the </style> that closes the
inline shared styles.

Conservative behavior:
- Only extracts page-specific <style> blocks (those NOT containing the leading
  /* CMDSolver Documentation — Shared Stylesheet */ marker — i.e., NOT docs.css)
- Skips files that already contain markers from a previous restore
- Skips i18n_demo.html, linktest.html, the index page, and any file that
  doesn't have a corresponding old version
"""
import re
from pathlib import Path

OLD_DIR = Path('/home/claude/old_docs')
CUR_DIR = Path('/home/claude/build')

SKIP_FILES = {'i18n_demo.html', 'linktest.html'}
RESTORE_MARKER = '/* ── Seitenspezifische Klassen'  # already-restored sentinel

processed = []
skipped = []
already_done = []

for old_path in sorted(OLD_DIR.glob('*.html')):
    name = old_path.name
    if name in SKIP_FILES:
        skipped.append((name, 'in skip list'))
        continue

    cur_path = CUR_DIR / name
    if not cur_path.exists():
        skipped.append((name, 'no current file'))
        continue

    cur_html = cur_path.read_text(encoding='utf-8')

    if RESTORE_MARKER in cur_html:
        already_done.append(name)
        continue

    old_html = old_path.read_text(encoding='utf-8')

    # Find all <style> blocks in the old file. Page-specific ones do NOT
    # contain the docs.css header marker. The pre-migration files had
    # <link rel="stylesheet" href="docs.css"> + a separate small <style> block.
    style_blocks = re.findall(r'<style[^>]*>(.*?)</style>', old_html, re.DOTALL)

    page_styles = []
    for block in style_blocks:
        # Heuristics for "this is the docs.css inlined" → skip
        if 'CMDSolver Documentation — Shared Stylesheet' in block:
            continue
        if '@import url' in block and ':root' in block:
            # Looks like the full shared sheet
            continue
        # Otherwise: page-specific
        cleaned = block.strip()
        if cleaned:  # don't add empty blocks
            page_styles.append(cleaned)

    if not page_styles:
        skipped.append((name, 'no page-specific styles in old version'))
        continue

    combined = '\n\n'.join(page_styles)

    # Build the insertion block
    insertion = (
        '\n\n/* ── Seitenspezifische Klassen ────────────────────────\n'
        f'   (aus alter {name} wiederhergestellt) */\n'
        + combined
        + '\n'
    )

    # Anchor: insert just before "</style>\n<link rel=\"stylesheet\" href=\"i18n.css\">"
    # If that exact anchor isn't there, fall back to just before </style></head>.
    anchor1 = '</style>\n<link rel="stylesheet" href="i18n.css">'
    anchor2 = '</style>\n</head>'

    if anchor1 in cur_html:
        new_html = cur_html.replace(anchor1, insertion + anchor1, 1)
    elif anchor2 in cur_html:
        new_html = cur_html.replace(anchor2, insertion + anchor2, 1)
    else:
        skipped.append((name, 'no insertion anchor found'))
        continue

    cur_path.write_text(new_html, encoding='utf-8')
    processed.append((name, len(combined)))


print(f'\n=== Restored {len(processed)} files ===')
for name, size in processed:
    print(f'  ✓ {name}: +{size} chars of page-specific CSS')

if already_done:
    print(f'\n=== Already restored ({len(already_done)}) ===')
    for n in already_done: print(f'  · {n}')

if skipped:
    print(f'\n=== Skipped ({len(skipped)}) ===')
    for n, reason in skipped: print(f'  – {n}: {reason}')
