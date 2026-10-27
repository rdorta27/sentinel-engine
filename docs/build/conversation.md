---
language: en
style: ASD-STE100
last_reviewed: 2026-10-05
---

# Conversation

This page describes how the assistant behaves with the customer, for each situation. It also describes how the assistant handles Spanish and Portuguese. It is the basis of the demo and the video.

**Purpose:** decide what the assistant says and does in each situation. **Related:** [system](../architecture/system-architecture.md), [security](security.md), [requirements](../requirements/requirements.md).

## Principles

- **AI understands. Code executes and verifies** (see [system](../architecture/system-architecture.md#central-principle)).
- **Autonomy by risk.** An action with consequences (blocking, opening a dispute) asks for confirmation (REQ-0006, autonomy rules).
- **Only verified facts.** If the data does not exist, say so and offer an alternative. Never answer with the own knowledge of the model (REQ-0003, verified records).
- **Separate what is verified from what the customer states.**
- **Report only actions that the tool confirms.** A timeout is not a success (REQ-0005, verified actions).

## When data is not up to date

REQ-0039 (declare freshness). If the customer mentions something more recent than the data, do not claim that the data shows it:

> "Mis registros están actualizados hasta hoy a las 00:00 y todavía no veo ese cobro. Puedo abrir el reclamo ahora como pendiente de verificación; se confirmará en la próxima actualización. ¿Lo abro?"
> ("My records are updated as of today at 00:00 and I still don't see that charge. I can open the dispute now as pending verification; it will be confirmed in the next update. Shall I open it?")

## When information is missing

REQ-0002 (clarify or abstain). Ask only what is essential. When possible, **show verified options**. Do not ask the customer to type data.

## When opening a dispute

REQ-0042 (minimum effort) and REQ-0043 (check the charge status).

1. Search the candidate transactions of the session customer.
2. Check the status. **Pending** may be a pre-authorization that clears on its own: offer to wait or to file the dispute. **Reversed** means that the bank already refunded it.
3. Show the candidates and let the customer choose:
   > "Veo estas compras repetidas en los últimos 7 días:
   > 1. Supermercado Éxito, 85.000 COP, 25/09, tarjeta de débito •••4521
   > 2. Rappi, 32.500 COP, 24/09, tarjeta de crédito •••7788
   > ¿Cuál quieres reclamar?"
   > ("I see these repeated purchases in the last 7 days:
   > 1. Éxito supermarket, 85,000 COP, 09/25, debit card •••4521
   > 2. Rappi, 32,500 COP, 09/24, credit card •••7788
   > Which one do you want to dispute?")
4. Two identical charges can be legitimate. Show the facts. Do not conclude that there was an error.
5. If the charge does not appear, ask for the minimum and open the dispute as **pending verification**.
6. Ask for confirmation before you open the dispute. Report the case number only when the tool confirms it.

## When the confirmation is open

A message that names another amount, merchant or date closes the box and grounds the new charge. A confirm opens only the charge of the box that the customer saw. A message that is not a correction shows the same box again.

## Status of an open dispute

REQ-0003 (verified records) and REQ-0043 (check the charge status first). A question about the status of a dispute is a code check. It runs before the model and before the confirm box. The reply reads the cases of the customer, or says that no case exists:

> "Tu caso D-… está en estado Open." ("Your case D-… has status Open.")
> "No tienes disputas abiertas." ("You have no open disputes.")

The check never opens a case. The phrases are in es-419 and pt-BR. A phrase has a case word (disputa, reclamo, caso, contestação) and a status word (ya abrí, en qué va, estado, status).

## After a handoff

REQ-0001 (keep context) and REQ-0008 (structured handoff package). The reference belongs to the case, not to the session.

- A message about the same case gets the ticket reference as the answer.
- A request about another charge continues the normal flow.
- The reason of a filed ticket does not change.

## When no charge matches a date

REQ-0002 (clarify or abstain). When a date phrase matches no charge, the reply names the date that the assistant searched. It then lists the newest charges:

> "No encontré cargos del 2026-06-16. Estos son los más recientes." ("I found no charges on 2026-06-16. These are the newest.")

## When the customer greets or makes small talk

REQ-0002 (clarify or abstain) and REQ-0012 (Spanish and Portuguese). These messages are an **opener**: a greeting, a thank you, a goodbye, an identity question or a help question. The router reads an opener as `missing` with a subtype. The reply is friendly and says what the assistant can do. An opener never hands off.

> "¡Hola! Puedo revisar un cargo que no reconozcas. Cuéntame cuál es." ("Hello! I can review a charge that you do not recognise. Tell me which one.")

A greeting that also names a charge is a **request**. It is not an opener. The assistant keeps the request.

When the model has no subtype (contract v2 or the baseline), short patterns in code find the opener. The patterns run only on a `missing` result and only on a short message.

## Status of a charge

REQ-0003 (verified records) and REQ-0043 (check the charge status). A question about the status of a charge has the label `status`. The reply gives the status, the date and the dispute eligibility of the verified charge. It **never opens a confirm box**.

> "Tu cargo en Cafe Central por 320.00 del 2026-06-12 está Approved y puedes reclamarlo." ("Your charge at Cafe Central for 320.00 on 2026-06-12 is Approved and you can dispute it.")

When the message names no charge, the assistant uses the newest verified charge.

## When the request is outside disputes

See decision [008](decisions/008-account-inquiry-scope.md). The router reads the request as `out_of_scope` with a subtype: balance, loan, card, address, transfer or other. The reply names what is not possible and what is possible. Then the assistant offers the advisor, as before.

> "No puedo tramitar préstamos. Sí puedo revisar un cargo que no reconozcas." ("I cannot process loans. I can review a charge that you do not recognise.")

## Why a named charge cannot be disputed

REQ-0029 (explain a decision). The customer asks why a named charge cannot be disputed. The assistant grounds the charge and reads the policy rule. The reply gives the rule and its verified values: the window, the charge date and the last eligible date.

> "¿Por qué no puedo reclamar el de enero?" ("Why can't I dispute the January one?")
> "Para reclamar un cargo hay un plazo de 90 días desde la fecha del cargo. Este cargo es del 2026-01-15, así que la última fecha para reclamar fue el 2026-04-15." ("To dispute a charge there is a 90-day window from the charge date. This charge is from 2026-01-15, so the last date to dispute was 2026-04-15.")

A why question that names a **safety** charge stays a new request. The assistant does not disclose a threshold, a score or the name of the rule (adversarial F6).

## Model words and templates

See decision [024](decisions/024-model-wording.md). On a turn that does not decide, the reply may show words that the model wrote, with placeholders only. Code fills each placeholder from the verified facts. The validator refuses a draft that has a figure, a name, a promise or the wrong language. A refused draft falls back to a reviewed template. The turn record names the reason for the refusal.

A turn that decides uses templates only: the confirm box, the case confirmation, the policy refusal, the handoff and the error. For the other turns, the assistant has two reviewed templates. It picks one by turn count, so a replay gives the same text.

## When the customer asks to speak to a person

REQ-0040 (advisor request). The policy in code decides. The predictor and the LLM do not decide.

- The assistant makes a single offer: "Puedo ayudarte con esto ahora mismo. ¿Prefieres intentarlo conmigo o que te comunique con un asesor?" ("I can help you with this right now. Would you prefer to try it with me or that I connect you with an advisor?")
- If the customer repeats the request or chooses the advisor, the assistant escalates at once. It does not insist.
- Log each request. Many requests at the same step show a problem in the flow.

## App context

REQ-0045 (recent app errors, only as auxiliary context). App diagnosis is not a flow in the challenge statement. Suppose the customer had a recent error, for example a failed transfer. The transfer can use SPEI (the Mexican instant-transfer system) or Pix (the Brazilian instant-payment system). Offer the error as a question: "¿Tu consulta tiene que ver con la transferencia que falló ayer?" ("Is your question about the transfer that failed yesterday?"). Never assert the error. Never surprise the customer.

## Language

REQ-0044 (neutral Spanish (es-419)) and REQ-0041 (original currency). The country of the account does not say where the customer is from. Example: a Venezuelan customer in Colombia.

- Use neutral, clear Spanish with no slang from one country.
- Explain acronyms and local terms on first use. Example: "SPEI, Mexico's instant-transfer system".
- Understand the terms of other countries and respond with what exists at their bank. Examples: "pago móvil" (the Venezuelan mobile-payment system) and "Pix" (the Brazilian instant-payment system).
- The response language follows the customer. The currency follows the account (see [languages](#language-country-and-currency-are-independent)).
- The [glossary](../glossary/) has the equivalences for each country.

## Languages

### Challenge requirements

- Interactions in Spanish and Portuguese must be **robust**. The kickoff marks this as mandatory.
- Report the limits of the data and of the language coverage.
- Exact parity is not required. The metrics must be split by language, and the team must investigate the differences.

### Main risk

**We have no Portuguese data to build with.** The dataset confirms it: all text is in Spanish, with Mexican, Colombian and Argentine variants. No Lusophone country is in the data. A bank team will likely still test in Portuguese, like a hidden test set.

### Strategy

- Prefer **multilingual** components (LLM, multilingual embeddings) to models that train only on Spanish.
- Deterministic logic does **not depend on language**. Use no Spanish-only keywords.
- Create our own pt-BR test cases. They can be translated, synthetic or drawn from external Brazilian complaint data. **Label them as such** and **hold them back**. Do not use them to tune the system. External data is allowed if the team justifies it (help channel, 9/28; REQ-0054).
- Put pt-BR in the adversarial set (injection, multilingual ambiguity).

### Language, country, and currency are independent

A customer may write in Portuguese and hold the account in MX, CO or AR.

- The **response language** follows the customer.
- The **currency** follows the account or the transaction (MXN, COP, ARS or USD). The system never converts it to match the language.
- We split the metrics by language **and** by country.

### Brazilian Portuguese

Portuguese tests most likely come from Brazil (pt-BR). The customer may use terms of the Brazilian system, even if the account is in MX, CO or AR:

- Pix, the Brazilian instant-payment system,
- extrato (statement),
- estorno (refund or chargeback),
- atendente (advisor),
- CPF (Cadastro de Pessoas Físicas, the Brazilian individual taxpayer ID).

The assistant must understand these terms. It must respond with the real data of the account. For example, the dataset has no Pix. The [glossary](../glossary/glossary.pt-br.md) has the equivalences.

### Spanish variants

The dataset has fields that detect the accent: Mexican, Colombian, Argentine and, in `customers`, neutral. We use them as segments to measure fairness within Spanish.

### Reporting

- Report the metrics by language, with n.
- If pt-BR performs worse, we explain the cause. Example: there is no pt-BR training data. We do not hide it.

### Generating and validating pt-BR cases

Nobody on the team speaks Portuguese, so the team checks the cases through Spanish. One model writes the pt-BR case. A different model back-translates it. The team compares the back-translation with the intended Spanish case. Each important es-419 case has a pt-BR twin ([017](decisions/017-portuguese.md)).
