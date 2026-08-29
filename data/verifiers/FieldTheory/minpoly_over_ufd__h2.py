import sympy
from sympy import Poly

# Top-level setup for witness expressions
x, y, z = sympy.symbols('x y z')
ZZ = sympy.ZZ
QQ = sympy.QQ

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "H_2: E is a field extension of F",
    "H_3: alpha in E is integral over R",
    "¬Q: The minimal polynomial of alpha over F does not have all its coefficients in R"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        R = witness['R']
        F = witness['F']
        E = witness.get('E', F)
        alpha = witness['alpha']
        poly_R_expr = witness['poly_R']
        minpoly_F_expr = witness['minpoly_F']
    except Exception:
        return [False, False, False, False]

    def in_domain(expr, domain):
        if hasattr(domain, 'from_sympy'):
            try:
                domain.from_sympy(sympy.sympify(expr))
                return True
            except Exception:
                pass
        try:
            if expr in domain:
                return True
        except Exception:
            pass
        return False

    # H_1: R is a Unique Factorization Domain
    try:
        h1_ok = bool(getattr(R, 'is_UFD', False))
    except Exception:
        h1_ok = False

    # H_2: E is a field extension of F
    try:
        # We verify that both F and E are fields.
        h2_ok = bool(getattr(F, 'is_Field', False) and getattr(E, 'is_Field', False))
    except Exception:
        h2_ok = False

    # H_3: alpha in E is integral over R
    try:
        if isinstance(poly_R_expr, Poly):
            poly_R = poly_R_expr
        else:
            try:
                poly_R = Poly(poly_R_expr)
            except Exception:
                poly_R = Poly(poly_R_expr, sympy.Symbol('x'))
        
        is_monic = (poly_R.LC() == 1)
        coeffs_in_R = all(in_domain(c, R) for c in poly_R.coeffs())
        
        val = poly_R.as_expr().subs(poly_R.gen, alpha)
        is_root = (sympy.simplify(val) == 0)
        
        alpha_in_E = in_domain(alpha, E)
        
        h3_ok = bool(is_monic and coeffs_in_R and is_root and alpha_in_E)
    except Exception:
        h3_ok = False

    # ¬Q: The minimal polynomial of alpha over F does not have all its coefficients in R
    try:
        if isinstance(minpoly_F_expr, Poly):
            minpoly_F = minpoly_F_expr
        else:
            try:
                minpoly_F = Poly(minpoly_F_expr)
            except Exception:
                minpoly_F = Poly(minpoly_F_expr, sympy.Symbol('x'))
            
        is_min_monic = (minpoly_F.LC() == 1)
        coeffs_in_F = all(in_domain(c, F) for c in minpoly_F.coeffs())
        
        val_min = minpoly_F.as_expr().subs(minpoly_F.gen, alpha)
        is_min_root = (sympy.simplify(val_min) == 0)
        
        # To robustly verify it is the minimal polynomial without complex irreducibility checks,
        # we require the witness to provide a degree 1 polynomial over F.
        is_deg_1 = (minpoly_F.degree() == 1)
        
        is_minpoly = is_min_monic and coeffs_in_F and is_min_root and is_deg_1
        
        coeffs_in_R_min = all(in_domain(c, R) for c in minpoly_F.coeffs())
        
        neg_q_ok = bool(is_minpoly and not coeffs_in_R_min)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]