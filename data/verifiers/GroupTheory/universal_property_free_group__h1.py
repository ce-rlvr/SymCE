import itertools
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup

# Top-level setup: named object bindings for witness expressions
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

def get_homomorphisms(F, G):
    """Finds all group homomorphisms from PermutationGroup F to PermutationGroup G."""
    F_elems = list(F.generate())
    G_elems = list(G.generate())
    gens = F.generators
    
    id_F = None
    for x in F_elems:
        if x * x == x:
            id_F = x
            break
            
    id_G = None
    for x in G_elems:
        if x * x == x:
            id_G = x
            break
            
    homs = []
    for images in itertools.product(G_elems, repeat=len(gens)):
        mapping = {}
        queue = []
        
        mapping[id_F] = id_G
        queue.append(id_F)
        
        valid = True
        head = 0
        while head < len(queue):
            fx = queue[head]
            gx = mapping[fx]
            head += 1
            
            for g, img in zip(gens, images):
                fy = fx * g
                gy = gx * img
                if fy in mapping:
                    if mapping[fy] != gy:
                        valid = False
                        break
                else:
                    mapping[fy] = gy
                    queue.append(fy)
            if not valid:
                break
                
        if valid and len(mapping) == len(F_elems):
            homs.append(mapping)
            
    return homs

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            S = witness.get('S')
            F = witness.get('F')
            G = witness.get('G')
            f = witness.get('f')
        else:
            S, F, G, f = witness
    except Exception:
        return [False, False, False]

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: f is a function from S to G
    try:
        if isinstance(f, dict) and isinstance(S, (list, tuple, set)):
            domain_match = set(f.keys()) == set(S)
            G_elems = list(G.generate())
            values_in_G = all(v in G_elems for v in f.values())
            h2 = domain_match and values_in_G
        else:
            h2 = False
    except Exception:
        h2 = False

    # ¬Q: It is NOT the case that there exists a unique group homomorphism from F to G that extends f
    try:
        if not isinstance(F, PermutationGroup) or not isinstance(G, PermutationGroup):
            neg_q = False
        else:
            homs = get_homomorphisms(F, G)
            extending_homs = 0
            for hom in homs:
                extends = True
                for s in S:
                    if s not in hom or hom[s] != f[s]:
                        extends = False
                        break
                if extends:
                    extending_homs += 1
            neg_q = (extending_homs != 1)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: f is a function from S to G",
    "¬Q: It is not the case that there exists a unique group homomorphism from F to G that extends f"
]

N_HYP = 2
NEG_Q_INDEX = 2