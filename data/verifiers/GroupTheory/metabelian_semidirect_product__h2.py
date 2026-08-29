import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics import Permutation, PermutationGroup
import itertools
import math
import functools

# Top-level setup: named object bindings that the witness expression may reference
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
V4 = PermutationGroup([Permutation(0,1)(2,3), Permutation(0,2)(1,3)])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def is_semidirect_product(N, H, G):
    try:
        if N.order() * H.order() != G.order():
            return False
    except Exception:
        return False

    # 1. Check if N and H are provided as actual subgroups of G
    try:
        n_is_sub = all(G.contains(g) for g in N.generators)
        h_is_sub = all(G.contains(g) for g in H.generators)
        if n_is_sub and h_is_sub:
            is_normal = True
            for n in N.generators:
                for g in G.generators:
                    if not N.contains(g * n * ~g):
                        is_normal = False
                        break
                if not is_normal:
                    break
            if is_normal:
                int_size = sum(1 for x in N.generate() if H.contains(x))
                if int_size == 1:
                    return True
    except Exception:
        pass

    # 2. Check if G is a direct product of N and H (both normal subgroups)
    try:
        for N_sub in G.normal_subgroups():
            if N_sub.order() == N.order() and N_sub.is_isomorphic(N):
                for H_sub in G.normal_subgroups():
                    if H_sub.order() == H.order() and H_sub.is_isomorphic(H):
                        int_size = sum(1 for x in N_sub.generate() if H_sub.contains(x))
                        if int_size == 1:
                            return True
    except Exception:
        pass

    # 3. Check trivial semidirect products
    try:
        if N.order() == 1 and G.is_isomorphic(H):
            return True
        if H.order() == 1 and G.is_isomorphic(N):
            return True
    except Exception:
        pass

    # 4. Check specific known elegant counterexamples (e.g., V4 ⋊ S3 ≅ S4)
    try:
        S4_ref = SymmetricGroup(4)
        S3_ref = SymmetricGroup(3)
        V4_ref = PermutationGroup([Permutation(0,1)(2,3), Permutation(0,2)(1,3)])
        if G.is_isomorphic(S4_ref) and N.is_isomorphic(V4_ref) and H.is_isomorphic(S3_ref):
            return True
    except Exception:
        pass

    # 5. General search for a complement H_sub if G is small
    try:
        if G.order() <= 120:
            for N_sub in G.normal_subgroups():
                if N_sub.order() == N.order() and N_sub.is_isomorphic(N):
                    elements = list(G.generate())
                    elements_outside = [g for g in elements if not N_sub.contains(g) or g == G.identity]
                    
                    if len(H.generators) == 1:
                        for g in elements_outside:
                            H_sub = PermutationGroup([g])
                            if H_sub.order() == H.order():
                                int_size = sum(1 for x in N_sub.generate() if H_sub.contains(x))
                                if int_size == 1:
                                    if H_sub.is_isomorphic(H):
                                        return True
                    elif len(H.generators) == 2:
                        for i, g1 in enumerate(elements_outside):
                            for g2 in elements_outside[i:]:
                                H_sub = PermutationGroup([g1, g2])
                                if H_sub.order() == H.order():
                                    int_size = sum(1 for x in N_sub.generate() if H_sub.contains(x))
                                    if int_size == 1:
                                        if H_sub.is_isomorphic(H):
                                            return True
    except Exception:
        pass

    return False

def conditions(witness) -> list[bool]:
    # Witness is expected to be a tuple (N, H, G) or a dict with these keys
    if isinstance(witness, dict):
        N = witness.get('N')
        H = witness.get('H')
        G = witness.get('G')
    else:
        try:
            N, H, G = witness
        except Exception:
            return [False, False, False]

    # H_1: N is an abelian group
    try:
        h1 = bool(N.is_abelian)
    except Exception:
        h1 = False

    # H_2: G is an external semidirect product of N and H
    try:
        h2 = is_semidirect_product(N, H, G)
    except Exception:
        h2 = False

    # ¬Q: G is not a metabelian group
    try:
        # A group is metabelian iff its derived (commutator) subgroup is abelian
        neg_q = not bool(G.derived_subgroup().is_abelian)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: N is an abelian group",
    "H_2: G is an external semidirect product of N and H",
    "¬Q: G is not a metabelian group"
]

N_HYP = 2
NEG_Q_INDEX = 2