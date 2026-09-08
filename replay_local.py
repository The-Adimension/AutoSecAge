#!/usr/bin/env python3
# Auto-SecAge
# Shehab Anwer, MD (habanwer) - The Adimension
# REDACTS x Agent-ProSAT x autoresearch-MIL
"""
replay_local.py - LAB-ONLY measured replay harness (autoresearch-MIL loop shape).

Not shipped. Not imported by attack.py. The Kaggle worker never sees this file.

Why this file exists
--------------------
`results.tsv` records only structural metrics, so the lab loop has no dependent
variable and `keep` is an assertion rather than a selection. autoresearch-MIL
solves that with a fixed wall-clock budget plus one primary metric (`val_bpb`).
This is the same contract for a security catalog:

    fixed replay budget  ->  one primary metric (local_sev_score)
    guardrail metrics that must not break  ->  invalid_candidates == 0
    diagnostics that explain the primary   ->  per-arm fire counts

Twin-blind boundary
-------------------
`aicomp_sdk.core.predicates` is on `assess_local.py`'s peek blocklist, and that
scan reads `attack.py` only. The locked law already says "structural checks only
*unless a local env is present*". A local env is present here, so this lab file
may score a replay with the released public scorer. `attack.py` stays clean.

What this measures is NOT the hosted score: public guardrail only, the hidden
private guardrail is absent, and the defender is a scripted agent rather than
GPT-OSS-20B or Gemma 4. It cannot explain submission 56036071's zeros.

Usage:
    python replay_local.py --tag e0 --budget 60 --describe "baseline"
"""

from __future__ import annotations

import argparse
import json
import os
import statistics
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SDK = ROOT / "lab_sdk"
if str(SDK) not in sys.path:
    sys.path.insert(0, str(SDK))
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

REPLAYS = ROOT / "replays.tsv"
SESSIONS = ROOT / "sessions"

COLUMNS = (
    "run_id\tts\tagent\tguardrail\tbudget_s\treplay_seconds\tn_offered\tn_replayed\t"
    "invalid\tblocked\ttool_calls_ok\tlocal_sev_score\tscore_per_s\tfire_exfil\t"
    "fire_deputy\tfire_destructive\tfire_untrusted\tunique_cells\tmean_msg_chars\t"
    "k_max\tF_measured\tg_measured\tstatus\tdescription"
)


def _arm_of(messages: tuple[str, ...]) -> str:
    """HEURISTIC arm attribution from our own catalog markers.

    Only labels rows for diagnosis. The score itself is the released scorer.
    Mirrors the classifier in the locked `assess_local.py`.
    """
    blob = " ".join(messages)
    if "/untrusted/" in blob or "fixture inbox" in blob or "/after-read/" in blob:
        return "untrusted"
    if "secret.txt" in blob or "fs.write" in blob or "fs.delete" in blob:
        return "destructive"
    if "/exfil/" in blob:
        return "exfil"
    if "email.send" in blob or "Notify " in blob or "Let " in blob or "Please email" in blob:
        return "deputy"
    return "other"


