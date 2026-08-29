import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros
from itertools import combinations, product

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

# V4 as the Klein four-group
V4 = PermutationGroup(Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]]))

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: N is a normal semisimple subgroup of G",
    "H_2: There is no normal semisimple subgroup of G that strictly contains N",
    "¬Q: N is not a characteristic subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2

def get_elements(obj):
    if hasattr(obj, 'generate'):
        return frozenset(obj.generate())
    elif hasattr(obj, 'elements'):
        return frozenset(obj.elements)
    else:
        return frozenset(obj)

def is_normal(G_elements, N_elements):
    if not N_elements.issubset(G_elements):
        return False
    id_elem = None
    for g in G_elements:
        if g.is_Identity:
            id_elem = g
            break
    if id_elem not in N_elements:
        return False
    for x in N_elements:
        for y in N_elements:
            if x * y not in N_elements:
                return False
    for n in N_elements:
        for g in G_elements:
            if g * n * ~g not in N_elements:
                return False
    return True

def is_simple_group(subset):
    if len(subset) <= 1:
        return False
    elements = list(subset)
    classes = []
    unseen = set(elements)
    while unseen:
        x = unseen.pop()
        cls = set()
        for g in elements:
            c = g * x * ~g
            cls.add(c)
        classes.append(cls)
        unseen -= cls
        
    id_class = None
    for c in classes:
        if list(c)[0].is_Identity:
            id_class = c
            break
    other_classes = [c for c in classes if c != id_class]
    
    count = 0
    for r in range(len(other_classes) + 1):
        for combo in combinations(other_classes, r):
            sub = set(id_class)
            for c in combo:
                sub.update(c)
            is_subgroup = True
            for x in sub:
                for y in sub:
                    if x * y not in sub:
                        is_subgroup = False
                        break
                if not is_subgroup:
                    break
            if is_subgroup:
                count += 1
                if count > 2:
                    return False
    return count == 2

def is_semisimple(subset):
    if not subset:
        return False
    id_elem = None
    for g in subset:
        if g.is_Identity:
            id_elem = g
            break
    if id_elem is None:
        return False
        
    if len(subset) == 1:
        return True
        
    elements = list(subset)
    classes = []
    unseen = set(elements)
    while unseen:
        x = unseen.pop()
        cls = set()
        for g in elements:
            c = g * x * ~g
            cls.add(c)
        classes.append(cls)
        unseen -= cls
        
    id_class = None
    for c in classes:
        if id_elem in c:
            id_class = c
            break
    other_classes = [c for c in classes if c != id_class]
    
    normal_subs = []
    for r in range(len(other_classes) + 1):
        for combo in combinations(other_classes, r):
            sub = set(id_class)
            for c in combo:
                sub.update(c)
            is_subgroup = True
            for x in sub:
                for y in sub:
                    if x * y not in sub:
                        is_subgroup = False
                        break
                if not is_subgroup:
                    break
            if is_subgroup:
                normal_subs.append(frozenset(sub))
                
    simple_normal_subs = [ns for ns in normal_subs if is_simple_group(ns)]
    
    generated = set([id_elem])
    for ns in simple_normal_subs:
        generated.update(ns)
        
    while True:
        new_elements = set()
        for x in generated:
            for y in generated:
                xy = x * y
                if xy not in generated:
                    new_elements.add(xy)
        if not new_elements:
            break
        generated.update(new_elements)
        
    return len(generated) == len(subset)

def is_maximal_normal_semisimple(G_elements, N_elements):
    if not is_normal(G_elements, N_elements):
        return False
    if not is_semisimple(N_elements):
        return False
        
    elements = list(G_elements)
    classes = []
    unseen = set(elements)
    while unseen:
        x = unseen.pop()
        cls = set()
        for g in elements:
            c = g * x * ~g
            cls.add(c)
        classes.append(cls)
        unseen -= cls
        
    id_class = None
    for c in classes:
        if list(c)[0].is_Identity:
            id_class = c
            break
    other_classes = [c for c in classes if c != id_class]
    
    for r in range(len(other_classes) + 1):
        for combo in combinations(other_classes, r):
            sub = set(id_class)
            for c in combo:
                sub.update(c)
            if not N_elements.issubset(sub):
                continue
            if len(sub) == len(N_elements):
                continue
                
            is_subgroup = True
            for x in sub:
                for y in sub:
                    if x * y not in sub:
                        is_subgroup = False
                        break
                if not is_subgroup:
                    break
            if is_subgroup:
                if is_semisimple(frozenset(sub)):
                    return False
    return True

