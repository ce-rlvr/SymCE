import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
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

def count_sylow_p_subgroups(G, p):
    order = G.order()
    p_power = 1
    while order % (p_power * p) == 0:
        p_power *= p
        
    if p_power == 1:
        return 1
        
    m = order // p_power
    candidates = [k for k in range(1, m + 1) if m % k == 0 and k % p == 1]
    if len(candidates) == 1:
        return candidates[0]
        
    P_sylow = G.sylow_subgroup(p)
    P_elements = frozenset(P_sylow.generate())
    
    orbit = {P_elements}
    queue = [P_elements]
    G_gens = G.generators
    
    while queue:
        current_P = queue.pop(0)
        for g in G_gens:
            next_P = frozenset(g * h * ~g for h in current_P)
            if next_P not in orbit:
                orbit.add(next_P)
                queue.append(next_P)
                
    return len(orbit)

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 4:
            return [False, False, False, False]
        G, p, n_p, P = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: G is a finite group
    try:
        h1_ok = isinstance(G, PermutationGroup) and G.order() > 0
    except Exception:
        h1_ok = False

    # H_2: p is a prime number
    try:
        h2_ok = bool(sympy.isprime(p))
    except Exception:
        h2_ok = False

    # H_3: n_p is the number of Sylow p-subgroups of G
    try:
        if h1_ok and h2_ok:
            actual_n_p = count_sylow_p_subgroups(G, p)
            h3_ok = (n_p == actual_n_p)
        else:
            h3_ok = False
    except Exception:
        h3_ok = False

    # ¬Q: n_p does not divide the index of P in G
    try:
        if h1_ok and isinstance(P, PermutationGroup):
            is_subgroup = True
            for gen in P.generators:
                if not G.contains(gen):
                    is_subgroup = False
                    break
            
            if is_subgroup:
                index = G.order() // P.order()
                neg_q_ok = (index % n_p != 0)
            else:
                neg_q_ok = False
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime number",
    "H_3: n_p is the number of Sylow p-subgroups of G",
    "¬Q: n_p does not divide the index of P in G"
]

N_HYP = 3
NEG_Q_INDEX = 3