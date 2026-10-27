---
language: en
style: ASD-STE100
last_reviewed: 2026-10-05
---

# Cost guard

**Choice:** a daily budget caps the model spend. When the spend of the day reaches the cap, the keyword baseline answers the next turns and the turn log records `budget` as the route.

**Why:** a public link with a real model has no natural limit ([REQ-0026](../requirements/non-functional.md#req-0026), [REQ-0055](../requirements/analytics.md#req-0055)). A stuck client or a curious reader must not run up the bill.

**Evidence:**

| Check | Field or file | Value |
|---|---|---|
| The guard reads the daily cap | `SENTINEL_LLM_DAILY_BUDGET_USD` in `app/ai/budget.py` | off when unset or not positive |
| The running total survives a restart | the state database file | `tests/test_model_serving.py` |
| The public link sets the cap | `deploy/azure/deploy.sh` | USD 5 a day |
| The sealed v8 measurement | [`2024Q4-eval-v8`](../../evidence/evaluation-runs/2024Q4-eval-v8/summary.json) `spend` | USD 0.388858 over 946 calls, cap USD 2.0 |
| The live timing run | [`2024Q4-resolution-live-v1`](../../evidence/evaluation-runs/2024Q4-resolution-live-v1/summary.json) `spend` | USD 0.008977 over 56 calls, cap USD 1.0 |

The cost per turn is small. The live run reports `timing.cost.per_attempted` 0.00016 USD and `timing.cost.per_resolution` 0.000561 USD. The daily cap of the link covers thousands of turns.

**Alternatives rejected:** no cap. One loop can drain the credit. A per-request cap. It hides the state of the day and needs a counter per request.

**In production:** a budget per tenant and per day, an alert before the cap, and a dashboard of the spend. The guard stays in code.

**On the slide:** "The model has a daily budget. Above it, the rules answer and the log says so."

Traces to [REQ-0026](../requirements/non-functional.md#req-0026) and [REQ-0055](../requirements/analytics.md#req-0055).
