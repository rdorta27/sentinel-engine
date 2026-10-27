---
language: en
style: ASD-STE100
last_reviewed: 2026-10-05
---

# Tasks

Paths are relative to the repository root. Merge `origin/main` first. Never push, open a pull request or create a tag.

**Mode.** Ask the owner for the three inputs of the proposal first: the tag names and the release URL, the video URL, and the confirmation that Pages deployed with the site URL. After that every task is automatic and needs no other answer.

**Priority (the submission is due on 2026-10-05, 11:59 PM COT).** The video is not a task of this change: the owner records it with his own voice, in English, on the redeployed link. If time runs out, do 1.3 (the check of the deployed site and the search for secrets) and 1.4 (the email check) first, and cut 1.1, 1.2, 2.1 and 2.2.

## 1. Links and checks

- [x] 1.1 Regenerate `site/numbers.json` with `scripts/site_numbers.py` from the final `summary.json` files. Run `python3 scripts/localize.py` and `python3 scripts/localize.py --check`. Portuguese numbers use the decimal comma. Check that the numbers test passes and that no run is missing. Evidence: the test output in the commit body.
- [x] 1.2 Add to the site, the slides and the README the release tag (`v1.0-submission`), the link to the GitHub release, the date and the link or embed of the video. Show the tag and the build line (model, prompt version, short `bundle_hash`) in the site footer. Add each new text to both dictionaries in `site/i18n/`. Export the three PDFs again with `python3 scripts/export_slides.py` if a slide changed. Evidence: the diff and the page counts.
- [x] 1.3 Search `site/`, the slides and the README for a password, key or bucket name. Open the deployed site at the URL of the owner. Check each link, the three languages and the language switch, the phone layout at 390 px and the diagrams. Evidence: a short list of the checks in `docs/build/delivery.md`.
- [x] 1.4 Check that the submission email lists the final site link, the repository, the public demo link, the slides, the video and the credentials block, in the order of the delivery checklist. Do not write a real password. Evidence: the checklist in `docs/build/delivery.md`.

## 2. Requirements and team

- [x] 2.1 Set the status of REQ-0036 and REQ-0037 where the evidence now exists (the slides, the video and the links). Evidence: `docs/requirements/`.
- [x] 2.2 Update `team/tasks.md` and `team/plan.md` with the final state of the submission. Evidence: the two files.
