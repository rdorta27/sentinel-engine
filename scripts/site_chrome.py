"""Shared header, footer and language links of every page of the site.

A page holds the markers <!--site:header-->, <!--site:footer--> and
<!--site:hudlang-->. expand() writes the shared block between the markers, so
each page has the same navigation. The block is plain English. scripts/localize.py
translates it with the rest of the page.
"""

from __future__ import annotations

import posixpath
import re

REPO = "https://github.com/rdorta27/sentinel-engine"

# (directory, label, name in its own language, value of the html lang attribute)
LANGS = [
    ("en", "English (US)", "English (United States)", "en"),
    ("es-419", "Español (LA)", "Español (Latinoamérica)", "es-419"),
    ("pt-br", "Português (BR)", "Português (Brasil)", "pt-BR"),
]
LANG_DIRS = [d for d, *_ in LANGS if d != "en"]

NAV = [
    ("Home", "index.html"),
    ("Architecture", "diagrams/architecture.html"),
    ("One turn", "diagrams/turn.html"),
    ("Cases", "diagrams/cases.html"),
    ("Evidence", "diagrams/evidence.html"),
    ("Evaluate", "judges.html"),
    ("Slides", "slides/deck.html"),
]

MARK = re.compile(r"<!--site:(header|footer|hudlang)-->(?:.*?<!--/site:\1-->)?", re.S)


def rel(target: str, page: str) -> str:
    """Relative link from a page to a path of the site, both relative to site/."""
    return posixpath.relpath(target, posixpath.dirname(page) or ".")


def lang_links(css: str = "lang") -> str:
    links = "".join(
        f'<a lang="{html}" hreflang="{html}" data-lang="{d}" href="#" title="{name}">{label}</a>'
        for d, label, name, html in LANGS
    )
    return f'<div class="{css}" role="group" aria-label="Language" data-t="keep">{links}</div>'


def header(page: str) -> str:
    links = []
    for label, target in NAV:
        cur = ' aria-current="page"' if target == page else ""
        links.append(f'<a href="{rel(target, page)}"{cur}>{label}</a>')
    return (
        '<header class="top">\n'
        f'    <a class="logo" href="{rel("index.html", page)}"><img src="{rel("favicon.svg", page)}" width="34" height="34" alt="">Sentinel</a>\n'
        f'    <nav aria-label="Main">{"".join(links)}<a class="cta" href="{REPO}">GitHub</a></nav>\n'
        f"    {lang_links()}\n"
        "  </header>"
    )


def footer(page: str) -> str:
    return (
        "<footer>\n"
        f'    <a href="{rel("index.html", page)}">Home</a>\n'
        f'    <a href="{rel("diagrams/architecture.html", page)}">Architecture</a>\n'
        f'    <a href="{rel("diagrams/evidence.html", page)}">Evidence</a>\n'
        f'    <a href="{REPO}/blob/main/docs/requirements/requirements.md">Requirements</a>\n'
        f'    <a href="{REPO}">Repository</a>\n'
        '    <span class="grow">Synthetic demo data. No credentials and no real data in the repository.</span>\n'
        "  </footer>"
    )


def hudlang() -> str:
    return lang_links("hudlang")


def expand(html: str, page: str) -> str:
    def block(m: re.Match) -> str:
        kind = m.group(1)
        body = {"header": header(page), "footer": footer(page), "hudlang": hudlang()}[kind]
        return f"<!--site:{kind}-->{body}<!--/site:{kind}-->"

    return MARK.sub(block, html)
