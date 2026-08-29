import math
import itertools
import functools
import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics import PermutationGroup
from sympy.matrices import eye, zeros

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

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 3:
            return [False] * 5
        G, H, K = witness
    except Exception:
        return [False] * 5

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: H is a normal subgroup of G
    try:
        h2 = False
        if h1 and isinstance(H, PermutationGroup):
            is_sub = True
            for g in H.generators:
                if g not in G:
                    is_sub = False
                    break
            if is_sub:
                is_norm = True
                for g in G.generators:
                    for h in H.generators:
                        if (g * h * ~g) not in H:
                            is_norm = False
                            break
                    if not is_norm:
                        break
                h2 = is_norm
    except Exception:
        h2 = False

    # H_3: K is a normal subgroup of G
    try:
        h3 = False
        if h1 and isinstance(K, PermutationGroup):
            is_sub = True
            for g in K.generators:
                if g not in G:
                    is_sub = False
                    break
            if is_sub:
                is_norm = True
                for g in G.generators:
                    for k in K.generators:
                        if (g * k * ~g) not in K:
                            is_norm = False
                            break
                    if not is_norm:
                        break
                h3 = is_norm
    except Exception:
        h3 = False

    # H_4: G is equal to the product set HK
    try:
        h4 = False
        if h1 and isinstance(H, PermutationGroup) and isinstance(K, PermutationGroup):
            H_els = list(H.generate())
            K_els = list(K.generate())
            HK = set()
            for h in H_els:
                for k in K_els:
                    HK.add(h * k)
            
            if len(HK) == G.order():
                h4 = True
                for x in HK:
                    if x not in G:
                        h4 = False
                        break
    except Exception:
        h4 = False

    # neg_Q: G is NOT isomorphic to the external direct product H x K
    try:
        neg_q = False
        if h1 and isinstance(H, PermutationGroup) and isinstance(K, PermutationGroup):
            if G.order() != H.order() * K.order():
                neg_q = True
            else:
                d1 = H.degree
                d2 = K.degree
                
                new_H_gens = []
                for g in H.generators:
                    arr = [g(i) for i in range(d1)] + list(range(d1, d1 + d2))
                    new_H_gens.append(Permutation(arr))
                    
                new_K_gens = []
                for g in K.generators:
                    arr = list(range(d1)) + [g(i) + d1 for i in range(d2)]
                    new_K_gens.append(Permutation(arr))
                    
                if not new_H_gens and not new_K_gens:
                    HxK = PermutationGroup([Permutation()])
                else:
                    HxK = PermutationGroup(new_H_gens + new_K_gens)
                
                if G.is_abelian != HxK.is_abelian:
                    neg_q = True
                else:
                    orders1 = sorted([g.order() for g in G.generate()])
                    orders2 = sorted([g.order() for g in HxK.generate()])
                    if orders1 != orders2:
                        neg_q = True
                    else:
                        try:
                            neg_q = not G.is_isomorphic(HxK)
                        except Exception:
                            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a normal subgroup of G",
    "H_3: K is a normal subgroup of G",
    "H_4: G is equal to the product set HK",
    "¬Q: G is not isomorphic to the external direct product H x K"
]

N_HYP = 4
NEG_Q_INDEX = 4