---
language: en
style: ASD-STE100
last_reviewed: 2026-10-05
---

# Plan: router v3 and a new held-out measurement (eval-v8)

This page is the record of the first phase. It is not the current plan. The index is in [the team record](README.md).

> **Superseded.** This plan is done. [Chat behavior](chat-behavior-plan.md) absorbed it as its first step. It stays as the record of the design.

**Status:** done on 2026-10-05. The sealed v8 measurement ran. `router_v2` stays served. Prompt v3 failed the zero-unsafe-wording gate and the subtype gate ([decision 018](../docs/build/decisions/018-evaluation-acceptance.md), Result v8).

- The change `router-v3` built the candidate (contract v3, prompt v3, draft validator and cut-offs). It is archived.
- The change `eval-v8` sealed the sets, ran the rehearsal and ran the measurement.

**Date of the plan:** 2026-10-02.

**Requirements:** REQ-0016, REQ-0017, REQ-0019, REQ-0020 and REQ-0047.

## Why

The served router_v2 showed a case that the evaluation never measured. GLM 5.3 Flash with prompt v2 classifies a greeting ("hola", "hola, me llamo Karl") as `out_of_scope`. The prompt names the four intents but does not define them. The eight v2 examples contain no greeting. The sealed set of 2024Q4-eval-v7 has no greeting-only case and no small-talk case. Its 0.98 says nothing about the most common first message of a chat.

The team already did this work on `feat/serve-router-v2`. It needs no new measurement:

- **A.** An out-of-scope turn explains and offers an advisor first ([008](../docs/build/decisions/008-account-inquiry-scope.md)). Two out-of-scope turns in a row get the offer. The third turn makes a handoff. A request for an advisor makes a handoff at once. A model mistake now costs a sentence, not a ticket.
- **D.** The system masks the names that the customer introduces ("me llamo Karl") before the model call (REQ-0047).
- **E.** The system keeps "who answered" for each thread. The turn log cannot attribute a turn to the model of another request.

Parts B and C below cover what A, D and E do not fix: the classification itself and the evidence behind it.

## C. Evaluation (written first; the order is the proof, as in 018)

1. **Inventory the gap.** List the first-message types that a chat receives and that no case covers. The starting list:
   - a greeting alone ("hola", "buenas", "oi", "olá");
   - a greeting with a name ("hola, me llamo Karl");
   - courtesy and closing ("gracias", "chau", "obrigado");
   - small talk and identity ("¿cómo estás?", "¿eres un bot?");
   - empty or meaningless text ("???", emoji, "asdf");
   - generic help ("necesito ayuda");
   - a greeting followed by a real request, which keeps its own intent;
   - out of scope without a baseline keyword (loan, address change, savings account, transfer not received, "¿cuánta plata tengo?"). 15 of 39 development `out_of_scope` cases have none.
2. **Add development cases** for each type, in the four variants (es-MX, es-CO, es-AR and pt-BR). Each case has the expected intent and the expected system outcome (clarification, offer or handoff). Use the development split only.
3. **New metrics.** Write them into an amendment to [018](../docs/build/decisions/018-evaluation-acceptance.md) before any number exists:
   - *unnecessary handoff rate*: the turns that end in a handoff although the expected outcome is not a handoff. 018 counts only missed handoffs, and the two errors have different costs;
   - *system outcome match*, next to intent accuracy, because A changes what an intent leads to;
   - accuracy for each new category, with the same confidence intervals as today.
4. **Acceptance rules.** Fix them with the amendment. v3 keeps each v7 gate (0 missed handoffs and 0 unsafe outcomes on attacks). v3 does not lose accuracy on the v7 categories beyond the interval. Set the target of the unnecessary handoff rate from the development numbers of the baseline and v2, before v3 runs on the sealed set.
5. **Write a new held-out set** with the same categories. The author has not seen v3 or its examples. The v7 review used an isolated subagent. Repeat that and record it. Seal the set with `python3 -m eval.seal`. The seal gives a new hash, different from `27ad2f1b…`. That hash stays in `eval/measured.json` untouched.
6. **Measure once** as `2024Q4-eval-v8`: the baseline, v2 and v3 on the same sealed set. Use the same seed and settings as v7 (reasoning low, 400 tokens, temperature 0). v2 enters the run so that the greeting gap shows with numbers. Freeze the run with `freeze.py`. Never edit the run.

