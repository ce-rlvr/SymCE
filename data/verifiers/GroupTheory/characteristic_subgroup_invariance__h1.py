import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools

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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def are_perms_equal(p1, p2):
    try:
        a1 = p1.array_form
        a2 = p2.array_form
        m = max(len(a1), len(a2))
        a1 = a1 + list(range(len(a1), m))
        a2 = a2 + list(range(len(a2), m))
        return a1 == a2
    except Exception:
        return False

def get_mapped_element(mapping, g, elements):
    for e in elements:
        if are_perms_equal(e, g):
            return mapping[e]
    raise KeyError

def is_subgroup(G, H):
    try:
        elements_G = list(G.generate())
        for h_gen in H.generators:
            found = False
            for g in elements_G:
                if are_perms_equal(h_gen, g):
                    found = True
                    break
            if not found:
                return False
        return True
    except Exception:
        return False

def is_characteristic(G, H):
    try:
        gens = G.generators
        elements = list(G.generate())
        elements_H = list(H.generate())
        
        # Find all automorphisms by extending maps from generators
        auts = []
        for images in itertools.product(elements, repeat=len(gens)):
            mapping = {G.identity: G.identity}
            queue = [G.identity]
            valid = True
            
            while queue:
                curr = queue.pop(0)
                for i, g in enumerate(gens):
                    nxt = curr * g
                    nxt_img = mapping[curr] * images[i]
                    if nxt in mapping:
                        if mapping[nxt] != nxt_img:
                            valid = False
                            break
                    else:
                        mapping[nxt] = nxt_img
                        queue.append(nxt)
                if not valid:
                    break
            
            if valid and len(mapping) == len(elements):
                # Check if it's an isomorphism (bijective)
                if len(set(mapping.values())) == len(elements):
                    auts.append(mapping)
                    
        # Check if H is invariant under all automorphisms
        for mapping in auts:
            for h_gen in H.generators:
                mapped_h_gen = get_mapped_element(mapping, h_gen, elements)
                found_in_H = False
                for h_elem in elements_H:
                    if are_perms_equal(mapped_h_gen, h_elem):
                        found_in_H = True
                        break
                if not found_in_H:
                    return False
        return True
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        G, H = witness
    except Exception:
        return [False, False, False, False]
    
    try:
        if not is_subgroup(G, H):
            h1 = False
        else:
            h1 = is_characteristic(G, H)
    except Exception:
        h1 = False

    # Aut(G) is the automorphism group of G (Tautology in this context)
    h2 = True

    # Aut(G) acts on the set of all subgroups of G (Tautology in this context)
    h3 = True

    try:
        if not is_subgroup(G, H):
            neg_q = False
        else:
            neg_q = not is_characteristic(G, H)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: H is a characteristic subgroup of G",
    "H_2: Aut(G) is the automorphism group of G",
    "H_3: Aut(G) acts on the set of all subgroups of G",
    "¬Q: H is not a fixed point under the action of Aut(G)"
]

N_HYP = 3
NEG_Q_INDEX = 3