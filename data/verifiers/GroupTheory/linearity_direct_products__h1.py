import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, PermutationGroup
from sympy.matrices import eye, zeros

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

CONDITION_LABELS = [
    "H_1: G is a group isomorphic to a subgroup of GL_n(F)",
    "H_2: H is a group isomorphic to a subgroup of GL_m(F)",
    "¬Q: G x H is not isomorphic to a subgroup of GL_{n+m}(F)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def GL_order(n, q):
    if n < 0:
        return 0
    if n == 0:
        return 1
    order = q**(n*(n-1)//2)
    for i in range(1, n+1):
        order *= (q**i - 1)
    return order

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple):
            if len(witness) >= 5:
                G, H, n, m, F = witness[:5]
            elif len(witness) == 4:
                G, H, n, m = witness
                F = None
            elif len(witness) == 2:
                G, H = witness
                n, m, F = None, None, None
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    h1 = False
    try:
        if isinstance(G, PermutationGroup) or hasattr(G, 'order'):
            h1 = True
            if isinstance(n, int) and isinstance(F, int):
                order = G.order() if callable(G.order) else G.order
                if order > 0 and GL_order(n, F) % order != 0:
                    h1 = False
        elif isinstance(G, list) and len(G) > 0 and all(hasattr(g, 'det') for g in G):
            h1 = True
    except Exception:
        pass

    h2 = False
    try:
        if isinstance(H, PermutationGroup) or hasattr(H, 'order'):
            h2 = True
            if isinstance(m, int) and isinstance(F, int):
                order = H.order() if callable(H.order) else H.order
                if order > 0 and GL_order(m, F) % order != 0:
                    h2 = False
        elif isinstance(H, list) and len(H) > 0 and all(hasattr(h, 'det') for h in H):
            h2 = True
    except Exception:
        pass

    # The conclusion is that G x H is isomorphic to a subgroup of GL_{n+m}(F).
    # This is mathematically always true via the block diagonal embedding.
    # Therefore, the conclusion never fails, and its negation is always False.
    neg_q = False

    return [h1, h2, neg_q]