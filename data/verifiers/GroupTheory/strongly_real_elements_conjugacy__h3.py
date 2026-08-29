import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: e is the identity element of G",
    "H_3: g = xy",
    "¬Q: g is not conjugate to its inverse g^-1 in G"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            x = witness.get('x')
            y = witness.get('y')
        elif isinstance(witness, (list, tuple)) and len(witness) >= 3:
            G = witness[0]
            x = witness[1]
            y = witness[2]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H2: e is the identity element of G
    try:
        e = G.identity
        h2 = h1 and (e is not None)
    except Exception:
        h2 = False

    # H3: g = xy
    try:
        h3 = (x in G) and (y in G)
        g = x * y
    except Exception:
        h3 = False

    # neg_Q: g is not conjugate to g^-1 in G
    try:
        g_inv = g**-1
        is_conj = False
        for c in G.generate():
            if c * g * c**-1 == g_inv:
                is_conj = True
                break
        neg_q = not is_conj
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]