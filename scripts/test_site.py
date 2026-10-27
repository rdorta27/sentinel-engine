"""Tests for the static site: numbers match the evidence, no secret, no external load.

Run from the repository root: python3 -m pytest scripts/test_site.py -q
"""

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import site_numbers as sn  # noqa: E402

SITE = sn.ROOT / "site"
PAGES = sorted(SITE.rglob("*.html"))


def test_numbers_json_matches_evidence():
    assert sn.OUT.read_text() == sn.render(sn.build()), "run scripts/site_numbers.py"


def test_each_number_slot_matches_numbers_json():
    numbers = json.loads(sn.OUT.read_text())["numbers"]
    slots = 0
    for page in PAGES:
        for m in sn.SLOT.finditer(page.read_text()):
            slots += 1
            key = m.group(4)
            assert key in numbers, f"{page.name}: unknown number {key}"
            expected = sn.slot_text(numbers, m.group(3), key, sn.page_lang(page, SITE))
            assert m.group(5) == expected, f"{page.name}: {key} shows {m.group(5)!r}, evidence says {expected!r}"
    assert slots > 0


def test_every_number_has_type_source_and_field():
    for key, entry in json.loads(sn.OUT.read_text())["numbers"].items():
        assert entry["type"] in {"Test suite", "Simulation", "Synthetic", "Projection"}, key
        assert entry["source"].startswith("evidence/") and entry["field"], key


def test_no_hand_typed_digits_in_result_cards():
    # Result cards must hold digits only inside number slots.
    html = (SITE / "index.html").read_text()
    proof = html.split('id="proof"')[1].split('id="demo"')[0]
    stripped = sn.SLOT.sub("", proof)
    stripped = re.sub(r'<span class="src">.*?</span>', "", stripped)
    stripped = re.sub(r"<[^>]+>", " ", stripped)
    stripped = re.sub(r"summary\.json|numbers\.json|v\d+|\d{4}Q\d", "", stripped)
    assert not re.search(r"\d", stripped), re.findall(r".{20}\d.{20}", stripped)


def test_no_secret_on_the_site():
    banned = re.compile(
        r"password|passwd|testpass|api[_-]?key|secret|bucket|account[_-]?id|CUST-\d|s3://|abfss://|\.blob\.core",
        re.I,
    )
    for path in SITE.rglob("*"):
        if path.is_file() and path.suffix in {".html", ".css", ".js", ".json", ".svg"}:
            hit = banned.search(path.read_text())
            assert not hit, f"{path.name}: {hit.group(0)}"


def test_no_external_request():
    # Links (<a href>) may leave the site. Loaded resources may not.
    load = re.compile(r'<(?:script|img|link|iframe|source|video|audio)\b[^>]*?(?:src|href)="(?:https?:)?//', re.I)
    for page in PAGES:
        assert not load.search(page.read_text()), page.name
    for css in SITE.rglob("*.css"):
        assert "url(http" not in css.read_text() and "@import" not in css.read_text(), css.name


def test_page_details():
    for page in PAGES:
        html = page.read_text()
        assert re.search(r'<html lang="(en|es-419|pt-BR)">', html) and "<title>" in html, page.name
        assert 'name="viewport"' in html, page.name
    home = (SITE / "index.html").read_text()
    assert 'name="description"' in home and 'rel="icon"' in home
    assert (SITE / "404.html").exists() and (SITE / "favicon.svg").exists()
    assert "prefers-color-scheme: dark" in (SITE / "style.css").read_text()


def test_product_page_numbers_match_the_evidence():
    page = (sn.ROOT / "docs" / "product.md").read_text()
    flows = json.loads((sn.EVIDENCE / "flows/2024Q4-v3/summary.json").read_text())
    problem = json.loads((sn.EVIDENCE / "problem/dev-v1/summary.json").read_text())
    expected = [
        f"{flows['accounts']['reason_transaccional']:,} of {flows['accounts']['n_calls']:,} calls",
        f"{flows['disputes']['unrecognized_claim']} of {flows['disputes']['n']:,}",
        f"{problem['hours']['transaction_dispute']['hours_per_month']}",
        f"{problem['reasons']['Queja']['share_pct']}%",
    ]
    for text in expected:
        assert text in page, f"docs/product.md does not show {text!r}"


# --- architecture drawing (tasks 2.4 and 4.1) ---

