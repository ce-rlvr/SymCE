import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "¬Q: The composition series S_1 and S_2 do not have the same length, or their multisets of composition factors are not isomorphic up to permutation"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        G, S1, S2 = witness
    except Exception:
        return [False, False]
        
    # H_1: G is a finite group
    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False
        
    # neg_Q: The conclusion fails
    try:
        if not isinstance(S1, (list, tuple)) or not isinstance(S2, (list, tuple)):
            neg_q_ok = True
        elif len(S1) != len(S2):
            neg_q_ok = True
        else:
            def get_factors(S):
                sigs = []
                for i in range(len(S)-1):
                    G_i = S[i]
                    H_i = S[i+1]
                    
                    if not hasattr(G_i, 'generators') or not hasattr(H_i, 'generators'):
                        return None
                    if not hasattr(G_i, 'order') or not hasattr(H_i, 'order'):
                        return None
                        
                    try:
                        # Check if H_i is a subgroup of G_i
                        if not all(h in G_i for h in H_i.generators):
                            return None
                            
                        # Check if H_i is normal in G_i
                        normal = True
                        for g in G_i.generators:
                            for h in H_i.generators:
                                if (g * h * ~g) not in H_i or (~g * h * g) not in H_i:
                                    normal = False
                                    break
                            if not normal:
                                break
                        if not normal:
                            return None
                            
                        order = G_i.order() // H_i.order()
                    except Exception:
                        return None
                        
                    q_orders = None
                    if G_i.order() <= 256:
                        try:
                            elements = list(G_i.generate())
                            cosets = []
                            for g in elements:
                                found = False
                                for c in cosets:
                                    if (~c * g) in H_i:
                                        found = True
                                        break
                                if not found:
                                    cosets.append(g)
                                    
                            q_orders_list = []
                            for g in cosets:
                                k = 1
                                curr = g
                                while curr not in H_i:
                                    curr = curr * g
                                    k += 1
                                q_orders_list.append(k)
                            q_orders = tuple(sorted(q_orders_list))
                        except Exception:
                            pass
                            
                    try:
                        D = G_i.derived_subgroup()
                        is_ab = all(g in H_i for g in D.generators)
                    except Exception:
                        is_ab = False
                        
                    sigs.append((order, is_ab, q_orders))
                return sorted(sigs)
                
            f1 = get_factors(S1)
            f2 = get_factors(S2)
            
            if f1 is None or f2 is None:
                neg_q_ok = True
            elif f1 != f2:
                neg_q_ok = True
            else:
                neg_q_ok = False
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]