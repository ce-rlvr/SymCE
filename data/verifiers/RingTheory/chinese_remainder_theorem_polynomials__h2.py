import sympy as sp
from sympy.abc import x, y, z

QQ = sp.QQ
ZZ = sp.ZZ
CC = sp.CC
RR = sp.RR

def conditions(witness):
    try:
        F, p1, p2 = witness
        p1 = sp.sympify(p1)
        p2 = sp.sympify(p2)
    except Exception:
        return [False, False, False]
    
    try:
        h1 = F.is_Field
        if h1 is None:
            h1 = False
        else:
            h1 = bool(h1)
    except Exception:
        h1 = False
        
    try:
        try:
            g = sp.gcd(p1, p2, domain=F)
        except Exception:
            g = sp.gcd(p1, p2)
        h2 = bool(g.is_number and g != 0)
    except Exception:
        h2 = False
        
    try:
        gens = list(p1.free_symbols | p2.free_symbols)
        if not gens:
            is_coprime = not (p1 == 0 and p2 == 0)
        else:
            gens = sorted(gens, key=lambda s: s.name)
            gb = sp.groebner([p1, p2], *gens, domain=F)
            is_coprime = (len(gb) == 1 and gb[0].is_number and gb[0] != 0)
        neg_q = not is_coprime
    except Exception:
        neg_q = True
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: p_1 and p_2 are relatively prime",
    "¬Q: Factor ring over p_1 p_2 is not isomorphic to product of factor rings"
]

N_HYP = 2
NEG_Q_INDEX = 2