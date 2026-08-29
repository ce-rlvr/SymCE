import sympy
from sympy import Poly, sqf_list, factor_list
from sympy.abc import x, y, z

def conditions(witness):
    try:
        if isinstance(witness, (tuple, list)):
            expr = witness[0]
        else:
            expr = witness
            
        if hasattr(expr, 'free_symbols'):
            syms = list(expr.free_symbols)
            if len(syms) == 1:
                var = syms[0]
            elif len(syms) > 1:
                var = x if x in syms else syms[0]
            else:
                var = x
        else:
            var = x
            
        f = Poly(expr, var)
        n = f.degree()
        
        if n < 1:
            H1 = False
        else:
            H1 = True
            factors = factor_list(f)
            for factor, mult in factors[1]:
                if Poly(factor, var).diff().is_zero:
                    H1 = False
                    break
    except Exception:
        H1 = False

    H2 = H1

    try:
        if not H1:
            neg_Q = False
        else:
            sqf = sqf_list(f)
            is_sqf = all(mult == 1 for factor, mult in sqf[1])
            neg_Q = not is_sqf
    except Exception:
        neg_Q = False

    return [bool(H1), bool(H2), bool(neg_Q)]

CONDITION_LABELS = [
    "H_1: f(x) is a separable polynomial of degree n over K",
    "H_2: L is the splitting field of f(x) over K",
    "¬Q: The action of Gal(L/K) on the roots does not induce an injective homomorphism into S_n"
]

N_HYP = 2
NEG_Q_INDEX = 2