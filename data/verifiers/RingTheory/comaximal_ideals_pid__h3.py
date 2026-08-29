import sympy
from sympy import gcd, degree, Poly

# Top-level setup
x, y, z = sympy.symbols('x y z')

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False]
        a = sympy.sympify(witness[0])
        b = sympy.sympify(witness[1])
    except Exception:
        return [False, False, False]

    # H1: R is a principal ideal domain
    try:
        is_Z = (a.is_integer is True) and (b.is_integer is True)
        is_poly = False
        if is_Z:
            a = sympy.Integer(a)
            b = sympy.Integer(b)
        else:
            syms = a.free_symbols | b.free_symbols
            if len(syms) == 1:
                poly_a = Poly(a)
                poly_b = Poly(b)
                is_poly = True
        h1 = bool(is_Z or is_poly)
    except Exception:
        h1 = False

    # H2: a and b are elements of R
    try:
        h2 = h1
    except Exception:
        h2 = False

    # neg_Q: <a> + <b> != R
    try:
        if is_Z:
            g = gcd(a, b)
            neg_q = bool(abs(g) != 1)
        elif is_poly:
            g = gcd(a, b)
            if g == 0:
                neg_q = True
            else:
                neg_q = bool(degree(g) > 0)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "H_2: a and b are elements of R",
    "¬Q: The ideal sum <a> + <b> is not equal to the entire ring R"
]

N_HYP = 2
NEG_Q_INDEX = 2