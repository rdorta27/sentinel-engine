---
language: en
style: ASD-STE100
last_reviewed: 2026-10-05
---

# Requirements: Delivery

This page covers what the evaluators receive: the repository, the deployed link, the slides, the video, the limits and the path to production. The [requirements index](requirements.md) holds the sources, the classification, the status counts and the dependency chains.

| ID | Requirement | P | Area | Depends on | Status |
|---|---|---|---|---|---|
| [REQ-0013](#req-0013) | Report data and language limits | P0 | analysis | [REQ-0012](frontend-backend.md#req-0012), [REQ-0024](analytics.md#req-0024) | In progress |
| [REQ-0030](#req-0030) | Declare what is missing | P0 | all | [REQ-0013](#req-0013), [REQ-0053](analytics.md#req-0053) | In progress |
| [REQ-0034](#req-0034) | Clean public repository | P0 | all | [REQ-0031](data-ml.md#req-0031) | Done |
| [REQ-0035](#req-0035) | Deployed tool link | P0 | ai | [REQ-0027](non-functional.md#req-0027), [REQ-0034](#req-0034) | Done |
| [REQ-0036](#req-0036) | Presentation, 4 to 6 slides | P0 | all | [REQ-0055](analytics.md#req-0055), [REQ-0056](non-functional.md#req-0056) | Done |
| [REQ-0037](#req-0037) | Video pitch | P0 | all | [REQ-0009](frontend-backend.md#req-0009), [REQ-0010](frontend-backend.md#req-0010), [REQ-0011](frontend-backend.md#req-0011), [REQ-0035](#req-0035) | Done |
| [REQ-0051](#req-0051) | Everything in English | P0 | all | [REQ-0036](#req-0036), [REQ-0037](#req-0037) | In progress |
| [REQ-0052](#req-0052) | Path to production | P0 | ai, all | [REQ-0025](non-functional.md#req-0025), [REQ-0050](analytics.md#req-0050) | In progress |

<a id="req-0013"></a>
### REQ-0013 · Report data and language limits

State openly what the data cannot support. The dataset is synthetic and in Spanish only. It covers only Mexico, Colombia and Argentina. No real material tests Portuguese or other countries. The [dataset assumptions](../data/dataset.md#assumptions) list the assumptions once.

**Priority:** P0 · **Status:** In progress · **Criterion:** Rationale · **Area:** analysis

**Source:** Problem statement: Scope · Kickoff p. 15 · Dataset summary

**Depends on:** [REQ-0012](frontend-backend.md#req-0012), [REQ-0024](analytics.md#req-0024). The coverage limits come from the language support and the breakdown.

**Evidence:** Proven by:

- The [dataset assumptions](../data/dataset.md#assumptions) and the [rationale](../rationale/data-assumptions.md). The data is synthetic and in Spanish only. Accounts exist only in México, Colombia and Argentina. Mexican accounts use only USD.
- The measured limits of the data. The balance has no usable as-of date. A complaint cannot link to a charge. No customer signal adds to `fraud_score`, and its label is a generator artefact. See [`customer-360/dev-v1`](../../evidence/customer-360/dev-v1/README.md), [`dev-signals-v1`](../../evidence/customer-360/dev-signals-v1/README.md) and the [investigation data support](../rationale/investigation-data-support.md).
- Two more limits on the [problem and demand](../rationale/problem-and-demand.md) page. The product field is empty on most transactional calls. No complaint links to a call.
- The language limits. The transcripts are two Spanish templates ([`transcript-chats/20261002T144836Z`](../../evidence/transcript-chats/20261002T144836Z/summary.json)). A model wrote the Portuguese cases ([018](../build/decisions/018-evaluation-acceptance.md)).
- The labels in [what is real](../architecture/what-is-real.md). Each input has a label.
- The README section [limitations](../../README.md#limitations).

**Review of the demo lines and the transcripts:**

- grok-4.7 wrote the three demo pt-BR lines. DeepSeek V4.1 Flash back-translated them ([`eval/review/demo-pt-br.md`](../../sentinel-ai-core/eval/review/demo-pt-br.md)). No native speaker reviewed them.
- A Colombian teammate accepted the three es-CO lines on 2026-10-02. The normal line had named the peso as mexicano before that.
- The same model found no drift on es-MX and es-AR. Nobody on the team speaks those varieties.
- A 2% replay of `customer_text` used the development side of the 70/30 time split (held-out cut 2025-07-01). The result is in [`evidence/transcript-chats/20261002T144836Z/summary.json`](../../evidence/transcript-chats/20261002T144836Z/summary.json): 280 handoffs out of 280, and 2 distinct prefixes.
- The engine data directory has no transcript files. The read used the analysis working copy. The team copied no customer data into the repository.
- The local files cover the 2024Q4 window only. No held-out row was present to exclude.
- The 14,023 transcripts are two templates. They are not customer language.
- Pix hands off. `extrato` and `fatura` are not marked out of scope, because the sealed set uses them inside charge inquiries.

Missing: the limits on the slides. They include the limits that [018](../build/decisions/018-evaluation-acceptance.md) fixes. The cases are model-written and model-reviewed. No human or native speaker reviewed them. The variants are not strictly equivalent.

Added by [`evidence-hardening`](../../openspec/changes/archive/2026-10-05-evidence-hardening/tasks.md): the [negative results](../rationale/negative-results.md) page records each rejected component and the rule that decided it; the [mocks](../architecture/mocks.md) page records each mock, its limit and its production backend. Remaining: the known limitation of the attack suite (category B, task 4.3), the 20-label human check (task 3.3) and the limits on the slides.

<a id="req-0030"></a>
### REQ-0030 · Declare what is missing

Give an honest list of what the prototype lacks before real use: capacity, data, languages, deployment and remaining risks.

**Priority:** P0 · **Status:** Done · **Criterion:** Rationale · **Area:** all

**Source:** Problem statement: Scope; What your solution should demonstrate 6 · Kickoff p. 15 · Help channel (9/28)

**Depends on:** [REQ-0013](#req-0013), [REQ-0053](analytics.md#req-0053). The page gathers the data, language and capacity limits.

**Evidence:** Proven by:

- The README section [limitations](../../README.md#limitations). It covers data, languages, model, state, privacy, safety evidence and deployment.
- The [sizing](../sizing-capacity.md) (REQ-0053).
- The [what is real](../architecture/what-is-real.md) page.
- The [investigation data support](../rationale/investigation-data-support.md) page.
- The README section [roadmap](../../README.md#roadmap). It lists each item that the team did not build, with the evidence for why.
- Slide 6 of the [presentation](../../site/slides/deck.html): the limits, the mocks and the roadmap.

Missing: the same limits on the slides.

<a id="req-0034"></a>
### REQ-0034 · Clean public repository

The team delivers the repository as public, with the name `sentinel-engine`. All links go to `hackathon.admin@factored.ai`. For this reason, the repository must hold no secrets, no private records and no restricted data.

**Priority:** P0 · **Status:** Done · **Criterion:** Rationale · **Area:** all

**Source:** Kickoff p. 18

**Depends on:** [REQ-0031](data-ml.md#req-0031). The public repository holds no restricted data.

**Evidence:** Proven by:

- The current tree holds no bucket name and no account id.
- `gitleaks git --redact` over the full history reports 0 findings across the 246 commits. It finds no AWS key shapes, no private key material and no real passwords.
- The team never committed dataset rows. No commit has a `.csv`, `.parquet`, `.duckdb` or database blob, or a `data/` or `raw/` folder.
- `.gitignore` covers `data/`, `.env` and the local data formats.
- `.github/workflows/gitleaks.yml` scans the commits that each push and pull request adds. It catches a new secret when the secret enters the repository.
- [`CONTRIBUTING.md`](../../CONTRIBUTING.md) states the rule for each person: no secret, no password, no dataset row and no bucket name in a commit.

The review and its blind spot are in [security](../build/security.md#history-review-req-0034-101).

Accepted residual risk, documented: the dataset bucket name is visible in commits before `d070faa`. The bucket is private. No credentials were exposed. The team decided not to rewrite history. The name is public. Access is not.

<a id="req-0035"></a>
### REQ-0035 · Deployed tool link

Give a link to the running tool, with usage limits and spending limits. A minimal deployment is enough. Cloud is not mandatory (help channel, 9/28).

**Priority:** P0 · **Status:** Done · **Criterion:** AI Engineering · **Area:** ai

**Source:** Kickoff p. 18 · Help channel (9/28)

**Depends on:** [REQ-0027](non-functional.md#req-0027), [REQ-0034](#req-0034). A public link needs the session and a clean repository.

**Evidence:** Proven by:

- **Router version.** The live link serves router_v2. The team checked it on 2026-10-02 with `GET /api/v1/health` (`model` `accounts/fireworks/models/glm-5p3-flash`, `prompt_version` `v2`, `gold_source` `mock`).
- **Redeploy.** The team redeployed the image on 2026-10-03 from `main` (`9664d9d`, PR #52). It now carries the keys that PRs #49 and #50 added.
- **Earlier proof.** The live link (retired after the hackathon) was. The team deployed it on 10/02 from [deploy/azure](../../deploy/azure/deploy.sh) under [019](../build/decisions/019-azure-container-apps.md). Hugging Face dropped its free Docker tier, so [019](../build/decisions/019-azure-container-apps.md) supersedes [012](../build/decisions/012-public-deployment.md).
- **Remote checks on 10/02.** `GET /api/v1/health` returns `{"status":"ok","gold_source":"mock","state_backend":"sqlite","reference_date":"2026-06-17"}`. The page and the branding load. `CUST-0001` logs in and creates a dispute (201). `ADV-0001` sees the handoffs.
- **Usage and spending limits.** Hosting sits inside the Azure monthly free grant. The registry adds about USD 0.08 a day. All of it stays within the USD 200 trial credit ([cost](../build/cost.md)).
- **Hardening of 10/02.** The deploy uses one replica, because SQLite is per instance. It uses a non-root user, with state under `/tmp/sentinel`. It has a container healthcheck. The health route answers 503 when the state store fails.
- **Redeploy of 10/03.** It runs with that image and the Azure Files share mounted at `/mnt/sentinel`. A dispute and a handoff ticket opened before the restart were both still there after `az containerapp revision restart` (health 200). `CUST-0001` read its own cases again. `ADV-0001` saw the queued ticket in `/api/v1/handoffs`.
- **Redeploy of 10/05.** The final redeploy runs the frozen code. `GET /api/v1/health` returns `model` `accounts/fireworks/models/glm-5p3-flash`, `prompt_version` `v2`, `gold_source` `mock` and `bundle_hash` `2efe5962f9a50d0b4fed8e7b91c10a4c7fd212d5229d74a2e58d1024ee96dfd2`. That hash equals the hash of the sealed v8 measurement (decision 018), so the measured code is the served code. `scripts/e2e_check.py --access-check` passes nine of nine checks (the persona route answers 404, the fixture password fails, the four judge logins work). `scripts/e2e_check.py` passes the demo cases. The state is reset after the checks. The queries are in [deploy/azure/queries.kql](../../deploy/azure/queries.kql).
- **Monitoring.** The app writes one JSON line per turn to standard output. The line reaches Log Analytics. The query counts turns with no identifier. For the two hours after the restart, it answered `MX | ok | 45`:

```
ContainerAppConsoleLogs_CL
| where TimeGenerated > ago(2h)
| where Log_s has "country"
| extend rec = parse_json(Log_s)
| summarize n = count() by country = tostring(rec.country), outcome = tostring(rec.outcome)
| order by country asc
```

<a id="req-0036"></a>
### REQ-0036 · Presentation, 4 to 6 slides

Write a short slide deck that describes the tool. It is part of the mandatory submission.

**Priority:** P0 · **Status:** Done · **Criterion:** Rationale · **Area:** all

**Source:** Kickoff p. 18

**Depends on:** [REQ-0055](analytics.md#req-0055), [REQ-0056](non-functional.md#req-0056). The slides present the metrics and the trade-offs.

**Evidence:** Proven by: the six slides in [`site/slides/deck.html`](../../site/slides/deck.html), in English, `es-419` and `pt-BR`. Each number comes from `site/numbers.json` and the numbers test checks it. `python3 scripts/export_slides.py` builds the three PDFs of six pages each. See [delivery](../build/delivery.md#presentation).

<a id="req-0037"></a>
### REQ-0037 · Video pitch

Make a short, mandatory video (3 minutes at most). It shows the working solution and explains the core architecture decisions.

**Priority:** P0 · **Status:** Done · **Criterion:** Rationale · **Area:** all

**Source:** Kickoff p. 18

**Depends on:** [REQ-0009](frontend-backend.md#req-0009), [REQ-0010](frontend-backend.md#req-0010), [REQ-0011](frontend-backend.md#req-0011), [REQ-0035](#req-0035). The video shows the three demo cases on the deployed tool.

**Evidence:** Proven by: the video (retired after the hackathon). It lasts 3 minutes at most and uses the voice of the owner, in English. The script matches the final build and the shot list. See [delivery](../build/delivery.md#video-pitch).

<a id="req-0051"></a>
### REQ-0051 · Everything in English

Write the README, the slides, the video script, `docs/` and `team/` in English. The hackathon is judged in English.

**Priority:** P0 · **Status:** In progress · **Criterion:** Rationale · **Area:** all

**Source:** Own: [language](../build/delivery.md#language)

**Depends on:** [REQ-0036](#req-0036), [REQ-0037](#req-0037). The language check covers the slides and the video script.

**Evidence:** Proven by:

- Every file under `docs/` and `team/` is in English.
- `AGENTS.md` requires simplified technical English (ASD-STE100) for all documentation.
- The team rewrote the deliverable pages in it: the README, `docs/README.md`, `docs/rationale/`, `evidence/README.md` and `docs/architecture/what-is-real.md`.
- The new pages [`CHANGELOG.md`](../../CHANGELOG.md) and [`CONTRIBUTING.md`](../../CONTRIBUTING.md) are in English, in ASD-STE100.

The video is published ([REQ-0037](#req-0037)). The slides, the video script and the [pre-submission check](../build/delivery.md#language) are done.

<a id="req-0052"></a>
### REQ-0052 · Path to production

Give a credible account of how the team would deploy, scale, monitor and secure the prototype. State what changes from the prototype.

**Priority:** P0 · **Status:** In progress · **Criterion:** AI Engineering / Rationale · **Area:** ai, all

**Source:** Help channel (9/28) · Kickoff p. 15

**Depends on:** [REQ-0025](non-functional.md#req-0025), [REQ-0050](analytics.md#req-0050). The path to production includes monitoring.

**Evidence:** Proven by the [path to production](../architecture/specification.md#path-to-production). The monitoring path of the demo is one JSON line per turn on standard output (`SENTINEL_LOG_STDOUT`). Container Apps forwards it to Log Analytics. The query text and its result are under [REQ-0035](#req-0035), with the 10/03 redeploy. OpenTelemetry remains the production path.

Missing: alerts by country (REQ-0050). The handoff delivery is specified ([015](../build/decisions/015-handoff-delivery.md)).
