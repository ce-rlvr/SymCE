import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros
import itertools

# Top-level setup for potential witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_automorphisms(G):
    """Finds all automorphisms of a finite permutation group G."""
    gens = G.generators
    elements = list(G.elements)
    autos = []
    
    identity = None
    for p in elements:
        if p.is_Identity:
            identity = p
            break
    if identity is None:
        if gens:
            identity = gens[0]**0
        else:
            return []

    # An automorphism is uniquely determined by its action on the generators.
    for imgs in itertools.product(elements, repeat=len(gens)):
        img_dict = dict(zip(gens, imgs))
        # Necessary condition: automorphisms preserve the order of elements
        if any(g.order() != img.order() for g, img in zip(gens, imgs)):
            continue
        
        map_dict = {identity: identity}
        queue = [identity]
        valid = True
        
        # BFS to extend the map to the entire group
        while queue:
            curr = queue.pop(0)
            for g in gens:
                nxt = curr * g
                nxt_img = map_dict[curr] * img_dict[g]
                if nxt in map_dict:
                    if map_dict[nxt] != nxt_img:
                        valid = False
                        break
                else:
                    map_dict[nxt] = nxt_img
                    queue.append(nxt)
            if not valid:
                break
                
        # If it's a valid homomorphism and bijective, it's an automorphism
        if valid and len(set(map_dict.values())) == len(elements):
            autos.append(map_dict)
            
    return autos

def is_subgroup_elements(G, H_elements):
    """Checks if a subset of elements forms a subgroup of G."""
    if not H_elements:
        return False
    
    identity = None
    for p in G.elements:
        if p.is_Identity:
            identity = p
            break
    if identity is None and G.generators:
        identity = G.generators[0]**0
        
    if identity is not None and identity not in H_elements:
        return False
        
    # Check closure under group operation
    for a in H_elements:
        for b in H_elements:
            if a * b not in H_elements:
                return False
    return True

def is_characteristic_elements(G, H_elements):
    """Checks if a subset of elements forms a characteristic subgroup of G."""
    G_elements = set(G.elements)
    if not H_elements.issubset(G_elements):
        return False
    if not is_subgroup_elements(G, H_elements):
        return False
        
    autos = get_automorphisms(G)
    for auto in autos:
        for h in H_elements:
            if auto[h] not in H_elements:
                return False
    return True

def conditions(witness) -> list[bool]:
    # Witness is expected to be a tuple: (G, [H_1, H_2, ..., H_k])
    try:
        G, H_list = witness
    except Exception:
        return [False, False, False]
    
    # H_1: I is a non-empty index set
    try:
        h1 = isinstance(H_list, (list, tuple)) and len(H_list) > 0
    except Exception:
        h1 = False

    # H_2: For each i in I, H_i is a characteristic subgroup of G
    try:
        h2 = True
        for H in H_list:
            if hasattr(H, 'elements'):
                H_elems = set(H.elements)
            else:
                H_elems = set(H)
            if not is_characteristic_elements(G, H_elems):
                h2 = False
                break
    except Exception:
        h2 = False

    # ¬Q: The intersection of H_i is NOT a characteristic subgroup of G
    try:
        intersect_elements = set(G.elements)
        for H in H_list:
            if hasattr(H, 'elements'):
                H_elems = set(H.elements)
            else:
                H_elems = set(H)
            intersect_elements = intersect_elements.intersection(H_elems)
        
        neg_q = not is_characteristic_elements(G, intersect_elements)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: I is a non-empty index set",
    "H_2: For each i in I, H_i is a characteristic subgroup of G",
    "¬Q: The intersection of H_i is not a characteristic subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2