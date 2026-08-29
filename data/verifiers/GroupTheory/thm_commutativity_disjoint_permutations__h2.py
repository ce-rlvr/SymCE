import sympy
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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
        h1 = (isinstance(witness, (tuple, list)) and len(witness) == 2 and
              isinstance(witness[0], Permutation) and isinstance(witness[1], Permutation))
    except Exception:
        h1 = False

    try:
        if h1:
            sigma, tau = witness
            neg_q = bool(sigma * tau != tau * sigma)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: sigma and tau are two permutations",
    "¬Q: sigma and tau do not commute"
]

N_HYP = 1
NEG_Q_INDEX = 1