import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, PermutationGroup
from sympy.combinatorics.permutations import Permutation

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            n = witness.get('n')
        else:
            if hasattr(witness[0], 'elements'):
                G, n = witness
            else:
                n, G = witness
    except Exception:
        return [False, False, False]

    try:
        h1 = isinstance(n, (int, sympy.Integer))
    except Exception:
        h1 = False

    try:
        h2 = isinstance(G, PermutationGroup)
    except Exception:
        h2 = False

    neg_q = False
    try:
        if h1 and h2:
            n_int = int(n)
            elements = list(G.elements)
            for x in elements:
                for y in elements:
                    xy = x * y
                    f_xy = xy ** n_int
                    fx = x ** n_int
                    fy = y ** n_int
                    if f_xy != fx * fy:
                        neg_q = True
                        break
                if neg_q:
                    break
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer",
    "H_2: f is a map from G to G defined by f(x) = x^n for all x in G",
    "¬Q: f is not a group homomorphism"
]

N_HYP = 2
NEG_Q_INDEX = 2