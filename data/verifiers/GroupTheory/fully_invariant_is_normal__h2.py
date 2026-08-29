import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.matrices import eye, zeros
from itertools import product

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_endomorphisms(G):
    """
    Computes all endomorphisms of a finite permutation group G.
    Returns a list of dictionaries, each mapping elements of G to elements of G.
    """
    elements = list(G.elements)
    gens = G.generators
    identity = G.identity
    endos = []
    
    for images in product(elements, repeat=len(gens)):
        mapping = dict(zip(gens, images))
        full_map = {identity: identity}
        queue = [identity]
        idx = 0
        valid = True
        
        while idx < len(queue):
            curr = queue[idx]
            idx += 1
            for g in gens:
                nxt = curr * g
                nxt_val = full_map[curr] * mapping[g]
                if nxt in full_map:
                    if full_map[nxt] != nxt_val:
                        valid = False
                        break
                else:
                    full_map[nxt] = nxt_val
                    queue.append(nxt)
            if not valid:
                break
                
        if valid and len(full_map) == len(elements):
            endos.append(full_map)
            
    return endos

def conditions(witness) -> list[bool]:
    try:
        G, H = witness
    except Exception:
        return [False, False, False]
    
    # H_1: G is a group (and H is a subset/subgroup of G)
    try:
        h1 = isinstance(G, PermutationGroup)
        if h1:
            if isinstance(H, PermutationGroup):
                h1 = H.is_subgroup(G)
            else:
                g_elements = list(G.elements)
                h1 = all(h in g_elements for h in H)
    except Exception:
        h1 = False

    # H_2: For every endomorphism \phi of G, \phi(H) \subseteq H
    try:
        h2 = False
        if isinstance(G, PermutationGroup):
            h2 = True
            endos = get_endomorphisms(G)
            if isinstance(H, PermutationGroup):
                h_elements = list(H.elements)
            else:
                h_elements = list(H)
                
            for phi in endos:
                for h in h_elements:
                    if h not in phi or phi[h] not in h_elements:
                        h2 = False
                        break
                if not h2:
                    break
    except Exception:
        h2 = False

    # ¬Q: H is not a normal subgroup of G
    try:
        neg_q = False
        if isinstance(G, PermutationGroup):
            if isinstance(H, PermutationGroup):
                if not H.is_subgroup(G):
                    is_normal = False
                else:
                    is_normal = H.is_normal(G)
            else:
                h_elements = list(H)
                g_elements = list(G.elements)
                if not h_elements or not all(h in g_elements for h in h_elements):
                    is_normal = False
                else:
                    is_subgroup = True
                    identity = G.identity
                    if identity not in h_elements:
                        is_subgroup = False
                    else:
                        for a in h_elements:
                            for b in h_elements:
                                if a * b not in h_elements:
                                    is_subgroup = False
                                    break
                            if not is_subgroup:
                                break
                    
                    if not is_subgroup:
                        is_normal = False
                    else:
                        is_normal = True
                        for g in g_elements:
                            for h in h_elements:
                                conj = g * h * (g**-1)
                                if conj not in h_elements:
                                    is_normal = False
                                    break
                            if not is_normal:
                                break
            neg_q = not is_normal
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: For every endomorphism phi of G, phi(H) is a subset of H",
    "¬Q: H is not a normal subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2