import sympy
from sympy.abc import x

QQ = sympy.QQ
ZZ = sympy.ZZ

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                F, p, f = witness
            elif len(witness) == 2:
                p, f = witness
                F = QQ
            else:
                return [False, False, False]
        else:
            return [False, False, False]
            
        p = sympy.sympify(p)
        f = sympy.sympify(f)
    except Exception:
        return [False, False, False]

    try:
        H1 = bool(getattr(F, 'is_Field', False))
    except Exception:
        H1 = False

    try:
        gens = list(p.free_symbols | f.free_symbols)
        if not gens:
            gens = [x]
        else:
            gens = sorted(gens, key=lambda s: s.name)
        p_poly = sympy.Poly(p, *gens, domain=F)
        H2 = not p_poly.is_ground
    except Exception:
        H2 = False

    try:
        if not gens:
            gens = [x]
        else:
            gens = sorted(gens, key=lambda s: s.name)
            
        f_poly = sympy.Poly(f, *gens, domain=F)
        p_poly = sympy.Poly(p, *gens, domain=F)
        
        gcd_poly = f_poly.gcd(p_poly)
        is_coprime = gcd_poly.is_ground
        
        basis = sympy.groebner([f, p], *gens, domain=F)
        is_unit = False
        for b in basis:
            if sympy.Poly(b, *gens, domain=F).is_ground and b != 0:
                is_unit = True
                break
            
        neg_Q = bool(is_unit != is_coprime)
    except Exception:
        neg_Q = False

    return [H1, H2, neg_Q]

CONDITION_LABELS = [
    'H_1: F is a field',
    'H_2: p is a non-constant polynomial',
    'not Q: equivalence fails'
]

N_HYP = 2
NEG_Q_INDEX = 2