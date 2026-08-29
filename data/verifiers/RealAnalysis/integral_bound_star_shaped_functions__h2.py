import sympy as sp
import math

x = sp.Symbol('x', real=True)

def conditions(witness):
    """
    Checks whether the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (f, b) where f is a sympy expression in terms of x
    (or a callable) and b is a strictly positive real number.
    """
    try:
        f, b = witness
        if callable(f):
            f = f(x)
        f = sp.sympify(f)
        b = sp.sympify(b)
    except Exception:
        return [False, False, False]

    # H1: b is a strictly positive real number
    try:
        h1 = bool(b > 0)
    except Exception:
        h1 = False

    # H2: The function g(x) = f(x)/x is monotonically non-decreasing on (0, b]
    try:
        if not h1:
            h2 = False
        else:
            g = f / x
            h2 = True
            b_float = float(b)
            # Check 1000 points in the interval (0, b]
            points = [b_float * i / 1000.0 for i in range(1, 1001)]
            
            val_expr = g.subs(x, points[0]).evalf()
            if val_expr == sp.nan:
                h2 = False
            else:
                prev_val = float(val_expr)
                if math.isnan(prev_val):
                    h2 = False
                else:
                    for p in points[1:]:
                        val_expr = g.subs(x, p).evalf()
                        if val_expr == sp.nan:
                            h2 = False
                            break
                        val = float(val_expr)
                        if math.isnan(val):
                            h2 = False
                            break
                        # Allow a tiny numerical tolerance for flat functions
                        if val < prev_val - 1e-11:
                            h2 = False
                            break
                        prev_val = val
    except Exception:
        h2 = False

    # Negated Conclusion: \int_0^b f(x) dx > \frac{b}{2} f(b)
    try:
        if not h1:
            neg_q = False
        else:
            integral_val = sp.integrate(f, (x, 0, b))
            if isinstance(integral_val, sp.Integral):
                integral_val = integral_val.evalf()
            
            integral_val = sp.sympify(integral_val)
            rhs = sp.sympify((b / 2) * f.subs(x, b))
            
            if integral_val == sp.oo:
                neg_q = True
            elif integral_val == -sp.oo or integral_val == sp.nan:
                neg_q = False
            else:
                diff = integral_val - rhs
                # Try exact symbolic evaluation first
                if hasattr(diff, 'is_positive') and diff.is_positive is True:
                    neg_q = True
                elif hasattr(diff, 'is_nonpositive') and diff.is_nonpositive is True:
                    neg_q = False
                else:
                    # Fallback to numerical evaluation
                    val = diff.evalf()
                    if val == sp.nan:
                        neg_q = False
                    else:
                        val_float = float(val)
                        if math.isnan(val_float):
                            neg_q = False
                        else:
                            neg_q = bool(val_float > 1e-9)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = ['H_1: b is a strictly positive real number', 'H_2: The function g(x) = f(x)/x is monotonically non-decreasing on 0 to b', 'not Q: integral of f(x) from 0 to b > (b/2)*f(b)']
N_HYP = 2
NEG_Q_INDEX = 2