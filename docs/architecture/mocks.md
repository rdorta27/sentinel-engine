---
language: en
style: ASD-STE100
last_reviewed: 2026-10-05
---

# Mocks: what they are, where they run and why

This page explains each mock in the submission. A mock is a stand-in with the same contract as the production component. Production replaces the backend. It does not replace the code. The [what is real](what-is-real.md) page gives the status of every part. The [demo architecture](demo-architecture.md#mocked-components) shows the mocks in the diagrams.

## What the brief says

| Rule | Source |
|---|---|
| Sandbox services and mock banking tools are acceptable when their contracts and limits are documented. | Problem statement, data and execution boundaries (REQ-0032) |
| Show authentication with a trusted test session or identity service. A national ID or customer number alone does not prove identity. | Same section (REQ-0027) |
| Say which inputs are real, de-identified, synthetic or team-generated. | Same section (REQ-0031) |
| With static data, show update correctness with a labelled test fixture. | Architecture freedom |
| No live lending decision and no movement of money. | Same section |
| Do not put private records, credentials or restricted data in public submissions or in external model requests. | Same section |

The brief does not ask for zero mocks. It asks that each mock has a documented contract and a stated limit.

## The mocks

| Mock | Where it runs | Why it is a mock | Limit | Production |
|---|---|---|---|---|
| Gold on the public link | Public link | The image holds no dataset rows. See [Gold on the public link](#gold-on-the-public-link) | The demo personas and their charges are team-generated. `GET /api/v1/health` reports `gold_source: mock` | Gold on Databricks |
| Login and session | Local run and public link | The team has no bank identity provider | Test users with a password fixture. The public link reads a test users file (hashes only) and sends the credentials in the submission email; the fixture passwords do not work there. They prove the session design, not a real identity check | The bank identity provider |
| Advisor | Local run and public link | No human advisor team exists | A demo advisor user with a read-only ticket view | A human advisor. Tickets go to the bank CRM through a queue ([015](../build/decisions/015-handoff-delivery.md)) |
| Case store | Local run and public link | PostgreSQL adds setup risk and no evidence | SQLite with the same models, on an Azure Files share on the public link | PostgreSQL |
| Dispute policy | Local run and public link | The bank policy is not available | Team-written country files, marked `synthetic: true` ([021](../build/decisions/021-dispute-policy-sources.md)) | The policy that the bank approves |
| Opening a dispute | Local run and public link | No bank dispute system exists to call | The case store records the case. No bank system receives it | The bank dispute system |
| Secrets | Local run | A key vault adds no evidence | `.env`, ignored by git. The public link uses Container App secrets | Azure Key Vault |
| Stand-in model (`DemoModel`) | Test suite only | A test must not depend on a live model | Three attack cases (A1, A2, A5) pass only because of this model. The adversarial summary counts them as `passes_on_mock`. Those three cases also run against the real router model and pass ([real-model run](../../evidence/adversarial/20261005T204313Z/summary.json)) | None. The live router replaces it |

## What is not a mock

The orchestrator, the policy engine, the confirm box, the read-back, the intent router with its live model calls, the personal-data masking and the turn records are real code. They run the same way in the demo and in production.

## Gold on the public link

The public link serves a labelled in-memory store. It does not serve the real Gold file. The decision is in [019](../build/decisions/019-azure-container-apps.md) and [what the public link runs](../rationale/public-link.md).

| Question | Answer |
|---|---|
| Can the public link read real Gold? | Yes, in a technical sense. The local run already reads the PII-free view `v_service_dispute_eligible_transactions` from DuckDB |
| Why does it not? | Five reasons, in the table below |
| What do we show instead? | The local run on real Gold code with synthetic data, and the labelled mock on the link |

| Consequence of real Gold on the link | Effect |
|---|---|
| Size | The Gold file is about 880 MB. A network share reads it slowly. A copy at start-up slows the first visit |
| Privacy | Gold holds name, document number and birth date in plain text ([023](../build/decisions/023-pii-gold-handling.md)). The service reads only the PII-free view. Even so, dataset rows would leave the team machine |
| Model calls | More real values would pass through the masking to the external model. REQ-0047 forbids personal data there. We would test the guarantee again |
| Behaviour | The generator leaves artefacts. A `fraud_score` above 30 is always fraud. Mexican accounts exist only in USD. The three demo cases were built on the mock and could change outcome |
| Measurements | The runs `eval-v7` and `resolution-v2` use the mock. Their numbers do not describe the link with real Gold |

A small derived sample could remove most of these costs. The team has not confirmed that the data-use terms allow a served sample. Until it does, the link keeps the mock.

## How we label a mock

- Each document, slide and evidence run uses the labels of [what is real](what-is-real.md#components).
- The code marks a mock in its name or in a field. The health endpoint reports the Gold source.
- Each evidence run states its data type in the [evidence index](../../evidence/README.md). A run on the mock store carries the label **Mock store**.
- No number from a mock is a production measurement.

## What the mocks do not change

| Claim | Why it holds |
|---|---|
| The policy decides, and the model converses | Policy runs in code, outside the prompt. The mock only supplies the facts |
| The orchestrator never sees `customer_id` | The session layer holds it. A mock login keeps the same rule |
| A written action is read back | The read-back uses the case store contract. SQLite and PostgreSQL share it |

## Path from mock to production

Each row of the mock table names its production backend. The steps are in the [path to production](specification.md#path-to-production). The remaining work is in the README `## Roadmap` and `## Limitations`.

## Checks (2026-10-05)

| Claim | Check | Result |
|---|---|---|
| The mock list | [what is real](what-is-real.md#components) and [demo architecture](demo-architecture.md#mocked-components) | The list matches. This page adds the opening of a dispute and the stand-in model. |
| `gold_source` | `app/main.py` sets `application.state.gold_source`; the health endpoint reports it | `gold_source: mock` on the public link and when no DuckDB file is readable. |
| Three `passes_on_mock` cases | [`adversarial/20261005T014816Z`](../../evidence/adversarial/20261005T014816Z/summary.json) `totals.passes_on_mock` | 3: A1, A2 and A5, all in `A_prompt_injection`. |
| The three cases on the real model | [`adversarial/20261005T204313Z`](../../evidence/adversarial/20261005T204313Z/summary.json) `totals.unsafe_outcome_rate` | `0/3`. The three cases now also run on the real router model. |
| The stand-in model | `app/ai/demo.py` `DemoModel` | Test suite only. The live router replaces it. |
