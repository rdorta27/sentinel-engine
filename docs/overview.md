---
language: en
style: ASD-STE100
last_reviewed: 2026-10-05
---

# The Challenge

**Purpose:** understand the hackathon without a read of the PDFs.

**Related:** [system](architecture/system-architecture.md), [dataset](data/dataset.md), [requirements](requirements/requirements.md) and [glossary](glossary/).

> "Build something that works, prove that it works, and know when it should not act. And show us what it would take to make it real."

## Objective

The team builds a **customer-support assistant for a bank** that operates in Mexico, Colombia and Argentina. It is a **system**, not a chatbot. The system does five things:

- It understands the customer.
- It queries verified data.
- It executes safe actions.
- It verifies that the actions happened.
- It hands the case to a person when necessary.

Rules from the brief:

- **A single flow.** The options are account or payment inquiries, cards, transaction disputes, or credit information and eligibility. More flows do not score points on their own. Depth and engineering judgment count. Our flow is transaction disputes ([decision 003](build/decisions/003-disputes-flow.md)).
- The system works in **Spanish and Portuguese**. The data is in Spanish only.
- **End-to-end first.** Then we optimize.

## Demo cases

| Case | What the assistant does |
|---|---|
| Normal | It resolves the case alone and follows the bank policies |
| Ambiguous or unsupported | It asks for what is missing, or it says that it cannot help |
| Requires a person | It makes a handoff with a structured summary for the advisor |

## Golden rules

This list is a summary. The [system](architecture/system-architecture.md) and [conversation](build/conversation.md) pages give the detail.

1. **AI understands. Code executes and verifies.** Permissions are in code, not in the prompt.
2. **Only verified facts.** If the data is missing or not current, the system says so.
3. **Autonomy depends on risk.** An action with consequences needs a confirmation.
4. **Honesty.** We report the failures, the limitations and what production still needs.

## Evaluation

| Criterion | What the judges look at |
|---|---|
| Rationale and documentation | Why we chose the flow, written decisions and limitations |
| AI Engineering | Backend, frontend and deployment |
| Data Analytics | Data quality and insights |
| Data Engineering | The extraction and transformation pipeline |
| Machine Learning | Selection, evaluation against a baseline and model tracking |

The main metrics are **safe automated resolution**, **unsafe outcomes** and **cost**. The [metrics](build/metrics.md) page has the detail.

## Deliverables

The deadline is **Monday 10/5, 11:59 pm (UTC-5)**. The organizers confirmed it on 9/28.

The challenge is a sprint of 10 days. It starts on 9/25. The submissions close on 10/5.

We send these items to hackathon.admin@factored.ai:

1. The public repository `sentinel-engine`
2. The link to the deployed tool
3. A presentation of 4 to 6 slides
4. A video of **3 minutes at most**: the demo and the architecture decisions

The rule is "Submit your tool no matter what". We deliver on time and we declare the limitations.

## Known risks

- **Portuguese without data.** The evaluators will most likely test in Brazilian Portuguese. See [languages](build/conversation.md#languages).
- **Data with intentional issues:** duplicates, nulls, late arrivals and a changing schema. See [dataset](data/dataset.md).
- **Nobody on the team comes from contact centers.** The [glossary](glossary/) explains the business acronyms.

## Official material

*Problem statement* · *Kickoff* · *Dataset summary* · *Data dictionary*
