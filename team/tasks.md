---
language: en
style: ASD-STE100
last_reviewed: 2026-10-05
---

# Tasks

This page is the record of the first phase. It is not the current plan. The index is in [the team record](README.md).

This page lists who does what and by when, for each day. When you pick a task, add your name. When you finish it, mark it. If a task covers a requirement, cite its `REQ-####` and update its status in the [requirements](../docs/requirements/requirements.md).

**States:** Pending, In progress, Done. Open tasks are in [open work by priority](#open-work-by-priority). Finished tasks stay in the day log.

## Summary

The [plan schedule](plan.md#schedule) has the daily goals and milestones. The flow is transaction disputes, entered through an account inquiry ([decision 003](../docs/build/decisions/003-disputes-flow.md)).

| Day | Milestone | Tasks |
|---|---|---|
| Mon 9/28 | Decisions recorded. First data measurements | [See](#mon-928) |
| Tue 9/29 | Flow confirmed. Architecture reviewed (skeleton not reached) | [See](#tue-929) |
| Wed 9/30 | The skeleton answers end to end. One case works fully | [See](#wed-930) |
| Thu 10/1 | 3 cases in es-419 and pt-BR, public link | [See](#thu-101) |
| Fri 10/2 | Router v2 served with baseline fallback. Router v3 planned | [See](#fri-102) |
| Sat 10/3 to Sun 10/4 | Router v3 measured and served. **Code and results frozen Sun 10/4 night** | [See](#sat-103-to-mon-105) |
| Mon 10/5 | Presentation and video done on the frozen build. Submitted before 11:59 pm (UTC-5) | [See](#sat-103-to-mon-105) |

## Open work by priority

This section lists each open task, ordered by what the submission needs first. Each task cites the requirement that it closes. The order follows the [dependencies between requirements](../docs/requirements/requirements.md#dependencies). The day sections below are the log of finished work.

### Critical: blocks the submission (P0)

| # | Task | REQ | Owner | Due | Unblocks | Status |
|---|---|---|---|---|---|---|
| 1 | Public link: `Dockerfile`, container secrets and demo variables ([019](../docs/build/decisions/019-azure-container-apps.md)) | REQ-0035 | Felix | Fri 10/2 | Video on the deployed tool (REQ-0037) | Done: the link is live with `router_v2`. The final redeploy of 10/5 serves the frozen build. `GET /api/v1/health` returns `bundle_hash` `2efe5962…` ([delivery](../docs/build/delivery.md#gate-g3-record)). The state is on an Azure Files share ([REQ-0035](../docs/requirements/delivery.md#req-0035)) |
| 2 | Pipeline quality report: add nulls, orphaned records, late arrivals and Bronze counts for partitioned tables. Explain the drop from the declared volumes | REQ-0015 | Natalia | Fri 10/2 | REQ-0015 done | Done: the runner generates the full report. A `verify` mode checks its figures (`quality-report`, PR #54, archived 10/3). Silver keeps the durations and `process_date` columns (PR #44) |
| 3 | Charge lookup on Gold, or the fixture if the read path is not up (declared) | REQ-0003, REQ-0015 | Natalia, Rubén | Fri 10/2 | Normal case on real data | Done: PR #50 (`real-gold`) reads the PII-free view from the DuckDB file. `SENTINEL_GOLD_DUCKDB` or the repository path selects the file. It excludes rows after the reference date. It writes local users for real customers outside git |
| 4 | Normal case end to end with real data | REQ-0009 | Rubén, Felix | Fri 10/2 | Demo on real data | Done: the normal, ambiguous and handoff cases ran on real Gold locally in es-419 and pt-BR ([MT-09](chat-manual-tests.md)). The public link stays on the mock |
| 5 | Measure the router models of [016](../docs/build/decisions/016-router-models.md). Expand the cases first. Run the five candidates on Fireworks from `.env`. Apply the selection rule. Freeze a new run. Then serve the chosen pair | REQ-0016, REQ-0019 | Rubén | Sun 10/4 | Metrics, trade-offs and slides with a real delta | Done: `2024Q4-eval-v7` froze the comparison (REQ-0016). The link serves router_v2 with a baseline fallback (checked 10/02) |
| 6 | Write the pt-BR twins of the key cases. Check them by back-translation ([017](../docs/build/decisions/017-portuguese.md)). Include the three demo cases | REQ-0012, REQ-0009 | Unassigned | Fri 10/2 | Normal case in Portuguese, the 3 demo cases in pt-BR | Done: four variants signed (`eval/review/demo-pt-br.md`). Pix hands off. Extrato and fatura show the charges of the account (`tests/test_demo_pt_br.py`). A 2% development replay gave 280 handoffs and 2 prefixes ([evidence](../evidence/transcript-chats/20261002T144836Z/summary.json)) |
| 7 | Final metrics report on the frozen run: n, mix, variability, failures, justified splits and thresholds | REQ-0055, REQ-0022, REQ-0017, REQ-0020 | Unassigned | — | Trade-offs, slides | Done: the [report](../docs/build/metrics-report.md) covers eval-v8 and the final resolution run `2024Q4-resolution-v2` (v1 beside it, both verify offline). It has the breakdown by variant and country (all groups descriptive), the country monitoring over the simulated replay workload and the ROI link. The v8 result serves `router_v2` (v3 fails the zero-unsafe-wording gate and the subtype gate). 018 documents the v8 verify difference in `router_v3` |
| 8 | Failure analysis and limitations: no Portuguese in the dataset, only MX, CO and AR, small samples, capacity, deployment and risks | REQ-0013, REQ-0030 | Unassigned | Fri 10/2 | README, slides | Done: the README has the limitations section and the roadmap. Slide 6 has the limits, the mocks and the roadmap. REQ-0013 stays in progress for the 20-label human check |
| 9 | Path to production write-up, including monitoring. Handoff delivery decided ([015](../docs/build/decisions/015-handoff-delivery.md)) | REQ-0052 | Rubén | Fri 10/2 | — | In progress: [specification](../docs/architecture/specification.md#path-to-production) |
| 10 | Review the repository for secrets and data, including the bucket id in older commits. Freeze the code | REQ-0034 | Felix | Sun 10/4 | Public link, submission | Done: gitleaks over the full history (0 findings) and a manual review. The team accepted and documented the bucket name in [security](../docs/build/security.md#history-review-req-0034-101). The freeze happened on 10/5 ([delivery](../docs/build/delivery.md#gate-g3-record)). The scan of the tracked files on 10/5 found no bucket name |
| 11 | Final README update: results and limitations | REQ-0030 | Unassigned | — | — | Done: the README states the sealed v8 results, the limitations, the roadmap and the served build |
| 12 | Start the video script | REQ-0037 | Unassigned | — | Video | Done: the video script matches the final build. The recording is task 16 |
| 13 | Outline the presentation: structure and sources of the 4 to 6 slides, no results yet | REQ-0036 | Unassigned | — | Validation Fri | Done: six slides in [the deck](https://rdorta27.github.io/sentinel-engine-site/slides/deck.html) |
| 14 | Validate the presentation outline with the group | REQ-0036 | Unassigned | — | Slides | Done: the group validated the outline. The final six slides are in [the deck](https://rdorta27.github.io/sentinel-engine-site/slides/deck.html), in the three languages |
| 15 | Review and complete the presentation with the frozen results | REQ-0036, REQ-0056 | Unassigned | — | Submission | Done: the slides use the numbers of [`numbers.json`](https://github.com/rdorta27/sentinel-engine-site/blob/main/site/numbers.json) and the build line of the frozen build. The three PDFs have six pages each |
| 16 | Record and edit the video (3 minutes at most) | REQ-0037 | Unassigned | — | Submission | Done: the video is published at (retired after the hackathon). It uses the voice of the owner, in English. The script and the 11 mockups match the final build |
| 17 | Pre-submission language check: README, slides, video script, `docs/`, `team/` | REQ-0051 | Unassigned | — | Submission | Done: the pages under `docs/` and `team/` carry the ASD-STE100 header, and the review rewrote them. The slides, the video script and the README match the final build. The style report is `scripts/check_docs.py`. The pass is archived on 10/5 |
| 18 | Submission, with an internal deadline well before Mon 11:59 pm (UTC-5) | — | Unassigned | — | — | Pending |
| 19 | Critical fixes only after the freeze | — | Unassigned | — | — | Pending |
| 20 | Router v3 and a new held-out measurement ([plan](router-v3-plan.md)): greeting and small-talk cases, definitions in the prompt, amendment to [018](../docs/build/decisions/018-evaluation-acceptance.md), new sealed set, one run `2024Q4-eval-v8`, then serve v3. If it does not land by Sun 10/4, submit router_v2 with the limit stated | REQ-0016, REQ-0017, REQ-0019, REQ-0020 | Unassigned | — | Final metrics, README, slides | Done: `router-v3` (PR #59) and `eval-v8` (PR #67) are merged. `router-v3` is archived. The single measurement `2024Q4-eval-v8` ran once. The verdict serves `router_v2`, because v3 fails the zero-unsafe-wording gate (4/93) and the subtype gate (0.8971 against 0.95) ([018](../docs/build/decisions/018-evaluation-acceptance.md#result-v8-added-2026-10-05)). Prompt v3 stays off |
| 21 | Make the synthetic policy honest ([sources](../docs/rationale/policy-sources.md)). A person verifies the rows of the verification table that are `secondary source only`. The person re-reads the Argentine article numbers, finds the window of Colombia and checks the data dictionary for a card network field. The person decides whether the engine learns the window start and the bank obligation ([021](../docs/build/decisions/021-dispute-policy-sources.md)). Then set `source` in each country file (the invented "(Art. 4)" citation, the hard-coded "90 días" and the unlabelled estimated time are fixed) | REQ-0033 | Unassigned | — | README, slides | In progress: the table was filled on 10/02 from a web search. Nobody verified it. The policy stays a declared demonstration |
| 22 | A chat that behaves better ([plan](chat-behavior-plan.md), observations in [manual tests](chat-manual-tests.md)): richer reading, locate the charge, contrast what the customer says with the data, explain decisions, evaluation by conversation and a new sealed set | REQ-0001, REQ-0002, REQ-0016, REQ-0017 | Unassigned | — | Final metrics, slides | Done: narrowing, the not-found reply, the prompt-extraction refusal and the injection record (PR #49, `chat-loop`). The interface (`ui-product`, `bank-ui`). Openers, status answers, the "why?" answer and validated drafts (`router-v3`, `chat-start`, PR #62). The final measurement is `2024Q4-eval-v8` |

### High: scores points once P0 is on track (P1 and team hygiene)

| # | Task | REQ | Owner | Due | Unblocks | Status |
|---|---|---|---|---|---|---|
| 1 | Archive the OpenSpec changes `align-canonical-api-v1`, `persist-state-and-dispute-api`, `serve-demo-ui-with-advisor-view` and `add-fraud-and-high-amount-rules` after PR #29 merges | — | Rubén | Fri 10/2 | — | Done: all four are under `openspec/changes/archive/` (2026-10-01). The main specs are synced |
| 2 | Ship a commit hook for every clone | — | Unassigned | — | — | Cancelled: the repository no longer ships a hook. The owner checks messages with a local hook |
| 3 | ROI against the baseline with cost per resolution, labelled as a projection | REQ-0057 | Unassigned | — | — | Done: [roi](../docs/build/roi.md) is a break-even over frozen call-center aggregates ([evidence](../evidence/roi/2023-2026-callcenter-v1/summary.json)). The assumed advisor hour is labelled assumed. The page claims no saving |
| 4 | Breakdown by authorized segment and disparity analysis on the frozen run | REQ-0024 | Unassigned | — | Limitations | Done: [resolution-v2](../evidence/evaluation-runs/2024Q4-resolution-v2/summary.json) breaks system outcomes down by variant and country with n and situation-level intervals (all descriptive). The segment is declared not measured (the cases carry no customer record). The dataset figures are cited as context |
| 5 | Report by country (latency, failures, escalations) from the JSONL logs | REQ-0050 | Unassigned | — | Path to production | Done: `sentinel-ai-core/eval/monitor.py` keeps aggregates only. It froze a run over the simulated replay workload ([evidence](../evidence/monitoring/2024Q4-resolution-v2-replay/summary.json)). A field run reads the Azure log with the same script |
| 6 | Neutral Spanish: apply the glossary and add a case with the term of another country | REQ-0044 | Unassigned | — | — | Pending |
| 7 | Keep `amount_usd` in `silver_transactions` (filled in about 95% of ARS and COP charges, empty by design in USD) for cross-country comparisons | REQ-0024 | Unassigned | — | — | Done: `silver_transactions` keeps `amount_usd` |
| 8 | Move the pages of `docs/understand/` to `docs/overview.md`, `docs/data/` and `docs/glossary/`. Fix the links. Update `AGENTS.md`. Remove the folder ([plan](../openspec/changes/archive/2026-10-05-docs-followups/tasks.md), group 6) | REQ-0034 | Unassigned | After the other plans merge | — | Done: the pages moved. The links are fixed. `scripts/check_links.py` is clean ([decision 30](pending-decisions.md#decided)) |
| 9 | Evidence hardening ([plan](../openspec/changes/archive/2026-10-05-evidence-hardening/tasks.md)): explain the resolution gap, measure latency and cost live, report bases and a 20-label human check, publish negative results | REQ-0022, REQ-0055, REQ-0021, REQ-0013 | Rubén | Before the slides close | Slides and site numbers (REQ-0036) | In progress: the gap run, the live rehearsal, `bases`, the negative-results page, the mocks page and the cut-off diagnosis are done. Remaining: the 20-label review, the live run on the frozen build (task 2.4), the three attack cases against the real model (task 4.2), the repeats (task 3.5) and the slide limits |
| 10 | Demo clarity ([plan](../openspec/changes/archive/2026-10-05-demo-clarity/tasks.md)): rename the example buttons, show them only in demo mode, add a build line and a guide for the judge, with no change to the chat | REQ-0038 | Unassigned | Before gate G3 | Phone captures and the slides | Done: label, build line, judge guide and the empty-account fixes. The screens are refreshed |
| 11 | Judge access ([plan](../openspec/changes/archive/2026-10-05-judge-access/tasks.md)): no passwordless entry on the public link. The judge credentials go in the submission email, not in the repository | REQ-0027 | Unassigned | Before gate G3 | The final redeploy and the submission email | In progress: the persona flag, the banner, the users script, the deploy pieces and the docs are done. Task 2.4 (the remote check) waits for `live-ops` 1.3. The final redeploy and the email stay in `post-freeze` |
| 12 | UI behavior ([plan](../openspec/changes/archive/2026-10-05-ui-behavior/tasks.md)): one turn at a time, the right language, URL navigation, the advisor list with a JSON tab, one ticket for each charge and information cards for closed charges | REQ-0038, REQ-0042, REQ-0008 | Rubén | Before gate G3 | The final redeploy: the page is part of the frozen build | Done: the code, the tests (`tests/test_ui_behavior.py`) and the checks are done. The owner approved the screens. Archived on 10/5. The product screens under `docs/build/screenshots/ui-product/` still need a new capture |
| 13 | Final documents pass after the release ([plan](../openspec/changes/archive/2026-10-05-docs-followups-2/tasks.md)): public link pages, numbers, requirement statuses, archive, team, language, links and repository hygiene | REQ-0051 | Unassigned | After `release` | The tags and the submission | Done: the pitch pages, the public link and evidence pages, the requirement statuses, the secret scan, the delivery checklist, the language pass and the archive are complete. The plan is archived on 10/5 |

### Low: only if time remains (P2) or to confirm and close

| # | Task | REQ | Owner | Due | Unblocks | Status |
|---|---|---|---|---|---|---|
| 1 | Close as not applicable if no LLM judge is used | REQ-0023 | Unassigned | — | — | Pending |
| 2 | Recent app-error context offered as a question | REQ-0045 | Unassigned | — | — | Pending |
| 3 | Simulated handoff routing by language and specialty | REQ-0046 | Unassigned | — | — | Pending |
| 4 | Keyword baseline for dispute category, with a time-based split. Confirm whether the served keyword baseline covers it. Then close | REQ-0016 | Unassigned | — | — | Pending |
| 5 | First look at the data: table inventory against the dictionary | — | Rubén | — | — | In progress |
| 6 | Record your preference in [pending decisions](pending-decisions.md) | — | Unassigned | — | — | Pending |

## Log by day

### Mon 9/28

| Task | Owner | Status |
|---|---|---|
| Confirm that the S3 credentials work for all 3 (Natalia already tested them. Rubén verified on 9/28: the bucket listing is OK) | Felix, Rubén | Done |
| Push the ingestion script to the repository, with no credentials. Read them from `.env` | Natalia | Done: Bronze ingestion is in `sentinel-data-engine/`. The code reads the bucket name from `.env`. It is no longer in the tree (older commits still have it, see the secrets review on Fri) |
| Measure the dispute volume for unrecognized charges (`case_type = Claim` and category) and its weight in `contact_reason` | Rubén | Done: [evidence](../docs/build/flows/02-flow-measurements.md) |
| Measure what % of dispute-related complaints has a valid `origin_interaction_id`. Measure what % of those interactions has a transcript | Rubén | Done: [evidence](../docs/build/flows/02-flow-measurements.md) |
| Profile the candidate labels: `category`, `subcategory` and `was_escalated` (balance, consistency, template-like or not) | Rubén | Done: [evidence](../docs/build/flows/02-flow-measurements.md) |
| List the opening fields and the outcome fields of `complaints`, to avoid data leakage | Rubén | Done: [evidence](../docs/build/flows/02-flow-measurements.md) |

### Tue 9/29

| Task | Owner | Status |
|---|---|---|
| Review [decision 003](../docs/build/decisions/003-disputes-flow.md): confirm the disputes flow or switch to cards. Set thresholds | Team | Done: the team confirmed disputes on 9/29 ([flow selection](../docs/build/flows/03-flow-selection.md)) |
| Pick the learned component | Team | Done: a prompted LLM, 9/29 ([decision 007](../docs/build/decisions/007-learned-component.md)) |
| Architecture: system, demo and specification | Rubén | Done: [architecture](../docs/architecture/README.md), PR #9 |
| Scope of the account inquiry | Rubén | Done: [decision 008](../docs/build/decisions/008-account-inquiry-scope.md) |
| Analysis that backs the flow: contact reasons, demand and data quality | Rubén | Done: [flow selection](../docs/build/flows/03-flow-selection.md) |

The team did not reach these items on Tuesday. They moved to Wednesday: the backend skeleton, the chat, the handoff schema, the held-out design and the Portuguese source.

### Wed 9/30

| Task | Owner | Status |
|---|---|---|
| Backend skeleton: orchestrator, policy engine and 4 mock tools with the [contracts](../docs/architecture/specification.md#tool-contracts) (open dispute is idempotent) | Rubén, Felix | Done: the loop, the policy engine and the tools are in `sentinel-ai-core/` (cases are now in SQLite). The handoff is an outcome that the system files as a ticket. The chat is connected |
| Simple chat with a test session and conversation state, connected to `POST /chat` | Felix | Done: the chat page, the test session and the confirm box are verified end to end. The route is now `POST /api/v1/chat` (web session to a verified case, and `test_full_turn_is_replayable_by_trace_id`) |
| Synthetic policy configuration for each country (MX, CO, AR), with placeholder thresholds for decisions 25–27 | Rubén | Done: `sentinel-ai-core/config/policy/`. `evidence/evaluation/2024Q4-v1/summary.json` froze the reference percentiles. The thresholds were still provisional |
| JSON handoff schema (request, verified facts, actions, evidence, open questions, language, country) | Rubén | Done: the package carries the request, the summary, the conversation for each turn, the verified facts, each attempted action, the evidence, the open questions, the language and the country. It has no `customer_id` and no raw text. The system files it as a ticket (`tests/test_handoff_package.py`) |
| Gold view with only the [data contract](../docs/architecture/specification.md#data-contract) columns and no personal data | Natalia | Done: the pipeline writes `v_service_dispute_eligible_transactions` without names or credit score (`sentinel-data-engine/src/sentinel_data/gold/build_gold.py`). It keeps `is_fraud` and segment. The service does not read them |
| Evidence run that records claim categories and subcategories with counts | Natalia, Rubén | Done: `evidence/evaluation/2024Q4-v1/summary.json` (10 Claim combinations, full counter) and the derived `sentinel-ai-core/eval/labels.json` |
| Design the held-out set: labels (from the v4 category list) and locales | Rubén | Done: development and held_out splits with no shared ids in `sentinel-ai-core/eval/cases/` |
| Define the source and the reviewer of the Portuguese test cases (decision 15) | Rubén | Done (source): 13 team-written pt-BR cases declared as simulation. The reviewer was still open (decision 15) |
| Look for a justified external source of pt-BR complaints (license, no PII) | Unassigned | Dropped: the team-written cases cover it. Reopen only if decision 15 requires it |
| Action verification: the dispute exists after creation | Rubén | Done: read-back verification with `lookup_dispute` and the `verify` record |
| Handoff integrated into the flow | Rubén | Done: the out-of-scope, person-insist and failure paths hand off with reason keys |
| Prompted LLM router against the keyword baseline, with cost and latency | Rubén | Done (mirrored fixtures, delta zero by construction): `openspec/specs/llm-router/spec.md`. The live-model comparison waited for decision 10 |
| First evaluation cases (JSONL) | Rubén | Done: 35 cases in `sentinel-ai-core/eval/cases/` |

### Thu 10/1

| Task | Owner | Status |
|---|---|---|
| Ambiguous and human cases | Rubén | Done: the missing, person and out-of-scope cases in `sentinel-ai-core/eval/cases/` replayed green |
| Decide the advisor queue, the role landing and the admin scope (pending decision 29): implement, JSON-only or counts-only | Rubén | Done: [009](../docs/build/decisions/009-demo-ui-and-advisor-view.md), a read-only advisor view, no admin panel |
| PII review of the advisor summary before any queue UI (REQ-0047, REQ-0008) | Rubén | Done: the package has no names, no raw text and no unverified references. The advisor sees the customer id and the country only (`tests/test_handoffs_api.py`, `tests/test_handoff_package.py`) |
| Portuguese | Rubén | Done (router only): 13 single-turn pt-BR utterances and router detection in `tests/test_ai_router.py`. Serving a Portuguese-speaking customer was still open (see open work) |
| Failure handling: down tools, expired session and bounded retries | Rubén | Done: the `ModelUnavailable` fallback and the fault injection of the runner. All degrade safely |
| Structured confirmation: confirm box and `confirmation_token` ([confirmation](../docs/architecture/specification.md#confirmation)) | Felix, Rubén | Done: the confirm box is verified end to end. The token stays on the server and the page never renders it |
| Structured logs with `trace_id`, latency, tokens and cost ([observability](../docs/architecture/specification.md#observability)) | Rubén | Done: the records and the JSONL writer of `app/observability/` run from `step()` and `POST /api/v1/chat`. The audit moved off cleartext PII. The acceptance test is green. `var/` is anchored to the package |
| Adversarial set: prompt injection and unauthorized access | Felix | Done: 36 attacks in `tests/adversarial/` (chat, disputes API and advisor endpoint), `0/36` unsafe (`evidence/adversarial/20261001T130342Z/summary.json`). The PII free-text attack `A9` stays `no_defense_yet` (REQ-0021, REQ-0047) |
| Integrate PR #20 and align one API: one app at `app.main:app`, everything under `/api/v1` and typed chat replies that the page renders | Natalia (Rubén integrated) | Done: `tests/test_contract.py`. OpenSpec change `align-canonical-api-v1` |
| Persist sessions, conversation and cases in SQLite (mentor feedback). Delete the conversation on logout and on expiry | Natalia (Rubén integrated) | Done: `tests/test_state_sqlite.py`. OpenSpec change `persist-state-and-dispute-api` |
| Two-step disputes API and one open dispute for each charge across sessions | Natalia, Felix (Rubén integrated) | Done: `tests/test_disputes_api.py`, adversarial B9, B10, C6, D6 and D7 |
| Handoff ticket with the conversation summary and each attempted action | Natalia (Rubén integrated. Rubén added the summary and the attempted actions) | Done: `tests/test_handoff_package.py` |
| Advisor view, role landing and roles in code. Remove the old mock backend | Felix (Rubén integrated) | Done: `tests/test_handoffs_api.py`, adversarial B11 and B12. [009](../docs/build/decisions/009-demo-ui-and-advisor-view.md) |
| Test that no reply shows amounts or merchants outside the verified facts | Rubén | Done: `tests/test_facts_grounding.py` (mutation-checked) |
| Tell Felix and Natalia: the old mock backend is retired, the single API replaced the routers of PR #20, and Gold eligibility uses `CURRENT_DATE` | Rubén | Done |
| Fraud and high-amount thresholds for each account country and currency (decisions 25 and 26) | Rubén | Done: [010](../docs/build/decisions/010-fraud-handoff-rule.md), [011](../docs/build/decisions/011-high-amount-threshold.md). Evidence `evidence/evaluation/2024Q4-v2/`, run `2024Q4-eval-v6` |
| Source inventory: each input is labeled by origin, no external data ([inventory](../docs/data_inventory.md)) | Natalia | Done: REQ-0031, REQ-0054 |
| Pipeline run end to end on the full dataset with a quality report. Silver normalizes `México`. Gold uses the 2026-06-17 cut-off | Natalia | Done: `data/gold_bank.duckdb` (gitignored), [report](../sentinel-data-engine/data_quality_report.md). The quality metrics were still incomplete (open task) |
| Labelled incremental fixture: late arrival, duplicate and schema change | Natalia | Done: `sentinel-data-engine/tests/test_incremental_fixture.py` (REQ-0018) |
| Homologate the file names | Rubén | Done: renamed the sizing page to [sizing-capacity](../docs/sizing-capacity.md) (REQ-0053) |
| Data setup in two steps: sync the raw tables, then build the DuckDB file | Natalia | Done: [quickstart](../sentinel-data-engine/README.md#9-local-development-quickstart) (REQ-0028) |
| Mask personal identifiers in free text before the model | Felix | Done: `app/privacy/`, `tests/privacy/`. Adversarial A9 is blocked in `evidence/adversarial/20261002T120107Z/summary.json` (REQ-0047) |
| Data findings for thresholds: Mexican accounts are USD only, `Mexico` names purchases in Mexico, Silver drops `amount_usd` | Rubén | Done: [dataset assumptions](../docs/data/dataset.md#assumptions). The team asked in the help channel |
| A person request while the confirm box is open makes a handoff like any other. Insisting after other messages still makes a handoff. The system logs the extra model call | Felix (Rubén reviewed and fixed) | Done: `tests/test_person_while_confirming.py`, PR #30 (REQ-0040) |
| Close pending decisions 10, 13, 14, 15, 16, 23, 27 and 28 | Rubén | Done: [012](../docs/build/decisions/012-public-deployment.md) to [017](../docs/build/decisions/017-portuguese.md) |
| Regroup the requirements by type (frontend and backend, non-functional, data and ML, analytics and delivery) with one card each and their dependencies | Rubén | Done: [requirements](../docs/requirements/requirements.md) |

### Fri 10/2

| Task | Owner | Status |
|---|---|---|
| Evaluation runner and held-out metrics (safe resolution, unsafe outcomes, handoff, latency and cost) | Rubén | Done early on 9/30. The latest frozen run was `evidence/evaluation-runs/2024Q4-eval-v5/` on the aligned API (0 failures, same metrics as v1 except latency) |
| Metrics by language and country, cost per resolution, frozen in `evidence/` | Natalia, Rubén | Done: the frozen run has the metrics by locale and by country with small-sample limits. Cost per resolution is "not defined" (no resolutions by design) |
| Retire the old mock backend once ai-core runs the demo alone (a cleanup change, only with ai-core E2E green and the migration change archived) | Rubén | Done: the team removed the backend, the tests, the packaging and the reference page ([009](../docs/build/decisions/009-demo-ui-and-advisor-view.md)) |

### Sat 10/3 to Mon 10/5

This table lists the pull requests that merged into `main` (read on 2026-10-05). [Open work by priority](#open-work-by-priority) lists the open work.

| Day | Pull request | What it did |
|---|---|---|
| Sat 10/3 | #52, #53 | `runtime-and-ci`: durable state, platform logs and CI. The public link was redeployed from #52 |
| Sat 10/3 | #54 | `quality-report`: the pipeline generates the data quality report |
| Sun 10/4 | #55, #56 | `evaluation-final` (breakdown, monitoring and ROI) and `router-confidence` |
| Sun 10/4 | #57, #58 | `ui-product` (product interface and advisor trace) and the customer-signals evidence |
| Sun 10/4 | #59, #60, #61 | `router-v3`, `flow-fixes` and `bank-ui` |
| Sun 10/4 | #62, #63 | `chat-start` (the chat behaves better) and `problem-evidence` |
| Sun 10/4 | #64, #65 | `trained-baseline` and `charge-ranker` (selector off by default) |
| Mon 10/5 | #66, #67 | `robustness-evidence` and `eval-v8` (sealed sets, rehearsal and ablation) |
| Mon 10/5 | `eval-v8-measure` | The single v8 measurement, the verdict, the reports and the analysis |
| Mon 10/5 | `post-freeze` (#81) | The freeze record, the final redeploy, the live latency run and the robustness runs |

After the freeze: the v8 measurement ran once. The verdict serves `router_v2`. The robustness runs and the final redeploy are done. The video recording, the tags and the submission email are still open.

## To find out

These items need information, not a decision. They are in date order.

| Question | Who finds out | By when | Status |
|---|---|---|---|
| What format and partitions does the S3 data have? | Natalia | Sun 9/27 | In progress |
| Are there published data terms of use? (the brief mentions them) | Hackathon help channel | Mon 9/28 | Pending |
| What does the "public\*" asterisk mean? Must the repository be public from the start? | Hackathon help channel | Mon 9/28 | Pending |
| Do the terms of use allow a copy of the S3 data to Azure (ADLS)? | Hackathon help channel | Mon 9/28 | Pending |
| How much does Databricks cost (SQL Warehouse and, if used, the Llama endpoint) from 10/1 to 10/5? | Natalia | Mon 9/28 | Done: USD 20-58 in total, within the trial credit |
| Deadline on Monday 10/5 and maximum video length | Hackathon help channel | Mon 9/28 | Done: 11:59 pm (UTC-5). The video lasts 3 minutes at most |
| Is the Azure OpenAI model that we want available in our region? | Whoever provides the subscription | Mon 9/28 | Pending |
| Are there several monthly snapshots? How did the data owner compute `is_repeat_complainer`? | Data area | With the data sample | In progress: there is one snapshot, with `last_updated` up to 2027. `is_repeat_complainer` is still open |
| How many late arrivals are there (gap between `process_date` and `transaction_date`)? | Data area | With the data sample | Done: about 25% of rows are one day late ([dataset](../docs/data/dataset.md#measured-issues-q4-2024)) |
| Where does the 90-day dispute window come from (regulation, card network or assumption)? | Natalia | Tue 9/29 | Pending |
| How do we build the reference labels (which cases need a human)? | ML area | Tue 9/29 | Done: team-written simulation cases (`requires_handoff` marks the human cases) and the frozen data labels in `evidence/evaluation/2024Q4-v1/summary.json` |
| Cost assumptions (LLM price and advisor cost) | Analysis area | Thu 10/1 | In progress: the frozen run measured the fixture cost for each turn. The advisor cost and the live-model prices are still open (decision 10) |

## Done

| Task | Owner | Date |
|---|---|---|
| S3 data access tested | Natalia | Sun 9/27 |
| Write access to the repository for Felix and Natalia | Rubén | Sun 9/27 |
| Full team in the hackathon channel | Team | Sun 9/27 |
| Repository created | Rubén | Sun 9/27 |
| Team name: Sentinel Engine | Team | Sun 9/27 |
| Analysis of the challenge documents (datathon kickoff and hackathon brief). Commit on Sunday | Rubén | Sat 9/26 |
| Session-bound charge lookup (`GET /transactions`, now `GET /api/v1/transactions`, and `lookup_transactions`) with isolation, currency and canary tests | Felix | Wed 9/30 |
| Adversarial set: 29 attacks measured, `0/29` unsafe, frozen in [evidence](../evidence/adversarial/20260930T214744Z/summary.json) | Felix | Wed 9/30 |
| Prompted LLM router with route table, fixtures and safe fallback (`openspec/specs/llm-router/spec.md`, change archived) | Rubén | Wed 9/30 |
| Evaluation evidence frozen: label universe, mix and thresholds (`evidence/evaluation/2024Q4-v1/`, change archived) | Rubén | Wed 9/30 |
| Evaluation runner frozen: bench and system replay, 0 failures, unsafe `0/35` (`evidence/evaluation-runs/2024Q4-eval-v1/`, change archived) | Rubén | Wed 9/30 |
| Runtime `var/` anchored to the app package (`SENTINEL_VAR_DIR` override). Stale root `var/` removed | Rubén | Wed 9/30 |
| One app and one API under `/api/v1`. PR #20 integrated | Natalia (Rubén integrated) | Thu 10/1 |
| Sessions, conversation and cases in SQLite with retention | Natalia (Rubén integrated) | Thu 10/1 |
| Disputes API, handoff tickets with summary, advisor view and roles | Natalia, Felix (Rubén integrated) | Thu 10/1 |
| Adversarial set at 36 attacks, `0/36` unsafe ([evidence](../evidence/adversarial/20261001T130342Z/summary.json)) | Rubén, Felix | Thu 10/1 |
| Security hardening of the served app: cookie, headers and CSRF. Write rate limit and chat input contract. Customer text as data. Owner-only database, turn log and salt. Bounded stored turns | Rubén | Fri 10/2 |
| The transactions panel shows only eligible charges. HTTP errors render as errors. Checked in headless Chromium | Rubén | Fri 10/2 |
| One handoff ticket for each conversation | Rubén | Fri 10/2 |
| Deploy: one replica, non-root user, ephemeral state under `/tmp/sentinel`, container healthcheck and a health route that queries the state store. Built and run locally, not yet redeployed | Rubén | Fri 10/2 |
| Adversarial set re-frozen on the hardened code, `0/36` unsafe ([evidence](../evidence/adversarial/20261002T120107Z/summary.json)) | Rubén | Fri 10/2 |
