import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

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

CONDITION_LABELS = [
    "H_1: M is a maximal subgroup of G",
    "H_2: M is a normal subgroup of G",
    "H_3: M is a solvable group",
    "¬Q: G is not a solvable group"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 2:
            return [False, False, False, False]
        G, M = witness
    except Exception:
        return [False, False, False, False]

    def is_subgroup(sub, grp):
        try:
            for g in sub.generators:
                if g not in grp:
                    return False
            return True
        except Exception:
            return False

    # H_1: M is a maximal subgroup of G
    try:
        h1 = False
        if is_subgroup(M, G) and M.order() < G.order():
            maximal = True
            for x in list(G.elements):
                if x not in M:
                    gens = list(M.generators) + [x]
                    H = PermutationGroup(*gens)
                    if H.order() < G.order():
                        maximal = False
                        break
            h1 = maximal
    except Exception:
        h1 = False

    # H_2: M is a normal subgroup of G
    try:
        h2 = False
        if is_subgroup(M, G):
            normal = True
            for g in G.generators:
                g_inv = ~g
                for m in M.generators:
                    if (g * m * g_inv) not in M:
                        normal = False
                        break
                    if (g_inv * m * g) not in M:
                        normal = False
                        break
                if not normal:
                    break
            h2 = normal
    except Exception:
        h2 = False

    # H_3: M is a solvable group
    try:
        h3 = bool(M.is_solvable)
    except Exception:
        h3 = False

    # ¬Q: G is not a solvable group
    try:
        neg_q = not bool(G.is_solvable)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]