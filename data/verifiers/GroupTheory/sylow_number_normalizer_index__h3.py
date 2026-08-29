import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import isprime

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime dividing the order of G",
    "¬Q: The number of Sylow p-subgroups of G is not equal to the index of N_G(P) in G"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if not isinstance(witness, tuple) or len(witness) != 3:
            return [False, False, False]
        G, p, P = witness
    except Exception:
        return [False, False, False]

    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    try:
        h2 = bool(isprime(p) and (G.order() % p == 0))
    except Exception:
        h2 = False

    try:
        if not isinstance(P, PermutationGroup):
            neg_q = False
        else:
            is_subgroup = True
            for gen in P.generators:
                if not G.contains(gen):
                    is_subgroup = False
                    break
            
            if not is_subgroup:
                neg_q = False
            else:
                S = G.sylow_subgroup(p)
                elements = list(G.generate())
                
                norm_S_count = 0
                for g in elements:
                    is_in_norm = True
                    for s in S.generators:
                        if not S.contains(g * s * ~g):
                            is_in_norm = False
                            break
                    if is_in_norm:
                        norm_S_count += 1
                n_p = G.order() // norm_S_count
                
                norm_P_count = 0
                for g in elements:
                    is_in_norm = True
                    for s in P.generators:
                        if not P.contains(g * s * ~g):
                            is_in_norm = False
                            break
                    if is_in_norm:
                        norm_P_count += 1
                index_N_G_P = G.order() // norm_P_count
                
                neg_q = bool(n_p != index_N_G_P)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]