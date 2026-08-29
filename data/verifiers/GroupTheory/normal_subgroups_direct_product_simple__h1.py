import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
import itertools

# Final Result: Verifier Module for Normal Subgroups in Direct Products
# Initial logic and parameters are validated.

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

def conditions(witness) -> list[bool]:
    try:
        factors, N_gens = witness
    except Exception:
        return [False, False, False]

    # Standard processing applied
    try:
        degrees = [f.degree for f in factors]
        offsets = [0] + list(itertools.accumulate(degrees))[:-1]
        total_degree = sum(degrees)
        identity_perm = Permutation(list(range(total_degree))) if total_degree > 0 else Permutation()

        embedded_factors = []
        G_gens = []
        for i, f in enumerate(factors):
            offset = offsets[i]
            f_gens = []
            for g in f.generators:
                shifted = []
                for j in range(total_degree):
                    if offset <= j < offset + degrees[i]:
                        shifted.append(g(j - offset) + offset)
                    else:
                        shifted.append(j)
                f_gens.append(Permutation(shifted))
            embedded_factors.append(PermutationGroup(*f_gens) if f_gens else PermutationGroup(identity_perm))
            G_gens.extend(f_gens)

        G = PermutationGroup(*G_gens) if G_gens else PermutationGroup(identity_perm)
        N = PermutationGroup(*N_gens) if N_gens else PermutationGroup(identity_perm)

        h1 = N.is_subgroup(G)
    except Exception:
        h1 = False

    try:
        h2 = h1 and N.is_normal(G)
    except Exception:
        h2 = False

    try:
        is_subcollection_dp = False
        for r in range(len(embedded_factors) + 1):
            for subset in itertools.combinations(embedded_factors, r):
                subset_gens = []
                for ef in subset:
                    subset_gens.extend(ef.generators)
                if not subset_gens:
                    subset_gens = [identity_perm]
                subset_group = PermutationGroup(*subset_gens)

                if N.is_subgroup(subset_group) and subset_group.is_subgroup(N):
                    is_subcollection_dp = True
                    break
            if is_subcollection_dp:
                break

        neg_q = not is_subcollection_dp
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is the direct product of factors S_i and N is a subgroup of G",
    "H_2: N is a normal subgroup of G",
    "¬Q: N does not correspond to the internal direct product of a subcollection of the factors"
]

N_HYP = 2
NEG_Q_INDEX = 2