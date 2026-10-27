---
language: en
style: ASD-STE100
last_reviewed: 2026-10-27
---

# Changelog

All notable changes to this repository are in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
The project marks each milestone with a tag. `1.0.0` is the delivered state and `1.0.1` is the archived record. The headings `v0.9-demo` and `v1.0-submission` below are the planned milestone names; the tag `1.0.0` replaced them.

## Unreleased

### 2026-10-27

- Publish the project site from its own repository, `rdorta27/sentinel-engine-site`, at https://rdorta27.github.io/sentinel-engine-site/.
- Write `numbers.json` to `../site/site/numbers.json` by default and accept `--out` for a CI clone of the site repository.
- Remove the old copy under `site/` and its workflow.

## 1.0.1 - 2026-10-26

The hackathon is over. This release is the archived record of the hackathon repository `factored-hackathon-2026-sentinel-engine`. Development continues here.

- Pause the live demo on Azure Container Apps: ingress off and no minimum replica. The public link is retired.
- Make the video private on YouTube and remove its links from the README, the site, the slides, `docs/` and `team/`.
- Delete the `video/` directory with the script and the mock pages, and the two scripts that read it.
- Add an archived notice to the README and a retired banner to the Azure deploy guide.
- Regenerate the Spanish and Portuguese pages from the English source, so the site checks pass.
- Verify the archive: the three test suites pass and gitleaks finds no leak in the history.
- Development continues in `sentinel-engine`.

## v0.9-demo - 2026-10-05

All the demo code is merged. The submission is due on 2026-10-05, 11:59 PM COT.

### 2026-10-05

- #80 Write the changelog, the contribution guide and the release notes.
- #79 Measure the sealed v8 set once and decide the served prompt.
- #78 Complete the `ui-behavior` specification and add the browser test.
- #77 Cover the page behavior fixes and close the `ui-behavior` change.
- #76 Repair the chat page behavior and the advisor view.
- #75 Guard the deploy salt, replay the frozen runs and add the end-to-end check.
- #74 Add the demo-and-production section and the charge resolution steps.
- #73 Adjust the pitch to the final message of the organizers.
- #72 Add the project site, the pitch slides and the product statement.
- #71 Give the judges their own credentials for the public link.
- #70 Make the demo explain itself and guide the judge.
- #69 Harden the evidence and publish the negative results.
- #68 Clean up the repository and write the pages in ASD-STE100.
- #67 Seal the v8 set, add the metrics and rehearse every candidate.
- #66 Add the robustness safeguards, fault handling and load test.

### 2026-10-04

- #65 Add the learned charge selector and its measurement.
- #64 Train and freeze the trained baseline for the router comparison.
- #63 Measure the problem and the demand behind the chosen workflow.
- #62 Add the chat start behavior, slot grounding and validated words.
- #61 Add the bank interface, charge states and the white label.
- #60 Repair the flow defects from the manual test of Felix.
- #59 Route with the v3 contract, prompt and drafts.
- #58 Measure customer transaction signals and write the docs in ASD-STE100.
- #57 Add the product interface and the advisor trace (REQ-0029, REQ-0038).
- #56 Add a confidence score and cut-offs to the router (REQ-0002, REQ-0016, REQ-0017).
- #55 Run the final evaluation with breakdown, monitoring and ROI (REQ-0024, REQ-0050, REQ-0055, REQ-0057).

### 2026-10-03

- #54 Generate the full quality report and verify it (REQ-0015).
- #53 Add the runtime-and-ci evidence and archive the change.
- #52 Add the durable runtime and the test workflow.

### 2026-10-02

- #51 Align the status pages with the merged implementation.
- #50 Read the real Gold file explicitly and make it usable (REQ-0009, REQ-0015).
- #49 Harden the chat loop and refuse prompt extraction (REQ-0002, REQ-0021, REQ-0026).
- #48 Measure the safe resolution on a multi-turn set (REQ-0055, REQ-0057).
- #47 Show the receipt charge line in the bank's voice.
- #46 Send the selected language with every chat message.
- #45 Add demo prompt chips built from the customer's own charges.
- #44 Restore the missing Silver columns for the ROI metrics and late arrivals.
- #43 Implement the multi-path DuckDB resolution for the Gold service.
- #42 Answer the why follow-ups and document the policy sources and the metrics report.
