import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros
import itertools
import functools
import math

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
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_characteristic(G, H):
    try:
        elements = list(G.elements)
        idx = {e: i for i, e in enumerate(elements)}
        n = len(elements)
        table = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                table[i][j] = idx[elements[i] * elements[j]]
                
        gens = G.generators
        gen_indices = [idx[g] for g in gens]
        
        orders = [e.order() for e in elements]
        gen_targets = []
        for g in gen_indices:
            targets = [i for i in range(n) if orders[i] == orders[g]]
            gen_targets.append(targets)
            
        def expand_map(gen_map):
            mapping = {idx[G.identity]: idx[G.identity]}
            queue = [idx[G.identity]]
            head = 0
            while head < len(queue):
                curr = queue[head]
                head += 1
                for g, t_g in gen_map.items():
                    prod = table[curr][g]
                    t_prod = table[mapping[curr]][t_g]
                    if prod in mapping:
                        if mapping[prod] != t_prod:
                            return None
                    else:
                        mapping[prod] = t_prod
                        queue.append(prod)
            if len(mapping) == n and len(set(mapping.values())) == n:
                return mapping
            return None

        H_indices = set(idx[h] for h in H.elements)
        
        for target_tuple in itertools.product(*gen_targets):
            gen_map = dict(zip(gen_indices, target_tuple))
            mapping = expand_map(gen_map)
            if mapping is not None:
                mapped_H = set(mapping[h] for h in H_indices)
                if mapped_H != H_indices:
                    return False
                    
        return True
    except Exception:
        return None

def conditions(witness):
    try:
        G, H = witness
    except Exception:
        return [False, False]
        
    try:
        h1 = False
        if hasattr(H, 'generators') and hasattr(G, '__contains__'):
            h1 = all(g in G for g in H.generators)
    except Exception:
        h1 = False
        
    try:
        if not h1:
            neg_q = False
        else:
            char_check = is_characteristic(G, H)
            if char_check is None:
                neg_q = False
            else:
                neg_q = not char_check
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: H is a subgroup of G",
    "¬Q: H is not a characteristic subgroup of G"
]

N_HYP = 1
NEG_Q_INDEX = 1