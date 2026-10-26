---
language: en
style: ASD-STE100
last_reviewed: 2026-10-05
---

# Contributing

This page tells a person how to work in this repository. [`AGENTS.md`](AGENTS.md) holds the same rules for an AI agent, with the full layout and the language rule.

## Branches and pull requests

- Work on a feature branch. Name it `feat/<topic>`, `fix/<topic>` or `docs/<topic>`.
- Keep each pull request small. One topic per pull request.
- Open a pull request only when the owner asks for it.
- Merge `origin/main` into the branch before you deliver it.

## Commits

- Use Conventional Commits: `<type>: <summary>`.
- Use one of these types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`.
- Write the summary in lowercase, with no final period.
- Add a body with two blocks. The first block gives the reason in prose. The second block starts with the line `Changes:` and holds one or more `- ` bullets.
- Do not put a version number in a message. A tag holds the version.
- Do not add a `Co-Authored-By` trailer.

## Plans

- The repository uses OpenSpec. A change lives in `openspec/changes/<name>/`.
- Propose a change with `/opsx:propose`. Apply it with `/opsx:apply`.
- Write a plan in English, in ASD-STE100.
- Trace each capability to a `REQ-####` id.

## Evidence

- An evidence run is write-once. A new run goes in a new folder under `evidence/`.
- Cite a field of `summary.json`. Do not copy a number by hand.
- Add each new run to [`evidence/README.md`](evidence/README.md) with its status and its data type.
- Label each number as real, mock, synthetic, simulation or projection.
- Do not commit a secret, a password, a dataset row or a bucket name.
