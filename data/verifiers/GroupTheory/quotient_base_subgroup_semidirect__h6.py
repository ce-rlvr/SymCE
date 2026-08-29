import sympy
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics import PermutationGroup

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

def conditions(witness) -> list[bool]:
    try:
        G, N, H, K = witness
    except Exception:
        return [False] * 6

    def safe_group(*groups):
        gens = []
        for g in groups:
            gens.extend(g.generators)
        if not gens:
            gens = [Permutation()]
        return PermutationGroup(gens)

    def is_subgroup(sub, parent):
        try:
            if hasattr(sub, 'is_subgroup'):
                return sub.is_subgroup(parent)
        except Exception:
            pass
        return all(g in parent for g in sub.generators)

    def is_normal(sub, parent):
        try:
            if hasattr(sub, 'is_normal'):
                return sub.is_normal(parent)
        except Exception:
            pass
        if not is_subgroup(sub, parent):
            return False
        return all((g * h * ~g) in sub for g in parent.generators for h in sub.generators)

    def group_intersect(g1, g2):
        if hasattr(g1, 'intersect'):
            return g1.intersect(g2)
        return g1.intersection(g2)

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: N is a normal subgroup of G
    try:
        h2 = is_subgroup(N, G) and is_normal(N, G)
    except Exception:
        h2 = False

    # H_3: H is a subgroup of G
    try:
        h3 = is_subgroup(H, G)
    except Exception:
        h3 = False

    # H_4: G is the internal semidirect product of N and H
    try:
        int_NH = group_intersect(N, H)
        gen_NH = safe_group(N, H)
        h4 = is_normal(N, G) and is_subgroup(H, G) and (int_NH.order() == 1) and (gen_NH.order() == G.order())
    except Exception:
        h4 = False

    # H_5: K is a normal subgroup of G
    try:
        h5 = is_subgroup(K, G) and is_normal(K, G)
    except Exception:
        h5 = False

    # neg_Q: The quotient group G/K is isomorphic to the internal semidirect product of the normal subgroup N/K and the subgroup HK/K.
    try:
        # Interpretation 1: N/K literally means K <= N.
        interp1_q = False
        if is_subgroup(K, N):
            HK = safe_group(H, K)
            int_N_HK = group_intersect(N, HK)
            NHK = safe_group(N, HK)
            # For G/K to be the internal semidirect product of N/K and HK/K,
            # their intersection in G/K must be trivial (i.e., N \cap HK = K)
            # and they must generate G/K (i.e., N(HK) = G).
            interp1_q = (int_N_HK.order() == K.order()) and (NHK.order() == G.order())

        # Interpretation 2: N/K is a typo for NK/K.
        NK = safe_group(N, K)
        HK = safe_group(H, K)
        int_NK_HK = group_intersect(NK, HK)
        NK_HK = safe_group(NK, HK)
        interp2_q = (int_NK_HK.order() == K.order()) and (NK_HK.order() == G.order())

        # The conclusion holds if either interpretation is true.
        q = interp1_q or interp2_q
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, h5, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: N is a normal subgroup of G",
    "H_3: H is a subgroup of G",
    "H_4: G is the internal semidirect product of N and H",
    "H_5: K is a normal subgroup of G",
    "¬Q: G/K is not isomorphic to the internal semidirect product of N/K and HK/K"
]

N_HYP = 5
NEG_Q_INDEX = 5