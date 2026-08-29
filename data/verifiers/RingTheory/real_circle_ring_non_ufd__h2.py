import sympy
from sympy import symbols, Poly, factor_list, degree, sympify

x, y = symbols('x y')

def conditions(witness):
    try:
        expr = sympify(witness)
        if not hasattr(expr, 'free_symbols'):
            h1 = False
        elif not expr.free_symbols.issubset({x, y}):
            h1 = False
        else:
            Poly(expr, x, y)
            h1 = True
    except Exception:
        h1 = False

    try:
        f = sympify(witness)
        
        is_integral_domain = True
        if f == 0:
            is_integral_domain = True
        else:
            try:
                factored = factor_list(f)
                if len(factored[1]) > 1:
                    is_integral_domain = False
                elif len(factored[1]) == 1 and factored[1][0][1] > 1:
                    is_integral_domain = False
                elif len(factored[1]) == 0:
                    is_integral_domain = False
            except Exception:
                is_integral_domain = False

        is_ufd = False
        if f == 0:
            is_ufd = True
        elif is_integral_domain:
            try:
                deg_x = degree(f, x)
                deg_y = degree(f, y)
                
                if deg_x == 0 or deg_y == 0:
                    is_ufd = True
                elif deg_x == 1:
                    p_x = Poly(f, x)
                    coeffs = p_x.all_coeffs()
                    A = coeffs[0]
                    B = coeffs[1] if len(coeffs) > 1 else 0
                    if Poly(A, y).is_constant():
                        is_ufd = True
                    elif Poly(B, y).is_constant() and B != 0:
                        is_ufd = True
                
                if not is_ufd and deg_y == 1:
                    p_y = Poly(f, y)
                    coeffs = p_y.all_coeffs()
                    A = coeffs[0]
                    B = coeffs[1] if len(coeffs) > 1 else 0
                    if Poly(A, x).is_constant():
                        is_ufd = True
                    elif Poly(B, x).is_constant() and B != 0:
                        is_ufd = True
                        
                if not is_ufd:
                    p = Poly(f, (x, y))
                    if p.total_degree() == 2:
                        A = p.coeff_monomial(x**2)
                        B = p.coeff_monomial(x*y)
                        C = p.coeff_monomial(y**2)
                        if B**2 - 4*A*C >= 0:
                            is_ufd = True
            except Exception:
                pass

        neg_q = (not is_integral_domain) or is_ufd
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = ["H_1: witness is a polynomial in x and y", "¬Q: R mod witness is not an integral domain or is a UFD"]
N_HYP = 1
NEG_Q_INDEX = 1