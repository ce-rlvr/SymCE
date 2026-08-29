import sympy
from sympy import QQ, ZZ, Poly
from sympy.abc import x, y, z

def conditions(witness):
    try:
        F, K, g = witness
    except Exception:
        return [False, False, False, False]
    
    try:
        h1 = getattr(F, 'is_Field', False)
    except Exception:
        h1 = False
        
    try:
        h2 = False
        if K == F:
            h2 = True
        elif getattr(K, 'is_AlgebraicField', False) and K.domain == F:
            minpoly = K.mod
            minpoly_K = minpoly.set_domain(K)
            factors = minpoly_K.factor_list()
            h2 = all(factor.degree() <= 1 for factor, mult in factors[1])
        elif getattr(K, 'is_FiniteField', False) and getattr(F, 'is_FiniteField', False):
            if K.characteristic == F.characteristic and K.degree % F.degree == 0:
                h2 = True
    except Exception:
        h2 = False
        
    try:
        if isinstance(g, Poly):
            g_F = g.set_domain(F)
        else:
            g_F = Poly(g, domain=F)
        h3 = g_F.is_univariate and g_F.is_irreducible
    except Exception:
        h3 = False
        
    try:
        if isinstance(g, Poly):
            g_K = g.set_domain(K)
        else:
            g_K = Poly(g, domain=K)
        
        factors = g_K.factor_list()
        neg_q = any(factor.degree() > 1 for factor, mult in factors[1])
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: K is a splitting field of some polynomial over F",
    "H_3: g is an irreducible polynomial over F",
    "¬Q: g does not split completely into linear factors over K"
]

N_HYP = 3
NEG_Q_INDEX = 3