import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3)])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def direct_product(G, H):
    degG = G.degree
    degH = H.degree
    gens = []
    for g in G.generators:
        arr = [g(i) for i in range(degG)] + list(range(degG, degG + degH))
        gens.append(Permutation(arr))
    for h in H.generators:
        arr = list(range(degG)) + [h(i) + degG for i in range(degH)]
        gens.append(Permutation(arr))
    if not gens:
        return PermutationGroup([Permutation(0)])
    return PermutationGroup(gens)

def count_automorphisms(G):
    try:
        elements = list(G.elements)
    except AttributeError:
        return 0
    n = len(elements)
    if n <= 1:
        return 1
    
    id_idx = -1
    for i, e in enumerate(elements):
        if e.is_Identity:
            id_idx = i
            break
    if id_idx == -1:
        return 0
    elements[0], elements[id_idx] = elements[id_idx], elements[0]
    
    elem_to_idx = {e: i for i, e in enumerate(elements)}
    
    mult = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            mult[i][j] = elem_to_idx[elements[i] * elements[j]]
            
    orders = [1]*n
    for i in range(n):
        curr = elements[i]
        o = 1
        while not curr.is_Identity:
            curr = curr * elements[i]
            o += 1
        orders[i] = o
        
    from collections import defaultdict
    by_order = defaultdict(list)
    for i in range(n):
        by_order[orders[i]].append(i)
        
    gens_idx = []
    subgroup_elements = {0}
    for i in range(1, n):
        if i not in subgroup_elements:
            gens_idx.append(i)
            new_subgroup = set(subgroup_elements)
            queue = [i]
            new_subgroup.add(i)
            head = 0
            while head < len(queue):
                x = queue[head]
                head += 1
                for y in list(new_subgroup):
                    z1 = mult[x][y]
                    if z1 not in new_subgroup:
                        new_subgroup.add(z1)
                        queue.append(z1)
                    z2 = mult[y][x]
                    if z2 not in new_subgroup:
                        new_subgroup.add(z2)
                        queue.append(z2)
            subgroup_elements = new_subgroup
            if len(subgroup_elements) == n:
                break
                
    def get_closure(mapping):
        extended = {0: 0}
        queue = []
        for g, img in mapping.items():
            extended[g] = img
            queue.append(g)
            
        head = 0
        while head < len(queue):
            x = queue[head]
            head += 1
            for y in list(extended.keys()):
                z = mult[x][y]
                img_z = mult[extended[x]][extended[y]]
                if z in extended:
                    if extended[z] != img_z:
                        return None
                else:
                    extended[z] = img_z
                    queue.append(z)
                
                z = mult[y][x]
                img_z = mult[extended[y]][extended[x]]
                if z in extended:
                    if extended[z] != img_z:
                        return None
                else:
                    extended[z] = img_z
                    queue.append(z)
        return extended

    count = 0
    def backtrack(gen_idx_pos, current_mapping):
        nonlocal count
        if gen_idx_pos == len(gens_idx):
            ext = get_closure(current_mapping)
            if ext is not None and len(ext) == n and len(set(ext.values())) == n:
                count += 1
            return
            
        g = gens_idx[gen_idx_pos]
        for img in by_order[orders[g]]:
            new_mapping = current_mapping.copy()
            new_mapping[g] = img
            ext = get_closure(new_mapping)
            if ext is not None:
                backtrack(gen_idx_pos + 1, new_mapping)
                
    backtrack(0, {0: 0})
    return count

def conditions(witness) -> list[bool]:
    try:
        G, H = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    try:
        h2 = isinstance(H, PermutationGroup)
    except Exception:
        h2 = False
        
    try:
        if not (h1 and h2):
            neg_q = False
        else:
            GxH = direct_product(G, H)
            aut_G = count_automorphisms(G)
            aut_H = count_automorphisms(H)
            aut_GxH = count_automorphisms(GxH)
            # If the sizes of the automorphism groups differ, they cannot be isomorphic.
            # For finite groups G, H where gcd(|G|, |H|) != 1, this size check is sufficient.
            neg_q = (aut_GxH != aut_G * aut_H)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: H is a finite group",
    "¬Q: Aut(G x H) is not isomorphic to Aut(G) x Aut(H)"
]

N_HYP = 2
NEG_Q_INDEX = 2