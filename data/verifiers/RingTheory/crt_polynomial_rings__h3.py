import sympy as sp
from sympy.abc import x, y, z
from sympy import QQ, ZZ, GF

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (F, f_list, f) or a dictionary with these keys.
    """
    try:
        if isinstance(witness, dict):
            F = witness.get('F')
            f_list = witness.get('f_list')
            f = witness.get('f')
        else:
            F, f_list, f = witness
    except Exception:
        return [False, False, False]

    # H_1: F is a field
    try:
        h1 = hasattr(F, 'is_Field') and bool(F.is_Field)
    except Exception:
        h1 = False

    # H_2: f_1, ..., f_k are pairwise coprime non-constant polynomials over F
    try:
        h2 = True
        if not isinstance(f_list, (list, tuple)) or len(f_list) < 1:
            h2 = False
        else:
            polys = []
            for p in f_list:
                poly_p = sp.Poly(p, x, domain=F)
                if poly_p.degree() < 1:
                    h2 = False
                polys.append(poly_p)
                
            if h2:
                for i in range(len(polys)):
                    for j in range(i + 1, len(polys)):
                        gcd_poly = polys[i].gcd(polys[j])
                        if gcd_poly.degree() > 0:
                            h2 = False
                            break
                    if not h2:
                        break
    except Exception:
        h2 = False

    # ¬Q: The quotient ring over f is NOT isomorphic to the direct product of quotients over f_i
    try:
        poly_f = sp.Poly(f, x, domain=F)
        
        valid_polys = []
        for p in f_list:
            valid_polys.append(sp.Poly(p, x, domain=F))
            
        if not valid_polys:
            neg_q = False
        else:
            g = valid_polys[0]
            for p in valid_polys[1:]:
                g = g * p
                
            if poly_f.degree() != g.degree():
                neg_q = True
            else:
                fac_f = poly_f.factor_list()
                fac_g = g.factor_list()
                
                deg_mult_f = sorted([(p.degree(), e) for p, e in fac_f[1]])
                deg_mult_g = sorted([(p.degree(), e) for p, e in fac_g[1]])
                
                if deg_mult_f != deg_mult_g:
                    neg_q = True
                else:
                    neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: f_1, ..., f_k are pairwise coprime non-constant polynomials over F",
    "not Q: The quotient ring over f is not isomorphic to the direct product of quotients over f_i"
]

N_HYP = 2
NEG_Q_INDEX = 2