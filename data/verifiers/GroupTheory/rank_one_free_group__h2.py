import sympy
from sympy.combinatorics.free_groups import FreeGroup, free_group
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
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
    F = None
    S = None
    
    try:
        if isinstance(witness, dict):
            F = witness.get('F')
            S = witness.get('S')
        elif hasattr(witness, 'F') and hasattr(witness, 'S'):
            F = witness.F
            S = witness.S
        else:
            F, S = witness
    except Exception:
        pass

    # H_1: Let F be a free group
    try:
        h1 = isinstance(F, FreeGroup)
    except Exception:
        h1 = False

    # H_2: Assume the cardinality of S is exactly 1
    try:
        h2 = hasattr(S, '__len__') and len(S) == 1
    except Exception:
        h2 = False

    # ¬Q: F is NOT isomorphic to the additive group of integers Z
    # A free group is isomorphic to Z if and only if its rank (number of generators) is exactly 1.
    try:
        if isinstance(F, FreeGroup):
            is_iso_Z = (len(F.generators) == 1)
        else:
            is_iso_Z = False
        neg_q = not is_iso_Z
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a free group",
    "H_2: The cardinality of S is exactly 1",
    "¬Q: F is not isomorphic to Z"
]

N_HYP = 2
NEG_Q_INDEX = 2