import sympy
from sympy.combinatorics import free_group
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

try:
    F1 = free_group("x")[0]
    F2 = free_group("x, y")[0]
    F3 = free_group("x, y, z")[0]
except Exception:
    pass

def conditions(witness) -> list[bool]:
    try:
        h1 = type(witness).__name__ in ('FreeGroup', 'FpGroup')
        if h1 and type(witness).__name__ == 'FpGroup':
            h1 = len(witness.relators) == 0
    except Exception:
        h1 = False

    try:
        if h1:
            neg_q = len(witness.generators) == 1
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: F is a free group on a set S",
    "¬Q: The center of F is not the trivial subgroup"
]

N_HYP = 1
NEG_Q_INDEX = 1