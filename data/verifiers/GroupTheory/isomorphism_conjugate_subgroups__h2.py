import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics import PermutationGroup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            g = witness.get('g')
            H = witness.get('H')
        else:
            G, g, H = witness
    except Exception:
        return [False, False, False]

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: g is an element of G
    try:
        h2 = g in G
    except Exception:
        h2 = False

    # ¬Q: The conjugate subgroup gHg^{-1} is not isomorphic to H
    try:
        if isinstance(H, PermutationGroup):
            g_inv = g**-1
            conj_gens = [g * h * g_inv for h in H.generators]
            conj_H = PermutationGroup(conj_gens)
            q = H.is_isomorphic(conj_H)
            neg_q = not q
        else:
            # If H is not a group (e.g., just a subset), it cannot be isomorphic to a group
            neg_q = True
    except Exception:
        neg_q = True

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: g is an element of G",
    "¬Q: The conjugate subgroup gHg^{-1} is not isomorphic to H"
]

N_HYP = 2
NEG_Q_INDEX = 2