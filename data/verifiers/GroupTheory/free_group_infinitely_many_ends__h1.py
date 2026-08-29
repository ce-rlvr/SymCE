import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.combinatorics.free_groups import FreeGroup
from sympy import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: The rank of F is at least 2",
    "¬Q: F does not have infinitely many ends"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    # H_1: The rank of F is at least 2
    try:
        if hasattr(witness, 'rank'):
            if callable(witness.rank):
                r = witness.rank()
            else:
                r = witness.rank
            h1 = bool(r >= 2)
        else:
            h1 = False
    except Exception:
        h1 = False

    # ¬Q: F does not have infinitely many ends
    try:
        # In SymPy, only FreeGroups of rank >= 2 have infinitely many ends.
        # Other objects (like matrices or finite permutation groups) do not.
        if isinstance(witness, FreeGroup):
            if callable(witness.rank):
                r = witness.rank()
            else:
                r = witness.rank
            has_inf_ends = bool(r >= 2)
        else:
            has_inf_ends = False
            
        neg_q = not has_inf_ends
    except Exception:
        neg_q = False

    return [h1, neg_q]