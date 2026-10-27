---
language: en
style: ASD-STE100
last_reviewed: 2026-10-05
---

# Proposal

## Why

The video, the tags and the release do not exist until the owner makes them. They come after the first pass of `docs-followups-2`. The site, the slides, the README and the requirement cards need their links: the release tag, the GitHub release, the date, the video and the public site. A plan that waits for them cannot run alone, so these tasks have their own change. It cites REQ-0036, REQ-0037 and REQ-0051.

## Owner inputs

The owner starts the session and gives these inputs. After that, every task is automatic.

- The names of the tags the owner created and the URL of the GitHub release.
- The URL of the video, or the file name if it is a local link.
- The confirmation that the owner pushed and that GitHub Pages deployed, and the URL of the public site.

## What Changes

- **Numbers.** Regenerate `site/numbers.json` and rebuild the Spanish and Portuguese copies.
- **Links.** Add the tag, the release link, the date and the video to the site, the slides and the README. Show the tag and the build line in the site footer.
- **Public site check.** Check the three languages, the links, the phone layout, the diagrams and the absence of secrets.
- **Email check.** Check the submission email against the delivery checklist, with no real password.
- **Requirements and team.** Set the status of REQ-0036 and REQ-0037 where their evidence now exists.

## Capabilities

### New Capabilities
- `final-links`: the site, the slides and the README link to the release and the video.

### Modified Capabilities
(none)

## Impact

- `site/`, `site/i18n/`, `README.md`, `docs/build/delivery.md`, `docs/requirements/`, `team/`.

## Non-goals

- Producing the video. The owner does it.
- Pushing, opening a pull request, creating a tag or sending the email.
- A change to code, prompts, policy, cut-offs or the `bundle_hash`.
