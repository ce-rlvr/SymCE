import sympy
from sympy import Symbol, oo, eye, zeros

# Top-level setup
k = Symbol('k', integer=True, positive=True)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        n, x = witness
    except Exception:
        return [False, False, False]
        
    # H1: n is a positive integer
    try:
        h1_ok = isinstance(n, int) and n > 0
    except Exception:
        h1_ok = False
        
    # H2: (x_k) is a sequence of vectors in R^n
    try:
        if callable(x):
            x_expr = x(k)
        else:
            x_expr = x
            
        if isinstance(x_expr, sympy.Matrix):
            x_list = list(x_expr)
        elif isinstance(x_expr, (list, tuple)):
            x_list = list(x_expr)
        else:
            x_list = [x_expr]
            
        if len(x_list) == n:
            h2_ok = True
            for comp in x_list:
                val = sympy.sympify(comp).subs(k, 1)
                if not val.is_real:
                    h2_ok = False
                    break
        else:
            h2_ok = False
    except Exception:
        h2_ok = False
        x_list = []
        
    # neg_Q: (x_k) does NOT contain a convergent subsequence
    # In R^n, a sequence has no convergent subsequence iff ||x_k|| -> oo as k -> oo.
    try:
        if h2_ok and x_list:
            norm_sq = sympy.simplify(sum(sympy.sympify(comp)**2 for comp in x_list))
            L = sympy.limit(norm_sq, k, sympy.oo)
            neg_q_ok = (L == sympy.oo)
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: (x_k) is a sequence of vectors in R^n",
    "¬Q: (x_k) does not contain a convergent subsequence"
]

N_HYP = 2
NEG_Q_INDEX = 2