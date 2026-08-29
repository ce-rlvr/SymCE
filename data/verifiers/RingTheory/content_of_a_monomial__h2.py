import sympy
from sympy.abc import x, y, z

ZZ = sympy.ZZ
QQ = sympy.QQ

def conditions(witness):
    try:
        if isinstance(witness, dict):
            R = witness.get('R')
            a = witness.get('a')
            n = witness.get('n')
        else:
            R, a, n = witness
    except Exception:
        return [False, False, False]

    # H_1: R is a Unique Factorization Domain
    try:
        h1 = bool(R.is_UFD)
    except Exception:
        h1 = False

    # H_2: n >= 0 is an integer
    try:
        h2 = isinstance(n, (int, sympy.Integer)) and n >= 0
    except Exception:
        h2 = False

    # neg_Q: The content of the monomial a*x**n is not associate to a in R
    try:
        if a not in R:
            neg_q = True
        elif a == 0 or a == R.zero:
            # The content of the zero polynomial is undefined, so it cannot be associate to 0
            neg_q = True
        else:
            X = sympy.Dummy('X')
            p = sympy.Poly(a * X**n, X, domain=R)
            c = p.content()
            q1 = R.exquo(a, c)
            q2 = R.exquo(c, a)
            neg_q = not (R.is_unit(q1) and R.is_unit(q2))
    except Exception:
        neg_q = True

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "H_2: n >= 0 is an integer",
    "¬Q: The content of the monomial a*x**n is not associate to a in R"
]

N_HYP = 2
NEG_Q_INDEX = 2