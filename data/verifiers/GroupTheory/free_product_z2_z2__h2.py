import sympy
from sympy.combinatorics import (
    PermutationGroup, SymmetricGroup, AlternatingGroup, 
    DihedralGroup, CyclicGroup
)
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_cyclic_order_2(G):
    if G == 2:
        return True
    if str(G).replace(" ", "") in ["Z2", "C2", "CyclicGroup(2)", "SymmetricGroup(2)", "DihedralGroup(1)"]:
        return True
    try:
        if hasattr(G, 'order'):
            ord_G = G.order() if callable(G.order) else G.order
            if ord_G == 2:
                return True
    except Exception:
        pass
    try:
        if hasattr(G, 'elements'):
            if len(list(G.elements)) == 2:
                return True
    except Exception:
        pass
    return False

def is_free_product(G, G1, G2):
    if G == ("free_product", G1, G2): return True
    if G == (G1, G2): return True
    if isinstance(G, str):
        s = str(G).replace(" ", "")
        s1 = str(G1).replace(" ", "")
        s2 = str(G2).replace(" ", "")
        if s == f"{s1}*{s2}": return True
        if s == f"FreeProduct({s1},{s2})": return True
    try:
        if hasattr(G, 'generators') and hasattr(G1, 'generators') and hasattr(G2, 'generators'):
            if len(G.generators) == len(G1.generators) + len(G2.generators):
                if hasattr(G, 'relators') and hasattr(G1, 'relators') and hasattr(G2, 'relators'):
                    if len(G.relators) == len(G1.relators) + len(G2.relators):
                        return True
    except Exception:
        pass
    return False

def conditions(witness):
    try:
        G1, G2, G = witness
    except Exception:
        return [False, False, False]
        
    # H1: G1 is a cyclic group of order 2
    try:
        h1 = is_cyclic_order_2(G1)
    except Exception:
        h1 = False
    
    # H2: G is the free product G1 * G2
    try:
        h2 = is_free_product(G, G1, G2)
    except Exception:
        h2 = False

    # neg_Q: G is NOT isomorphic to the infinite dihedral group
    # G is isomorphic to D_infty iff G1 and G2 are both cyclic of order 2
    try:
        is_d_infty = is_cyclic_order_2(G1) and is_cyclic_order_2(G2)
        neg_q = not is_d_infty
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G_1 is a cyclic group of order 2",
    "H_2: G is the free product G_1 * G_2",
    "¬Q: G is not isomorphic to the infinite dihedral group"
]

N_HYP = 2
NEG_Q_INDEX = 2