# Provenance — LIVE strings only

Re-queried from the Kaggle API on 2026-09-06 unless marked otherwise. Nothing here
was scraped from a rendered web page; values came from the CLI/SDK or from files
on disk. Anything not verified is listed under Gaps rather than guessed.

## Author

Shehab Anwer, MD — Kaggle / GitHub `habanwer` — The Adimension.

## Competition

- <https://www.kaggle.com/competitions/ai-agent-security-multi-step-tool-attacks>
- Scored deadline: **2026-09-01T23:59:00**
- Working Note deadline: **2026-09-08 23:59 UTC**
- Benchmark lineage: AgentDojo, arXiv:2406.13352. Defenders: GPT-OSS-20B and
  Gemma 4 26B-A4B.

## Published artifacts

- Working Note (personal writeup): <https://www.kaggle.com/writeups/habanwer/Auto-SecAge>
  — forum topic **739748**, write-up id **113013**, state PUBLISHED, votes 0,
  commentCount 0. Body 13694 chars, SHA-256
  `a8a544bb45f47edc6f554bcb9c0f25a072967617363d8dd1150eda3d31b6396b`
  (re-fetched 2026-09-06; byte-identical to the local snapshot, `updateTime`
  equal to `createTime`, i.e. not revised since publication).
- Inference notebook: <https://www.kaggle.com/code/habanwer/auto-secage>
  — kernel id 133239645, status COMPLETE, public, GPU T4, internet off.

## Submissions

| ref | status | publicScore | privateScore |
| --- | --- | --- | --- |
| 56035703 | `SubmissionStatus.ERROR` | `""` | `""` |
| 56036071 | `SubmissionStatus.COMPLETE` | `0.00000` | `0.00000` |

Both are **late and therefore unofficial** (scored deadline 2026-09-01 had passed).
The zeros are the literal strings returned by the API. A COMPLETE zero is not a
timeout; an overrun fails without a score.

## Shipped case (asa-0001)

N = 420; arm mix 0.45 / 0.35 / 0.10 / 0.10 → **189 / 147 / 42 / 42**
(exfil / deputy / destructive / untrusted). FrozenCase knobs: `k_hops_exfil = 1`,
`framing = imperative_plain`, `harmony_gpt_oss = false`, `env_probe = false`,
`seed = 123`, `time_budget_s = 1800`, `replay_budget_s = 9000`,
`replay_safe = 0.99`, `max_tool_hops = 8`, `max_user_messages = 32`.
Priors (not measurements): `F_s = 8.0`, `g_s = 6.0`.
Conservative projection `N(F + K_max·g) = 8400 s` against a cap of `8910 s`.

Seal digests, read from `case.toml`:

- `digest` — `d436e65a5960ca299e6f47bf58e188ef8d6fa07960c22c9e4a733fd2904db116`
- `ground_digest` — `cf17073eb9668b8149b0bafde9f8319d300a8caf0da429a59b8f662b0e40e916`
- `model_digest` — `6909099a392089c4813810a522fc24791c424e9d1a710489b51ed70466b282af`

In-file FrozenCase digest reported by `attack.py` / `assess_local.py`:
`50053788945dad3fd33e79c3ec33957de6d301e8f07bd79416ca1c45a06ae555` (unchanged by
the asa-0002 / asa-0003 repairs, which touched arm bodies only).

## Cited, not reproduced

Two public writeups by other teams on the same competition, credited as prior art.
No technique of theirs is restated here and none of their code is carried:

- Kaggle competition discussion **739181** — "1st place solution", xz, 2026-09-03.
- Kaggle competition discussion **739040** — "4th Place Solution - Optimizing a
  Simple email.send Attack", Rick, 2026-09-02.

## Gaps (open; do not fill by inference)

- No hosted four-cell / per-model split for 56036071; no gateway rerun log.
- No fitted `F, g`. The local deterministic harness produced a *negative* g, so
  `F + K·g` does not describe it; only an LLM-in-the-loop run can fit it.
- No N / mix / framing sweep since the arms went live (a sweep before the repairs
  would have measured nothing, as 80% of the catalog could not fire).
- asa-0002 was never stored as a file; the bytes shipped in
  `catalogs/asa-0002-exfil/` were recovered from the session edit record and
  hash-verified (`7ee41b12…`) by two independent derivations. See `lineage.md`.
- The oracle is a perfect-compliance measurement against the **public** scorer.
  The private guardrail is absent and no model is in the loop, so it is not a
  fire-rate and cannot explain the zeros.
