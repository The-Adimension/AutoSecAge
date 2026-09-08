# Auto-SecAge
# Shehab Anwer, MD (habanwer) — The Adimension
# REDACTS × Agent-ProSAT × autoresearch-MIL
#
# REDACTS-style threat base: four predicate arms as auditable scanners.
# Canonical generators live in attack.py (the scored Kaggle file) so the
# notebook and this lab catalog cannot drift. Re-export only.

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from attack import (  # noqa: E402
    arm_deputy,
    arm_destructive,
    arm_exfil,
    arm_untrusted,
)

ARM_NAMES = ("exfil", "deputy", "destructive", "untrusted")

__all__ = [
    "ARM_NAMES",
    "arm_exfil",
    "arm_deputy",
    "arm_destructive",
    "arm_untrusted",
]
