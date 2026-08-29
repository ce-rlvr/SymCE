import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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
    # H_1: n is a non-negative integer
    try:
        G, n = witness
        h1 = isinstance(n, (int, sympy.Integer)) and n >= 0
    except Exception:
        h1 = False

    # ¬Q: The n-th term of the derived series G^{(n)} is not equal to G
    try:
        G, n = witness
        if not (isinstance(n, (int, sympy.Integer)) and n >= 0):
            neg_q = False
        else:
            n_int = int(n)
            series = G.derived_series()
            if n_int < len(series):
                curr = series[n_int]
            else:
                curr = series[-1]
            neg_q = curr.order() != G.order()
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: n is a non-negative integer",
    "¬Q: The n-th term of the derived series G^{(n)} is not equal to G"
]

N_HYP = 1
NEG_Q_INDEX = 1