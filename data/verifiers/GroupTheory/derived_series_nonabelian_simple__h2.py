import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
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

def conditions(witness):
    # H_1: G is a non-abelian simple group
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G = witness[0]
        else:
            G = witness
            
        is_ab = G.is_abelian
        if callable(is_ab):
            is_ab = is_ab()
            
        is_simp = G.is_simple
        if callable(is_simp):
            is_simp = is_simp()
            
        h1_ok = bool((not is_ab) and is_simp)
    except Exception:
        h1_ok = False

    # ¬Q: The n-th term of the derived series G^{(n)} is not equal to G
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, n = witness
            series = G.derived_series()
            if n < len(series):
                nth = series[n]
            else:
                nth = series[-1]
            neg_q_ok = bool(nth.order() != G.order())
        else:
            G = witness
            series = G.derived_series()
            neg_q_ok = bool(series[-1].order() != G.order())
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a non-abelian simple group",
    "¬Q: The n-th term of the derived series G^{(n)} is not equal to G"
]

N_HYP = 1
NEG_Q_INDEX = 1