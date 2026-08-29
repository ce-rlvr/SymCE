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

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            x = witness.get('x')
            C = witness.get('C')
        else:
            G, x, C = witness
    except Exception:
        return [False, False, False]

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: C is the conjugacy class of x in G
    try:
        if not h1:
            h2 = False
        else:
            if x not in G.elements:
                h2 = False
            else:
                true_C = {g * x * g**-1 for g in G.elements}
                h2 = (set(C) == true_C)
    except Exception:
        h2 = False

    # ¬Q: The set of inverses C^{-1} is NOT exactly the conjugacy class of the inverse element x^{-1} in G
    try:
        if not h1:
            neg_q = False
        else:
            C_inv = {c**-1 for c in C}
            x_inv = x**-1
            true_C_x_inv = {g * x_inv * g**-1 for g in G.elements}
            q = (C_inv == true_C_x_inv)
            neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: C is the conjugacy class of x in G",
    "¬Q: The set of inverses C^{-1} is not exactly the conjugacy class of x^{-1} in G"
]

N_HYP = 2
NEG_Q_INDEX = 2