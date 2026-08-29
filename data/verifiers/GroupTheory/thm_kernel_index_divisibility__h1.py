import sympy
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

def get_order(group):
    """Helper to safely get the order of a group, handling both methods and properties."""
    order_attr = group.order
    if callable(order_attr):
        return order_attr()
    return order_attr

def conditions(witness) -> list[bool]:
    try:
        G, H, phi = witness
    except Exception:
        return [False, False, False]
        
    # H_1: H is a finite group
    try:
        h_order = get_order(H)
        h1 = h_order != sympy.oo and h_order != float('inf')
    except Exception:
        h1 = False
        
    # H_2: phi: G -> H is a group homomorphism
    try:
        h2 = (hasattr(phi, 'domain') and phi.domain == G and 
              hasattr(phi, 'codomain') and phi.codomain == H and 
              hasattr(phi, 'kernel') and hasattr(phi, 'image'))
    except Exception:
        h2 = False
        
    # ¬Q: The index of ker(phi) in G does not divide the order of H
    try:
        ker = phi.kernel()
        g_order = get_order(G)
        k_order = get_order(ker)
        h_order = get_order(H)
        
        if g_order != sympy.oo and k_order != sympy.oo and g_order != float('inf') and k_order != float('inf'):
            idx = g_order // k_order
        else:
            idx = get_order(phi.image())
            
        q = (h_order % idx == 0)
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: H is a finite group",
    "H_2: phi: G -> H is a group homomorphism",
    "¬Q: The index of ker(phi) in G does not divide the order of H"
]

N_HYP = 2
NEG_Q_INDEX = 2