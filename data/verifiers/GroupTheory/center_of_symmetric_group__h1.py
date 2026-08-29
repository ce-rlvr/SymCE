import math
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics import PermutationGroup

S2 = SymmetricGroup(2)
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
    is_n = False
    n = None
    try:
        n_val = int(witness)
        if n_val == witness:
            is_n = True
            n = n_val
    except Exception:
        pass

    is_group = False
    try:
        if isinstance(witness, PermutationGroup):
            is_group = True
    except Exception:
        pass

    # H_1: witness is a valid degree n >= 1, or a symmetric group
    h1 = False
    try:
        if is_n:
            h1 = bool(n >= 1)
        elif is_group:
            degree = witness.degree
            order = witness.order()
            h1 = bool(math.factorial(degree) == order and degree >= 1)
    except Exception:
        h1 = False

    # ¬Q: The center of S_n is not the trivial subgroup
    neg_q = False
    try:
        if is_n:
            if 1 <= n <= 100:
                G = SymmetricGroup(n)
                neg_q = bool(G.center().order() > 1)
        elif is_group:
            neg_q = bool(witness.center().order() > 1)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: S_n is the symmetric group of degree n",
    "¬Q: The center of S_n is not the trivial subgroup"
]

N_HYP = 1
NEG_Q_INDEX = 1