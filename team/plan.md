---
language: en
style: ASD-STE100
last_reviewed: 2026-10-05
---

# Team plan

Sentinel Engine · Factored AI & Data Hackathon 2026 · Submission: **Monday 10/5, 11:59 pm (UTC-5)**

> We start on Monday 9/28. The daily tasks are in [tasks](tasks.md). The open choices are in [pending decisions](pending-decisions.md).

## Schedule

The schedule is tentative. We adjust it if anything slips.

| Day | Date | Goal | Milestone |
|---|---|---|---|
| Sun | 9/27 | Prepare: data access, repository and readings | Everyone has access |
| Mon | 9/28 | **Decide** the flow, the stack, the owners and the working method. First look at the data | Decisions recorded |
| Tue | 9/29 | Skeleton: 4 mock tools, orchestrator, simple chat and minimal pipeline. Analysis that backs the flow | **The skeleton answers end to end** · *not reached: moved to Wed 9/30* |
| Wed | 9/30 | Skeleton (moved from Tue). Normal case with real data, JSON handoff, learned component against baseline | **The skeleton answers end to end. One case works fully** |
| Thu | 10/1 | Ambiguous and human cases, Portuguese, adversarial set and deployment. The video script and the slide outline start. P1 if time allows | **3 cases in es-419 and pt-BR, public link** · *partly reached: 3 cases in es-419. Portuguese serving and the public link were still open* |
| Fri | 10/2 | Held-out evaluation and metrics. README in English with limitations. Review the repository for secrets. The group validates the slide outline. Router v2 served with baseline fallback. Router v3 planned ([plan](router-v3-plan.md)) | **Router v2 served** |
| Sat to Sun | 10/3 to 10/4 | Router v3, new held-out set and eval-v8. README and results. Freeze the code on Sunday night | **Code and results frozen** · *reached on Mon 10/5: router v3, the chat changes, the bank interface and the sealed v8 sets merged. The single v8 measurement ran once. The verdict serves `router_v2`* |
| Mon | 10/5 | Presentation review and video recording on the frozen build. Critical fixes only. Submit with margin. The deadline is 11:59 pm (UTC-5) | **Submitted** |

```mermaid
gantt
    title Milestones
    dateFormat YYYY-MM-DD
    axisFormat %a %d/%m
    tickInterval 1day
    todayMarker off
    Decisions recorded           :milestone, 2026-09-28, 0d
    Skeleton answers end to end  :milestone, 2026-09-30, 0d
    One case works fully         :milestone, 2026-09-30, 0d
    3 cases, public link         :milestone, 2026-10-01, 0d
    Code and results frozen      :milestone, 2026-10-04, 0d
    Submitted                    :milestone, 2026-10-05, 0d
```

[Tasks](tasks.md) has the work of each person. This chart does not show it. We want **code, results and README frozen by Sunday 10/4 night**. We moved the date from Friday 10/2 on 10/2, to measure router v3. We finish the presentation and the video on Monday 10/5, on top of the frozen build. Set an internal submission time on Monday, well before 11:59 pm. Working first: if an optional item blocks a mandatory item, the optional item waits. The [requirements](../docs/requirements/requirements.md) hold the priorities.

## Decisions made

