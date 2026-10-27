# roles Specification

## Purpose

Restricts every endpoint to the role stored in the server-side session and gives advisors and admins exactly the data their job needs, nothing more.

## Requirements

### Requirement: Documented mock users per role

The repository SHALL document one false, test-only credential per active role (customers and the demo advisor) and SHALL state that the advisor needs `SENTINEL_DEMO_AUTH=1`. Traces to REQ-0028 (P0, Done).

#### Scenario: Each role can sign in from docs alone

- **WHEN** a reader follows the documented credential for a role, with the flag for the advisor
- **THEN** the session carries that role and lands on the matching view

### Requirement: Customer and advisor roles enforced in code

The system SHALL store one role per session (`customer`, `advisor`) and SHALL check it on every role-restricted endpoint: chat, transactions and disputes require `customer`; `/api/v1/handoffs` requires `advisor`. A role failure SHALL return 403 and record `access_denied`. Traces to REQ-0007 (P0, Done) and REQ-0027 (P0, Done).

#### Scenario: Customer cannot reach advisor endpoints

- **WHEN** a customer session calls `/api/v1/handoffs`
- **THEN** the system returns 403 and records `access_denied`

#### Scenario: Advisor cannot use customer endpoints

- **WHEN** an advisor session calls chat, transactions or disputes
- **THEN** the system returns 403

#### Scenario: No role means no access

- **WHEN** a request has a valid session without a usable role
- **THEN** the system returns 403 for any role-restricted endpoint

### Requirement: Read-only advisor ticket view

The advisor SHALL read escalated tickets at `GET /api/v1/handoffs` (newest first) and `GET /api/v1/handoffs/{id}`: reason key, summary, per-turn conversation, verified facts, actions attempted, evidence, open questions, and the customer id and country. The advisor SHALL NOT see names, the customer profile or the raw transcript. The view is read-only: no claim or state change. A dispute case id SHALL NOT be readable as a ticket. Traces to REQ-0008 (P0, Done), REQ-0011 (P0, Done), and REQ-0046 (P2, Pending).

#### Scenario: Handoff appears in the ticket list

- **WHEN** a chat escalates to `handoff`
- **THEN** the advisor list shows that ticket with a package equal to the one the chat produced

#### Scenario: A dispute is not a ticket

- **WHEN** the advisor requests the id of an opened dispute
- **THEN** the system returns 404
