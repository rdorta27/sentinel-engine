---
language: en
style: ASD-STE100
last_reviewed: 2026-10-05
---

# Design

## Decisions

| Topic | Choice | Reason |
|---|---|---|
| Own change | Yes | The work needs the tags and the video, which exist only after the owner acts |
| Inputs | Three, given at the start | The session then runs with no question |
| Three languages | Add each new text to both dictionaries | A text with no translation stops the build of `scripts/localize.py` |
| Requirement status | Change only where the evidence exists | REQ-0037 needs the video |
| Order | Numbers, links, public site, email, requirements | Each step reads the output of the step before |

## Risks

| Risk | Control |
|---|---|
| The owner has not pushed yet | Stop and say so. Do not check the public site |
| A link to the video is missing | Leave a clear marker and tell the owner |
| A password in the pitch | The search of task 1.3 covers the site, the slides and the README |
