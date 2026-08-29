import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
        h2 = h1 and isinstance(H, PermutationGroup) and H.is_subgroup(G)
    except Exception:
        h2 = False

    # H_3: K is a subgroup of G
    try:
        h3 = h1 and isinstance(K, PermutationGroup) and K.is_subgroup(G)
    except Exception:
        h3 = False

    # H_4: H is a normal subgroup of K
    try:
        h4 = isinstance(H, PermutationGroup) and isinstance(K, PermutationGroup) and H.is_normal(K)
    except Exception:
        h4 = False

    # ¬Q: K is not a subgroup of the normalizer N_G(H)
    # K is a subgroup of N_G(H) iff K <= G and K normalizes H.
    try:
        if not (isinstance(K, PermutationGroup) and isinstance(H, PermutationGroup) and isinstance(G, PermutationGroup)):
            q = False
        elif not K.is_subgroup(G):
            q = False
        else:
            q = True
            for k in K.generators:
                k_inv = k**-1
                for h in H.generators:
                    if (k * h * k_inv) not in H:
                        q = False
                        break
                    if (k_inv * h * k) not in H:
                        q = False
                        break
                if not q:
                    break
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a subgroup of G",
    "H_3: K is a subgroup of G",
    "H_4: H is a normal subgroup of K",
    "¬Q: K is not a subgroup of the normalizer N_G(H)"
]

N_HYP = 4
NEG_Q_INDEX = 4