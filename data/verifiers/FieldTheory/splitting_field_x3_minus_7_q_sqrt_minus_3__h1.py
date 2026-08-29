import sympy
from sympy import Poly, Symbol, QQ, I, sqrt

def conditions(witness):
    x = Symbol('x')
    
    try:
        F = witness
        if not getattr(F, 'is_Field', False) or getattr(F, 'char', None) != 0:
            h1 = False
        else:
            p = Poly(x**3 - 7, x, domain=F)
            h1 = True
    except Exception:
        h1 = False

    h2 = h1

    try:
        if not h1:
            neg_q = False
        else:
            p_f = Poly(x**3 - 7, x, domain=F)
            factors_f = p_f.factor_list()[1]
            has_root_f = any(f[0].degree() == 1 for f in factors_f)
            is_irreducible_f = len(factors_f) == 1 and factors_f[0][0].degree() == 3
            
            p_omega = Poly(x**2 + 3, x, domain=F)
            factors_omega = p_omega.factor_list()[1]
            has_root_omega = any(f[0].degree() == 1 for f in factors_omega)
            
            if is_irreducible_f and has_root_omega:
                degree_E_F = 3
            elif is_irreducible_f and not has_root_omega:
                degree_E_F = 6
            elif has_root_f and not has_root_omega:
                degree_E_F = 2
            else:
                degree_E_F = 1
                
            if degree_E_F != 3:
                neg_q = True
            else:
                neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f(x) = x^3 - 7 in F(x)",
    "H_2: E is the splitting field of f(x) over F",
    "not Q: degree of E over F is not 3 or E is not F(cbrt(7))"
]

N_HYP = 2
NEG_Q_INDEX = 2