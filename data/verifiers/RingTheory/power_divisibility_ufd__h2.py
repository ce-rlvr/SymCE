import sympy
from sympy import ZZ, QQ
from sympy.abc import x, y, z

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "H_2: n is a positive integer",
    "H_3: a^n divides b^n in R",
    "¬Q: a does not divide b in R"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        if isinstance(witness, dict):
            R = witness.get('R', sympy.ZZ)
            a = witness['a']
            b = witness['b']
            n = witness['n']
        elif len(witness) == 4:
            R, a, b, n = witness
        elif len(witness) == 3:
            a, b, n = witness
            R = sympy.ZZ
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H1: R is a Unique Factorization Domain
    try:
        h1 = bool(getattr(R, 'is_UFD', False))
    except Exception:
        h1 = False

    # H2: n is a positive integer
    try:
        h2 = isinstance(n, (int, sympy.Integer)) and int(n) > 0
    except Exception:
        h2 = False

    # H3: a^n divides b^n in R
    try:
        if not h1 or not h2:
            h3 = False
        else:
            a_R = R(a)
            b_R = R(b)
            a_n = a_R ** int(n)
            b_n = b_R ** int(n)
            
            if a_n == R.zero:
                h3 = (b_n == R.zero)
            else:
                try:
                    R.exquo(b_n, a_n)
                    h3 = True
                except Exception:
                    h3 = False
    except Exception:
        h3 = False

    # neg_Q: a does not divide b in R
    try:
        if not h1:
            neg_q = False
        else:
            a_R = R(a)
            b_R = R(b)
            if a_R == R.zero:
                divides_ab = (b_R == R.zero)
            else:
                try:
                    R.exquo(b_R, a_R)
                    divides_ab = True
                except Exception:
                    divides_ab = False
            neg_q = not divides_ab
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]