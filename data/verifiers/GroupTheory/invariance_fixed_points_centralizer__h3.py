import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros, Integer

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            g = witness.get('g')
            h = witness.get('h')
            x = witness.get('x')
        else:
            G, g, h, x = witness
    except Exception:
        return [False, False, False, False]

    try:
        h1 = (isinstance(G, PermutationGroup) and 
              isinstance(h, Permutation) and h in G and 
              isinstance(x, (int, Integer)) and 0 <= x < G.degree)
    except Exception:
        h1 = False

    try:
        h2 = isinstance(g, Permutation) and g in G
    except Exception:
        h2 = False

    try:
        h3 = g(x) == x
    except Exception:
        h3 = False

    try:
        hx = h(x)
        neg_q = g(hx) != hx
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group acting on a set X",
    "H_2: g is an element of G",
    "H_3: x is a fixed point of g",
    "¬Q: h * x is not a fixed point of g"
]

N_HYP = 3
NEG_Q_INDEX = 3