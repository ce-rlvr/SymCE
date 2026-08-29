import sympy
from sympy import Symbol, oo, Min, Abs, limit, S

# Top-level setup: named object bindings that the witness expression may reference.
n = Symbol('n', integer=True, nonnegative=True)

def radius_of_convergence(expr, n_sym):
    expr = sympy.sympify(expr)
    if expr.is_zero or expr == 0:
        return sympy.oo
    
    # Try ratio test
    try:
        ratio = sympy.Abs(expr / expr.subs(n_sym, n_sym + 1))
        L = sympy.limit(ratio, n_sym, sympy.oo)
        if not L.has(sympy.Limit) and not L.has(sympy.nan) and not L.has(sympy.zoo):
            return L
    except Exception:
        pass
        
    # Try root test
    try:
        root = sympy.Abs(expr)**(1/n_sym)
        lim_root = sympy.limit(root, n_sym, sympy.oo)
        if lim_root == 0:
            return sympy.oo
        elif lim_root == sympy.oo:
            return sympy.S(0)
        else:
            L = 1 / lim_root
            if not L.has(sympy.Limit) and not L.has(sympy.nan) and not L.has(sympy.zoo):
                return L
    except Exception:
        pass
        
    raise ValueError(f"Could not compute radius of convergence for {expr}")

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) >= 2:
            a_n_obj = witness[0]
            b_n_obj = witness[1]
        else:
            return [False, False, False]
            
        if callable(a_n_obj):
            a_n = a_n_obj(n)
        else:
            a_n = a_n_obj
            
        if callable(b_n_obj):
            b_n = b_n_obj(n)
        else:
            b_n = b_n_obj
            
        a_n = sympy.sympify(a_n)
        b_n = sympy.sympify(b_n)
    except Exception:
        return [False, False, False]
        
    # H_1: a_n forms a power series with radius of convergence R_1
    try:
        R1 = radius_of_convergence(a_n, n)
        h1 = True
    except Exception:
        h1 = False
        R1 = None

    # H_2: b_n forms a power series with radius of convergence R_2
    try:
        R2 = radius_of_convergence(b_n, n)
        h2 = True
    except Exception:
        h2 = False
        R2 = None

    # ¬Q: The radius of convergence of the sum series is not exactly min(R_1, R_2)
    try:
        if R1 is not None and R2 is not None:
            R_sum = radius_of_convergence(a_n + b_n, n)
            expected = Min(R1, R2)
            neg_q = bool(R_sum != expected)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: a_n forms a power series with radius of convergence R_1",
    "H_2: b_n forms a power series with radius of convergence R_2",
    "¬Q: The radius of convergence of the sum series is not exactly min(R_1, R_2)"
]

N_HYP = 2
NEG_Q_INDEX = 2