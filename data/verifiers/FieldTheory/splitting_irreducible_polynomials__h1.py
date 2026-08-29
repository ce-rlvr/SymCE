import sympy
from sympy import factor_list, Poly
from sympy.abc import x

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False]
        f, ext = witness
        f_expr = f.as_expr() if hasattr(f, 'as_expr') else f
    except Exception:
        return [False, False, False]
        
    try:
        coeff, factors = factor_list(f_expr, domain='QQ')
        h1_ok = (len(factors) == 1) and (factors[0][1] == 1) and (Poly(factors[0][0], x).degree() > 0)
    except Exception:
        h1_ok = False
        
    try:
        if not isinstance(ext, (list, tuple)):
            ext_list = [ext]
        else:
            ext_list = list(ext)
            
        coeff_K, factors_K = factor_list(f_expr, extension=ext_list)
        h2_ok = any(Poly(fac, x).degree() == 1 for fac, mult in factors_K)
    except Exception:
        h2_ok = False
        
    try:
        neg_q_ok = not all(Poly(fac, x).degree() == 1 for fac, mult in factors_K)
    except Exception:
        neg_q_ok = False
        
    return [bool(h1_ok), bool(h2_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: f is an irreducible polynomial over F",
    "H_2: f has at least one root in K",
    "¬Q: f does not split completely into linear factors over K"
]

N_HYP = 2
NEG_Q_INDEX = 2