import build_architecture as ba  # noqa: E402


def test_architecture_files_are_current():
    for path, text in ba.outputs().items():
        assert path.read_text() == text, f"{path.name} is stale: run scripts/build_architecture.py"


def test_architecture_evidence_paths_exist():
    data = ba.load()
    ids = {n["id"] for n in data["nodes"]}
    assert len(ids) == len(data["nodes"])
    for n in data["nodes"]:
        assert n["status"] in {"real", "mock", "synthetic"} and n["decides"] in ba.DECIDES
        assert n["evidence"], n["id"]
        for rel in n["evidence"]:
            assert (sn.ROOT / rel).exists(), f"{n['id']}: missing {rel}"
        for key in n["metrics"]:
            assert key in sn.METRICS, f"{n['id']}: unknown number {key}"
    for e in data["edges"]:
        assert e["from"] in ids and e["to"] in ids


def test_architecture_nodes_are_keyboard_operable():
    html = (SITE / "diagrams" / "architecture.html").read_text()
    for n in ba.load()["nodes"]:
        assert f'id="n-{n["id"]}"' in html and f'id="d-{n["id"]}"' in html
    assert html.count('role="button" aria-label=') == len(ba.load()["nodes"])
    assert html.count('tabindex="0"') >= len(ba.load()["nodes"])
    # No library, no external request: one local script.
    assert html.count("<script") == 2 and 'src="architecture.js"' in html and 'src="../lang.js"' in html


def test_every_mock_names_its_production_replacement():
    for n in ba.load()["nodes"]:
        if n["status"] == "mock":
            assert n["prod"] and n["prod_short"] and n["prod"] != n["runs"], n["id"]


def test_architecture_page_in_the_browser():
    pytest = __import__("pytest")
    sync = pytest.importorskip("playwright.sync_api")
    chromium = next((p for p in ("/usr/bin/chromium", "/usr/bin/chromium-browser", "/usr/bin/google-chrome") if Path(p).exists()), None)
    if not chromium:
        pytest.skip("no Chromium found")
    url = (SITE / "diagrams" / "architecture.html").as_uri()
    with sync.sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path=chromium, args=["--no-sandbox"])
        errors = []
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        page.on("pageerror", lambda e: errors.append(str(e)))
        requests = []
        page.on("request", lambda r: requests.append(r.url))
        page.goto(url)
        page.click("#n-gold")
        assert page.inner_text(".detail.on h3") == "Gold store"
        page.click("[data-view=prod]")
        assert "Gold on Databricks" in page.text_content("#n-gold")
        page.click("[data-view=demo]")
        assert "Labelled in-memory mock" in page.text_content("#n-gold")
        page.focus("#n-policy")
        page.keyboard.press("Enter")
        assert page.inner_text(".detail.on h3") == "Policy engine"
        phone = browser.new_page(viewport={"width": 390, "height": 800})
        phone.goto(url)
        assert not phone.evaluate("document.documentElement.scrollWidth > innerWidth")
        browser.close()
    assert not errors
    assert all(u.startswith("file:") for u in requests), requests


# --- slides (task 3.2) ---

DECK = SITE / "slides" / "deck.html"


def test_deck_has_six_slides_with_the_right_order():
    html = DECK.read_text()
    assert html.count('<section class="slide"') == 6
    labels = re.findall(r'<section class="slide" id="s\d" aria-label="([^"]+)"', html)
    assert labels == ["Why", "What", "How", "Proof", "For the bank", "Limits and roadmap"]
    assert "The AI talks." in html and "The rules decide." in html
    assert "architecture-light.svg" in html


def test_deck_numbers_only_in_number_slots():
    html = DECK.read_text()
    outside = sn.SLOT.sub("", html)
    outside = re.sub(r"<style.*?</style>|<script.*?</script>", "", outside, flags=re.S)
    for key, entry in json.loads(sn.OUT.read_text())["numbers"].items():
        text = entry["text"]
        if len(text) >= 3:
            assert text not in outside, f"{key} ({text}) is typed by hand in the deck"


