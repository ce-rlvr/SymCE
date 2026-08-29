import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros

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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: G is a group and N_i are subgroups of G",
    "H_2: The intersection of all N_i is the trivial subgroup",
    "¬Q: G is not isomorphic to a subgroup of the direct product of G/N_i"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        G, N_list = witness
    except Exception:
        return [False, False, False]

    try:
        h1 = False
        if isinstance(G, PermutationGroup) and isinstance(N_list, (list, tuple)) and len(N_list) > 0:
            h1 = True
            for N in N_list:
                if not isinstance(N, PermutationGroup):
                    h1 = False
                    break
                for h in N.generators:
                    if h not in G:
                        h1 = False
                        break
                if not h1:
                    break
    except Exception:
        h1 = False

    try:
        h2 = False
        if h1:
            common_count = 0
            for elem in N_list[0].elements:
                in_all = True
                for N in N_list[1:]:
                    if elem not in N:
                        in_all = False
                        break
                if in_all:
                    common_count += 1
            h2 = (common_count == 1)
    except Exception:
        h2 = False

    try:
        neg_q = False
        if h1:
            all_normal = True
            for N in N_list:
                for g in G.generators:
                    g_inv = ~g
                    for h in N.generators:
                        if (g * h * g_inv) not in N:
                            all_normal = False
                            break
                    if not all_normal:
                        break
                if not all_normal:
                    break
            
            # If any N_i is not normal, G/N_i is not a group, so the direct product is undefined.
            # Thus G cannot be isomorphic to a subgroup of it, meaning the conclusion fails.
            neg_q = not all_normal
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]