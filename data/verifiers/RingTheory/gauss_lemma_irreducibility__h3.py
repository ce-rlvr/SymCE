import sympy
from sympy import Poly, factor_list
from sympy.ntheory import factorint
from sympy.abc import x

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain (UFD)",
    "H_2: F is the field of fractions of R",
    "H_3: f(x) is irreducible over R",
    "¬Q: f(x) is not irreducible over F"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness) -> list[bool]:
    if isinstance(witness, tuple):
        if len(witness) == 3:
            witness = witness[2]
        elif len(witness) >= 1:
            witness = witness[-1]
        else:
            return [False, False, False, False]

    if isinstance(witness, Poly):
        try:
            f = witness.as_expr()
        except Exception:
            return [False, False, False, False]
    else:
        try:
            f = sympy.sympify(witness)
        except Exception:
            return [False, False, False, False]

    try:
        free = f.free_symbols
        if len(free) == 1:
            var = list(free)[0]
        elif len(free) == 0:
            var = sympy.Symbol('x')
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    try:
        p_Z = Poly(f, var, domain='ZZ')
        h1 = True
    except Exception:
        h1 = False

    h2 = h1

    h3 = False
    if h1:
        try:
            cont, factors = factor_list(p_Z)
            if cont == 0:
                h3 = False
            else:
                prime_factors = factorint(abs(cont))
                num_prime_factors = sum(prime_factors.values())
                num_poly_factors = sum(mult for base, mult in factors)
                h3 = (num_prime_factors + num_poly_factors) == 1
        except Exception:
            h3 = False

    neg_q = False
    if h1:
        try:
            p_Q = Poly(f, var, domain='QQ')
            cont_Q, factors_Q = factor_list(p_Q)
            if cont_Q == 0:
                neg_q = True
            else:
                num_poly_factors_Q = sum(mult for base, mult in factors_Q)
                neg_q = (num_poly_factors_Q != 1)
        except Exception:
            neg_q = False

    return [h1, h2, h3, neg_q]