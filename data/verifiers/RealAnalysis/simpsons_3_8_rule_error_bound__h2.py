import sympy

x = sympy.Symbol('x')

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion
    for the Simpson's 3/8 Rule Error Bound conjecture.
    
    Witness is expected to be a tuple (f_expr, a, b, M).
    """
    try:
        if len(witness) == 4:
            f_expr, a, b, M = witness
        else:
            return [False, False]

        f_expr = sympy.sympify(f_expr)
        a = sympy.sympify(a)
        b = sympy.sympify(b)
        M = sympy.sympify(M)

        # H_1: f is a four times continuously differentiable real-valued function on the interval
        h1_ok = False
        try:
            if a.is_real and b.is_real and M.is_real and bool(a < b):
                # Check if 4th derivative can be computed
                f4 = sympy.diff(f_expr, x, 4)
                v_a = f_expr.subs(x, a)
                v_b = f_expr.subs(x, b)
                if v_a.is_real is not False and v_b.is_real is not False:
                    h1_ok = True
        except Exception:
            h1_ok = False

        # ¬Q: The error of Simpson's 3/8 rule exceeds the bound
        neg_q_ok = False
        try:
            h = (b - a) / sympy.Integer(3)
            exact_val = sympy.integrate(f_expr, (x, a, b))
            approx_val = sympy.Integer(3) * h / sympy.Integer(8) * (
                f_expr.subs(x, a) + 
                sympy.Integer(3) * f_expr.subs(x, a + h) + 
                sympy.Integer(3) * f_expr.subs(x, a + sympy.Integer(2) * h) + 
                f_expr.subs(x, b)
            )
            
            error = abs(exact_val - approx_val)
            bound = sympy.Integer(3) * M * h**5 / sympy.Integer(80)
            
            if error.is_number and bound.is_number:
                if error.evalf() > bound.evalf():
                    neg_q_ok = True
            else:
                diff = error - bound
                if diff.is_positive:
                    neg_q_ok = True
        except Exception:
            neg_q_ok = False

        return [h1_ok, neg_q_ok]
    except Exception:
        return [False, False]

CONDITION_LABELS = ["H_1: f is a four times continuously differentiable real-valued function on the interval", "not Q: The error of Simpsons rule exceeds the bound"]

N_HYP = 1
NEG_Q_INDEX = 1