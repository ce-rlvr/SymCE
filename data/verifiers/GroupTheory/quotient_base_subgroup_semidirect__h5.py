import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Standard group theory objects
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3)])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

# Standard linear algebra objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        G, N, H, K = witness
    except Exception:
        return [False] * 6

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: N is a normal subgroup of G
    try:
        h2 = isinstance(N, PermutationGroup) and isinstance(G, PermutationGroup) and N.is_subgroup(G) and N.is_normal(G)
    except Exception:
        h2 = False

    # H_3: H is a subgroup of G
    try:
        h3 = isinstance(H, PermutationGroup) and isinstance(G, PermutationGroup) and H.is_subgroup(G)
    except Exception:
        h3 = False

    # H_4: G is the internal semidirect product of N and H
    try:
        if not (isinstance(N, PermutationGroup) and isinstance(H, PermutationGroup) and isinstance(G, PermutationGroup)):
            h4 = False
        else:
            is_N_normal = N.is_subgroup(G) and N.is_normal(G)
            is_H_subgroup = H.is_subgroup(G)
            if not (is_N_normal and is_H_subgroup):
                h4 = False
            elif not (N.order() * H.order() == G.order()):
                h4 = False
            else:
                n_elements = set(N.elements)
                h_elements = set(H.elements)
                h4 = len(n_elements.intersection(h_elements)) == 1
    except Exception:
        h4 = False

    # H_5: K is a subgroup of N
    try:
        h5 = isinstance(K, PermutationGroup) and isinstance(N, PermutationGroup) and K.is_subgroup(N)
    except Exception:
        h5 = False

    # neg_Q: The quotient group G/K is not isomorphic to the internal semidirect product of N/K and HK/K
    # This happens exactly when K is not normal in G (so G/K is not even a valid quotient group).
    try:
        if not (isinstance(K, PermutationGroup) and isinstance(G, PermutationGroup)):
            neg_q = False
        elif not K.is_subgroup(G):
            neg_q = True
        else:
            neg_q = not K.is_normal(G)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, h5, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: N is a normal subgroup of G",
    "H_3: H is a subgroup of G",
    "H_4: G is the internal semidirect product of N and H",
    "H_5: K is a subgroup of N",
    "¬Q: The quotient group G/K is not isomorphic to the internal semidirect product of N/K and HK/K"
]

N_HYP = 5
NEG_Q_INDEX = 5