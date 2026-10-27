# Sentinel Engine branding

Source of truth for slides, docs and the one-page chat (decision 006).
Palette: bank blue `#1f4fa3` on cool white, with a dark variant. Violet `#6d4aff` and rose `#ff4f8b` stay as the Sentinel mark (`--sentinel-violet`, `--sentinel-rose`) and are not the accent of the customer interface.
Typography: Newsreader (titles) + Source Sans 3 (body) + Source Code Pro (mono).

## Files

| File | Use |
|---|---|
| `brand.css` | Variables only. `:root` is light, `[data-theme="dark"]` is dark. Import first. |
| `theme-sentinel.css` | Gradient details, focus rings, cards. Used by slides and docs on top of their own base stylesheet. |
| `chat.css` | Chat thread, candidates, confirm box, input. Used by the FastAPI one-page chat. |
| `preview.html` | Static preview, no build step. Open directly in a browser. |

## Usage

Slides/docs (local PDF pipeline):

```html
<link rel="stylesheet" href="branding/brand.css">
<link rel="stylesheet" href="base.css">
<link rel="stylesheet" href="branding/theme-sentinel.css">
```

Paths are relative to the repository root. Adjust them to the page that links the files.

Chat (FastAPI serves `branding/` at `/branding/`):

```html
<link rel="stylesheet" href="/branding/brand.css">
<link rel="stylesheet" href="/branding/chat.css">
```

Dark mode: set `data-theme="dark"` on `<html>`. Light: `data-theme="light"` or no attribute.
Print/PDF always renders light.

## Rules

- No pandoc, chromium or any build step required for this folder. The PDF pipeline
  (`estilos/build.py`) is a local tool outside the repository and never a repo dependency.
- The `estilos/` folder is a loose copy for internal PDFs. It may diverge from this folder;
  no sync is enforced. To refresh it, copy `brand.css` and `theme-sentinel.css` into it.
- Never commit PDFs, `.env` or datasets. See `AGENTS.md`.
