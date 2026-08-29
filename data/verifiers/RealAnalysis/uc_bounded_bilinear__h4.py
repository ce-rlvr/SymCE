import sympy
from sympy import Interval, FiniteSet, Union, oo, S

# Top-level setup: named object bindings that the witness expression may reference
x, y = sympy.symbols('x y', real=True)
Reals = S.Reals

CONDITION_LABELS = [
    "H_1: X, Y, and Z are normed vector spaces",
    "H_2: B is a bounded bilinear operator",
    "H_3: S_X is a bounded subset of X",
    "¬Q: The restriction of B to S_X x S_Y is not uniformly continuous"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness) -> list[bool]:
    try:
        X = witness.get('X')
        Y = witness.get('Y')
        Z = witness.get('Z')
        B = witness.get('B')
        S_X = witness.get('S_X')
        S_Y = witness.get('S_Y')
    except Exception:
        return [False, False, False, False]
        
    # H_1: X, Y, and Z are normed vector spaces
    try:
        valid_spaces = ('R', S.Reals, 'R^1', 'R1')
        h1 = bool(X in valid_spaces and Y in valid_spaces and Z in valid_spaces)
    except Exception:
        h1 = False

    # H_2: B is a bounded bilinear operator
    try:
        B_expr = B(x, y) if callable(B) else B
        
        if hasattr(B_expr, 'free_symbols'):
            free_syms = list(B_expr.free_symbols)
            if len(free_syms) == 0:
                is_bilinear = (B_expr == 0)
                c = 0
            elif len(free_syms) == 1:
                is_bilinear = False
                c = 0
            elif len(free_syms) == 2:
                v1, v2 = free_syms
                is_bilinear = (
                    sympy.diff(B_expr, v1, 2) == 0 and 
                    sympy.diff(B_expr, v2, 2) == 0 and 
                    B_expr.subs(v1, 0) == 0 and 
                    B_expr.subs(v2, 0) == 0
                )
                c = B_expr.subs({v1: 1, v2: 1})
            else:
                is_bilinear = False
                c = 0
        else:
            is_bilinear = False
            c = 0
            
        h2 = bool(is_bilinear and (c == 0 or getattr(c, 'is_real', True) is not False))
    except Exception:
        h2 = False

    # Convert tuples/lists to Intervals for convenience
    try:
        if isinstance(S_X, (list, tuple)) and len(S_X) == 2:
            S_X = Interval(S_X[0], S_X[1])
        if isinstance(S_Y, (list, tuple)) and len(S_Y) == 2:
            S_Y = Interval(S_Y[0], S_Y[1])
    except Exception:
        pass

    # H_3: S_X is a bounded subset of X
    try:
        h3 = bool(S_X.inf.is_finite and S_X.sup.is_finite)
    except Exception:
        h3 = False

    # ¬Q: The restriction of B to S_X x S_Y is not uniformly continuous
    try:
        c_nonzero = (c != 0)
        sx_not_singleton = (S_X.inf != S_X.sup) and (getattr(S_X, 'is_empty', False) is not True)
        
        try:
            sy_inf_finite = S_Y.inf.is_finite
            sy_sup_finite = S_Y.sup.is_finite
            sy_unbounded = not (sy_inf_finite and sy_sup_finite)
        except Exception:
            sy_unbounded = False
            
        neg_q = bool(c_nonzero and sx_not_singleton and sy_unbounded)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]