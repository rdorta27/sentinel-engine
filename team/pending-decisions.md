---
language: en
style: ASD-STE100
last_reviewed: 2026-10-05
---

# Pending decisions

This page is the record of the first phase. It is not the current plan. The index is in [the team record](README.md).

This page lists the choices of that phase. Each choice has its options, its supporting material and its deadline. No choice is open.

## How we decide

1. Read the supporting material. Record your preference in your column or in the team channel.
2. If we agree, the choice is decided. If we do not agree, we settle it in the channel or on a short call.
3. If we still disagree at the deadline, the area owner decides. Anything outside an area goes by majority.
4. Record the outcome. Then remove the row from the open lists:
   - Put product and technical decisions in [decisions](../docs/build/decisions/), one file each. Use the [template](../docs/build/decisions/_template.md).
   - Put team decisions in the [plan](plan.md#decisions-made) and in the [decided](#decided) table below.

## Open

No choice is open. This list is the record of that phase.

## Decided

| # | Decision | Outcome | Date |
|---|---|---|---|
| 1 | Flow | Transaction disputes, entered through an account inquiry. The measurements confirmed it | 9/29 |
| 2 | Learned component | A prompted LLM that classifies the dispute category. The comparison is a keyword baseline and the same LLM zero-shot. The text is team-written es-419 and pt-BR, declared as simulation ([007](../docs/build/decisions/007-learned-component.md)) | 9/29 |
| 3 | Demo scope | The system looks up charges and their status, explains, opens a dispute after a structured confirmation, reads it back and makes a handoff. Out of scope: balances, products, cards, credit, a decision on fraud and a decision on the dispute outcome ([decision 008](../docs/build/decisions/008-account-inquiry-scope.md), [Demo Architecture](../docs/architecture/demo-architecture.md)) | 9/29 |
| 4 | Owners per area | Natalia: data and data analysis. Rubén: AI, architecture and ML. Felix: full-stack | 9/28 |
| 5 | Daily sync | No meeting. Slack is enough if we talk every day. If a status is necessary, it goes in the channel at the end of the day | 9/28 |
| 6 | Task tool | [tasks.md](tasks.md) in the repository. The follow-up is in the team channel. Rubén reviews what is still pending | 9/29 |
| 7 | Code flow | Each person works on a branch, pushes it and asks in Slack for authorization to merge. Any other teammate can authorize. The author merges. Nobody pushes directly to `main` | 9/29 |
| 8 | Milestone meetings | No standing meetings. We assign tasks as they come up. A meeting, individual or with the group, happens only when necessary | 9/29 |
| 9 | Backend | Python and FastAPI. The tool loop (LangGraph or plain Python) is deferred. Policy, session and idempotency stay in code | 9/28 |
| 11 | Frontend | A one-page chat that FastAPI serves. Streamlit and Gradio are out. Node only if Felix asks for it for the video | 9/28 |
| 12 | Data storage and pipeline | Delta Lakehouse. Locally: DuckDB with the Delta extension. In production: Azure Databricks with PySpark and Delta Lake on ADLS Gen2. Bronze, Silver and Gold are in `sentinel-data-engine/` ([stack](../docs/architecture/system-architecture.md#stack-and-deployment)) | 9/29 |
| 17 | Repository visibility | Public from the start. It stays public | 9/28 |
| 18 | OpenSpec spec language | English, because we submit the specs | 9/28 |
| 19 | Language of `docs/` and `team/` | Everything in English, including folder and file names | 9/28 |
| 20 | Video and slides | Rubén. The script starts on Thursday 10/1. Slides: Rubén. The outline is on Thursday 10/1. The group validates it on Friday 10/2. Review from Friday to Monday with the results. Frozen on Monday 10/5 | 9/29 |
| 21 | Repositories | One public repository. Git submodules are decision 22 | 9/29 |
| 22 | Git submodules | Not used. The team works by folders in the single repository ([repository layout](../docs/architecture/system-architecture.md#repository-layout)) | 9/29 |
| 24 | Account-inquiry scope | The entry point covers charges and transactions only: what a charge is, its status and whether the customer can dispute it. Balances, products, cards and credit are out of scope. The assistant says so and offers a handoff. One read tool: `lookup_transactions` ([scope](../docs/architecture/specification.md#scope)) | 9/29 |
| 29 | Advisor queue, admin panel, role landing | A role landing and a read-only advisor view of escalated tickets (`GET /api/v1/handoffs`) in the ai-core page. The demo advisor exists only with `SENTINEL_DEMO_AUTH=1`. No admin panel. We removed the old mock backend and its reference page ([009](../docs/build/decisions/009-demo-ui-and-advisor-view.md)) | 10/1 |
| 25 | Suspected-fraud handoff rule | A claim (`fraud.claim`) or a score above the p95 for each account country and currency (`fraud.score`). The values are synthetic, from evidence 2024Q4-v2 ([010](../docs/build/decisions/010-fraud-handoff-rule.md)) | 10/1 |
| 26 | High-amount handoff threshold | The p95 for each account country and charge currency. The values are synthetic, from evidence 2024Q4-v2. Mexican MXN has none ([011](../docs/build/decisions/011-high-amount-threshold.md)) | 10/1 |
| 13, 16 | Deployment and subscription | Azure Container Apps, one Docker container, inside the free grant and the trial credit. We decided it for the submission on 10/2, after Hugging Face dropped its free Docker tier ([019](../docs/build/decisions/019-azure-container-apps.md), which supersedes [012](../docs/build/decisions/012-public-deployment.md)) | 10/2 |
| 14 | Experiment tracking | The frozen evaluation runs are the tracking record. MLflow on Databricks in production ([013](../docs/build/decisions/013-experiment-tracking.md)) | 10/1 |
| 23 | `team/` in the submission | Kept. It shows the plan, the decisions and the evidence behind the build. We review it before the submission | 10/1 |
| 27 | Data staleness threshold | Off in the demo (the age of Gold is always zero). A threshold for each country in production ([014](../docs/build/decisions/014-data-staleness.md)) | 10/1 |
| 28 | Handoff delivery in production | Demo: a ticket store and an advisor view. Production: a queue to the CRM of the bank ([015](../docs/build/decisions/015-handoff-delivery.md)) | 10/1 |
| 10 | Router models | Open-weight models on Fireworks AI, a cheap route and a strong route. A rule fixed before the measurement chooses the model for each route. gpt-oss-120b is the starting cheap model ([016](../docs/build/decisions/016-router-models.md)) | 10/1 |
| 15 | Portuguese | A Portuguese-speaking customer holds an MX, CO or AR account. The key cases have pt-BR twins. One model writes them. Another model back-translates them to Spanish. The team checks them ([017](../docs/build/decisions/017-portuguese.md)) | 10/1 |
| 30 | Where the pages of `docs/understand/` go | `overview.md` goes to `docs/overview.md`. `dataset.md` goes to `docs/data/dataset.md`. `reference/` goes to `docs/data/reference/`. `glossary/` goes to `docs/glossary/`. `docs/data_inventory.md` and `docs/sizing-capacity.md` stay where they are. The `.gitignore` rule `data/` has the exception `!docs/data/`. The data formats stay ignored ([`docs-followups`](../openspec/changes/archive/2026-10-05-docs-followups/tasks.md), group 6) | 10/5 |
| 32 | Who checks the 20 labels | A team member who did not write the cases. The sample is in `sentinel-ai-core/eval/review/human-check-v1.md`. The review is pending. An LLM does not judge, so REQ-0023 stays not applicable ([`evidence-hardening`](../openspec/changes/archive/2026-10-05-evidence-hardening/tasks.md) task 3.3) | 10/5 |
| 33 | Router-sensitive resolution block | Not added. The gap run shows the policy ceiling: both systems resolve all 16 resolvable cases, so the paired difference is 0. The claim stays sealed ([`2024Q4-resolution-gap-v1`](../evidence/evaluation-runs/2024Q4-resolution-gap-v1/summary.json), [decision 022](../docs/build/decisions/022-resolution-acceptance.md)) | 10/5 |
| 16 | Judge access | One shared set of test credentials (three customers and one advisor). The public link has no passwordless entry. The passwords go in the submission email, not in the repository ([`judge-access`](../openspec/changes/archive/2026-10-05-judge-access/tasks.md)) | 10/5 |
