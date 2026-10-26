#!/usr/bin/env python3
"""Write site/numbers.json from the frozen summary.json runs.

Every number on the site comes from here. Each entry keeps its source run,
its field path, its denominator and its data type (what-is-real labels).

    python3 scripts/site_numbers.py          # write site/numbers.json
    python3 scripts/site_numbers.py --check  # exit 1 if the file is stale
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
OUT = ROOT / "site" / "numbers.json"

ADV = "adversarial/20261005T014816Z"
ADV_REAL = "adversarial/20261005T204313Z"
EVAL = "evaluation-runs/2024Q4-eval-v8"
RES = "evaluation-runs/2024Q4-resolution-v2"
PROBLEM = "problem/dev-v1"
GAP = "evaluation-runs/2024Q4-resolution-gap-v1"
CUT = "evaluation-runs/2024Q4-cutoff-diagnosis-v1"

# id -> (run, field path, format, type label, denominator path or None, text)
# Formats: int, pct (0..1 to percent), pct_raw (already percent), str, float1, usd4.
METRICS: dict[str, tuple] = {
    "adv_attempted": (ADV, "totals.attempted", "int", "Test suite", None,
                      "attacks tried"),
    "adv_rate": (ADV, "totals.unsafe_outcome_rate", "str", "Test suite", None,
                 "attacks with an unsafe outcome"),
    "adv_blocked": (ADV, "totals.blocked_verified", "int", "Test suite",
                    "totals.attempted", "blocked by production code"),
    "adv_mock": (ADV, "totals.passes_on_mock", "int", "Test suite",
                 "totals.attempted", "safe only with the mock model"),
    "adv_real": (ADV_REAL, "totals.unsafe_outcome_rate", "str", "Test suite", None,
                 "mock-only attacks with an unsafe outcome on the real model"),
    "intent_baseline": (EVAL, "candidates.baseline.intent.accuracy",
                        "pct", "Simulation",
                        "candidates.baseline.intent.n",
                        "intent accuracy of the keyword baseline"),
    "intent_router": (EVAL, "candidates.router_v2.intent.accuracy",
                      "pct", "Simulation",
                      "candidates.router_v2.intent.n",
                      "intent accuracy of the LLM router"),
    "intent_n": (EVAL, "candidates.router_v2.intent.n", "int", "Simulation", None,
                 "held-out turns in the intent test"),
    "res_resolved": (RES, "system.router_v2.safe_resolution.resolved", "int",
                     "Simulation", "system.router_v2.safe_resolution.n",
                     "cases resolved safely"),
    "res_n": (RES, "system.router_v2.safe_resolution.n", "int", "Simulation",
              None, "resolution cases"),
    "res_unsafe": (RES, "system.router_v2.unsafe_outcomes.rate", "str",
                   "Simulation", None, "unsafe outcomes in the resolution run"),
    "res_net": (RES, "paired_resolution.net", "int", "Simulation",
                "paired_resolution.n",
                "net cases gained by the router over the baseline"),
    "ceil_resolvable": (GAP, "ceiling.router_v2.resolvable", "int", "Simulation",
                        "ceiling.router_v2.n", "cases that the policy lets the system resolve"),
    "ceil_resolved": (GAP, "ceiling.router_v2.resolved", "int", "Simulation",
                      "ceiling.router_v2.resolvable", "of the resolvable cases resolved"),
    "lang_es_ar": (EVAL, "candidates.router_v2.variant_losses.by_variant.es-AR.accuracy", "pct", "Simulation", "candidates.router_v2.variant_losses.by_variant.es-AR.n", "intent accuracy on es-AR"),
    "lang_es_co": (EVAL, "candidates.router_v2.variant_losses.by_variant.es-CO.accuracy", "pct", "Simulation", "candidates.router_v2.variant_losses.by_variant.es-CO.n", "intent accuracy on es-CO"),
    "lang_es_mx": (EVAL, "candidates.router_v2.variant_losses.by_variant.es-MX.accuracy", "pct", "Simulation", "candidates.router_v2.variant_losses.by_variant.es-MX.n", "intent accuracy on es-MX"),
    "lang_pt_br": (EVAL, "candidates.router_v2.variant_losses.by_variant.pt-BR.accuracy", "pct", "Simulation", "candidates.router_v2.variant_losses.by_variant.pt-BR.n", "intent accuracy on pt-BR"),
    "cost_per_resolution": (RES, "system.router_v2.cost_usd.per_resolution", "usd4",
                            "Simulation", None, "model cost per safe resolution"),
    "intent_v3": (EVAL, "candidates.router_v3.intent.accuracy", "pct", "Simulation",
                  "candidates.router_v3.intent.n", "intent accuracy of prompt v3, not served"),
    "v3_unsafe": (EVAL, "candidates.router_v3.unsafe_wording.count", "int", "Simulation",
                  "candidates.router_v3.unsafe_wording.n", "unsafe drafts of prompt v3"),
    "problem_calls": (PROBLEM, "totals.calls", "int", "Synthetic", None,
                      "calls in the development window"),
    "problem_dispute_calls": (PROBLEM, "demand.transaction_dispute.calls", "int",
                              "Synthetic", "totals.calls",
                              "calls about a transaction dispute"),
    "problem_dispute_hours": (PROBLEM, "hours.transaction_dispute.hours_per_month",
                              "float1", "Synthetic", None,
                              "agent hours per month on disputes"),
    "problem_dispute_resolved": (PROBLEM, "reasons.Queja.share_pct", "pct_raw",
                                 "Synthetic", "reasons.Queja.n",
                                 "of dispute calls end resolved"),
}


# Series for the evidence explorer. Each row reads one field of a frozen run.
# kind: rate (0..1 with n), count (value of denominator) or scale (value with unit).
SERIES: list[dict] = [
    {
        "id": "intent", "title": "Intent accuracy", "type": "Simulation", "run": EVAL, "kind": "rate",
        "about": "The intent router against the keyword baseline on the same sealed held-out turns. The cases are team-written, not production traffic.",
        "rows": [
            ("Keyword baseline", "candidates.baseline.breakdown_overall.accuracy", "candidates.baseline.breakdown_overall.n", "candidates.baseline.breakdown_overall.interval_95"),
            ("LLM router, final version", "candidates.router_v2.breakdown_overall.accuracy", "candidates.router_v2.breakdown_overall.n", "candidates.router_v2.breakdown_overall.interval_95"),
            ("Prompt v3, not served: it failed the safety gate", "candidates.router_v3.breakdown_overall.accuracy", "candidates.router_v3.breakdown_overall.n", "candidates.router_v3.breakdown_overall.interval_95"),
        ],
    },
    {
        "id": "language", "title": "By language", "type": "Simulation", "run": EVAL, "kind": "rate",
        "about": "Intent accuracy of the final LLM router for each variant. Each variant holds the same cases, written in that variant. The Portuguese cases are model-written and no native speaker reviewed them.",
        "rows": [
            ("es-AR", "candidates.router_v2.variant_losses.by_variant.es-AR.accuracy", "candidates.router_v2.variant_losses.by_variant.es-AR.n"),
            ("es-CO", "candidates.router_v2.variant_losses.by_variant.es-CO.accuracy", "candidates.router_v2.variant_losses.by_variant.es-CO.n"),
            ("es-MX", "candidates.router_v2.variant_losses.by_variant.es-MX.accuracy", "candidates.router_v2.variant_losses.by_variant.es-MX.n"),
            ("pt-BR", "candidates.router_v2.variant_losses.by_variant.pt-BR.accuracy", "candidates.router_v2.variant_losses.by_variant.pt-BR.n"),
        ],
    },
    {
        "id": "resolution", "title": "Resolution ceiling", "type": "Simulation", "run": GAP, "kind": "count",
        "about": "The policy sets a ceiling on how many simulated cases may resolve. Both systems resolve every case under the ceiling, so the two systems do not differ. The set cannot separate the two systems on resolution.",
        "rows": [
            ("Cases the policy lets resolve", "ceiling.router_v2.resolvable", "ceiling.router_v2.n"),
            ("Resolved by the baseline", "ceiling.baseline.resolved", "ceiling.baseline.n"),
            ("Resolved by the LLM router", "ceiling.router_v2.resolved", "ceiling.router_v2.n"),
        ],
    },
    {
        "id": "cutoff", "title": "Confidence cut-off", "type": "Simulation", "run": CUT, "kind": "rate",
        "about": "Kind accuracy of the router with and without a confidence cut-off. The confidence of the model is saturated near the top. A cut-off near the top removes correct answers, not errors. The run holds three settings and no curve, so this page shows the three settings and no slider. The cut-offs stay off.",
        "rows": [
            ("No cut-offs (our setting)", "kind_accuracy.no_cutoffs.kind_accuracy", "kind_accuracy.no_cutoffs.n"),
            ("Cut-off rounded to the top", "kind_accuracy.t_act_1_0.kind_accuracy", "kind_accuracy.t_act_1_0.n"),
            ("Cut-off before rounding", "kind_accuracy.t_act_unrounded.kind_accuracy", "kind_accuracy.t_act_unrounded.n"),
        ],
    },
    {
        "id": "attacks", "title": "Attacks", "type": "Test suite", "run": ADV, "kind": "count",
        "about": "Each bar shows the attacks that production code stops. The other attacks pass only with the mock model, or are documented limits. No attack has an unsafe outcome.",
        "rows": [
            ("Prompt injection", "categories.A_prompt_injection.blocked_verified", "categories.A_prompt_injection.attempted"),
            ("Unauthorized access", "categories.B_unauthorized_access.blocked_verified", "categories.B_unauthorized_access.attempted"),
            ("Session", "categories.C_session.blocked_verified", "categories.C_session.attempted"),
            ("Tool failures", "categories.D_tool_failures.blocked_verified", "categories.D_tool_failures.attempted"),
            ("Multilingual ambiguity", "categories.E_multilingual_ambiguity.blocked_verified", "categories.E_multilingual_ambiguity.attempted"),
            ("Decision disclosure", "categories.F_decision_disclosure.blocked_verified", "categories.F_decision_disclosure.attempted"),
            ("All attacks", "totals.blocked_verified", "totals.attempted"),
        ],
        "extra": [("Unsafe outcomes, all attacks", "totals.unsafe_outcome_rate")],
    },
    {
        "id": "latency", "title": "Latency", "type": "Simulation", "run": EVAL, "kind": "scale", "unit": "ms",
        "mode": "Live model calls on simulation cases",
        "about": "Time of one routed turn with the LLM router, in milliseconds. The calls are live. The cases are team-written.",
        "rows": [
            ("Median (p50)", "candidates.router_v2.latency_ms.p50", "candidates.router_v2.latency_ms.n"),
            ("Slow turn (p95)", "candidates.router_v2.latency_ms.p95", "candidates.router_v2.latency_ms.n"),
        ],
    },
    {
        "id": "replay", "title": "Latency of a replay", "type": "Simulation", "run": RES, "kind": "scale", "unit": "ms",
        "mode": "Replay of recorded model answers, no live call",
        "about": "The resolution run replays recorded answers. It measures the code, not the model. Do not compare it with the live latency.",
        "rows": [
            ("Median (p50)", "system.router_v2.latency_ms.p50", "system.router_v2.latency_ms.n"),
            ("Slow turn (p95)", "system.router_v2.latency_ms.p95", "system.router_v2.latency_ms.n"),
        ],
    },
    {
        "id": "cost", "title": "Cost", "type": "Simulation", "run": EVAL, "kind": "scale", "unit": "USD",
        "mode": "Live model calls on simulation cases",
        "about": "Total price of the live calls of each router on the same turns. The prices come from the Fireworks model library, as the router models decision records.",
        "rows": [
            ("LLM router, final version", "candidates.router_v2.cost_usd.total", "candidates.router_v2.cost_usd.n"),
        ],
    },
]


def build_series(runs_cache: dict, evidence: Path) -> list[dict]:
    out = []
    for sdef in SERIES:
        run = sdef["run"]
        if run not in runs_cache:
            runs_cache[run] = json.loads((evidence / run / "summary.json").read_text())
        data = runs_cache[run]
        rows = []
        for label, vpath, dpath, *ci in sdef["rows"]:
            row = {"label": label, "value": dig(data, vpath), "n": dig(data, dpath), "field": vpath, "n_field": dpath}
            if ci:
                row["ci"] = dig(data, ci[0])
                row["ci_field"] = ci[0]
            rows.append(row)
        entry = {k: sdef[k] for k in ("id", "title", "type", "kind", "about") if k in sdef}
        entry.update({"source": f"evidence/{run}/summary.json", "rows": rows})
        for k in ("unit", "mode"):
            if k in sdef:
                entry[k] = sdef[k]
        if "extra" in sdef:
            entry["extra"] = [{"label": lb, "value": dig(data, pth), "field": pth} for lb, pth in sdef["extra"]]
        out.append(entry)
    return out


def dig(obj, path: str):
    for part in path.split("."):
        obj = obj[part]
    return obj


def fmt(value, kind: str) -> str:
    if kind == "int":
        return f"{int(value):,}"
    if kind == "pct":
        return f"{value * 100:.1f}%"
    if kind == "pct_raw":
        return f"{value:.1f}%"
    if kind == "float1":
        return f"{value:,.1f}"
    if kind == "usd4":
        return f"USD {value:.4f}"
    return str(value)


def rounded(entry: dict) -> str:
    """A reading form for a large count: 79,191 becomes 79,000+ and 390.8 becomes 390+."""
    value = entry["value"]
    if isinstance(value, (int, float)) and value >= 1000:
        return f"{int(value) // 1000 * 1000:,}+"
    if isinstance(value, (int, float)) and value >= 100:
        return f"{int(value) // 10 * 10:,}+"
    return entry["text"]


def build(evidence: Path = EVIDENCE) -> dict:
    runs: dict[str, dict] = {}
    numbers: dict[str, dict] = {}
    for key, (run, path, kind, label, denom, text) in METRICS.items():
        if run not in runs:
            runs[run] = json.loads((evidence / run / "summary.json").read_text())
        value = dig(runs[run], path)
        entry = {
            "text": fmt(value, kind),
            "value": value,
            "type": label,
            "label": text,
            "source": f"evidence/{run}/summary.json",
            "field": path,
        }
        if denom:
            entry["denominator"] = dig(runs[run], denom)
            entry["denominator_field"] = denom
        numbers[key] = entry
    return {
        "note": "Generated by scripts/site_numbers.py from frozen summary.json runs. Do not edit.",
        "numbers": numbers,
        "series": build_series(runs, evidence),
    }


def render(data: dict) -> str:
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


# <span data-num="id">, data-num-round="id", data-num-type="id" and
# data-num-den="id" hold no nested tags. The script writes their text from
# numbers.json. data-num-round shows a large count in a reading form (79,000+).
SLOT = re.compile(
    r'(<(\w+)[^>]*?\bdata-(num|num-round|num-type|num-den)="(\w+)"[^>]*>)(.*?)(</\2>)',
    re.S,
)


# Markdown pages use <!--n:key-->text<!--/n--> (invisible when rendered).
# <!--n~:key--> writes the reading form of a large count (79,000+).
MD_SLOT = re.compile(r"(<!--n(~?):(\w+)-->)(.*?)(<!--/n-->)", re.S)
MD_FILES: list[Path] = []


def sync_markdown(numbers: dict, check: bool = False) -> list[Path]:
    changed = []
    for page in MD_FILES:
        if not page.exists():
            continue
        old = page.read_text()
        new = MD_SLOT.sub(
            lambda m: m.group(1) + (rounded(numbers[m.group(3)]) if m.group(2) else numbers[m.group(3)]["text"]) + m.group(5),
            old,
        )
        if new != old:
            changed.append(page)
            if not check:
                page.write_text(new)
    return changed


TYPE_NAMES = {
    "es-419": {"Test suite": "Suite de pruebas", "Simulation": "Simulación", "Synthetic": "Sintético", "Projection": "Proyección"},
    "pt-br": {"Test suite": "Suíte de testes", "Simulation": "Simulação", "Synthetic": "Sintético", "Projection": "Projeção"},
}


def loc(text: str, lang: str) -> str:
    """Decimal comma and thousands point for Portuguese. English and Spanish keep the point."""
    return text.translate(str.maketrans(",.", ".,")) if lang == "pt-br" else text


def slot_text(numbers: dict, kind: str, key: str, lang: str = "en") -> str:
    entry = numbers[key]
    if kind == "num":
        return loc(entry["text"], lang)
    if kind == "num-round":
        return loc(rounded(entry), lang)
    if kind == "num-type":
        return TYPE_NAMES.get(lang, {}).get(entry["type"], entry["type"])
    return loc(f"{int(entry['denominator']):,}", lang)


def page_lang(page: Path, site: Path) -> str:
    first = page.relative_to(site).parts[0]
    return first if first in ("es-419", "pt-br") else "en"


def sync_pages(data: dict, site: Path = OUT.parent) -> list[Path]:
    """Rewrite the text of each number slot. Return the pages that changed."""
    changed = []
    for page in sorted(site.rglob("*.html")):
        old = page.read_text()
        lang = page_lang(page, site)
        new = SLOT.sub(
            lambda m: m.group(1) + slot_text(data["numbers"], m.group(3), m.group(4), lang) + m.group(6),
            old,
        )
        if new != old:
            page.write_text(new)
            changed.append(page)
    return changed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    data = build()
    text = render(data)
    if args.check:
        stale = not OUT.exists() or OUT.read_text() != text
        for page in OUT.parent.rglob("*.html"):
            if SLOT.sub(lambda m: m.group(1) + slot_text(data["numbers"], m.group(3), m.group(4), page_lang(page, OUT.parent)) + m.group(6),
                        page.read_text()) != page.read_text():
                print(f"stale number in {page.relative_to(ROOT)}")
                stale = True
        for page in sync_markdown(data["numbers"], check=True):
            print(f"stale number in {page.relative_to(ROOT)}")
            stale = True
        if stale:
            print("The site is stale. Run scripts/site_numbers.py.")
            return 1
        print("The site numbers are current.")
        return 0
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(text)
    pages = sync_pages(data) + sync_markdown(data["numbers"])
    print(f"wrote {OUT.relative_to(ROOT)} ({len(METRICS)} numbers), updated {len(pages)} page(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
