import sympy
from sympy.abc import x, y, z, t

def conditions(witness) -> list[bool]:
    if not isinstance(witness, dict):
        return [False, False, False, False]

    # H_1: K is an algebraically closed field
    try:
        K = witness.get('K')
        if isinstance(K, str):
            K_upper = K.upper()
            h1 = K_upper in ['C', 'CC', 'COMPLEXES', 'COMPLEX NUMBERS'] or 'ALGEBRAICALLY CLOSED' in K_upper
        else:
            h1 = K == sympy.S.Complexes
    except Exception:
        h1 = False

    # H_2: X and Y are algebraic varieties over K
    try:
        X = witness.get('X')
        Y = witness.get('Y')
        def is_variety(v):
            if isinstance(v, str):
                v_upper = v.upper()
                if 'A' in v_upper and any(c.isdigit() for c in v_upper): return True
                if 'P' in v_upper and any(c.isdigit() for c in v_upper): return True
                if 'VARIETY' in v_upper or 'SPACE' in v_upper: return True
            return False
        h2 = is_variety(X) and is_variety(Y)
    except Exception:
        h2 = False

    # H_3: f: X -> Y is a morphism of varieties
    try:
        f = witness.get('f')
        if isinstance(f, sympy.Expr):
            f = [f]
        
        X = witness.get('X')
        Y = witness.get('Y')
        
        def get_dim(v):
            if isinstance(v, str):
                digits = ''.join(filter(str.isdigit, v))
                if digits:
                    return int(digits)
            return 1
            
        X_dim = get_dim(X)
        Y_dim = get_dim(Y)
        
        if isinstance(f, (list, tuple)) and len(f) == Y_dim:
            free_syms = set()
            for p in f:
                if isinstance(p, sympy.Expr):
                    free_syms.update(p.free_symbols)
            
            if len(free_syms) <= X_dim:
                h3 = True
                for p in f:
                    if not isinstance(p, sympy.Expr):
                        h3 = False
                        break
                    if not p.is_polynomial():
                        h3 = False
                        break
            else:
                h3 = False
        else:
            h3 = False
    except Exception:
        h3 = False

    # ¬Q: The image f(C) is not a constructible set in Y
    try:
        C = witness.get('C')
        f = witness.get('f')
        if isinstance(f, sympy.Expr):
            f = [f]
            
        is_non_constructible = False
        if isinstance(C, str):
            C_upper = C.upper()
            if any(C_upper.startswith(prefix) for prefix in ['Z', 'Q', 'R', 'N', 'INT', 'REAL', 'RAT', 'NAT', 'NON', 'INF', 'COUNT']):
                is_non_constructible = True
        elif C in [sympy.S.Integers, sympy.S.Reals, sympy.S.Naturals, sympy.S.Naturals0, sympy.S.Rationals]:
            is_non_constructible = True
            
        neg_q = False
        if is_non_constructible and isinstance(f, (list, tuple)):
            is_constant = True
            for p in f:
                if isinstance(p, sympy.Expr) and len(sympy.simplify(p).free_symbols) > 0:
                    is_constant = False
                    break
            if not is_constant:
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: K is an algebraically closed field",
    "H_2: X and Y are algebraic varieties over K",
    "H_3: f: X -> Y is a morphism of varieties",
    "¬Q: The image f(C) is not a constructible set in Y"
]

N_HYP = 3
NEG_Q_INDEX = 3