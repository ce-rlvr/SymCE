import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
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

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 3:
            return [False, False, False]
        G, x, C = witness
    except Exception:
        return [False, False, False]

    # H_1: G is a group
    try:
        h1 = hasattr(G, 'generate') and hasattr(G, 'identity')
    except Exception:
        h1 = False

    # H_2: x is an element of G
    try:
        h2 = False
        if h1:
            elements = list(G.generate())
            h2 = x in elements
    except Exception:
        h2 = False

    # ¬Q: The set of inverses C^{-1} is not exactly the conjugacy class of the inverse element x^{-1} in G
    try:
        x_inv = x**-1
        conj_class = set()
        for g in G.generate():
            conj_class.add(g * x_inv * g**-1)
        
        c_inv = {c**-1 for c in C}
        
        q = (c_inv == conj_class)
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: x is an element of G",
    "¬Q: The set of inverses C^{-1} is not exactly the conjugacy class of x^{-1} in G"
]

N_HYP = 2
NEG_Q_INDEX = 2