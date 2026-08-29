import math
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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
    if isinstance(witness, tuple) and len(witness) == 2:
        n, H = witness
    else:
        H = witness
        try:
            n = H.degree
        except Exception:
            return [False, False, False, False]
            
    try:
        n_val = int(n)
        h1 = n_val >= 5
        n = n_val
    except Exception:
        h1 = False
        
    try:
        h2 = isinstance(H, PermutationGroup) and H.degree <= n
    except Exception:
        h2 = False
        
    try:
        h3 = math.factorial(n) == n * int(H.order())
    except Exception:
        h3 = False
        
    try:
        is_iso = False
        if int(H.order()) == math.factorial(n-1):
            if int(H.center().order()) == 1:
                if int(H.derived_subgroup().order()) == math.factorial(n-1) // 2:
                    is_iso = True
                    # Distinguish S_6 from M_10 and PGL(2, 9) for n=7
                    if n == 7:
                        orders = set(g.order() for g in H.elements)
                        if 8 in orders or 10 in orders:
                            is_iso = False
        neg_q = not is_iso
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: n >= 5 is an integer",
    "H_2: H is a subgroup of S_n",
    "H_3: The index of H in S_n is exactly n",
    "¬Q: H is not isomorphic to S_{n-1}"
]

N_HYP = 3
NEG_Q_INDEX = 3