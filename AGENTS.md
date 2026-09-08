# Auto-SecAge — start here (agent loop)

Auto-SecAge is one **autoresearch loop** (REDACTS × Agent-ProSAT × autoresearch-MIL,
contracts only). If you are an agent pointed at this repo, run the loop; do not
rebuild it.

## The loop

1. **READ** the law and the state, in order:
   `program.md` (LOCKED protocol) · `ground.json` (LOCKED) · `model.json` · `handoff.md`
   (evidence index + next-task gates) · `sessions/memory.md` · `results.tsv` · `replays.tsv`.
2. **RUN a metric file** — this is the decision input, not decoration:
   - `python oracle_local.py` → per-arm severity under the released public scorer +
     baseline guardrail (perfect-compliance). **This is the primary metric** (the
     `val_bpb` analog): an arm is live only if its severity > 0.
   - `python assess_local.py` → twin-blind / determinism / literal-call **gate**
     (must pass: `peeking_violations = 0`, deterministic, exit 0).
   - `python replay_local.py --tag <e> --budget <s> --describe "..."` → structural
     replay through the real `SandboxEnv` (validity, tool calls, cells; not a score).
3. **DECIDE** by the metric (ProSAT keep/revert): keep the edit if the oracle
   severity improved and the gate still passes; otherwise revert. One change per
   iteration; take the lowest-coverage arm next.
4. **EDIT one file** — `attack.py` (an arm) or `model.json` (a knob). Nothing else.
5. **LOG** — append `results.tsv` (structural + keep/revert, with the `attack.py`
   SHA-256), `replays.tsv` (measured rows), `sessions/memory.md` (signed
   Auto-SecAge), and write any LIVE change back into `handoff.md`.

## Hard rules (from `program.md`, do not break)

- **Twin-blind.** `attack.py` never imports the private scorer, never reads a hidden
  guardrail, never conditions on peeked predicate behaviour. The `*_local.py` files
  may use the released SDK because a local env is present; the shipped file may not.
- **No `os.environ` case config.** The in-file `FROZEN_CASE` is the case.
- **Fixtures only.** `.invalid` URLs, fixture-style secrets, mock tools. No live systems.
- **Do not submit to Kaggle.** The scored deadline (2026-09-01) has passed; this is a
  Working Note lab. Late scores stay the strings `0.00000` / `0.00000` and are not a
  timeout, not proof `N` was too large, not a per-model split.
- **Do not** copy third-party `attack.py`, invent leaderboard places or fire-rates, or
  commit the excluded paths (see `.gitignore`).

## Bootstrap (the metric files need the competition SDK, which is NOT committed)

```bash
kaggle competitions download -c ai-agent-security-multi-step-tool-attacks -p lab_sdk
# unzip in place, then:
python -m venv .venv_replay
.venv_replay/Scripts/python -m pip install "gymnasium<1,>=0.29" pydantic
```

Run the metric files with that interpreter. If `lab_sdk/` is missing, the runners
print this same bootstrap line and exit 3.

## File map

| File | Owner | Role |
|---|---|---|
| `program.md` `ground.json` `assess_local.py` `DISCLAIMER.md` | user, **locked** | law + the twin-blind gate |
| `attack.py` `model.json` `case.toml` | agent | the scored solver + knobs |
| `oracle_local.py` `replay_local.py` | agent, lab-only | metric runners (never shipped) |
| `results.tsv` `replays.tsv` `sessions/memory.md` | agent, append-only | the log |
| `handoff.md` | agent, rewrite-in-place with dates | evidence index + next-task gates |
| `working_note.ipynb` | agent | the Kaggle Working Note artifact |

Deeper protocol: `program.md`. Current state and next gates: `handoff.md` §16.
