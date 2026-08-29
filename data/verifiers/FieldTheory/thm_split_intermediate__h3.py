import sympy
from sympy import Poly, QQ
from sympy.abc import x

def in_domain(c, D):
    try:
        D.from_sympy(c)
        return True
    except Exception:
        return False

def is_subfield(D1, D2):
    try:
        if D1 == D2:
            return True
        if D1.unify(D2) == D2:
            return True
    except Exception:
        pass
    return False

def get_roots_in_K(f, K):
    try:
        f_K = Poly(f, domain=K)
        factors = f_K.factor_list()[1]
        roots = []
        for fac, mult in factors:
            if fac.degree() == 1:
                coeffs = fac.all_coeffs()
                r_domain = -coeffs[1] / coeffs[0]
                r_expr = K.to_sympy(r_domain)
                roots.extend([r_expr] * mult)
            else:
                return None
        return roots
    except Exception:
        return None

def conditions(witness):
    if isinstance(witness, dict):
        try:
            F = witness.get('F')
            if F is None:
                F_gens = witness.get('F_gens', [])
                F = QQ.algebraic_field(*F_gens) if F_gens else QQ
        except Exception:
            F = None

        try:
            E = witness.get('E')
            if E is None:
                E_gens = witness.get('E_gens', [])
                E = QQ.algebraic_field(*E_gens) if E_gens else QQ
        except Exception:
            E = None

        try:
            K = witness.get('K')
            if K is None:
                K_gens = witness.get('K_gens', [])
                K = QQ.algebraic_field(*K_gens) if K_gens else QQ
        except Exception:
            K = None

        try:
            f_val = witness.get('f')
            if isinstance(f_val, Poly):
                f = f_val
            else:
                f = Poly(f_val, x)
        except Exception:
            f = None
            
    elif isinstance(witness, (list, tuple)) and len(witness) == 4:
        F_val, f_val, E_val, K_val = witness
        
        try:
            if hasattr(F_val, 'is_Field'):
                F = F_val
            elif isinstance(F_val, (list, tuple)):
                F = QQ.algebraic_field(*F_val) if F_val else QQ
            else:
                F = None
        except Exception:
            F = None
            
        try:
            if hasattr(E_val, 'is_Field'):
                E = E_val
            elif isinstance(E_val, (list, tuple)):
                E = QQ.algebraic_field(*E_val) if E_val else QQ
            else:
                E = None
        except Exception:
            E = None
            
        try:
            if hasattr(K_val, 'is_Field'):
                K = K_val
            elif isinstance(K_val, (list, tuple)):
                K = QQ.algebraic_field(*K_val) if K_val else QQ
            else:
                K = None
        except Exception:
            K = None
            
        try:
            if isinstance(f_val, Poly):
                f = f_val
            else:
                f = Poly(f_val, x)
        except Exception:
            f = None
    else:
        F = E = K = f = None

    try:
        h1 = hasattr(F, 'is_Field') and F.is_Field
    except Exception:
        h1 = False

    try:
        if f is not None and F is not None:
            h2 = all(in_domain(c, F) for c in f.coeffs())
        else:
            h2 = False
    except Exception:
        h2 = False

    try:
        if F is not None and E is not None and K is not None:
            h3 = is_subfield(F, E) and is_subfield(E, K)
        else:
            h3 = False
    except Exception:
        h3 = False

    try:
        if f is not None and E is not None and K is not None:
            roots = get_roots_in_K(f, K)
            if roots is None:
                is_splitting_field = False
            else:
                if roots:
                    E_roots = E.unify(QQ.algebraic_field(*roots))
                else:
                    E_roots = E
                is_splitting_field = is_subfield(K, E_roots) and is_subfield(E_roots, K)
        else:
            is_splitting_field = True
    except Exception:
        is_splitting_field = True

    neg_q = not is_splitting_field

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: f is a polynomial over F",
    "H_3: E is an intermediate field between F and K",
    "¬Q: K is not a splitting field of f over E"
]

N_HYP = 3
NEG_Q_INDEX = 3