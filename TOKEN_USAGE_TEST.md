# Token Usage Test — Living Doc

> Ever-evolving. Audience: just us. Updated as the plan changes.

## The goal (what "winning" looks like)

> "The winning literally just looks like you putting all the prompts. That's the goal. That's really it."

Push all **100 prompts** from `promptb.json` through the Neuralwatt tester, **in
file order**. Done = every prompt sent and answered.

## How we run it

- **Programmatic**, hitting `POST /chat` one at a time. Ignore the human/UI
  copy-paste-Enter flow.
- **One at a time, no pause**: fire the next prompt the instant the previous
  one finishes (the UI equivalent is the green "DONE — READY FOR THE NEXT
  PROMPT" banner).
- **In order**, prompt 0 → 99.
- **Stats:** leave whatever is already there (a couple of warm-up requests are
  fine). No reset.
- **Failures:** retry up to **3×**, then continue and note which prompt failed.
  One bad prompt must never stall the whole run.

Runner: `run_token_test.py` (reads `promptb.json`, posts each to `/chat`).

## Zero caching (hard requirement)

> "We want the caching to be zero."

Every request must be a genuine fresh inference — no cache hits. This is baked
into `neuralwatt_test.py` by construction:

- a random UUID **nonce** injected into the system prompt,
- a random **seed**,
- **temperature jitter**,
- `no-cache` request headers.

Caveat: this is **client-side cache-busting**. There's no cache-hit flag in the
response, so "zero cache" is *by construction, not by measurement* — we trust
Neuralwatt honors it.

## No capture — livestream only

> "We're gonna have no capture of what is gonna happen... it's only on live.
> If we were to stop this right now, there will be no remember to what
> happened. It's just a livestream."

No videos, no screenshots, no saved artifacts of the run itself. Watch it live;
if it stops, there's no record. (This doc is the one lasting thing — it captures
*how* we run, not a transcript of any run.)

## Run log

_(Append short notes per run here: when, how many succeeded, any prompts that
hit the 3× retry limit. Keep it terse.)_
