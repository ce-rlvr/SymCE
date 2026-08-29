import sympy
import sympy.ntheory
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation

# Top-level setup: named object bindings for witness expressions
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

def conditions(witness) -> list[bool]:
    try:
        G, H = witness
    except Exception:
        return [False, False, False]
        
    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: The index of H in G is a prime number
    try:
        if isinstance(G, PermutationGroup):
            order_G = G.order()
            if isinstance(H, PermutationGroup):
                order_H = H.order()
            elif isinstance(H, (list, set, tuple)):
                order_H = len(set(H))
            else:
                order_H = 0
                
            if order_H > 0 and order_G % order_H == 0:
                index = order_G // order_H
                h2 = sympy.ntheory.isprime(index)
            else:
                h2 = False
        else:
            h2 = False
    except Exception:
        h2 = False
        
    # neg_Q: H is NOT a maximal subgroup of G
    try:
        def is_maximal_subgroup(H, G):
            if not isinstance(G, PermutationGroup):
                return False
            
            if isinstance(H, (list, set, tuple)):
                for h in H:
                    if h not in G:
                        return False
                try:
                    H_group = PermutationGroup(list(H))
                    if H_group.order() != len(set(H)):
                        return False
                    H = H_group
                except Exception:
                    return False
                    
            if not isinstance(H, PermutationGroup):
                return False
                
            for gen in H.generators:
                if gen not in G:
                    return False
            if H.order() == G.order():
                return False
            
            for g in G.generate():
                if g not in H:
                    K = PermutationGroup(list(H.generators) + [g])
                    if K.order() < G.order():
                        return False
            return True
            
        neg_q = not is_maximal_subgroup(H, G)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = ["H_1: G is a group", "H_2: The index of H in G is a prime number", "neg_Q: H is not a maximal subgroup of G"]

N_HYP = 2
NEG_Q_INDEX = 2