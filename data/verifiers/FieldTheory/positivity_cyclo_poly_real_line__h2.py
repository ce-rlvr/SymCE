import sympy
from sympy.polys import cyclotomic_poly

def conditions(witness):
    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            x = witness.get('x')
        else:
            n, x = witness
    except Exception:
        return [False, False, False]
        
    # H1: n >= 3 is an integer
    try:
        n_sym = sympy.sympify(n)
        h1 = bool(n_sym.is_integer and n_sym >= 3)
    except Exception:
        h1 = False
        
    # H2: x is a real number
    try:
        x_val = sympy.sympify(x)
        h2 = x_val.is_real
        if h2 is None:
            h2 = bool(sympy.im(x_val) == 0)
        h2 = bool(h2)
    except Exception:
        h2 = False
        
    # neg_Q: \Phi_n(x) <= 0
    try:
        t = sympy.Symbol('t')
        n_int = int(n_sym)
        poly = cyclotomic_poly(n_int, t)
        val = poly.subs(t, x_val)
        # Evaluate the condition that the conclusion fails
        neg_q = bool(val <= 0)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n >= 3 is an integer",
    "H_2: x is a real number",
    "¬Q: \Phi_n(x) <= 0"
]

N_HYP = 2
NEG_Q_INDEX = 2