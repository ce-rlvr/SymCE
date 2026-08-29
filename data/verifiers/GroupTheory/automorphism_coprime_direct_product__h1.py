import math
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.free_groups import FreeGroup
from sympy import oo

class InfiniteCyclicGroup:
    def __init__(self):
        self.is_finite = False
        self.is_infinite_cyclic = True
        
    def order(self):
        return oo
        
    @property
    def is_abelian(self):
        return True

# Top-level setup for named groups
Z = InfiniteCyclicGroup()
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

def get_order(grp):
    if hasattr(grp, 'order'):
        if callable(grp.order):
            return grp.order()
        return grp.order
    if getattr(grp, 'is_finite', None) is False:
        return oo
    if type(grp).__name__ == 'FreeGroup':
        return oo
    return oo

def is_finite_group(grp):
    if hasattr(grp, 'is_finite'):
        return grp.is_finite
    if type(grp).__name__ == 'FreeGroup':
        return False
    if get_order(grp) < oo:
        return True
    return False

def neg_q_eval(G, H):
    oG = get_order(G)
    oH = get_order(H)
    
    if oG == oo and oH > 1:
        return True
    if oH == oo and oG > 1:
        return True
    if oG == 1 or oH == 1:
        return False
    if math.gcd(int(oG), int(oH)) == 1:
        return False
        
    if G == H:
        return True
        
    try:
        if hasattr(G, 'derived_subgroup') and hasattr(H, 'center'):
            G_ab_order = oG // G.derived_subgroup().order()
            H_center_order = H.center().order()
            if math.gcd(int(G_ab_order), int(H_center_order)) > 1:
                return True
                
            H_ab_order = oH // H.derived_subgroup().order()
            G_center_order = G.center().order()
            if math.gcd(int(H_ab_order), int(G_center_order)) > 1:
                return True
    except Exception:
        pass
        
    try:
        is_G_ab = getattr(G, 'is_abelian', False)
        if callable(is_G_ab): is_G_ab = is_G_ab()
        is_H_ab = getattr(H, 'is_abelian', False)
        if callable(is_H_ab): is_H_ab = is_H_ab()
        
        if is_G_ab and is_H_ab:
            if math.gcd(int(oG), int(oH)) > 1:
                return True
    except Exception:
        pass

    return False

def conditions(witness):
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False]
        G, H = witness
    except Exception:
        return [False, False, False]
    
    # H_1: H is a finite group
    try:
        h1 = is_finite_group(H)
    except Exception:
        h1 = False
        
    # H_2: The greatest common divisor of |G| and |H| is 1
    try:
        oG = get_order(G)
        oH = get_order(H)
        if oG == oo and oH < oo:
            h2 = True
        elif oH == oo and oG < oo:
            h2 = True
        elif oG == oo and oH == oo:
            h2 = False
        else:
            h2 = (math.gcd(int(oG), int(oH)) == 1)
    except Exception:
        h2 = False
        
    # ¬Q: The automorphism group Aut(G x H) is not isomorphic to Aut(G) x Aut(H)
    try:
        neg_q = neg_q_eval(G, H)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: H is a finite group",
    "H_2: The greatest common divisor of |G| and |H| is 1",
    "¬Q: The automorphism group Aut(G x H) is not isomorphic to Aut(G) x Aut(H)"
]

N_HYP = 2
NEG_Q_INDEX = 2