def test_deck_in_the_browser_and_pdf():
    pytest = __import__("pytest")
    sync = pytest.importorskip("playwright.sync_api")
    chromium = next((p for p in ("/usr/bin/chromium", "/usr/bin/chromium-browser", "/usr/bin/google-chrome") if Path(p).exists()), None)
    if not chromium:
        pytest.skip("no Chromium found")
    with sync.sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path=chromium, args=["--no-sandbox"])
        page = browser.new_page(viewport={"width": 1280, "height": 784})
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.goto(DECK.as_uri())
        assert page.locator(".slide.on").count() == 1
        for _ in range(7):
            page.keyboard.press("ArrowRight")
        assert page.locator(".slide.on").get_attribute("id") == "s6"
        page.keyboard.press("Home")
        assert page.locator(".slide.on").get_attribute("id") == "s1"
        page.emulate_media(media="print")
        assert page.locator(".slide").evaluate_all("els => els.every(e => getComputedStyle(e).display !== 'none')")
        browser.close()
    assert not errors


def test_markdown_number_marks_match_the_evidence():
    assert sn.sync_markdown(json.loads(sn.OUT.read_text())["numbers"], check=True) == []


# --- all diagrams (task 4.6) ---

import build_cases as bc  # noqa: E402
import build_evidence as be  # noqa: E402

DIAGRAMS = ["architecture", "cases", "evidence", "turn"]


def test_cases_and_evidence_files_are_current():
    import build_turn as bt
    for mod in (bc, be, bt):
        for path, text in mod.outputs().items():
            assert path.read_text() == text, f"{path.name} is stale: run scripts/{mod.__name__}.py"


def test_evidence_text_holds_no_typed_number():
    # Prose is free of digits. Every digit on a bar comes from numbers.json.
    for s in json.loads(sn.OUT.read_text())["series"]:
        assert not re.search(r"\d", s["about"]), s["id"]
        assert s["type"] in {"Test suite", "Simulation", "Synthetic", "Projection"}
        for row in s["rows"]:
            assert row["field"] and row["n_field"], (s["id"], row["label"])
    html = (SITE / "diagrams" / "evidence.html").read_text()
    assert html.count("<script") == 2 and 'src="evidence.js"' in html and 'src="../lang.js"' in html


def test_cases_page_uses_the_real_demo_lines_and_package_fields():
    html = (SITE / "diagrams" / "cases.html").read_text()
    replay = (sn.ROOT / "sentinel-ai-core/eval/demo/replay.md").read_text()
    for c in bc.CASES:
        assert c["line"] in replay, f"demo line of {c['id']} is not in replay.md"
    schema = (sn.ROOT / "sentinel-ai-core/app/schemas/chat.py").read_text()
    package = schema.split("class HandoffPackage")[1].split("class Handoff(")[0]
    for name, _ in bc.PACKAGE:
        for field in name.split(", "):
            assert f"{field}:" in package, f"{field} is not a HandoffPackage field"
    assert 'id="package"' in html


def test_every_diagram_in_the_browser():
    pytest = __import__("pytest")
    sync = pytest.importorskip("playwright.sync_api")
    chromium = next((p for p in ("/usr/bin/chromium", "/usr/bin/chromium-browser", "/usr/bin/google-chrome") if Path(p).exists()), None)
    if not chromium:
        pytest.skip("no Chromium found")
    with sync.sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path=chromium, args=["--no-sandbox"])
        for name in DIAGRAMS:
            url = (SITE / "diagrams" / f"{name}.html").as_uri()
            for width in (1280, 390):
                page = browser.new_page(viewport={"width": width, "height": 800})
                errors, requests = [], []
                page.on("pageerror", lambda e: errors.append(str(e)))
                page.on("request", lambda r: requests.append(r.url))
                page.goto(url)
                assert not errors, (name, errors)
                assert all(u.startswith("file:") for u in requests), (name, requests)
                assert not page.evaluate("document.documentElement.scrollWidth > innerWidth"), (name, width)
                page.close()
            # Keyboard: every tab or node is reachable and works with the keys.
            page = browser.new_page(viewport={"width": 1280, "height": 800})
            page.goto(url)
            if name == "architecture":
                page.focus("#n-gold")
                page.keyboard.press("Enter")
                assert page.inner_text(".detail.on h3") == "Gold store"
            elif name == "turn":
                page.locator("[data-go]").nth(0).focus()
                page.keyboard.press("Enter")
                page.click("#next")
                assert page.inner_text(".tstep.on h3").startswith("2.")
            else:
                tabs = page.locator("[role=tab]")
                assert tabs.count() >= 3
                tabs.nth(0).focus()
                page.keyboard.press("ArrowRight")
                assert page.locator("[role=tab][aria-selected=true]").get_attribute("data-tab") == tabs.nth(1).get_attribute("data-tab")
            # Without JS the content is still on the page.
            nojs = browser.new_context(java_script_enabled=False).new_page()
            nojs.goto(url)
            assert len(nojs.inner_text("main")) > 400, name
            page.close()
        browser.close()


