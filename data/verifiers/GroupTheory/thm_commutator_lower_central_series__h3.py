import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]]))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

N_HYP = 2
NEG_Q_INDEX = 2

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: i and j are positive integers",
    "not Q: Commutator of gamma_i and gamma_j is not a subgroup of gamma_i_plus_j"
]

def get_identity(G):
    if G.generators:
        return G.generators[0]**0
    return Permutation()

def commutator_subgroup(H, K):
    gens = []
    for h in list(H.generate()):
        for k in list(K.generate()):
            gens.append(~h * ~k * h * k)
    if not gens:
        return PermutationGroup([get_identity(H)])
    return PermutationGroup(gens)

def gamma(lcs, k):
    idx = k - 1
    if idx < len(lcs):
        return lcs[idx]
    else:
        return lcs[-1]

def conditions(witness):
    try:
        G, i, j = witness
    except Exception:
        return [False, False, False]
        
    # H_1: G is a group
    try:
        h1 = hasattr(G, 'lower_central_series') and hasattr(G, 'generators')
    except Exception:
        h1 = False
        
    # H_2: i and j are positive integers
    try:
        h2 = isinstance(i, (int, sympy.Integer)) and isinstance(j, (int, sympy.Integer)) and i > 0 and j > 0
    except Exception:
        h2 = False
        
    # neg_Q: The commutator subgroup is NOT a subgroup of gamma_{i+j}(G)
    try:
        if not (h1 and h2):
            neg_q = False
        else:
            lcs = G.lower_central_series()
            gamma_i = gamma(lcs, i)
            gamma_j = gamma(lcs, j)
            gamma_ij = gamma(lcs, i + j)
            
            comm = commutator_subgroup(gamma_i, gamma_j)
            
            is_sub = True
            for g in comm.generators:
                if g not in gamma_ij:
                    is_sub = False
                    break
            neg_q = not is_sub
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]