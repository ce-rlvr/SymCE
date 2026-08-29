import sympy
from sympy.combinatorics.named_groups import CyclicGroup
from sympy.matrices import eye, zeros

Z2 = CyclicGroup(2)
I2 = eye(2)
O2 = zeros(2, 2)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get("is_finitely_generated", False))
            h2 = bool(witness.get("is_flat", False))
            q = bool(witness.get("is_projective", True))
        else:
            h1 = bool(getattr(witness, "is_finitely_generated", False))
            h2 = bool(getattr(witness, "is_flat", False))
            q = bool(getattr(witness, "is_projective", True))
    except Exception:
        h1 = False
        h2 = False
        q = True
        
    return [h1, h2, not q]

CONDITION_LABELS = [
    "H_1: M is a finitely generated R-module",
    "H_2: M is a flat R-module",
    "¬Q: M is not a projective R-module"
]

N_HYP = 2
NEG_Q_INDEX = 2