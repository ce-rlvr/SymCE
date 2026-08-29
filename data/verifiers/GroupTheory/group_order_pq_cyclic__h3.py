import sympy
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G = witness['G']
            p = witness['p']
            q = witness['q']
        else:
            G, p, q = witness
    except Exception:
        return [False, False, False, False]

    try:
        h1 = bool(sympy.isprime(p) and sympy.isprime(q))
    except Exception:
        h1 = False

    try:
        h2 = bool(p < q)
    except Exception:
        h2 = False

    try:
        h3 = bool((q - 1) % p != 0)
    except Exception:
        h3 = False

    try:
        if hasattr(G, 'is_cyclic'):
            neg_q = not bool(G.is_cyclic)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: p and q are prime numbers",
    "H_2: p < q",
    "H_3: p does not divide q - 1",
    "¬Q: G is not a cyclic group"
]

N_HYP = 3
NEG_Q_INDEX = 3