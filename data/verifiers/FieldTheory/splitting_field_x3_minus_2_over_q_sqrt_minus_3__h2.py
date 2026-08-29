import sympy
from sympy import sqrt, Rational, cbrt
from sympy.abc import x

def conditions(witness):
    H_1_ok = True
    H_2_ok = False
    neg_Q_ok = False
    
    try:
        if isinstance(witness, tuple):
            f = witness[-1]
        else:
            f = witness
            
        f_expr = sympy.nsimplify(sympy.sympify(f))
        
        try:
            poly_F = sympy.Poly(f_expr, x, extension=[sqrt(-3)])
            domain = poly_F.domain
            if domain.is_AlgebraicField or domain.is_QQ or domain.is_ZZ:
                H_2_ok = True
            else:
                H_2_ok = False
        except Exception:
            H_2_ok = False
            
        if not H_2_ok:
            return [H_1_ok, H_2_ok, False]
            
        ext_F = [sqrt(-3)]
        ext_M = [sqrt(-3), cbrt(2)]
        
        def splits_completely(poly_expr, exts):
            facs = sympy.factor_list(poly_expr, extension=exts)[1]
            for fac, _ in facs:
                if sympy.Poly(fac, x).degree() > 1:
                    return False
            return True
            
        splits_M = splits_completely(f_expr, ext_M)
        splits_F = splits_completely(f_expr, ext_F)
        
        K_eq_M = splits_M and not splits_F
        
        neg_Q_ok = not K_eq_M
        
    except Exception:
        neg_Q_ok = False
        
    return [H_1_ok, H_2_ok, neg_Q_ok]

CONDITION_LABELS: list[str] = [
    "H_1: F is Q(sqrt(-3))",
    "H_2: K is the splitting field of f(x) over F",
    "not Q: K is not F(cbrt(2)) or degree is not 3"
]

N_HYP: int = 2
NEG_Q_INDEX: int = 2