import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

Z = sympy.S.Integers
Q = sympy.S.Rationals
R = sympy.S.Reals
C = sympy.S.Complexes

def conditions(witness) -> list[bool]:
    # H_1: G is a group
    try:
        if isinstance(witness, PermutationGroup):
            h1 = True
        elif witness in (Z, Q, R, C):
            h1 = True
        elif isinstance(witness, tuple) and len(witness) > 0 and all(w in (Z, Q, R, C) for w in witness):
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False

    # H_2: G is infinite
    try:
        h2 = False
        if isinstance(witness, PermutationGroup):
            h2 = False
        elif witness in (Z, Q, R, C):
            h2 = True
        elif isinstance(witness, tuple) and len(witness) > 0 and all(w in (Z, Q, R, C) for w in witness):
            h2 = True
    except Exception:
        h2 = False

    # ¬Q: G is NOT isomorphic to the additive group of integers Z
    try:
        is_Z = False
        if isinstance(witness, PermutationGroup):
            is_Z = False
        elif witness == Z:
            is_Z = True
        elif witness in (Q, R, C):
            is_Z = False
        elif isinstance(witness, tuple) and len(witness) > 0 and all(w in (Z, Q, R, C) for w in witness):
            if len(witness) == 1 and witness[0] == Z:
                is_Z = True
            else:
                is_Z = False
            
        neg_q = not is_Z
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: G is infinite",
    "¬Q: G is not isomorphic to the additive group of integers Z"
]

N_HYP = 2
NEG_Q_INDEX = 2