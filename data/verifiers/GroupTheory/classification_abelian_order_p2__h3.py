import sympy
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
)

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, tuple) or len(witness) != 2:
            return [False, False, False]
        p, G = witness
    except Exception:
        return [False, False, False]
    
    # H_1: p is a prime number
    try:
        h1 = sympy.isprime(p)
    except Exception:
        h1 = False
        
    # H_2: G is an abelian group
    try:
        is_ab = getattr(G, 'is_abelian', False)
        if callable(is_ab):
            is_ab = is_ab()
        h2 = bool(is_ab)
    except Exception:
        h2 = False
        
    # ¬Q: G is neither isomorphic to Z/p^2Z nor to (Z/pZ) x (Z/pZ)
    try:
        if hasattr(G, 'order'):
            order = G.order() if callable(G.order) else G.order
        else:
            order = None
            
        is_ab = getattr(G, 'is_abelian', False)
        if callable(is_ab):
            is_ab = is_ab()
            
        # The only abelian groups of order p^2 are Z/p^2Z and (Z/pZ) x (Z/pZ).
        # Thus, G is isomorphic to one of them iff G is abelian and has order p^2.
        is_iso = bool(is_ab) and order == p**2
        neg_q = not is_iso
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: G is an abelian group",
    "¬Q: G is neither isomorphic to Z/p^2Z nor to (Z/pZ) x (Z/pZ)"
]

N_HYP = 2
NEG_Q_INDEX = 2