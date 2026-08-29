import sympy
from sympy.combinatorics import Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
)
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
V4 = AbelianGroup(2, 2)

def conditions(witness):
    try:
        G, H, phi = witness
    except Exception:
        return [False, False, False]
        
    # H_1: G is a perfect group
    try:
        h1 = (G.derived_subgroup().order() == G.order())
    except Exception:
        h1 = False
        
    # H_2: H is an abelian group
    try:
        h2 = bool(H.is_abelian)
    except Exception:
        h2 = False
        
    # neg_Q: phi is not the trivial homomorphism
    # (i.e., it is a valid map from G to H, but does not map all of G to the identity of H)
    try:
        is_function = True
        is_trivial = True
        
        for g in G.elements:
            try:
                val = phi(g) if callable(phi) else phi[g]
            except Exception:
                is_function = False
                break
                
            if val not in H:
                is_function = False
                break
                
            if not val.is_Identity:
                is_trivial = False
                
        neg_q = is_function and not is_trivial
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a perfect group",
    "H_2: H is an abelian group",
    "¬Q: phi is not the trivial homomorphism (does not map all of G to the identity of H)"
]

N_HYP = 2
NEG_Q_INDEX = 2