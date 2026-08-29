import sympy
from sympy.abc import x, y, z

def conditions(witness):
    try:
        a, b, c = witness
    except Exception:
        return [False, False, False, False]

    # H_1: R is a unique factorization domain
    try:
        # Integers and polynomials over fields are UFDs.
        # We verify the elements are valid SymPy expressions or Python integers.
        h1 = all(isinstance(val, (int, sympy.Integer, sympy.Expr)) for val in (a, b, c))
    except Exception:
        h1 = False

    # H_2: a, b, and c are non-zero elements of R
    try:
        h2 = all(sympy.expand(val) != 0 for val in (a, b, c))
    except Exception:
        h2 = False

    # H_3: a is coprime to c
    try:
        h3 = sympy.gcd(a, c) == 1
    except Exception:
        h3 = False

    # ¬Q: a is not coprime to bc
    try:
        neg_q = sympy.gcd(a, b * c) != 1
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a unique factorization domain",
    "H_2: a, b, and c are non-zero elements of R",
    "H_3: a is coprime to c",
    "¬Q: a is not coprime to bc"
]

N_HYP = 3
NEG_Q_INDEX = 3