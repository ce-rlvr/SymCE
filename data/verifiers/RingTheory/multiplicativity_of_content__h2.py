import sympy
from sympy import Poly, ZZ, QQ
from sympy.abc import x, y, z

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    neg_Q = False
    
    try:
        if isinstance(witness, (tuple, list)):
            if len(witness) == 3:
                R, f, g = witness
            elif len(witness) == 2:
                f, g = witness
                R = None
            else:
                return [False, False, False]
        elif isinstance(witness, dict):
            R = witness.get('R', None)
            f = witness.get('f', None)
            g = witness.get('g', None)
            if f is None or g is None:
                return [False, False, False]
        else:
            return [False, False, False]
            
        if R is not None:
            if R == 'ZZ' or R == ZZ:
                domain = ZZ
            elif R == 'QQ' or R == QQ:
                domain = QQ
            else:
                domain = R
        else:
            poly_g_infer = Poly(g, x)
            domain = poly_g_infer.domain
            
        h1 = bool(domain.is_UFD)
    except Exception:
        h1 = False

    try:
        poly_g = Poly(g, x, domain=domain)
        h2 = not poly_g.is_zero
    except Exception:
        h2 = False

    try:
        poly_f = Poly(f, x, domain=domain)
        poly_fg = Poly(f*g, x, domain=domain)
        
        c_f = poly_f.content()
        c_g = poly_g.content()
        c_fg = poly_fg.content()
        
        prod = c_f * c_g
        
        def are_associated(a, b, dom):
            try:
                a_dom = dom.from_sympy(a)
                b_dom = dom.from_sympy(b)
            except Exception:
                return False
                
            if a_dom == dom.zero and b_dom == dom.zero:
                return True
            if a_dom == dom.zero or b_dom == dom.zero:
                return False
            if dom.is_Field:
                return True
            if dom == ZZ:
                return a_dom == b_dom or a_dom == -b_dom
            try:
                q1 = dom.exquo(a_dom, b_dom)
                q2 = dom.exquo(b_dom, a_dom)
                return True
            except Exception:
                return False
                
        Q = are_associated(c_fg, prod, domain)
        neg_Q = not Q
    except Exception:
        neg_Q = True

    return [h1, h2, neg_Q]

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "H_2: g is a non-zero polynomial over R",
    "not_Q: c(fg) is not associated to c(f)c(g) in R"
]

N_HYP = 2
NEG_Q_INDEX = 2