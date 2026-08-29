import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]]))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_characteristic(G, H):
    try:
        if not isinstance(G, PermutationGroup) or not isinstance(H, PermutationGroup):
            return False
        if not H.is_subgroup(G):
            return False
        if not H.is_normal(G):
            return False
            
        elements = list(G.generate())
        n_el = len(elements)
        
        gens = G.generators
        
        for images in itertools.product(elements, repeat=len(gens)):
            if any(g.order() != img.order() for g, img in zip(gens, images)):
                continue
                
            img_list = list(images)
            if not img_list:
                if n_el != 1:
                    continue
            else:
                if PermutationGroup(img_list).order() != n_el:
                    continue
                
            mapping = {}
            id_el = G.identity
            mapping[id_el] = id_el
            
            frontier = [id_el]
            valid_hom = True
            
            head = 0
            while head < len(frontier):
                curr = frontier[head]
                head += 1
                for g, img in zip(gens, images):
                    nxt = curr * g
                    nxt_img = mapping[curr] * img
                    if nxt not in mapping:
                        mapping[nxt] = nxt_img
                        frontier.append(nxt)
                    else:
                        if mapping[nxt] != nxt_img:
                            valid_hom = False
                            break
                if not valid_hom:
                    break
                    
            if valid_hom and len(mapping) == n_el:
                for h in H.generators:
                    mapped_h = mapping.get(h)
                    if mapped_h is None or mapped_h not in H:
                        return False
                        
        return True
    except Exception:
        return False

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            n = witness.get('n')
            H = witness.get('H')
        elif isinstance(witness, tuple) and len(witness) == 3:
            G, n, H = witness
        else:
            G, n, H = None, None, None
            
        if isinstance(H, list):
            H = PermutationGroup(H)
    except Exception:
        G, n, H = None, None, None

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: n is a positive integer
    try:
        h2 = isinstance(n, int) and not isinstance(n, bool) and n > 0
    except Exception:
        h2 = False

    # neg_Q: H is not a characteristic subgroup of G
    try:
        if not h1:
            neg_q = False
        else:
            neg_q = not is_characteristic(G, H)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: n is a positive integer",
    "¬Q: H is not a characteristic subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2