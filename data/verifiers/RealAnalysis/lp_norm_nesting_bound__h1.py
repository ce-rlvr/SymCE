import sympy
import math
from sympy import Symbol, Abs, integrate, oo

# Top-level setup
x = Symbol('x', real=True)

def conditions(witness):
    """
    Given a witness tuple (f, a, b, p, q), checks if it is a valid counterexample
    to the L_p Norm Nesting Bound on Finite Intervals.
    """
    try:
        f, a, b, p, q = witness
    except Exception:
        return [False, False, False]
        
    # Parse the function expression
    try:
        if callable(f):
            f_expr = f(x)
        else:
            f_expr = sympy.sympify(f)
            free_syms = f_expr.free_symbols
            if len(free_syms) == 1:
                sym = list(free_syms)[0]
                f_expr = f_expr.subs(sym, x)
    except Exception:
        return [False, False, False]

    # H_1: a < b
    try:
        a_sym = sympy.sympify(a)
        b_sym = sympy.sympify(b)
        h1 = bool(a_sym < b_sym)
    except Exception:
        h1 = False

    # H_2: p and q are real numbers such that 0 < p < q
    try:
        p_sym = sympy.sympify(p)
        q_sym = sympy.sympify(q)
        h2 = bool(0 < p_sym) and bool(p_sym < q_sym)
    except Exception:
        h2 = False

    # ¬Q: The conclusion fails (LHS > RHS or undefined such that LHS <= RHS is false)
    try:
        int_p = integrate(Abs(f_expr)**p_sym, (x, a_sym, b_sym))
        int_q = integrate(Abs(f_expr)**q_sym, (x, a_sym, b_sym))
        
        lhs = (int_p / (b_sym - a_sym))**(1/p_sym)
        rhs = (int_q / (b_sym - a_sym))**(1/q_sym)
        
        try:
            if lhs.is_number and rhs.is_number:
                lhs_f = float(lhs.evalf())
                rhs_f = float(rhs.evalf())
                if math.isinf(lhs_f) or math.isinf(rhs_f) or math.isnan(lhs_f) or math.isnan(rhs_f):
                    neg_q = not (lhs_f <= rhs_f)
                else:
                    # Use rounding to prevent false positives from floating point inaccuracies
                    neg_q = round(lhs_f, 10) > round(rhs_f, 10)
            else:
                neg_q = not bool(lhs <= rhs)
        except Exception:
            neg_q = not bool(lhs <= rhs)
            
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: a < b",
    "H_2: p and q are real numbers such that 0 < p < q",
    "¬Q: L_p norm is not less than or equal to L_q norm"
]

N_HYP = 2
NEG_Q_INDEX = 2