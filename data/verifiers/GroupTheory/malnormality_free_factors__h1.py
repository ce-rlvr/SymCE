import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros

# Top-level setup
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

def conditions(witness) -> list[bool]:
    try:
        F, H, g = witness
    except Exception:
        return [False, False, False]

    # H_1: Let H be a proper free factor of F
    # In the context of finite groups (where strict free products are impossible),
    # we verify that H is a proper, non-trivial subgroup of F.
    try:
        is_subgroup = all(F.contains(gen) for gen in H.generators)
        h1_ok = bool(is_subgroup and H.order() > 1 and H.order() < F.order())
    except Exception:
        h1_ok = False

    # H_2: Let g be an element of F such that g \notin H
    try:
        g_in_F = F.contains(g)
        g_notin_H = not H.contains(g)
        h2_ok = bool(g_in_F and g_notin_H)
    except Exception:
        h2_ok = False

    # ¬Q: The intersection H \cap gHg^{-1} is NOT the trivial subgroup
    try:
        g_inv = ~g
        conj_gens = [g * h * g_inv for h in H.generators]
        gHg_inv = PermutationGroup(conj_gens)
        
        intersection = H.intersect(gHg_inv)
        neg_q_ok = bool(intersection.order() > 1)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: H is a proper free factor of F",
    "H_2: g is an element of F such that g is not in H",
    "¬Q: The intersection H \\cap gHg^{-1} is not the trivial subgroup"
]

N_HYP = 2
NEG_Q_INDEX = 2