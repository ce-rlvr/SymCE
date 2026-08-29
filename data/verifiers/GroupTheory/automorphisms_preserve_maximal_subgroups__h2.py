import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup
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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def apply_alpha(alpha, x):
    if isinstance(alpha, dict):
        return alpha[x]
    return alpha(x)

def is_maximal(G, H):
    try:
        if H.order() == G.order():
            return False
        H_elems = set(H.generate())
        G_elems = set(G.generate())
        if not H_elems.issubset(G_elems):
            return False
        for x in G_elems - H_elems:
            gens = list(H.generators) + [x]
            K = PermutationGroup(gens)
            if K.order() != G.order():
                return False
        return True
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        G, alpha, M = witness
    except Exception:
        return [False, False, False]

    # H1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H2: alpha is an automorphism of G
    try:
        h2 = False
        if h1:
            G_elems = list(G.generate())
            mapped_elems = set()
            is_auto = True
            for g in G_elems:
                ag = apply_alpha(alpha, g)
                if ag not in G_elems:
                    is_auto = False
                    break
                mapped_elems.add(ag)
            if is_auto and len(mapped_elems) == len(G_elems):
                for g in G_elems:
                    for h in G_elems:
                        if apply_alpha(alpha, g * h) != apply_alpha(alpha, g) * apply_alpha(alpha, h):
                            is_auto = False
                            break
                    if not is_auto:
                        break
                h2 = is_auto
    except Exception:
        h2 = False

    # neg_Q: alpha(M) is NOT a maximal subgroup of G
    try:
        if not isinstance(G, PermutationGroup):
            neg_q = True
        else:
            if isinstance(M, PermutationGroup):
                alpha_M_gens = [apply_alpha(alpha, g) for g in M.generators]
                if not alpha_M_gens:
                    id_elem = list(G.generate())[0]**0
                    alpha_M_gens = [id_elem]
                alpha_M = PermutationGroup(alpha_M_gens)
                neg_q = not is_maximal(G, alpha_M)
            elif isinstance(M, (list, set, tuple)):
                alpha_M_set = set([apply_alpha(alpha, g) for g in M])
                is_subgroup = True
                for x in alpha_M_set:
                    for y in alpha_M_set:
                        if x * y not in alpha_M_set:
                            is_subgroup = False
                            break
                    if not is_subgroup:
                        break
                if not is_subgroup:
                    neg_q = True
                else:
                    if len(alpha_M_set) == 0:
                        neg_q = True
                    else:
                        alpha_M = PermutationGroup(list(alpha_M_set))
                        neg_q = not is_maximal(G, alpha_M)
            else:
                neg_q = True
    except Exception:
        neg_q = True

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: alpha is an automorphism of G",
    "¬Q: alpha(M) is not a maximal subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2