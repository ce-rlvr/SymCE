import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def is_virtually_free(G):
    if type(G).__name__ == 'FreeGroup':
        return True
    if hasattr(G, "order"):
        try:
            o = G.order()
            if o != sympy.oo:
                return True
        except Exception:
            pass
    if hasattr(G, "relators"):
        try:
            if len(G.relators) == 0:
                return True
        except Exception:
            pass
    return False

def is_torsion_free(G):
    if type(G).__name__ == 'FreeGroup':
        return True
    if hasattr(G, "order"):
        try:
            o = G.order()
            if o != sympy.oo:
                return o == 1
        except Exception:
            pass
    if hasattr(G, "relators"):
        try:
            if len(G.relators) == 0:
                return True
        except Exception:
            pass
    return False

def is_free(G):
    if type(G).__name__ == 'FreeGroup':
        return True
    if hasattr(G, "order"):
        try:
            o = G.order()
            if o != sympy.oo:
                return o == 1
        except Exception:
            pass
    if hasattr(G, "relators"):
        try:
            if len(G.relators) == 0:
                return True
        except Exception:
            pass
    return False

def conditions(witness):
    try:
        h1 = bool(is_virtually_free(witness))
    except Exception:
        h1 = False

    try:
        h2 = bool(is_torsion_free(witness))
    except Exception:
        h2 = False

    try:
        q = bool(is_free(witness))
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is virtually free",
    "H_2: G is torsion-free",
    "¬Q: G is not a free group"
]

N_HYP = 2
NEG_Q_INDEX = 2