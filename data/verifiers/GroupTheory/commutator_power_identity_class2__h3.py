import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: G is nilpotent of class at most 2",
    "H_3: n is an integer",
    "¬Q: (xy)^n != x^n y^n commutator(y, x)^(n(n-1)/2)"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness) -> list[bool]:
    try:
        if len(witness) == 4:
            G, n, x, y = witness
            search = False
        elif len(witness) == 2:
            G, n = witness
            search = True
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    try:
        h2 = bool(G.is_nilpotent and G.nilpotency_class <= 2)
    except Exception:
        h2 = False

    try:
        h3 = isinstance(n, int)
    except Exception:
        h3 = False

    neg_q = False
    try:
        def check_identity(x_elem, y_elem, n_val):
            comm = (y_elem**-1) * (x_elem**-1) * y_elem * x_elem
            lhs = (x_elem * y_elem)**n_val
            rhs = (x_elem**n_val) * (y_elem**n_val) * (comm**(n_val * (n_val - 1) // 2))
            return lhs != rhs

        if search:
            if hasattr(G, 'elements'):
                elements = list(G.elements)
                for x_elem in elements:
                    for y_elem in elements:
                        if check_identity(x_elem, y_elem, n):
                            neg_q = True
                            break
                    if neg_q:
                        break
        else:
            neg_q = check_identity(x, y, n)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]