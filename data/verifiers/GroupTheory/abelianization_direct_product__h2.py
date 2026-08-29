import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

# Top-level setup: named object bindings
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

def conditions(witness) -> list[bool]:
    try:
        G, H = witness
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            G_prime = G.derived_subgroup()
            H_prime = H.derived_subgroup()
            
            m = G.degree
            n = H.degree
            if m == 0: m = 1
            if n == 0: n = 1
            
            gens = []
            if not G.generators:
                gens.append(Permutation(list(range(m+n))))
            else:
                for g in G.generators:
                    arr = g.array_form
                    arr = arr + list(range(len(arr), m))
                    gens.append(Permutation(arr + list(range(m, m+n))))
                    
            if not H.generators:
                gens.append(Permutation(list(range(m+n))))
            else:
                for h in H.generators:
                    arr = h.array_form
                    arr = arr + list(range(len(arr), n))
                    gens.append(Permutation(list(range(m)) + [x + m for x in arr]))
                    
            GxH = PermutationGroup(gens)
            GxH_prime = GxH.derived_subgroup()
            
            G_ab_order = G.order() // G_prime.order()
            H_ab_order = H.order() // H_prime.order()
            GxH_ab_order = GxH.order() // GxH_prime.order()
            
            if G_ab_order * H_ab_order != GxH_ab_order:
                neg_q = True
            else:
                neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "¬Q: (G x H)_ab is not isomorphic to G_ab x H_ab"
]

N_HYP = 1
NEG_Q_INDEX = 1