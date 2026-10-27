# chat-ui Specification

## Purpose

Shows each role an interface where verified outcomes look verified, so the customer trusts the receipt instead of calling to confirm it.

## Requirements

### Requirement: Role-based landing

After login the interface SHALL route each role to its view: the chat for customers and the read-only ticket view for the advisor. There is no admin view. The chat SHALL render a `handoff` reply as a card with the translated reason and the estimated date. Traces to REQ-0038 (P0, Done) and REQ-0008 (P0, Done).

#### Scenario: Login lands on the role view

- **WHEN** a customer or the demo advisor signs in
- **THEN** the browser shows the chat or the ticket view respectively

### Requirement: Receipt card with timeline

A `case_confirmation` SHALL render as a receipt card whose first line states the outcome in plain language, followed by a large case number, then what happens next, and finally the detail. Amounts SHALL show the transaction's own currency with its code visible, dates SHALL follow one shared locale-aware format, and the card SHALL state that no funds were held or moved. The card SHALL show the reference date. The card SHALL NOT require a receipt download. Traces to REQ-0003 (P0, Done), REQ-0041 (P0, Done), and REQ-0004 (P0, Done).

#### Scenario: Confirmation is visually distinct

- **WHEN** a verified confirmation arrives
- **THEN** the card shows the verified check, the case number, what happens next, the detail, and the reference date

#### Scenario: One formatter for amounts and dates

- **WHEN** amounts and dates appear on the chips, the transaction panel, and the card
- **THEN** all three use the same locale-aware formatters and the currency code is always visible

#### Scenario: Customer data is never translated

- **WHEN** a merchant name or an amount is rendered
- **THEN** it is shown as stored, because customer data does not pass through the translation files

### Requirement: Always-visible agent button

The customer chat SHALL keep a "talk to an agent" control visible at all times. The first activation SHALL offer help and SHALL NOT hand off. A later activation on the same session SHALL take the handoff path. Traces to REQ-0040 (P0, Done).

#### Scenario: Agent button escalates

- **WHEN** the customer activates the agent control again on the same session
- **THEN** the chat returns the handoff path

#### Scenario: First agent press offers help

- **WHEN** the customer activates the agent control for the first time
- **THEN** the chat offers help and does not return `handoff`

### Requirement: Masked sensitive data

The interface SHALL mask sensitive values (for example card numbers as `****1234`) and SHALL never render full identifiers. Traces to REQ-0047 (P0, Done).

#### Scenario: No full identifier on screen

- **WHEN** any view renders account or card data
- **THEN** every sensitive value appears masked

### Requirement: Session and denial handling

An expired session SHALL show a re-login notice and return to login; a 403 SHALL show a denied-access message without technical detail. Traces to REQ-0021 (P0, Done).

#### Scenario: Expired session guides back to login

- **WHEN** an action returns 401 for expiry
- **THEN** the interface shows the re-login notice and routes to login

### Requirement: Themes without session leakage

The interface SHALL support light and dark themes through the brand variables only, defaulting to the OS preference with a toggle, and SHALL persist only the theme choice in browser storage, never session data. Theme selection SHALL be expressed as `data-theme` on the document element. Traces to REQ-0038 (P0, Done).

#### Scenario: Theme persists, session does not

- **WHEN** the customer toggles the theme and reloads
- **THEN** the theme persists while no session token exists in browser storage

#### Scenario: Colors come from the brand sheet

- **WHEN** any screen renders in either theme
- **THEN** every color resolves to a brand variable, with no literal color in the application's own sheet

### Requirement: Locales with fallback

The interface SHALL offer `es-419` as the Spanish base with `es-MX`, `es-CO`, and `es-AR` overriding only changed strings, plus `pt-BR`, from separate translation files with a language selector, starting in the language that matches the customer's country. A missing regional string SHALL fall back to `es-419`. Traces to REQ-0012 (P0, Done) and REQ-0044 (P1, Pending).

#### Scenario: Regional fallback works

- **WHEN** `es-AR` lacks a string that `es-419` defines
- **THEN** the interface shows the `es-419` text

#### Scenario: Portuguese is selectable

- **WHEN** the customer selects `pt-BR`
- **THEN** the interface renders the `pt-BR` strings, labeled as team-generated where customer-facing content applies

#### Scenario: Default language follows the customer's country

- **WHEN** the demo customer signs in
- **THEN** the interface starts in that customer's country locale and remains switchable

### Requirement: Customer-facing functional additions

The interface SHALL add a transactions panel where tapping a charge selects exactly that charge, candidate quick-reply chips for clarifications, typing and loading states, a visible reference-date line, and a confirm box before any dispute write. A tap or a chip SHALL NOT open a dispute. Traces to REQ-0038 (P0, Done) and REQ-0042 (P1, Done).

