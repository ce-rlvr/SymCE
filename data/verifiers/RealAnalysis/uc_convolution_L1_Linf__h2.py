import sympy
from sympy import Piecewise, And, oo, Abs, limit, diff, Integral

# Top-level setup: named object bindings that the witness expression may reference.
x = sympy.Symbol('x', real=True)
y = sympy.Symbol('y', real=True)

def is_unbounded(lim):
    """Helper to check if a limit evaluates to infinity or an unbounded accumulation."""
    if lim == oo or lim == -oo:
        return True
    if isinstance(lim, sympy.AccumBounds):
        if lim.min == -oo or lim.max == oo:
            return True
    return False

def conditions(witness) -> list[bool]:
    try:
        # The witness should be a tuple of two sympy expressions (f, g) in terms of x.
        f, g = witness
    except Exception:
        return [False, False]
        
    # H_1: f is in L^1(R)
    try:
        integral_f = sympy.integrate(Abs(f), (x, -oo, oo))
        if integral_f.has(Integral):
            # Fallback: try integrating without Abs if SymPy struggles (assumes f is non-negative)
            integral_f = sympy.integrate(f, (x, -oo, oo))
            
        if integral_f.has(Integral):
            h1_ok = False
        else:
            h1_ok = bool(integral_f.is_finite) or (integral_f.is_number and bool(integral_f < oo))
    except Exception:
        h1_ok = False
        
    # ¬Q: The convolution f * g is NOT bounded OR NOT uniformly continuous on R
    try:
        t = sympy.Symbol('t', real=True)
        f_t = f.subs(x, t)
        g_yt = g.subs(x, y - t)
        
        # Compute the convolution h(y) = (f * g)(y)
        h = sympy.integrate(f_t * g_yt, (t, -oo, oo))
        
        if h.has(Integral):
            # If the integral cannot be evaluated, we cannot verify the condition
            neg_q = False
        else:
            # Check if h is bounded by evaluating limits at infinity
            lim_inf = sympy.limit(h, y, oo)
            lim_minf = sympy.limit(h, y, -oo)
            
            if is_unbounded(lim_inf) or is_unbounded(lim_minf):
                neg_q = True
            else:
                # If bounded, check uniform continuity by checking if the derivative is bounded
                dh = sympy.diff(h, y)
                lim_dh_inf = sympy.limit(dh, y, oo)
                lim_dh_minf = sympy.limit(dh, y, -oo)
                
                if is_unbounded(lim_dh_inf) or is_unbounded(lim_dh_minf):
                    neg_q = True
                else:
                    neg_q = False
    except Exception:
        neg_q = False
        
    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: f is a Lebesgue integrable function on R",
    "¬Q: The convolution f * g is NOT bounded or NOT uniformly continuous on R"
]

N_HYP = 1
NEG_Q_INDEX = 1