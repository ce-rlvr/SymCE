import sympy
from sympy import Poly
from sympy.abc import x, y, z

Z = sympy.ZZ
Q = sympy.QQ

def conditions(witness):
    res = [False, False, False, False]
    
    try:
        if not isinstance(witness, Poly):
            witness = Poly(witness)
    except Exception:
        pass

    try:
        if isinstance(witness, Poly):
            res[0] = True
            if len(witness.gens) == 1:
                res[1] = True
    except Exception:
        pass

    try:
        if res[1]:
            if witness.degree() >= 1:
                res[2] = True
    except Exception:
        pass

    try:
        if res[1] and res[2]:
            domain = witness.domain
            LC = witness.LC()
            
            is_unit = False
            if domain.is_Field:
                is_unit = (LC != domain.zero)
            elif domain == sympy.ZZ:
                is_unit = (LC == domain.one or LC == -domain.one)
            else:
                try:
                    q = domain.exquo(domain.one, LC)
                    if q * LC == domain.one:
                        is_unit = True
                except Exception:
                    pass
            
            res[3] = not is_unit
    except Exception:
        pass

    return res

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: f is a polynomial over R",
    "H_3: The degree of f is at least 1",
    "¬Q: The factor ring is not a free R-module of rank n"
]

N_HYP = 3
NEG_Q_INDEX = 3