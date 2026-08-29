import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    try:
        n = int(witness)
        h1 = (n == witness) and (n >= 1)
    except Exception:
        h1 = False

    try:
        if h1:
            Sn = SymmetricGroup(n)
            An = AlternatingGroup(n)
            comm = Sn.derived_subgroup()
            is_equal = (comm.order() == An.order()) and all((g in An) for g in comm.generators)
            neg_q = not is_equal
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is a valid degree for a symmetric group",
    "not Q: The commutator subgroup of S_n is not equal to A_n"
]

N_HYP = 1
NEG_Q_INDEX = 1