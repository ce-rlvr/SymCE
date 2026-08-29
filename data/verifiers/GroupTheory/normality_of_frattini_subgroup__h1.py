import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)  # V4 is isomorphic to A4's Sylow 2-subgroup, but A4 is provided as fallback
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def get_all_subgroups(G):
    """
    Computes all subgroups of a finite permutation group G.
    Returns a set of frozensets, where each frozenset contains the elements of a subgroup.
    """
    elements = list(G.elements)
    identity = G.identity
    
    trivial_subgroup = frozenset([identity])
    all_subgroups = {trivial_subgroup}
    queue = [trivial_subgroup]
    
    while queue:
        current = queue.pop(0)
        for g in elements:
            if g not in current:
                new_subgroup = set(current)
                new_elements = [g]
                new_subgroup.add(g)
                
                while new_elements:
                    x = new_elements.pop()
                    for y in list(new_subgroup):
                        xy = x * y
                        if xy not in new_subgroup:
                            new_subgroup.add(xy)
                            new_elements.append(xy)
                        yx = y * x
                        if yx not in new_subgroup:
                            new_subgroup.add(yx)
                            new_elements.append(yx)
                
                new_subgroup_fs = frozenset(new_subgroup)
                if new_subgroup_fs not in all_subgroups:
                    all_subgroups.add(new_subgroup_fs)
                    queue.append(new_subgroup_fs)
                    
    return all_subgroups

def frattini_subgroup_elements(G):
    """
    Computes the Frattini subgroup of G (intersection of all maximal subgroups).
    Returns a frozenset of its elements.
    """
    all_subgroups = get_all_subgroups(G)
    order_G = G.order()
    
    proper_subgroups = [H for H in all_subgroups if len(H) < order_G]
    if not proper_subgroups:
        return frozenset(G.elements)
        
    maximal = []
    for M in proper_subgroups:
        is_max = True
        for H in proper_subgroups:
            if len(M) < len(H) and M.issubset(H):
                is_max = False
                break
        if is_max:
            maximal.append(M)
            
    if not maximal:
        return frozenset(G.elements)
        
    intersect = set(maximal[0])
    for M in maximal[1:]:
        intersect = intersect.intersection(M)
        
    return frozenset(intersect)

def is_normal_subgroup(H_elements, G_elements):
    """
    Checks if H is a normal subgroup of G.
    """
    H_set = set(H_elements)
    for h in H_set:
        for g in G_elements:
            # Conjugate of h by g
            conj = (~g) * h * g
            if conj not in H_set:
                return False
    return True

def conditions(witness) -> list[bool]:
    h1 = False
    neg_q = False
    
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, Phi_G = witness
            G_elements = list(G.elements)
            
            if hasattr(Phi_G, 'elements'):
                Phi_G_elements = list(Phi_G.elements)
            else:
                Phi_G_elements = list(Phi_G)
                
            expected_phi = frattini_subgroup_elements(G)
            h1 = (frozenset(Phi_G_elements) == expected_phi)
            
            neg_q = not is_normal_subgroup(Phi_G_elements, G_elements)
        else:
            G = witness
            G_elements = list(G.elements)
            expected_phi = frattini_subgroup_elements(G)
            
            h1 = True
            neg_q = not is_normal_subgroup(expected_phi, G_elements)
            
    except Exception:
        pass

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: \\Phi(G) is the Frattini subgroup of G",
    "¬Q: \\Phi(G) is not a normal subgroup of G"
]

N_HYP = 1
NEG_Q_INDEX = 1