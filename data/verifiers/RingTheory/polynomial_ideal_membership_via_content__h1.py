import functools
from sympy import symbols, groebner, reduced, gcd, sympify

x, y, z, t = symbols('x y z t')

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, dict):
            return [False, False, False]
            
        vars_ = witness.get('vars', [])
        I_gens_raw = witness.get('I_gens', [])
        f_coeffs_raw = witness.get('f_coeffs', [])
        domain = witness.get('domain', 'ZZ')
        
        h1 = isinstance(I_gens_raw, list)
        h2 = isinstance(f_coeffs_raw, list) and len(f_coeffs_raw) > 0
        
        if not (h1 and h2):
            return [h1, h2, False]
            
        I_gens = [sympify(g) for g in I_gens_raw]
        f_coeffs = [sympify(c) for c in f_coeffs_raw]
            
        def in_ideal(p, gens, vs, dom):
            if p in gens:
                return True
            if not gens:
                return p == 0
            if not vs:
                if dom == 'ZZ':
                    g = functools.reduce(gcd, gens)
                    if g == 0:
                        return p == 0
                    return p % g == 0
                else:
                    if any(g != 0 for g in gens):
                        return True
                    return p == 0
            gb = groebner(gens, *vs, domain=dom)
            _, rem = reduced(p, list(gb), *vs, domain=dom)
            return rem == 0

        P = all(in_ideal(c, I_gens, vars_, domain) for c in f_coeffs)
        c_f = functools.reduce(gcd, f_coeffs)
        Q = in_ideal(c_f, I_gens, vars_, domain)
        
        neg_q = bool(P != Q)
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: I is an ideal of R",
    "H_2: f is a polynomial",
    "not Q: f in I is not equivalent to c_f subseteq I"
]

N_HYP = 2
NEG_Q_INDEX = 2