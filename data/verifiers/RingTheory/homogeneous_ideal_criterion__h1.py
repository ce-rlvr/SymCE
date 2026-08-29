import sympy
from sympy import Poly, groebner
from sympy.abc import a, b, c, x, y, z, t, u, v, w

def conditions(witness):
    try:
        if hasattr(witness, 'gens'):
            gens = witness.gens
        elif isinstance(witness, (list, tuple)):
            gens = witness
        else:
            return [False, False]
            
        if not gens:
            return [False, False]
            
        symbols = set()
        for p in gens:
            symbols.update(sympy.sympify(p).free_symbols)
        symbols = sorted(list(symbols), key=lambda s: s.name)
        
        h1 = True
    except Exception:
        return [False, False]
        
    try:
        if not symbols:
            is_hom_ideal = True
            given_hom = True
        else:
            polys = [Poly(p, *symbols) for p in gens]
            given_hom = all(p.is_homogeneous for p in polys)
            
            gb = groebner(gens, *symbols, order='grevlex')
            is_hom_ideal = all(Poly(p, *symbols).is_homogeneous for p in gb)
            
        q = (is_hom_ideal == given_hom)
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: I is an ideal in the polynomial ring",
    "¬Q: I is a homogeneous ideal but the given generators are not homogeneous"
]

N_HYP = 1
NEG_Q_INDEX = 1