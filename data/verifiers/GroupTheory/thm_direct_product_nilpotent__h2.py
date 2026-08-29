import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics import DirectProduct
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

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False]
        G, H = witness
    except Exception:
        return [False, False]

    try:
        nilp_G = G.is_nilpotent
        if callable(nilp_G):
            h1_ok = bool(nilp_G())
        else:
            h1_ok = bool(nilp_G)
    except Exception:
        h1_ok = False

    try:
        GxH = DirectProduct(G, H)
        nilp_GxH = GxH.is_nilpotent
        if callable(nilp_GxH):
            neg_q_ok = not bool(nilp_GxH())
        else:
            neg_q_ok = not bool(nilp_GxH)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a nilpotent group",
    "¬Q: The direct product G x H is not a nilpotent group"
]

N_HYP = 1
NEG_Q_INDEX = 1