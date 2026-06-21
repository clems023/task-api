#!/usr/bin/env python3
"""Génère le site statique GitHub Pages depuis la landing Django."""

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
STATIC_OUT = DOCS / "static" / "home"

TEMPLATE_PATH = ROOT / "api/templates/home/index.html"

REPLACEMENTS = [
    ("{% load static %}\n", ""),
    ("{% static 'home/styles.css' %}", "static/home/styles.css"),
    ("{% static 'home/app.js' %}", "static/home/app.js"),
    ('href="/api/health/"', 'href="#start"'),
    ("Tester le health check →", "Voir le quick start →"),
    ('data-api-health="/api/health/"', 'data-api-health=""'),
]

REQUIRED_IN_OUTPUT = [
    'href="static/home/styles.css"',
    'src="static/home/app.js"',
    'data-api-health=""',
    'href="#start"',
]


def apply_replacements(template: str) -> str:
    html = template
    for old, new in REPLACEMENTS:
        if old not in html:
            raise SystemExit(
                f"Échec : chaîne attendue introuvable dans le template : {old!r}"
            )
        html = html.replace(old, new)
    return html


def validate_output(html: str) -> None:
    if "{%" in html or "{{" in html:
        raise SystemExit(
            f"Échec : syntaxe Django restante dans le HTML généré ({TEMPLATE_PATH})."
        )

    for required in REQUIRED_IN_OUTPUT:
        if required not in html:
            raise SystemExit(
                f"Échec : contenu attendu absent du HTML généré : {required!r}"
            )


def main() -> None:
    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    html = apply_replacements(template)
    validate_output(html)

    STATIC_OUT.mkdir(parents=True, exist_ok=True)
    (DOCS / ".nojekyll").touch()
    (DOCS / "index.html").write_text(html, encoding="utf-8")
    shutil.copy2(ROOT / "api/static/home/styles.css", STATIC_OUT / "styles.css")
    shutil.copy2(ROOT / "api/static/home/app.js", STATIC_OUT / "app.js")

    print(f"Site statique généré dans {DOCS}")


if __name__ == "__main__":
    main()
