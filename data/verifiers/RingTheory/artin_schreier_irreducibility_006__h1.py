import sympy
from sympy import Poly, Symbol, GF, QQ, ZZ

CONDITION_LABELS = [
    "H_1: a is an element of K",
    "H_2: The polynomial x^p - x - a has no roots in K",
    "¬Q: The polynomial x^p - x - a is not irreducible over K"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        K, p, a = witness
    except Exception:
        return [False, False, False]

    if not isinstance(p, int) or p < 2:
        return [False, False, False]

    # H_1: a is an element of K
    try:
        if not hasattr(K, 'convert'):
            h1_ok = False
        else:
            # Check if 'a' can be converted to an element of the domain K
            K.convert(a)
            h1_ok = True
    except Exception:
        h1_ok = False

    # H_2: The polynomial x^p - x - a has no roots in K
    try:
        x = Symbol('x')
        # Construct the polynomial x^p - x - a over K
        coeffs = [0] * (p + 1)
        coeffs[0] = 1
        coeffs[p - 1] = -1
        coeffs[p] = -a
        
        poly = Poly(coeffs, x, domain=K)
        
        # A polynomial has a root in K iff it has a linear factor over K
        factors = poly.factor_list()
        has_root = False
        for fac, mult in factors[1]:
            if fac.degree() == 1:
                has_root = True
                break
        h2_ok = not has_root
    except Exception:
        h2_ok = False

    # ¬Q: The polynomial x^p - x - a is not irreducible over K
    try:
        is_irred = poly.is_irreducible
        if is_irred is None:
            neg_q_ok = False
        else:
            neg_q_ok = not is_irred
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]