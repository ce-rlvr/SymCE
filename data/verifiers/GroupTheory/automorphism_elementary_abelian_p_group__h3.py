import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros
import itertools

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

def conditions(witness):
    try:
        p, n, G = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = bool(sympy.isprime(p))
    except Exception:
        h1 = False
        
    try:
        h2 = bool(int(n) == n and n > 0)
    except Exception:
        h2 = False
        
    try:
        n_int = int(n)
        p_int = int(p)
        gl_ord = 1
        for i in range(n_int):
            gl_ord *= (p_int**n_int - p_int**i)
            
        elements = []
        try:
            gen = G.generate()
        except Exception:
            gen = G
            
        for e in gen:
            elements.append(e)
            if len(elements) > 256:
                break
                
        if len(elements) > 256:
            neg_q = False
        else:
            n_elems = len(elements)
            if n_elems == 1:
                aut_count = 1
                neg_q = bool(aut_count != gl_ord)
            else:
                ident = G.identity
                elements = [ident] + [e for e in elements if e != ident]
                idx = {e: i for i, e in enumerate(elements)}
                mult_table = [[idx[e1 * e2] for e2 in elements] for e1 in elements]
                
                gens = []
                subgroup_elems = {0}
                for i in range(1, n_elems):
                    if i not in subgroup_elems:
                        gens.append(i)
                        subgroup_elems.add(i)
                        while True:
                            added = False
                            items = list(subgroup_elems)
                            for x in items:
                                for y in items:
                                    prod = mult_table[x][y]
                                    if prod not in subgroup_elems:
                                        subgroup_elems.add(prod)
                                        added = True
                            if not added:
                                break
                        if len(subgroup_elems) == n_elems:
                            break
                            
                if (n_elems - 1) ** len(gens) > 200000:
                    neg_q = False
                else:
                    aut_count = 0
                    for target_tuple in itertools.product(range(1, n_elems), repeat=len(gens)):
                        mapping = {0: 0}
                        for g_idx, t_idx in zip(gens, target_tuple):
                            mapping[g_idx] = t_idx
                            
                        queue = list(mapping.keys())
                        head = 0
                        is_hom = True
                        
                        while head < len(queue):
                            u = queue[head]
                            head += 1
                            for v in list(mapping.keys()):
                                uv = mult_table[u][v]
                                map_uv = mult_table[mapping[u]][mapping[v]]
                                if uv in mapping:
                                    if mapping[uv] != map_uv:
                                        is_hom = False
                                        break
                                else:
                                    mapping[uv] = map_uv
                                    queue.append(uv)
                                    
                                vu = mult_table[v][u]
                                map_vu = mult_table[mapping[v]][mapping[u]]
                                if vu in mapping:
                                    if mapping[vu] != map_vu:
                                        is_hom = False
                                        break
                                else:
                                    mapping[vu] = map_vu
                                    queue.append(vu)
                                    
                            if not is_hom:
                                break
                                
                        if is_hom and len(mapping) == n_elems and len(set(mapping.values())) == n_elems:
                            aut_count += 1
                            
                    neg_q = bool(aut_count != gl_ord)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: n is a positive integer",
    "¬Q: Aut(G) is not isomorphic to GL(n, p)"
]

N_HYP = 2
NEG_Q_INDEX = 2