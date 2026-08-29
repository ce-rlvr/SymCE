import itertools
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

def get_mult_table(G):
    elements = list(G.generate())
    n = len(elements)
    if n > 100:
        raise ValueError("Group too large")
    
    id_elem = elements[0]**0
    elements.remove(id_elem)
    elements.insert(0, id_elem)
    
    elem_to_idx = {e: i for i, e in enumerate(elements)}
    mult_table = [[elem_to_idx[e1 * e2] for e2 in elements] for e1 in elements]
    return mult_table, n

def get_automorphisms(mult_table, n):
    gens = []
    subgroup = {0}
    for i in range(1, n):
        if i not in subgroup:
            gens.append(i)
            new_subgroup = set(subgroup)
            queue = [i]
            while queue:
                curr = queue.pop(0)
                new_subgroup.add(curr)
                for x in list(new_subgroup):
                    prod1 = mult_table[curr][x]
                    if prod1 not in new_subgroup:
                        new_subgroup.add(prod1)
                        queue.append(prod1)
                    prod2 = mult_table[x][curr]
                    if prod2 not in new_subgroup:
                        new_subgroup.add(prod2)
                        queue.append(prod2)
            subgroup = new_subgroup
            if len(subgroup) == n:
                break
                
    auts = set()
    for gen_images in itertools.product(range(n), repeat=len(gens)):
        p = {0: 0}
        queue = [0]
        
        valid = True
        for g, img in zip(gens, gen_images):
            if g in p:
                if p[g] != img:
                    valid = False
                    break
            else:
                p[g] = img
                queue.append(g)
                
        if not valid:
            continue
            
        head = 0
        while head < len(queue):
            x = queue[head]
            px = p[x]
            head += 1
            for y in queue[:head]:
                py = p[y]
                
                xy = mult_table[x][y]
                pxy = mult_table[px][py]
                if xy in p:
                    if p[xy] != pxy:
                        valid = False; break
                else:
                    p[xy] = pxy
                    queue.append(xy)
                
                yx = mult_table[y][x]
                pyx = mult_table[py][px]
                if yx in p:
                    if p[yx] != pyx:
                        valid = False; break
                else:
                    p[yx] = pyx
                    queue.append(yx)
            if not valid:
                break
                
        if valid and len(p) == n and len(set(p.values())) == n:
            auts.add(tuple(p[i] for i in range(n)))
            
    return auts

def get_inner_automorphisms(mult_table, n):
    inv_table = [0] * n
    for i in range(n):
        for j in range(n):
            if mult_table[i][j] == 0:
                inv_table[i] = j
                break
                
    inn_auts = set()
    for g in range(n):
        p = [0] * n
        for x in range(n):
            gx = mult_table[g][x]
            gxg_inv = mult_table[gx][inv_table[g]]
            p[x] = gxg_inv
        inn_auts.add(tuple(p))
            
    return inn_auts

def get_aut_mult_table(auts, n):
    id_aut = tuple(range(n))
    auts_list = list(auts)
    if id_aut in auts_list:
        auts_list.remove(id_aut)
    auts_list.insert(0, id_aut)
    
    aut_to_idx = {p: i for i, p in enumerate(auts_list)}
    k = len(auts_list)
    aut_mult_table = [[0]*k for _ in range(k)]
    for i, p1 in enumerate(auts_list):
        for j, p2 in enumerate(auts_list):
            comp = tuple(p1[p2[x]] for x in range(n))
            aut_mult_table[i][j] = aut_to_idx[comp]
    return aut_mult_table

def are_isomorphic(mult_table1, mult_table2):
    n = len(mult_table1)
    if len(mult_table2) != n:
        return False
    
    def get_orders(table):
        orders = []
        for i in range(n):
            curr = i
            order = 1
            while curr != 0:
                curr = table[curr][i]
                order += 1
            orders.append(order)
        return orders
        
    orders1 = get_orders(mult_table1)
    orders2 = get_orders(mult_table2)
    
    if sorted(orders1) != sorted(orders2):
        return False
        
    gens = []
    subgroup = {0}
    for i in range(1, n):
        if i not in subgroup:
            gens.append(i)
            new_subgroup = set(subgroup)
            queue = [i]
            while queue:
                curr = queue.pop(0)
                new_subgroup.add(curr)
                for x in list(new_subgroup):
                    prod1 = mult_table1[curr][x]
                    if prod1 not in new_subgroup:
                        new_subgroup.add(prod1)
                        queue.append(prod1)
                    prod2 = mult_table1[x][curr]
                    if prod2 not in new_subgroup:
                        new_subgroup.add(prod2)
                        queue.append(prod2)
            subgroup = new_subgroup
            if len(subgroup) == n:
                break
                
    candidates = [[j for j in range(n) if orders2[j] == orders1[g]] for g in gens]
    for gen_images in itertools.product(*candidates):
        p = {0: 0}
        queue = [0]
        valid = True
        for g, img in zip(gens, gen_images):
            if g in p:
                if p[g] != img:
                    valid = False; break
            else:
                p[g] = img
                queue.append(g)
        if not valid: continue
        
        head = 0
        while head < len(queue):
            x = queue[head]
            px = p[x]
            head += 1
            for y in queue[:head]:
                py = p[y]
                
                xy = mult_table1[x][y]
                pxy = mult_table2[px][py]
                if xy in p:
                    if p[xy] != pxy:
                        valid = False; break
                else:
                    p[xy] = pxy
                    queue.append(xy)
                    
                yx = mult_table1[y][x]
                pyx = mult_table2[py][px]
                if yx in p:
                    if p[yx] != pyx:
                        valid = False; break
                else:
                    p[yx] = pyx
                    queue.append(yx)
            if not valid:
                break
        if valid and len(p) == n and len(set(p.values())) == n:
            return True
    return False

def conditions(witness):
    try:
        mult_table, n = get_mult_table(witness)
        auts = get_automorphisms(mult_table, n)
    except Exception:
        return [False, False]

    try:
        inn_auts = get_inner_automorphisms(mult_table, n)
        h1 = (len(auts) == len(inn_auts))
    except Exception:
        h1 = False

    try:
        if len(auts) != n:
            neg_q = True
        else:
            aut_mult_table = get_aut_mult_table(auts, n)
            is_iso = are_isomorphic(mult_table, aut_mult_table)
            neg_q = not is_iso
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: Every automorphism of G is an inner automorphism",
    "¬Q: Aut(G) is not isomorphic to G"
]

N_HYP = 1
NEG_Q_INDEX = 1