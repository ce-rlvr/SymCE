import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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
    """
    Given a witness tuple (G, g, x), checks if it is a valid counterexample.
    Returns [H_1_ok, neg_Q_ok].
    """
    try:
        G, g, x = witness
    except Exception:
        return [False, False]
    
    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # ¬Q: C_G(gxg^{-1}) != g C_G(x) g^{-1}
    try:
        # Compute C_G(x)
        C_G_x = set()
        for y in G.elements:
            if y * x == x * y:
                C_G_x.add(y)
                
        # Compute g C_G(x) g^{-1}
        g_inv = g**-1
        g_C_G_x_g_inv = set(g * y * g_inv for y in C_G_x)
        
        # Compute g x g^{-1}
        gxg_inv = g * x * g_inv
        
        # Compute C_G(gxg^{-1})
        C_G_gxg_inv = set()
        for z in G.elements:
            if z * gxg_inv == gxg_inv * z:
                C_G_gxg_inv.add(z)
                
        # The conclusion fails if the two sets are not equal
        neg_q = (C_G_gxg_inv != g_C_G_x_g_inv)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "¬Q: C_G(gxg^{-1}) is not equal to g C_G(x) g^{-1}"
]

N_HYP = 1
NEG_Q_INDEX = 1