---
language: en
style: ASD-STE100
last_reviewed: 2026-10-04
---

# Rationale

Why the system is built this way. A bank team and a developer are the readers. Each page explains one choice: what we chose, what we rejected and what changes in production.

This folder is not a decision log. The [decisions](../build/decisions/) record *what* we chose. These pages explain *why*, what we rejected and what changes in production. The slide column names the slides in the deck on the project site.

## Pages

| Page | The choice in one line | Main evidence | Slide |
|---|---|---|---|
| [Data assumptions](data-assumptions.md) | Accounts exist only in México, Colombia and Argentina. Currency belongs to the product. | [`customer-360/dev-v1`](../../evidence/customer-360/dev-v1/README.md) | 1, 5 |
| [Investigation data support](investigation-data-support.md) | The data cannot support balances, product status, complaint history or customer signals, so the assistant does not use them | [`customer-360/dev-v1`](../../evidence/customer-360/dev-v1/README.md), [`dev-signals-v1`](../../evidence/customer-360/dev-signals-v1/README.md) | 1, 5 |
| [Problem and demand](problem-and-demand.md) | Demand sits in account inquiries; the dispute reason is harder and carries the chosen flow | [`problem/dev-v1`](../../evidence/problem/dev-v1/README.md) | 1 |
| [Policy thresholds](policy-thresholds.md) | Fraud and high-amount handoffs use synthetic values per currency. A bank replaces them with no code change. | [`evaluation/2024Q4-v2`](../../evidence/evaluation/2024Q4-v2/summary.json), [`dev-signals-v1`](../../evidence/customer-360/dev-signals-v1/README.md) | 3 |
| [Policy sources](policy-sources.md) | The dispute policy is synthetic: what the customer sees, its known defects and where real values come from | tests and the [`decision-explanation`](../../openspec/specs/decision-explanation/spec.md) spec | 3 |
| [Charge selector](charge-selector.md) | A small learned model ranks the charges. It beats the rules at the first pick but fails the safety rule, so it stays off | [`charge-ranker/test-v1`](../../evidence/charge-ranker/test-v1/summary.json) | 2, 4 |
| [Failure handling](failure-handling.md) | A model or tool failure ends in a safe reply or a handoff | [`robustness/20261005T210525Z`](../../evidence/robustness/20261005T210525Z/summary.json) | 3, 5 |
| [Capacity and latency](capacity-and-latency.md) | One replica serves about ten requests a second at the deployed limits | [`robustness/20261005T211031Z`](../../evidence/robustness/20261005T211031Z/summary.json) | 3 |
| [Cost guard](cost-guard.md) | A daily budget caps the model spend; the baseline answers above it | [`2024Q4-eval-v8`](../../evidence/evaluation-runs/2024Q4-eval-v8/summary.json), [`2024Q4-resolution-live-v1`](../../evidence/evaluation-runs/2024Q4-resolution-live-v1/summary.json) | 3, 5 |
| [Attack coverage](attack-coverage.md) | Every attack is attempted and counted; 0 of 42 outcomes are unsafe | [`adversarial/20261005T014816Z`](../../evidence/adversarial/20261005T014816Z/summary.json) | 4, 5 |
| [Negative results](negative-results.md) | The charge selector and the confidence cut-offs of prompt v3 stay off. A fixed rule decided it | [`charge-ranker/test-v1`](../../evidence/charge-ranker/test-v1/summary.json), [`2024Q4-cutoff-diagnosis-v1`](../../evidence/evaluation-runs/2024Q4-cutoff-diagnosis-v1/summary.json) | 4, 5 |
| [Router model selection](router-model-selection.md) | One open-weight model, chosen by a rule fixed before the measurement | [`2024Q4-select-v2`](../../evidence/evaluation-runs/2024Q4-select-v2/summary.json), [`2024Q4-eval-v7`](../../evidence/evaluation-runs/2024Q4-eval-v7/summary.json) | 2, 4 |
| [What the model never receives](model-data-minimization.md) | The model gets the masked words of the customer only. Ids, personal data and the fraud score stay in code. | [`adversarial/20261002T222323Z`](../../evidence/adversarial/20261002T222323Z/summary.json), privacy tests | 3 |
| [One app, state outside the process](one-app-state-outside.md) | One FastAPI app and one API. Sessions, conversations and cases survive a restart. | restart check in [REQ-0035](../requirements/delivery.md#req-0035) | 2 |
| [What the public link runs](public-link.md) | The demo runs the measured router with a baseline fallback on the labelled Gold mock, and says so | [REQ-0035](../requirements/delivery.md#req-0035) | 5 |
| [Repository history](repository-history.md) | An old commit names the data bucket. We did not rewrite the history. | [security: history review](../build/security.md#history-review-req-0034-101) | 5 |

Related pages: [what is real and what is not](../architecture/what-is-real.md), [evidence index](../../evidence/README.md).

## How to write a page

Each page has the same parts:

1. **Choice:** one sentence.
2. **Why:** the evidence or the constraint, with links.
3. **Evidence:** a table of checks. Each row cites a `summary.json` field, a test or a requirement.
4. **Alternatives rejected:** and why.
5. **In production:** what changes.
6. **On the slide:** the sentence we say.

Do not type a number by hand. Cite a field of a frozen `summary.json`. Write in simplified technical English (ASD-STE100): short sentences, active voice, one idea per sentence.
