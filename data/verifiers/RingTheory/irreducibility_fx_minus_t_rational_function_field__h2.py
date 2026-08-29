import sympy
from sympy import Symbol, Poly, QQ

X = Symbol('X')
T = Symbol('T')

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            K, f_expr = witness
        else:
            K = QQ
            f_expr = witness
            
        if isinstance(f_expr, sympy.Poly):
            f_expr = f_expr.as_expr()
    except Exception:
        return [False, False, False]
        
    try:
        h1 = bool(K.is_Field)
    except Exception:
        h1 = False
        
    try:
        p = sympy.Poly(f_expr, X, domain=K)
        h2 = bool(p.degree() >= 1 and p.domain == K)
    except Exception:
        h2 = False
        
    neg_q = False
    try:
        T_in_K = False
        try:
            K.from_sympy(T)
            T_in_K = True
        except Exception:
            pass
            
        if T_in_K:
            KT = K
        else:
            KT = K.frac_field(T)
            
        p_KT = sympy.Poly(f_expr - T, X, domain=KT)
        
        resolved = False
        try:
            irred = p_KT.is_irreducible
            if irred is not None:
                neg_q = not irred
                resolved = True
        except Exception:
            pass
            
        if not resolved:
            try:
                _, factors = p_KT.factor_list()
                num_non_constant = sum(mult for fac, mult in factors if fac.degree() >= 1)
                neg_q = bool(num_non_constant > 1)
                resolved = True
            except Exception:
                pass
                
        if not resolved:
            _, factors = sympy.factor_list(f_expr - T, X)
            num_non_constant = sum(mult for fac, mult in factors if sympy.Poly(fac, X).degree() >= 1)
            neg_q = bool(num_non_constant > 1)
            
    except Exception:
        try:
            _, factors = sympy.factor_list(f_expr - T, X)
            num_non_constant = sum(mult for fac, mult in factors if sympy.Poly(fac, X).degree() >= 1)
            neg_q = bool(num_non_constant > 1)
        except Exception:
            neg_q = False
            
    return [h1, h2, neg_q]

CONDITION_LABELS = ["H_1: K is a field", "H_2: f(X) is a polynomial over K of degree n >= 1", "¬Q: f(X) - T is reducible over K(T)"]
N_HYP = 2
NEG_Q_INDEX = 2