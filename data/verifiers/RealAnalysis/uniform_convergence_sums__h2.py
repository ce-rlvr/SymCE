import sympy
from sympy import Symbol, Interval, oo, Reals, Abs, limit, maximum

# Top-level setup: named object bindings that the witness expression may reference.
x = Symbol('x', real=True)
n = Symbol('n', integer=True, positive=True)

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    The witness should be a tuple: (S, f_n, f, g_n, g)
    where:
      - S is a SymPy set (e.g., Reals, Interval(0, 1))
      - f_n, f, g_n, g are SymPy expressions in terms of x and n
    """
    try:
        S, f_n, f, g_n, g = witness
    except Exception:
        return [False, False]
    
    # H_1: (f_n) converges uniformly to f on S
    try:
        diff_f = Abs(f_n - f)
        sup_f = maximum(diff_f, x, S)
        if sup_f == oo:
            h1_ok = False
        else:
            lim_f = limit(sup_f, n, oo)
            h1_ok = (lim_f == 0)
    except Exception:
        h1_ok = False

    # neg_Q: (f_n + g_n) does NOT converge uniformly to f + g on S
    try:
        diff_fg = Abs((f_n + g_n) - (f + g))
        sup_fg = maximum(diff_fg, x, S)
        if sup_fg == oo:
            neg_q_ok = True
        else:
            lim_fg = limit(sup_fg, n, oo)
            neg_q_ok = (lim_fg != 0)
    except Exception:
        neg_q_ok = False

    return [bool(h1_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: (f_n) converges uniformly to f on S",
    "¬Q: (f_n + g_n) does not converge uniformly to f + g on S"
]

N_HYP = 1
NEG_Q_INDEX = 1