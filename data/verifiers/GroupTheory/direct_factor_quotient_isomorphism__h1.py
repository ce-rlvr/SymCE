import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.permutations import Permutation
import math
import itertools
import functools

# Top-level setup: named object bindings
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

def get_order(G):
    try:
        return G.order()
    except TypeError:
        return G.order
    except Exception:
        return len(list(G.generate()))

def check_subgroup(H, G):
    try:
        return bool(H.is_subgroup(G))
    except AttributeError:
        elements_G = set(G.generate())
        return all(g in elements_G for g in H.generators)

def check_normal(H, G):
    try:
        return bool(H.is_normal(G))
    except AttributeError:
        elements_G = list(G.generate())
        elements_H = set(H.generate())
        for g in elements_G:
            g_inv = ~g
            for h in H.generators:
                if g * h * g_inv not in elements_H:
                    return False
        return True

def get_quotient_group(G, H):
    elements_G = list(G.generate())
    elements_H = list(H.generate())
    
    cosets = []
    coset_reps = []
    for g in elements_G:
        c = frozenset([g * h for h in elements_H])
        if c not in cosets:
            cosets.append(c)
            coset_reps.append(g)
            
    n = len(cosets)
    coset_to_idx = {c: i for i, c in enumerate(cosets)}
    
    gens = G.generators
    perms = []
    for gen in gens:
        p = [0] * n
        for j in range(n):
            rep_j = coset_reps[j]
            prod = rep_j * gen
            prod_coset = frozenset([prod * h for h in elements_H])
            p[j] = coset_to_idx[prod_coset]
        perms.append(Permutation(p))
        
    if not perms:
        perms = [Permutation([0])]
        
    return PermutationGroup(perms)

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 3:
            return [False, False, False, False, False]
        G, H, K = witness
    except Exception:
        return [False, False, False, False, False]

    # H_1: H is a normal subgroup of G
    try:
        h1 = check_subgroup(H, G) and check_normal(H, G)
    except Exception:
        h1 = False

    # H_2: K is a normal subgroup of G
    try:
        h2 = check_subgroup(K, G) and check_normal(K, G)
    except Exception:
        h2 = False

    # H_3: G is the set product HK
    try:
        if check_subgroup(H, G) and check_subgroup(K, G):
            elements_H = set(H.generate())
            elements_K = set(K.generate())
            intersection_order = len(elements_H.intersection(elements_K))
            h3 = bool(get_order(G) == (get_order(H) * get_order(K)) // intersection_order)
        else:
            h3 = False
    except Exception:
        h3 = False

    # H_4: The intersection of H and K contains only the identity element
    try:
        elements_H = set(H.generate())
        elements_K = set(K.generate())
        intersection_order = len(elements_H.intersection(elements_K))
        h4 = bool(intersection_order == 1)
    except Exception:
        h4 = False

    # neg_Q: G/H is NOT isomorphic to K
    try:
        if not h1:
            neg_q = True
        else:
            Q = get_quotient_group(G, H)
            neg_q = not bool(Q.is_isomorphic(K))
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: H is a normal subgroup of G",
    "H_2: K is a normal subgroup of G",
    "H_3: G is the set product HK",
    "H_4: The intersection of H and K contains only the identity element",
    "¬Q: G/H is not isomorphic to K"
]

N_HYP = 4
NEG_Q_INDEX = 4