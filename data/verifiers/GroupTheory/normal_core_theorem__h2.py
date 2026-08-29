import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import factorint
import math
from itertools import combinations

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

def conditions(witness) -> list[bool]:
    try:
        G, H = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    try:
        if hasattr(H, 'elements'):
            H_elements = list(set(H.elements))
        else:
            H_elements = list(set(H))
            
        if len(H_elements) == 0:
            h2 = False
            n = None
        elif not all(x in G for x in H_elements):
            h2 = False
            n = None
        else:
            order_G = G.order()
            if order_G % len(H_elements) == 0:
                h2 = True
                n = order_G // len(H_elements)
            else:
                h2 = False
                n = None
    except Exception:
        h2 = False
        n = None
        
    try:
        if not h1 or not h2:
            neg_q = False
        else:
            def divides_n_fact(k, n_val):
                if k <= n_val:
                    return True
                if n_val < 5000:
                    return math.factorial(n_val) % k == 0
                factors = factorint(k)
                for p, count in factors.items():
                    if p > n_val:
                        return False
                    c = 0
                    temp = n_val
                    while temp > 0:
                        c += temp // p
                        temp //= p
                    if c < count:
                        return False
                return True

            id_elem = G.identity
            
            if id_elem not in H_elements:
                conclusion_holds = False
            else:
                conclusion_holds = False
                H_without_id = [x for x in H_elements if x != id_elem]
                
                for r in range(len(H_without_id) + 1):
                    len_N = r + 1
                    if order_G % len_N != 0:
                        continue
                    index_N = order_G // len_N
                    if not divides_n_fact(index_N, n):
                        continue
                        
                    for combo in combinations(H_without_id, r):
                        N_set = set(combo)
                        N_set.add(id_elem)
                        
                        has_inverses = True
                        for a in N_set:
                            if ~a not in N_set:
                                has_inverses = False
                                break
                        if not has_inverses:
                            continue
                            
                        is_subgroup = True
                        for a in N_set:
                            for b in N_set:
                                if a * b not in N_set:
                                    is_subgroup = False
                                    break
                            if not is_subgroup:
                                break
                        if not is_subgroup:
                            continue
                            
                        is_normal = True
                        for gen in G.generators:
                            gen_inv = ~gen
                            for n_elem in N_set:
                                if gen * n_elem * gen_inv not in N_set:
                                    is_normal = False
                                    break
                            if not is_normal:
                                break
                                
                        if is_normal:
                            conclusion_holds = True
                            break
                    if conclusion_holds:
                        break
            
            neg_q = not conclusion_holds
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: The index of H in G is finite and equal to n",
    "¬Q: No normal subgroup N of G exists such that N is a subset of H and the index of N divides n factorial"
]

N_HYP = 2
NEG_Q_INDEX = 2