import sympy

# Top-level setup
QQ = sympy.QQ
I = sympy.I
pi = sympy.pi
sqrt = sympy.sqrt
exp = sympy.exp
Rational = sympy.Rational

CONDITION_LABELS = [
    "H_1: α is algebraic over F",
    "H_2: The minimal polynomial of α over F has degree n",
    "H_3: k is a positive integer such that gcd(k, n) = 1",
    "¬Q: The minimal polynomial of α^k over F does not have degree n"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 4:
                alpha, F, n, k = witness
            elif len(witness) == 3:
                alpha, n, k = witness
                F = sympy.QQ
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    x = sympy.Symbol('x')

    # H_1: α is algebraic over F
    try:
        poly_alpha = sympy.minpoly(alpha, x, polys=True, domain=F)
        h1 = True
    except Exception:
        h1 = False

    # H_2: The minimal polynomial of α over F has degree n
    try:
        h2 = bool(poly_alpha.degree() == n)
    except Exception:
        h2 = False

    # H_3: k is a positive integer such that gcd(k, n) = 1
    try:
        h3 = bool(k > 0 and int(k) == k and sympy.gcd(k, n) == 1)
    except Exception:
        h3 = False

    # ¬Q: The minimal polynomial of α^k over F does not have degree n
    try:
        alpha_k = sympy.expand(alpha**k)
        poly_alpha_k = sympy.minpoly(alpha_k, x, polys=True, domain=F)
        neg_q = bool(poly_alpha_k.degree() != n)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]