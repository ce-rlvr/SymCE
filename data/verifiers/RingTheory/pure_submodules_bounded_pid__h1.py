import sympy
from sympy.abc import x, y, z

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get("is_bounded_module", False))
        else:
            h1 = bool(getattr(witness, "is_bounded_module", False))
    except Exception:
        h1 = False

    try:
        if isinstance(witness, dict):
            h2 = bool(witness.get("is_pure_submodule", False))
        else:
            h2 = bool(getattr(witness, "is_pure_submodule", False))
    except Exception:
        h2 = False

    try:
        if isinstance(witness, dict):
            has_q = "is_direct_summand" in witness
            q = bool(witness.get("is_direct_summand", True))
        else:
            has_q = hasattr(witness, "is_direct_summand")
            q = bool(getattr(witness, "is_direct_summand", True))
        
        neg_q = has_q and (not q)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: M is a bounded R-module",
    "H_2: N is a pure submodule of M",
    "¬Q: N is not a direct summand of M"
]

N_HYP = 2
NEG_Q_INDEX = 2