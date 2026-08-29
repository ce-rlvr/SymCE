import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import factorint
from itertools import combinations

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # Isomorphic to the Klein four-group
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def has_subgroup_of_order(G, m):
    """
    Helper function to check if a finite group G has a subgroup of order m.
    """
    m = int(m)
    order = G.order()
    
    # Trivial cases
    if m == 1 or m == order:
        return True
    if order % m != 0:
        return False
        
    # The converse of Lagrange's theorem holds for all finite nilpotent groups 
    # (and thus for all finite abelian groups).
    if getattr(G, 'is_abelian', False):
        return True
    try:
        if hasattr(G, 'is_nilpotent') and G.is_nilpotent():
            return True
    except Exception:
        pass
        
    # By Sylow's theorems, if m is a prime power, G has a subgroup of order m.
    factors = factorint(m)
    if len(factors) == 1:
        return True
        
    # If we cannot easily enumerate elements, assume True to avoid false positives for neg_Q
    if not isinstance(G, PermutationGroup):
        return True

    # General bounded search for small groups
    try:
        elements = list(G.generate_elements())
    except Exception:
        return True
        
    # A subgroup of order m can only contain elements whose order divides m
    valid_elements = [e for e in elements if m % e.order() == 0]
    if len(valid_elements) < m:
        return False
        
    # Check 1-generated (cyclic) subgroups
    for e in valid_elements:
        if e.order() == m:
            return True
            
    # Check 2-generated subgroups
    for gens in combinations(valid_elements, 2):
        H = PermutationGroup(*gens)
        if H.order() == m:
            return True
            
    # Check 3-generated subgroups (only needed for larger m, bounded to prevent timeouts)
    if m >= 24:
        count = 0
        for gens in combinations(valid_elements, 3):
            count += 1
            if count > 10000:
                break
            H = PermutationGroup(*gens)
            if H.order() == m:
                return True
                
    return False

def conditions(witness) -> list[bool]:
    """
    Given a witness (G, m), evaluates the hypotheses and the negated conclusion.
    Returns [H_1, H_2, H_3, neg_Q].
    """
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False, False]
        G, m = witness
    except Exception:
        return [False, False, False, False]
        
    # H_1: G is a finite group
    try:
        h1 = hasattr(G, 'order') and G.order() > 0 and G.order() < float('inf')
    except Exception:
        h1 = False
        
    # H_2: G is an abelian group
    try:
        h2 = bool(G.is_abelian)
    except Exception:
        h2 = False
        
    # H_3: m divides the order of G
    try:
        if not isinstance(m, (int, sympy.Integer)):
            h3 = False
        else:
            m_val = int(m)
            h3 = (m_val > 0) and (G.order() % m_val == 0)
    except Exception:
        h3 = False
        
    # ¬Q: G does not contain a subgroup of order m
    try:
        neg_q = not has_subgroup_of_order(G, m)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: G is an abelian group",
    "H_3: m divides the order of G",
    "¬Q: G does not contain a subgroup of order m"
]

N_HYP = 3
NEG_Q_INDEX = 3