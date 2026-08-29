import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics import PermutationGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import isprime
import math
import itertools
import functools

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_simple(G):
    try:
        order = G.order()
        if order <= 1 or order > 1000:
            return False
        if G.is_abelian:
            return isprime(order)
            
        elements = list(G.generate())
        n = len(elements)
        elem_to_idx = {e: i for i, e in enumerate(elements)}
        
        mult = [[0]*n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                mult[i][j] = elem_to_idx[elements[i] * elements[j]]
                
        id_idx = -1
        for i in range(n):
            if mult[i][i] == i:
                id_idx = i
                break
                
        inv_idx = [0] * n
        for i in range(n):
            for j in range(n):
                if mult[i][j] == id_idx:
                    inv_idx[i] = j
                    break
                    
        classes = []
        unseen = set(range(n))
        
        while unseen:
            rep = unseen.pop()
            c = set()
            for g in range(n):
                res = mult[mult[g][rep]][inv_idx[g]]
                c.add(res)
            classes.append(list(c))
            unseen -= c
            
        id_class_idx = -1
        for i, c in enumerate(classes):
            if id_idx in c:
                id_class_idx = i
                break
                
        class_sizes = [len(c) for c in classes]
        n_classes = len(classes)
        
        for r in range(2, n_classes):
            for subset in itertools.combinations(range(n_classes), r):
                if id_class_idx not in subset:
                    continue
                subset_size = sum(class_sizes[i] for i in subset)
                if order % subset_size != 0:
                    continue
                    
                union_elements = set()
                for i in subset:
                    union_elements.update(classes[i])
                    
                is_closed = True
                union_list = list(union_elements)
                for x in union_list:
                    for y in union_list:
                        if mult[x][y] not in union_elements:
                            is_closed = False
                            break
                    if not is_closed:
                        break
                if is_closed:
                    return False
                    
        return True
    except Exception:
        return False

def is_center_of_aut_trivial(G):
    try:
        order = G.order()
        if order > 1000:
            return True
            
        elements = list(G.generate())
        n = len(elements)
        if n == 1:
            return True
            
        elem_to_idx = {e: i for i, e in enumerate(elements)}
        mult_table = [[0]*n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                mult_table[i][j] = elem_to_idx[elements[i] * elements[j]]
                
        id_idx = -1
        for i in range(n):
            if mult_table[i][i] == i:
                id_idx = i
                break
        
        orders = [1] * n
        for i in range(n):
            if i == id_idx:
                continue
            curr = i
            ord_val = 1
            while curr != id_idx:
                curr = mult_table[curr][i]
                ord_val += 1
            orders[i] = ord_val
            
        gens = G.generators
        gen_indices = [elem_to_idx[g] for g in gens]
        gen_orders = [orders[g_idx] for g_idx in gen_indices]
        
        possible_targets = []
        for g_ord in gen_orders:
            targets = [i for i in range(n) if orders[i] == g_ord]
            possible_targets.append(targets)
            
        automorphisms = []
        
        for target_gen_indices in itertools.product(*possible_targets):
            phi = {id_idx: id_idx}
            queue = [id_idx]
            
            valid = True
            head = 0
            while head < len(queue):
                u = queue[head]
                head += 1
                for i, g_idx in enumerate(gen_indices):
                    v = mult_table[u][g_idx]
                    tg_idx = target_gen_indices[i]
                    tv = mult_table[phi[u]][tg_idx]
                    
                    if v in phi:
                        if phi[v] != tv:
                            valid = False
                            break
                    else:
                        phi[v] = tv
                        queue.append(v)
                if not valid:
                    break
                    
            if valid and len(phi) == n and len(set(phi.values())) == n:
                aut = tuple(phi[i] for i in range(n))
                automorphisms.append(aut)
                
        center_size = 0
        for f in automorphisms:
            is_central = True
            for g in automorphisms:
                for i in range(n):
                    if f[g[i]] != g[f[i]]:
                        is_central = False
                        break
                if not is_central:
                    break
            if is_central:
                center_size += 1
                
        return center_size == 1
    except Exception:
        return False

def conditions(witness):
    try:
        h1 = bool(not witness.is_abelian and is_simple(witness))
    except Exception:
        h1 = False
        
    try:
        neg_q = bool(not is_center_of_aut_trivial(witness))
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a non-abelian simple group",
    "¬Q: The center Z(A) is not the trivial subgroup"
]
N_HYP = 1
NEG_Q_INDEX = 1