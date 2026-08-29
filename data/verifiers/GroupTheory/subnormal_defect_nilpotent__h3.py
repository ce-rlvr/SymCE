import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup: named object bindings
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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        G, H = witness
    except Exception:
        return [False, False, False]
        
    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: G is nilpotent of class c
    try:
        if isinstance(G, PermutationGroup):
            h2 = G.is_nilpotent
        else:
            h2 = False
    except Exception:
        h2 = False
        
    # neg_Q: H is not a subnormal subgroup of G with subnormal defect at most c
    try:
        if not isinstance(G, PermutationGroup):
            c = 0
        else:
            c = len(G.lower_central_series()) - 1
            
        if not isinstance(H, PermutationGroup):
            neg_q = True
        else:
            is_sub = True
            for g in H.generators:
                try:
                    if not G.contains(g):
                        is_sub = False
                        break
                except Exception:
                    is_sub = False
                    break
                    
            if not is_sub:
                neg_q = True
            elif H.order() == 1:
                neg_q = False
            else:
                K = G
                defect = 0
                while K.order() > H.order():
                    gens = list(H.generators)
                    grp_gens = list(K.generators)
                    closure = PermutationGroup(gens)
                    while True:
                        old_order = closure.order()
                        new_gens = list(closure.generators)
                        for g in closure.generators:
                            for k in grp_gens:
                                new_gens.append(k**-1 * g * k)
                                new_gens.append(k * g * k**-1)
                        closure = PermutationGroup(new_gens)
                        if closure.order() == old_order:
                            break
                    next_K = closure
                    if next_K.order() == K.order():
                        defect = float('inf')
                        break
                    K = next_K
                    defect += 1
                neg_q = defect > c
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: G is nilpotent of class c",
    "¬Q: H is not a subnormal subgroup of G with subnormal defect at most c"
]

N_HYP = 2
NEG_Q_INDEX = 2