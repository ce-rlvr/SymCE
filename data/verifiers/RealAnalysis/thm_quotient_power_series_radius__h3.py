import sympy
from sympy.abc import x

def conditions(witness) -> list[bool]:
    """
    Given a witness tuple (f, g) representing two expressions in x,
    checks if they satisfy the hypotheses and falsify the conclusion.
    """
    try:
        # Witness should be a tuple or list of two expressions: (f(x), g(x))
        if len(witness) != 2:
            return [False, False, False]
        f, g = witness
    except Exception:
        return [False, False, False]

    def is_analytic_at_zero(expr):
        """
        Checks if the given expression is analytic at x = 0.
        An expression is analytic at 0 if its Taylor/Maclaurin series 
        has no negative powers, fractional powers, or logarithmic singularities.
        """
        try:
            expr = sympy.sympify(expr)
            
            # Reject undefined or infinite expressions
            if expr.has(sympy.nan) or expr.has(sympy.oo) or expr.has(-sympy.oo) or expr.has(sympy.zoo):
                return False
            
            free_syms = list(expr.free_symbols)
            # If it's a constant (no free symbols), it's analytic everywhere
            if not free_syms:
                return True
                
            # Prefer 'x' if present, otherwise pick the first free symbol
            if x in free_syms:
                sym = x
            else:
                sym = free_syms[0]
                
            # Compute the series expansion around 0 up to order 6
            s = expr.series(sym, 0, 6)
            
            # Remove the Big-O term to get the truncated polynomial
            p = s.removeO()
            
            # If it's a valid power series, the truncated series must be a polynomial
            return bool(p.is_polynomial(sym))
        except Exception:
            return False

    # Check Hypothesis 1: f(x) is a power series with R_1 > 0
    try:
        h1 = is_analytic_at_zero(f)
    except Exception:
        h1 = False

    # Check Hypothesis 2: g(x) is a power series with R_2 > 0
    try:
        h2 = is_analytic_at_zero(g)
    except Exception:
        h2 = False

    # Check Negated Conclusion: f(x)/g(x) does NOT have a strictly positive radius of convergence
    try:
        f_sym = sympy.sympify(f)
        g_sym = sympy.sympify(g)
        
        # The conclusion is that f/g is a power series with R > 0 (i.e., analytic at 0).
        # We want the conclusion to FAIL, so neg_q is True if f/g is NOT analytic at 0.
        q = is_analytic_at_zero(f_sym / g_sym)
        neg_q = not q
    except Exception:
        # If division or evaluation fails entirely, it's definitely not a valid power series
        neg_q = True

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f(x) is a power series with radius of convergence R_1 > 0",
    "H_2: g(x) is a power series with radius of convergence R_2 > 0",
    "¬Q: The formal quotient series f(x)/g(x) does not have a strictly positive radius of convergence"
]

N_HYP = 2
NEG_Q_INDEX = 2