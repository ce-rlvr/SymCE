import sympy
from sympy import Poly
from sympy.abc import x
from sympy.polys.domains import QQ, ZZ, GF

def check_is_root(f, alpha):
    try:
        if isinstance(f, Poly):
            val = f.eval(alpha)
            if val == 0 or val == f.domain.zero:
                return True
            val_expr = f.as_expr().subs(f.gen, alpha)
            if sympy.simplify(val_expr) == 0:
                return True
        else:
            val_expr = f.subs(x, alpha)
            if sympy.simplify(val_expr) == 0:
                return True
    except Exception:
        pass
    return False

def conditions(witness):
    try:
        F, f, alpha = witness
    except Exception:
        return [False, False, False, False]

    # H_1: F is a field
    try:
        h1 = bool(F.is_Field)
    except Exception:
        h1 = False

    # H_2: f is a monic polynomial of degree 3 over F
    try:
        if isinstance(f, Poly):
            f_poly = f
            try:
                domain_ok = (f.domain == F or f.domain.is_subset(F))
            except Exception:
                domain_ok = (f.domain == F)
        else:
            f_poly = Poly(f, x)
            domain_ok = True
            
        is_monic = (f_poly.LC() == 1 or f_poly.LC() == F.one)
        is_deg3 = (f_poly.degree() == 3)
        
        h2 = bool(domain_ok and is_deg3 and is_monic)
    except Exception:
        h2 = False

    # H_3: alpha is a root of f in some extension field of F
    try:
        h3 = check_is_root(f, alpha)
    except Exception:
        h3 = False

    # ¬Q: f is not the minimal polynomial of alpha over F
    try:
        if isinstance(f, Poly):
            f_poly = f
        else:
            f_poly = Poly(f, x)
            
        is_monic = (f_poly.LC() == 1 or f_poly.LC() == F.one)
        is_root = check_is_root(f, alpha)
        
        if isinstance(f, Poly) and f.domain == F:
            is_irred = bool(f.is_irreducible)
        else:
            f_F = Poly(f_poly, domain=F)
            is_irred = bool(f_F.is_irreducible)
            
        is_min_poly = is_monic and is_root and is_irred
        neg_q = not is_min_poly
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: f is a monic polynomial of degree 3 over F",
    "H_3: alpha is a root of f in some extension field of F",
    "¬Q: f is not the minimal polynomial of alpha over F"
]

N_HYP = 3
NEG_Q_INDEX = 3