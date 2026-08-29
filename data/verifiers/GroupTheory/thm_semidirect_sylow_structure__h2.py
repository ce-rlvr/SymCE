import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import isprime, factorint

# Top-level setup for witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3)])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def is_subgroup(sub, group):
    try:
        if sub.order() > group.order():
            return False
        return all(group.contains(g) for g in sub.generators)
    except Exception:
        return False

def is_normal(sub, group):
    try:
        if not is_subgroup(sub, group): 
            return False
        for g in group.generators:
            for n in sub.generators:
                if not sub.contains(g * n * ~g):
                    return False
                if not sub.contains(~g * n * g):
                    return False
        return True
    except Exception:
        return False

def conditions(witness):
    try:
        if len(witness) == 6:
            G, N, H, P_N, P_H, p = witness
        elif len(witness) == 4:
            G, N, H, p = witness
            P_N = N.sylow_subgroup(p)
            P_H = H.sylow_subgroup(p)
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: G = N \rtimes H is a finite semidirect product
    try:
        h1 = False
        if is_subgroup(N, G) and is_subgroup(H, G):
            if is_normal(N, G):
                gens_NH = list(N.generators) + list(H.generators)
                if not gens_NH:
                    gens_NH = [Permutation()]
                NH_group = PermutationGroup(gens_NH)
                if NH_group.order() == G.order() and N.order() * H.order() == G.order():
                    h1 = True
    except Exception:
        h1 = False

    # H_2: N has a normal Sylow p-subgroup P_N
    try:
        h2 = False
        if isprime(p):
            if is_subgroup(P_N, N):
                if is_normal(P_N, N):
                    order_N = N.order()
                    factors = factorint(order_N)
                    max_p_power = p ** factors.get(p, 0)
                    if P_N.order() == max_p_power:
                        h2 = True
    except Exception:
        h2 = False

    # H_3: H has a Sylow p-subgroup P_H
    try:
        h3 = False
        if isprime(p):
            if is_subgroup(P_H, H):
                order_H = H.order()
                factors = factorint(order_H)
                max_p_power = p ** factors.get(p, 0)
                if P_H.order() == max_p_power:
                    h3 = True
    except Exception:
        h3 = False

    # ¬Q: P_N \rtimes P_H does not form a Sylow p-subgroup of G
    try:
        q = False
        gens_K = list(P_N.generators) + list(P_H.generators)
        if not gens_K:
            gens_K = [Permutation()]
        K = PermutationGroup(gens_K)
        K_order = K.order()
        
        # Check if P_N P_H is a subgroup (order must be exactly |P_N| * |P_H|)
        if K_order == P_N.order() * P_H.order():
            order_G = G.order()
            factors = factorint(order_G)
            max_p_power = p ** factors.get(p, 0)
            # Check if it is a Sylow p-subgroup of G
            if K_order == max_p_power:
                q = True
    except Exception:
        q = False

    return [h1, h2, h3, not q]

CONDITION_LABELS = [
    "H_1: G = N \\rtimes H is a finite semidirect product",
    "H_2: N has a normal Sylow p-subgroup P_N",
    "H_3: H has a Sylow p-subgroup P_H",
    "¬Q: P_N \\rtimes P_H does not form a Sylow p-subgroup of G"
]

N_HYP = 3
NEG_Q_INDEX = 3