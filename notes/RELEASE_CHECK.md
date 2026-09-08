# Release check — Auto-SecAge public tree

> **Status 2026-09-08, pass 3 + packaging pass 4.** Early sections are the
> contemporaneous log. They are not deleted. Where they say
> `catalogs/asa-0002-exfil/attack.py` is omitted, **pass 3 supersedes that**:
> the file is in the tree, hash `7ee41b12…`, recovered from the Edit record.
> Pass 4 only fixes docs, bootstrap paths, `02-loop.md`, `SHA256SUMS` text
> mode, and POSIX zip layout. Catalog bytes were not edited in pass 4.

Built 2026-09-06 from the lab checkout at
`C:\Users\sheha\Desktop\The-Adimension\repos\AutoSecAge`. Catalog bytes were
copied from files that already existed on disk, except asa-0002 (pass 3).

## Hashes measured (not quoted)

| Path in this tree | Bytes | SHA-256 |
| --- | ---: | --- |
| `attack.py` | 25556 | `9d49773c42769cf461f2dfd6affdb14beea686a214a222b54dbb845ae3953a18` |
| `catalogs/asa-0001-shipped/attack.py` | 23036 | `3b33f018342444f3e959b3849de09b7b864a398ff9e593243b45ea626f1a92ea` |
| `catalogs/asa-0003-deputy/attack.py` | 25556 | `9d49773c42769cf461f2dfd6affdb14beea686a214a222b54dbb845ae3953a18` |

Source hashes in the lab, measured the same way:

| Lab path | Bytes | SHA-256 |
| --- | ---: | --- |
| `attack.py` (HEAD) | 25556 | `9d49773c…` — matches the required asa-0003 value |
| `kaggle_kernel/kaggle_snapshot/kernel_output/attack.py` | 23036 | `3b33f018…` — matches the required asa-0001 value |
| `kaggle_kernel/output/attack.py` | 22393 | `82025cb600d1478fd7c2fa6d69432a2486f495076d77b99915b6819e1ef1cd63` (v1, not a named keep) |

`cmp` confirms `attack.py` and `catalogs/asa-0003-deputy/attack.py` are byte-identical.
`sha256sum -c catalogs/SHA256SUMS` passes for both catalog files.

## asa-0002: searched once, NOT found

Target `7ee41b127502e1d77969edd2991cbc900da2f367cafae17cb23a74d5fbcd0625`.

- Filesystem: hashed every `attack.py*` and `*.bak*` under
  `Desktop/The-Adimension/repos` (excluding venvs). Matches found were only
  `3b33f018…`, `82025cb6…`, and `9d49773c…`.
- Git: content-hashed **every blob** in the lab object store. No match.

Conclusion **at pass 1**: `catalogs/asa-0002-exfil/attack.py` was omitted
because no retained file hashed to `7ee41b12…`. The hash stayed in
`results.tsv`. Pass 3 later recovered those bytes from the Edit transcript
(see the pass-3 section). This subsection is the pass-1 record, not the
current tree.

## Files omitted, and why

| Omitted | Reason |
| --- | --- |
| `lab_sdk/`, competition zip | Licensed competition SDK/data. Left on disk in the lab; excluded here and from the upload. Bootstrap instructions are in `README.md`. |
| `.venv_replay/`, `__pycache__/`, `*.pyc` | Generated. |
| `kaggle_kernel/kaggle_snapshot/` | Raw evidence dump; distilled into `notes/provenance.md` instead. |
| `kaggle_kernel/submission_notebook.ipynb` | Not distributed wholesale; the `serve()` / `KAGGLE_IS_COMPETITION_RERUN` cells are quoted in `kaggle/serve-cell.md`. |
| `handoff.md` | Internal working ledger. LIVE facts distilled into `notes/provenance.md` and `notes/lineage.md`. |
| `README_SUBMIT.md` | Kaggle submission ops; relevant content folded into `README.md` and `kaggle/README.md`. |
| `sessions/oracle-*.log` | Regenerable metric snapshots; the decision record is `results.tsv` / `replays.tsv` / `sessions/memory.md`. |
| `notes/02-loop.md` | Absent at pass 1 (only one writeup body in the lab checkout). **Added in pass 4** from the second working-note draft. |
| `catalogs/asa-0002-exfil/attack.py` | Absent at pass 1. **Added in pass 3** (recovered, hash-verified). |

