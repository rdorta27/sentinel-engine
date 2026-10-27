## ADDED Requirements

### Requirement: The site, the slides and the README link to the release and the video

The site, the slides and the README SHALL show the release tag, the link to the GitHub release, the date and the link to the video. The site footer SHALL show the tag and the build line. Each new text SHALL exist in the three languages. Traces to REQ-0036 (P0, Pending), REQ-0037 (P0, Pending) and REQ-0051 (P0, In progress).

#### Scenario: A link is missing

- **WHEN** an input is missing
- **THEN** the session stops and tells the owner which input it needs

### Requirement: The public site matches the release

The public site SHALL show the numbers of the final `summary.json` files in the three languages. It SHALL hold no password, key, bucket name or dataset row. Traces to REQ-0034 (P0, Done) and REQ-0027 (P0, Done).

#### Scenario: Check

- **WHEN** the checks of task 1.3 run on the deployed site
- **THEN** each link works, the three languages load and the search finds no secret
