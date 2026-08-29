import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics.named_groups import *
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        G, N = witness
    except Exception:
        return [False, False, False]

    # H1: G is a finite semisimple group
    # H2: G is the direct product of pairwise non-isomorphic simple groups
    try:
        elements = list(G.generate())
        id_el = G.identity
        
        if len(elements) == 1:
            h1 = True
            h2 = True
        else:
            seen = set([id_el])
            classes = []
            gens = G.generators
            for g in elements:
                if g not in seen:
                    c = set([g])
                    queue = [g]
                    while queue:
                        curr = queue.pop(0)
                        for gen in gens:
                            nxt1 = gen * curr * ~gen
                            if nxt1 not in c:
                                c.add(nxt1)
                                queue.append(nxt1)
                            nxt2 = ~gen * curr * gen
                            if nxt2 not in c:
                                c.add(nxt2)
                                queue.append(nxt2)
                    classes.append(c)
                    seen.update(c)
                    
            closures = []
            for c in classes:
                try:
                    H = PermutationGroup(list(c))
                    closure = set(H.generate())
                except Exception:
                    closure = set([id_el])
                    closure.update(c)
                    added = list(c)
                    while added:
                        new_added = []
                        for a in added:
                            for b in c:
                                prod = a * b
                                if prod not in closure:
                                    closure.add(prod)
                                    new_added.append(prod)
                        added = new_added
                closures.append(closure)
                
            unique_closures = []
            for M in closures:
                if M not in unique_closures:
                    unique_closures.append(M)
                    
            min_normals = []
            for M in unique_closures:
                if len(M) == 1:
                    continue
                is_minimal = True
                for K in unique_closures:
                    if len(K) == 1 or K == M:
                        continue
                    if K.issubset(M):
                        is_minimal = False
                        break
                if is_minimal:
                    min_normals.append(M)
                    
            h1 = True
            for M in min_normals:
                M_list = list(M)
                is_ab = True
                for i in range(len(M_list)):
                    for j in range(i + 1, len(M_list)):
                        if M_list[i] * M_list[j] != M_list[j] * M_list[i]:
                            is_ab = False
                            break
                    if not is_ab:
                        break
                if is_ab:
                    h1 = False
                    break
                    
            prod_sizes = 1
            sizes = []
            for M in min_normals:
                prod_sizes *= len(M)
                sizes.append(len(M))
                
            h2 = (prod_sizes == len(elements)) and (len(set(sizes)) == len(sizes))
    except Exception:
        h1 = False
        h2 = False

    # neg_Q: N is not a characteristic subgroup of G
    try:
        if not G.is_normal(N):
            neg_q = True
        else:
            N_elements = set(N.generate())
            if len(N_elements) == 1 or len(N_elements) == len(elements):
                neg_q = False
            else:
                gens = G.generators
                words = {id_el: []}
                queue = [id_el]
                while queue:
                    curr = queue.pop(0)
                    for i, g in enumerate(gens):
                        nxt = curr * g
                        if nxt not in words:
                            words[nxt] = words[curr] + [i]
                            queue.append(nxt)
                            
                gen_orders = [g.order() for g in gens]
                candidates = [[x for x in elements if x.order() == o] for o in gen_orders]
                
                is_char = True
                for p in itertools.product(*candidates):
                    try:
                        H_p = PermutationGroup(list(p))
                        if H_p.order() != len(elements):
                            continue
                    except Exception:
                        pass
                        
                    mapping = {id_el: id_el}
                    for x, word in words.items():
                        if x == id_el: continue
                        val = id_el
                        for idx in word:
                            val = val * p[idx]
                        mapping[x] = val
                        
                    if len(set(mapping.values())) != len(elements):
                        continue
                        
                    valid = True
                    for x in elements:
                        for i, g in enumerate(gens):
                            if mapping[x * g] != mapping[x] * p[i]:
                                valid = False
                                break
                        if not valid:
                            break
                            
                    if valid:
                        for n in N_elements:
                            if mapping[n] not in N_elements:
                                is_char = False
                                break
                    if not is_char:
                        break
                neg_q = not is_char
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite semisimple group",
    "H_2: G is the direct product of pairwise non-isomorphic simple groups",
    "¬Q: N is not a characteristic subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2