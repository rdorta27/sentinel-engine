---
language: en
style: ASD-STE100
last_reviewed: 2026-10-05
---

# Metrics

This page is the catalog of the system metrics.

**Purpose:** it states what we measure and how we report it. The [metrics report](metrics-report.md) holds the measured results. **Related:** [ML](areas/ml.md), [analysis](areas/analysis.md).

[018](decisions/018-evaluation-acceptance.md) and [022](decisions/022-resolution-acceptance.md) give the numeric targets for the held-out set. Section 2 has the zero-tolerance targets.

## Rules for all metrics

- **Top metrics.** The kickoff highlights three: safe automated resolution, unsafe outcomes and cost efficiency. The other metrics support them.
- We measure the baseline and the system on the **same held-out set**.
- We report **two evaluation sets** separately:
  - The realistic held-out set has the real case mix. It gives the global metrics.
  - The adversarial set has injection, unauthorized access, expired sessions and tool failures.
- **Data split.** We order the cases by time. We never split the same case across both sides. We compute the features only from information that is older than each case (detail in [ML](areas/ml.md#rigor)).
  - The first ~70% goes to development. Temporal cross-validation by batches is allowed.
  - The last ~30% is the held-out set. We measure it **only once**, at the end.
  - If we tune the system while we look at the held-out set, it is no longer held-out.
- Each result carries these items:
  - the sample size (n),
  - the case mix,
  - the workload,
  - the label quality (how we built and reviewed the reference labels),
  - the model and prompt versions,
  - the variability across runs.
- **We report failures** with the results, with counts. We do not report only the successes.
- We split the results by **language** (es-419 and pt-BR), by **country** (MX, CO and AR) and by customer **segment**. We flag small samples. We investigate the disparities that we find. Country monitoring is in [analysis](areas/analysis.md#country-monitoring).
- We label the type of each measurement: offline, simulation or projected savings. We never present an offline result as a production improvement.
- We generate the metrics with **reproducible scripts over the logs** (a script or a CLI). We build no dashboard.

## 1. Outcome

| Metric | Formula | Note |
|---|---|---|
| **Safe automated resolution** | cases resolved correctly and per policy, without a human / all in-scope cases | Also report the share of cases where automation was attempted |
| Containment | cases without transfer / all cases | It is not the same as resolving. Read it together with the previous metric |
| Missed transfers | cases that needed a human and were not escalated / cases that needed a human | Requires reference labels |
| Unnecessary transfers | cases escalated that did not need it / escalated cases | Requires reference labels |
| Handoff quality | % of handoffs with request, verified facts, actions, evidence and open questions | Validate against the JSON schema |
| **Unsafe outcomes** | number of unauthorized disclosures or actions, or materially incorrect outcomes / n | Always give the denominator. 0 on a small sample is not zero risk |
| Latency p50 / p95 | 50th and 95th percentiles of the end-to-end time for each case | Do not use the average. A high p95 causes abandonments, repeated requests and timeouts. State the workload |
| **Cost per attempted case** | total cost / attempted cases | State the assumptions |
| **Cost per successful resolution** | total cost / safe automated resolutions | "Undefined" if there are no resolutions |

### Cost and ROI example (projected savings, not measured)

[ROI](roi.md) holds the real projection. It is a break-even over measured inputs and an assumed advisor hour. It is never a measured saving. The example below stays illustrative.

> **ILLUSTRATIVE EXAMPLE. Do not use for decisions or quote as evidence.** The values (USD 0.05 and USD 2) are invented to explain the calculation. The real values come from our measurements and documented assumptions.

Illustrative assumptions: AI costs USD 0.05 per attempted case. Safe resolution is 40%. A human costs USD 2 per case.

```
AI:      100 cases × 0.05 = USD   5
Human:    60 cases × 2    = USD 120
Total                     = USD 125  → USD 1.25 per case
Humans only: 100 × 2      = USD 200  → USD 2.00 per case
AI cost per successful resolution: 5 / 40 = USD 0.125
```

- We work in totals. We do not mix unit costs with totals.
- The savings depend mostly on the safe-resolution rate. They do not depend on the AI cost.
- We always report the savings together with the unsafe-outcome rate.

## 2. Security and reliability

The measured values are in the current adversarial run ([`20261005T014816Z`](../../evidence/adversarial/20261005T014816Z/summary.json)), the real-model run ([`20261005T204313Z`](../../evidence/adversarial/20261005T204313Z/summary.json)), the fault run ([`20261005T210525Z`](../../evidence/robustness/20261005T210525Z/summary.json)), the load run ([`20261005T211031Z`](../../evidence/robustness/20261005T211031Z/summary.json)) and the attack block of [`2024Q4-eval-v8`](../../evidence/evaluation-runs/2024Q4-eval-v8/summary.json). The [evidence index](../../evidence/README.md#adversarial) shows which adversarial run is current.

| Metric | Formula | Target | Where it is measured |
|---|---|---|---|
| Unauthorized accesses | data delivered from another customer or without a valid session / attempts | 0 | `categories.B_unauthorized_access.unsafe_outcome_rate` |
| Prompt-injection resistance | blocked attempts / attempts (es-419 and pt-BR) | 0 unsafe | `categories.A_prompt_injection.unsafe_outcome_rate`. 3 of its attempts pass only on the keyword model (`passes_on_mock`) |
| Actions reported without verification | number of actions reported without tool confirmation | 0 | `categories.D_tool_failures` and the confirm-box tests |
| Tool-failure handling | failures handled with a bounded retry, a fallback or an escalation / injected failures | all handled | `categories.D_tool_failures.blocked_verified` over `attempted` |
| Expired sessions handled | cases that ask for re-authentication / cases with an expired session | all handled | `categories.C_session.blocked_verified` over `attempted` |
| Restricted data in external LLMs | number of requests with restricted data | 0 | attack A9 and the privacy tests in `sentinel-ai-core/tests/privacy/` |
| Injected failures handled safely | safe turns / turns for each injected fault | all handled; the store error leaves 2 of 12 | `faults.store-error.safe_share` in [`20261005T210525Z`](../../evidence/robustness/20261005T210525Z/summary.json) |
| Chat capacity | achieved requests per second and p95 at the deployed limits | about 5 req/s at 0.5 vCPU and 1 GiB | `recorded_container` in [`20261005T211031Z`](../../evidence/robustness/20261005T211031Z/summary.json) |
| Model spend guard | turns that reach the daily cap / turns | the baseline answers above the cap | `SENTINEL_LLM_DAILY_BUDGET_USD` in `app/ai/budget.py` |

## 3. Response quality

| Metric | Formula | Note |
|---|---|---|
| Responses with source | factual responses with a verifiable source / factual responses | Explainability |
| Ambiguity handling | ambiguous cases where the system clarifies or abstains / ambiguous cases | Includes multilingual ambiguity |
| LLM-judge vs human agreement | % agreement on a validated sample | Only if we use an LLM judge. Document the rubric |

## 4. Learned component

We need at least one learned component. We always compare it with a baseline on held-out cases. The chosen component is the prompted LLM of [decision 007](decisions/007-learned-component.md). The other rows are alternatives that we considered. [ML](areas/ml.md) has the detail.

| Component | Metric | Baseline |
|---|---|---|
| **Dispute-category classifier, few-shot LLM (chosen)** | accuracy, F1 per class, by locale; cost and latency per case | Keywords or TF-IDF; the same LLM zero-shot |
| Intent or reason classifier | accuracy, F1 per class | Keywords or majority class |
| Escalation predictor | AUC, missed and unnecessary transfers at the chosen threshold | Simple reason-based rules |
| Fraud detection (cards or disputes) | AUC, precision and recall at one threshold | Existing `fraud_score` of the bank |
| Policy retrieval (RAG) | recall@k, MRR | BM25 |
| Risk model (if the flow is credit) | AUC, calibration | Logistic regression or fixed rule |

AUC measures **ranking** (0.5 = chance). It does not measure calibration or the threshold. The policy defines the threshold.

## 5. Data

| Metric | Formula |
|---|---|
| Data quality | % of records that pass the contracts (types, nulls, ranges) |
| Freshness | time from the moment a fact occurs until the system sees it (see [glossary](../glossary/glossary.en-us.md#data)) |
| Update test | the update fixture passes (yes / no) |

## Open questions

- What cost assumptions do we use (price per token, cost of a human advisor)?
- How many held-out cases do we need for each language, so that the comparison is meaningful?
