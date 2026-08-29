import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
import itertools
import functools
import math

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

CONDITION_LABELS = [
    "H_1: G is a group and H, K are subgroups of G",
    "H_2: H is a normal subgroup of G",
    "H_3: The intersection of H and K contains only the identity element of G",
    "H_4: G is equal to the product set HK",
    "¬Q: G is not isomorphic to the external direct product H x K"
]

N_HYP = 4
NEG_Q_INDEX = 4

def conditions(witness):
    try:
        G, H, K = witness
    except Exception:
        return [False] * 5

    # H_1: G is a group and H, K are subgroups of G
    try:
        h1 = (isinstance(G, PermutationGroup) and 
              isinstance(H, PermutationGroup) and 
              isinstance(K, PermutationGroup) and 
              all(G.contains(g) for g in H.generators) and 
              all(G.contains(g) for g in K.generators))
    except Exception:
        h1 = False

    # H_2: H is a normal subgroup of G
    try:
        if hasattr(H, 'is_normal'):
            h2 = bool(H.is_normal(G))
        else:
            h2 = True
            for g in G.generators:
                g_inv = ~g
                for h in H.generators:
                    if not H.contains(g * h * g_inv):
                        h2 = False
                        break
                if not h2:
                    break
    except Exception:
        h2 = False

    # H_3: The intersection of H and K contains only the identity element of G
    try:
        h_elems = set(H.generate_dimino())
        k_elems = set(K.generate_dimino())
        intersection = h_elems.intersection(k_elems)
        h3 = (len(intersection) == 1) and list(intersection)[0].is_Identity
    except Exception:
        h3 = False

    # H_4: G is equal to the product set HK
    try:
        h_elems = list(H.generate_dimino())
        k_elems = list(K.generate_dimino())
        hk_elems = set(h * k for h in h_elems for k in k_elems)
        g_elems = set(G.generate_dimino())
        h4 = (hk_elems == g_elems)
    except Exception:
        h4 = False

    # neg_Q: G is not isomorphic to the external direct product H x K
    try:
        n = max(getattr(H, 'degree', 1), 1)
        m = max(getattr(K, 'degree', 1), 1)
        for g in H.generators:
            n = max(n, g.size)
        for g in K.generators:
            m = max(m, g.size)
            
        gens = []
        for g in H.generators:
            arr = g.array_form
            if len(arr) < n:
                arr = arr + list(range(len(arr), n))
            arr = arr + list(range(n, n + m))
            gens.append(Permutation(arr))
        for g in K.generators:
            arr = g.array_form
            if len(arr) < m:
                arr = arr + list(range(len(arr), m))
            arr = list(range(n)) + [x + n for x in arr]
            gens.append(Permutation(arr))
        
        if not gens:
            HxK = PermutationGroup([Permutation(0)])
        else:
            HxK = PermutationGroup(gens)
            
        try:
            is_iso = G.is_isomorphic(HxK)
        except Exception:
            # Fallback for isomorphism check if is_isomorphic is unavailable or fails
            if G.order() != HxK.order():
                is_iso = False
            elif G.is_abelian != HxK.is_abelian:
                is_iso = False
            else:
                g_orders = sorted([g.order() for g in G.generate_dimino()])
                hx_orders = sorted([g.order() for g in HxK.generate_dimino()])
                if g_orders != hx_orders:
                    is_iso = False
                else:
                    is_iso = True
                    
        neg_q = not is_iso
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]