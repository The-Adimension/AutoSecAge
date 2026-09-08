# Auto-SecAge

**A sealed-case autoresearch lab for red-teaming tool-using AI agents.**
Shehab Anwer, MD ([`habanwer`](https://www.kaggle.com/habanwer)) — The Adimension.

An AI coding agent reads a sealed case, runs a metric, decides by that metric,
edits one file, and logs the result — repeatedly, without peeking at the grader.
Auto-SecAge ports the *contracts* of three first-party systems and executes none
of their runtimes: **REDACTS** (FrozenCase; ingest → baseline → static catalog →
severity gate → report), **Agent-ProSAT** (mutable solver, locked evaluator,
twin-blind, keep/revert), **autoresearch-MIL** (user-owned law vs agent-owned
solver, append-only memory, time budget as law).

Built as a case study for the Kaggle competition *AI Agent Security – Multi-Step
Tool Attacks* (AgentDojo lineage, arXiv:2406.13352). The scored artifact is
`attack.py`, which returns replayable `AttackCandidate` message chains.

> ⚠️ **Ethics and scope.** Authorized research against a **sealed offline
> benchmark**, using **mock tools and synthetic fixtures only**. URLs use the
> reserved `.invalid` TLD (RFC 2606) and are never resolved; secrets are
> fixture-style strings; there are no live systems, no live mail, and no real
> filesystem outside the sandbox. Findings are replay-dependent and **expert
> review remains mandatory**. See [`DISCLAIMER.md`](DISCLAIMER.md) and
> [`SECURITY.md`](SECURITY.md).

## The loop

Full contract in [`AGENTS.md`](AGENTS.md):

1. **Read** — `program.md` (locked), `ground.json` (locked), `model.json`,
   `sessions/memory.md`, `results.tsv`, `replays.tsv`.
2. **Run a metric** — `oracle_local.py` (**primary metric**: per-arm severity
   under the released public scorer, perfect-compliance), `assess_local.py`
   (twin-blind / determinism **gate**), `replay_local.py` (structural replay).
3. **Decide** — keep the edit if the metric improved and the gate still passes,
   else revert. One change per iteration.
4. **Edit one file** — `attack.py` (an arm) or `model.json` (a knob).
5. **Log** — append `results.tsv`, `replays.tsv`, `sessions/memory.md`.

## File ownership

| Files | Owner | Rule |
| --- | --- | --- |
| `program.md` `ground.json` `assess_local.py` `DISCLAIMER.md` | user | **locked** — read, do not change meaning |
| `attack.py` `model.json` `case.toml` `threat_base/arms.py` | agent | mutable, one change per iteration |
| `oracle_local.py` `replay_local.py` | agent | lab-only, **never shipped to the worker** |
| `results.tsv` `replays.tsv` `sessions/memory.md` | agent | **append-only** |

## Twin-blind

The official score is an evaluator **replay** of `user_messages`, with predicates
recomputed on the successful tool calls — fabricated traces score nothing. So
`attack.py` never imports the private scorer, never reads a hidden guardrail, and
never conditions generation on peeked predicate behaviour. `assess_local.py` is
locked: it AST-checks the solver, proves determinism (same FrozenCase + same `i` →
same text), and sets `peeking_violations` if a peeking pattern appears. The
`*_local.py` runners may use the **released** SDK because a local env is present;
the shipped file may not. Local numbers are structural or perfect-compliance
oracle values — **never hosted fire-rates**.

## Bootstrap

The competition SDK is licensed and **not distributed here**:

```bash
kaggle competitions download -c ai-agent-security-multi-step-tool-attacks -p lab_sdk
# unzip in place, then:
python -m venv .venv_replay
# POSIX:
.venv_replay/bin/python -m pip install "gymnasium<1,>=0.29" pydantic
# Windows:
# .venv_replay\Scripts\python -m pip install "gymnasium<1,>=0.29" pydantic
```

Then:

```bash
PY=.venv_replay/bin/python          # POSIX
# PY=.venv_replay/Scripts/python   # Windows
"$PY" assess_local.py             # gate: twin-blind pass, exit 0
"$PY" oracle_local.py             # primary metric: per-arm severity
"$PY" replay_local.py --tag e0 --budget 120 --describe "baseline"
```

`assess_local.py` and `attack.py` run on **plain stdlib** (a stub stands in for the
SDK), so the gate and the catalog work with any Python. If `lab_sdk/` is missing,
the metric runners print that bootstrap line and exit 3.

## Results, stated plainly

Against the released **public** scorer under a perfect-compliance assumption, the
shipped catalog had **80% of its 420 candidates (336) unable to fire by design**:
the exfil arm pasted a fixture literal where the scorer keys on secrets read
in-trace, and the deputy arm's own wording (`send` / `email` / `upload`) set
`user_allows_share` and killed its predicate. Two one-knob repairs took that dead
share to **0%** (`asa-0002`, `asa-0003`). See [`catalogs/`](catalogs/) and
[`notes/lineage.md`](notes/lineage.md).

**Those repairs were never submitted.** The two late submissions are unofficial —
the scored deadline was 2026-09-01. Submission 56035703 returned `ERROR`;
submission 56036071 returned `COMPLETE` with public `0.00000` and private
`0.00000`, and it contains the *unrepaired* `asa-0001` catalog. Those zeros stay
zeros: a COMPLETE zero is not a timeout, it is not evidence that N was too large,
and no per-model cell split is claimed. **This repo is not a medal writeup.**

## Kaggle artifacts

- Working Note: <https://www.kaggle.com/writeups/habanwer/Auto-SecAge>
- Inference notebook: <https://www.kaggle.com/code/habanwer/auto-secage>

Two public writeups by other teams are **cited, not reproduced** — competition
discussions 739181 and 739040. See [`notes/provenance.md`](notes/provenance.md).

## License

Apache-2.0 ([`LICENSE`](LICENSE)). © 2026 Shehab Anwer / The Adimension.
