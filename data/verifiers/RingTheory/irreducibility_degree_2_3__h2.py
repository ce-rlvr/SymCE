import sympy
from sympy import Poly, Rational, Integer
from sympy.abc import x, y, z
from sympy import QQ, RR, CC, ZZ, GF

def conditions(witness):
    try:
        F, f = witness
    except Exception:
        return [False, False, False]
        
    # H1: F is a field
    try:
        h1 = bool(F.is_Field)
    except Exception:
        h1 = False
        
    # H2: The degree of f(x) is either 2 or 3
    try:
        if isinstance(f, Poly):
            var = f.gen
            expr = f.as_expr()
        else:
            expr = f
            free_syms = expr.free_symbols
            if len(free_syms) == 1:
                var = list(free_syms)[0]
            elif len(free_syms) == 0:
                var = x
            else:
                var = list(free_syms)[0]
                
        deg = sympy.degree(expr, var)
        h2 = deg in (2, 3)
    except Exception:
        h2 = False
        var = x
        expr = f
        
    # Q: f(x) is irreducible in F[x] if and only if f(x) has no roots in F
    try:
        try:
            poly_f = Poly(expr, var)
            coeffs_in_F = all((c in F) for c in poly_f.coeffs())
        except Exception:
            coeffs_in_F = False

        try:
            if coeffs_in_F:
                coeff, factors = sympy.factor_list(expr, var, domain=F)
                is_irred = (len(factors) == 1 and factors[0][1] == 1)
            else:
                is_irred = False
        except Exception:
            is_irred = False

        try:
            if coeffs_in_F:
                rts = sympy.roots(expr, var, domain=F)
                has_no_roots = (len(rts) == 0)
            else:
                rts = sympy.roots(expr, var)
                has_no_roots = True
                for r in rts.keys():
                    if r in F:
                        has_no_roots = False
                        break
        except Exception:
            has_no_roots = False
            
        q = (is_irred == has_no_roots)
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: The degree of f is either 2 or 3",
    "¬Q: f is irreducible over F XOR f has no roots in F"
]

N_HYP = 2
NEG_Q_INDEX = 2