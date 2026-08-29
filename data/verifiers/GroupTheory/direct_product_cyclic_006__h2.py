import math
from sympy.combinatorics import PermutationGroup, DirectProduct
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup: named object bindings
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
V4 = DirectProduct(Z2, Z2)

def get_order(obj):
    """Safely get the order of a group or element, handling both method and property."""
    o = obj.order
    return o() if callable(o) else o

def is_cyclic(G):
    """Check if a permutation group is cyclic."""
    try:
        if hasattr(G, 'is_cyclic'):
            res = G.is_cyclic
            if res is not None:
                return bool(res)
        order = get_order(G)
        for g in G.elements:
            if get_order(g) == order:
                return True
        return False
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    # Parse witness: can be (G_1, G_2, m, n) or just (G_1, G_2)
    try:
        if len(witness) == 4:
            G_1, G_2, m, n = witness
        elif len(witness) == 2:
            G_1, G_2 = witness
            m = get_order(G_1)
            n = get_order(G_2)
        else:
            return [False, False]
    except Exception:
        return [False, False]
    
    # H_1: G_1 is a cyclic group of order m
    try:
        h1 = is_cyclic(G_1) and get_order(G_1) == m
    except Exception:
        h1 = False
        
    # ¬Q: The conclusion "G_1 x G_2 is cyclic iff gcd(m, n) = 1" FAILS
    try:
        prod = DirectProduct(G_1, G_2)
        prod_cyclic = is_cyclic(prod)
        gcd_1 = (math.gcd(int(m), int(n)) == 1)
        neg_q = (prod_cyclic != gcd_1)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G_1 is a cyclic group of order m",
    "¬Q: G_1 x G_2 is cyclic iff gcd(m, n) = 1 is FALSE"
]

N_HYP = 1
NEG_Q_INDEX = 1