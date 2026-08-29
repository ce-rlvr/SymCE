import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros

# Top-level setup
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

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                G, H = witness
                x = 0
            elif len(witness) == 3:
                G, H, x = witness
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: G is a group acting on a set X
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: H is a subgroup of G
    try:
        h2 = isinstance(H, PermutationGroup) and H.is_subgroup(G)
    except Exception:
        h2 = False

    # H_3: The restricted action of H on X is transitive
    try:
        if h1 and h2:
            if 0 <= x < G.degree:
                h3 = len(H.orbit(x)) == G.degree
            else:
                h3 = False
        else:
            h3 = False
    except Exception:
        h3 = False

    # neg_Q: G cannot be exactly factored as G = H G_x
    try:
        if h1 and h2 and h3:
            # G = H G_x as sets is always true for transitive H.
            # "Factored as" implies exact factorization, meaning H \cap G_x == {e}.
            # H \cap G_x is the stabilizer of x in H.
            # So the factorization is NOT exact if H.stabilizer(x) is non-trivial.
            neg_q = H.stabilizer(x).order() > 1
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group acting on a set X",
    "H_2: H is a subgroup of G",
    "H_3: The restricted action of H on X is transitive",
    "¬Q: G cannot be exactly factored as G = H G_x (i.e., H ∩ G_x ≠ {e})"
]

N_HYP = 3
NEG_Q_INDEX = 3