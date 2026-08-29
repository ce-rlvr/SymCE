import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.free_groups import FreeGroup, free_group

# Standard group theory objects
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

# Free groups for potential witnesses
F1 = free_group("x")[0]
F2 = free_group("x, y")[0]

def conditions(witness) -> list[bool]:
    # H_1: F is a free group
    try:
        h1 = isinstance(witness, FreeGroup)
    except Exception:
        h1 = False

    # ¬Q: F is a nilpotent group
    try:
        if isinstance(witness, FreeGroup):
            # A free group is nilpotent if and only if its rank is 0 or 1
            neg_q = witness.rank <= 1
        elif hasattr(witness, 'is_nilpotent'):
            if callable(witness.is_nilpotent):
                neg_q = bool(witness.is_nilpotent())
            else:
                neg_q = bool(witness.is_nilpotent)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: F is a free group",
    "¬Q: F is a nilpotent group"
]

N_HYP = 1
NEG_Q_INDEX = 1