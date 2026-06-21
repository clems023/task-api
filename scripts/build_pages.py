#!/usr/bin/env python3
"""Génère le site statique GitHub Pages depuis la landing Django."""

from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
STATIC_OUT = DOCS / "static" / "home"

template = (ROOT / "api/templates/home/index.html").read_text(encoding="utf-8")

html = template.replace("{% load static %}\n", "")
html = html.replace("{% static 'home/styles.css' %}", "static/home/styles.css")
html = html.replace("{% static 'home/app.js' %}", "static/home/app.js")
html = html.replace('href="/api/health/"', 'href="#start"')
html = html.replace(
    'Tester le health check →',
    "Voir le quick start →",
)
html = html.replace('data-api-health="/api/health/"', 'data-api-health=""')

if 'data-api-health="/api/health/"' in html:
    raise SystemExit("Échec : data-api-health n'a pas été vidé pour GitHub Pages.")

STATIC_OUT.mkdir(parents=True, exist_ok=True)
(DOCS / ".nojekyll").touch()
(DOCS / "index.html").write_text(html, encoding="utf-8")
shutil.copy2(ROOT / "api/static/home/styles.css", STATIC_OUT / "styles.css")
shutil.copy2(ROOT / "api/static/home/app.js", STATIC_OUT / "app.js")

print(f"Site statique généré dans {DOCS}")
