import sympy
from sympy import Symbol, Poly
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
    "H_1: f(x) is x^6 + x^3 + 1",
    "¬Q: The degree of the splitting field is not 6, or its Galois group over Q is not C_6"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    x = Symbol('x')
    h1 = False
    neg_q = False
    
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                f, deg, G = witness
                h1 = bool(f == x**6 + x**3 + 1 or f == Poly(x**6 + x**3 + 1, x))
                neg_q = not (deg == 6 and G.is_isomorphic(Z6))
                return [h1, neg_q]
            elif len(witness) == 2:
                deg, G = witness
                h1 = True
                neg_q = not (deg == 6 and G.is_isomorphic(Z6))
                return [h1, neg_q]
    except Exception:
        pass

    try:
        if hasattr(witness, 'degree') and hasattr(witness, 'galois_group'):
            h1 = bool(witness == x**6 + x**3 + 1 or witness == Poly(x**6 + x**3 + 1, x))
            deg = witness.degree() if callable(witness.degree) else witness.degree
            G = witness.galois_group() if callable(witness.galois_group) else witness.galois_group
            neg_q = not (deg == 6 and G.is_isomorphic(Z6))
            return [h1, neg_q]
    except Exception:
        pass

    try:
        f = witness
        h1 = bool(f == x**6 + x**3 + 1 or f == Poly(x**6 + x**3 + 1, x))
    except Exception:
        h1 = False

    if h1:
        neg_q = False
    else:
        neg_q = True

    return [h1, neg_q]