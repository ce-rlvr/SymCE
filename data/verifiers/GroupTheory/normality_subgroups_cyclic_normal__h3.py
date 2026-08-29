import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation

# Top-level setup: named object bindings
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

def is_subgroup(sub, grp):
    if not isinstance(sub, PermutationGroup) or not isinstance(grp, PermutationGroup):
        return False
    try:
        return sub.is_subgroup(grp)
    except Exception:
        for gen in sub.generators:
            if gen not in grp:
                return False
        return True

def is_normal_subgroup(sub, grp):
    if not is_subgroup(sub, grp):
        return False
    try:
        for g in grp.generators:
            g_inv = ~g
            for h in sub.generators:
                if (g * h * g_inv) not in sub:
                    return False
        return True
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 3:
            return [False, False, False, False]
        G, N, H = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is a finite group
    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False

    # H_2: N is a normal subgroup of G
    try:
        h2_ok = is_normal_subgroup(N, G)
    except Exception:
        h2_ok = False

    # H_3: H is a subgroup of N
    try:
        h3_ok = is_subgroup(H, N)
    except Exception:
        h3_ok = False

    # neg_Q: H is NOT a normal subgroup of G
    try:
        neg_q_ok = not is_normal_subgroup(H, G)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: N is a normal subgroup of G",
    "H_3: H is a subgroup of N",
    "¬Q: H is not a normal subgroup of G"
]

N_HYP = 3
NEG_Q_INDEX = 3