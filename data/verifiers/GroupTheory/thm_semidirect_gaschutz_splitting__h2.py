import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import sympy.ntheory
import math
import itertools
import functools

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

def get_identity(G):
    if G.generators:
        return G.generators[0] ** 0
    return Permutation()

def is_normal(N, G):
    try:
        if not N.is_subgroup(G):
            return False
        N_elements = set(N.generate())
        for g in G.generators:
            for n in N.generators:
                if (g * n * ~g) not in N_elements:
                    return False
        return True
    except Exception:
        return False

def is_p_group(N, p):
    try:
        order = N.order()
        if order == 1:
            return True
        factors = sympy.ntheory.factorint(order)
        return list(factors.keys()) == [p]
    except Exception:
        return False

def is_sylow_p_subgroup(P, G, p):
    try:
        if not P.is_subgroup(G):
            return False
        if not is_p_group(P, p):
            return False
        order_G = G.order()
        order_P = P.order()
        return order_G % (order_P * p) != 0
    except Exception:
        return False

def has_complement(N, G):
    try:
        if not N.is_subgroup(G):
            return False
        order_G = G.order()
        order_N = N.order()
        if order_G % order_N != 0:
            return False
        target_order = order_G // order_N
        if target_order == 1:
            return True
        if target_order == order_G:
            return True
            
        N_set = set(N.generate())
        identity = get_identity(G)
        
        cands = []
        for g in G.generate():
            if target_order % g.order() == 0:
                if g == identity or g not in N_set:
                    cands.append(g)
                    
        cands.sort(key=lambda x: x.order(), reverse=True)
        
        def search(current_H_set, cands_left):
            if len(current_H_set) == target_order:
                return True
            for i, g in enumerate(cands_left):
                if g in current_H_set:
                    continue
                
                new_H = set(current_H_set)
                queue = [g]
                queue_set = {g}
                valid = True
                while queue:
                    x = queue.pop(0)
                    queue_set.remove(x)
                    if x in new_H:
                        continue
                    
                    to_add = set()
                    for y in new_H:
                        xy = x * y
                        if xy not in new_H: to_add.add(xy)
                        yx = y * x
                        if yx not in new_H: to_add.add(yx)
                    xx = x * x
                    if xx not in new_H: to_add.add(xx)
                    to_add.add(x)
                    
                    for e in to_add:
                        if e in N_set and e != identity:
                            valid = False
                            break
                        if e not in new_H and e not in queue_set:
                            queue.append(e)
                            queue_set.add(e)
                    if not valid:
                        break
                    new_H.update(to_add)
                    if len(new_H) > target_order:
                        valid = False
                        break
                
                if valid:
                    if search(new_H, cands_left[i+1:]):
                        return True
            return False

        return search({identity}, cands)
    except Exception:
        return False

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            N = witness.get('N')
            P = witness.get('P')
            p = witness.get('p')
        else:
            G, N, P, p = witness
    except Exception:
        return [False] * 5

    try:
        h1 = isinstance(G, PermutationGroup) and G.order() > 0
    except Exception:
        h1 = False

    try:
        h2 = (isinstance(N, PermutationGroup) and 
              N.is_subgroup(G) and 
              N.is_abelian and 
              is_normal(N, G) and 
              is_p_group(N, p))
    except Exception:
        h2 = False

    try:
        h3 = (isinstance(P, PermutationGroup) and 
              is_sylow_p_subgroup(P, G, p))
    except Exception:
        h3 = False

    try:
        h4 = has_complement(N, P)
    except Exception:
        h4 = False

    try:
        neg_q = not has_complement(N, G)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(h4), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: N is an abelian normal p-subgroup of G",
    "H_3: P is a Sylow p-subgroup of G",
    "H_4: There exists a complement of N in P",
    "¬Q: There does not exist a complement of N in G"
]

N_HYP = 4
NEG_Q_INDEX = 4