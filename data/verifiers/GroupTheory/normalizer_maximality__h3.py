import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
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
        G, H, K = witness
    except Exception:
        return [False, False, False, False, False]

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: H is a subgroup of G
    try:
        h2 = isinstance(H, PermutationGroup) and isinstance(G, PermutationGroup) and H.is_subgroup(G)
    except Exception:
        h2 = False

    # H_3: K contains H
    try:
        h3 = isinstance(K, PermutationGroup) and isinstance(H, PermutationGroup) and H.is_subgroup(K)
    except Exception:
        h3 = False

    # H_4: H is a normal subgroup of K
    try:
        h4 = isinstance(H, PermutationGroup) and isinstance(K, PermutationGroup) and H.is_normal(K)
    except Exception:
        h4 = False

    # neg_Q: K is not a subgroup of the normalizer N_G(H)
    try:
        if not (isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup) and isinstance(K, PermutationGroup)):
            neg_q = False
        else:
            # K is a subgroup of N_G(H) iff K is a subgroup of G and K normalizes H
            is_subgroup = K.is_subgroup(G)
            normalizes = True
            for k in K.generators:
                for h in H.generators:
                    if (k * h * ~k) not in H:
                        normalizes = False
                        break
                if not normalizes:
                    break
            q = is_subgroup and normalizes
            neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a subgroup of G",
    "H_3: K contains H",
    "H_4: H is a normal subgroup of K",
    "¬Q: K is not a subgroup of the normalizer N_G(H)"
]

N_HYP = 4
NEG_Q_INDEX = 4