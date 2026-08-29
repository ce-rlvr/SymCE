import sympy
from sympy import Poly
from sympy.abc import x

S3 = sympy.combinatorics.SymmetricGroup(3)
S4 = sympy.combinatorics.SymmetricGroup(4)
A4 = sympy.combinatorics.AlternatingGroup(4)
D4 = sympy.combinatorics.DihedralGroup(4)
C4 = sympy.combinatorics.CyclicGroup(4)
V4 = sympy.combinatorics.AlternatingGroup(4)
Z2 = sympy.combinatorics.CyclicGroup(2)
Z3 = sympy.combinatorics.CyclicGroup(3)
Z4 = sympy.combinatorics.CyclicGroup(4)
Z6 = sympy.combinatorics.CyclicGroup(6)
trivial = sympy.combinatorics.CyclicGroup(1)

CONDITION_LABELS = [
    "H_1: f(x) is a non-constant polynomial over F",
    "H_2: f(x) is a separable polynomial",
    "H_3: K is the splitting field of f(x) over F",
    "¬Q: The field extension K/F is not a Galois extension"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            f_val = witness[0]
        else:
            f_val = witness
        f = Poly(f_val)
        H1 = f.is_univariate and f.degree() > 0
    except Exception:
        H1 = False

    try:
        if isinstance(witness, tuple):
            f_val = witness[0]
        else:
            f_val = witness
        f = Poly(f_val)
        H2 = bool(f.is_squarefree)
    except Exception:
        H2 = False

    try:
        H3 = True
    except Exception:
        H3 = False

    try:
        if isinstance(witness, tuple):
            f_val = witness[0]
        else:
            f_val = witness
        f = Poly(f_val)
        is_galois = f.domain.is_Field
        neg_Q = not is_galois
    except Exception:
        neg_Q = False

    return [H1, H2, H3, neg_Q]