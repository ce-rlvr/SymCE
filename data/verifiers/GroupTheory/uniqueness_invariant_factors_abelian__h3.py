import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
)

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    try:
        G, D, E = witness
    except Exception:
        return [False, False, False]
    
    # H1: G is a finite abelian group
    try:
        h1 = False
        if hasattr(G, 'is_abelian') and hasattr(G, 'order'):
            order = G.order() if callable(G.order) else G.order
            h1 = bool(G.is_abelian) and order > 0 and order < float('inf')
    except Exception:
        h1 = False

    # H2: G is isomorphic to the direct sum of Z_{d_i} where d_i > 1 and d_i | d_{i+1}
    try:
        if not isinstance(D, (list, tuple)):
            h2 = False
        else:
            d_gt_1 = all(int(d) == d and d > 1 for d in D)
            d_div = all(D[i+1] % D[i] == 0 for i in range(len(D)-1))
            
            if hasattr(G, 'abelian_invariants'):
                invs = G.abelian_invariants()
                h2 = d_gt_1 and d_div and list(invs) == list(D)
            else:
                h2 = False
    except Exception:
        h2 = False

    # neg_Q: r != s or d_i != e_i for some i
    try:
        if not isinstance(E, (list, tuple)):
            neg_q = False
        else:
            neg_q = list(D) != list(E)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a finite abelian group",
    "H_2: G is isomorphic to the direct sum of Z_{d_i} where d_i > 1 and d_i | d_{i+1}",
    "¬Q: r != s or d_i != e_i for some i"
]

N_HYP = 2
NEG_Q_INDEX = 2