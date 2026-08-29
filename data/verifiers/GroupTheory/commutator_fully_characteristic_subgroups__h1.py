import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics import PermutationGroup
from sympy.matrices import eye, zeros
from itertools import product

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

def get_endomorphisms(G):
    """Find all endomorphisms of a PermutationGroup G using BFS."""
    elements = list(G.generate())
    gens = G.generators
    endos = []
    id_el = G.identity
    for images in product(elements, repeat=len(gens)):
        mapping = {id_el: id_el}
        valid = True
        
        queue = [id_el]
        gen_img = {g: img for g, img in zip(gens, images)}
        
        while queue:
            curr = queue.pop(0)
            for g in gens:
                nxt = curr * g
                nxt_img = mapping[curr] * gen_img[g]
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
            endos.append(mapping)
            
    return endos

def is_subgroup(G, H):
    try:
        if not hasattr(H, 'generators'):
            return False
        G_elements = set(G.generate())
        return all(h in G_elements for h in H.generators)
    except Exception:
        return False

def is_fully_characteristic(G, H, endos):
    if not endos:
        return False
    try:
        H_elements = set(H.generate())
        for mapping in endos:
            for h in H.generators:
                if h not in mapping:
                    return False
                if mapping[h] not in H_elements:
                    return False
        return True
    except Exception:
        return False

def mutual_commutator_subgroup(G, H, K):
    H_elements = list(H.generate())
    K_elements = list(K.generate())
    commutators = set()
    for h in H_elements:
        for k in K_elements:
            c = h * k * (~h) * (~k)
            commutators.add(c)
    return PermutationGroup(list(commutators))

def conditions(witness) -> list[bool]:
    try:
        G, H, K = witness
    except Exception:
        return [False, False, False, False, False]
    
    # H_1: H is a subgroup of G
    try:
        h1 = is_subgroup(G, H)
    except Exception:
        h1 = False

    # H_2: K is a subgroup of G
    try:
        h2 = is_subgroup(G, K)
    except Exception:
        h2 = False

    try:
        if h1 and h2:
            endos = get_endomorphisms(G)
        else:
            endos = []
    except Exception:
        endos = []

    # H_3: H is a fully characteristic subgroup of G
    try:
        h3 = h1 and is_fully_characteristic(G, H, endos)
    except Exception:
        h3 = False

    # H_4: K is a fully characteristic subgroup of G
    try:
        h4 = h2 and is_fully_characteristic(G, K, endos)
    except Exception:
        h4 = False

    # neg_Q: The mutual commutator subgroup of H and K is NOT a fully characteristic subgroup of G
    try:
        if not (h1 and h2) or not endos:
            neg_q = False
        else:
            HK = mutual_commutator_subgroup(G, H, K)
            q = is_fully_characteristic(G, HK, endos)
            neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: H is a subgroup of G",
    "H_2: K is a subgroup of G",
    "H_3: H is a fully characteristic subgroup of G",
    "H_4: K is a fully characteristic subgroup of G",
    "not Q: The mutual commutator subgroup of H and K is not a fully characteristic subgroup of G"
]

N_HYP = 4
NEG_Q_INDEX = 4