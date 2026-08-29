import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy import eye, zeros

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
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
    # Parse witness: can be either (G, d) or just G
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, d = witness
        else:
            G = witness
            d = len(G.derived_series()) - 1
    except Exception:
        return [False, False, False]
        
    # H_1: d is the derived length of G
    try:
        h1 = (d == len(G.derived_series()) - 1)
    except Exception:
        h1 = False
        
    # H_2: d >= 1
    try:
        h2 = (d >= 1)
    except Exception:
        h2 = False
        
    # ¬Q: The (d-1)-th derived subgroup G^{(d-1)} is a non-trivial abelian normal subgroup of G.
    try:
        derived_series = G.derived_series()
        if not (0 <= d - 1 < len(derived_series)):
            # If the index is out of bounds, the conclusion fails
            neg_q = True
        else:
            H = derived_series[d - 1]
            
            try:
                order = H.order()
            except TypeError:
                order = H.order
                
            is_non_trivial = (order > 1)
            is_abelian = bool(H.is_abelian)
            is_normal = bool(H.is_normal(G))
            
            q = is_non_trivial and is_abelian and is_normal
            neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: d is the derived length of G",
    "H_2: d >= 1",
    "¬Q: G^{(d-1)} is not a non-trivial abelian normal subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2