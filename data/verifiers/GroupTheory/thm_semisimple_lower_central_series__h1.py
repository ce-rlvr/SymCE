import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

# Top-level setup: named object bindings
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
        G, n = witness
    except Exception:
        return [False, False]

    # H_1: n is an integer greater than or equal to 1
    try:
        h1 = isinstance(n, (int, sympy.Integer)) and n >= 1
    except Exception:
        h1 = False

    # ¬Q: The n-th term of the lower central series, \gamma_n(G), is not equal to G
    try:
        if not isinstance(G, PermutationGroup):
            neg_q = False
        else:
            lcs = G.lower_central_series()
            # \gamma_1(G) is lcs[0], \gamma_2(G) is lcs[1], etc.
            idx = int(n) - 1
            if idx < 0:
                neg_q = False
            else:
                if idx < len(lcs):
                    gamma_n = lcs[idx]
                else:
                    gamma_n = lcs[-1]
                
                # Since gamma_n is a subgroup of G, comparing orders is sufficient for equality
                neg_q = gamma_n.order() != G.order()
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer greater than or equal to 1",
    "¬Q: The n-th term of the lower central series, \\gamma_n(G), is not equal to G"
]

N_HYP = 1
NEG_Q_INDEX = 1