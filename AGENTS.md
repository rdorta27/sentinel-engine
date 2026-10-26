---
language: en
style: ASD-STE100
last_reviewed: 2026-10-04
---

# AGENTS.md

Guidance for each person or AI agent who works in this repository.

## Language

The judges evaluate the hackathon in English. The whole repository is in English, working documents included.

| Where | Language | Why |
|---|---|---|
| [`team/`](team/) | English | Internal planning, ready for the submission. |
| [`docs/`](docs/) | English | The working copy that the team edits each day. |
| Root [`README.md`](README.md), slides, video script | English | The deliverable that the evaluators read. |

**Rule of thumb: write everything in English from the first draft.** There is no translation pass at the end. REQ-0051 tracks this. The status table is in [`docs/build/delivery.md`](docs/build/delivery.md#language).

### ASD-STE100

**Write all documentation in simplified technical English (ASD-STE100).** This applies to each new or edited Markdown file: README, `docs/`, `team/`, the `evidence/` READMEs, OpenSpec artifacts, decisions, commit bodies and PR descriptions. The most important rules:

- One idea per sentence. 20 words or less in a procedure step. 25 words or less in a description.
- Active voice and present tense. Write "the router labels the intent". Do not write "the intent is labelled by the router".
- One instruction per sentence, in the imperative: "Set the variable."
- One term for one concept. Do not use synonyms for variety. For example, always write "handoff". Do not also write "transfer" or "escalation" for the same event.
- Simple, common words. No idioms, no phrasal verbs with a vague meaning, no noun clusters of more than three words.
- Tables and lists, not long paragraphs.
- Keep exact technical names as they are: code identifiers, field paths, REQ ids, decision numbers and dataset values.
- Keep the headings of a page that you rewrite. Other pages link to their anchors.

**Mark each file that you write or rewrite in ASD-STE100** with this frontmatter at the top of the file, before the title. Set `last_reviewed` to the date of the last full review of the file in ASD-STE100:

```yaml
---
language: en
style: ASD-STE100
last_reviewed: 2026-10-04
---
```

A file without this frontmatter is not yet in ASD-STE100. When you rewrite it, add the frontmatter. Do not add the frontmatter to a file that you edit only in part. To list the files that are done:

```bash
grep -rl '^style: ASD-STE100' --include=*.md . | grep -v AGENTS.md
```

### Rules for agents

- Write new documentation in English and in ASD-STE100. When you edit a page, rewrite the parts that you change in ASD-STE100.
- Do **not** add Spanish files under `docs/` or `team/` unless a person asks for it.
- Do **not** write new documentation in Portuguese. The system answers in Spanish and Portuguese. Our own writing stays in English.
- Keep banking terms, acronyms and dialogue examples in Spanish or Portuguese in the original. Give an English explanation the first time. The locale vocabulary is in [`docs/glossary/`](docs/glossary/).
- Write locales as BCP 47 tags: `en-US`, `es-MX`, `es-CO`, `es-AR`, `pt-BR`. For Spanish in the three countries, use `es-419` (Latin American Spanish). Do not write `ES` or `PT` alone.

## Layout

| Path | What it holds |
|---|---|
| [`docs/architecture/`](docs/architecture/) | System Architecture, Demo Architecture, their specification, and [what is real](docs/architecture/what-is-real.md) (real, mock, synthetic, team-generated, simulation, projection) |
| [`docs/rationale/`](docs/rationale/README.md) | Why each choice, with an evidence table and the slide sentence |
| [`docs/overview.md`](docs/overview.md), [`docs/data/`](docs/data/), [`docs/glossary/`](docs/glossary/) | The challenge overview, the dataset page with the [official data dictionary](docs/data/reference/), and the glossary of the locales |
| [`docs/requirements/`](docs/requirements/) | Requirements. [`requirements.md`](docs/requirements/requirements.md) is the index (sources, status, dependencies). One file per type holds the cards with description and evidence. |
| [`docs/build/`](docs/build/) | Areas, design rules, decisions, metrics and delivery |
| [`team/`](team/) | Plan, tasks and pending decisions |
| [`evidence/`](evidence/README.md) | Frozen, reproducible runs (scripts and `summary.json`) that the docs cite. [`evidence/README.md`](evidence/README.md) indexes each run with its status and data type. |
| [`openspec/`](openspec/) | OpenSpec config, specs and changes |
| [`scripts/`](scripts/) | Repository scripts. `render_flow_measurements.py` generates the flow measurements page and can verify it against a new run. |
| [`sentinel-data-engine/`](sentinel-data-engine/) | Data pipeline (Bronze, Silver, Gold). Owner: Natalia. |
| [`sentinel-ai-core/`](sentinel-ai-core/) | Charge-inquiry loop, policy engine, the page (customer chat and advisor view) and the API under `/api/v1`. Owners are in [team/plan.md](team/plan.md#folders). |
| `.claude/`, `.opencode/` | OpenSpec commands and skills for Claude Code and OpenCode (generated) |

A new person reads the pages in the order of [`docs/README.md`](docs/README.md).

## Stack

Accepted decisions that the code must follow:

- **Backend:** Python and FastAPI. The loop is plain Python. LangGraph stays deferred. Policy, the authenticated session and idempotency stay in code. No orchestrator ever sees `customer_id`. See [005](docs/build/decisions/005-backend.md).
- **Frontend:** a one-page chat (HTML and a little JavaScript), served by the same FastAPI process. It talks to `POST /api/v1/chat`. See [006](docs/build/decisions/006-frontend.md).
- **Platform:** Azure. Locally, it runs on Linux. See [001](docs/build/decisions/001-azure-platform.md) and [019](docs/build/decisions/019-azure-container-apps.md).
- **Flow** (confirmed at the 9/29 review): a dispute starts as an account inquiry. The learned component is a prompted LLM intent router against a keyword baseline. See [flow selection](docs/build/flows/03-flow-selection.md) and [007](docs/build/decisions/007-learned-component.md).
- **Router model:** GLM 5.3 Flash on Fireworks AI, on both routes. The keyword baseline answers a turn when the model fails. See [016](docs/build/decisions/016-router-models.md).

## Rules

- **No secrets and no data in the repository.** The repository is public. Credentials are in `.env` (gitignored). Teammates share them by direct message. Never commit the hackathon datasets (`data/` is gitignored). The one exception is the official data dictionary in [`docs/data/reference/`](docs/data/reference/): schema, not rows.
- **Commit messages** follow Conventional Commits with a mandatory body of two blocks. [`.githooks/commit-msg`](.githooks/commit-msg) enforces this. Activate it once per clone: `git config core.hooksPath .githooks`.
- **Decisions:** product and technique decisions go to [`docs/build/decisions/`](docs/build/decisions/), one file each, from the template. Team decisions go to [`team/plan.md`](team/plan.md). List the requirements that a decision cites in [`docs/requirements/requirements.md`](docs/requirements/requirements.md).
- **Label what is real.** Each component, data source and number is real, mock, synthetic, team-generated, simulation or projection, as [what is real](docs/architecture/what-is-real.md) defines. Never show a simulation or a projection as a production measurement.
- **Evidence runs are write-once.**
  - A new run goes in a new folder under `evidence/` (for example `evidence/flows/2024Q4-v3/` or `evidence/adversarial/<run-id>/`). Never edit a committed run.
  - Cite `summary.json` fields. Never copy numbers by hand.
  - Add each new run to [`evidence/README.md`](evidence/README.md) with its status (current or superseded), its data type and its requirements.
  - Scripts read the bucket name from `.env` and the data from the gitignored data folders. Never write the bucket name, account ids or dataset rows in the repository.
- **The test suite makes the adversarial evidence, not a person.** From `sentinel-ai-core/`, run `SENTINEL_WRITE_EVIDENCE=1 python -m pytest tests/adversarial -q`. It writes one new run under `evidence/adversarial/<run-id>/summary.json`. The counts come from the real pytest outcomes. The denominator of `unsafe_outcome_rate` is every attack attempted. See [`sentinel-ai-core/tests/adversarial/summary.py`](sentinel-ai-core/tests/adversarial/summary.py).
- **Specs and changes** use OpenSpec (`/opsx:propose`, `/opsx:apply`, and others) with the rules in [`openspec/config.yaml`](openspec/config.yaml): English only, in ASD-STE100, and each capability traced to a `REQ-####`.
- **No `Co-Authored-By` trailers.** The commit hook refuses them. Credit people in the message body.
- **No push and no pull request without an explicit request** from the repository owner.
- **PDFs:** run `python3 estilos/build.py` from outside the repository. PDFs are gitignored.
