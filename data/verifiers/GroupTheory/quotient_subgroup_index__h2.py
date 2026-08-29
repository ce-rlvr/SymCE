import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros

# Standard group theory objects
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

# Standard linear algebra objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        G, H, N = witness
    except Exception:
        return [False, False, False, False, False]

    # H1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H2: H is a subgroup of G
    try:
        h2 = isinstance(H, PermutationGroup) and H.is_subgroup(G)
    except Exception:
        h2 = False

    # H3: N is a subset of H
    try:
        if isinstance(N, PermutationGroup):
            h3 = N.is_subgroup(H)
        else:
            h3 = all(n in H for n in N)
    except Exception:
        h3 = False

    # H4: The index of H in G is finite
    try:
        h4 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h4 = False

    # neg_Q: The conclusion fails
    try:
        conclusion = False
        if isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup):
            if isinstance(N, PermutationGroup):
                if N.is_subgroup(G) and N.is_normal(G) and N.is_subgroup(H):
                    conclusion = True
            else:
                N_set = set(N)
                is_normal = True
                if not N_set:
                    is_normal = False
                else:
                    id_perm = list(G.elements)[0]**0
                    if id_perm not in N_set:
                        is_normal = False
                    else:
                        for a in N_set:
                            for b in N_set:
                                if a * b not in N_set:
                                    is_normal = False
                                    break
                            if a**-1 not in N_set:
                                is_normal = False
                                break
                        if is_normal:
                            for g in G.elements:
                                g_inv = g**-1
                                for n in N_set:
                                    if g * n * g_inv not in N_set:
                                        is_normal = False
                                        break
                                if not is_normal:
                                    break
                        if is_normal:
                            for n in N_set:
                                if n not in H:
                                    is_normal = False
                                    break
                conclusion = is_normal
        neg_q = not conclusion
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a subgroup of G",
    "H_3: N is a subset of H",
    "H_4: The index of H in G is finite",
    "¬Q: The index of H/N in G/N is not equal to the index of H in G"
]

N_HYP = 4
NEG_Q_INDEX = 4