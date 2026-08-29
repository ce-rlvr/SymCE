import sympy
from sympy import Symbol, limit, oo, Sum, S

# Top-level setup: named object bindings that the witness expression may reference.
n = Symbol('n', integer=True, nonnegative=True)

def conditions(witness):
    try:
        a_expr, R, x = witness
    except Exception:
        return [False, False, False]
        
    # H_1: 0 <= R < infinity
    try:
        R_sym = sympy.sympify(R)
        h1 = bool(R_sym >= 0 and R_sym < oo)
    except Exception:
        h1 = False
        
    # H_2: x in R and |x| > R
    try:
        x_sym = sympy.sympify(x)
        h2 = bool(x_sym.is_real is not False and abs(x_sym) > R_sym)
    except Exception:
        h2 = False
        
    # ¬Q: The sequence a_n x^n converges to zero OR the series sum a_n x^n converges
    try:
        if callable(a_expr):
            term = a_expr(n) * (x_sym ** n)
        else:
            term = sympy.sympify(a_expr) * (x_sym ** n)
            
        lim = limit(term, n, oo)
        if lim == 0 or lim.is_zero:
            neg_q = True
        else:
            s = Sum(term, (n, 0, oo))
            conv = s.is_convergent()
            neg_q = (conv is S.true)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: 0 <= R < infinity",
    "H_2: x in R and |x| > R",
    "¬Q: a_n x^n converges to 0 or sum a_n x^n converges"
]

N_HYP = 2
NEG_Q_INDEX = 2