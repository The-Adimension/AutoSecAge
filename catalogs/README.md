# Catalogs — the named `attack.py` keeps

Every file here is a **byte-identical copy** of a file that exists on disk. Nothing
was reconstructed, re-generated, or edited to match a hash. Verify with
`sha256sum -c SHA256SUMS` from this directory.

| Id | Role | Bytes | SHA-256 | Verified source | Submitted |
| --- | --- | ---: | --- | --- | --- |
| asa-0001 | shipped catalog | 23036 | `3b33f018342444f3e959b3849de09b7b864a398ff9e593243b45ea626f1a92ea` | `kaggle_kernel/kaggle_snapshot/kernel_output/attack.py`; **independently confirmed** as the `%%writefile` payload in cell 1 of `submission_notebook.ipynb`, of the kernel pull, and of a live `kaggle kernels pull` on 2026-09-08 | yes, submission 56036071 |
| asa-0002 | exfil repair | 24646 | `7ee41b127502e1d77969edd2991cbc900da2f367cafae17cb23a74d5fbcd0625` | **recovered 2026-09-08** by replaying the recorded `Edit` operations from the Claude session transcript; hash-verified by two independent derivations (see below) | no |
| asa-0003 | deputy repair = HEAD | 25556 | `9d49773c42769cf461f2dfd6affdb14beea686a214a222b54dbb845ae3953a18` | lab `attack.py`; present in **no** notebook | no |

## Not a named keep

| Id | Bytes | SHA-256 | Source | Note |
| --- | ---: | --- | --- | --- |
| `kaggle-v1-22393` | 22393 | `82025cb600d1478fd7c2fa6d69432a2486f495076d77b99915b6819e1ef1cd63` | `kaggle_kernel/output/attack.py` | v1 worker file behind submission **56035703 (ERROR)** — the run where the notebook never called `JEDAttackInferenceServer().serve()`. It is **not** part of the asa-* lineage. No notebook on disk writes these bytes, so it came from an earlier, unretained notebook version. |

It is kept here because it is hash-verified evidence of the ERROR path, not
because it is a catalog. Do not relabel it asa-0001 or asa-0002.

## asa-0002 was recovered, not found

The bytes were **never stored as a file**: not on disk, not in any git blob, not in
any notebook, not in the Kaggle kernel, and not in the Grok or Claude log trees.
asa-0002 was an intermediate lab state between the two repairs.

What *was* stored is the **edit record**. The Claude Code session transcript
(`~/.claude/projects/.../<session>.jsonl`) contains the three `Edit` tool calls
made to `attack.py`, each with its exact `old_string` and `new_string`. asa-0002
is recoverable from that record by two independent routes:

- **Path A** — take asa-0003 and reverse the deputy edit (`new_string` → `old_string`).
- **Path B** — take asa-0001 and apply the exfil edit and the projection edit.

Both paths produce **byte-identical** output, 24646 bytes, hashing to
`7ee41b127502e1d77969edd2991cbc900da2f367cafae17cb23a74d5fbcd0625` — the value
independently logged in `results.tsv` at the time asa-0002 existed. Two derivations
from different starting points converging on the pre-registered hash is
cryptographic identification, not reconstruction by guesswork.

The recovered file was further checked: it parses (`ast`), runs to 420 candidates
with the unchanged case digest `50053788945dad3f…`, and shows exactly the asa-0002
profile — read-then-post exfil **with** the old `Use email.send` deputy wording,
which is the state that made the oracle read EXFILTRATION 5 / CONFUSED_DEPUTY 0.

Nothing here was edited toward a target hash. If any byte differed, the SHA-256
would not match.

## What changed between the keeps

asa-0001 → asa-0002: the EXFILTRATION arm stopped pasting a fixture literal and
instead reads `secret.txt` in-trace, then posts the read value.
asa-0002 → asa-0003: the CONFUSED_DEPUTY arm dropped `send` / `email` / `upload`
from its sole user message. See `../program.md` Amendment 2026-09-06,
`../notes/lineage.md`, and `../notes/notebook-inventory.md`.
