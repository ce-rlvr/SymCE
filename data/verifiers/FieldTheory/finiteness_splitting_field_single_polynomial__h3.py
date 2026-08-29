import sympy
from sympy import Poly
from sympy.polys.domains import QQ, RR, CC, ZZ
from sympy.abc import x, y, z

def conditions(witness):
    try:
        F, f, E = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = bool(getattr(F, 'is_Field', False))
    except Exception:
        h1 = False
        
    try:
        free_syms = getattr(f, 'free_symbols', set())
        if len(free_syms) > 1:
            h2 = False
        else:
            sym = list(free_syms)[0] if free_syms else x
            poly_f = Poly(f, sym)
            h2 = True
            for c in poly_f.coeffs():
                try:
                    F.from_sympy(c)
                except Exception:
                    h2 = False
                    break
    except Exception:
        h2 = False
        
    try:
        def is_fin_dim(E, F):
            if E == F:
                return True
            if getattr(E, 'is_PolynomialRing', False) or getattr(E, 'is_FractionField', False):
                if E.domain == F:
                    return False
            if getattr(F, 'name', None) == 'QQ':
                if getattr(E, 'name', None) in ('RR', 'CC', 'RR_mpmath', 'CC_mpmath'):
                    return False
                if hasattr(E, 'ext'):
                    return True
            if getattr(F, 'name', None) in ('RR', 'RR_mpmath'):
                if getattr(E, 'name', None) in ('CC', 'CC_mpmath'):
                    return True
            if getattr(F, 'is_FiniteField', False) and getattr(E, 'is_FiniteField', False):
                if E.characteristic == F.characteristic:
                    return True
            return False
            
        neg_q = not is_fin_dim(E, F)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: f is a polynomial over F",
    "¬Q: E is not a finite-dimensional vector space over F"
]

N_HYP = 2
NEG_Q_INDEX = 2