#### Scenario: Tapping a charge removes ambiguity

- **WHEN** the customer taps one of the listed charges
- **THEN** the interface selects exactly that transaction and does not open a dispute

#### Scenario: Chip resolves the ambiguity

- **WHEN** the customer taps a candidate chip
- **THEN** the interface continues the conversation with that explicit choice and does not open a dispute

#### Scenario: Ineligible candidate is not selectable

- **WHEN** a candidate is outside the dispute window
- **THEN** its control is disabled and says why, so the customer cannot select it

#### Scenario: Waiting state is visible

- **WHEN** a request is in flight
- **THEN** the interface shows a typing or loading indicator until the reply arrives

#### Scenario: Reference date is on screen

- **WHEN** the interface loads
- **THEN** it shows the reference date the system used for eligibility

#### Scenario: Confirm box uses the brand class

- **WHEN** policy allows a dispute
- **THEN** the interface shows the confirm box and the button sends the candidate id as a structured field

### Requirement: No internal identifiers on screen

The interface SHALL never display an internal transaction identifier to the customer. Selecting a transaction SHALL send the identifier as a structured request field, and the conversation SHALL show a human-readable description instead. Traces to REQ-0047 (P0, Done).

#### Scenario: Selection is described, not coded

- **WHEN** the customer selects a transaction
- **THEN** the thread shows the merchant, amount, and date, and the identifier travels only in the request body

### Requirement: Complete localization of visible text

Every visible string SHALL come from the translation files for `es-419`, `es-MX`, `es-CO`, `es-AR`, and `pt-BR`; no raw keys and no untranslated English SHALL reach the screen, and server replies SHALL carry translation keys rather than authored prose. Traces to REQ-0012 (P0, Done), REQ-0044 (P1, Pending), and REQ-0051 (P0, In progress).

#### Scenario: Missing card string fails the build

- **WHEN** any receipt, handoff, or shell string is absent from a locale file
- **THEN** a test fails naming the locale and the key

#### Scenario: No raw key on screen

- **WHEN** any view renders
- **THEN** no key name such as `hold`, `rule`, or `ref` appears as visible text

### Requirement: XSS-safe rendering

The interface SHALL insert all server and customer text via safe text methods, never as executable markup. Traces to REQ-0021 (P0, Done).

#### Scenario: Markup in text is inert

- **WHEN** any rendered text contains markup characters
- **THEN** the browser displays them literally without executing them

### Requirement: Brand sheets as the only color and type source

The interface SHALL load the team's brand stylesheets and SHALL take every color, font family, and font size from the variables they define. The application SHALL ship at most one local sheet, and it SHALL be limited to layout and positioning. Traces to REQ-0038 (P0, Done) and REQ-0051 (P0, In progress).

#### Scenario: Brand stylesheets are served

- **WHEN** the interface loads
- **THEN** the brand base sheet and the brand chat sheet are requested and return 200

#### Scenario: Local sheet stays layout-only

- **WHEN** the application's own sheet is inspected
- **THEN** it declares no color literal and no font family

#### Scenario: Brand folder is never modified

- **WHEN** the change is reviewed
- **THEN** `branding/` shows no modification and the app reads it as-is

### Requirement: Contrast-safe text tokens

The interface SHALL use AA-passing tokens for body text and SHALL NOT use the muted token for small text on light surfaces. Information SHALL never be carried by color alone. Traces to REQ-0038 (P0, Done).

#### Scenario: Small text uses an AA token

- **WHEN** a label, value, or hint is rendered at body or smaller size
- **THEN** its color is a text token that meets AA against its background

#### Scenario: Status is stated in words

- **WHEN** a status such as verified or escalated is shown
- **THEN** it is accompanied by text, and a color change alone never conveys it

### Requirement: Brand-class receipt and queue surfaces

The verified receipt, the advisor queue cards, and the admin tables SHALL be composed from the classes the brand sheet provides, using the brand's table and callout variables, so all surfaces follow the active theme. Traces to REQ-0041 (P0, Done) and REQ-0003 (P0, Done).

#### Scenario: Receipt follows the theme

- **WHEN** the theme switches
- **THEN** the receipt, queue cards, and tables change with it, because they use brand variables rather than fixed values

#### Scenario: Layout adapts without restyling

- **WHEN** the viewport crosses the desktop breakpoint
- **THEN** the transactions panel moves between the second column and the strip above the thread, and only positioning changes

### Requirement: One-click demo personas behind the demo flag

