import sympy
from sympy import minpoly, degree, factor, Mul, Pow
from sympy.abc import x
from sympy.polys import primitive_element

CONDITION_LABELS = [
    "H_1: f(x) = x^3 - 5 is in Q polynomials",
    "¬Q: Degree of K over Q is not 6 or K is not Q(cbrt(5), sqrt(-3))"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        if hasattr(witness, 'ext'):
            prim = witness.ext
        elif isinstance(witness, (list, tuple)):
            prim, _ = primitive_element(witness, x)
        else:
            prim = witness
            
        minpoly(prim, x)
        h1_ok = True
    except Exception:
        h1_ok = False

    try:
        if hasattr(witness, 'ext'):
            prim = witness.ext
        elif isinstance(witness, (list, tuple)):
            prim, _ = primitive_element(witness, x)
        else:
            prim = witness
            
        poly = minpoly(prim, x)
        deg = degree(poly, x)
        
        if deg != 6:
            neg_q_ok = True
        else:
            f1 = factor(x**3 - 5, extension=prim)
            f2 = factor(x**2 + 3, extension=prim)
            
            def has_linear_factor(poly_expr, var):
                if not poly_expr.has(var):
                    return False
                if isinstance(poly_expr, Mul):
                    factors = poly_expr.args
                else:
                    factors = [poly_expr]
                for f in factors:
                    if not f.has(var):
                        continue
                    if isinstance(f, Pow):
                        base = f.args[0]
                        if degree(base, var) == 1:
                            return True
                    else:
                        if degree(f, var) == 1:
                            return True
                return False
            
            has_root_3 = has_linear_factor(f1, x)
            has_root_2 = has_linear_factor(f2, x)
            
            is_K = has_root_3 and has_root_2
            neg_q_ok = not is_K
            
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]