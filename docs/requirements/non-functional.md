---
language: en
style: ASD-STE100
last_reviewed: 2026-10-05
---

# Requirements: Non-functional

This page covers how the system behaves: security, privacy, reliability, observability and reproducibility. The [requirements index](requirements.md) holds the sources, the classification, the status counts and the dependency chains.

| ID | Requirement | P | Area | Depends on | Status |
|---|---|---|---|---|---|
| [REQ-0005](#req-0005) | Report only verified actions | P0 | ai | [REQ-0032](#req-0032) | Done |
| [REQ-0007](#req-0007) | Permissions and policy in code | P0 | ai | [REQ-0027](#req-0027) | Done |
| [REQ-0021](#req-0021) | Failure tests | P0 | ml, ai | [REQ-0007](#req-0007), [REQ-0012](frontend-backend.md#req-0012), [REQ-0026](#req-0026), [REQ-0027](#req-0027) | Done |
| [REQ-0025](#req-0025) | Observability | P1 | ai | — | Done |
| [REQ-0026](#req-0026) | Bounded retries and safe fallback | P1 | ai | [REQ-0005](#req-0005) | Done |
| [REQ-0027](#req-0027) | Authentication, isolation and retention | P0 | ai, data | — | Done |
| [REQ-0028](#req-0028) | Reproducible setup | P0 | all | [REQ-0015](data-ml.md#req-0015), [REQ-0019](data-ml.md#req-0019) | Done |
| [REQ-0029](#req-0029) | Explanations from sources and rules | P1 | ai | [REQ-0025](#req-0025) | Done |
| [REQ-0032](#req-0032) | Documented mock tools | P1 | ai | — | Done |
| [REQ-0047](#req-0047) | No personal data to the LLM | P0 | ai | [REQ-0027](#req-0027) | Done |
| [REQ-0048](#req-0048) | Decision order | P0 | ai, ml | [REQ-0016](data-ml.md#req-0016) | Done |
| [REQ-0049](#req-0049) | Country as configuration | P2 | ai | — | Done |
| [REQ-0056](#req-0056) | Explicit trade-offs | P0 | all | [REQ-0016](data-ml.md#req-0016), [REQ-0055](analytics.md#req-0055) | In progress |

<a id="req-0005"></a>
### REQ-0005 · Report only verified actions

The system tells the customer that an action happened only after it reads the action back. The system never reports a timeout or an error as a success.

**Priority:** P0 · **Status:** Done · **Criterion:** AI Engineering · **Area:** ai

**Source:** Problem statement: What your solution should demonstrate 2 · Kickoff p. 11

**Depends on:** [REQ-0032](#req-0032). The read-back uses the tool contracts.

**Evidence:** Proven by tool-failure tests. When a write fails or is not confirmed, the result is a handoff and not a success message (`lookup_dispute` read-back and the `verify` record).

<a id="req-0007"></a>
### REQ-0007 · Permissions and policy in code

Code in the service enforces who can see or do what. The prompt does not enforce it. A manipulated model still cannot break the rules.

**Priority:** P0 · **Status:** Done · **Criterion:** AI Engineering · **Area:** ai

**Source:** Problem statement: What your solution should demonstrate 3; Data and execution boundaries · Kickoff p. 13

**Depends on:** [REQ-0027](#req-0027). Roles and per-customer checks need the session.

**Evidence:** Proven by:

- The policy engine in code.
- Roles enforced for each route. Customer routes need `customer`. `/api/v1/handoffs` needs `advisor`. A failure is a 403 and the system records it as `access_denied`.
- The adversarial groups B, C and D in [`evidence/adversarial/20261001T130342Z/summary.json`](../../evidence/adversarial/20261001T130342Z/summary.json).

<a id="req-0021"></a>
### REQ-0021 · Failure tests

Test the cases that the brief names: bad or missing data, expired session, unauthorized access, prompt injection, tool failure and multilingual ambiguity.

**Priority:** P0 · **Status:** Done · **Criterion:** Machine Learning · **Area:** ml, ai

**Source:** Problem statement: What your solution should demonstrate 5 · Kickoff p. 13

**Depends on:** [REQ-0007](#req-0007), [REQ-0012](frontend-backend.md#req-0012), [REQ-0026](#req-0026), [REQ-0027](#req-0027). The attacks test permissions, languages, fallback and the session.

**Evidence:** Proven by 42 attacks in `tests/adversarial/`. They target the chat, the disputes API and the advisor endpoint. The `unsafe_outcome_rate` is `0/42`: 38 `blocked_verified`, 3 `passes_on_mock`, 1 `documented` and 0 `no_defense_yet`. The source is [`evidence/adversarial/20261005T014816Z/summary.json`](../../evidence/adversarial/20261005T014816Z/summary.json).

- A3 refuses prompt extraction in code.
- A4b records an injection and does not change the reply.
- D4 bounds the Gold reads (`SENTINEL_GOLD_TIMEOUT_S`, default 2 s, above the measured cold read of 0.28 s).
- The three attacks that pass on the stand-in model run against the real router model. All 3 pass, so `totals.unsafe_outcome_rate` is `0/3`. See [`evidence/adversarial/20261005T204313Z/summary.json`](../../evidence/adversarial/20261005T204313Z/summary.json).
- The fault-injection run drives the app through seven faults. The baseline answers every model fault and the Gold faults; the store error leaves 2 of 12 unsafe turns. See [`evidence/robustness/20261005T210525Z/summary.json`](../../evidence/robustness/20261005T210525Z/summary.json) and [failure handling](../rationale/failure-handling.md).

<a id="req-0025"></a>
### REQ-0025 · Observability

Keep execution traces and logs for each turn, with the country and the language. Then anyone can rebuild any conversation.

**Priority:** P1 · **Status:** Done · **Criterion:** AI Engineering · **Area:** ai

**Source:** Problem statement: What your solution should demonstrate 6 · Kickoff p. 15

**Evidence:** Proven by:

- Records for each step and each turn in `app/observability/`, with the country and the language. A replay by `trace_id` works (`test_full_turn_is_replayable_by_trace_id`).
- The runner. It reads records by trace id in [`evidence/evaluation-runs/2024Q4-eval-v5/summary.json`](../../evidence/evaluation-runs/2024Q4-eval-v5/summary.json).

<a id="req-0026"></a>
### REQ-0026 · Bounded retries and safe fallback

Retries have a limit. A failure falls back to a safe outcome, usually a handoff. Repeating an action never duplicates it.

**Priority:** P1 · **Status:** Done · **Criterion:** AI Engineering · **Area:** ai

**Source:** Problem statement: What your solution should demonstrate 6 · Kickoff p. 15

**Depends on:** [REQ-0005](#req-0005). A retry is safe only when the system verifies the success.

**Evidence:** Proven by tool-failure tests, the `ModelUnavailable` fallback and the idempotent creation of a dispute. The fault run measures each fallback with counts: the model timeout, the model 5xx and the invalid JSON answer 12 of 12 turns through the baseline, and the store error answers 10 of 12 ([`evidence/robustness/20261005T210525Z/summary.json`](../../evidence/robustness/20261005T210525Z/summary.json), [failure handling](../rationale/failure-handling.md)). The daily budget caps the model spend (`app/ai/budget.py`, [cost guard](../rationale/cost-guard.md)).

<a id="req-0027"></a>
### REQ-0027 · Authentication, isolation and retention

A trusted test session proves the identity. A customer number alone does not prove it. Each customer reaches only their own records. Personal data and conversation data have a retention policy.

**Priority:** P0 · **Status:** Done · **Criterion:** AI Engineering / Data Engineering · **Area:** ai, data

**Source:** Problem statement: What your solution should demonstrate 6; Data and execution boundaries · Kickoff p. 15

**Evidence:** Proven by:

- Password login on `/api/v1/auth/*`.
- The isolation matrix `test_foreign_access_attempts_are_blocked_8_of_8`.
- The `me` route. It returns the role and the country only.
- Sessions and conversations stored by token hash. The system deletes them on logout and on expiry (`tests/test_state_sqlite.py`).
- File permissions. The SQLite file, the turn log and the dev salt are created with mode `0600`. A folder that the app creates has mode `0700` (`test_database_file_is_owner_only`, `test_turn_log_and_dev_salt_are_owner_only`).
- A startup check. The app fails to start if the state directory is not writable (`test_unwritable_state_path_fails_fast`). `SENTINEL_SQLITE_JOURNAL=DELETE` opens the file in that mode (`test_journal_mode_delete`).
- A cap of 50 on the stored turn window.
- The cookie, header, CSRF, rate-limit and input controls in [security](../build/security.md#controls-on-the-served-app-102-hardening).
- The [retention table](../architecture/specification.md#data-retention).

The deploy script keeps the file on an Azure Files share. A restart can then keep an unexpired session. The team redeployed the public revision with that share on 2026-10-03. The cases survived a revision restart ([REQ-0035](delivery.md#req-0035)).

- The public link has no one-click entry. `SENTINEL_DEMO_PERSONAS=0` makes `GET /api/v1/auth/demo` and `POST /api/v1/auth/demo/{persona}` answer 404, and the advisor login keeps its password (`tests/test_demo_auth.py`).
- The test users file holds salted hashes only. The documented fixture passwords fail on the link. The script writes the file and an ignored password sheet, and it prints no password (`tests/test_make_judge_users.py`, `tests/test_judge_users_cases.py`). The deploy copies the file to the share and sets the flag ([deploy notes](../../deploy/azure/README.md), [`judge-access`](../../openspec/changes/archive/2026-10-05-judge-access/tasks.md)).

<a id="req-0028"></a>
### REQ-0028 · Reproducible setup

Anyone can set up the project, rerun the evaluation and get the same results. The code and the data runs have versions.

**Priority:** P0 · **Status:** Done · **Criterion:** Rationale · **Area:** all

**Source:** Problem statement: What your solution should demonstrate 6 · Kickoff p. 15

**Depends on:** [REQ-0015](data-ml.md#req-0015), [REQ-0019](data-ml.md#req-0019). The pipeline is reproducible and the runs have versions.

**Evidence:** Proven by:

- Evidence scripts that use only the standard library, with a `verify` step. `evidence/evaluation/eval_measure.py` also verifies against the hash of the pipeline DuckDB.
- Write-once frozen runs.
- An offline replayable harness (`python3 -m eval.freeze`).
- The data setup in two steps: sync the raw tables, then run the pipeline ([`sentinel-data-engine/README.md`](../../sentinel-data-engine/README.md#9-local-development-quickstart)).
- A local run that reproduced the committed quality report.

<a id="req-0029"></a>
### REQ-0029 · Explanations from sources and rules

Explanations cite the data sources, the policy rules and the execution records. The hidden reasoning of the model is not an audit artifact.

**Priority:** P1 · **Status:** Done · **Criterion:** AI Engineering · **Area:** ai

**Source:** Problem statement: What your solution should demonstrate 6

**Depends on:** [REQ-0025](#req-0025). Explanations cite the logged rules and sources.

**Evidence:** Proven by `policy_rule` on each decide record and in the handoff evidence. The system builds the summary from turn codes. It never builds it from model reasoning (`tests/test_handoff_package.py`).

<a id="req-0032"></a>
### REQ-0032 · Documented mock tools

The team may use mock banking tools if it documents their contracts and limits.

**Priority:** P1 · **Status:** Done · **Criterion:** AI Engineering · **Area:** ai

**Source:** Problem statement: Data and execution boundaries

**Evidence:** Proven by:

- The tool and Gold contracts in the [specification](../architecture/specification.md#tool-contracts).
- The mock Gold and the DuckDB Gold behind one seam, with a fallback (`tests/test_gold_duckdb.py`).
- Memory state and SQLite state behind the same ports.
- The list of mocks in the [demo architecture](../architecture/demo-architecture.md#mocked-components) and in [what is real](../architecture/what-is-real.md#components).
- The [mocks](../architecture/mocks.md) page, which gives the reason, the limit and the production backend of each mock.

<a id="req-0047"></a>
### REQ-0047 · No personal data to the LLM

The model never receives identifiers or personal data. No restricted data goes into an external model request. The tools filter by the session customer instead.

**Priority:** P0 · **Status:** Done · **Criterion:** AI Engineering · **Area:** ai

**Source:** Problem statement: Data and execution boundaries · Own: [security](../build/security.md#llm-visibility)

**Depends on:** [REQ-0027](#req-0027). The tools filter by the session customer.

**Evidence:** Proven by:

- A lookup that the session binds. It takes no customer argument. The 8/8 denial test covers it.
- Auth events stored as salted `session_ref` records with no IP (`test_audit_session_ref_is_a_hash_not_the_customer`).
- A whitelist for the router request. It also keeps the fraud score out (`tests/test_ai_router.py`).
- The orchestrator. It sees an opaque customer hash and never the id.
- Masking. The system masks personal identifiers that the customer types in free text before the model reads them (`app/privacy/`, `tests/privacy/`). For this reason, attack `A9` is `blocked_verified` in [`evidence/adversarial/20261002T120107Z/summary.json`](../../evidence/adversarial/20261002T120107Z/summary.json).

<a id="req-0048"></a>
### REQ-0048 · Decision order

When the sources disagree, the policy in code wins over the learned component. The learned component wins over the LLM.

**Priority:** P0 · **Status:** Done · **Criterion:** Rationale / ML · **Area:** ai, ml

**Source:** Problem statement: introduction · Kickoff p. 11 · Own: [system](../architecture/specification.md#decision-priority)

**Depends on:** [REQ-0016](data-ml.md#req-0016). The order needs a learned component in the middle.

**Evidence:** Proven by the [decision priority](../architecture/specification.md#decision-priority) in the specification.

<a id="req-0049"></a>
### REQ-0049 · Country as configuration

Country rules live in configuration files. A new country needs no new code.

**Priority:** P2 · **Status:** Done · **Criterion:** Rationale · **Area:** ai

**Source:** Own: [AI](../build/areas/ai.md#technical-rules)

**Evidence:** Proven by the policy file of each country in `sentinel-ai-core/config/policy/`.

<a id="req-0056"></a>
### REQ-0056 · Explicit trade-offs

Explain the trade-offs between autonomy, accuracy, latency, cost and human oversight. Justify where the system uses AI and where deterministic logic is better.

**Priority:** P0 · **Status:** In progress · **Criterion:** Rationale · **Area:** all

**Source:** Problem statement: introduction · Kickoff p. 11

**Depends on:** [REQ-0016](data-ml.md#req-0016), [REQ-0055](analytics.md#req-0055). The measured metrics support the trade-offs.

**Evidence:** Proven by the [decisions](../build/decisions/).

Missing: the argument with the final metrics, in the presentation.
