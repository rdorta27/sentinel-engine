---
language: en
style: ASD-STE100
last_reviewed: 2026-10-05
---

# What is real and what is not

This page tells which parts of the submission are real, which are mocks, and which numbers are simulations or projections. The brief asks for this split ("Identify which inputs are real, de-identified, synthetic, or team-generated"; REQ-0031, REQ-0032).

Use these labels in every document, slide and evidence run:

| Label | Meaning |
|---|---|
| **Real** | The component or value is the same in production. |
| **Synthetic** | The hackathon dataset. The organizers generated it. No value is a real customer. |
| **Team-generated** | The team or a model wrote it for this project. |
| **Mock** | A stand-in with the same contract as the production component. Production replaces the backend, not the code. |
| **Simulation** | A measurement on team-generated cases, not on production traffic. |
| **Projection** | A calculation from assumed values. It is not a measurement. |

## Components

| Component | Status | What runs | What production uses |
|---|---|---|---|
| Orchestrator, policy engine, confirm box, read-back | **Real** | The production code | The same code |
| Intent router (LLM) | **Real** | GLM 5.3 Flash on Fireworks AI, with live calls ([016](../build/decisions/016-router-models.md)) | The same weights on Azure AI Foundry or Databricks |
| Keyword baseline | **Real** | The per-turn fallback when the model fails | The same code |
| Personal-data masking before the model | **Real** | The production code (`app/privacy/`) | The same code |
| Turn records and logs | **Real** | JSON lines to Log Analytics on the public link | The same records |
| Data pipeline (Bronze, Silver, Gold) | **Real** code, run locally | `sentinel_data` on DuckDB | The same package on Databricks |
| Gold on the public link | **Mock** | A labelled in-memory store (`app/tools/gold.py`) | Gold on Databricks |
| Gold on a local run | **Real** code, **Synthetic** data | The PII-free DuckDB view, when the file is present | Gold on Databricks |
| Login and session | **Mock** | Test users with a password fixture. The public link reads a test users file and sends the credentials in the submission email; the fixture passwords do not work there | The bank identity provider |
| Advisor | **Mock** | A demo advisor user with a read-only ticket view | A human advisor; tickets go to the bank CRM through a queue ([015](../build/decisions/015-handoff-delivery.md)) |
| Case store | **Mock** | SQLite, with the same models | PostgreSQL |
| Dispute policy (window, fraud and amount thresholds) | **Mock**, labelled `synthetic: true` | Team-written country files ([021](../build/decisions/021-dispute-policy-sources.md)) | The bank approved policy |
| Opening a dispute | **Mock** | The case store records the case. No bank system receives it. | The bank dispute system |
| Secrets | **Mock** | `.env`, gitignored | Azure Key Vault |

The [demo architecture](demo-architecture.md#mocked-components) shows the mocks in the diagrams. The [mocks](mocks.md) page explains each one.

## Data

| Data | Status | Note |
|---|---|---|
| Customers, products, transactions, calls, complaints | **Synthetic** | The organizers' dataset. Text is Spanish only. |
| Transcripts | **Synthetic** | Two Spanish templates. They are not customer language ([evidence](../../evidence/transcript-chats/20261002T144836Z/summary.json)). |
| `fraud_score` and `is_fraud` | **Synthetic** | A score above 30 is always fraud. This is an artefact of the generator ([evidence](../../evidence/customer-360/dev-signals-v1/README.md)). |
| Product balance | **Synthetic**, not used | It has no usable as-of date ([evidence](../../evidence/customer-360/dev-v1/README.md)). |
| Evaluation conversations (es-419, pt-BR) | **Team-generated** | Model-written and model-reviewed. No native speaker reviewed the Portuguese ([018](../build/decisions/018-evaluation-acceptance.md)). |
| Demo personas and their charges on the public link | **Team-generated** | The labelled Gold mock |
| Policy values | **Team-generated** | The p95 thresholds come from the synthetic dataset. The 90-day window is a declared demonstration value. |

## Numbers

| Number | Status | Source |
|---|---|---|
| Router accuracy against the baseline | **Simulation** | The sealed [`2024Q4-eval-v8`](../../evidence/evaluation-runs/2024Q4-eval-v8/summary.json) run, `candidates.<version>.intent.accuracy`. It set the verdict: the link serves `router_v2`. The earlier [`2024Q4-eval-v7`](../../evidence/evaluation-runs/2024Q4-eval-v7/summary.json) is superseded |
| Safe automated resolution | **Simulation** on the **Mock** store | [`2024Q4-resolution-v2`](../../evidence/evaluation-runs/2024Q4-resolution-v2/summary.json) and the ceiling run [`2024Q4-resolution-gap-v1`](../../evidence/evaluation-runs/2024Q4-resolution-gap-v1/summary.json) |
| Unsafe outcomes on attacks | **Test suite** | [`adversarial/20261005T014816Z`](../../evidence/adversarial/20261005T014816Z/summary.json). The three cases that pass only on the mock model also run on the real model in [`adversarial/20261005T204313Z`](../../evidence/adversarial/20261005T204313Z/summary.json) |
| Model latency and cost per case | **Real** model calls on **Simulation** cases | `eval-v8`, `resolution-v2`, [`resolution-live-v1`](../../evidence/evaluation-runs/2024Q4-resolution-live-v1/summary.json) |
| Behavior under faults and under load | **Simulation** (injected faults, recorded model answers) | [`robustness/20261005T210525Z`](../../evidence/robustness/20261005T210525Z/summary.json), [`robustness/20261005T211031Z`](../../evidence/robustness/20261005T211031Z/summary.json) |
| Monitoring by country | **Simulation** (replayed workload) | [`monitoring/2024Q4-resolution-v2-replay`](../../evidence/monitoring/2024Q4-resolution-v2-replay/summary.json) |
| Contact demand and call aggregates | **Synthetic** dataset | [`flows/2024Q4-v3`](../../evidence/flows/2024Q4-v3/README.md), [`roi/2023-2026-callcenter-v1`](../../evidence/roi/2023-2026-callcenter-v1/report.md) |
| ROI and savings | **Projection** | [roi](../build/roi.md). The advisor-hour cost is assumed. |

No number in this submission is a production measurement.

The [evidence index](../../evidence/README.md) labels every run with these statuses.
