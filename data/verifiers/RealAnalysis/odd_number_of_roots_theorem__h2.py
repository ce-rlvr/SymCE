import sympy
from sympy.abc import x

CONDITION_LABELS = ["H_1: f is continuous on the closed interval from a to b", "H_2: The set of roots in the open interval from a to b is finite", "¬Q: The number of roots in the open interval from a to b is not an odd integer"]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        f_val, a, b = witness
        
        # Parse the function expression and identify the variable
        if isinstance(f_val, str):
            f_expr = sympy.sympify(f_val)
            sym = sympy.Symbol('x')
        elif callable(f_val):
            sym = sympy.Symbol('x')
            f_expr = f_val(sym)
        else:
            f_expr = f_val
            if hasattr(f_expr, 'free_symbols'):
                free_syms = f_expr.free_symbols
                if len(free_syms) == 1:
                    sym = list(free_syms)[0]
                elif len(free_syms) == 0:
                    sym = sympy.Symbol('x')
                else:
                    x_sym = sympy.Symbol('x')
                    sym = x_sym if x_sym in free_syms else list(free_syms)[0]
            else:
                f_expr = sympy.sympify(f_val)
                sym = sympy.Symbol('x')
                
        # Parse the interval bounds
        a_sym = sympy.sympify(a)
        b_sym = sympy.sympify(b)
        a_val = float(a_sym)
        b_val = float(b_sym)
        valid_interval = (a_val < b_val)
    except Exception:
        return [False, False, False]

    # H_1: f is continuous on the closed interval from a to b
    try:
        if not valid_interval:
            h1 = False
        else:
            from sympy.calculus.util import continuous_domain
            from sympy import Interval
            domain = continuous_domain(f_expr, sym, Interval(a_sym, b_sym))
            h1 = (domain == Interval(a_sym, b_sym))
    except Exception:
        h1 = False

    # H_2: The set of roots in the open interval from a to b is finite
    try:
        if not valid_interval:
            h2 = False
        else:
            from sympy import solveset, Interval
            roots = solveset(f_expr, sym, domain=Interval.open(a_sym, b_sym))
            h2 = roots.is_FiniteSet
            if h2 is None:
                h2 = False
    except Exception:
        h2 = False

    # ¬Q: The number of roots in the open interval from a to b is not an odd integer
    try:
        if h2 and valid_interval:
            num_roots = len(roots)
            neg_q = (num_roots % 2 == 0)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]