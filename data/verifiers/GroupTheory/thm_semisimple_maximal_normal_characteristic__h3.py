import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup for standard groups
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

def parse_witness(witness):
    if isinstance(witness, tuple):
        if len(witness) == 2:
            return witness[0], witness[1], None
        elif len(witness) == 3:
            return witness[0], witness[1], witness[2]
    return None, None, None

def is_semisimple(N):
    if N.order() > 20000:
        return False
    if N.order() == 1:
        return True
        
    identity = N.identity
    checked = {identity}
    
    elements = []
    queue = [identity]
    visited = {identity}
    while queue:
        curr = queue.pop(0)
        elements.append(curr)
        for g in N.generators:
            nxt = curr * g
            if nxt not in visited:
                visited.add(nxt)
                queue.append(nxt)
                
    for x in elements:
        if x in checked:
            continue
            
        conjugates = {x}
        q = [x]
        while q:
            c = q.pop(0)
            for g in N.generators:
                conj = g * c * ~g
                if conj not in conjugates:
                    conjugates.add(conj)
                    q.append(conj)
                    
        checked.update(conjugates)
        
        is_abelian = True
        conj_list = list(conjugates)
        for i in range(len(conj_list)):
            for j in range(i + 1, len(conj_list)):
                if conj_list[i] * conj_list[j] != conj_list[j] * conj_list[i]:
                    is_abelian = False
                    break
            if not is_abelian:
                break
                
        if is_abelian:
            return False
            
    return True

def check_H2(G, N):
    if not isinstance(N, PermutationGroup):
        return False
    for n in N.generators:
        if not G.contains(n):
            return False
    for g in G.generators:
        for n in N.generators:
            if not N.contains(g * n * ~g):
                return False
    return is_semisimple(N)

def check_neg_Q(G, N, phi_dict):
    if phi_dict is not None:
        mapping = {G.identity: G.identity}
        queue = [G.identity]
        while queue:
            curr = queue.pop(0)
            for g in G.generators:
                nxt = curr * g
                if nxt not in mapping:
                    mapping[nxt] = mapping[curr] * phi_dict[g]
                    queue.append(nxt)
                else:
                    if mapping[nxt] != mapping[curr] * phi_dict[g]:
                        return False
        
        if len(set(mapping.values())) != G.order():
            return False
            
        for n in N.generators:
            if not N.contains(mapping[n]):
                return True
        return False
        
    if G.order() > 20000:
        return False
        
    classes = []
    visited = set()
    queue = [G.identity]
    visited_el = {G.identity}
    while queue:
        curr = queue.pop(0)
        if curr not in visited:
            cls = {curr}
            q = [curr]
            while q:
                c = q.pop(0)
                for g in G.generators:
                    conj = g * c * ~g
                    if conj not in cls:
                        cls.add(conj)
                        q.append(conj)
            classes.append(cls)
            visited.update(cls)
            
        for g in G.generators:
            nxt = curr * g
            if nxt not in visited_el:
                visited_el.add(nxt)
                queue.append(nxt)
                
    id_class = None
    other_classes = []
    target_size = N.order()
    for c in classes:
        if G.identity in c:
            id_class = c
        elif len(c) < target_size:
            other_classes.append(c)
            
    target = target_size - 1
    valid_subgroups = []
    
    def get_subsets(index, current_sum, current_subset):
        if current_sum == target:
            elements = set(id_class)
            for c in current_subset:
                elements.update(c)
            
            is_subgroup = True
            elements_list = list(elements)
            for x in elements_list:
                for y in elements_list:
                    if x * y not in elements:
                        is_subgroup = False
                        break
                if not is_subgroup:
                    break
            if is_subgroup:
                if not any(elements == v for v in valid_subgroups):
                    valid_subgroups.append(elements)
            return
            
        if index >= len(other_classes) or current_sum > target:
            return
            
        get_subsets(index + 1, current_sum, current_subset)
        
        c = other_classes[index]
        if current_sum + len(c) <= target:
            get_subsets(index + 1, current_sum + len(c), current_subset + [c])
            
    get_subsets(0, 0, [])
    
    if len(valid_subgroups) > 1:
        return True
    else:
        return False

def conditions(witness):
    try:
        G, N, phi_dict = parse_witness(witness)
        if G is None:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    try:
        h2 = check_H2(G, N)
    except Exception:
        h2 = False
        
    try:
        neg_q = check_neg_Q(G, N, phi_dict)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: N is a normal semisimple subgroup of G",
    "¬Q: N is not a characteristic subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2