def test_home_page_links_every_diagram_and_the_slides():
    home = (SITE / "index.html").read_text()
    for target in ("diagrams/architecture.html", "diagrams/cases.html", "diagrams/evidence.html", "slides/deck.html"):
        assert f'href="{target}"' in home, target
        assert (SITE / target).exists()
    assert 'property="og:image"' in home and (SITE / "preview.png").exists()
    assert 'id="limits"' in home


def test_turn_page_uses_demo_lines_and_real_stops():
    import build_turn as bt
    replay = (sn.ROOT / "sentinel-ai-core/eval/demo/replay.md").read_text()
    for sample in bt.SAMPLES:
        assert sample["text"] in replay, sample["id"]
    assert len(bt.STEPS) == 7
    assert [s["decides"] for s in bt.STEPS].count("model") == 1
    for step in bt.STEPS:
        for rel in step["evidence"]:
            assert (sn.ROOT / rel).exists(), f"{step['id']}: missing {rel}"


def test_judges_page_commands_and_links_exist():
    html = (SITE / "judges.html").read_text()
    code = re.search(r"<pre><code>(.*?)</code></pre>", html, re.S).group(1)
    assert "git clone https://github.com/" in code and "pip install -e" in code
    assert (sn.ROOT / "sentinel-ai-core/eval/run.py").exists() and "-m eval.run verify" in code
    run = re.search(r"verify (\S+)", code).group(1)
    assert (sn.ROOT / "evidence/evaluation-runs" / run / "summary.json").exists()
    env = (sn.ROOT / ".env.example").read_text()
    for name in re.findall(r"export (SENTINEL_\w+)=", code):
        assert name in env, name
    extras = (sn.ROOT / "sentinel-ai-core/pyproject.toml").read_text()
    assert "dev = [" in extras and "eval = [" in extras
    assert (sn.ROOT / "sentinel-ai-core/tests/adversarial").is_dir()
    # Every repository link of the page points to a file that exists.
    base = "https://github.com/rdorta27/sentinel-engine/blob/main/"
    for rel in re.findall(re.escape(base) + r"([^\"#]+)", html):
        assert (sn.ROOT / rel).exists(), rel


def test_judges_page_in_the_browser():
    pytest = __import__("pytest")
    sync = pytest.importorskip("playwright.sync_api")
    chromium = next((p for p in ("/usr/bin/chromium", "/usr/bin/chromium-browser", "/usr/bin/google-chrome") if Path(p).exists()), None)
    if not chromium:
        pytest.skip("no Chromium found")
    url = (SITE / "judges.html").as_uri()
    with sync.sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path=chromium, args=["--no-sandbox"])
        page = browser.new_page(viewport={"width": 390, "height": 800})
        requests = []
        page.on("request", lambda r: requests.append(r.url))
        page.goto(url)
        assert not page.evaluate("document.documentElement.scrollWidth > innerWidth")
        page.locator("summary").first.click()
        assert page.locator("details[open]").count() == 1
        assert all(u.startswith("file:") for u in requests), requests
        browser.close()


# --- languages: English, Spanish (es-419) and Portuguese (pt-BR) ---

import localize as lz  # noqa: E402
import site_chrome as chrome  # noqa: E402

LANGS = ["en", "es-419", "pt-br"]


def lang_path(lang: str, page: str) -> Path:
    return SITE / page if lang == "en" else SITE / lang / page


def test_language_copies_are_current_and_complete():
    outputs, translators = lz.build()
    for lang, tr in translators.items():
        assert not tr.missing, f"{lang}: missing {sorted(tr.missing)[:3]}"
        assert not tr.errors, f"{lang}: {tr.errors[:2]}"
    for path, text in outputs.items():
        assert path.read_text() == text, f"{path.relative_to(SITE)} is stale: run scripts/localize.py"