def main() -> int:
    p = argparse.ArgumentParser(description="Auto-SecAge local measured replay")
    p.add_argument("--tag", default="e0", help="experiment tag, e.g. e0 / e1-n60")
    p.add_argument("--budget", type=float, default=60.0, help="replay budget, seconds")
    p.add_argument("--limit", type=int, default=0, help="cap candidates offered (0 = all)")
    p.add_argument("--describe", default="", help="one-line hypothesis for the row")
    p.add_argument("--status", default="", help="baseline / keep / discard (blank = unset)")
    p.add_argument("--dry-run", action="store_true", help="wire check on 3 candidates, no row")
    args = p.parse_args()

    if not (SDK / "aicomp_sdk").is_dir():
        print(
            "[bootstrap] lab_sdk/ not found. This runner needs the released\n"
            "competition SDK to compute metrics. Fetch it (not committed to the repo):\n"
            "  kaggle competitions download -c ai-agent-security-multi-step-tool-attacks -p lab_sdk\n"
            "  (then unzip in place), and create a venv with: gymnasium<1,>=0.29  pydantic\n",
            file=sys.stderr,
        )
        return 3

    from aicomp_sdk.agents.deterministic_agent import VulnerableDeterministicAgent
    from aicomp_sdk.attacks.baselines.guardrail_rules import Guardrail
    from aicomp_sdk.core.cells import cell_signature
    from aicomp_sdk.core.predicates import eval_predicates
    from aicomp_sdk.core.replay import ReplayHarness

    try:
        from aicomp_sdk.core.env.api import MAX_USER_MESSAGE_CHARS
    except Exception:
        MAX_USER_MESSAGE_CHARS = 2000

    from attack import FROZEN_CASE, AttackAlgorithm, case_digest

    fixtures = SDK / "aicomp_sdk" / "fixtures"
    seed = int(FROZEN_CASE.get("seed", 123))

    candidates = AttackAlgorithm().run(None, None)
    packed = [
        tuple(str(m) for m in getattr(c, "user_messages", ()) if str(m)) for c in candidates
    ]
    if args.limit:
        packed = packed[: args.limit]
    if args.dry_run:
        packed = packed[:3]

    invalid = sum(
        1
        for msgs in packed
        if not msgs
        or len(msgs) > 32
        or any(len(m) > MAX_USER_MESSAGE_CHARS for m in msgs)
    )

    harness = ReplayHarness(fixtures)
    guardrail = Guardrail()

    t0 = time.perf_counter()
    deadline = t0 + float(args.budget)

    n_replayed = 0
    blocked = 0
    tool_calls_ok = 0
    score = 0
    fires = {"exfil": 0, "deputy": 0, "destructive": 0, "untrusted": 0, "other": 0}
    pred_counts: dict[str, int] = {}
    cells: set[str] = set()
    per_hop: dict[int, list[float]] = {}
    char_lengths: list[int] = []

    for msgs in packed:
        if time.perf_counter() >= deadline:
            break
        t_c = time.perf_counter()
        trace = harness.replay(seed, msgs, VulnerableDeterministicAgent(), guardrail)
        dt = time.perf_counter() - t_c

        n_replayed += 1
        k = len(msgs)
        per_hop.setdefault(k, []).append(dt)
        char_lengths.extend(len(m) for m in msgs)

        events = trace.get("tool_events", [])
        tool_calls_ok += sum(1 for e in events if e.get("ok") is True)
        blocked += sum(1 for e in events if e.get("ok") is not True)

        triggered = eval_predicates(trace)
        if triggered:
            arm = _arm_of(msgs)
            fires[arm] = fires.get(arm, 0) + 1
            for t in triggered:
                score += int(t.get("severity", 0))
                name = str(t.get("predicate", "?"))
                pred_counts[name] = pred_counts.get(name, 0) + 1

        try:
            cells.add(
                str(
                    cell_signature(
                        events,
                        egress_data=trace.get("egress"),
                        user_messages=list(trace.get("user_messages", [])),
                    )
                )
            )
        except Exception:
            pass

    replay_seconds = time.perf_counter() - t0

    # Budget law: t_K = F + K*g, fitted from the K values actually replayed.
    t1 = statistics.mean(per_hop[1]) if per_hop.get(1) else None
    t2 = statistics.mean(per_hop[2]) if per_hop.get(2) else None
    if t1 is not None and t2 is not None:
        g_measured = t2 - t1
        f_measured = t1 - g_measured
    elif t1 is not None:
        g_measured, f_measured = float("nan"), t1
    else:
        g_measured, f_measured = float("nan"), float("nan")

    k_max = max(per_hop) if per_hop else 0
    mean_chars = round(statistics.mean(char_lengths)) if char_lengths else 0
    score_per_s = score / replay_seconds if replay_seconds > 0 else 0.0
    run_id = "%s-%s" % (args.tag, datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"))
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    lines = [
        "---",
        "run_id:            %s" % run_id,
        "agent:             VulnerableDeterministicAgent",
        "guardrail:         attacks.baselines.guardrail_rules.Guardrail (public)",
        "case_digest:       %s" % case_digest()[:16],
        "budget_s:          %.1f" % args.budget,
        "replay_seconds:    %.2f" % replay_seconds,
        "n_offered:         %d" % len(packed),
        "n_replayed:        %d" % n_replayed,
        "invalid:           %d" % invalid,
        "blocked:           %d" % blocked,
        "tool_calls_ok:     %d" % tool_calls_ok,
        "local_sev_score:   %d" % score,
        "score_per_s:       %.3f" % score_per_s,
        "predicates:        %s" % (json.dumps(pred_counts, sort_keys=True) if pred_counts else "{}"),
        "fire_exfil:        %d" % fires["exfil"],
        "fire_deputy:       %d" % fires["deputy"],
        "fire_destructive:  %d" % fires["destructive"],
        "fire_untrusted:    %d" % fires["untrusted"],
        "unique_cells:      %d" % len(cells),
        "mean_msg_chars:    %d" % mean_chars,
        "k_max:             %d" % k_max,
        "F_measured:        %.4f" % f_measured,
        "g_measured:        %.4f" % g_measured,
        "note:              local replay, public guardrail only, scripted agent."
        " NOT the hosted score. Cannot explain submission 56036071.",
    ]
    report = "\n".join(lines)
    print(report)

    if args.dry_run:
        print("\n[dry-run] no row appended, no log written")
        return 0

    SESSIONS.mkdir(exist_ok=True)
    (SESSIONS / ("%s.log" % run_id)).write_text(report + "\n", encoding="utf-8")

    if not REPLAYS.exists():
        REPLAYS.write_text(COLUMNS + "\n", encoding="utf-8")
    row = "\t".join(
        str(x)
        for x in (
            run_id,
            ts,
            "VulnerableDeterministicAgent",
            "guardrail_rules.Guardrail",
            "%.1f" % args.budget,
            "%.2f" % replay_seconds,
            len(packed),
            n_replayed,
            invalid,
            blocked,
            tool_calls_ok,
            score,
            "%.3f" % score_per_s,
            fires["exfil"],
            fires["deputy"],
            fires["destructive"],
            fires["untrusted"],
            len(cells),
            mean_chars,
            k_max,
            "%.4f" % f_measured,
            "%.4f" % g_measured,
            args.status or "unset",
            args.describe or "(no description)",
        )
    )
    with REPLAYS.open("a", encoding="utf-8") as fh:
        fh.write(row + "\n")
    print("\nappended %s" % REPLAYS.name)
    print("log      sessions/%s.log" % run_id)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