## B. Prompt v3 (designed on development only)

1. **Define the intents** in the system prompt, one line for each:
   - `charge`: the customer names a charge, debit or movement that they want to review;
   - `missing`: the customer has not yet said what they need (greeting, introduction, thanks, "I have a problem" or "help");
   - `out_of_scope`: the customer asks for something else from the bank (balance, loan, card, address or products);
   - `person`: the customer asks for a human.
2. **Examples.** Keep the eight v2 ids. Add the minimum that covers the new categories (a greeting alone, a greeting with a name and a closing). All examples come from the development split. `eval/examples.py` builds them. It refuses held-out ids. The ids go in `eval/examples_v3.json`.
3. **Iterate on development** until the new development set passes. Nobody reads a sealed case at any point.
4. **Do not add a guard in code** on `out_of_scope`. 15 of 39 development out-of-scope cases carry no baseline keyword. A keyword guard would turn real out-of-scope requests into clarifications.
5. **Serve v3 with the same guarantee as v2.** `SENTINEL_LLM_PROMPT_VERSION=v3` loads its examples through the same loader. Startup fails if they do not load. A test pins the example ids to the ids that the eval-v8 summary records.

## Order and dependencies

| # | Step | Needs |
|---|---|---|
| 1 | Inventory and development cases (C1, C2) | Nothing |
| 2 | Amendment to 018: metrics, rules and targets (C3, C4), committed | Step 1 |
| 3 | Prompt v3 on development (B1 to B3) | Step 1. It does not depend on step 2 |
| 4 | Held-out set written and sealed (C5) | Steps 2 and 3 frozen. The author has not seen v3 |
| 5 | Measure eval-v8 once (C6) | Step 4 |
| 6 | Serve v3, docs and requirement statuses (B5) | Step 5 |

Until step 5, the served app runs v2 with A, D and E. The README limitations say so: the classifier labels a greeting alone as out of scope. The app now answers it with an offer, not a ticket.

## Confidence cut-offs handed from `router-confidence`

The `router-confidence` change gave the router a confidence for each label. It calibrated two cut-offs on the development and validation split. The run [`2024Q4-calibration-v1`](../evidence/evaluation-runs/2024Q4-calibration-v1/summary.json) froze them: `t_act` = 0.86 and `t_abstain` = 0.0.

- They live in `sentinel-ai-core/app/ai/router_config.json` with the run id.
- The served app loads them only when `SENTINEL_LLM_CUTOFFS` is on. With the setting off, the app serves v2 exactly.
- When the setting is on, a label below `t_act` that is not a `person` request becomes `missing`. The loop then asks its clarifying question first. The policy, the handoff rules and the confirm box still decide.

What eval-v8 must do with the cut-offs:

- Measure router v3 with the setting on, next to the baseline and v2. The sealed set then covers the confidence path. The `_router` helper in `eval/run.py` builds its config without cut-offs. The v3 version adds them.
- Keep `t_act` and `t_abstain` frozen with the run. A change to either needs a new calibration run before the seal, never after.
- Record two rules: the system never downgrades a `person` request, and a cut-off never overrides a policy refusal, a handoff rule or the confirm box (018 amendment). The validation split is descriptive. eval-v8 stays the clean measurement.

## Open decisions

The owner closed these decisions on 2026-10-05:

- **Schedule.** The owner moved the code freeze to Sunday 10/4 night ([plan](plan.md)). The plan landed before the submission.
- **Author of the new held-out set.** Two isolated authors write the sealed blocks. Each block has its provenance file in `sentinel-ai-core/eval/review/` (`eval-v8` design, decision 3).
- **Budget.** The development run `2024Q4-dev-v8-v2` used a cap of USD 1 and spent USD 0.025202 ([evidence index](../evidence/README.md#evaluation-runs)). The cap of the final measurement is part of the 018 amendment.
