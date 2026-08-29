import sympy
from sympy import Symbol
from sympy.polys.domains import QQ, ZZ, RR, CC
from sympy.polys.domains import FractionField, AlgebraicField

x = Symbol('x')
y = Symbol('y')
z = Symbol('z')

CONDITION_LABELS = [
    "H_1: L/K is a separable extension",
    "¬Q: The trace pairing is not a non-degenerate symmetric bilinear form"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    # Duck-typing for mock objects
    try:
        if hasattr(witness, 'is_separable') and hasattr(witness, 'is_finite'):
            h1 = bool(witness.is_separable)
            neg_q = not bool(witness.is_finite)
            return [h1, neg_q]
    except Exception:
        pass

    try:
        L, K = witness
    except Exception:
        return [False, False]
    
    h1 = False
    try:
        if getattr(L, 'is_Field', False) and getattr(K, 'is_Field', False):
            is_sub = False
            if L == K:
                is_sub = True
            elif getattr(L, 'domain', None) == K:
                is_sub = True
            elif isinstance(L, FractionField):
                ring = getattr(L, 'ring', None)
                if getattr(ring, 'domain', None) == K:
                    is_sub = True
            
            if is_sub:
                char = getattr(K, 'characteristic', None)
                if callable(char):
                    try:
                        char = char()
                    except Exception:
                        char = None
                if char == 0:
                    h1 = True
                elif isinstance(L, FractionField):
                    h1 = True
    except Exception:
        pass

    neg_q = False
    try:
        if isinstance(L, FractionField):
            neg_q = True
        elif isinstance(L, AlgebraicField):
            neg_q = False
        elif L == K:
            neg_q = False
        else:
            # If it's an unknown extension type, assume it's infinite or trace is undefined
            neg_q = True
    except Exception:
        pass

    return [h1, neg_q]