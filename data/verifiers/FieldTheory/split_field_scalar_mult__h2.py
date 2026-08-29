import sympy
from sympy import Poly, QQ, RR, CC, ZZ, Rational, AlgebraicField, sqrt, I
from sympy.abc import x, y, z

def is_field(F):
    if hasattr(F, 'is_Field') and F.is_Field:
        return True
    if F in [QQ, RR, CC]:
        return True
    return False

def is_nonzero_in_F(c, F):
    if c == 0:
        return False
    try:
        if hasattr(F, '__contains__'):
            return c in F
    except Exception:
        pass
    try:
        F.to_sympy(c)
        return True
    except Exception:
        pass
    return True

def is_splitting_field(K, f, F):
    try:
        if not is_field(K):
            return False
        if not is_field(F):
            return False
        
        if isinstance(f, Poly):
            f_expr = f.as_expr()
        else:
            f_expr = f
            
        if hasattr(f_expr, 'free_symbols'):
            free_syms = list(f_expr.free_symbols)
            if len(free_syms) == 1:
                poly_K = Poly(f_expr, free_syms[0], domain=K)
            else:
                poly_K = Poly(f_expr, domain=K)
        else:
            poly_K = Poly(f_expr, domain=K)
            
        if poly_K.is_zero:
            return K == F
            
        roots = poly_K.ground_roots()
        
        if sum(roots.values()) != poly_K.degree():
            return False
            
        if F == QQ:
            irrational_roots = []
            for r in roots.keys():
                if r not in QQ:
                    irrational_roots.append(r)
            if not irrational_roots:
                expected_K = QQ
            else:
                expected_K = QQ.algebraic_field(*irrational_roots)
            if K != expected_K:
                return False
        else:
            pass
            
        return True
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            F = witness.get('F')
            c = witness.get('c')
            f = witness.get('f')
            K = witness.get('K')
        else:
            F, c, f, K = witness
    except Exception:
        return [False, False, False, False]

    try:
        h1 = is_field(F)
    except Exception:
        h1 = False

    try:
        h2 = is_nonzero_in_F(c, F)
    except Exception:
        h2 = False

    try:
        h3 = is_splitting_field(K, f, F)
    except Exception:
        h3 = False

    try:
        if isinstance(f, Poly):
            cf = c * f.as_expr()
        else:
            cf = c * f
        q = is_splitting_field(K, cf, F)
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: c is a non-zero element of F",
    "H_3: K is the splitting field of f(x) over F",
    "¬Q: K is not the splitting field of the polynomial c * f(x) over F"
]

N_HYP = 3
NEG_Q_INDEX = 3