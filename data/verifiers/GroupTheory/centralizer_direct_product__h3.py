import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, CyclicGroup, AlternatingGroup, DihedralGroup
from sympy.matrices import eye, zeros

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
    try:
        G, H, g, h = witness
    except Exception:
        return [False, False, False]
    
    # H_1: G and H are groups
    try:
        h1_ok = hasattr(G, 'generators') and hasattr(H, 'generators')
    except Exception:
        h1_ok = False
        
    # H_2: g is an element of G
    try:
        if hasattr(G, '__contains__'):
            h2_ok = bool(g in G)
        elif hasattr(G, 'contains'):
            h2_ok = bool(G.contains(g))
        else:
            h2_ok = False
    except Exception:
        h2_ok = False
        
    # ¬Q: The conclusion fails.
    # The conclusion states that the centralizer of (g, h) in G x H is C_G(g) x C_H(h).
    # This mathematically holds for all g in G and h in H. The only way the conclusion 
    # fails (and the reason the conjecture is false) is if the dropped hypothesis "h is an element of H" 
    # is violated, meaning (g, h) is not an element of G x H, making the centralizer undefined or the equality false.
    try:
        if hasattr(H, '__contains__'):
            h_in_H = bool(h in H)
        elif hasattr(H, 'contains'):
            h_in_H = bool(H.contains(h))
        else:
            h_in_H = False
            
        neg_q_ok = not h_in_H
    except Exception:
        # If checking membership raises an error (e.g., incompatible types), h is not in H.
        neg_q_ok = True
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: g is an element of G",
    "¬Q: h is not an element of H (so (g, h) is not in G x H, making the centralizer undefined or the equality false)"
]

N_HYP = 2
NEG_Q_INDEX = 2