# kaggle/

Facts about the two submissions. No leaderboard claims.

- **v1 → submission 56035703 → `ERROR`, empty scores.** The notebook never called
  `JEDAttackInferenceServer().serve()`. The official harness loads
  `/kaggle/working/attack.py` over gRPC and reports a failure when the server
  never starts. The Save Version run had been green, which is misleading: the
  commit phase does not serve.
- **v2 → submission 56036071 → `COMPLETE`, public `0.00000`, private `0.00000`.**
  The last cell calls `JEDAttackInferenceServer().serve()` guarded on
  `KAGGLE_IS_COMPETITION_RERUN`. See `serve-cell.md`.
- `env_probe = False` in the FrozenCase, so generation issues no `RemoteEnv` RPCs
  and the static catalog is the scored path.
- The catalog inside that notebook is **asa-0001**
  (`3b33f018342444f3e959b3849de09b7b864a398ff9e593243b45ea626f1a92ea`).
  The asa-0002 / asa-0003 repairs in this repo were **never submitted**.

Both submissions are **late and unofficial** — the scored deadline was
2026-09-01. The zeros are the strings the API returned. A COMPLETE zero is not a
timeout: an overrun fails without any score at all.

## Which kernel version holds which catalog (verified 2026-09-08)

A live `kaggle kernels pull habanwer/auto-secage --metadata` returned a notebook
byte-identical (`853df5bd…`) to the copy captured on 2026-09-06. Its cell 1
`%%writefile` payload hashes to
`3b33f018342444f3e959b3849de09b7b864a398ff9e593243b45ea626f1a92ea` — **asa-0001**,
23036 bytes.

So the kernel currently on Kaggle still carries the **unrepaired** catalog. The
asa-0002 / asa-0003 repairs live only in the lab and were never pushed. Kernel
metadata at that pull: id_no 133239645, `enable_internet: false`,
`enable_gpu: true`, `NvidiaTeslaT4`, competition source attached, status COMPLETE,
lastRunTime 2026-09-05 15:34:42.860000.

The v1 worker file (22393 bytes, `82025cb6…`, `catalogs/kaggle-v1-22393/`) is from
the earlier notebook version behind the ERROR submission; that version was not
retained locally.
