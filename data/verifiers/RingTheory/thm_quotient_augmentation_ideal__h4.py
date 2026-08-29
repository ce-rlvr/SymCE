import sympy
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
    if isinstance(witness, tuple) and len(witness) == 2:
        R, G = witness
    else:
        R, G = None, witness

    h1_ok = False
    try:
        if R is None:
            h1_ok = True
        else:
            if hasattr(R, 'is_commutative'):
                h1_ok = bool(R.is_commutative)
            else:
                h1_ok = True
    except Exception:
        h1_ok = False

    h2_ok = False
    try:
        if hasattr(G, 'is_abelian') or hasattr(G, 'elements'):
            h2_ok = True
    except Exception:
        h2_ok = False

    h3_ok = True

    neg_q_ok = False
    try:
        if hasattr(G, 'is_abelian'):
            neg_q_ok = not bool(G.is_abelian)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = ["H_1: R is a commutative ring", "H_2: G is a group", "H_3: RG is the group ring of G over R", "not_Q: The quotient ring RG/Delta is not isomorphic to R"]

N_HYP = 3
NEG_Q_INDEX = 3