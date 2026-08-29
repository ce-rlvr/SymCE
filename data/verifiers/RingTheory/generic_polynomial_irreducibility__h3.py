import sympy
from sympy import Poly, Symbol, QQ, ZZ, GF, Rational, Integer

# Top-level setup for witness expressions
x = Symbol('x')
t = Symbol('t')

def conditions(witness):
    K = None
    n = None
    coeffs = None
    poly = None

    # Parse witness
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                K, n, coeffs = witness
            elif len(witness) == 2:
                K, coeffs = witness
                if isinstance(coeffs, (list, tuple)):
                    n = len(coeffs)
                else:
                    poly = Poly(coeffs, x)
                    n = poly.degree()
        elif isinstance(witness, (list, tuple)):
            coeffs = witness
            n = len(coeffs)
            K = QQ
        else:
            poly = Poly(witness, x)
            n = poly.degree()
            K = poly.domain
            if not K.is_Field:
                K = K.get_field()
    except Exception:
        pass

    # H_1: K is a field
    try:
        h1 = bool(getattr(K, 'is_Field', False))
    except Exception:
        h1 = False

    # H_2: n >= 1 is an integer
    try:
        h2 = bool(isinstance(n, int) and n >= 1)
    except Exception:
        h2 = False

    # ¬Q: The polynomial is reducible
    neg_q = False
    try:
        if h1 and h2:
            if poly is None and coeffs is not None:
                # coeffs is [t_0, t_1, ..., t_{n-1}]
                # polynomial is x^n + t_{n-1}x^{n-1} + ... + t_0
                expr = x**n + sum(coeffs[i] * x**i for i in range(n))
                poly = Poly(expr, x, domain=K)
            elif poly is not None:
                poly = Poly(poly, x, domain=K)
            
            if poly is not None:
                # Ensure the polynomial matches the generic form (monic of degree n)
                if poly.degree() == n and poly.LC() == 1:
                    neg_q = not poly.is_irreducible
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: K is a field",
    "H_2: n >= 1 is an integer",
    "¬Q: The polynomial is reducible"
]

N_HYP = 2
NEG_Q_INDEX = 2