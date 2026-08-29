import sympy as sp

# Top-level setup
x = sp.Symbol('x', positive=True)
t = sp.Symbol('t', positive=True)

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    """
    # H_1: f is a strictly positive measurable function on (0, oo)
    try:
        f = sp.sympify(witness)
        h1 = True
        # Check positivity at a few sample points in (0, oo)
        for val in [0.01, 0.1, 0.5, 1, 2, 5, 10, 100]:
            val_eval = f.subs(x, val).evalf()
            if val_eval.is_real == False:
                h1 = False
                break
            try:
                if bool(val_eval <= 0):
                    h1 = False
                    break
            except TypeError:
                h1 = False
                break
    except Exception:
        h1 = False

    # neg_Q: The conclusion fails (LHS > RHS or the integrals diverge)
    try:
        f = sp.sympify(witness)
        f_t = f.subs(x, t)
        
        # Evaluate the inner integral: \int_0^x \ln f(t) dt
        ln_f = sp.log(f_t)
        inner_int = sp.integrate(ln_f, (t, 0, x))
        
        # Evaluate the left-hand side integral
        left_integrand = sp.exp(inner_int / x)
        left_side = sp.integrate(left_integrand, (x, 0, sp.oo))
        
        # Evaluate the right-hand side integral
        right_side = sp.E * sp.integrate(f, (x, 0, sp.oo))
        
        # The inequality fails if it evaluates to strictly greater, or if the integrals diverge
        # (since the standard inequality implicitly asserts the integrals converge to finite real numbers).
        if left_side in [sp.oo, -sp.oo, sp.zoo] or right_side in [sp.oo, -sp.oo, sp.zoo]:
            neg_q = True
        elif left_side.has(sp.nan) or right_side.has(sp.nan):
            neg_q = True
        else:
            try:
                ls_val = float(left_side.evalf())
            except Exception:
                ls_val = -1.0
            try:
                rs_val = float(right_side.evalf())
            except Exception:
                rs_val = float('inf')
            
            neg_q = ls_val > rs_val
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: f is a strictly positive measurable function on (0, oo)",
    "¬Q: The inequality fails (e.g. LHS > RHS or integrals diverge)"
]

N_HYP = 1
NEG_Q_INDEX = 1