def test_every_page_exists_in_each_language_with_the_same_structure():
    for page in lz.sources():
        base = lang_path("en", page).read_text()
        for lang in LANGS[1:]:
            other = lang_path(lang, page).read_text()
            for pattern in (r"<h[1-3]\b", r"data-num[\w-]*=", r'id="[^"]+"', r"<a ", r"<section\b"):
                assert len(re.findall(pattern, base)) == len(re.findall(pattern, other)), (page, lang, pattern)


def test_navigation_is_the_same_on_every_page():
    for lang in LANGS:
        navs = set()
        for page in lz.sources():
            if not page.endswith(".html") or page.startswith("slides/"):
                continue
            html = lang_path(lang, page).read_text()
            nav = re.search(r'<nav aria-label="[^"]*">(.*?)</nav>', html, re.S).group(1)
            labels = tuple(re.findall(r">([^<]+)</a>", nav))
            navs.add(labels)
            assert 'aria-current="page"' in nav, (lang, page)
            assert html.count('aria-current="true"') == 1, (lang, page)
            assert "<footer>" in html, (lang, page)
        assert len(navs) == 1, (lang, navs)


def test_language_links_and_alternates_resolve():
    for lang in LANGS:
        for page in lz.sources():
            if not page.endswith(".html"):
                continue
            here = lang_path(lang, page)
            html = here.read_text()
            for target in re.findall(r'data-lang="[^"]+" href="([^"]+)"', html):
                assert (here.parent / target).resolve().exists(), (lang, page, target)
            for target in re.findall(r'rel="alternate" hreflang="[^"]+" data-lang="[^"]+" href="([^"]+)"', html):
                assert (here.parent / target).resolve().exists(), (lang, page, target)
            # Every relative asset and page link resolves.
            for target in re.findall(r'(?:href|src)="((?!https?:|mailto:|#|//)[^"#]+)', html):
                assert (here.parent / target).resolve().exists(), (lang, page, target)


def test_demo_lines_stay_in_their_own_language():
    for lang in LANGS:
        html = lang_path(lang, "diagrams/cases.html").read_text()
        assert "Quiero hablar con un asesor." in html and "não reconheço uma cobrança" in html, lang
        assert "Cafe Central" in lang_path(lang, "index.html").read_text()


def test_portuguese_numbers_use_a_decimal_comma():
    pt = lang_path("pt-br", "index.html").read_text()
    en = lang_path("en", "index.html").read_text()
    assert ">81,8%<" in pt and ">81.8%<" in en
    assert ">79.000+<" in pt and ">79,000+<" in en
    es = lang_path("es-419", "index.html").read_text()
    assert ">81.8%<" in es and ">Simulación<" in es and ">Simulação<" in pt


def test_all_languages_in_the_browser():
    pytest = __import__("pytest")
    sync = pytest.importorskip("playwright.sync_api")
    chromium = next((p for p in ("/usr/bin/chromium", "/usr/bin/chromium-browser", "/usr/bin/google-chrome") if Path(p).exists()), None)
    if not chromium:
        pytest.skip("no Chromium found")
    with sync.sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path=chromium, args=["--no-sandbox"])
        for lang in LANGS:
            for page in ("index.html", "judges.html", "diagrams/architecture.html", "diagrams/cases.html", "diagrams/evidence.html", "diagrams/turn.html", "slides/deck.html"):
                for width in (1280, 390):
                    p = browser.new_page(viewport={"width": width, "height": 800})
                    errors, requests = [], []
                    p.on("pageerror", lambda e: errors.append(str(e)))
                    p.on("request", lambda r: requests.append(r.url))
                    p.goto(lang_path(lang, page).as_uri())
                    assert not errors, (lang, page, errors)
                    assert all(u.startswith("file:") for u in requests), (lang, page, requests)
                    if page != "slides/deck.html":
                        assert not p.evaluate("document.documentElement.scrollWidth > innerWidth"), (lang, page, width)
                    p.close()
            # The switcher moves to the same page in the other language.
            p = browser.new_page(viewport={"width": 1280, "height": 800})
            p.goto(lang_path(lang, "diagrams/turn.html").as_uri())
            other = "es-419" if lang != "es-419" else "pt-br"
            p.click(f'.lang a[data-lang="{other}"]')
            assert f"/{other}/diagrams/turn.html" in p.url, (lang, p.url)
            p.close()
        browser.close()


