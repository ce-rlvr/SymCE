import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Standard group theory bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(3), Permutation(0,1)(2,3), Permutation(0,2)(1,3), Permutation(0,3)(1,2))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def is_subgroup(H, G):
    try:
        return all(G.contains(g) for g in H.generators)
    except Exception:
        return False

def is_normal(N, G):
    if not is_subgroup(N, G):
        return False
    try:
        for n in N.generators:
            for g in G.generators:
                if not N.contains(g * n * ~g):
                    return False
                if not N.contains(~g * n * g):
                    return False
        return True
    except Exception:
        return False

def is_sylow_p_subgroup(P, G, p):
    if not is_subgroup(P, G):
        return False
    try:
        p = int(p)
    except Exception:
        return False
    if p <= 1:
        return False
        
    try:
        order_P = P.order()
        order_G = G.order()
        
        k = -1
        curr = 1
        for i in range(1000):
            if curr == order_P:
                k = i
                break
            if curr > order_P:
                break
            curr *= p
        if k == -1:
            return False
            
        if order_G % (p**(k+1)) == 0:
            return False
        if order_G % order_P != 0:
            return False
            
        return True
    except Exception:
        return False

def conditions(witness):
    try:
        if len(witness) == 4:
            G, N, P, p = witness
            p_list = [int(p)]
        elif len(witness) == 3:
            G, N, P = witness
            try:
                order_P = P.order()
                if order_P == 1:
                    order_G = G.order()
                    p_list = []
                    for p_cand in range(2, order_G + 2):
                        if order_G % p_cand != 0:
                            p_list.append(p_cand)
                            break
                else:
                    p_list = []
                    for p_cand in range(2, order_P + 1):
                        if order_P % p_cand == 0:
                            curr = 1
                            while curr < order_P:
                                curr *= p_cand
                            if curr == order_P:
                                p_list.append(p_cand)
            except Exception:
                p_list = []
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]
        
    # H1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup) and G.order() > 0
    except Exception:
        h1 = False
        
    # H2: N is a normal subgroup of G
    try:
        h2 = is_normal(N, G)
    except Exception:
        h2 = False
        
    h3 = False
    neg_q = False
    
    # Compute P \cap N
    try:
        if P.order() <= 10000:
            elements = [g for g in P.generate() if N.contains(g)]
            P_cap_N = PermutationGroup(elements)
        else:
            if hasattr(P, 'intersect'):
                P_cap_N = P.intersect(N)
            elif hasattr(P, 'intersection'):
                P_cap_N = P.intersection(N)
            else:
                P_cap_N = None
    except Exception:
        P_cap_N = None

    # H3: P is a Sylow p-subgroup of G
    # neg_Q: P \cap N is NOT a Sylow p-subgroup of N
    try:
        for p_cand in p_list:
            if is_sylow_p_subgroup(P, G, p_cand):
                h3 = True
                if P_cap_N is not None:
                    if not is_sylow_p_subgroup(P_cap_N, N, p_cand):
                        neg_q = True
                        break
    except Exception:
        pass
        
    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: N is a normal subgroup of G",
    "H_3: P is a Sylow p-subgroup of G",
    "¬Q: P \\cap N is not a Sylow p-subgroup of N"
]

N_HYP = 3
NEG_Q_INDEX = 3