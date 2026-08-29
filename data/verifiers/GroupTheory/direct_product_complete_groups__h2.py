import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics.perm_groups import PermutationGroup
from sympy.combinatorics.permutations import Permutation
import itertools

# Top-level setup for potential witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def get_order(g):
    return g.order() if callable(g.order) else g.order

def direct_product(G, H):
    deg_G = G.degree
    deg_H = H.degree
    gens = []
    for g in G.generators:
        arr = [g(i) for i in range(deg_G)] + list(range(deg_G, deg_G + deg_H))
        gens.append(Permutation(arr))
    for h in H.generators:
        arr = list(range(deg_G)) + [h(i) + deg_G for i in range(deg_H)]
        gens.append(Permutation(arr))
    if not gens:
        return CyclicGroup(1)
    return PermutationGroup(gens)

def is_complete(grp):
    try:
        grp_order = get_order(grp)
        if grp_order == 1:
            return True
        
        center = grp.center()
        c_len = len(center) if isinstance(center, list) else get_order(center)
        if c_len != 1:
            return False
            
        gens = grp.generators
        elements = list(grp.generate())
        identity = next(e for e in elements if e * e == e)
        n_aut = 0
        
        gen_orders = [get_order(g) for g in gens]
        
        for images in itertools.product(elements, repeat=len(gens)):
            valid_orders = True
            for order, img in zip(gen_orders, images):
                if get_order(img) != order:
                    valid_orders = False
                    break
            if not valid_orders:
                continue
            
            mapping = {identity: identity}
            queue = [identity]
            head = 0
            is_homo = True
            while head < len(queue):
                curr = queue[head]
                head += 1
                curr_img = mapping[curr]
                for g, img in zip(gens, images):
                    nxt = curr * g
                    nxt_img = curr_img * img
                    if nxt in mapping:
                        if mapping[nxt] != nxt_img:
                            is_homo = False
                            break
                    else:
                        mapping[nxt] = nxt_img
                        queue.append(nxt)
                if not is_homo:
                    break
            
            if is_homo and len(set(mapping.values())) == grp_order:
                n_aut += 1
                
        return n_aut == grp_order
    except Exception:
        return False

def conditions(witness):
    try:
        if not isinstance(witness, tuple) or len(witness) != 2:
            return [False, False, False]
        G, H = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1 = False
        
    try:
        h2 = h1 and is_complete(H)
    except Exception:
        h2 = False
        
    try:
        if h1:
            GxH = direct_product(G, H)
            neg_q = not is_complete(GxH)
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: H is a complete group",
    "¬Q: G \\times H is not a complete group"
]

N_HYP = 2
NEG_Q_INDEX = 2