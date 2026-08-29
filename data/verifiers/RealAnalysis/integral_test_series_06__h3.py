import sympy
from sympy import Symbol, Interval, oo, Sum, Integral

# Top-level setup: define the variable that the witness expression will use
x = Symbol('x', real=True)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    """
    # H1: f is a positive real-valued function on [1, \infty)
    h1 = False
    try:
        h1_num = True
        # Check a dense grid of points in [1, 100)
        for i in range(10, 1000):
            try:
                val = float(witness.subs(x, i / 10.0).evalf())
                if val <= 0:
                    h1_num = False
                    break
            except TypeError:
                # If it evaluates to a complex number, float() raises TypeError
                h1_num = False
                break
        
        # Check some large values to ensure it remains positive
        if h1_num:
            for i in [10**4, 10**5, 10**6]:
                try:
                    val = float(witness.subs(x, i).evalf())
                    if val <= 0:
                        h1_num = False
                        break
                except TypeError:
                    h1_num = False
                    break
        h1 = h1_num
    except Exception:
        h1 = False

    # H2: f is continuous on [1, \infty)
    h2 = False
    try:
        from sympy.calculus.util import continuous_domain
        dom = continuous_domain(witness, x, Interval(1, oo))
        if dom == Interval(1, oo):
            h2 = True
    except Exception:
        pass

    if not h2:
        try:
            # Fallback: if continuous_domain fails, check if denominator has roots in [1, oo)
            # We avoid doing this for Piecewise functions as they may have jump discontinuities
            if not witness.has(sympy.Piecewise):
                n_expr, d_expr = witness.as_numer_denom()
                roots = sympy.solveset(d_expr, x, domain=Interval(1, oo))
                if roots == sympy.EmptySet:
                    h2 = True
        except Exception:
            pass

    # neg_Q: The series converges if and only if the integral converges is FALSE
    neg_q = False
    try:
        n_sym = Symbol('n', integer=True, positive=True)
        f_n = witness.subs(x, n_sym)
        
        # Check series convergence
        series_conv = None
        sum_expr = Sum(f_n, (n_sym, 1, oo))
        
        try:
            c = sum_expr.is_convergent()
            if c is not None:
                series_conv = bool(c)
        except Exception:
            pass
            
        if series_conv is None:
            try:
                val = sum_expr.doit()
                if val.is_finite:
                    series_conv = True
                elif val in [oo, -oo]:
                    series_conv = False
            except Exception:
                pass

        # Check integral convergence
        integral_conv = None
        int_expr = Integral(witness, (x, 1, oo))
        
        try:
            c = int_expr.is_convergent()
            if c is not None:
                integral_conv = bool(c)
        except Exception:
            pass
            
        if integral_conv is None:
            try:
                val = int_expr.doit()
                if val.is_finite:
                    integral_conv = True
                elif val in [oo, -oo]:
                    integral_conv = False
            except Exception:
                pass
                
        # The conclusion fails if one converges and the other diverges
        if series_conv is not None and integral_conv is not None:
            neg_q = (series_conv != integral_conv)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f is a positive real-valued function on [1, \\infty)",
    "H_2: f is continuous on [1, \\infty)",
    "¬Q: The series converges if and only if the integral converges is FALSE"
]

N_HYP = 2
NEG_Q_INDEX = 2