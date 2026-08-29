import sympy
from sympy.combinatorics import free_group
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

# Free groups
try:
    res1 = free_group("x")
    F1 = res1[0]
    FreeGroupType = type(F1)
    
    res2 = free_group("x, y")
    F2 = res2[0]
    
    res3 = free_group("x, y, z")
    F3 = res3[0]
except Exception:
    F1 = None
    F2 = None
    F3 = None
    FreeGroupType = type(None)

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    """
    try:
        # H_1: F is a free group
        if isinstance(witness, FreeGroupType):
            h1 = True
        elif type(witness).__name__ == 'FpGroup' and len(getattr(witness, 'relators', [])) == 0:
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False

    try:
        # ¬Q: F is not isomorphic to the infinite cyclic group Z
        # A free group is isomorphic to Z if and only if its rank (number of generators) is exactly 1.
        if h1:
            if hasattr(witness, 'rank'):
                neg_q = witness.rank != 1
            elif hasattr(witness, 'generators'):
                neg_q = len(witness.generators) != 1
            else:
                neg_q = False
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: F is a free group",
    "¬Q: F is not isomorphic to the infinite cyclic group Z"
]

N_HYP = 1
NEG_Q_INDEX = 1