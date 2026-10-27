---
language: en
style: ASD-STE100
last_reviewed: 2026-10-05
---

# Plan: a chat that behaves better

This page is the record of the first phase. It is not the current plan. The index is in [the team record](README.md).

> **Superseded.** This plan is done. It stays as the record of the design. The status is in [component status](component-status.md) and in [tasks](tasks.md).

**Status:** implemented on 2026-10-05. The sealed v8 measurement ran. `router_v2` stays served. Prompt v3 failed the zero-unsafe-wording gate and the subtype gate ([decision 018](../docs/build/decisions/018-evaluation-acceptance.md), Result v8, and [delivery](../docs/build/delivery.md#release-notes)).

- The changes `router-v3` and `chat-start` (both archived) hold the code.
- The change `eval-v8` holds the sealed sets, the rehearsal and the measurement.
- Decision [024](../docs/build/decisions/024-model-wording.md) accepted step 5 (model words) with a validator.

**Date of the plan:** 2026-10-02. When we wrote the plan, no time limit applied to this work. The owner lifted the Sunday 10/4 freeze in [tasks](tasks.md) for it. The owner also decided what goes in the submission.

This plan replaces the prompt part of [router v3](router-v3-plan.md). That part is step 1 here.

**Requirements:** REQ-0001, REQ-0002, REQ-0016, REQ-0017, REQ-0044 and REQ-0047.

## What the chat does today (probe, 2026-10-02, router_v2, real model)

The probe sent sixteen synthetic first messages. Each message had one fresh session and the mock Gold:

| Message | Answer | Problem |
|---|---|---|
| "hola", "gracias", "¿eres un bot?" | "I can only help with charges…" | The chat treats small talk as out of scope |
| "no reconozco un cargo de Tienda Lumbre", "me cobraron dos veces en la cafetería ayer", "hay un cobro de 849…", "el de ayer", "oi, não reconheço… R$ 215" | The same three chips (the newest charges) | What the customer said never narrows the list |
| "quiero ver el estado de mi último cargo" | Which charge? | The chat does not understand a status question |
| "no fui yo, alguien usó mi tarjeta" | The same chips | The chat registers the claim. The answer does not change |
| "hola, tengo un problema… no sé cómo explicarlo" | The same chips | The chat gives no guidance on what to say |

There are two causes:

- The model returns one label (and an `amount` that the code ignores). The code finds the charge with regex parsers (`app/ai/grounding.py`). They need an exact merchant name. They understand dates only in some phrasings.
- The replies are translation keys. Each situation gets one fixed sentence.

## Principles that do not change

- The model understands. Code decides and verifies. Policy, eligibility, the confirm box, idempotency and the handoff stay in code.
- The model never sees `customer_id` or any other identifier. The system masks free text.
- A claim of the model about a charge counts only if it matches a verified candidate.
- Replies carry keys and verified values. They never carry model prose (the `chat` contract), unless the owner accepts step 5.
- If the model fails, the baseline answers the turn. The chat never shows an error.

## Steps

1. **A richer reading, in one call.** The model returns this data in the same call:
   - `intent`: charge, status, missing, chitchat, out_of_scope (with a subtype: balance, loan, card, address or other) or person;
   - `not_mine`;
   - slots as the customer said them: merchant words, amount, a date phrase, and whether the customer says it happened twice.

   The prompt defines each intent and each slot, with development examples (greeting, thanks, "are you a bot", status and a vague complaint). The output stays in JSON mode. Reasoning is low. The token count has a limit.
2. **Grounding with the reading.** Code does four things:
   - It turns the date phrase into a date, from the reference date.
   - It resolves the merchant words against the real candidates. The match is fuzzy and ignores accents: "cafetería" finds "Cafe Central".
   - It keeps the existing regex parsers as a cross-check.
   - It drops a slot that matches no candidate. A wrong slot of the model cannot pick a charge.

   One match goes to the confirm box. Several matches show only those matches. No match shows the list and says that nothing was found.
3. **Behavior by situation, in code:**
   - chitchat: a friendly reply by subtype (greeting, thanks, "are you a bot": yes, an assistant for charge disputes) and what the assistant can do next. Never a handoff;
   - status: answer from the verified candidate (status, date and whether the customer can dispute it). Do not open a dispute;
   - missing: ask for the one missing item (which charge, amount or date), with chips when useful;
   - out of scope by subtype: say what is not possible and what is possible. Then offer an advisor. The third turn in a row makes a handoff. A request for an advisor makes a handoff at once (already built);
   - corrections ("no, el otro", "era ayer") use the turns and the candidates that the chat already showed.
4. **Varied but fixed wording.** Each key has several reviewed variants for each language (es-419 and pt-BR). A deterministic rule picks the variant from the turn count, so the answer is reproducible. Code inserts the verified values (merchant, amount and date) from the candidate. The model never supplies them. The register follows the [conversation rules](../docs/build/conversation.md).
5. **Optional. It needs a decision: wording that the model writes**, for turns that do not decide (greeting, small talk, clarifying questions and out-of-scope explanations).
   - A schema, the language and a length limit constrain the text.
   - The text cannot contain figures, names or promises that are not in the verified facts.
   - If a validation fails, the chat uses the template of step 4.
   - The text reads more naturally. It changes the `chat` contract (keys only) and decision 007. It adds an injection surface. It needs its own measurement.
   - We recommend it only after the measurement of steps 1 to 4.
6. **Evaluation by conversation, not only by intent** (an amendment to [018](../docs/build/decisions/018-evaluation-acceptance.md) before any number):
   - The cases are short dialogues (1 to 4 turns) in es-MX, es-CO, es-AR and pt-BR. Each has a label for the right charge, the expected outcome and whether a handoff is right;
   - The metrics are: right charge found, turns to reach it, unnecessary handoff rate, missed handoffs (still 0), unsafe outcomes (still 0), clarification rate, language kept, p50 and p95 latency, and cost per turn;
   - No LLM judge. The labels come from the design of the cases, so REQ-0023 stays not applicable;
   - A new sealed held-out set. Someone who has not seen the prompt writes it. It has a new seal hash. One measurement (`2024Q4-eval-v8`) compares the baseline, router_v2 and the new reading on the same set. `eval/measured.json` keeps the v7 hash untouched.
7. **Serve it** with the same guarantee as v2. The eval loader loads the examples. Startup fails if they do not load. A test pins the example ids to the summary of the run. Then update the README limitations, the requirement statuses and the decisions (the annexes of 007 and 016).

## Order

1. Steps 1 and 6 first (the cases first).
2. Steps 2, 3 and 4.
3. Freeze the rules in 018.
4. Write and seal the held-out set.
5. Measure once.
6. Step 7.

Step 5 comes only after that, as its own change.

## Risks

- **Latency and cost:** a longer prompt and a longer output. Budget: p95 under about 5 s for each turn. Cost for each turn within 2 times the cost of v7. We measure both.
- **Wrong slots:** the grounding against verified candidates only reduces this risk.
- **Over-fitting to the probe:** the sixteen messages above are not test cases. We write the cases by category and we seal them before the model sees them.
- **pt-BR quality:** the team has no Portuguese speaker. We back-translate the wording variants, as in [017](../docs/build/decisions/017-portuguese.md).

## Open decisions

The owner closed these decisions on 2026-10-05:

- **Step 5 (model-written wording).** Accepted now, for turns that do not decide ([024](../docs/build/decisions/024-model-wording.md), option A).
- **Author of the sealed dialogues.** Isolated authors write the sealed blocks. Each block has its provenance file in `sentinel-ai-core/eval/review/` (`eval-v8` design).
- **Budget cap.** The rehearsal and the development runs of `eval-v8` use a cap. The final measurement uses the cap of the 018 amendment ([evidence index](../evidence/README.md#evaluation-runs)).
