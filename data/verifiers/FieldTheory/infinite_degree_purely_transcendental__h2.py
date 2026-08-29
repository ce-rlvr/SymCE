import sympy
from sympy import QQ, RR, CC, sqrt, I, pi, sympify, Dummy, minpoly
from sympy.abc import x, y, z, t

CONDITION_LABELS = [
    "H_1: L is a field extension of K containing t",
    "¬Q: K(t) is of finite degree over K"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                K, L, t_val = witness
            elif len(witness) == 2:
                K, t_val = witness
                try:
                    d = Dummy('d')
                    minpoly(t_val, d, domain=K)
                    # If minpoly succeeds, t_val is algebraic over K
                    try:
                        L = K.algebraic_field(t_val)
                    except Exception:
                        L = K
                except Exception:
                    # If minpoly fails, t_val is likely transcendental
                    try:
                        L = K.frac_field(t_val)
                    except Exception:
                        L = K
            else:
                return [False, False]
        else:
            return [False, False]
    except Exception:
        return [False, False]

    try:
        t_val = sympify(t_val)
    except Exception:
        pass

    # H_1: L is a field extension of K containing t
    h1 = False
    try:
        if getattr(K, 'is_Field', False) and getattr(L, 'is_Field', False):
            # Check if K is a subfield of L
            if K.unify(L) == L:
                # Check if t is an element of L
                try:
                    L.from_sympy(t_val)
                    h1 = True
                except Exception:
                    if t_val in L:
                        h1 = True
    except Exception:
        pass

    # ¬Q: K(t) is of finite degree over K (i.e. t is algebraic over K)
    neg_q = False
    try:
        d = Dummy('d')
        p = minpoly(t_val, d, domain=K)
        if p is not None:
            neg_q = True
    except Exception:
        pass

    return [h1, neg_q]