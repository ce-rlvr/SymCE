import sympy
import math
import itertools
import functools

# Top-level setup
# No specific named groups or matrices are required for this Real Analysis conjecture.

CONDITION_LABELS = [
    "H_1: c is a non-zero real number",
    "H_2: L is a real number",
    "¬Q: L is a subsequential limit of (c x_n) if and only if L/c is a subsequential limit of (x_n) FAILS"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        c, L, x = witness
    except Exception:
        return [False, False, False]
        
    # H1: c is a non-zero real number
    try:
        if hasattr(c, 'is_real') and c.is_real is not None:
            h1 = bool(c.is_real and c.is_nonzero)
        else:
            h1 = isinstance(c, (int, float)) and float(c) != 0.0
    except Exception:
        h1 = False
        
    # H2: L is a real number
    try:
        if hasattr(L, 'is_real') and L.is_real is not None:
            h2 = bool(L.is_real)
        else:
            h2 = isinstance(L, (int, float))
    except Exception:
        h2 = False
        
    # neg_Q: The conclusion fails
    try:
        # Compute the sequence c * x
        try:
            if isinstance(x, list):
                c_x = [c * v for v in x]
            elif isinstance(x, tuple):
                c_x = tuple(c * v for v in x)
            elif isinstance(x, set):
                c_x = {c * v for v in x}
            else:
                try:
                    c_x = c * x
                except Exception:
                    if callable(x):
                        c_x = lambda n: c * x(n)
                    else:
                        c_x = []
        except Exception:
            c_x = []

        def get_vals(seq):
            if isinstance(seq, (list, tuple, set)):
                return list(seq)
            if hasattr(seq, 'free_symbols'):
                if len(seq.free_symbols) == 1:
                    n = list(seq.free_symbols)[0]
                    return [seq.subs(n, i) for i in range(1, 101)]
                elif len(seq.free_symbols) == 0:
                    return [seq]
            if callable(seq):
                return [seq(i) for i in range(1, 101)]
            return []

        vals_x = get_vals(x)
        vals_cx = get_vals(c_x)

        def is_in(val, vals):
            # Fast checks first
            for v in vals:
                try:
                    if v == val: 
                        return True
                except Exception: 
                    pass
                try:
                    if abs(float(v) - float(val)) < 1e-9: 
                        return True
                except Exception: 
                    pass
            # Fallback to symbolic equality
            for v in vals:
                try:
                    if sympy.simplify(v - val) == 0: 
                        return True
                except Exception: 
                    pass
            return False

        P = is_in(L, vals_cx)
        
        try:
            L_c = L / c
        except Exception:
            L_c = None
            
        if L_c is not None:
            Q = is_in(L_c, vals_x)
        else:
            Q = False
            
        neg_q = (P != Q)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]