def is_characteristic(G_elements, N_elements):
    if not N_elements.issubset(G_elements):
        return False
        
    G_list = list(G_elements)
    id_elem = None
    for g in G_list:
        if g.is_Identity:
            id_elem = g
            break
            
    gens = []
    current_gen = {id_elem}
    for g in G_list:
        if g not in current_gen:
            gens.append(g)
            current_gen.add(g)
            while True:
                new_elements = set()
                for x in current_gen:
                    for y in current_gen:
                        xy = x * y
                        if xy not in current_gen:
                            new_elements.add(xy)
                if not new_elements:
                    break
                current_gen.update(new_elements)
            if len(current_gen) == len(G_list):
                break
                
    elem_to_idx = {g: i for i, g in enumerate(G_list)}
    n = len(G_list)
    mult_table = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            mult_table[i][j] = elem_to_idx[G_list[i] * G_list[j]]
            
    orders = []
    id_idx = elem_to_idx[id_elem]
    for i in range(n):
        curr = i
        order = 1
        while curr != id_idx:
            curr = mult_table[curr][i]
            order += 1
        orders.append(order)
        
    gen_indices = [elem_to_idx[g] for g in gens]
    gen_orders = [orders[g] for g in gen_indices]
    
    target_choices = [ [j for j in range(n) if orders[j] == gen_orders[k]] for k in range(len(gens)) ]
    
    for target_gen_indices in product(*target_choices):
        mapping = {id_idx: id_idx}
        queue = [(id_idx, id_idx)]
        conflict = False
        for g_idx, t_idx in zip(gen_indices, target_gen_indices):
            if g_idx in mapping and mapping[g_idx] != t_idx:
                conflict = True
                break
            if g_idx not in mapping:
                mapping[g_idx] = t_idx
                queue.append((g_idx, t_idx))
                
        if conflict:
            continue
            
        head = 0
        while head < len(queue):
            x, fx = queue[head]
            head += 1
            for y, fy in list(mapping.items()):
                xy = mult_table[x][y]
                fx_fy = mult_table[fx][fy]
                if xy in mapping:
                    if mapping[xy] != fx_fy:
                        conflict = True
                        break
                else:
                    mapping[xy] = fx_fy
                    queue.append((xy, fx_fy))
                    
                yx = mult_table[y][x]
                fy_fx = mult_table[fy][fx]
                if yx in mapping:
                    if mapping[yx] != fy_fx:
                        conflict = True
                        break
                else:
                    mapping[yx] = fy_fx
                    queue.append((yx, fy_fx))
            if conflict:
                break
                
        if conflict:
            continue
            
        if len(mapping) == n and len(set(mapping.values())) == n:
            N_indices = {elem_to_idx[g] for g in N_elements}
            mapped_N = {mapping[idx] for idx in N_indices}
            if mapped_N != N_indices:
                return False
                
    return True

def conditions(witness):
    try:
        G, N = witness
        G_elems = get_elements(G)
        N_elems = get_elements(N)
        
        if not G_elems:
            return [False, False, False]
            
        max_size = max([p.size for p in G_elems | N_elems])
        
        def pad(p):
            if p.size < max_size:
                return Permutation(p.array_form + list(range(p.size, max_size)))
            return p
            
        G_elements = frozenset(pad(p) for p in G_elems)
        N_elements = frozenset(pad(p) for p in N_elems)
    except Exception:
        return [False, False, False]
        
    try:
        h1 = is_normal(G_elements, N_elements) and is_semisimple(N_elements)
    except Exception:
        h1 = False
        
    try:
        h2 = is_maximal_normal_semisimple(G_elements, N_elements)
    except Exception:
        h2 = False
        
    try:
        neg_q = not is_characteristic(G_elements, N_elements)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]