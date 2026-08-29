import sympy
from sympy.abc import x
import math

def conditions(witness) -> list[bool]:
    """
    Checks the hypotheses and the negated conclusion for the Mean Value Theorem 
    for the Error of Simpson's 3/8 Rule.
    
    The witness is expected to be a tuple: (f_expr, a_val, b_val, h_val)
    Example of a valid counterexample (where a >= b): ('x**4', 1, 0, -1/3)
    """
    try:
        if len(witness) != 4:
            return [False, False, False]
        f_raw, a_raw, b_raw, h_raw = witness
        f = sympy.sympify(f_raw, locals={'x': x})
        a = sympy.sympify(a_raw)
        b = sympy.sympify(b_raw)
        h = sympy.sympify(h_raw)
    except Exception:
        return [False, False, False]

    # H_1: f^(4) is continuous on the interval
    h1_ok = True
    try:
        f4 = sympy.diff(f, x, 4)
        if f4.has(sympy.Derivative):
            h1_ok = False
        else:
            a_f = float(a)
            b_f = float(b)
            # Check for continuity by evaluating on a grid
            for i in range(101):
                val = a_f + i * (b_f - a_f) / 100
                res = f4.subs(x, val).evalf()
                if res.is_real is not True:
                    h1_ok = False
                    break
    except Exception:
        h1_ok = False

    # H_2: h = (b - a) / 3
    h2_ok = False
    try:
        diff = sympy.simplify(h - (b - a) / 3)
        if diff == 0:
            h2_ok = True
        else:
            try:
                if abs(float(diff)) < 1e-9:
                    h2_ok = True
            except Exception:
                pass
    except Exception:
        h2_ok = False

    # neg_Q: There does NOT exist c in (a, b) such that the error formula holds
    neg_q_ok = False
    try:
        integral = sympy.integrate(f, (x, a, b))
        if integral.has(sympy.Integral):
            # If sympy cannot compute the integral, we cannot verify the conclusion
            neg_q_ok = False
        else:
            rule = 3 * h / 8 * (f.subs(x, a) + 3 * f.subs(x, a + h) + 3 * f.subs(x, a + 2 * h) + f.subs(x, b))
            error = integral - rule
            
            c = sympy.Symbol('c', real=True)
            rhs = -3 * h**5 / 80 * f4.subs(x, c)
            
            diff_eq = sympy.simplify(error - rhs)
            
            has_solution = False
            is_identically_zero = False
            
            if diff_eq == 0:
                is_identically_zero = True
            elif diff_eq.free_symbols == set():
                try:
                    if abs(float(diff_eq)) < 1e-9:
                        is_identically_zero = True
                except Exception:
                    pass
                    
            if is_identically_zero:
                # If the equation is an identity, a solution exists in (a, b) iff the interval is non-empty
                has_solution = (float(a) < float(b))
            else:
                solutions = sympy.solve(diff_eq, c)
                if isinstance(solutions, list):
                    for sol in solutions:
                        try:
                            if sol.is_real or sol.is_real is None:
                                sol_val = float(sol)
                                # The point c must be strictly between a and b
                                if float(a) < sol_val < float(b):
                                    has_solution = True
                                    break
                        except Exception:
                            pass
            
            # The conclusion fails if NO such c exists
            neg_q_ok = not has_solution
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: f^(4) is continuous on the interval from a to b",
    "H_2: h = (b - a) / 3",
    "not_Q: There does not exist c in (a, b) satisfying the error formula"
]

N_HYP = 2
NEG_Q_INDEX = 2