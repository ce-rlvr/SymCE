import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import (SymmetricGroup, AlternatingGroup,
                                              DihedralGroup, CyclicGroup)
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: G is a nilpotent group
    try:
        if hasattr(witness, 'is_nilpotent'):
            val = witness.is_nilpotent
            h1 = bool(val() if callable(val) else val)
        elif hasattr(witness, 'is_nilpotent_group'):
            val = witness.is_nilpotent_group
            h1 = bool(val() if callable(val) else val)
        elif hasattr(witness, 'is_abelian'):
            val = witness.is_abelian
            h1 = bool(val() if callable(val) else val)
        else:
            h1 = False
    except Exception:
        h1 = False

    # neg_Q: G is NOT finitely presented
    try:
        if hasattr(witness, 'is_finitely_presented'):
            val = witness.is_finitely_presented
            is_fp = bool(val() if callable(val) else val)
        elif isinstance(witness, PermutationGroup):
            is_fp = True
        elif type(witness).__name__ == 'FpGroup':
            is_fp = True
        elif type(witness).__name__ == 'FreeGroup':
            is_fp = len(witness.generators) < float('inf')
        else:
            # If we cannot determine, assume it is finitely presented to avoid false positives
            is_fp = True
            
        neg_q = not is_fp
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a nilpotent group",
    "¬Q: G is not finitely presented"
]

N_HYP = 1
NEG_Q_INDEX = 1