import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import factorint

# Top-level setup
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

def conditions(witness):
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False]
        G, H = witness
    except Exception:
        return [False, False]
        
    try:
        h1 = hasattr(G, 'order') and hasattr(H, 'order')
        if h1:
            oG = G.order()
            oH = H.order()
            h1 = isinstance(oG, (int, sympy.Integer)) and isinstance(oH, (int, sympy.Integer)) and oG > 0 and oH > 0
    except Exception:
        h1 = False
        
    try:
        order_G = G.order()
        order_H = H.order()
        order_GxH = order_G * order_H
        
        def is_p_group(n):
            if n == 1:
                return True
            return len(factorint(n)) == 1
            
        p_GxH = is_p_group(order_GxH)
        p_G = is_p_group(order_G)
        p_H = is_p_group(order_H)
        
        # The conclusion is: G x H is a p-group iff both G and H are p-groups.
        # We want the negated conclusion (i.e., the conclusion fails).
        neg_q = p_GxH != (p_G and p_H)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G and H are finite groups",
    "¬Q: It is NOT the case that (G x H is a p-group iff both G and H are p-groups)"
]

N_HYP = 1
NEG_Q_INDEX = 1