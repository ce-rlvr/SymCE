import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, Permutation
from sympy.matrices import eye, zeros
import itertools
import math
import functools

# Top-level setup
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
    """
    Computes all automorphisms of a finite permutation group G.
    Returns a list of dictionaries, each representing an automorphism mapping.
    """
    elements = list(G.generate())
    gens = G.generators
    autos = []
    
    for images in itertools.product(elements, repeat=len(gens)):
        mapping = {G.identity: G.identity}
        valid = True
        
        for g, img in zip(gens, images):
            if g in mapping:
                if mapping[g] != img:
                    valid = False
            else:
                mapping[g] = img
        
        if not valid:
            continue
            
        queue = list(mapping.keys())
        
        while queue and valid:
            curr = queue.pop(0)
            for g in gens:
                nxt = curr * g
                nxt_img = mapping[curr] * mapping[g]
                if nxt in mapping:
                    if mapping[nxt] != nxt_img:
                        valid = False
                        break
                else:
                    mapping[nxt] = nxt_img
                    queue.append(nxt)
                    
        if valid and len(mapping) == len(elements) and len(set(mapping.values())) == len(elements):
            autos.append(mapping)
            
    return autos

def is_subgroup(H, G):
    """Checks if H is a subgroup of G by verifying all elements of H are in G."""
    try:
        G_elements = set(G.generate())
        return all(h in G_elements for h in H.generate())
    except Exception:
        return False

def is_characteristic(G, H, autos):
    """Checks if H is invariant under all automorphisms of G."""
    try:
        H_elements = set(H.generate())
        for phi in autos:
            for h in H_elements:
                if phi[h] not in H_elements:
                    return False
        return True
    except Exception:
        return False

def conditions(witness):
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    The witness is expected to be a tuple (G, H).
    """
    try:
        if not isinstance(witness, tuple) or len(witness) != 2:
            return [False, False, False, False]
        G, H = witness
    except Exception:
        return [False, False, False, False]
        
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    autos = None
    is_char = False
    is_sub = False
    
    try:
        if h1 and isinstance(H, PermutationGroup):
            is_sub = is_subgroup(H, G)
            if is_sub:
                autos = get_automorphisms(G)
                is_char = is_characteristic(G, H, autos)
    except Exception:
        pass

    try:
        h2 = is_char
    except Exception:
        h2 = False
        
    try:
        # Aut(G) acting on the set of all subgroups of G is a fundamental mathematical property
        # that holds for any valid group G.
        h3 = h1
    except Exception:
        h3 = False
        
    try:
        neg_q = False
        if h1 and isinstance(H, PermutationGroup) and is_sub:
            neg_q = not is_char
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a characteristic subgroup of G",
    "H_3: Aut(G) acts on the set of all subgroups of G",
    "¬Q: The subgroup H is not a fixed point under the action of Aut(G)"
]

N_HYP = 3
NEG_Q_INDEX = 3