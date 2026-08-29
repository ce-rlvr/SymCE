import sympy
from sympy.combinatorics import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, free_group
)
from sympy import ZZ

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

try:
    Z_inf, (a,) = free_group("a")
except Exception:
    Z_inf = ZZ
    a = 1

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            e = witness.get('e')
            x = witness.get('x')
        else:
            G, e, x = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is an infinite cyclic group
    try:
        if G == ZZ:
            h1_ok = True
        elif type(G).__name__ == 'FreeGroup':
            h1_ok = (len(G.generators) == 1)
        elif type(G).__name__ == 'FpGroup':
            h1_ok = (len(G.generators) == 1 and len(G.relators) == 0)
        else:
            h1_ok = False
    except Exception:
        h1_ok = False

    # H_2: e is the identity element of G
    try:
        if G == ZZ:
            h2_ok = (e == 0)
        else:
            h2_ok = (e == G.identity)
    except Exception:
        h2_ok = False

    # H_3: x is an element of G
    try:
        if G == ZZ:
            h3_ok = (x in ZZ)
        else:
            h3_ok = (x in G)
    except Exception:
        h3_ok = False

    # ¬Q: x is not equal to the identity element e
    try:
        neg_q_ok = (x != e)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is an infinite cyclic group",
    "H_2: e is the identity element of G",
    "H_3: x is an element of G",
    "¬Q: x is not equal to the identity element e"
]

N_HYP = 3
NEG_Q_INDEX = 3