import math
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy import eye, zeros, Integer

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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # Parse witness: can be a tuple (n, H) or just H
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            n, H = witness
        else:
            H = witness
            n = max(5, getattr(H, 'degree', 5))
    except Exception:
        return [False, False, False, False]
        
    # H_1: n >= 5 is an integer
    try:
        h1 = int(n) == n and n >= 5
    except Exception:
        h1 = False
        
    # H_2: S_n is the symmetric group on n letters
    # This is a definitional hypothesis, so it holds by definition in our context.
    try:
        h2 = True
    except Exception:
        h2 = False
        
    # H_3: H is a subgroup of S_n
    try:
        h3 = isinstance(H, PermutationGroup) and H.degree <= n
    except Exception:
        h3 = False
        
    # neg_Q: H is not isomorphic to S_{n-1}
    try:
        is_iso = False
        if h1 and h3:
            target_order = math.factorial(int(n) - 1)
            if H.order() == target_order:
                try:
                    # Attempt to use sympy's built-in isomorphism checker
                    is_iso = H.is_isomorphic(SymmetricGroup(int(n) - 1))
                except Exception:
                    # Fallback heuristic for S_k if is_isomorphic is unavailable or fails
                    k = int(n) - 1
                    if k == 4:
                        is_iso = (H.center().order() == 1 and H.derived_subgroup().order() == 12)
                    elif k >= 5:
                        is_iso = (H.center().order() == 1 and H.derived_subgroup().order() == math.factorial(k) // 2)
                    else:
                        is_iso = True
        neg_q = not is_iso
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: n >= 5 is an integer",
    "H_2: S_n is the symmetric group on n letters",
    "H_3: H is a subgroup of S_n",
    "¬Q: H is not isomorphic to S_{n-1}"
]

N_HYP = 3
NEG_Q_INDEX = 3