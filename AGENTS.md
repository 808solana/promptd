# AGENTS.md

## Cursor Cloud specific instructions

### What this is
A single-file Flask web app (`neuralwatt_test.py`) that proxies prompts to the
Neuralwatt LLM API (OpenAI-compatible) and reports per-request token usage,
energy (kWh), and cost. `promptb.json` is just a static list of sample prompts
and is not imported by the app.

### Running
- Python deps live in a local virtualenv at `.venv` (created by the update
  script). Run the server with `.venv/bin/python neuralwatt_test.py`.
- The server listens on `http://localhost:3000` (hardcoded `PORT = 3000`). It
  runs with `debug=False`, so there is **no auto-reload** — restart the process
  after editing the file.

### Gotchas
- The Neuralwatt API key and base URL are hardcoded near the top of
  `neuralwatt_test.py` (`NEURALWATT_API_KEY`, `NEURALWATT_BASE_URL`,
  `MODEL = "glm-5.2"`). The `/chat` route makes a live external call, so it
  needs outbound network access to `api.neuralwatt.com`.
- Stats are in-memory and reset on every restart. `POST /reset` clears them.
- Endpoints: `GET /` (UI), `POST /chat` (`{"prompt": "..."}`), `GET /stats`,
  `POST /reset`.
- There are no automated tests or lint config in this repo.
