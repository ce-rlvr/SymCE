import sympy

x = sympy.Symbol('x')

CONDITION_LABELS = ['H_1: F is a field', 'not Q: factor ring is zero ring iff resultant is non-zero']

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                f, g = witness
            elif len(witness) == 3:
                _, f, g = witness
            else:
                return [False, False]
        else:
            return [False, False]
    except Exception:
        return [False, False]
    
    try:
        p_f = sympy.Poly(f, x)
        p_g = sympy.Poly(g, x)
        h1 = True
    except Exception:
        h1 = False

    try:
        d = sympy.gcd(f, g)
        p_d = sympy.Poly(d, x)
        is_zero_ring = (p_d.degree() <= 0 and not p_d.is_zero)
        
        try:
            res = sympy.resultant(f, g, x)
        except Exception:
            if p_f.is_zero or p_g.is_zero:
                res = 0
            elif p_f.degree() <= 0 and p_g.degree() <= 0:
                res = 1
            else:
                res = 0
                
        res_not_zero = (res != 0)
        
        neg_q = bool(is_zero_ring != res_not_zero)
    except Exception:
        neg_q = False

    return [h1, neg_q]