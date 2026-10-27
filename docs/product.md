---
language: en
style: ASD-STE100
last_reviewed: 2026-10-27
---

# Product

Sentinel is the trust layer for bank customer-service AI. It turns "I do not recognize this charge" into a verified case, or into a well-informed advisor. It works in Spanish and Portuguese. It never invents a fact.

**Tagline:** The AI talks. The rules decide.

This page is the product statement. Each claim links to its evidence. [What is real](architecture/what-is-real.md) gives the type of each number.

## The user

| Item | Detail |
|---|---|
| Who | A customer of a bank in México, Colombia or Argentina |
| Situation | The customer sees a charge that they do not recognize |
| Language | `es-419` (Spanish) or `pt-BR` (Portuguese) |
| Need | A clear answer, a real case number or a person who knows the facts |
| Second user | The bank advisor who receives a handoff |

## The problem

A customer who does not recognize a charge calls or writes to the bank. Two failures cost trust:

- A chatbot that invents a fact or opens a case that does not exist.
- A handoff where the advisor must ask the customer everything again.

The data supports the choice. The dataset is synthetic. It describes the dataset, not a real bank.

| What | Value | Field | Type |
|---|---|---|---|
| Account and payment inquiries, the entry point of a dispute | 19,630 of 56,045 calls | `accounts.reason_transaccional`, `accounts.n_calls` in [`flows/2024Q4-v3`](../evidence/flows/2024Q4-v3/summary.json) | Synthetic |
| Complaints that say "unrecognized charge" | 251 of 5,611 | `disputes.unrecognized_claim`, `disputes.n` in [`flows/2024Q4-v3`](../evidence/flows/2024Q4-v3/summary.json) | Synthetic |
| Agent hours a month on transaction disputes | 390.78 | `hours.transaction_dispute.hours_per_month` in [`problem/dev-v1`](../evidence/problem/dev-v1/summary.json) | Synthetic |
| Dispute calls that end resolved | 43.64% | `reasons.Queja.share_pct` in [`problem/dev-v1`](../evidence/problem/dev-v1/summary.json) | Synthetic |

The volume of disputes is low. The product is not a volume story. It is a story of controlled action: the system acts, verifies and hands off. See [problem and demand](rationale/problem-and-demand.md) and [flow selection](build/flows/03-flow-selection.md).

## The difference

| Other assistants | Sentinel |
|---|---|
| The model decides and acts | The model only labels the intent. The code decides. |
| The model sees customer data | Code masks personal data. The model never sees `customer_id`. |
| The reply can state an unverified fact | Code writes each fact from the data and checks that the case exists before it says so |
| An unclear case gets a guess | An unclear case gets a question. A risky case gets a handoff. |
| "Why?" gets a new answer | "Why?" gets the stored policy decision, with its rule id |

The loop is Understand → Decide → Act → Verify → Escalate. See the [architecture](architecture/README.md) and the [rationale](rationale/README.md).

## The proof

| Claim | Evidence | Field | Type |
|---|---|---|---|
| No attack gives an unsafe outcome | [`adversarial/20261005T014816Z`](../evidence/adversarial/20261005T014816Z/summary.json) | `totals.unsafe_outcome_rate` | Test suite |
| Production code blocks most attacks. The mock model alone makes the rest safe, and we say so. | [`adversarial/20261005T014816Z`](../evidence/adversarial/20261005T014816Z/summary.json) | `totals.blocked_verified`, `totals.passes_on_mock` | Test suite |
| The LLM router labels the intent better than the keyword baseline | [`evaluation-runs/2024Q4-eval-v8`](../evidence/evaluation-runs/2024Q4-eval-v8/summary.json) | `candidates.<version>.intent.accuracy`, `paired.router_v2_vs_baseline` | Simulation |
| A more accurate prompt was not shipped, because it failed the safety gate | [`evaluation-runs/2024Q4-eval-v8`](../evidence/evaluation-runs/2024Q4-eval-v8/summary.json), [decision 018](build/decisions/018-evaluation-acceptance.md) | `candidates.router_v3.intent.accuracy`, `candidates.router_v3.unsafe_wording` | Simulation |
| The system resolves every case that the policy allows, and no other. The rest need a handoff or a question. | [`evaluation-runs/2024Q4-resolution-gap-v1`](../evidence/evaluation-runs/2024Q4-resolution-gap-v1/summary.json) | `ceiling.router_v2.resolvable`, `ceiling.router_v2.resolved` | Simulation |
| The router gains no resolution over the baseline in this run | [`evaluation-runs/2024Q4-resolution-v2`](../evidence/evaluation-runs/2024Q4-resolution-v2/summary.json) | `paired_resolution.net` | Simulation |

There is no public demo. Run the service locally. The local service serves `router_v2`, a prompted GLM 5.3 Flash, prompt `v2`. The sealed v8 hash is `2efe5962…` ([delivery](build/delivery.md)).

The [project site](../site/index.html) shows these numbers with their denominators. The [evidence index](../evidence/README.md) lists every run. A simulation is not a production measurement.

## What we do not claim

- No time saving. We did not measure one.
- No result on real customers or on a real bank. The data and the cases are synthetic or team-written.
- No result on other countries or other languages than the three countries and the two languages above.
- No balances and no account history. The data does not support them. See the [investigation data support](rationale/investigation-data-support.md).

## Requirements

[REQ-0013](requirements/delivery.md#req-0013), [REQ-0030](requirements/delivery.md#req-0030), [REQ-0036](requirements/delivery.md#req-0036), [REQ-0037](requirements/delivery.md#req-0037) and [REQ-0056](requirements/non-functional.md#req-0056).
