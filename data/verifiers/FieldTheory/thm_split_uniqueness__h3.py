import sympy
from sympy import QQ, Poly, factor_list
from sympy.polys.numberfields import primitive_element
from sympy.abc import x
import math

def conditions(witness) -> list[bool]:
    try:
        F, f, K_1, K_2 = witness
    except Exception:
        return [False, False, False, False]
        
    # H1: F is a field
    try:
        h1 = getattr(F, 'is_Field', False)
    except Exception:
        h1 = False
        
    # H2: f is a non-constant polynomial over F
    try:
        if isinstance(f, Poly):
            poly_f = f
        else:
            syms = getattr(f, 'free_symbols', set())
            gen = list(syms)[0] if syms else x
            poly_f = Poly(f, gen, domain=F)
        h2 = poly_f.degree() > 0
    except Exception:
        h2 = False
        
    # H3: K_2 is a splitting field of f over F
    try:
        h3 = False
        if F == QQ and getattr(K_2, 'is_Field', False):
            ext2 = getattr(K_2, 'ext', None)
            expr_f = poly_f.as_expr()
            
            if ext2 is not None:
                facs = factor_list(expr_f, extension=ext2)
            else:
                facs = factor_list(expr_f)
            
            splits_completely = all(fac.degree() == 1 for fac, mult in facs[1])
            
            if splits_completely:
                if ext2 is None:
                    h3 = True
                else:
                    try:
                        roots = poly_f.all_roots()
                        non_rat_roots = [r for r in roots if not r.is_rational]
                        if not non_rat_roots:
                            exact_deg = 1
                        else:
                            _, minpoly = primitive_element(non_rat_roots, domain=QQ)
                            exact_deg = minpoly.degree()
                        
                        if K_2.mod.degree() == exact_deg:
                            h3 = True
                    except Exception:
                        if K_2.mod.degree() <= math.factorial(poly_f.degree()):
                            h3 = True
    except Exception:
        h3 = False
        
    # neg_Q: K_1 is NOT isomorphic to K_2 over F
    try:
        neg_q = False
        if not getattr(K_1, 'is_Field', False):
            neg_q = True
        elif F == QQ:
            if K_1 == K_2:
                neg_q = False
            else:
                ext1 = getattr(K_1, 'ext', None)
                ext2 = getattr(K_2, 'ext', None)
                
                if (ext1 is None) != (ext2 is None):
                    neg_q = True
                elif ext1 is None and ext2 is None:
                    neg_q = True
                else:
                    if K_1.mod.degree() != K_2.mod.degree():
                        neg_q = True
                    else:
                        expr_mod = K_1.mod.as_expr()
                        facs = factor_list(expr_mod, extension=ext2)
                        has_root = any(fac.degree() == 1 for fac, mult in facs[1])
                        neg_q = not has_root
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: f is a non-constant polynomial over F",
    "H_3: K_2 is a splitting field of f over F",
    "¬Q: K_1 is not isomorphic to K_2 over F"
]

N_HYP = 3
NEG_Q_INDEX = 3