def test_browser_language_is_the_default_and_the_choice_is_kept():
    pytest = __import__("pytest")
    sync = pytest.importorskip("playwright.sync_api")
    chromium = next((p for p in ("/usr/bin/chromium", "/usr/bin/chromium-browser", "/usr/bin/google-chrome") if Path(p).exists()), None)
    if not chromium:
        pytest.skip("no Chromium found")
    home = (SITE / "index.html").as_uri()
    with sync.sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path=chromium, args=["--no-sandbox"])

        def open_home(locale: str):
            ctx = browser.new_context(locale=locale)
            page = ctx.new_page()
            page.goto(home)
            return ctx, page

        for locale, expected in (("es-MX", "/es-419/index.html"), ("es-CO", "/es-419/index.html"), ("pt-BR", "/pt-br/index.html"), ("en-US", "/site/index.html"), ("fr-FR", "/site/index.html")):
            ctx, page = open_home(locale)
            assert page.url.endswith(expected), (locale, page.url)
            ctx.close()
        # A Spanish page that someone opens directly stays in Spanish.
        ctx = browser.new_context(locale="en-US")
        page = ctx.new_page()
        page.goto((SITE / "es-419" / "index.html").as_uri())
        assert page.url.endswith("/es-419/index.html")
        # The visitor changes the language. The choice stays for the next visit.
        page.click('.lang a[data-lang="pt-br"]')
        assert page.url.endswith("/pt-br/index.html")
        page.goto(home)
        assert page.url.endswith("/pt-br/index.html"), page.url
        page.click('.lang a[data-lang="en"]')
        assert page.url.endswith("/site/index.html")
        page.goto(home)
        assert page.url.endswith("/site/index.html"), "English was chosen: no redirect"
        ctx.close()
        # An English browser that chose Spanish earlier keeps Spanish. A Spanish browser that chose English keeps English.
        ctx = browser.new_context(locale="es-MX")
        page = ctx.new_page()
        page.goto(home)
        assert page.url.endswith("/es-419/index.html")
        page.click('.lang a[data-lang="en"]')
        page.goto(home)
        assert page.url.endswith("/site/index.html")
        ctx.close()
        browser.close()


def test_no_text_leaves_its_box_in_any_language():
    pytest = __import__("pytest")
    pytest.importorskip("playwright.sync_api")
    if not any(Path(p).exists() for p in ("/usr/bin/chromium", "/usr/bin/chromium-browser", "/usr/bin/google-chrome")):
        pytest.skip("no Chromium found")
    import audit_overflow as ao
    findings = ao.audit()
    assert not findings, "\n".join(findings[:10])


def test_screenshots_are_on_the_home_page():
    home = (SITE / "index.html").read_text()
    shots = re.findall(r'<img src="(screenshots/[^"]+)"[^>]*alt="([^"]+)"', home)
    assert len(shots) == 4
    for src, alt in shots:
        assert (SITE / src).exists() and len(alt) > 20, src


def test_language_in_the_address_wins_over_the_browser():
    pytest = __import__("pytest")
    sync = pytest.importorskip("playwright.sync_api")
    chromium = next((p for p in ("/usr/bin/chromium", "/usr/bin/chromium-browser", "/usr/bin/google-chrome") if Path(p).exists()), None)
    if not chromium:
        pytest.skip("no Chromium found")
    home = (SITE / "index.html").as_uri()
    with sync.sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path=chromium, args=["--no-sandbox"])
        # A Spanish browser that opens the link with ?lang=en reads English, and the choice is kept.
        ctx = browser.new_context(locale="es-MX")
        page = ctx.new_page()
        page.goto(home + "?lang=en")
        assert page.url.split("?")[0].endswith("/site/index.html")
        page.goto(home)
        assert page.url.endswith("/site/index.html"), page.url
        ctx.close()
        # The address can also ask for another language, even from a translated page.
        ctx = browser.new_context(locale="en-US")
        page = ctx.new_page()
        page.goto(home + "?lang=pt")
        assert "/pt-br/index.html" in page.url, page.url
        page.goto((SITE / "pt-br" / "index.html").as_uri() + "?lang=es")
        assert "/es-419/index.html" in page.url, page.url
        ctx.close()
        browser.close()