When `SENTINEL_DEMO_AUTH=1`, the entry SHALL offer demo personas that sign in with one click as fixture users: a normal case in es-MX, an ambiguous case in pt-BR on the Mexican account, a high-amount case in es-CO and a "not me" case in es-AR. A banner SHALL state that data is simulated and that the test access needs no password. Without the flag, the personas and the one-click route SHALL NOT exist and the user-and-password form SHALL be the only entry. The personas SHALL NOT show customer identifiers. Traces to REQ-0010 (P0, Done), REQ-0011 (P0, Done), REQ-0012 (P0, Done) and REQ-0027 (P0, Done).

#### Scenario: Personas only in demo mode

- **WHEN** the app starts without `SENTINEL_DEMO_AUTH=1`
- **THEN** the one-click route answers 404 and no persona is shown

#### Scenario: A persona opens its case

- **WHEN** the demo user chooses the high-amount persona
- **THEN** a session for the Colombian fixture customer starts in es-CO under the demo banner

### Requirement: The customer sees how each turn was resolved in plain language

Each chat reply SHALL carry the ordered steps of its turn as translation keys from a closed list (understood the request, looked up the charges, checked the policy, opened and verified a case, did not open a case, handed off to an advisor, refused), and the interface SHALL render them as a "Cómo lo resolví" panel. No step SHALL contain a model name, tool name, rule id, score, threshold or identifier. Traces to REQ-0029 (P1, Done), REQ-0006 (P0, Done) and REQ-0047 (P0, Done).

#### Scenario: A handoff turn is explained without internals

- **WHEN** a high-amount charge is handed off
- **THEN** the panel shows understood, looked up, checked the policy, did not open a case and handed off, and the reply contains no rule id, model or threshold

#### Scenario: No status hints at fraud before the customer acts

- **WHEN** the transaction panel lists a charge whose fraud score is above the threshold
- **THEN** its status label shows the transaction status only

### Requirement: The advisor sees the turn trace

The advisor's ticket detail SHALL show the handoff package and the trace of the turn that filed the ticket: each step with its outcome and latency, the model and prompt version, the cost and the policy version. The trace SHALL be served only to the advisor role and SHALL contain no customer text or identifier. Traces to REQ-0025 (P1, Done), REQ-0008 (P0, Done) and REQ-0007 (P0, Done).

#### Scenario: A customer cannot read a trace

- **WHEN** a customer session requests a ticket trace
- **THEN** the request is refused

#### Scenario: The advisor sees the steps

- **WHEN** the advisor opens a ticket
- **THEN** the detail lists the steps of the escalating turn with outcome and latency

### Requirement: The interface carries the product identity

The interface SHALL show the Sentinel product mark and the line stating its purpose, load fonts and assets only from `branding/`, use the bank accent color for actions and the user's messages, use a success color distinct from the accent for verified states, and keep a text label on every status color. The Sentinel violet and rose SHALL appear only in the product mark. Traces to REQ-0038 (P0, Done).

#### Scenario: No external font request

- **WHEN** the page loads
- **THEN** no font or asset is requested from outside the app

#### Scenario: Bank accent, Sentinel mark

- **WHEN** the page shows a button and the product mark
- **THEN** the button uses the bank accent and the mark keeps the Sentinel colors

### Requirement: Each recent charge shows its case state

The recent-charges panel SHALL show a state for each charge from the server: eligible, in review, with an advisor, already disputed, outside the window, or not disputable. The page SHALL NOT compute the state. Traces to REQ-0038 (P0, Done) and REQ-0043 (P1, Done).

#### Scenario: Charge with an open dispute

- **WHEN** a charge has an open dispute
- **THEN** the panel shows it as already disputed

### Requirement: The page shows a bank shell without balances

The header SHALL show the configured bank name, the product type and last four digits of the session product, the country, the language and the as-of date. It SHALL NOT show a balance. Traces to REQ-0038 (P0, Done) and REQ-0039 (P0, Done).

#### Scenario: Header of a customer session

- **WHEN** a customer logs in
- **THEN** the header shows the masked product and the as-of date, and no balance

### Requirement: The brand is configuration

`SENTINEL_BRAND_NAME` and `SENTINEL_BRAND_ACCENT` SHALL set the bank name and the accent color. An accent that fails the contrast check SHALL fall back to the default. Traces to REQ-0049 (P2, Done).

#### Scenario: Another bank

- **WHEN** the service starts with another name and a valid accent
- **THEN** the page shows that name and color

### Requirement: The thread works on a phone

At 390 px wide, the thread SHALL fill the screen, the side panels SHALL open from a button, and every control SHALL be at least 44 px high. Traces to REQ-0038 (P0, Done).

#### Scenario: Phone width

- **WHEN** the page is 390 px wide
- **THEN** no horizontal scroll appears and the side panels open from a button
