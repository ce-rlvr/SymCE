import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
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
trivial = PermutationGroup(Permutation(0))

def perm_order(p):
    if callable(p.order):
        return p.order()
    return p.order

def is_subgroup(sub, G):
    try:
        deg_G = G.degree
        sub_elems = set()
        for p in sub.generate():
            arr = list(p.array_form)
            if len(arr) < deg_G:
                arr += list(range(len(arr), deg_G))
            elif len(arr) > deg_G:
                if any(arr[i] != i for i in range(deg_G, len(arr))):
                    return False
                arr = arr[:deg_G]
            sub_elems.add(tuple(arr))
            
        G_elems = set()
        for p in G.generate():
            arr = list(p.array_form)
            if len(arr) < deg_G:
                arr += list(range(len(arr), deg_G))
            G_elems.add(tuple(arr))
            
        return sub_elems.issubset(G_elems)
    except Exception:
        return False

def get_automorphisms(G):
    elements = list(G.generate())
    n = len(elements)
    if n > 512:
        raise ValueError("Group too large to compute automorphisms quickly")
    
    elem_to_idx = {e: i for i, e in enumerate(elements)}
    mult = [[elem_to_idx[e1 * e2] for e2 in elements] for e1 in elements]
    
    orders = [perm_order(e) for e in elements]
    id_idx = orders.index(1)
    
    gens = G.generators
    gen_indices = [elem_to_idx[g] for g in gens]
    gen_orders = [orders[i] for i in gen_indices]
    
    possible_images = []
    for go in gen_orders:
        possible_images.append([i for i, o in enumerate(orders) if o == go])
        
    autos = []
    for img_indices in itertools.product(*possible_images):
        mapping = {id_idx: id_idx}
        valid = True
        for g_idx, i_idx in zip(gen_indices, img_indices):
            if g_idx in mapping:
                if mapping[g_idx] != i_idx:
                    valid = False
                    break
            else:
                mapping[g_idx] = i_idx
        if not valid:
            continue
        
        queue = list(mapping.keys())
        head = 0
        while head < len(queue):
            u = queue[head]
            head += 1
            for v in gen_indices:
                uv = mult[u][v]
                mapped_uv = mult[mapping[u]][mapping[v]]
                if uv in mapping:
                    if mapping[uv] != mapped_uv:
                        valid = False
                        break
                else:
                    mapping[uv] = mapped_uv
                    queue.append(uv)
            if not valid:
                break
        
        if valid and len(mapping) == n and len(set(mapping.values())) == n:
            auto_map = {elements[k]: elements[v] for k, v in mapping.items()}
            autos.append(auto_map)
            
    return autos

def is_characteristic(H, B):
    if not is_subgroup(B, H):
        return False
    autos = get_automorphisms(H)
    
    deg_H = H.degree
    
    H_elements = list(H.generate())
    H_dict = {tuple(p.array_form): p for p in H_elements}
    
    B_in_H = set()
    for p in B.generate():
        arr = list(p.array_form)
        if len(arr) < deg_H:
            arr += list(range(len(arr), deg_H))
        elif len(arr) > deg_H:
            arr = arr[:deg_H]
        t = tuple(arr)
        if t in H_dict:
            B_in_H.add(H_dict[t])
        else:
            return False
            
    for auto in autos:
        for b in B_in_H:
            if auto[b] not in B_in_H:
                return False
    return True

def direct_product_subgroups(G, H, A, B):
    deg_G = max(G.degree, A.degree)
    deg_H = max(H.degree, B.degree)
    
    gens = []
    for a in A.generators:
        images = list(a.array_form)
        if len(images) < deg_G:
            images += list(range(len(images), deg_G))
        elif len(images) > deg_G:
            images = images[:deg_G]
        images += list(range(deg_G, deg_G + deg_H))
        gens.append(Permutation(images))
        
    for b in B.generators:
        images = list(range(deg_G))
        b_images = list(b.array_form)
        if len(b_images) < deg_H:
            b_images += list(range(len(b_images), deg_H))
        elif len(b_images) > deg_H:
            b_images = b_images[:deg_H]
        images += [x + deg_G for x in b_images]
        gens.append(Permutation(images))
        
    if not gens:
        size = deg_G + deg_H
        if size == 0:
            return PermutationGroup([Permutation()])
        else:
            return PermutationGroup([Permutation(size - 1)])
    return PermutationGroup(gens)

def conditions(witness):
    if isinstance(witness, dict):
        G = witness.get('G')
        H = witness.get('H')
        A = witness.get('A')
        B = witness.get('B')
    else:
        try:
            G, H, A, B = witness
        except Exception:
            return [False, False, False]
            
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1 = False
        
    try:
        h2 = isinstance(B, PermutationGroup) and is_characteristic(H, B)
    except Exception:
        h2 = False
        
    try:
        if not (isinstance(A, PermutationGroup) and isinstance(B, PermutationGroup)):
            neg_q = False
        elif not is_subgroup(A, G) or not is_subgroup(B, H):
            neg_q = False
        else:
            GxH = direct_product_subgroups(G, H, G, H)
            AxB = direct_product_subgroups(G, H, A, B)
            neg_q = not is_characteristic(GxH, AxB)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: B is a characteristic subgroup of H",
    "¬Q: A x B is not a characteristic subgroup of G x H"
]

N_HYP = 2
NEG_Q_INDEX = 2