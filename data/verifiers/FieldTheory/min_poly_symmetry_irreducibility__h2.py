import sympy as sp
from sympy import QQ
from sympy.abc import x, t, u

CONDITION_LABELS = [
    "H_1: alpha is algebraic over Q",
    "not Q: minimal poly of alpha irreducible over Q(beta) iff minimal poly of beta irreducible over Q(alpha) fails"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        alpha, beta = witness
    except Exception:
        return [False, False]
        
    x_sym = sp.Symbol('x')
    
    try:
        f = sp.minpoly(alpha, x_sym, domain=sp.QQ)
        h1 = True
    except Exception:
        h1 = False

    def is_irreducible(poly, ext_elem):
        try:
            sp.minpoly(ext_elem, x_sym, domain=sp.QQ)
            is_alg = True
        except Exception:
            is_alg = False
            
        if is_alg:
            try:
                factors = sp.factor_list(poly, x_sym, extension=ext_elem)
                return len(factors[1]) == 1 and factors[1][0][1] == 1
            except Exception:
                try:
                    factors = sp.factor_list(poly, x_sym, domain=sp.QQ)
                    return len(factors[1]) == 1 and factors[1][0][1] == 1
                except Exception:
                    return False
        else:
            try:
                factors = sp.factor_list(poly, x_sym, domain=sp.QQ)
                return len(factors[1]) == 1 and factors[1][0][1] == 1
            except Exception:
                return False

    try:
        if h1:
            lhs = is_irreducible(f, beta)
        else:
            lhs = False
    except Exception:
        lhs = False

    try:
        g = sp.minpoly(beta, x_sym, domain=sp.QQ)
        rhs = is_irreducible(g, alpha)
    except Exception:
        rhs = False

    try:
        neg_q = (lhs != rhs)
    except Exception:
        neg_q = False

    return [h1, neg_q]