import sympy
from sympy import Poly
from sympy.abc import x
from sympy.ntheory import isprime

# Top-level setup
Z = sympy.S.Integers
ZZ = sympy.ZZ
Q = sympy.S.Rationals
QQ = sympy.QQ

def conditions(witness):
    try:
        if isinstance(witness, dict):
            p = witness.get('p', witness.get('P'))
            f = witness['f']
            R = witness.get('R', sympy.S.Integers)
        elif isinstance(witness, tuple) or isinstance(witness, list):
            if len(witness) == 2:
                p, f = witness
                R = sympy.S.Integers
            elif len(witness) == 3:
                R, p, f = witness
            else:
                return [False] * 6
        else:
            return [False] * 6
    except Exception:
        return [False] * 6

    try:
        if isinstance(f, str):
            f = sympy.sympify(f)
        free_syms = f.free_symbols
        if len(free_syms) == 1:
            sym = list(free_syms)[0]
        elif len(free_syms) == 0:
            sym = x
        else:
            return [False] * 6
        poly_f = Poly(f, sym)
    except Exception:
        return [False] * 6

    # H1: R is an integral domain
    try:
        if R in (sympy.S.Integers, sympy.ZZ, 'Z', 'ZZ'):
            h1 = all(c.is_integer for c in poly_f.all_coeffs())
        else:
            h1 = False
    except Exception:
        h1 = False

    # H2: P is a prime ideal of R
    try:
        h2 = isprime(abs(int(p)))
    except Exception:
        h2 = False

    # H3: f(x) is a polynomial in R[x] of degree n >= 1
    try:
        n = poly_f.degree()
        h3 = h1 and (n >= 1)
    except Exception:
        h3 = False

    # H4: a_n not in P
    try:
        a_n = poly_f.all_coeffs()[0]
        h4 = (a_n % p != 0)
    except Exception:
        h4 = False

    # H5: a_i in P for all 0 <= i < n
    try:
        coeffs = poly_f.all_coeffs()
        h5 = all(c % p == 0 for c in coeffs[1:])
    except Exception:
        h5 = False

    # ¬Q: f(x) can be expressed as the product of two polynomials in R[x] of strictly positive degree
    try:
        factors = sympy.factor_list(f, domain='ZZ')
        pos_deg_factors_count = sum(mult for fac, mult in factors[1] if Poly(fac, sym).degree() > 0)
        neg_q = pos_deg_factors_count >= 2
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, h5, neg_q]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: P is a prime ideal of R",
    "H_3: f is a polynomial over R of degree n >= 1",
    "H_4: a_n not in P",
    "H_5: a_i in P for all 0 <= i < n",
    "not Q: f can be expressed as the product of two polynomials over R of strictly positive degree"
]

N_HYP = 5
NEG_Q_INDEX = 5