import sympy
from sympy import Poly, factor_list, RootOf
from sympy.abc import x

# Top-level setup
# Witness is expected to be a tuple of two SymPy expressions in x: (minpoly_L, f)
# K is implicitly the field of rational numbers QQ.
# L is the field extension QQ(alpha) where alpha is a root of minpoly_L.
# f is a polynomial in QQ[x].

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 2:
            return [False, False, False]
        minpoly_L, f = witness
    except Exception:
        return [False, False, False]
    
    # H1: L/K is a normal field extension
    try:
        poly_L = Poly(minpoly_L, x)
        if not all(c.is_Rational for c in poly_L.coeffs()):
            h1 = False
        elif poly_L.degree() < 1:
            h1 = False
        else:
            factors_L = factor_list(poly_L)[1]
            is_irred_L = len(factors_L) == 1 and factors_L[0][1] == 1
            if not is_irred_L:
                h1 = False
            else:
                if poly_L.degree() == 1:
                    h1 = True
                else:
                    alpha = RootOf(poly_L, 0)
                    ext_factors = factor_list(poly_L, extension=alpha)[1]
                    h1 = all(Poly(fac, x).degree() == 1 for fac, mult in ext_factors)
    except Exception:
        h1 = False

    # H2: f in K[x] is an irreducible polynomial
    try:
        poly_f = Poly(f, x)
        if not all(c.is_Rational for c in poly_f.coeffs()):
            h2 = False
        elif poly_f.degree() < 1:
            h2 = False
        else:
            factors_f = factor_list(poly_f)[1]
            h2 = len(factors_f) == 1 and factors_f[0][1] == 1
    except Exception:
        h2 = False

    # neg_Q: f does NOT split completely into linear factors in L[x]
    try:
        poly_L = Poly(minpoly_L, x)
        if poly_L.degree() == 1:
            ext_factors_f = factor_list(f)[1]
        else:
            alpha = RootOf(poly_L, 0)
            ext_factors_f = factor_list(f, extension=alpha)[1]
        splits = all(Poly(fac, x).degree() == 1 for fac, mult in ext_factors_f)
        neg_q = not splits
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = ["H_1: L/K is a normal field extension", "H_2: f is an irreducible polynomial over K", "¬Q: f does not split completely into linear factors over L"]

N_HYP = 2
NEG_Q_INDEX = 2