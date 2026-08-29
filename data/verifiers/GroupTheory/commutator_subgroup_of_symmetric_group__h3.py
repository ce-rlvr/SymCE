import sympy
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

def conditions(witness):
    try:
        if not isinstance(witness, (int, sympy.Integer)):
            h1 = False
        else:
            n = int(witness)
            h1 = (n >= 2)
    except Exception:
        h1 = False

    try:
        h2 = h1
    except Exception:
        h2 = False

    try:
        if h1 and h2:
            n = int(witness)
            Sn = SymmetricGroup(n)
            An = AlternatingGroup(n)
            comm = Sn.derived_subgroup()
            q = comm.is_subgroup(An) and An.is_subgroup(comm)
            neg_q = not q
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer such that n >= 2",
    "H_2: S_n is the symmetric group of degree n",
    "¬Q: The commutator subgroup of S_n is not equal to A_n"
]

N_HYP = 2
NEG_Q_INDEX = 2