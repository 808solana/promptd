"""
Token usage test runner.

Pushes every prompt in promptb.json through the running Neuralwatt tester
(POST /chat), one at a time, in file order, with no pause between prompts.
Retries each prompt up to 3x, then continues and notes the failure.

Usage (server must already be running on PORT 3000):
    .venv/bin/python run_token_test.py
"""

import json
import sys
import time

import requests

BASE_URL = "http://localhost:3000"
PROMPTS_FILE = "promptb.json"
MAX_RETRIES = 3
TIMEOUT_SECONDS = 600


def main():
    with open(PROMPTS_FILE) as f:
        prompts = json.load(f)

    total = len(prompts)
    print(f"Loaded {total} prompts from {PROMPTS_FILE}", flush=True)

    failed = []
    for i, prompt in enumerate(prompts):
        label = f"[{i + 1}/{total}]"
        ok = False
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                r = requests.post(
                    f"{BASE_URL}/chat",
                    json={"prompt": prompt},
                    timeout=TIMEOUT_SECONDS,
                )
                data = r.json()
                if r.status_code == 200 and "reply" in data:
                    req = data.get("request", {})
                    st = data.get("stats", {})
                    print(
                        f"{label} OK  "
                        f"tok={req.get('total_tokens')} "
                        f"(p{req.get('prompt_tokens')}/c{req.get('completion_tokens')}) "
                        f"cost=${req.get('cost_usd')} "
                        f"kwh={req.get('energy_kwh')} | "
                        f"cumulative: reqs={st.get('total_requests')} "
                        f"tok={st.get('total_tokens')} "
                        f"cost=${round(st.get('total_cost_usd') or 0, 6)}",
                        flush=True,
                    )
                    ok = True
                    break
                err = data.get("error", f"HTTP {r.status_code}")
                print(f"{label} attempt {attempt} failed: {err}", flush=True)
            except Exception as e:
                print(f"{label} attempt {attempt} error: {e}", flush=True)
            time.sleep(2)

        if not ok:
            print(f"{label} GAVE UP after {MAX_RETRIES} retries", flush=True)
            failed.append(i + 1)

    print("\n==== RUN COMPLETE ====", flush=True)
    print(f"Sent: {total} | Failed: {len(failed)}", flush=True)
    if failed:
        print(f"Failed prompt numbers: {failed}", flush=True)

    try:
        s = requests.get(f"{BASE_URL}/stats", timeout=30).json()
        print(
            f"Final stats: requests={s.get('total_requests')} "
            f"total_tokens={s.get('total_tokens')} "
            f"total_cost_usd=${round(s.get('total_cost_usd') or 0, 6)} "
            f"total_energy_kwh={s.get('total_energy_kwh')} "
            f"cost_per_million=${s.get('cost_per_million')}",
            flush=True,
        )
    except Exception as e:
        print(f"Could not fetch final stats: {e}", flush=True)

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