`sessions/e0-full-*.log` and `sessions/asa0003-*.log` were also left out of this
tree; the measured rows they summarise are in `replays.tsv`, which is copied
verbatim.

## Unmodified copies

`results.tsv` and `sessions/memory.md` are byte-identical to the lab (`cmp` clean).
No row was rewritten or reordered.

## Functional check in this tree

```
assess_local.py  -> AST ok, 420 candidates, Deterministic True,
                    Twin Blind True (peeking_violations=0), Literal calls 0,
                    case digest 50053788945dad3f…, exit 0
oracle_local.py  -> exit 3 with the bootstrap message (lab_sdk/ absent, as intended)
```

`program.md` contains the heading `## Amendment 2026-09-06` (line 164) plus a
one-line pointer under "Threat base — four predicate arms" so the asa-0001 bullets
are not read as current.

## Recommended zip command

`zip` is not on PATH in this environment; use PowerShell from the parent of the
public tree:

```powershell
Compress-Archive -Path .\Auto-SecAge-public\* -DestinationPath .\Auto-SecAge-public.zip -Force
```

POSIX equivalent where `zip` exists:

```bash
zip -r Auto-SecAge-public.zip Auto-SecAge-public -x '*.pyc' -x '*__pycache__*' -x '*.venv*'
```

Do not zip the lab checkout, and never include `lab_sdk/`.

---

# Pass 2 — recover asa-* from Kaggle notebooks (2026-09-08)

Question: were any `asa-000x` catalogs written into notebooks pushed to Kaggle?

## Method

Inventoried every `.ipynb` on the machine (lab, sibling checkouts, `~/Downloads`),
hashed each notebook, then extracted every embedded `AttackAlgorithm` module —
`%%writefile` payloads plus any module-shaped string literal, unescaped via `ast`
— into a scratch dir outside this repo and hashed each extract. Cross-checked
against a live `kaggle kernels pull`.

## Hashes measured today

| Extract source | Cell | Bytes | SHA-256 |
| --- | ---: | ---: | --- |
| `submission_notebook.ipynb` (×3 identical copies) | 1 | 23036 | `3b33f018…` |
| `kaggle_snapshot/kernel_pull/auto-secage.ipynb` | 1 | 23036 | `3b33f018…` |
| live kernel pull 2026-09-08 | 1 | 23036 | `3b33f018…` |
| `~/Downloads/auto-secage.ipynb`, `auto-secage (1).ipynb` | 1 | 23036 | `3b33f018…` |
| `working_note.ipynb` (both versions) | — | — | no module cell |

Live pull notebook `853df5bd…` is `cmp`-identical to the 2026-09-06 snapshot.

## CLI

Used. `kaggle` is not on PATH; invoked at
`AppData\Roaming\Python\Python314\Scripts\kaggle.exe`.
`kernels list --mine` (one Auto-SecAge kernel), `kernels status` (COMPLETE),
`kernels pull --metadata` (succeeded). No push, no submit, no private APIs.

## asa-0002: still NOT found — now a positive finding

Absent from every notebook on disk **and** from the notebook currently on Kaggle,
in addition to the pass-1 filesystem sweep and git blob scan. Conclusion:
asa-0002 was a **lab-only keep**, never written to a file, a commit, or a
notebook. `catalogs/asa-0002-exfil/` stays absent; `program.md`'s amendment
sentence about it remains accurate and was left unchanged.

## Unlabeled catalogs

None. Exactly three distinct full-module hashes exist on this machine:
`3b33f018…` (asa-0001), `82025cb6…` (v1 worker), `9d49773c…` (asa-0003).

## Paths added or changed this pass

