import sympy
import math
import itertools
import functools

def conditions(witness):
    try:
        if isinstance(witness, dict):
            c_star = witness.get('c_star', [])
            x_star = witness.get('x_star', None)
        elif isinstance(witness, tuple) and len(witness) == 2:
            c_star, x_star = witness
        elif isinstance(witness, tuple) and len(witness) == 3:
            _, c_star, x_star = witness
        else:
            c_star, x_star = [], None
            
        if hasattr(c_star, 'tolist'):
            c_star = c_star.tolist()
        elif not isinstance(c_star, (list, tuple)):
            try:
                c_star = list(c_star)
            except TypeError:
                c_star = [c_star]
    except Exception:
        c_star, x_star = [], None

    try:
        h1 = len(c_star) >= 1 and all(sympy.sympify(c).is_real for c in c_star) and x_star is not None and sympy.sympify(x_star).is_real
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            n = len(c_star)
            x = sympy.Symbol('x', real=True)
            P = x**n + sum(sympy.sympify(c) * x**i for i, c in enumerate(c_star))
            P_x = sympy.diff(P, x)
            
            x_val = sympy.sympify(x_star)
            p_val = sympy.simplify(P.subs(x, x_val))
            p_x_val = sympy.simplify(P_x.subs(x, x_val))
            
            try:
                p_val_c = complex(p_val)
                p_x_val_c = complex(p_x_val)
                neg_q = abs(p_val_c) > 1e-12 or abs(p_x_val_c) < 1e-12
            except TypeError:
                neg_q = bool(p_val != 0 or p_x_val == 0)
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = ["H_1: P is a monic polynomial with real coefficients and x_star is real", "¬Q: No continuously differentiable function r exists in a neighborhood of c_star"]
N_HYP = 1
NEG_Q_INDEX = 1