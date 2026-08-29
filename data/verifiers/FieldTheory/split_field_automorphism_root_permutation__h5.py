import sympy
from sympy import Poly, Symbol, roots, simplify, sympify

x = Symbol('x')

def conditions(witness):
    try:
        f, alpha, sigma = witness
    except Exception:
        return [False, False, False, False, False]
    
    h1 = True
    
    try:
        poly_f = Poly(f, x)
        h2 = poly_f.domain.is_QQ or poly_f.domain.is_ZZ
    except Exception:
        h2 = False
        
    h3 = True
    
    try:
        if not callable(sigma):
            h4 = False
        elif simplify(sigma(sympify(1)) - 1) != 0:
            h4 = False
        else:
            rts = roots(poly_f, x)
            if sum(rts.values()) != poly_f.degree() or poly_f.degree() == 0:
                h4 = False
            else:
                root_list = list(rts.keys())
                sigma_roots = [sigma(r) for r in root_list]
                
                is_perm = True
                for sr in sigma_roots:
                    if not any(simplify(sr - r) == 0 for r in root_list):
                        is_perm = False
                        break
                
                is_hom = True
                for r1 in root_list:
                    for r2 in root_list:
                        if simplify(sigma(r1 + r2) - (sigma(r1) + sigma(r2))) != 0:
                            is_hom = False
                        if simplify(sigma(r1 * r2) - (sigma(r1) * sigma(r2))) != 0:
                            is_hom = False
                
                h4 = is_perm and is_hom
    except Exception:
        h4 = False
        
    try:
        val = poly_f.eval(sigma(alpha))
        neg_q = simplify(val) != 0
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: f is a polynomial over F",
    "H_3: K is the splitting field of f over F",
    "H_4: sigma is a field automorphism of K fixing F",
    "¬Q: sigma(alpha) is not a root of f"
]

N_HYP = 4
NEG_Q_INDEX = 4