import sympy
from sympy import Poly, factor_list, roots
from sympy.abc import x

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            f, g = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    try:
        f_poly = Poly(f, x)
        h1 = f_poly.domain.is_RationalField or f_poly.domain.is_IntegerRing
    except Exception:
        h1 = False
        
    try:
        g_poly = Poly(g, x)
        h2 = g_poly.domain.is_RationalField or g_poly.domain.is_IntegerRing
    except Exception:
        h2 = False
        
    try:
        if not h1 or not h2:
            neg_q = False
        else:
            f_roots = roots(f, x)
            if sum(f_roots.values()) < f_poly.degree():
                neg_q = False
            else:
                exts = []
                for r in f_roots.keys():
                    if not r.is_Rational:
                        if not any(r == e or r == -e for e in exts):
                            exts.append(r)
                
                if g_poly.degree() <= 0:
                    splits = True
                else:
                    if not exts:
                        facs = factor_list(g, x)[1]
                    else:
                        facs = factor_list(g, x, extension=exts)[1]
                    splits = all(Poly(fac[0], x).degree() == 1 for fac in facs)
                neg_q = not splits
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: f is a polynomial",
    "H_2: L is the splitting field of f over K",
    "neg_Q: The splitting field of g over K is not contained in L or is not a normal extension"
]

N_HYP = 2
NEG_Q_INDEX = 2