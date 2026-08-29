import math
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # Klein four-group
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

CONDITION_LABELS = [
    "H_1: S_n is the symmetric group on n letters",
    "H_2: H is a subgroup of S_n",
    "H_3: The index of H in S_n is exactly n",
    "¬Q: The subgroup H is not isomorphic to the symmetric group S_{n-1}"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness) -> list[bool]:
    # Extract n and H from the witness
    try:
        if isinstance(witness, tuple):
            n, H = witness
        else:
            H = witness
            n = H.degree
    except Exception:
        return [False, False, False, False]

    # H_1: n is a positive integer
    try:
        h1 = int(n) == n and n >= 1
    except Exception:
        h1 = False

    # H_2: H is a subgroup of S_n
    try:
        h2 = isinstance(H, PermutationGroup) and H.degree <= n
    except Exception:
        h2 = False

    # H_3: The index of H in S_n is exactly n
    try:
        h3 = math.factorial(int(n)) == int(n) * H.order()
    except Exception:
        h3 = False

    # ¬Q: H is not isomorphic to S_{n-1}
    try:
        n_int = int(n)
        k = n_int - 1
        is_iso = False
        
        # Check if H is isomorphic to S_k
        if k >= 1 and H.order() == math.factorial(k):
            if k == 1 or k == 2:
                is_iso = True
            elif k == 3:
                is_iso = not H.is_abelian
            elif k == 4:
                # S4 is the unique group of order 24 with a trivial center
                is_iso = (H.center().order() == 1)
            elif k == 5:
                # S5 is the unique group of order 120 with a trivial center that is not solvable
                is_iso = (H.center().order() == 1) and not H.is_solvable
            elif k == 6:
                # Distinguish S6 from PGL2(9) and M10
                has_6 = any(g.order() == 6 for g in H.elements)
                has_8 = any(g.order() == 8 for g in H.elements)
                is_iso = (H.center().order() == 1) and not H.is_solvable and has_6 and not has_8
            else:
                # For k >= 7, S_k has trivial center and derived subgroup of index 2
                is_iso = (H.center().order() == 1) and (H.derived_subgroup().order() == math.factorial(k) // 2)
                
        neg_q = not is_iso
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]