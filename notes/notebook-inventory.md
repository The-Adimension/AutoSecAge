# Notebook inventory — where the catalogs actually live

> **Status 2026-09-08, pass 3.** Findings 1–2 below are still true of *notebooks*:
> neither asa-0002 nor asa-0003 is embedded in any `.ipynb` or in the live kernel.
> The sentence “`catalogs/asa-0002-exfil/` stays absent” is **stale**. That file
> was added in pass 3 from the Edit transcript, not from a notebook. See
> `lineage.md` § “asa-0002 recovered (pass 3)”.

Pass run 2026-09-08 on the author's machine. Question asked: **were any `asa-000x`
catalogs written into notebooks pushed to Kaggle?** Every hash below was measured
with `sha256sum`; no bytes were reconstructed.

## Notebooks examined

| Path | Bytes | mtime (local) | SHA-256 of the .ipynb |
| --- | ---: | --- | --- |
| `AutoSecAge/submission_notebook.ipynb` | 34026 | 2026-09-05 18:34:03 | `7254621e0f40e0dd976e49bc8e7ade02aea4c76523fac165000cacc771bb21e8` |
| `AutoSecAge/kaggle_kernel/submission_notebook.ipynb` | 34026 | 2026-09-05 18:34:03 | `7254621e…` (identical copy) |
| `AutoSecAge/kaggle_kernel/kaggle_snapshot/kernel_pull/auto-secage.ipynb` | 27436 | 2026-09-06 10:34:50 | `853df5bdb4e747ce0387378cb325e86782769257e6ab9c9b76580643b11c176e` |
| `~/Downloads/auto-secage.ipynb` | 32887 | 2026-09-06 02:19:19 | `d0b8a915fc21df79ce53d89aa0a868b32985d3504fd986572ce216ce93fc0e50` |
| `~/Downloads/auto-secage (1).ipynb` | 32887 | 2026-09-08 15:39:32 | `d0b8a915…` (identical to the above) |
| `AutoSecAge/working_note.ipynb` | 26768 | 2026-09-06 21:22:25 | `ec8a15b09931f4809486339957ecef5b3da1e82812d8dd08b6e96da006f465ff` |
| `AutoSecAge-3/working_note.ipynb` | 20875 | 2026-09-05 17:29:45 | `ffa141abc41bd0386245fb6848ab1e5b5a0594caa4add778dca07e798fb51105` |
| `AutoSecAge-3/submission_notebook.ipynb` | 34026 | 2026-09-05 18:34:03 | `7254621e…` (identical copy) |

`AutoSecAge-3/` and `AutoSecAge-Repo/` are other local checkouts, scanned for
completeness; they introduced no new module bytes.

## Live kernel pull (2026-09-08)

```
kaggle kernels pull habanwer/auto-secage -p <tmp> --metadata
```

The freshly pulled `auto-secage.ipynb` is **byte-identical** (`cmp` clean,
`853df5bd…`) to the copy stored in `kaggle_kernel/kaggle_snapshot/kernel_pull/`
during the 2026-09-06 gather. Metadata read from `kernel-metadata.json`:

- id `habanwer/auto-secage`, id_no **133239645**, title "Auto-SecAge"
- `is_private: false`, `enable_gpu: true`, `enable_internet: **false**`
- `machine_shape: NvidiaTeslaT4`
- `competition_sources: ["ai-agent-security-multi-step-tool-attacks"]`
- status `KernelWorkerStatus.COMPLETE`, lastRunTime 2026-09-05 15:34:42.860000

`kaggle kernels list --mine` shows exactly one Auto-SecAge kernel.

## Embedded module extracted from each notebook

Extraction rule: for every code cell, take a `%%writefile` payload, or any string
literal / bare cell containing `class AttackAlgorithm` together with `arm_exfil`
or `FROZEN_CASE`. Payloads were written to a scratch dir and hashed.

| Notebook | Cell | How embedded | Bytes | SHA-256 | Identified as |
| --- | ---: | --- | ---: | --- | --- |
| `submission_notebook.ipynb` (all 3 copies) | 1 | `%%writefile` | 23036 | `3b33f018…` | **asa-0001** |
| `kernel_pull/auto-secage.ipynb` | 1 | `%%writefile` | 23036 | `3b33f018…` | **asa-0001** |
| live pull `auto-secage.ipynb` (2026-09-08) | 1 | `%%writefile` | 23036 | `3b33f018…` | **asa-0001** |
| `~/Downloads/auto-secage.ipynb` | 1 | `%%writefile` | 23036 | `3b33f018…` | **asa-0001** |
| `~/Downloads/auto-secage (1).ipynb` | 1 | `%%writefile` | 23036 | `3b33f018…` | **asa-0001** |
| `working_note.ipynb` (both versions) | — | no module cell | — | — | prose + a budget-arithmetic cell only |

First line of every extracted payload: `# Auto-SecAge`. Last line:
`    print(len(cands))`.

## Findings

1. **asa-0002 (`7ee41b12…`) is in no notebook.** Not in any local `.ipynb`, not in
   the notebook currently on Kaggle. Combined with the previous pass (filesystem
   sweep + git blob scan), it was a **lab-only keep** at the time of this
   inventory: never written to a commit or a notebook. The file now at
   `catalogs/asa-0002-exfil/` arrived later (pass 3, Edit-transcript recovery),
   not from this notebook pass.
2. **asa-0003 (`9d49773c…`) is in no notebook either.** It exists only as lab
   HEAD. The repairs were never packaged for Kaggle, which is consistent with
   "not submitted".
3. **Every Kaggle-facing notebook carries asa-0001**, including the notebook that
   is on Kaggle right now. Submission 56036071 therefore ran the *unrepaired*
   catalog — independently confirmed here from the notebook bytes, not just from
   the kernel output file.
4. The extracted cell payload hashes **exactly** to the kernel's output
   `attack.py` (23036 bytes, `3b33f018…`). Notebook cell → worker file →
   downloaded output all agree.
5. One variant is not explained by any notebook on disk: the v1 worker file
   `kaggle_kernel/output/attack.py`, 22393 bytes, `82025cb6…`. No notebook here
   writes those bytes, so it came from an earlier, unretained notebook version.
   Recorded as `kaggle-v1-22393`, **not** as a named keep and **not** as asa-0002.
