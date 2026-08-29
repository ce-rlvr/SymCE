import math
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros

# Top-level setup bindings
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

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 4:
                G, H, n, K = witness
            elif len(witness) == 2:
                G, H = witness
                if hasattr(G, 'order') and hasattr(H, 'order') and H.is_subgroup(G):
                    n = G.order() // H.order()
                    core = H
                    while core.order() > 1:
                        prev_order = core.order()
                        for g in G.generators:
                            conj_gens = [g * c * ~g for c in core.generators]
                            if conj_gens:
                                conj = PermutationGroup(conj_gens)
                                core = core.intersect(conj)
                        if core.order() == prev_order:
                            break
                    K = core
                else:
                    n = None
                    K = None
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H1: H is a subgroup of G of index n
    try:
        h1 = H.is_subgroup(G) and (G.order() // H.order() == n)
    except Exception:
        h1 = False

    # H2: K is the normal core of H in G
    try:
        if not H.is_subgroup(G):
            h2 = False
        else:
            core = H
            while core.order() > 1:
                prev_order = core.order()
                for g in G.generators:
                    conj_gens = [g * c * ~g for c in core.generators]
                    if conj_gens:
                        conj = PermutationGroup(conj_gens)
                        core = core.intersect(conj)
                if core.order() == prev_order:
                    break
            h2 = K.is_subgroup(core) and core.is_subgroup(K)
    except Exception:
        h2 = False

    # neg_Q: The index of K in G does not divide n!
    try:
        index_K = G.order() // K.order()
        fact_n = math.factorial(n)
        neg_q = (fact_n % index_K != 0)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: H is a subgroup of G of index n",
    "H_2: K is the normal core of H in G",
    "¬Q: The index of K in G does not divide n!"
]

N_HYP = 2
NEG_Q_INDEX = 2