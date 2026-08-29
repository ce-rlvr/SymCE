import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            G, Z = witness
        else:
            G = witness
            Z = G.center() if callable(getattr(G, "center", None)) else G.center
    except Exception:
        return [False, False, False]

    try:
        C = G.center() if callable(getattr(G, "center", None)) else G.center
        h1_ok = bool(Z.is_subgroup(C) and C.is_subgroup(Z))
    except Exception:
        h1_ok = False

    try:
        L = G.lower_central_series() if callable(getattr(G, "lower_central_series", None)) else G.lower_central_series
        h2_ok = bool(L[-1].is_subgroup(Z))
    except Exception:
        h2_ok = False

    try:
        nilp = G.is_nilpotent() if callable(getattr(G, "is_nilpotent", None)) else G.is_nilpotent
        neg_q_ok = (nilp == False)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: Z(G) is the center of G",
    "H_2: The quotient group G/Z(G) is nilpotent",
    "¬Q: G is not a nilpotent group"
]

N_HYP = 2
NEG_Q_INDEX = 2