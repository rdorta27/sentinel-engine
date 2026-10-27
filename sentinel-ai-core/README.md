# Sentinel AI Core

This package is the only submission server.

## Run

From this directory, with Python 3.12:

```
python3 -m uvicorn app.main:app --port 8000
```

The reference date is not the wall clock. The dataset ends on 2026-06-17, so
the real clock would put every charge outside the filing window. The process
reads `SENTINEL_REFERENCE_DATE` once at startup. Default: `2026-06-17`.

```
SENTINEL_REFERENCE_DATE=2026-06-17 python3 -m uvicorn app.main:app --port 8000
```

## Demo credentials (local runs, false)

These credentials are for local runs and tests. The public link uses the
credentials of the submission email. No password is in the repository.

| Login | Password | Country |
|---|---|---|
| `CUST-0001` | `Testpass-001` | MX |
| `CUST-0002` | `Testpass-001` | CO |
| `CUST-0003` | `Testpass-001` | AR |
| `ADV-0001` | `Advisor-001` | advisor (only with `SENTINEL_DEMO_AUTH=1`) |

Login is `POST /api/v1/auth/login` with `login` and `password`, always; there is
no login by customer number alone. Do not send `customer_id` in the body.
Customers land on the chat; the advisor lands on the escalated tickets
(`GET /api/v1/handoffs`, role `advisor` only).

The fixture users exist only in the labelled mock. A local run reads the real
Gold file when it exists, so these logins have no charges. Set
`SENTINEL_GOLD_SOURCE=mock` for the demo.

## Demo entry (demo users only)

With `SENTINEL_DEMO_AUTH=1` the login page offers four one-click personas
(normal in es-MX, ambiguous in pt-BR on the Mexican account, high amount in
es-CO, "not me" in es-AR) under a banner stating the data is simulated:
`POST /api/v1/auth/demo/{persona}`. Without the flag the route answers 404 and
the user-and-password form is the only entry. The public link sets
`SENTINEL_DEMO_PERSONAS=0`, so the one-click entry answers 404 and a demo user
uses the credentials of the submission email.

Limitation: a persona id alone proves nothing about identity. One-click
sign-in is a demo shortcut for demo users, never an authentication method;
keep the flag off outside the demo.

## Screens

Four screens: the demo entry, the chat with the "Cómo lo resolví" panel, the
advisor ticket list and the advisor detail (package and turn trace). They are
captured in es-MX and pt-BR at desktop and phone width under
[`docs/build/screenshots/ui-product/`](../docs/build/screenshots/ui-product/),
regenerated from the repository root with
`python3 scripts/capture_ui_product.py` (headless Chromium, demo mode).

## API

One app, one API under `/api/v1`: `auth/{login,logout,me}`, `transactions`,
`chat`, `disputes` (`POST preview`, `POST`, `GET`, `GET {case_id}`),
`handoffs` (advisor), `health`. The chat page is at `/ui/`. Replies are the typed models in
`app/schemas/chat.py`.

Gold is read through `GoldTransactions`. The DuckDB file is
`SENTINEL_GOLD_DUCKDB` when set, otherwise
`sentinel-data-engine/data/gold_bank.duckdb` resolved from the repository, never
from the folder the process was started from. A Delta view under
`SENTINEL_GOLD_DIR` is the next probe. The labelled mock is used when neither is
readable, and whenever `SENTINEL_GOLD_SOURCE` is `mock` (no file is opened).
`GET /api/v1/health` reports which one is active. Rows dated after the reference
date are excluded in the query. Real Gold needs logins mapped to real customer
ids: `scripts/write_real_gold_users.py` writes that file under the gitignored
`data/` and prints counts only; point `SENTINEL_USERS_PATH` at it.

Sessions, conversation state and cases live in SQLite at `SENTINEL_DB_PATH`
(default `var/sentinel.db`, gitignored), so a restart keeps them; set
`SENTINEL_STATE_BACKEND=memory` for a throwaway run. Conversation state is
deleted on logout and on expiry. Login-attempt counters are per process.
The database file is created owner-only (`0600`, and `0700` for a folder the app
creates), like the turn log and the generated dev salt. A conversation keeps its
last 50 turns and files one handoff ticket: later handoff replies point at it.
`GET /api/v1/health` runs a query against the store and answers 503 when it
fails.

## Model seam

The loop talks to `ModelPort.understand`. `create_app(model=...)` stores the
chosen model on `app.state.model` and defaults to the keyword baseline
(`DemoModel`), so the same loop runs with either implementation and no code
edit is needed to switch.

The `SENTINEL_LLM_*` variables (see the repo `.env.example`, names only, no
values) configure the prompted router for the evaluation's recording runs.
The served app does not read them yet: `create_app` still defaults to the
baseline, so leaving `SENTINEL_LLM_BASE_URL` empty changes nothing. The router picks a model per route (cheap frequent turns
vs. strong ambiguous or pt-BR turns) with a configured default fallback, and
reports `model`, `route`, `prompt_version`, tokens and cost on every
`understand` record. Tests replay committed fixtures under
`app/ai/fixtures/` and open no network connection.

## Recording live router replies

Live calls happen only on the owner's machine, once per recording, and the
key never enters the repository (decision
[016](../docs/build/decisions/016-router-models.md)). Everything else replays
the recordings offline.

1. From the repo root, create the env file and make it readable only by you:
   `cp .env.example .env && chmod 600 .env`. Edit it with an editor, not with
   `echo`, so the key stays out of the shell history. Set
   `SENTINEL_LLM_BASE_URL=https://api.fireworks.ai/inference/v1`, the key, and
   the model ids from 016.
2. Check that git ignores it: `git check-ignore -v .env` prints the
   `.gitignore` rule, and `git status --short` does not list `.env`.
3. Set a spending limit of USD 1 on the Fireworks account. The runner's own
   cap is a second guard, not the first.
4. Load the variables into the current shell only: `set -a; source .env; set +a`.
5. Recordings land in `app/ai/fixtures/` as `rec-<key>.json`, keyed by model,
   prompt version, input and repetition. The recorder refuses to write a reply
   that contains the key, an authorization header or a bearer token.
6. Before every commit that adds recordings, check what is staged:
   `git diff --cached | grep -iE "fw_|authorization|bearer"` must print
   nothing. If a key ever reaches a commit, revoke it on Fireworks: removing
   it from the file leaves it in the history.
