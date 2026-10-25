# Course Advisory Lab

An English, browser-based demo of the adult-training FDE reference prototype. Visitors can choose four synthetic scenarios, edit learner requirements, inspect matching and escalation decisions, review the reply draft and download the structured result. No account, API key or server-side application is required.

**[Open the GitHub Pages demo](https://xiaohongzhao.github.io/fde-education-simulation/)**

## Run locally

From this directory:

```bash
python3 -m http.server 8765 --directory dist
```

Open `http://localhost:8765`. Serve the files over HTTP; opening `index.html` directly as a file will not load the data module correctly.

## Implementation

- `dist/engine.mjs`: a dependency-free JavaScript port of `prototype/education.py` for offline decisions and English templates.
- `dist/app.js`: form, presets, accessible result tabs, copy and JSON download.
- `dist/data.json`: the original synthetic catalogue and four example inputs.
- `dist/index.html` and `dist/style.css`: responsive interface.
- `../.github/workflows/pages.yml`: GitHub Actions workflow that publishes `web/dist` to GitHub Pages when website files change on `main`.
- `.openai/hosting.json`: retained metadata for the earlier Sites deployment; GitHub Pages does not use this file.

The simulated date defaults to 2026-10-25 and can be changed in More controls. CNY prices and UTC+08:00 trial times retain the original scenario. The browser trace omits Python's input fingerprint; matching, routing, draft content and action states follow the reference implementation.

This is a rule-based simulation without live AI. It does not send messages, reserve places, charge payments or connect to a CRM. The host serves static assets, and Google Fonts may fetch typefaces; profile inputs are processed only in browser memory and are not submitted by the app. Nothing is persisted between visits.

## Verify the browser port

In the complete project checkout, run `python3 web/check_parity.py` from the project root. It requires Node.js and compares all 32 original cases, five times each, against both their expected behaviour and the Python output. The intentionally omitted input fingerprint is excluded from comparison. This check does not assess live AI quality or real business outcomes.

## Attribution

Part of [XiaohongZhao/fde-education-simulation](https://github.com/XiaohongZhao/fde-education-simulation). The original FDE exercise structure is credited in the parent project's `NOTICE.md`; this browser interface is an added portfolio adaptation.
