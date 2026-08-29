import sympy
from sympy.abc import x, y
import math

def conditions(witness):
    try:
        if len(witness) != 3:
            return [False, False, False]
        q_raw, N_raw, E_expr = witness
        if not isinstance(q_raw, (int, sympy.Integer)):
            return [False, False, False]
        if not isinstance(N_raw, (int, sympy.Integer)):
            return [False, False, False]
        q = int(q_raw)
        N = int(N_raw)
    except Exception:
        return [False, False, False]
        
    # H_1: F_q is a finite field with q elements
    try:
        if q < 2:
            h1 = False
        else:
            factors = sympy.ntheory.factorint(q)
            h1 = (len(factors) == 1)
    except Exception:
        h1 = False

    # H_2: N is the number of F_q-rational points on E, including the point at infinity
    try:
        if not sympy.isprime(q) or q == 2:
            # For simplicity and speed, we only verify point counts over prime fields of odd characteristic
            h2 = False
        else:
            from sympy import Poly, Eq
            
            if isinstance(E_expr, Eq):
                E_expr = E_expr.lhs - E_expr.rhs
                
            if isinstance(E_expr, str):
                E_expr = sympy.sympify(E_expr)
                
            symbols = list(E_expr.free_symbols)
            if len(symbols) > 2:
                h2 = False
            else:
                if len(symbols) == 1:
                    E_expr = y**2 - E_expr.subs(symbols[0], x)
                elif len(symbols) == 2:
                    if x not in symbols and y not in symbols:
                        E_expr = E_expr.subs({symbols[0]: x, symbols[1]: y})
                    elif x in symbols and y not in symbols:
                        other = [s for s in symbols if s != x][0]
                        E_expr = E_expr.subs(other, y)
                    elif y in symbols and x not in symbols:
                        other = [s for s in symbols if s != y][0]
                        E_expr = E_expr.subs(other, x)
                        
                E_poly = Poly(E_expr, x, y)
                
                if E_poly.is_zero or E_poly.total_degree() < 1:
                    h2 = False
                else:
                    affine_pts = 0
                    optimized = False
                    
                    # Fast path for curves of the form c2*y^2 + P(x) = 0
                    if E_poly.degree(y) == 2:
                        E_poly_y = Poly(E_expr, y)
                        coeffs = E_poly_y.all_coeffs()
                        if len(coeffs) == 3:
                            c2, c1, c0 = coeffs
                            if c1 == 0 and c2.is_Integer:
                                c2_val = int(c2) % q
                                if c2_val != 0:
                                    inv_c2 = pow(c2_val, -1, q)
                                    P_expr_opt = -c0 * inv_c2
                                    P_poly_opt = Poly(P_expr_opt, x)
                                    for i in range(q):
                                        val = P_poly_opt.eval(i) % q
                                        if val == 0:
                                            affine_pts += 1
                                        else:
                                            leg = sympy.ntheory.legendre_symbol(val, q)
                                            if leg == 1:
                                                affine_pts += 2
                                    optimized = True

                    # Fallback for general plane curves
                    if not optimized:
                        for i in range(q):
                            for j in range(q):
                                if E_poly.eval({x: i, y: j}) % q == 0:
                                    affine_pts += 1
                                    
                    # Points at infinity (solutions to the highest degree homogeneous part)
                    d = E_poly.total_degree()
                    terms = E_poly.terms()
                    highest_terms = [t for t in terms if sum(t[0]) == d]
                    
                    pts_inf = 0
                    Y_d_coeff = sum(coeff for (deg_x, deg_y), coeff in highest_terms if deg_y == d)
                    if Y_d_coeff % q == 0:
                        pts_inf += 1
                        
                    for y_val in range(q):
                        val = sum(coeff * (1**deg_x) * (y_val**deg_y) for (deg_x, deg_y), coeff in highest_terms)
                        if val % q == 0:
                            pts_inf += 1
                            
                    total_pts = affine_pts + pts_inf
                    h2 = (N == total_pts)
    except Exception:
        h2 = False

    # ¬Q: The number of points N violates the Hasse-Weil bound
    try:
        neg_q = abs(N - (q + 1)) > 2 * math.sqrt(q)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F_q is a finite field with q elements",
    "H_2: N is the number of F_q-rational points on E, including the point at infinity",
    "¬Q: The number of points N violates the Hasse-Weil bound (|N - (q + 1)| > 2√q)"
]

N_HYP = 2
NEG_Q_INDEX = 2