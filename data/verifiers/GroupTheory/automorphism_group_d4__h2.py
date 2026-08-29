import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_automorphism_group(G):
    elements = list(G.generate())
    gens = G.generators
    
    identity = elements[0] ** 0
    for e in elements:
        if e.order() == 1:
            identity = e
            break
            
    words = {identity: []}
    queue = [identity]
    while queue:
        curr = queue.pop(0)
        for i, g in enumerate(gens):
            nxt = curr * g
            if nxt not in words:
                words[nxt] = words[curr] + [i]
                queue.append(nxt)
                
    elem_to_idx = {e: i for i, e in enumerate(elements)}
    
    n = len(elements)
    mult_table = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            mult_table[i][j] = elem_to_idx[elements[i] * elements[j]]
            
    automorphisms = []
    for target_gens in itertools.product(elements, repeat=len(gens)):
        possible = True
        for g, tg in zip(gens, target_gens):
            if g.order() != tg.order():
                possible = False
                break
        if not possible:
            continue
            
        mapping_idx = [0] * n
        for i, elem in enumerate(elements):
            val = identity
            for idx in words[elem]:
                val = val * target_gens[idx]
            mapping_idx[i] = elem_to_idx[val]
            
        if len(set(mapping_idx)) != n:
            continue
            
        is_homo = True
        for i in range(n):
            map_i = mapping_idx[i]
            for j in range(n):
                if mapping_idx[mult_table[i][j]] != mult_table[map_i][mapping_idx[j]]:
                    is_homo = False
                    break
            if not is_homo:
                break
                
        if is_homo:
            perm = Permutation(mapping_idx)
            automorphisms.append(perm)
            
    if not automorphisms:
        return PermutationGroup([Permutation(0)])
    return PermutationGroup(automorphisms)

def are_isomorphic(G1, G2):
    elems1 = list(G1.generate())
    elems2 = list(G2.generate())
    
    if len(elems1) != len(elems2):
        return False
        
    def is_ab(elems):
        for i in range(len(elems)):
            for j in range(i + 1, len(elems)):
                if elems[i] * elems[j] != elems[j] * elems[i]:
                    return False
        return True
        
    if is_ab(elems1) != is_ab(elems2):
        return False
        
    def ord_prof(elems):
        prof = {}
        for e in elems:
            o = e.order()
            prof[o] = prof.get(o, 0) + 1
        return prof
        
    if ord_prof(elems1) != ord_prof(elems2):
        return False
        
    if len(elems1) > 15:
        try:
            return G1.is_isomorphic(G2)
        except Exception:
            pass
            
    return True

def conditions(witness):
    try:
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False
        
    try:
        if not h1:
            neg_q = False
        else:
            aut_G = get_automorphism_group(witness)
            neg_q = not are_isomorphic(witness, aut_G)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "¬Q: The automorphism group of G is not isomorphic to G"
]

N_HYP = 1
NEG_Q_INDEX = 1