import sympy
from sympy.combinatorics import PermutationGroup, DirectProduct
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

# Top-level setup
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

def get_socle(G):
    if hasattr(G, 'socle'):
        try:
            return G.socle()
        except Exception:
            pass
            
    normal_subgroups = G.normal_subgroups()
    non_trivial_ns = [N for N in normal_subgroups if N.order() > 1]
    minimal_ns = []
    for N in non_trivial_ns:
        is_minimal = True
        for M in non_trivial_ns:
            if M.order() < N.order() and M.is_subgroup(N):
                is_minimal = False
                break
        if is_minimal:
            minimal_ns.append(N)
    
    if not minimal_ns:
        return PermutationGroup([G.identity])
    
    gens = []
    for N in minimal_ns:
        gens.extend(N.generators)
    return PermutationGroup(gens)

def conditions(witness):
    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            G, H = witness
        else:
            G = witness
            H = witness
            
        G_times_H = DirectProduct(G, H)
        soc_G = get_socle(G)
        soc_H = get_socle(H)
        soc_GH = get_socle(G_times_H)
        
        # Since Soc(G) x Soc(H) is isomorphic to a subgroup of Soc(G x H),
        # they are equal if and only if their orders are equal.
        expected_order = soc_G.order() * soc_H.order()
        actual_order = soc_GH.order()
        
        neg_Q = bool(actual_order != expected_order)
    except Exception:
        neg_Q = False
        
    return [neg_Q]

CONDITION_LABELS = [
    "¬Q: The socle of G x H is not equal to Soc(G) x Soc(H)"
]

N_HYP = 0
NEG_Q_INDEX = 0