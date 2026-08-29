import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
)

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
Z = sympy.S.Integers

def conditions(witness) -> list[bool]:
    if isinstance(witness, dict):
        G = witness.get('G')
        H = witness.get('H')
    elif isinstance(witness, (tuple, list)) and len(witness) == 2:
        G, H = witness
    else:
        return [False, False]

    def is_group(grp):
        if grp is None:
            return False
        if isinstance(grp, PermutationGroup):
            return True
        if grp == sympy.S.Integers:
            return True
        t_name = type(grp).__name__
        if t_name in ('FreeGroup', 'FpGroup'):
            return True
        return False

    def is_locally_finite(grp):
        if not is_group(grp):
            return False
        if isinstance(grp, PermutationGroup):
            return True
        if grp == sympy.S.Integers:
            return False
        t_name = type(grp).__name__
        if t_name == 'FreeGroup':
            return len(grp.generators) == 0
        if t_name == 'FpGroup':
            try:
                return grp.order() != sympy.oo
            except Exception:
                return False
        return False

    try:
        h1 = is_locally_finite(G)
    except Exception:
        h1 = False

    try:
        if not is_group(H):
            neg_q = False
        else:
            neg_q = not (is_locally_finite(G) and is_locally_finite(H))
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a locally finite group",
    "¬Q: The direct product G x H is not a locally finite group"
]

N_HYP = 1
NEG_Q_INDEX = 1