- `notes/notebook-inventory.md` — **new**
- `notes/lineage.md` — added "Notebook and kernel sources (pass 2)"
- `catalogs/README.md` — rewritten with a verified-source column
- `catalogs/kaggle-v1-22393/attack.py` — **new**, 22393 bytes, `82025cb6…`,
  labelled *not a named keep* (ERROR submission 56035703 path)
- `catalogs/SHA256SUMS` — regenerated, 3 entries, `sha256sum -c` passes
- `kaggle/README.md` — added the verified version → SHA section
- `notes/RELEASE_CHECK.md` — this section

Unchanged on purpose: `results.tsv`, `sessions/memory.md`, `program.md`
(the 0002 sentence is still correct), root `attack.py`, and both existing catalog
copies.

---

# Pass 3 — asa-0002 recovered outside the repo (2026-09-08)

Question: could asa-0002 be in the agent tooling's temp dirs or logs?

## Searched outside the repository

| Location | Result |
| --- | --- |
| `~/.claude/` (transcripts, backups, session dirs, shell snapshots) | no file with the hash |
| `%LOCALAPPDATA%\Temp`, `Temp\claude\`, `C:\tmp\` | no file with the hash |
| `~/.grok/` sessions, logs, memtrace, worktrees (881 MB) | no asa-0002; `3b33f018…` in 10 files (asa-0001 corroboration) |
| `AutoSecAge-3/` full-content scan (28 files) | no asa-0002 |

Only one file on the machine contains both the new-exfil and old-deputy markers:
the Claude session transcript — because it records the `Edit` calls, not because
it holds a copy of the file.

## Recovery

Extracted the three recorded `Edit` tool calls on `attack.py` from the transcript
and rebuilt asa-0002 two independent ways:

- Path A: asa-0003 with the deputy edit reversed → `7ee41b12…`, 24646 bytes
- Path B: asa-0001 with the exfil + projection edits applied → `7ee41b12…`, 24646 bytes
- Path A == Path B, byte-identical

Both match the hash logged in `results.tsv` at the time asa-0002 existed.
Validation: `ast` parses; runs to 420 candidates; case digest `50053788945dad3f…`
unchanged; profile is read-then-post exfil **+** old `Use email.send` deputy — the
exact asa-0002 signature.

This is recovery by **replaying a recorded edit and verifying against a
pre-registered hash**, not reconstruction from memory and not editing asa-0001
toward asa-0003. Provenance is labelled "recovered from the edit record, never
stored as a file" in `catalogs/README.md`, `notes/lineage.md`, and the
`program.md` amendment.

## Paths changed this pass

- `catalogs/asa-0002-exfil/attack.py` — **new**, 24646 bytes, `7ee41b12…`
- `catalogs/SHA256SUMS` — regenerated, 4 entries, `sha256sum -c` passes
- `catalogs/README.md` — asa-0002 row filled in; "intentionally absent" section
  replaced with "was recovered, not found"
- `notes/lineage.md` — "asa-0002 recovered (pass 3)"
- `program.md` — the amendment sentence about the missing file
- `notes/RELEASE_CHECK.md` — this section

Unchanged: `results.tsv`, `sessions/memory.md`, root `attack.py`, and the other
three catalog copies.

---

# Pass 4 — packaging and doc consistency (2026-09-08)

Review of `Auto-SecAge-public.zip` found correct catalog hashes and a
self-contradiction: pass-1/pass-2 prose still said asa-0002 was absent after
pass 3 had added the file. Also the zip used Windows `Compress-Archive`
backslash paths.

## Changes (docs and archive layout only)

- Banners on `notes/lineage.md`, `notes/notebook-inventory.md`, this file:
  pass 3 supersedes “0002 missing.”
- `notes/02-loop.md` added (second working-note body).
- `README.md` bootstrap lists POSIX `bin/python` and Windows `Scripts/python`.
- `catalogs/SHA256SUMS` rewritten in text mode (two spaces, no `*` prefix)
  so GNU `sha256sum -c` is unambiguous.
- Re-zipped with `zip -r` and POSIX `/` separators.

## Unchanged on purpose

All five `attack.py` files (root + four catalog copies), `results.tsv`,
`sessions/memory.md`, `program.md` amendment body, `assess_local.py`.
