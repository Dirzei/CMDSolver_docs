#!/usr/bin/env python3
"""Fix the three review pages so their styling matches the rest of the docs.

Bug: the harmonization step left an external <link rel="stylesheet" href="../docs.css">
in place. The path is wrong (docs.css lives next to the HTML, not one level up),
and even with the right path it would diverge from how every other doc page works
— all other pages inline the contents of docs.css into their own <style> block.

Fix: drop the broken external link, prepend the contents of docs.css into the
existing <style> block (just before the page-specific rules), so styling is
self-contained and matches the rest of the docs.
"""
from pathlib import Path
import re

docs_css = Path('docs.css').read_text(encoding='utf-8')

for f in ['infra_reviews.html', 'parser_reviews.html', 'solver_reviews.html']:
    p = Path(f)
    html = p.read_text(encoding='utf-8')
    orig = len(html)

    # 1. Remove the broken <link rel="stylesheet" href="../docs.css">
    html, n_link = re.subn(
        r'<link rel="stylesheet" href="\.\./docs\.css">\s*\n?',
        '', html, count=1
    )
    assert n_link == 1, f'broken docs.css link not found in {f}'

    # 2. Prepend docs.css contents into the existing <style> block.
    html, n_style = re.subn(
        r'<style>\n',
        '<style>\n' + docs_css + '\n/* ── Page-specific styles ──────────────────────────── */\n',
        html, count=1
    )
    assert n_style == 1, f'<style> opening not found in {f}'

    p.write_text(html, encoding='utf-8')
    print(f'  {f}: {orig} → {len(html)} bytes (+{len(html)-orig})')
