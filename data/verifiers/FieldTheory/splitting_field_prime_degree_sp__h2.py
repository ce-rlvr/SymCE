import sympy
from sympy import Poly, degree, factor_list, roots
import math

x = sympy.Symbol('x')

def conditions(witness):
    try:
        p, f = witness
    except Exception:
        return [False, False, False]
        
    # H_1: p is a prime number
    try:
        h1 = sympy.isprime(p)
    except Exception:
        h1 = False
        
    # H_2: f(x) has exactly two non-real roots in C
    try:
        f_expr = sympy.sympify(f)
        free_syms = f_expr.free_symbols
        if len(free_syms) == 1:
            var = list(free_syms)[0]
        elif len(free_syms) == 0:
            var = sympy.Symbol('x')
        else:
            raise ValueError("Too many free symbols")
            
        f_poly = Poly(f_expr, var)
        nrts = sympy.nroots(f_poly)
        non_real_count = sum(1 for r in nrts if abs(sympy.im(r)) > 1e-9)
        h2 = (non_real_count == 2)
    except Exception:
        h2 = False
        
    # neg_Q: The Galois group of the splitting field of f(x) over Q is NOT isomorphic to S_p
    try:
        f_expr = sympy.sympify(f)
        free_syms = f_expr.free_symbols
        if len(free_syms) == 1:
            var = list(free_syms)[0]
        else:
            var = sympy.Symbol('x')
            
        f_poly = Poly(f_expr, var)
        facs = factor_list(f_poly)[1]
        if not facs:
            is_Sp = False
        else:
            d_max = max(degree(base, var) for base, exp in facs)
            
            if d_max < p:
                is_Sp = False
            elif len(facs) == 1 and degree(facs[0][0], var) == p:
                is_Sp = True
            else:
                rts = roots(f_poly)
                if sum(rts.values()) == degree(f_poly):
                    alg_roots = [r for r in rts.keys() if not r.is_rational]
                    if not alg_roots:
                        is_Sp = (math.factorial(p) == 1)
                    else:
                        try:
                            from sympy.polys.numberfields import primitive_element
                            minpoly, _ = primitive_element(alg_roots, var, ex=True)
                            deg = degree(minpoly, var)
                            is_Sp = (deg == math.factorial(p))
                        except Exception:
                            is_Sp = False
                else:
                    deg_p_factors = [base for base, exp in facs if degree(base, var) == p]
                    other_factors = [base for base, exp in facs if degree(base, var) != p]
                    if len(deg_p_factors) == 1 and all(degree(base, var) == 1 for base in other_factors):
                        is_Sp = True
                    else:
                        is_Sp = False
                        
        neg_q = not is_Sp
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: f(x) has exactly two non-real roots in C",
    "¬Q: The Galois group of the splitting field of f(x) over Q is not isomorphic to S_p"
]

N_HYP = 2
NEG_Q_INDEX = 2