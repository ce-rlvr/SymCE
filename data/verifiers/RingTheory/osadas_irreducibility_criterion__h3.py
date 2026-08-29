import sympy
from sympy import Poly, factor_list
from sympy.abc import x

CONDITION_LABELS = [
    "H_1: f is a monic polynomial over Z",
    "H_2: The degree n of f is at least 1",
    "H_3: p > sum of absolute values of a_i",
    "not Q: f is reducible over Q"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            f, p = witness
        else:
            f = witness
            p = None
            
        free_symbols = f.free_symbols
        if len(free_symbols) == 1:
            var = list(free_symbols)[0]
        else:
            var = x
            
        f_poly = Poly(f, var)
        if p is None:
            p = abs(f_poly.nth(0))
    except Exception:
        return [False, False, False, False]

    # H1: f is a monic polynomial in Z[x]
    h1 = False
    try:
        if f_poly.LC() == 1 and f_poly.domain.is_ZZ:
            h1 = True
    except Exception:
        pass

    # H2: The degree n of f is at least 1
    h2 = False
    try:
        if f_poly.degree() >= 1:
            h2 = True
    except Exception:
        pass

    # H3: p > sum_{i=1}^{n-1} |a_i|
    h3 = False
    try:
        coeffs = f_poly.all_coeffs()
        # coeffs is [a_n, a_{n-1}, ..., a_0]
        # We need the sum of |a_i| for i=1 to n-1
        sum_abs = sum(abs(c) for c in coeffs[1:-1])
        if p > sum_abs:
            h3 = True
    except Exception:
        pass

    # neg_Q: f is reducible over Q
    neg_q = False
    try:
        factors = factor_list(f)
        # A polynomial is irreducible if it has exactly one factor, 
        # with multiplicity 1, and its degree equals the degree of f.
        is_irreducible = (
            len(factors[1]) == 1 
            and factors[1][0][1] == 1 
            and sympy.degree(factors[1][0][0], var) == f_poly.degree()
        )
        neg_q = not is_irreducible
    except Exception:
        pass

    return [h1, h2, h3, neg_q]