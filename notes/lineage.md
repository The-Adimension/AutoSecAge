# Lineage — how the three catalogs relate, and what git does not hold

> **Status 2026-09-08, pass 3.** `catalogs/asa-0002-exfil/attack.py` is present.
> It was **recovered from the recorded Edit transcript** and hash-verified against
> `results.tsv` (`7ee41b12…`). It was never found as a retained file. Sections
> below that still say “asa-0002 is missing” are the pass-1 record and are
> **superseded** by “asa-0002 recovered (pass 3)” at the end of this file.

Measured on this machine, 2026-09-06, with pass-2/pass-3 updates on 2026-09-08.
Hashes below were produced by `sha256sum` on files that exist on disk; none was
copied from a document.

## Measured hashes

| File on disk | Bytes | SHA-256 |
| --- | ---: | --- |
| `attack.py` (lab HEAD) | 25556 | `9d49773c42769cf461f2dfd6affdb14beea686a214a222b54dbb845ae3953a18` |
| `kaggle_kernel/kaggle_snapshot/kernel_output/attack.py` | 23036 | `3b33f018342444f3e959b3849de09b7b864a398ff9e593243b45ea626f1a92ea` |
| `kaggle_kernel/output/attack.py` | 22393 | `82025cb600d1478fd7c2fa6d69432a2486f495076d77b99915b6819e1ef1cd63` |
| `catalogs/asa-0002-exfil/attack.py` (pass 3, recovered) | 24646 | `7ee41b127502e1d77969edd2991cbc900da2f367cafae17cb23a74d5fbcd0625` |

## Git holds only asa-0003

The lab checkout has exactly two commits:

```
6603f62 Clean-up: untrack regenerable oracle logs; record git init in KB
7415aaa Baseline: Auto-SecAge autoresearch loop as a single clean repo
```

`git log -- attack.py` returns only `7415aaa`. Both commits therefore point at
**asa-0003**. Git was initialised *after* the repairs, so there is **no git blob
for asa-0001 or asa-0002**. A content-hash scan of every object in the store
confirmed this.

Consequence: git history is not the provenance record for this project. The
provenance record is `results.tsv` + `sessions/memory.md` + the file hashes above.

## How asa-0001 survived

Not as a commit. It survived because the Kaggle kernel commit phase wrote
`/kaggle/working/attack.py`, and that output was downloaded into
`kaggle_kernel/kaggle_snapshot/kernel_output/attack.py` during the 2026-09-06
evidence gather. That downloaded file is the copy in
`catalogs/asa-0001-shipped/attack.py`.

## asa-0002 was missing from disk and git (pass 1)

`7ee41b127502e1d77969edd2991cbc900da2f367cafae17cb23a74d5fbcd0625` was measured
in the session that produced it and logged to `results.tsv`. Pass 1 searched
every `attack.py*` / `*.bak*` in the checkout and every git blob: **not found
as a retained file**. Pass 2 (notebooks + live kernel pull) also found no
copy. Pass 3 recovered the bytes from the Edit transcript; see the last
section. Do not read this subsection as “the catalog directory is empty.”

## Submissions

- **56035703** — v1, `SubmissionStatus.ERROR`, empty scores. Root cause: the
  notebook never called `JEDAttackInferenceServer().serve()`, so the gateway had
  no server. The 22393-byte `kaggle_kernel/output/attack.py` is that variant.
- **56036071** — v2, `SubmissionStatus.COMPLETE`, publicScore `0.00000`,
  privateScore `0.00000`. Unofficial: submitted after the 2026-09-01 scored
  deadline. The catalog inside it is **asa-0001**.

A COMPLETE zero is not a timeout — an overrun fails *without* a score. The zeros
are not evidence that N was too large, and no per-model cell split is claimed.

## Oracle result that drove the repairs

Against the released public scorer under a perfect-compliance assumption
(`oracle_local.py`): EXFILTRATION 0 → 5 (asa-0002), CONFUSED_DEPUTY 0 → 3
(asa-0003), DESTRUCTIVE_WRITE 4 throughout, UNTRUSTED_TO_ACTION 5 throughout.
Dead share of the N=420 catalog: **80% (336/420) → 0%**.

That is a catalog-design measurement, not a hosted fire-rate, and it does not
explain submission 56036071's zeros.

## Do not treat Repomix as a SHA source

A packed/markdown rendering of this repo is not a byte source. Never reconstruct
`attack.py` (or any hash) from a Repomix bundle, a chat transcript, or a document.
Copy bytes from a file, or omit the file.

## Notebook and kernel sources (pass 2, 2026-09-08)

Question: were any `asa-000x` catalogs written into notebooks pushed to Kaggle?
Method: parse every `.ipynb` on the machine, pull the live kernel, extract each
embedded `AttackAlgorithm` module (`%%writefile` payload or module-shaped string
literal), and hash it. Full table in `notebook-inventory.md`.

