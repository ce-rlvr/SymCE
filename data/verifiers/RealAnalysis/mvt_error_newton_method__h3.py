import sympy

x = sympy.Symbol('x', real=True)

def conditions(witness) -> list[bool]:
    try:
        f_expr, r_val, xn_val = witness
        f_expr = sympy.sympify(f_expr)
        r_val = sympy.sympify(r_val)
        xn_val = sympy.sympify(xn_val)
    except Exception:
        return [False, False, False]

    try:
        f_double_prime = f_expr.diff(x, 2)
        h1 = True
    except Exception:
        h1 = False

    try:
        h2 = bool(sympy.simplify(f_expr.subs(x, r_val)) == 0)
    except Exception:
        h2 = False

    try:
        if sympy.simplify(r_val - xn_val) == 0:
            neg_q = True
        else:
            f_prime = f_expr.diff(x)
            f_prime_xn = f_prime.subs(x, xn_val)
            if sympy.simplify(f_prime_xn) == 0:
                neg_q = True
            else:
                f_xn = f_expr.subs(x, xn_val)
                target_val = -2 * (f_prime_xn * (r_val - xn_val) + f_xn) / ((r_val - xn_val)**2)
                eq = f_double_prime - target_val
                sols = sympy.solveset(eq, x, domain=sympy.S.Reals)
                
                lower = min(float(r_val.evalf()), float(xn_val.evalf()))
                upper = max(float(r_val.evalf()), float(xn_val.evalf()))
                
                has_c = False
                if sols.is_FiniteSet:
                    for sol in sols:
                        try:
                            val = float(sol.evalf())
                            if lower < val < upper:
                                has_c = True
                                break
                        except Exception:
                            pass
                else:
                    inter = sympy.Intersection(sols, sympy.Interval.open(lower, upper))
                    if not inter.is_empty:
                        has_c = True
                
                neg_q = not has_c
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f is a twice continuously differentiable function",
    "H_2: r is a root of f such that f(r) = 0",
    "¬Q: There does not exist c strictly between r and x_n satisfying the error formula"
]

N_HYP = 2
NEG_Q_INDEX = 2