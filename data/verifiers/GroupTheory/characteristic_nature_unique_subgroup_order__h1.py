import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.homomorphisms import homomorphism
from sympy.matrices import eye, zeros
import itertools

# Top-level setup
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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_elements_tuple(grp):
    res = []
    for p in grp.elements:
        if hasattr(p, 'array_form'):
            res.append(tuple(p.array_form))
        else:
            res.append(str(p))
    try:
        return tuple(sorted(res))
    except Exception:
        return tuple(sorted([str(p) for p in grp.elements]))

def get_all_subgroups(G):
    from sympy import oo
    try:
        if callable(G.order):
            if G.order() == oo:
                raise ValueError("Group is infinite")
        else:
            if G.order == oo:
                raise ValueError("Group is infinite")
    except Exception:
        pass

    elements = list(G.elements)
    G_cls = type(G)
    
    id_perm = elements[0]**0
    trivial_sub = G_cls([id_perm])
    
    subgroups_dict = {get_elements_tuple(trivial_sub): trivial_sub}
    
    cyclic_subgroups = []
    for g in elements:
        cg = G_cls([g])
        tup = get_elements_tuple(cg)
        if tup not in subgroups_dict:
            subgroups_dict[tup] = cg
            cyclic_subgroups.append(cg)
            
    new_added = True
    while new_added:
        new_added = False
        current_subgroups = list(subgroups_dict.values())
        for H1 in current_subgroups:
            for H2 in cyclic_subgroups:
                gens = H1.generators + H2.generators
                K = G_cls(gens)
                tup = get_elements_tuple(K)
                if tup not in subgroups_dict:
                    subgroups_dict[tup] = K
                    new_added = True
                    if len(subgroups_dict) > 2000:
                        return list(subgroups_dict.values())
    return list(subgroups_dict.values())

def is_characteristic(G, H):
    from sympy import oo
    try:
        if callable(G.order):
            if G.order() == oo:
                raise ValueError("Group is infinite")
        else:
            if G.order == oo:
                raise ValueError("Group is infinite")
    except Exception:
        pass

    if not H.is_subgroup(G):
        return False
    gens = G.generators
    elements = list(G.elements)
    
    elements_by_order = {}
    for g in elements:
        try:
            o = g.order()
        except Exception:
            o = 0
        elements_by_order.setdefault(o, []).append(g)
        
    candidates_per_gen = []
    for gen in gens:
        try:
            o = gen.order()
        except Exception:
            o = 0
        candidates_per_gen.append(elements_by_order.get(o, []))
        
    H_elements = set(get_elements_tuple(H))
    
    for images in itertools.product(*candidates_per_gen):
        try:
            phi = homomorphism(G, G, gens, images)
            is_inj = False
            try:
                is_inj = phi.is_injective()
            except Exception:
                try:
                    is_inj = (phi.kernel().order() == 1)
                except Exception:
                    pass
            if is_inj:
                for h in H.generators:
                    try:
                        h_img = phi(h)
                        if hasattr(h_img, 'array_form'):
                            h_img_tup = tuple(h_img.array_form)
                        else:
                            h_img_tup = str(h_img)
                        if h_img_tup not in H_elements:
                            return False
                    except Exception:
                        return False
        except Exception:
            pass
    return True

def conditions(witness):
    try:
        G, H = witness
    except Exception:
        return [False, False, False]
        
    # H_1: H is a subgroup of G
    try:
        h1 = bool(H.is_subgroup(G))
    except Exception:
        h1 = False
        
    # H_2: There are no other subgroups of G having the same order as H
    try:
        if not h1:
            h2 = False
        else:
            order_H = H.order()
            subgroups = get_all_subgroups(G)
            count = 0
            for sub in subgroups:
                if sub.order() == order_H:
                    count += 1
            h2 = (count == 1)
    except Exception:
        h2 = False
        
    # neg_Q: H is NOT a characteristic subgroup of G
    try:
        if not h1:
            neg_q = False
        else:
            neg_q = not is_characteristic(G, H)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: H is a subgroup of G",
    "H_2: There are no other subgroups of G having the same order as H",
    "¬Q: H is not a characteristic subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2