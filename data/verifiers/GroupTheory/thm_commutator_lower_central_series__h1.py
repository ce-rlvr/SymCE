import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        G, i, j = witness
    except Exception:
        return [False, False, False]
        
    # H_1: i and j are positive integers
    try:
        h1 = isinstance(i, int) and isinstance(j, int) and i > 0 and j > 0
    except Exception:
        h1 = False
        
    # H_2: gamma_k(G) denotes the k-th term of the lower central series of G
    try:
        if hasattr(G, 'lower_central_series'):
            lcs = G.lower_central_series()
            h2 = True
        else:
            h2 = False
    except Exception:
        h2 = False
        
    # ¬Q: The commutator subgroup of gamma_i(G) and gamma_j(G) is NOT a subgroup of gamma_{i+j}(G)
    try:
        if not h2 or not h1:
            neg_q = False
        else:
            def get_gamma(k):
                if k - 1 < len(lcs):
                    return lcs[k - 1]
                else:
                    return lcs[-1]
            
            gamma_i = get_gamma(i)
            gamma_j = get_gamma(j)
            gamma_ij = get_gamma(i + j)
            
            is_subgroup = True
            for g1 in gamma_i.generators:
                for g2 in gamma_j.generators:
                    comm = (g1**-1) * (g2**-1) * g1 * g2
                    if not gamma_ij.contains(comm):
                        is_subgroup = False
                        break
                if not is_subgroup:
                    break
            
            neg_q = not is_subgroup
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: i and j are positive integers",
    "H_2: gamma_k(G) denotes the k-th term of the lower central series of G",
    "¬Q: The commutator subgroup of gamma_i(G) and gamma_j(G) is NOT a subgroup of gamma_{i+j}(G)"
]

N_HYP = 2
NEG_Q_INDEX = 2