| Decision | Status | Record |
|---|---|---|
| Team name: Sentinel Engine | Accepted | — |
| Platform: Microsoft Azure | Accepted | [001](../docs/build/decisions/001-azure-platform.md) |
| Specs with OpenSpec, written in English (decision 18) | Accepted | [002](../docs/build/decisions/002-openspec.md) |
| Owners: Natalia, data and data analysis. Rubén, AI, architecture and ML. Felix, full-stack | Accepted | — |
| Hybrid LLM with a router across models: open-weight models on Fireworks AI, chosen for each route by measurement (closes decision 10) | Accepted | [016](../docs/build/decisions/016-router-models.md) |
| Infrastructure budget: the estimate of Natalia (USD 20-60, within the USD 200 Azure trial credit) as the working assumption | Accepted | [cost](../docs/build/cost.md) |
| Case store (disputes and handoff tickets), sessions and conversation state: SQLite for the submission (updated 10/1, mentor feedback: externalize conversation state). Postgres on Azure is the production backend of the same models. Memory only for tests and the offline eval. Not written to Gold | Accepted | [demo](../docs/architecture/demo-architecture.md), [path to production](../docs/architecture/specification.md#path-to-production) |
| No .NET: it is outside the stack of the team (Python and FastAPI). The target is Azure. Locally it runs on Linux | Accepted | [stack](../docs/architecture/system-architecture.md#stack-and-deployment) |
| Flow: transaction disputes, entered through an account inquiry (confirmed 9/29) | Accepted | [003](../docs/build/decisions/003-disputes-flow.md) |
| Repository language: everything in English, including `docs/` and `team/` (decision 19, closed 9/28) | Accepted | [pending decisions](pending-decisions.md) |
| No daily sync meeting. Slack if we talk every day. A status, if necessary, at the end of the day (decision 5) | Accepted | [pending decisions](pending-decisions.md) |
| Backend: Python and FastAPI (decision 9). The loop tool (LangGraph or plain Python) is deferred | Accepted | [005](../docs/build/decisions/005-backend.md) |
| Frontend: a one-page chat that FastAPI serves. No Streamlit or Gradio (decision 11) | Accepted | [006](../docs/build/decisions/006-frontend.md) |
| Learned component: a prompted LLM that classifies the dispute category, against a keyword baseline, on team-written text | Accepted | [007](../docs/build/decisions/007-learned-component.md) |
| Prompted router behind `ModelPort` with route table, fixtures and safe fallback (change archived 9/30) | Accepted | `openspec/specs/llm-router/spec.md` |
| Evaluation evidence frozen: label universe, mix and thresholds in `evidence/evaluation/2024Q4-v1/` (change archived 9/30) | Accepted | `openspec/specs/evaluation-evidence/spec.md` |
| Evaluation runner frozen: bench and system replay in `evidence/evaluation-runs/2024Q4-eval-v1/` (change archived 9/30) | Accepted | `openspec/specs/evaluation-runner/spec.md` |
| Video and slides: Rubén. Script from Thursday 10/1. Slide outline on Thursday 10/1, validated by the group on Friday 10/2, reviewed from Friday to Monday with the results. Frozen on Monday 10/5. The video is published at (retired after the hackathon) (decision 20) | Accepted | [delivery](../docs/build/delivery.md) |
| Tasks live in the repository. The follow-up is in the team channel. Rubén reviews what is still pending (decision 6) | Accepted | [tasks](tasks.md) |
| Code: branch, push, Slack authorization, the author merges. No direct push to `main` (decision 7) | Accepted | [pending decisions](pending-decisions.md) |
| No standing milestone meetings. Ad hoc only (decision 8) | Accepted | [pending decisions](pending-decisions.md) |
| One public repository (decision 21), organized by folders. No git submodules (decision 22). Service folder: `sentinel-ai-core/` | Accepted | [Folders](#folders) |
| Public link on Azure Container Apps, one Docker container. It supersedes 012, after Hugging Face dropped its free Docker tier (closes decisions 13 and 16) | Accepted | [019](../docs/build/decisions/019-azure-container-apps.md) |
| Documentation layout: the `docs/understand/` folder is split into `docs/overview.md`, `docs/data/` and `docs/glossary/` (decision 30 in [pending decisions](pending-decisions.md)) | Accepted | [`docs-followups`](../openspec/changes/archive/2026-10-05-docs-followups/tasks.md) |
| Judge access: one shared set of test credentials, sent in the submission email. No passwordless entry on the public link | Accepted | [`judge-access`](../openspec/changes/archive/2026-10-05-judge-access/tasks.md) |
| Keep `team/` in the submission, reviewed before the submission (closes decision 23) | Accepted | [pending decisions](pending-decisions.md) |
| Demo UI with a role landing and a read-only advisor view in the ai-core page. We removed the old mock backend and its reference page. No admin panel (closes decision 29) | Accepted | [009](../docs/build/decisions/009-demo-ui-and-advisor-view.md) |

Product and technical decisions go in [decisions](../docs/build/decisions/), one file for each decision. Team decisions (working method and owners) are recorded here.

## Working method

| Topic | How we work |
|---|---|
| Communication | Everything in the team channel. Challenge questions go to the hackathon help channel |
| Status | No standing sync and no standing milestone meetings. We talk on Slack during the day. A meeting, individual or with the group, happens only when a task needs it. The outcome goes in the channel |
| Tasks | In [tasks](tasks.md), with owner, date and status |
| Specs | With OpenSpec. We propose each change before we implement it and cite its requirements |
| Code | One branch for each change. Push. Ask in Slack for authorization to merge. Any other teammate can authorize. The author merges. No direct push to `main` |
| Decisions | Product and technical decisions are in [decisions](../docs/build/decisions/). Team decisions are here. We announce all of them in the channel |
| Progress | When a task closes, we update the card of the requirement in its type file and its row in the [requirements index](../docs/requirements/requirements.md). [Tasks](tasks.md#open-work-by-priority) orders the open tasks by priority |
| Repository | A single repository (`factored-hackathon-2026-sentinel-engine`). It is public from the start and it stays public |

Two hackathon rules are non-negotiable. No secrets or data in the repository (credentials go in `.env` and teammates share them by direct message). The submission is in English.

## Folders

There are two code folders. `sentinel-ai-core/` is the whole FastAPI process, including the chat, its policy configuration and the evaluation runner. It is not a separate AI service. There is no web package and no infrastructure folder.

That process serves one app from `sentinel-ai-core/app/main.py` (`app = create_app()`). It has one API under `/api/v1`: `auth/{login,logout,me}`, `transactions`, `chat`, `disputes`, `handoffs` (advisor) and `health`. The demo and the later service share it. Only the adapters behind the ports change (Gold: DuckDB view or mock. State: SQLite or memory. Model: baseline or prompted router). Disputes also have their own two-step API (`/api/v1/disputes/preview`, `/api/v1/disputes` and a read-only listing). It runs the turn cycle of the chat.

| Path | Who | What | Status |
|---|---|---|---|
| `sentinel-data-engine/` | Natalia | Medallion pipeline. Gold table and columns of the [data contract](../docs/architecture/specification.md#data-contract), as-of date and labelled incremental fixture. | Done: run end to end on the full dataset into `data/gold_bank.duckdb`, reproduced by a fresh run on 10/02. Incremental fixture tested (REQ-0018). Silver keeps the durations, `process_date` and `amount_usd` (PR #44). The [source inventory](../docs/data_inventory.md) and the [sizing](../docs/sizing-capacity.md) are written. The runner generates the [quality report](../sentinel-data-engine/data_quality_report.md), and a `verify` mode checks its figures (`quality-report`, PR #54) |
| `sentinel-ai-core/app/static/`, `routers/` | Felix | Chat page with the confirm box. `POST /api/v1/chat` with the structured confirmation field ([confirmation](../docs/architecture/specification.md#confirmation)). | Done: chat page, test session, `POST /api/v1/chat` and confirm box verified end to end. Role landing and read-only advisor view of `GET /api/v1/handoffs` ([009](../docs/build/decisions/009-demo-ui-and-advisor-view.md)) |
| `sentinel-ai-core/app/session/` | Felix | Test session and [conversation state](../docs/architecture/specification.md#conversation-state), deleted on expiry. | Done: password login on `/api/v1/auth/*` with roles (customer, and a demo advisor behind `SENTINEL_DEMO_AUTH`). Sessions and conversation in SQLite, keyed by a token hash and deleted on logout and expiry |
| `sentinel-ai-core/app/orchestrator/`, `policy/`, `ai/` | Rubén | Loop, policy engine (it evaluates the rules and the decision priority), `confirmation_token`, router and learned component. | Done: loop and policy engine with tests. router_v2 is served behind `ModelPort` with a baseline fallback. `2024Q4-eval-v8` measured it against the baseline (decision 016). The v8 verdict serves router_v2. The "why?" answer from the stored decision (PR #42). Narrowing, the prompt-extraction refusal, the injection record and the Gold read budget (PR #49). Contract v3, openers, status answers and validated drafts (`router-v3` and `chat-start`, PRs #59 and #62). Prompt v3, the cut-offs and the charge selector are off by default |
| `sentinel-ai-core/config/policy/` | Rubén | Policy parameters, not code: the synthetic [policy source](../docs/architecture/specification.md#policy-source), one file for each country (MX, CO, AR), fraud and high-amount thresholds for each currency ([010](../docs/build/decisions/010-fraud-handoff-rule.md), [011](../docs/build/decisions/011-high-amount-threshold.md)) and staleness (decision 27). The engine in `app/policy/` reads them. | Done: synthetic p95 values for each account country and currency from `evidence/evaluation/2024Q4-v2/summary.json`. Mexican MXN has none. Staleness stays off |
| `sentinel-ai-core/app/tools/` | Felix and Rubén | The four tool contracts. Natalia owns what Gold returns. | Done: `lookup_transactions` with isolation, currency and canary tests. Open and read-back on the SQLite case store with one open dispute for each charge. The handoff is filed as a ticket. Gold reads run under a time budget, from the mock or the DuckDB file (PR #50) |
| `sentinel-ai-core/app/privacy/` | Felix | It masks the personal identifiers that the customer types, before the orchestrator, the model, the logs and the stored state (REQ-0047, decision 004). | Done: `tests/privacy/`. Adversarial A9 is blocked |
| `sentinel-ai-core/app/observability/` | Rubén | Structured log records with `trace_id`, latency, tokens and cost ([observability](../docs/architecture/specification.md#observability)). | Done: the records and the JSONL writer run from `step()` and `POST /api/v1/chat`. `var/` is anchored to the package. The acceptance replay test is green |
| `sentinel-ai-core/eval/` | Rubén | [Evaluation](../docs/architecture/specification.md#evaluation) cases (JSONL) and runner, system against baseline, with fault injection. | Done: the development cases, the sealed held-out sets measured once (`2024Q4-eval-v8`) and the multi-turn resolution set (`2024Q4-resolution-v1`, PR #48). The runner has the confirmation turn, fault injection and an offline `verify` |
| `evidence/` (evaluation runs) | Natalia | Metrics by language and country from the output of the runner, frozen for each run. Cost per resolution (REQ-0055, REQ-0057). | Done: the label universe `evidence/evaluation/2024Q4-v1/` and the thresholds `2024Q4-v2`, both verified on the regenerated data on 10/02. Each run is frozen in its folder. The latest are `2024Q4-eval-v8` and `2024Q4-resolution-v2`. `evaluation-final` covers the breakdown by language and country of the system outcomes, and the cost per resolution against the baseline as ROI |
| `sentinel-ai-core/app/services/`, `tools/gold_duckdb.py`, `schemas/`, `db/`, `models/` | Natalia, Felix | The reader of the PII-free Gold view behind `GoldTransactions` (with a fallback to the mock), the typed API contract (`schemas/chat.py`), and the SQLite models and stores for sessions, conversation and cases (`db/`, `models/`, `state/`). | Done: the contract, the SQLite state and the Gold reader over the DuckDB file of the pipeline, with tests (PRs #43 and #50). A local users file for real customers is written outside git |
| Infrastructure as code | Nobody yet | Not necessary for the submission. It runs on Azure Container Apps from `deploy/azure/deploy.sh` ([019](../docs/build/decisions/019-azure-container-apps.md)). Scaled-out Azure infrastructure stays production work. | Not started |

Evaluation lives inside `sentinel-ai-core/` because it drives `POST /api/v1/chat`. It is not a third code folder. Its results follow the write-once rule of `evidence/`.

## Mocks

We start with well-documented mocks. We swap them for the real component one by one, without a change to their contracts. This section shows the plan for the transaction-disputes flow.

- **Wed 9/30, skeleton (planned for Tue 9/29):** the loop and the policy engine are in `sentinel-ai-core/`, with in-memory fakes for look up, open (idempotent) and read-back. The chat, the test session and `POST /chat` are connected and verified end to end. The confirm box, the structured logs, the adversarial set (29 attacks, `0/29` unsafe), the prompted router, the evaluation evidence and the evaluation runner all landed and the team archived them on 9/30. The handoff stays an outcome, not a tool. Policy lives in code. The country parameters live in `config/policy/`. The LLM understands, drafts and picks which tool to call. It never decides permissions and never confirms actions.
- **When we swap each mock:** when the milestone asks for it, without a change to the contract.

| Milestone | Stays a mock | Becomes real | Not in this submission |
|---|---|---|---|
| Tue 9/29 | Nothing was ready. The skeleton moves to Wed | — | — |
| Wed 9/30 | Four tools in memory, test session, synthetic policy configuration, simulated advisor and `.env` | Chat and `POST /chat`, orchestrator loop, policy engine and JSON handoff | Identity provider and Key Vault |
| Thu 10/1 | Test session with false credentials, synthetic policy, demo advisor user, and the Gold mock when the DuckDB view is absent | Case store, sessions and conversation out of the process (SQLite). DuckDB Gold adapter. Advisor ticket view. Structured confirmation, bounded retries and structured logs | PostgreSQL and more than one instance |
| Fri 10/2 | Anything that we did not reach, reported as a limitation | Evaluation runner and results. Incremental pipeline (tested). Free-text masking before the model | Advisor delivery channel: a queue to the CRM ([015](../docs/build/decisions/015-handoff-delivery.md)) |

The dispute-record engine is SQLite for the submission. Postgres is the production step (a URL change, same models).

- **Rule:** each mock documents its contract and its limitations, as the brief asks (Data and execution boundaries): REQ-0004 (safe tools), REQ-0007 (permissions in code) and REQ-0032 (documented mocks).
- **Learned component:** where a fixed rule stands today, we keep it as the baseline. We compare it with the component on the same held-out set (REQ-0016).
