import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    # H_1: G is a group
    try:
        is_perm_group = isinstance(witness, PermutationGroup)
        is_fp_group = type(witness).__name__ == 'FpGroup'
        is_group = bool(is_perm_group or is_fp_group)
    except Exception:
        is_group = False

    # H_2: G is finitely generated
    try:
        # Both PermutationGroup and FpGroup in SymPy are finitely generated
        is_fg = is_group
    except Exception:
        is_fg = False

    # ¬Q: G is not polycyclic
    try:
        if is_perm_group:
            # For finite groups, polycyclic is equivalent to solvable
            solvable = witness.is_solvable
            if callable(solvable):
                solvable = solvable()
            neg_q = not bool(solvable)
        else:
            # For FpGroup, polycyclicity is not easily decidable in SymPy.
            # We return False to be safe (user should provide a finite non-solvable group like A5).
            neg_q = False
    except Exception:
        neg_q = False

    return [is_group, is_fg, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: G is finitely generated",
    "¬Q: G is not polycyclic"
]

N_HYP = 2
NEG_Q_INDEX = 2