import sympy
from sympy import oo
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        G, N = witness
    except Exception:
        return [False, False, False, False]

    # H1: N is a normal subgroup of G
    try:
        h1 = bool(N.is_subgroup(G) and N.is_normal(G))
    except Exception:
        h1 = False

    # H2: N is a finite group
    try:
        if hasattr(N, 'is_finite') and N.is_finite is not None:
            h2 = bool(N.is_finite)
        else:
            h2 = bool(N.order() < oo)
    except Exception:
        h2 = False

    # H3: The quotient group G/N is a finite group
    try:
        if hasattr(G, 'index'):
            idx = G.index(N)
            h3 = bool(idx < oo)
        else:
            o_G = G.order()
            o_N = N.order()
            if o_G == oo and o_N < oo:
                h3 = False
            elif o_G < oo and o_N < oo:
                h3 = True
            else:
                h3 = False
    except Exception:
        h3 = False

    # neg_Q: G is NOT a finite group
    try:
        if hasattr(G, 'is_finite') and G.is_finite is not None:
            neg_q = not bool(G.is_finite)
        else:
            neg_q = bool(G.order() == oo)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "H_2: N is a finite group",
    "H_3: The quotient group G/N is a finite group",
    "¬Q: G is not a finite group"
]

N_HYP = 3
NEG_Q_INDEX = 3