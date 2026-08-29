import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        G, H = witness
    except Exception:
        return [False, False, False]

    # H_1: G is a nilpotent group
    try:
        h1 = bool(G.is_nilpotent)
    except Exception:
        h1 = False

    # H_2: The product H[G, G] is equal to G
    try:
        G_elems = set(G.elements)
        if hasattr(H, 'elements'):
            H_elems = set(H.elements)
        else:
            H_elems = set(H)
            
        C = G.derived_subgroup()
        C_elems = set(C.elements)
        
        prod_set = set()
        for h in H_elems:
            for c in C_elems:
                prod_set.add(h * c)
                
        h2 = (prod_set == G_elems)
    except Exception:
        h2 = False

    # neg_Q: H != G
    try:
        G_elems = set(G.elements)
        if hasattr(H, 'elements'):
            H_elems = set(H.elements)
        else:
            H_elems = set(H)
            
        neg_q = (H_elems != G_elems)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a nilpotent group",
    "H_2: The product of H and the derived subgroup of G is equal to G",
    "¬Q: H is not equal to G"
]

N_HYP = 2
NEG_Q_INDEX = 2