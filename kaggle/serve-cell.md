# The JED serve cell

Quoted from the lab's `kaggle_kernel/submission_notebook.ipynb`. Only the two
cells that matter for the gateway are reproduced; the worker notebook itself is
not distributed here.

## Dry-run guard (cell 4)

```python
import os
import importlib.util
from pathlib import Path

if os.getenv("KAGGLE_IS_COMPETITION_RERUN"):
    print("rerun: skip local dry-run; inference server loads /kaggle/working/attack.py")
else:
    p = Path("/kaggle/working/attack.py")
    spec = importlib.util.spec_from_file_location("auto_secage_attack", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    cands = mod.AttackAlgorithm().run(None, None)
    print("n_candidates", len(cands))
    print("first_hops", len(cands[0].user_messages) if cands else 0)
```

## The serve cell (cell 5) — this is what v1 was missing

```python
import os

if os.getenv('KAGGLE_IS_COMPETITION_RERUN'):
    from kaggle_evaluation.jed_attack_134815.jed_attack_inference_server import (
        JEDAttackInferenceServer,
    )
    # Official harness. serve() blocks until the gateway finishes.
    JEDAttackInferenceServer().serve()
else:
    print('commit run: not serving (gateway only on competition rerun)')
```

`serve()` runs **only** on the competition rerun. On a Save Version / commit run
the else-branch prints and exits, which is why a green commit log is not evidence
that scoring will work.
