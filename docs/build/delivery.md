---
language: en
style: ASD-STE100
last_reviewed: 2026-10-05
---

# Delivery

The submission is due on Monday 10/5, 11:59 pm (UTC-5). The video lasts 3 minutes at most. We work and deliver in **English**. The [overview](../overview.md#deliverables) has the full list of deliverables.

## Language

We write everything in **English from the first draft**, working material included. There is no translation pass at the end. The README, the presentation and the video script start in English. `docs/` and `team/` are in English. This rule is [REQ-0051](../requirements/requirements.md).

| Piece | Language | Status | Reviewed by | Frozen |
|---|---|---|---|---|
| Repo `README.md` (the delivery link) | English | Done | Rubén | Kept in English |
| GitHub repo title and description | English | Done | Rubén | Kept in English |
| Presentation (4 to 6 slides) | Born in English | Done | Rubén | Final numbers and build line on 2026-10-05 |
| Video script | Born in English | Done | Rubén | Final build on 2026-10-05. The recording is pending |
| Demos: es-419 and pt-BR cases | Spanish and Portuguese | — | — | What the system says |
| `docs/` and `team/` | English | Done | Rubén | Written in English (decision 19 closed) |
| ASD-STE100 header on each Markdown page | English | In progress | Rubén | The command in [AGENTS.md](../../AGENTS.md#asd-ste100) counts the pages |

We update the table at each review, not at the end. The statuses are Pending, In progress and Done.

## Presentation

The presentation has six slides in English. They are static HTML pages: [the deck](https://rdorta27.github.io/sentinel-engine-site/slides/deck.html) (1280×720). Open the page in a browser. The arrow keys move between slides. The `f` key opens full screen. Each number comes from [`numbers.json`](https://github.com/rdorta27/sentinel-engine-site/blob/main/site/numbers.json) with its type.

| # | Slide | Source |
|---|---|---|
| 1 | Why: the problem and its data | [problem and demand](../rationale/problem-and-demand.md), [`problem/dev-v1`](../../evidence/problem/dev-v1/summary.json) |
| 2 | What: the product and the four demo cases | [product](../product.md), [demo replay](../../sentinel-ai-core/eval/demo/replay.md) |
| 3 | How: "The AI talks. The rules decide." with the architecture drawing | [architecture](../architecture/README.md), [`architecture.json`](https://github.com/rdorta27/sentinel-engine-site/blob/main/site/diagrams/architecture.json) |
| 4 | Proof: results and 0 unsafe outcomes | [evidence index](../../evidence/README.md), [metrics](metrics.md) |
| 5 | For the bank: the case file of the advisor, the controls that a risk team can audit, the white label and the model cost per resolution | [handoff package](../architecture/specification.md), [branding](../../sentinel-ai-core/app/branding.py), [`resolution-v2`](../../evidence/evaluation-runs/2024Q4-resolution-v2/summary.json) |
| 6 | Limits and roadmap, with the mocks | [mocks](../architecture/mocks.md), [README roadmap](../../README.md#roadmap) |

Build the PDFs before the submission. Run this command in the site repository:

```bash
python3 scripts/export_slides.py
```

The command writes the three PDFs into the slides folder of the site repository. Git ignores them. Each PDF has one page for each slide. Submit the English PDF.

- The [rationale](../rationale/README.md) gives the reason for each choice, with a sentence for each slide.
- Each figure shows its denominator and its type: test suite, simulation or synthetic.
- We include the failures and the limitations. Hiding them counts against us.

## Video pitch

The video is mandatory. It lasts **3 minutes at most**. It shows the solution working and explains the architecture decisions. The video script has the full script (Why → What → How) and the shot list.

1. The problem, in one sentence and with one data point.
2. Demo of the **normal case** (es-419). Type the es-MX line from [replay](../../sentinel-ai-core/eval/demo/replay.md).
3. Demo of the **ambiguous case** (pt-BR). Use the same sheet.
4. Demo of the **human case**. Show the JSON handoff.
5. A prompt injection attempt that fails.
6. The key architecture decisions (from [decisions](decisions/)).
7. The top results and the limitations.

## Project site

The site and the slides exist in English, Spanish (Latin America, `es-419`) and Portuguese (`pt-BR`). English is the source and the submission language ([language](#language)). The other two languages are translations for readers. The site repository builds them from the English pages with `scripts/localize.py`, and holds `site/i18n/` with the dictionaries. The ASD-STE100 rule applies to the English text only.

The static site lives in its own repository, [sentinel-engine-site](https://github.com/rdorta27/sentinel-engine-site). It has plain HTML and CSS and no build step. Its workflow publishes it to GitHub Pages on each push to `main` that changes `site/`.

| Item | Detail |
|---|---|
| Numbers | `python3 scripts/site_numbers.py` writes `../site/site/numbers.json` and the number slots of each page from the frozen `summary.json` runs |
| Check | `python3 scripts/site_numbers.py --check` fails when a number differs from the evidence |
| Rebuild the copies | After a change to the English text or to `numbers.json`, run `python3 scripts/localize.py` and `python3 scripts/export_slides.py` in the site repository. Run `python3 scripts/localize.py --check` to find a stale copy |
| Link for the judges | Use `https://rdorta27.github.io/sentinel-engine-site/?lang=en`. It opens in English for each browser language. The browser keeps the choice. Without `?lang`, the first visit follows the browser language |
| Owner action | Done: Settings, Pages uses GitHub Actions, and the `pages` workflow ran green |
| Status | Published at https://rdorta27.github.io/sentinel-engine-site/ |

## Submission email

The owner sends this email with the submission. Fill in each placeholder. Do not put a password in the slides or in the video.

- **Repository:** `<repository URL>`
- **Live link:** `<link>`
- **Slides:** `<slides URL or file>`
- **Video:** (retired after the hackathon)

### Credentials

All judges use the same set. The cases share state between judges.

| Login | Role | Country | Password |
|---|---|---|---|
| `CUST-0001` | customer | MX | `<password>` |
| `CUST-0002` | customer | CO | `<password>` |
| `CUST-0003` | customer | AR | `<password>` |
| `ADV-0001` | advisor | MX | `<password>` |

- The plain passwords are in `deploy/judge-users/passwords.csv` on the machine of the owner. Git ignores the file. The users file on the link holds salted hashes only.
- Lockout rule: after 10 failed logins for one login id or one address, the login answers HTTP 429. The lock lasts 15 minutes. On HTTP 429, the entry page shows an "access is blocked" message. It does not show the wrong-credentials message.
- The public link has no one-click entry. The documented fixture passwords do not work on the link.

## Submission checklist

Each row has one owner and one proof. A row stays pending until its proof exists. The checklist covers [REQ-0034](../requirements/delivery.md#req-0034), [REQ-0035](../requirements/delivery.md#req-0035), [REQ-0036](../requirements/delivery.md#req-0036), [REQ-0037](../requirements/delivery.md#req-0037) and [REQ-0051](../requirements/delivery.md#req-0051).

| Item | Owner | Proof | Status |
|---|---|---|---|
| Repository | Rubén | The public repository and its [README](../../README.md) | Done |
| Deployed link | Rubén | The `GET /api/v1/health` response of the 2026-10-05 redeploy, with `bundle_hash` `2efe5962…` | Done |
| Project site | Rubén | The [Pages workflow](https://github.com/rdorta27/sentinel-engine-site/blob/main/.github/workflows/pages.yml). Published at https://rdorta27.github.io/sentinel-engine-site/ | Done |
| Slides PDF | Rubén | `python3 scripts/export_slides.py` in the site repository writes the three PDFs | Pending |
| Video | Rubén | The video at (retired after the hackathon), 3 minutes at most, in English with the voice of the owner. The `video` change owns this row | Done |
| Tags and release | Rubén | The `git tag` and `gh release create` commands in [release notes](#release-notes). The `video` change owns this row | Pending |
| Submission email | Rubén | The email to `hackathon.admin@factored.ai`, with the [credentials block](#credentials). The `video` change owns this row | Pending |
| Credentials block | Rubén | The [credentials](#credentials) table, with no real password | Done |
| GitHub Pages | Rubén | Published from the site repository with GitHub Actions | Done |
| Secret scan | Rubén | The `scan` job in CI | Done |
| Green tests | Rubén | `python3 -m pytest -q` from `sentinel-ai-core/` | Done |

## Freeze procedure

This procedure comes before gate G3. `post-freeze` task 1.1 reads it. The code freeze starts when the team merges all the code plans. After the last check, nobody changes the code, the prompt, the policy, the cut-offs or the templates.

Merge these items before the freeze:

- Each code plan, `bank-ui` included.
- The switch decisions: `SENTINEL_LLM_PROMPT_VERSION`, `SENTINEL_LLM_CUTOFFS` and `SENTINEL_CHARGE_RANKER`.

Run the last checks in this order:

1. `python3 scripts/e2e_check.py`
2. `python3 scripts/e2e_check.py --access-check`
3. `python3 -m pytest -q` from `sentinel-ai-core/`
4. The secret scan in CI

The rule: after the last check, nobody changes the code. A change restarts the procedure.

## Gate G3 record

The owner confirmed the freeze on 2026-10-05. This record closes `post-freeze` task 1.1.

| Item | Value |
|---|---|
| Branch | `feat/post-freeze` |
| Freeze commit | `f18be6a` |
| Measured commit (sealed run) | `8ee4575` |
| `bundle_hash` of `/health` | `2efe5962f9a50d0b4fed8e7b91c10a4c7fd212d5229d74a2e58d1024ee96dfd2` |
| Local end-to-end check | Pass, `post-freeze` task 1.2 |

The `bundle_hash` of the local `/health` equals the served hash of the sealed run `2024Q4-eval-v8` (decision 018). The measured behavior is the served behavior.

Owner inputs:

| Input | Answer |
|---|---|
| (a) Freeze confirmation | Yes, the code is frozen |
| (b) Spend allowed for live model calls | USD 1 |
| (c) OK for `az` and the redeploy, and the subscription | Yes. The owner named the subscription. This page does not repeat its id |
| (d) Judge sheet and users file | `deploy/judge-users/passwords.csv` and `deploy/judge-users/users.json` (generated, gitignored) |

This record holds no password and no account id.

## Release notes

There are two milestones. The owner runs the tag and release commands after the final redeploy. Nobody pushes from the worktree.

### v0.9-demo - 2026-10-05

The team merged and froze the demo code. The link serves `router_v2` with prompt `v2` and the labelled Gold mock.

- Sealed v8 measurement: 444 cases in the main set and 92 in the top-up set (`evidence/evaluation-runs/2024Q4-eval-v8/summary.json`, `seals.v8` and `seals.v8b`). The verdict serves `router_v2`. Prompt `v3` fails the zero-unsafe-wording gate and the subtype gate (decision 018, Result v8).
- Router against the baseline: the paired difference is above zero (`paired.router_v2_vs_baseline`).
- Attacks: 0 unsafe outcomes of 42 (`evidence/adversarial/20261005T014816Z/summary.json`, `totals.unsafe_outcome_rate`). The three mock-only attacks pass on the real model (`evidence/adversarial/20261005T204313Z/summary.json`).
- Live latency on the frozen build: `timing.per_call.p50` and `timing.per_call.p95` of `evidence/evaluation-runs/2024Q4-resolution-live-v1/summary.json` give the p50 and p95 for each call.
- `bundle_hash` of the deployed link: `2efe5962f9a50d0b4fed8e7b91c10a4c7fd212d5229d74a2e58d1024ee96dfd2`. It is the hash of the sealed v8 measurement.

### v1.0-submission - after the video

This milestone is the delivered state: the frozen code, the repository, the public link, the site, the slides PDF and the video.

The owner runs these commands on `main`, after this branch merges and the video is published:

```bash
git tag v0.9-demo
git tag v1.0-submission
git push origin v0.9-demo v1.0-submission
gh release create v0.9-demo --title "v0.9-demo" --notes-file docs/build/delivery.md
gh release create v1.0-submission --title "v1.0-submission" --notes-file docs/build/delivery.md
```

## Handover to docs-followups-2

This record closes `post-freeze` task 6.1. The `docs-followups-2` change reads it.

| Item | Value |
|---|---|
| Freeze commit | `f18be6a` |
| `bundle_hash` of the link | `2efe5962f9a50d0b4fed8e7b91c10a4c7fd212d5229d74a2e58d1024ee96dfd2` |
| Model served | `accounts/fireworks/models/glm-5p3-flash` |
| Prompt version served | `v2` |
| Gold source served | `mock` |
| Final measurement run | `evidence/evaluation-runs/2024Q4-eval-v8` |
| Live latency run | `evidence/evaluation-runs/2024Q4-resolution-live-v1` |
| Adversarial run on the real model | `evidence/adversarial/20261005T204313Z` |
| Robustness runs | `evidence/robustness/20261005T210525Z` (fault injection) and `evidence/robustness/20261005T211031Z` (load) |
| Date of the final redeploy | 2026-10-05 |

## Pending

- [x] Maximum video length: 3 minutes (confirmed 9/28)
- [ ] Recording tool
