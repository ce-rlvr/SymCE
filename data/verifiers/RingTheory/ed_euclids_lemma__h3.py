import sympy
from sympy import Rational, Integer

# Top-level setup for witness expressions
x = sympy.Symbol('x')
y = sympy.Symbol('y')
z = sympy.Symbol('z')

def conditions(witness):
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 3:
            return [False, False, False, False]
        a, b, c = witness
    except Exception:
        return [False, False, False, False]

    def is_int(val):
        return isinstance(val, int) or (isinstance(val, sympy.Expr) and val.is_Integer)

    domain = None
    sym = None
    try:
        if is_int(a) and is_int(b) and is_int(c):
            domain = 'Z'
        else:
            syms = set()
            for elem in (a, b, c):
                if isinstance(elem, sympy.Expr):
                    syms.update(elem.free_symbols)
            if len(syms) == 1:
                sym = list(syms)[0]
                is_poly = True
                for elem in (a, b, c):
                    if not is_int(elem):
                        if not isinstance(elem, sympy.Expr) or not elem.is_polynomial(sym):
                            is_poly = False
                            break
                if is_poly:
                    domain = 'Q[x]'
    except Exception:
        pass

    # H1: R is a Euclidean domain and a, b, c in R
    try:
        h1 = (domain is not None)
    except Exception:
        h1 = False

    # H2: a, b, c are non-zero
    try:
        h2 = False
        if h1:
            h2 = (a != 0) and (b != 0) and (c != 0)
    except Exception:
        h2 = False

    # H3: a and b are coprime
    try:
        h3 = False
        if h1:
            if domain == 'Z':
                g = sympy.gcd(a, b)
                h3 = (g == 1 or g == -1)
            elif domain == 'Q[x]':
                g = sympy.gcd(a, b)
                if isinstance(g, sympy.Expr):
                    p = sympy.poly(g, sym, domain='QQ')
                    h3 = (p.degree() == 0)
                else:
                    h3 = (g != 0)
    except Exception:
        h3 = False

    # neg_Q: a does not divide c
    try:
        neg_q = False
        if h1:
            if a == 0:
                neg_q = (c != 0)
            elif domain == 'Z':
                neg_q = (c % a != 0)
            elif domain == 'Q[x]':
                q, r = sympy.div(c, a, domain='QQ')
                neg_q = (r != 0)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: a, b, c are elements of a Euclidean domain",
    "H_2: a, b, c are non-zero",
    "H_3: a and b are coprime",
    "¬Q: a does not divide c"
]

N_HYP = 3
NEG_Q_INDEX = 3