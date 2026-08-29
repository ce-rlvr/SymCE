import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics import PermutationGroup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def get_identity(elements):
    for e in elements:
        if e * e == e:
            return e
    return elements[0]

def get_order(g, id_el):
    if hasattr(g, 'order') and callable(g.order):
        return g.order()
    curr = g
    order = 1
    while curr != id_el:
        curr = curr * g
        order += 1
        if order > 1000:
            break
    return order

def close_subgroup(S):
    if not S:
        return frozenset()
    subgroup = set(S)
    queue = list(S)
    while queue:
        c = queue.pop(0)
        for s in S:
            y = c * s
            if y not in subgroup:
                subgroup.add(y)
                queue.append(y)
    return frozenset(subgroup)

def get_all_subgroups(G, elements, id_el):
    subgroups = {frozenset([id_el]): [id_el]}
    queue = [frozenset([id_el])]
    
    while queue:
        curr_fs = queue.pop(0)
        curr_gens = subgroups[curr_fs]
        for g in elements:
            if g not in curr_fs:
                new_gens = curr_gens + [g]
                new_fs = close_subgroup(new_gens)
                if new_fs not in subgroups:
                    subgroups[new_fs] = new_gens
                    queue.append(new_fs)
    return set(subgroups.keys())

def get_maximal_subgroups(G, elements, id_el):
    subgroups = get_all_subgroups(G, elements, id_el)
    G_fs = frozenset(elements)
    proper_subgroups = [H for H in subgroups if H != G_fs]
    maximal = []
    for H in proper_subgroups:
        is_maximal = True
        for K in proper_subgroups:
            if H != K and H.issubset(K):
                is_maximal = False
                break
        if is_maximal:
            maximal.append(H)
    return maximal

def frattini_subgroup(G, elements, id_el):
    maximals = get_maximal_subgroups(G, elements, id_el)
    if not maximals:
        return frozenset(elements)
    frattini = set(maximals[0])
    for M in maximals[1:]:
        frattini = frattini.intersection(M)
    return frozenset(frattini)

def get_automorphisms(G, elements, id_el):
    gens = G.generators
    if not gens:
        return [ {id_el: id_el} ]
    
    automorphisms = []
    orders = [get_order(g, id_el) for g in gens]
    valid_imgs_lists = []
    for order in orders:
        valid_imgs = [e for e in elements if get_order(e, id_el) == order]
        valid_imgs_lists.append(valid_imgs)
        
    for imgs in itertools.product(*valid_imgs_lists):
        mapping = {id_el: id_el}
        valid = True
        queue = [id_el]
        
        while queue:
            curr = queue.pop(0)
            for g, img in zip(gens, imgs):
                new_el = curr * g
                new_img = mapping[curr] * img
                if new_el in mapping:
                    if mapping[new_el] != new_img:
                        valid = False
                        break
                else:
                    mapping[new_el] = new_img
                    queue.append(new_el)
            if not valid:
                break
                
        if valid and len(set(mapping.values())) == len(elements):
            automorphisms.append(mapping)
            
    return automorphisms

def is_characteristic(G, H_fs, elements, id_el):
    autos = get_automorphisms(G, elements, id_el)
    for mapping in autos:
        mapped_H = frozenset(mapping[h] for h in H_fs)
        if mapped_H != H_fs:
            return False
    return True

def conditions(witness):
    try:
        if not hasattr(witness, 'generate') or not hasattr(witness, 'generators'):
            return [False, False]
        elements = list(witness.generate())
        if len(elements) > 1000:
            return [False, False]
        id_el = get_identity(elements)
    except Exception:
        return [False, False]
        
    try:
        phi_G = frattini_subgroup(witness, elements, id_el)
        is_char = is_characteristic(witness, phi_G, elements, id_el)
        neg_Q = not is_char
    except Exception:
        neg_Q = False
        
    return [True, neg_Q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "¬Q: \\Phi(G) is not a characteristic subgroup of G"
]
N_HYP = 1
NEG_Q_INDEX = 1