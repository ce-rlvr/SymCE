import sympy
from sympy import Poly, roots, simplify, sympify, QQ
from sympy.abc import x

def in_field(c, F):
    try:
        F.from_sympy(sympify(c))
        return True
    except Exception:
        try:
            F.from_sympy(simplify(c))
            return True
        except Exception:
            return False

def conditions(witness):
    try:
        if isinstance(witness, dict):
            F = witness.get('F')
            x_var = witness.get('x', x)
            if 'f_expr' in witness:
                f_expr = witness['f_expr']
                f_poly = Poly(f_expr, x_var)
            elif 'f' in witness:
                f_poly = witness['f']
                if isinstance(f_poly, Poly):
                    f_expr = f_poly.as_expr()
                    x_var = f_poly.gen
                else:
                    f_expr = f_poly
                    f_poly = Poly(f_expr, x_var)
            else:
                return [False] * 5
            K = witness.get('K')
            alpha = witness.get('alpha')
            sigma = witness.get('sigma')
        elif isinstance(witness, tuple) and len(witness) == 5:
            F, f_val, K, alpha, sigma = witness
            x_var = x
            if isinstance(f_val, Poly):
                f_poly = f_val
                f_expr = f_poly.as_expr()
                x_var = f_poly.gen
            else:
                f_expr = f_val
                f_poly = Poly(f_expr, x_var)
        else:
            return [False] * 5
    except Exception:
        return [False] * 5

    # H1: F is a field
    try:
        h1 = hasattr(F, 'is_Field') and F.is_Field
    except Exception:
        h1 = False

    # H2: f(x) is a polynomial over F
    try:
        h2 = all(in_field(c, F) for c in f_poly.coeffs())
    except Exception:
        h2 = False

    # H3: K is the splitting field of f(x) over F
    try:
        h3 = False
        if hasattr(K, 'is_Field') and K.is_Field:
            subfield_ok = True
            if F != QQ:
                gens = []
                if hasattr(F, 'ext'):
                    if hasattr(F.ext, 'exts'):
                        gens = F.ext.exts
                    elif hasattr(F.ext, 'ext'):
                        gens = [F.ext.ext]
                for g in gens:
                    if not in_field(g, K):
                        subfield_ok = False
                        break
            
            if subfield_ok:
                rts = roots(f_expr, x_var)
                if sum(rts.values()) == f_poly.degree():
                    roots_in_K = all(in_field(r, K) for r in rts)
                    if roots_in_K:
                        if all(in_field(r, F) for r in rts):
                            h3 = (K == F)
                        else:
                            F_gens = []
                            if F != QQ and hasattr(F, 'ext'):
                                if hasattr(F.ext, 'exts'):
                                    F_gens = list(F.ext.exts)
                                elif hasattr(F.ext, 'ext'):
                                    F_gens = [F.ext.ext]
                            expected_gens = F_gens + list(rts.keys())
                            expected_K = QQ.algebraic_field(*expected_gens)
                            h3 = (K == expected_K)
    except Exception:
        h3 = False

    # H4: alpha in K is a root of f(x)
    try:
        h4 = False
        if in_field(alpha, K):
            val = simplify(f_expr.subs(x_var, alpha))
            h4 = (val == 0)
    except Exception:
        h4 = False

    # neg_Q: sigma(alpha) is NOT a root of f(x)
    try:
        neg_q = False
        if callable(sigma):
            sigma_alpha = sigma(alpha)
        elif isinstance(sigma, dict):
            sigma_alpha = alpha.subs(sigma)
        else:
            sigma_alpha = None
            
        if sigma_alpha is not None:
            val = simplify(f_expr.subs(x_var, sigma_alpha))
            neg_q = (val != 0)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(h4), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: f(x) is a polynomial over F",
    "H_3: K is the splitting field of f(x) over F",
    "H_4: alpha in K is a root of f(x)",
    "not Q: sigma(alpha) is not a root of f(x)"
]

N_HYP = 4
NEG_Q_INDEX = 4