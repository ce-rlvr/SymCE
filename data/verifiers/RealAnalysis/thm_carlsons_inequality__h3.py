import sympy as sp
import math

# Top-level setup
x = sp.Symbol('x', real=True)

def evaluate_integral(expr):
    """
    Evaluates the integral of expr over the real line.
    Tries numerical evaluation first for speed, falls back to symbolic.
    """
    # Try numerical evaluation first
    integ = sp.Integral(expr, (x, -sp.oo, sp.oo))
    val = integ.evalf()
    if not val.has(sp.Integral):
        return float(sp.re(val))
    
    # Fallback to symbolic integration
    sym_val = sp.integrate(expr, (x, -sp.oo, sp.oo))
    if not sym_val.has(sp.Integral):
        return float(sp.re(sym_val.evalf()))
        
    raise ValueError("Could not evaluate integral")

def conditions(witness):
    """
    Checks the hypotheses and the negated conclusion for Carlson's Inequality over R.
    """
    # H1: f is a measurable function
    try:
        if not isinstance(witness, sp.Expr):
            h1 = False
        else:
            free_symbols = witness.free_symbols
            if not free_symbols.issubset({x}):
                h1 = False
            else:
                h1 = True
    except Exception:
        h1 = False

    # H2: f in L^2(R)
    try:
        val_I2 = evaluate_integral(sp.Abs(witness)**2)
        h2 = (not math.isnan(val_I2)) and (val_I2 < float('inf'))
    except Exception:
        h2 = False
        val_I2 = float('nan')

    # Negated Conclusion: ( \int |f| )^4 > pi^2 ( \int |f|^2 ) ( \int x^2 |f|^2 )
    try:
        val_I1 = evaluate_integral(sp.Abs(witness))
        val_I3 = evaluate_integral(x**2 * sp.Abs(witness)**2)
        
        if math.isnan(val_I1) or math.isnan(val_I3) or math.isnan(val_I2):
            neg_q = False
        else:
            lhs = val_I1**4
            rhs = (math.pi**2) * val_I2 * val_I3
            # We check for strict inequality with a small tolerance for float inaccuracies
            neg_q = lhs > rhs + 1e-7
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f is a measurable function",
    "H_2: f is in L^2(R)",
    "¬Q: (\\int |f|)^4 > pi^2 (\\int |f|^2) (\\int x^2 |f|^2)"
]

N_HYP = 2
NEG_Q_INDEX = 2