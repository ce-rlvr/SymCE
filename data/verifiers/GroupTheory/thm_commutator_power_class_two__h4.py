import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            n = witness.get('n')
            x = witness.get('x')
            y = witness.get('y')
        else:
            G, n, x, y = witness
    except Exception:
        return [False, False, False, False]

    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    try:
        D = G.derived_subgroup()
        C = G.center()
        h2 = bool(D.is_subgroup(C))
    except Exception:
        try:
            h2 = all(g in C for g in D.generators)
        except Exception:
            h2 = False

    try:
        h3 = isinstance(n, int) or isinstance(n, sympy.Integer)
    except Exception:
        h3 = False

    try:
        try:
            n_int = int(n)
        except Exception:
            n_int = n

        lhs = (x**n_int) * y * (x**-n_int) * (y**-1)
        rhs = (x * y * (x**-1) * (y**-1))**n_int
        neg_q = not bool(lhs == rhs)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: derived subgroup is contained in the center",
    "H_3: n is an integer",
    "neg_Q: commutator identity fails"
]

N_HYP = 3
NEG_Q_INDEX = 3