| Source | Cell | Bytes | SHA-256 | Verdict |
| --- | ---: | ---: | --- | --- |
| `submission_notebook.ipynb` (3 identical copies) | 1 | 23036 | `3b33f018…` | asa-0001 |
| `kaggle_snapshot/kernel_pull/auto-secage.ipynb` | 1 | 23036 | `3b33f018…` | asa-0001 |
| live `kaggle kernels pull` 2026-09-08 | 1 | 23036 | `3b33f018…` | asa-0001 |
| `~/Downloads/auto-secage.ipynb` and `(1)` | 1 | 23036 | `3b33f018…` | asa-0001 |
| `working_note.ipynb` (both versions) | — | — | — | no module cell |

Results against the decision table:

- **`3b33f018…` confirmed.** `cmp` shows `catalogs/asa-0001-shipped/attack.py` is
  identical to the notebook-extracted payload and to the kernel output file. The
  shipped catalog is now corroborated by three independent routes: the notebook
  cell that writes it, the worker output that was downloaded, and a live pull of
  the kernel as it stands today.
- **`7ee41b12…` in no notebook.** asa-0002 is in no notebook, on disk or on
  Kaggle. Together with the pass-1 filesystem and git-blob sweeps this is a
  positive finding rather than an absence of evidence: **asa-0002 was a lab-only
  keep**, never written to a file, a commit, or a notebook. It was later
  recovered from the session edit record and now ships as
  `catalogs/asa-0002-exfil/` — see “asa-0002 recovered (pass 3)” below.
- **`9d49773c…` in no notebook.** asa-0003 exists only as lab HEAD. The two
  repairs were never packaged for Kaggle. Nothing here suggests they were hosted.
- **`82025cb6…` recorded as `kaggle-v1-22393`.** The v1 worker file behind the
  ERROR submission 56035703, now copied to `catalogs/kaggle-v1-22393/attack.py`
  and labelled *not a named keep*. No notebook on disk writes those 22393 bytes,
  so the notebook version that produced them was not retained.
- **No unlabeled full catalog appeared.** Exactly three distinct full-module
  hashes exist anywhere on this machine: `3b33f018…`, `82025cb6…`, `9d49773c…`.

Consequence for the record: submission **56036071 ran asa-0001**, confirmed from
the notebook bytes and not merely from the kernel output. The unofficial
`0.00000` / `0.00000` therefore describe the *unrepaired* catalog — the one the
oracle later showed had 80% of its candidates unable to fire by design. That is a
consistency check, **not** a causal explanation of the zeros: the hosted run used
real models and the private guardrail, neither of which is measured here.

## asa-0002 recovered (pass 3, 2026-09-08)

Pass 1 (filesystem + git blobs) and pass 2 (every notebook + a live kernel pull)
both concluded asa-0002 had no stored bytes. Pass 3 extended the search **outside
the repository**, to the agent tooling's own state:

| Searched | Result |
| --- | --- |
| `~/.claude/` — transcripts, backups, session dirs, shell snapshots | no file with the asa-0002 hash |
| `%LOCALAPPDATA%\Temp\`, `%LOCALAPPDATA%\Temp\claude\`, `C:\tmp\` | no file with the asa-0002 hash |
| `~/.grok/` — sessions, logs, memtrace, worktrees (881 MB) | **no** asa-0002; asa-0001's hash `3b33f018…` appears in **10** files, corroborating the shipped catalog's lineage from the earlier Grok sessions |
| `AutoSecAge-3/` (full-content scan of all 28 files) | no asa-0002 |

So asa-0002 was never written to a file anywhere. **But the edit record survived.**
The Claude Code session transcript stores each `Edit` tool call with its exact
`old_string` and `new_string`. Three such calls were made to `attack.py`:

| # | Target | old len | new len |
| ---: | --- | ---: | ---: |
| 0 | `arm_exfil` (asa-0001 → asa-0002) | 1114 | 2445 |
| 1 | projection `k_exfil_eff` (part of asa-0002) | 210 | 487 |
| 2 | `arm_deputy` (asa-0002 → asa-0003) | 897 | 1807 |

Reconstructing from that record, two independent ways:

- **Path A** — asa-0003 with edit 2 reversed → `7ee41b12…`, 24646 bytes
- **Path B** — asa-0001 with edits 0 and 1 applied → `7ee41b12…`, 24646 bytes
- Path A output **==** Path B output, byte for byte

Both match the hash logged in `results.tsv` when asa-0002 actually existed. Two
derivations from different starting points landing on a pre-registered hash is
identification by cryptographic proof; a single wrong byte would break it.

Post-recovery validation: parses under `ast`; `AttackAlgorithm().run(None, None)`
returns 420 candidates with case digest `50053788945dad3f…` unchanged; and it
carries exactly the asa-0002 signature — read-then-post exfil together with the
old `Use email.send` deputy wording. That is the state in which the oracle read
EXFILTRATION 5 and CONFUSED_DEPUTY 0, which is why asa-0003 was needed.

The file now ships as `catalogs/asa-0002-exfil/attack.py`. Its provenance is
**recovered from the edit record**, not *found as a file* — recorded that way
everywhere so no reader mistakes it for a retained artifact.
